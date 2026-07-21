from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.audit_deadlines import (
    GENERATED_MARKER,
    extract_deadline_records,
    main,
    render_markdown,
    summarize_deadlines,
)


DEADLINE_DOCUMENT = """# Commissioning Actions

Use this record to track dated owner actions.

| Item | Owner | Target Close Date | Status |
| --- | --- | --- | --- |
| Fire interface retest | Commissioning | 2026-07-19 | Open |
| Meter evidence | Grid | 2026-07-20 | In progress |
| O and M manual | Supplier | 2026-07-25 | Open |
| Closed label action | Construction | 2026-07-10 | Closed |
| Missing relay deadline | Protection | | Open |
| | | | |

| Status | Meaning |
| --- | --- |
| Open | Action remains with its owner. |
| Closed | Evidence has been accepted. |
"""


class DeadlineAuditTests(unittest.TestCase):
    def write_document(self, content: str = DEADLINE_DOCUMENT) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "readiness.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_classifies_deadline_states_and_skips_blank_rows(self):
        records = extract_deadline_records(
            self.write_document(),
            date(2026, 7, 20),
        )
        self.assertEqual(len(records), 5)
        self.assertEqual(
            [record.state for record in records],
            ["overdue", "due_today", "upcoming", "closed", "missing"],
        )
        self.assertEqual(
            [record.days_to_deadline for record in records],
            [-1, 0, 5, -10, None],
        )
        self.assertEqual(records[0].deadline_column, "Target Close Date")
        self.assertEqual(records[0].status_column, "Status")

    def test_terminal_status_matching_is_case_insensitive(self):
        content = DEADLINE_DOCUMENT.replace(
            "| Closed label action | Construction | 2026-07-10 | Closed |",
            "| Closed label action | Construction | 2026-07-10 | ACCEPTED |",
        )
        records = extract_deadline_records(
            self.write_document(content),
            date(2026, 7, 20),
        )
        self.assertEqual(records[3].state, "closed")

    def test_controlled_placeholder_is_classified_as_missing(self):
        content = DEADLINE_DOCUMENT.replace(
            "| Missing relay deadline | Protection | | Open |",
            "| Missing relay deadline | Protection | TBD | Open |",
        )
        records = extract_deadline_records(
            self.write_document(content),
            date(2026, 7, 20),
        )
        self.assertEqual(records[-1].state, "missing")
        self.assertEqual(records[-1].deadline, "TBD")

    def test_custom_date_column_and_terminal_status_replace_defaults(self):
        content = """# Action Register

Track action timing and disposition.

| Action | Required On | Review Status |
| --- | --- | --- |
| Confirm firmware | 2026-07-18 | Waived |
"""
        records = extract_deadline_records(
            self.write_document(content),
            date(2026, 7, 20),
            date_columns=("required on",),
            terminal_statuses=("waived",),
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].state, "closed")
        self.assertEqual(records[0].deadline_column, "Required On")

    def test_generated_reports_are_not_reingested(self):
        records = extract_deadline_records(
            self.write_document(),
            date(2026, 7, 20),
        )
        report = render_markdown(summarize_deadlines(records, date(2026, 7, 20)))
        self.assertTrue(report.startswith(GENERATED_MARKER))
        self.assertEqual(
            extract_deadline_records(
                self.write_document(report),
                date(2026, 7, 20),
            ),
            [],
        )

    def test_rejects_malformed_deadline(self):
        content = DEADLINE_DOCUMENT.replace("2026-07-19", "19/07/2026")
        with self.assertRaisesRegex(ValueError, "must use YYYY-MM-DD"):
            extract_deadline_records(
                self.write_document(content),
                date(2026, 7, 20),
            )

    def test_rejects_multiple_recognized_deadline_columns(self):
        content = """# Ambiguous Register

Do not allow two active deadline definitions.

| Item | Due Date | Target Close Date | Status |
| --- | --- | --- | --- |
| Relay test | 2026-07-20 | 2026-07-21 | Open |
"""
        with self.assertRaisesRegex(ValueError, "multiple deadline columns"):
            extract_deadline_records(
                self.write_document(content),
                date(2026, 7, 20),
            )

    def test_summary_and_markdown_include_line_level_evidence(self):
        records = extract_deadline_records(
            self.write_document(),
            date(2026, 7, 20),
        )
        summary = summarize_deadlines(records, date(2026, 7, 20))
        self.assertEqual(summary["row_count"], 5)
        self.assertEqual(summary["state_counts"]["overdue"], 1)
        self.assertEqual(summary["state_counts"]["missing"], 1)
        report = render_markdown(summary)
        self.assertIn("# Readiness Deadline Audit", report)
        self.assertIn("| overdue | 1 |", report)
        self.assertIn(
            "| Fire interface retest | Status | Open | Target Close Date | "
            "2026-07-19 |",
            report,
        )

    def test_cli_json_gate_reports_selected_states(self):
        standard_output = io.StringIO()
        standard_error = io.StringIO()
        with (
            contextlib.redirect_stdout(standard_output),
            contextlib.redirect_stderr(standard_error),
        ):
            exit_code = main(
                [
                    str(self.write_document()),
                    "--as-of",
                    "2026-07-20",
                    "--format",
                    "json",
                    "--fail-on",
                    "overdue",
                    "--fail-on",
                    "missing",
                ]
            )
        self.assertEqual(exit_code, 2)
        summary = json.loads(standard_output.getvalue())
        self.assertEqual(summary["state_counts"]["due_today"], 1)
        self.assertIn("overdue (1), missing (1)", standard_error.getvalue())

    def test_cli_writes_nested_report_and_rejects_invalid_as_of(self):
        path = self.write_document()
        output_directory = tempfile.TemporaryDirectory()
        self.addCleanup(output_directory.cleanup)
        output_path = Path(output_directory.name) / "reports" / "deadlines.md"
        self.assertEqual(
            main(
                [
                    str(path),
                    "--as-of",
                    "2026-07-20",
                    "--output",
                    str(output_path),
                ]
            ),
            0,
        )
        self.assertTrue(output_path.is_file())
        self.assertIn("As of: 2026-07-20", output_path.read_text(encoding="utf-8"))

        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main([str(path), "--as-of", "20260720"])
        self.assertEqual(exit_code, 1)
        self.assertIn("must use YYYY-MM-DD", standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
