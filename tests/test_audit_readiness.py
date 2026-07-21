from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.audit_completeness import load_completeness_policy
from scripts.audit_readiness import evaluate_readiness, main, render_markdown
from scripts.summarize_status import extract_status_records, load_status_policy


READINESS_DOCUMENT = """# Project Readiness

Use this completed record to make a release decision.

| Item | Owner | Target Close Date | Evidence Link | Status |
| --- | --- | --- | --- | --- |
| Protection trip test | Commissioning lead | 2026-07-31 | SAT-017 | Open |
"""

STATUS_POLICY = {
    "allowed_statuses": ["Open", "Closed"],
    "blocking_statuses": [],
    "require_status": True,
}

COMPLETENESS_POLICY = {
    "missing_values": ["TBD", "-"],
    "rules": [
        {
            "name": "Open action control",
            "match": {"columns": ["Status"], "values": ["Open"]},
            "required_fields": [
                {"label": "owner", "columns": ["Owner"]},
                {"label": "deadline", "columns": ["Target Close Date"]},
                {"label": "evidence", "columns": ["Evidence Link"]},
            ],
        }
    ],
}

STATUS_ONLY_DOCUMENT = """# Status-Only Record

This controlled record intentionally has no deadline or completeness match.

| Item | Status |
| --- | --- |
| Archived drawing review | Closed |
"""


