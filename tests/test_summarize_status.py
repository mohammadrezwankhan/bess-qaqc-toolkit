from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.summarize_status import (
    BLANK_STATUS,
    StatusPolicy,
    evaluate_status_policy,
    extract_status_records,
    load_status_policy,
    main,
    render_markdown,
    summarize_records,
)


STATUS_DOCUMENT = """# Project Readiness

Use this record to track readiness evidence.

| Item | Owner | Status |
| --- | --- | --- |
| Battery racks | QA/QC | Closed |
| Protection test | Commissioning | Blocked |
| Meter record | Grid | |

| Document | Approval Status |
| --- | --- |
| Operating manual | Pending approval |

| Status | Meaning |
| --- | --- |
| Closed | Evidence accepted. |
| Blocked | Release cannot proceed. |
"""


class StatusSummaryTests(unittest.TestCase):
    def write_document(self, content: str = STATUS_DOCUMENT) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "readiness.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_extracts_status_aliases_and_ignores_legend(self):
        records = extract_status_records(self.write_document())
        self.assertEqual(len(records), 4)
        self.assertEqual(
            [record.status for record in records],
            ["Closed", "Blocked", BLANK_STATUS, "Pending approval"],
        )
        self.assertEqual(records[-1].column, "Approval Status")

    def test_summary_counts_blank_and_named_states(self):
        records = extract_status_records(self.write_document())
        summary = summarize_records(records)
        self.assertEqual(summary["row_count"], 4)
        self.assertEqual(summary["status_counts"][BLANK_STATUS], 1)
        self.assertEqual(summary["status_counts"]["Closed"], 1)

    def test_markdown_report_contains_source_lines_and_items(self):
        records = extract_status_records(self.write_document())
        report = render_markdown(summarize_records(records))
        self.assertIn("# Readiness Status Summary", report)
        self.assertIn("| Blocked | 1 |", report)
        self.assertIn("| Protection test | Blocked |", report)

    def test_generated_report_is_not_reingested(self):
        records = extract_status_records(self.write_document())
        generated_path = self.write_document(
            render_markdown(summarize_records(records))
        )
        self.assertEqual(extract_status_records(generated_path), [])

    def test_rejects_inconsistent_status_table_width(self):
        content = STATUS_DOCUMENT.replace(
            "| Protection test | Commissioning | Blocked |",
            "| Protection test | Blocked |",
        )
        with self.assertRaisesRegex(ValueError, "expected 3"):
            extract_status_records(self.write_document(content))

    def test_cli_json_output_and_case_insensitive_gate(self):
        path = self.write_document()
        standard_output = io.StringIO()
        standard_error = io.StringIO()
        with (
            contextlib.redirect_stdout(standard_output),
            contextlib.redirect_stderr(standard_error),
        ):
            exit_code = main([str(path), "--format", "json", "--fail-on", "blocked"])
        self.assertEqual(exit_code, 2)
        self.assertEqual(json.loads(standard_output.getvalue())["row_count"], 4)
        self.assertIn("gate failed on: Blocked", standard_error.getvalue())

    def test_loads_example_status_policy(self):
        policy = load_status_policy(Path("config/readiness-status-policy.example.json"))
        self.assertTrue(policy.require_status)
        self.assertIn("Blocked", policy.blocking_statuses)
        self.assertIn("Approved", policy.allowed_statuses)

    def test_policy_finds_blank_unknown_and_blocking_rows(self):
        records = extract_status_records(self.write_document())
        policy = StatusPolicy(
            allowed_statuses=("closed", "blocked"),
            blocking_statuses=("blocked",),
            require_status=True,
        )
        violations = evaluate_status_policy(records, policy)
        self.assertEqual(
            [violation.reason for violation in violations],
            [
                "status is blocking",
                "status is required",
                "status is not in allowed_statuses",
            ],
        )
        self.assertEqual(violations[0].item, "Protection test")

    def test_rejects_invalid_status_policy(self):
        path = self.write_document(
            json.dumps(
                {
                    "allowed_statuses": ["Closed", "closed"],
                    "blocking_statuses": [],
                    "require_status": True,
                }
            )
        )
        with self.assertRaisesRegex(ValueError, "case-insensitive duplicates"):
            load_status_policy(path)

        path.write_text(
            json.dumps(
                {
                    "allowed_statuses": ["Closed"],
                    "blocking_statuses": ["Failed"],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "must also be allowed"):
            load_status_policy(path)

    def test_cli_policy_reports_line_level_violations(self):
        path = self.write_document()
        standard_output = io.StringIO()
        standard_error = io.StringIO()
        with (
            contextlib.redirect_stdout(standard_output),
            contextlib.redirect_stderr(standard_error),
        ):
            exit_code = main(
                [
                    str(path),
                    "--format",
                    "json",
                    "--policy",
                    "config/readiness-status-policy.example.json",
                ]
            )
        report = json.loads(standard_output.getvalue())
        self.assertEqual(exit_code, 2)
        self.assertEqual(len(report["policy_violations"]), 2)
        self.assertEqual(
            {item["reason"] for item in report["policy_violations"]},
            {"status is blocking", "status is required"},
        )
        markdown_report = render_markdown(report)
        self.assertIn("## Policy Evaluation", markdown_report)
        self.assertIn(
            "| Protection test | Blocked | status is blocking |", markdown_report
        )
        self.assertIn("Protection test: status is blocking", standard_error.getvalue())
        self.assertIn("Status policy gate failed with 2", standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
