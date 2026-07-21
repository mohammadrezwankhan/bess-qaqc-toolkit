from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_completeness import (
    extract_completeness_results,
    load_completeness_policy,
    main,
    render_markdown,
    summarize_completeness,
)


COMPLETE_DOCUMENT = """# Closeout Actions

Use this register to control commissioning actions.

| ID | Owner | Evidence Link | Target Close Date | Status |
| --- | --- | --- | --- | --- |
| ACT-001 | Commissioning lead | Test record 17 | 2026-08-01 | Open |
| ACT-002 | QA/QC lead | Signed report | 2026-07-20 | Closed |
"""


POLICY_DOCUMENT = {
    "missing_values": ["TBD", "TBC", "N/A", "-"],
    "rules": [
        {
            "name": "Open action control",
            "match": {
                "columns": ["Status", "Review Status"],
                "values": ["Open", "In progress"],
            },
            "required_fields": [
                {
                    "label": "owner",
                    "columns": ["Owner", "Action Owner"],
                },
                {
                    "label": "deadline",
                    "columns": ["Target Close Date", "Due Date"],
                },
                {
                    "label": "evidence",
                    "columns": ["Evidence Link", "Closeout Evidence"],
                },
            ],
        }
    ],
}


class CompletenessAuditTests(unittest.TestCase):
    def write_document(self, content: str = COMPLETE_DOCUMENT) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "readiness.md"
        path.write_text(content, encoding="utf-8")
        return path

    def write_policy(self, document: object = POLICY_DOCUMENT) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "policy.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def test_complete_matching_row_passes_and_unmatched_row_is_skipped(self):
        policy = load_completeness_policy(self.write_policy())
        matches, violations = extract_completeness_results(
            self.write_document(),
            policy,
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].item, "ACT-001")
        self.assertEqual(matches[0].match_value, "Open")
        self.assertEqual(violations, [])

    def test_blank_and_controlled_placeholders_are_violations(self):
        content = COMPLETE_DOCUMENT.replace(
            "| ACT-001 | Commissioning lead | Test record 17 | 2026-08-01 | Open |",
            "| ACT-001 | | TBD | - | open |",
        )
        policy = load_completeness_policy(self.write_policy())
        matches, violations = extract_completeness_results(
            self.write_document(content),
            policy,
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(
            {violation.field for violation in violations},
            {"owner", "deadline", "evidence"},
        )
        self.assertTrue(
            all(
                violation.reason == "required field value is missing"
                for violation in violations
            )
        )

    def test_one_of_column_aliases_can_satisfy_a_required_field(self):
        content = COMPLETE_DOCUMENT.replace("Evidence Link", "Closeout Evidence")
        policy = load_completeness_policy(self.write_policy())
        matches, violations = extract_completeness_results(
            self.write_document(content),
            policy,
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(violations, [])

    def test_absent_required_field_column_is_reported(self):
        content = (
            COMPLETE_DOCUMENT.replace(" | Evidence Link", "")
            .replace(" | Test record 17", "")
            .replace(" | Signed report", "")
        )
        policy = load_completeness_policy(self.write_policy())
        _, violations = extract_completeness_results(
            self.write_document(content),
            policy,
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].field, "evidence")
        self.assertEqual(violations[0].values, ())
        self.assertEqual(
            violations[0].reason,
            "required field column is absent from table",
        )

    def test_ambiguous_match_columns_are_rejected(self):
        content = (
            COMPLETE_DOCUMENT.replace(
                "| ID | Owner | Evidence Link | Target Close Date | Status |",
                "| ID | Owner | Evidence Link | Target Close Date | Status | "
                "Review Status |",
            )
            .replace(
                "| --- | --- | --- | --- | --- |",
                "| --- | --- | --- | --- | --- | --- |",
            )
            .replace(" | Open |", " | Open | Open |")
            .replace(" | Closed |", " | Closed | Closed |")
        )
        policy = load_completeness_policy(self.write_policy())
        with self.assertRaisesRegex(ValueError, "matched multiple columns"):
            extract_completeness_results(self.write_document(content), policy)

    def test_policy_rejects_unknown_fields_and_duplicate_names(self):
        unknown = dict(POLICY_DOCUMENT)
        unknown["unexpected"] = True
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            load_completeness_policy(self.write_policy(unknown))

        duplicate = json.loads(json.dumps(POLICY_DOCUMENT))
        duplicate["rules"].append(json.loads(json.dumps(duplicate["rules"][0])))
        duplicate["rules"][1]["name"] = "open ACTION control"
        with self.assertRaisesRegex(ValueError, "duplicate names"):
            load_completeness_policy(self.write_policy(duplicate))

    def test_policy_rejects_overlapping_required_column_aliases(self):
        document = json.loads(json.dumps(POLICY_DOCUMENT))
        document["rules"][0]["required_fields"][1]["columns"].append("Owner")
        with self.assertRaisesRegex(ValueError, "assigns column"):
            load_completeness_policy(self.write_policy(document))

    def test_generated_report_is_not_reingested(self):
        policy = load_completeness_policy(self.write_policy())
        matches, violations = extract_completeness_results(
            self.write_document(),
            policy,
        )
        summary = summarize_completeness(
            matches,
            violations,
            policy,
            "policy.json",
        )
        generated = self.write_document(render_markdown(summary))
        self.assertEqual(
            extract_completeness_results(generated, policy),
            ([], []),
        )

    def test_summary_and_markdown_keep_line_level_evidence(self):
        content = COMPLETE_DOCUMENT.replace("Test record 17", "TBD")
        policy = load_completeness_policy(self.write_policy())
        matches, violations = extract_completeness_results(
            self.write_document(content),
            policy,
        )
        summary = summarize_completeness(
            matches,
            violations,
            policy,
            "policy.json",
        )
        self.assertEqual(summary["evaluated_row_count"], 1)
        self.assertEqual(summary["violation_count"], 1)
        report = render_markdown(summary)
        self.assertIn("# Readiness Conditional Completeness Audit", report)
        self.assertIn("| ACT-001 | Open action control |", report)
        self.assertIn("required field value is missing", report)

    def test_cli_json_gate_returns_two_for_violations(self):
        content = COMPLETE_DOCUMENT.replace("Test record 17", "TBD")
        document_path = self.write_document(content)
        policy_path = self.write_policy()
        standard_output = io.StringIO()
        standard_error = io.StringIO()
        with (
            contextlib.redirect_stdout(standard_output),
            contextlib.redirect_stderr(standard_error),
        ):
            exit_code = main(
                [
                    str(document_path),
                    "--policy",
                    str(policy_path),
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(exit_code, 2)
        summary = json.loads(standard_output.getvalue())
        self.assertEqual(summary["violation_count"], 1)
        self.assertIn("1 violation", standard_error.getvalue())

    def test_cli_writes_clean_report_and_rejects_no_matches(self):
        document_path = self.write_document()
        policy_path = self.write_policy()
        output_directory = tempfile.TemporaryDirectory()
        self.addCleanup(output_directory.cleanup)
        output_path = Path(output_directory.name) / "reports" / "complete.md"
        self.assertEqual(
            main(
                [
                    str(document_path),
                    "--policy",
                    str(policy_path),
                    "--output",
                    str(output_path),
                ]
            ),
            0,
        )
        self.assertIn(
            "No completeness violations found.",
            output_path.read_text(encoding="utf-8"),
        )

        no_match = self.write_document(COMPLETE_DOCUMENT.replace("Open", "Closed"))
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main([str(no_match), "--policy", str(policy_path)])
        self.assertEqual(exit_code, 1)
        self.assertIn("no rows matched", standard_error.getvalue())

    def test_example_policy_accepts_the_starter_templates(self):
        policy = load_completeness_policy(
            Path("config/readiness-completeness-policy.example.json")
        )
        matches = []
        violations = []
        for path in sorted(Path("templates").glob("*.md")):
            path_matches, path_violations = extract_completeness_results(
                path,
                policy,
            )
            matches.extend(path_matches)
            violations.extend(path_violations)
        self.assertEqual(len(matches), 4)
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