class ReadinessGateTests(unittest.TestCase):
    def write_file(self, name: str, content: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / name
        path.write_text(content, encoding="utf-8")
        return path

    def write_document(self, content: str = READINESS_DOCUMENT) -> Path:
        return self.write_file("readiness.md", content)

    def write_policy(self, name: str, document: object) -> Path:
        return self.write_file(name, json.dumps(document))

    def evaluate(
        self,
        content: str = READINESS_DOCUMENT,
        status_document: object = STATUS_POLICY,
        deadline_fail_states: tuple[str, ...] = ("overdue", "missing"),
        additional_documents: tuple[str, ...] = (),
        require_source_coverage: bool = False,
    ) -> dict[str, object]:
        status_path = self.write_policy("status.json", status_document)
        completeness_path = self.write_policy(
            "completeness.json",
            COMPLETENESS_POLICY,
        )
        paths = [self.write_document(content)]
        paths.extend(
            self.write_file(f"additional-{index}.md", document)
            for index, document in enumerate(additional_documents, start=1)
        )
        return evaluate_readiness(
            paths,
            status_policy=load_status_policy(status_path),
            status_policy_source=status_path.as_posix(),
            completeness_policy=load_completeness_policy(completeness_path),
            completeness_policy_source=completeness_path.as_posix(),
            as_of=date(2026, 7, 21),
            deadline_fail_states=deadline_fail_states,
            require_source_coverage=require_source_coverage,
        )

    def test_combined_gate_passes_all_three_controls(self):
        report = self.evaluate()
        self.assertEqual(report["gate"]["result"], "pass")
        self.assertEqual(report["gate"]["finding_count"], 0)
        self.assertEqual(
            {name: check["result"] for name, check in report["checks"].items()},
            {
                "status_policy": "pass",
                "deadlines": "pass",
                "conditional_completeness": "pass",
                "source_coverage": "pass",
            },
        )
        self.assertEqual(report["checks"]["deadlines"]["row_count"], 1)

    def test_status_policy_finding_fails_only_status_check(self):
        status_document = dict(STATUS_POLICY)
        status_document["blocking_statuses"] = ["Open"]
        report = self.evaluate(status_document=status_document)
        self.assertEqual(report["gate"]["failed_checks"], ["status_policy"])
        self.assertEqual(report["checks"]["status_policy"]["finding_count"], 1)

    def test_selected_overdue_deadline_fails_gate(self):
        content = READINESS_DOCUMENT.replace("2026-07-31", "2026-07-20")
        report = self.evaluate(content)
        self.assertEqual(report["gate"]["failed_checks"], ["deadlines"])
        self.assertEqual(report["checks"]["deadlines"]["finding_count"], 1)
        self.assertEqual(
            report["checks"]["deadlines"]["failures"][0]["state"],
            "overdue",
        )

    def test_unselected_deadline_state_does_not_fail_gate(self):
        content = READINESS_DOCUMENT.replace("2026-07-31", "2026-07-21")
        report = self.evaluate(content, deadline_fail_states=("overdue",))
        self.assertEqual(report["checks"]["deadlines"]["state_counts"]["due_today"], 1)
        self.assertEqual(report["gate"]["result"], "pass")

    def test_missing_required_evidence_fails_completeness_check(self):
        content = READINESS_DOCUMENT.replace("SAT-017", "TBD")
        report = self.evaluate(content)
        self.assertEqual(
            report["gate"]["failed_checks"],
            ["conditional_completeness"],
        )
        violation = report["checks"]["conditional_completeness"]["violations"][0]
        self.assertEqual(violation["field"], "evidence")

    def test_markdown_preserves_combined_line_level_findings(self):
        content = READINESS_DOCUMENT.replace("2026-07-31", "2026-07-20").replace(
            "SAT-017",
            "TBD",
        )
        status_document = dict(STATUS_POLICY)
        status_document["blocking_statuses"] = ["Open"]
        report = self.evaluate(content, status_document)
        rendered = render_markdown(report)
        self.assertIn("Gate result: **FAIL**", rendered)
        self.assertIn("| Status policy | FAIL | 1 | 1 |", rendered)
        self.assertIn("| Deadlines | FAIL | 1 | 1 |", rendered)
        self.assertIn("| Conditional completeness | FAIL | 1 | 1 |", rendered)
        self.assertIn("status is blocking", rendered)
        self.assertIn("required field value is missing", rendered)

    def test_generated_combined_report_is_not_reingested(self):
        generated_content = render_markdown(self.evaluate())
        generated = self.write_document(generated_content)
        self.assertEqual(extract_status_records(generated), [])
        strict_report = self.evaluate(
            additional_documents=(generated_content,),
            require_source_coverage=True,
        )
        self.assertEqual(strict_report["checks"]["source_coverage"]["source_count"], 1)
        self.assertEqual(strict_report["checks"]["source_coverage"]["gap_count"], 0)

    def test_source_coverage_reports_partial_file_without_failing_by_default(self):
        report = self.evaluate(additional_documents=(STATUS_ONLY_DOCUMENT,))

        self.assertEqual(report["gate"]["result"], "pass")
        coverage = report["checks"]["source_coverage"]
        self.assertFalse(coverage["required"])
        self.assertEqual(coverage["gap_count"], 2)
        self.assertEqual(coverage["finding_count"], 0)
        partial = next(
            row
            for row in coverage["coverage"]
            if row["source"].endswith("additional-1.md")
        )
        self.assertTrue(partial["status_policy"])
        self.assertFalse(partial["deadlines"])
        self.assertFalse(partial["conditional_completeness"])
        self.assertEqual(
            partial["missing_checks"],
            ["deadlines", "conditional_completeness"],
        )

    def test_required_source_coverage_fails_for_each_missing_control(self):
        report = self.evaluate(
            additional_documents=(STATUS_ONLY_DOCUMENT,),
            require_source_coverage=True,
        )

        self.assertEqual(report["gate"]["failed_checks"], ["source_coverage"])
        self.assertEqual(report["gate"]["finding_count"], 2)
        coverage = report["checks"]["source_coverage"]
        self.assertEqual(coverage["result"], "fail")
        rendered = render_markdown(report)
        self.assertIn("Enforcement: required", rendered)
        self.assertIn("| Source coverage | FAIL | 2 | 2 |", rendered)
        self.assertIn(
            "| yes | no | no | deadlines, conditional_completeness |",
            rendered,
        )

    def test_cli_json_pass_uses_recommended_deadline_failures(self):
        document_path = self.write_document()
        status_path = self.write_policy("status.json", STATUS_POLICY)
        completeness_path = self.write_policy(
            "completeness.json",
            COMPLETENESS_POLICY,
        )
        standard_output = io.StringIO()
        with contextlib.redirect_stdout(standard_output):
            exit_code = main(
                [
                    str(document_path),
                    "--status-policy",
                    str(status_path),
                    "--completeness-policy",
                    str(completeness_path),
                    "--as-of",
                    "2026-07-21",
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(exit_code, 0)
        report = json.loads(standard_output.getvalue())
        self.assertEqual(
            report["configuration"]["deadline_fail_states"],
            ["overdue", "missing"],
        )

    def test_cli_writes_failure_report_and_returns_two(self):
        document_path = self.write_document(
            READINESS_DOCUMENT.replace("SAT-017", "TBD")
        )
        status_path = self.write_policy("status.json", STATUS_POLICY)
        completeness_path = self.write_policy(
            "completeness.json",
            COMPLETENESS_POLICY,
        )
        output_directory = tempfile.TemporaryDirectory()
        self.addCleanup(output_directory.cleanup)
        output_path = Path(output_directory.name) / "reports" / "gate.md"
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main(
                [
                    str(document_path),
                    "--status-policy",
                    str(status_path),
                    "--completeness-policy",
                    str(completeness_path),
                    "--as-of",
                    "2026-07-21",
                    "--output",
                    str(output_path),
                ]
            )
        self.assertEqual(exit_code, 2)
        self.assertTrue(output_path.is_file())
        self.assertIn("conditional_completeness (1)", standard_error.getvalue())

    def test_cli_strict_source_coverage_returns_two_and_reports_gaps(self):
        document_path = self.write_document()
        partial_path = self.write_file("partial.md", STATUS_ONLY_DOCUMENT)
        status_path = self.write_policy("status.json", STATUS_POLICY)
        completeness_path = self.write_policy(
            "completeness.json",
            COMPLETENESS_POLICY,
        )
        standard_output = io.StringIO()
        standard_error = io.StringIO()
        with contextlib.redirect_stdout(standard_output), contextlib.redirect_stderr(
            standard_error
        ):
            exit_code = main(
                [
                    str(document_path),
                    str(partial_path),
                    "--status-policy",
                    str(status_path),
                    "--completeness-policy",
                    str(completeness_path),
                    "--as-of",
                    "2026-07-21",
                    "--require-source-coverage",
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(exit_code, 2)
        report = json.loads(standard_output.getvalue())
        self.assertTrue(report["configuration"]["require_source_coverage"])
        self.assertEqual(report["checks"]["source_coverage"]["gap_count"], 2)
        self.assertIn("source_coverage (2)", standard_error.getvalue())

    def test_cli_returns_one_for_incomplete_input(self):
        no_deadline = READINESS_DOCUMENT.replace("Target Close Date | ", "").replace(
            "2026-07-31 | ",
            "",
        )
        document_path = self.write_document(no_deadline)
        status_path = self.write_policy("status.json", STATUS_POLICY)
        completeness_path = self.write_policy(
            "completeness.json",
            COMPLETENESS_POLICY,
        )
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main(
                [
                    str(document_path),
                    "--status-policy",
                    str(status_path),
                    "--completeness-policy",
                    str(completeness_path),
                    "--as-of",
                    "2026-07-21",
                ]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("no deadline-bearing rows found", standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
