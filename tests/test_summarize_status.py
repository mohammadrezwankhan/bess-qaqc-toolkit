from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.summarize_status import (
    BLANK_STATUS,
    ColumnStatusPolicy,
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
        self.assertEqual(
            {rule.column for rule in policy.column_rules},
            {"Approval Status", "Review Status"},
        )

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
        self.assertEqual(violations[0].column, "Status")

    def test_column_rule_replaces_global_rule_case_insensitively(self):
        records = extract_status_records(self.write_document())
        policy = StatusPolicy(
            allowed_statuses=(
                "Closed",
                "Blocked",
                "Pending approval",
            ),
            blocking_statuses=(),
            require_status=False,
            column_rules=(
                ColumnStatusPolicy(
                    column=" approval STATUS ",
                    allowed_statuses=("Approved",),
                    blocking_statuses=(),
                    require_status=True,
                ),
            ),
        )
        violations = evaluate_status_policy(records, policy)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].item, "Operating manual")
        self.assertEqual(violations[0].column, "Approval Status")
        self.assertEqual(
            violations[0].reason,
            "status is not in allowed_statuses",
        )

    def test_column_rule_can_define_its_own_blocking_state(self):
        content = STATUS_DOCUMENT.replace("Pending approval", "Rejected")
        records = extract_status_records(self.write_document(content))
        policy = StatusPolicy(
            allowed_statuses=("Closed", "Blocked", "Rejected"),
            blocking_statuses=(),
            require_status=False,
            column_rules=(
                ColumnStatusPolicy(
                    column="Approval Status",
                    allowed_statuses=("Approved", "Rejected"),
                    blocking_statuses=("Rejected",),
                    require_status=True,
                ),
            ),
        )
        violations = evaluate_status_policy(records, policy)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].status, "Rejected")
        self.assertEqual(violations[0].reason, "status is blocking")

    def test_column_rule_completeness_overrides_global_optional_status(self):
        content = STATUS_DOCUMENT.replace("Pending approval", "")
        records = extract_status_records(self.write_document(content))
        policy = StatusPolicy(
            allowed_statuses=(),
            blocking_statuses=(),
            require_status=False,
            column_rules=(
                ColumnStatusPolicy(
                    column="Approval Status",
                    allowed_statuses=("Approved",),
                    blocking_statuses=(),
                    require_status=True,
                ),
            ),
        )
        violations = evaluate_status_policy(records, policy)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].item, "Operating manual")
        self.assertEqual(violations[0].reason, "status is required")

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

    def test_rejects_invalid_column_rules(self):
        path = self.write_document(
            json.dumps(
                {
                    "column_rules": {
                        "Status": {
                            "allowed_statuses": [],
                            "blocking_statuses": [],
                            "require_status": False,
                        },
                        " status ": {
                            "allowed_statuses": [],
                            "blocking_statuses": [],
                            "require_status": False,
                        },
                    }
                }
            )
        )
        with self.assertRaisesRegex(ValueError, "duplicate columns"):
            load_status_policy(path)

        path.write_text(
            json.dumps(
                {
                    "column_rules": {
                        "Status": {
                            "allowed_statuses": [],
                            "blocking_statuses": [],
                            "require_status": False,
                            "unexpected": True,
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            load_status_policy(path)

        path.write_text(
            json.dumps(
                {
                    "column_rules": {
                        "Status": {
                            "allowed_statuses": [],
                            "blocking_statuses": [],
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "missing fields: require_status"):
            load_status_policy(path)

        path.write_text(
            json.dumps({"column_rules": []}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "must be a JSON object"):
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
        self.assertIn("Approval Status", report["status_policy"]["column_rules"])
        markdown_report = render_markdown(report)
        self.assertIn("## Policy Evaluation", markdown_report)
        self.assertIn(
            "| Protection test | Blocked | Status | status is blocking |",
            markdown_report,
        )
        self.assertIn("Protection test: status is blocking", standard_error.getvalue())
        self.assertIn("Status policy gate failed with 2", standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
