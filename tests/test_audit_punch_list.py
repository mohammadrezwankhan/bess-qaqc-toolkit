from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

from scripts.audit_punch_list import (
    GENERATED_MARKER,
    audit_punch_list,
    extract_punch_list_records,
    main,
    render_markdown,
    summarize_punch_list,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "examples" / "punch-list-closeout-passing.md"
AS_OF = date(2026, 7, 21)


class PunchListAuditTests(unittest.TestCase):
    def setUp(self):
        self.records = extract_punch_list_records(EXAMPLE_PATH)

    def kinds(self, records=None):
        issues = audit_punch_list(
            self.records if records is None else records,
            AS_OF,
        )
        return [issue.kind for issue in issues]

    def test_extracts_all_status_and_severity_examples(self):
        self.assertEqual(len(self.records), 4)
        self.assertEqual(
            [record.item_id for record in self.records],
            ["NCR-001", "PL-002", "PL-003", "NCR-004"],
        )
        self.assertEqual(
            [record.status for record in self.records],
            ["Closed", "Ready for verification", "In progress", "Deferred"],
        )

    def test_passing_example_has_no_issues(self):
        self.assertEqual(self.kinds(), [])

    def test_invalid_and_duplicate_ids_are_reported(self):
        records = [
            self.records[0],
            replace(self.records[1], item_id="NCR-001"),
            replace(self.records[2], item_id="bad id"),
            self.records[3],
        ]
        kinds = self.kinds(records)
        self.assertIn("invalid_item_id", kinds)
        self.assertIn("duplicate_item_id", kinds)

    def test_missing_controlled_fields_are_reported_together(self):
        records = [
            replace(
                self.records[2],
                owner="TBD",
                target_close_date="-",
                system_area="",
            )
        ]
        issues = audit_punch_list(records, AS_OF)
        self.assertEqual([issue.kind for issue in issues], ["missing_required_field"])
        self.assertIn("System Area, Owner, Target Close Date", issues[0].detail)

    def test_unknown_severity_and_status_are_reported(self):
        record = replace(
            self.records[2],
            severity="High",
            status="Pending",
        )
        kinds = self.kinds([record])
        self.assertIn("invalid_severity", kinds)
        self.assertIn("invalid_status", kinds)

    def test_invalid_date_and_overdue_active_item_are_distinct(self):
        records = [
            replace(self.records[1], target_close_date="24-07-2026"),
            replace(self.records[2], target_close_date="2026-07-20"),
        ]
        kinds = self.kinds(records)
        self.assertIn("invalid_target_close_date", kinds)
        self.assertIn("overdue_item", kinds)

    def test_unresolved_and_deferred_critical_items_fail(self):
        active = replace(
            self.records[2],
            severity="Critical",
        )
        deferred = replace(
            self.records[3],
            severity="Critical",
        )
        kinds = self.kinds([active, deferred])
        self.assertIn("unresolved_critical_item", kinds)
        self.assertIn("critical_item_deferred", kinds)

    def test_ready_and_terminal_items_require_evidence(self):
        records = [
            replace(self.records[1], evidence_link="-"),
            replace(self.records[3], evidence_link="TBD"),
        ]
        kinds = self.kinds(records)
        self.assertEqual(kinds.count("missing_closeout_evidence"), 2)

    def test_terminal_item_requires_closeout_note(self):
        record = replace(self.records[0], closeout_note="")
        self.assertIn("missing_closeout_note", self.kinds([record]))

    def test_summary_and_markdown_preserve_closeout_state(self):
        records = [
            replace(self.records[0], severity="critical", status="closed"),
            *self.records[1:],
        ]
        summary = summarize_punch_list(records, [], AS_OF)
        self.assertEqual(summary["item_count"], 4)
        self.assertEqual(summary["severity_counts"]["Major"], 2)
        self.assertEqual(summary["status_counts"]["Closed"], 1)
        self.assertEqual(summary["items"][0]["days_to_target"], -3)
        self.assertFalse(summary["items"][0]["overdue"])
        rendered = render_markdown(summary)
        self.assertIn("# Punch-List Closeout Audit", rendered)
        self.assertIn("## Counts", rendered)
        self.assertIn("## Items", rendered)

    def test_generated_report_is_not_ingested(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            path.write_text(
                GENERATED_MARKER + "\n\n# Punch-List Closeout Audit\n",
                encoding="utf-8",
            )
            records = extract_punch_list_records(path)
        self.assertEqual(records, [])

    def test_extraction_rejects_missing_columns_and_bad_row_width(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.md"
            path.write_text(
                "# Record\n\n"
                "| ID | Severity | Finding or Nonconformance | Status |\n"
                "| --- | --- | --- | --- |\n"
                "| PL-001 | Major | Finding | Open |\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing required column"):
                extract_punch_list_records(path)

            path.write_text(
                "# Record\n\n"
                "| ID | Severity | Finding | System Area | Owner | Evidence | "
                "Due Date | Status | Closeout Note |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| PL-001 | Major | Finding | PCS | Owner | - | 2026-08-01 | "
                "Open |\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "table row has 8 cells"):
                extract_punch_list_records(path)

    def test_cli_emits_json_for_passing_record(self):
        standard_output = io.StringIO()
        with contextlib.redirect_stdout(standard_output):
            exit_code = main(
                [
                    str(EXAMPLE_PATH),
                    "--as-of",
                    "2026-07-21",
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(exit_code, 0)
        report = json.loads(standard_output.getvalue())
        self.assertEqual(report["issue_count"], 0)
        self.assertEqual(report["item_count"], 4)

    def test_cli_writes_failure_report_and_returns_two(self):
        document = EXAMPLE_PATH.read_text(encoding="utf-8").replace(
            "| 2026-07-28 | In progress |",
            "| 2026-07-20 | In progress |",
        )
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "record.md"
            output_path = Path(directory) / "reports" / "punch-list.md"
            input_path.write_text(document, encoding="utf-8")
            standard_error = io.StringIO()
            with contextlib.redirect_stderr(standard_error):
                exit_code = main(
                    [
                        str(input_path),
                        "--as-of",
                        "2026-07-21",
                        "--output",
                        str(output_path),
                    ]
                )
            self.assertEqual(exit_code, 2)
            self.assertTrue(output_path.is_file())
            self.assertIn("overdue_item", standard_error.getvalue())

    def test_cli_returns_one_for_empty_input_and_invalid_date(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "empty.md"
            input_path.write_text("# Empty\n", encoding="utf-8")
            for arguments, message in (
                (
                    [str(input_path), "--as-of", "2026-07-21"],
                    "no punch-list rows found",
                ),
                (
                    [str(EXAMPLE_PATH), "--as-of", "21-07-2026"],
                    "must use YYYY-MM-DD",
                ),
            ):
                with self.subTest(arguments=arguments):
                    standard_error = io.StringIO()
                    with contextlib.redirect_stderr(standard_error):
                        exit_code = main(arguments)
                    self.assertEqual(exit_code, 1)
                    self.assertIn(message, standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
