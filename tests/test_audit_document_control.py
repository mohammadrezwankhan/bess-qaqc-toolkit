from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.audit_document_control import (
    GENERATED_MARKER,
    DocumentRevision,
    audit_document_control,
    extract_document_revisions,
    main,
    render_markdown,
    summarize_document_control,
)


ROOT = Path(__file__).resolve().parents[1]
PASSING_EXAMPLE = ROOT / "examples" / "document-control-passing.md"


def revision(**overrides: str | int) -> DocumentRevision:
    values: dict[str, str | int] = {
        "source": "records.md",
        "line": 4,
        "document_id": "HND-001",
        "document_type": "As-built drawing",
        "system_area": "Electrical",
        "owner": "Engineering lead",
        "revision": "Rev A",
        "approval_status": "Approved",
        "issue_date": "2026-07-01",
        "supersedes_revision": "-",
        "evidence_link": "Controlled drawings / HND-001 / Rev A",
        "closeout_notes": "Matches the energized configuration.",
    }
    values.update(overrides)
    return DocumentRevision(**values)  # type: ignore[arg-type]


class DocumentControlAuditTests(unittest.TestCase):
    def test_passing_example_has_no_issues(self) -> None:
        records = extract_document_revisions(PASSING_EXAMPLE)

        issues = audit_document_control(records, date(2026, 7, 21))

        self.assertEqual(4, len(records))
        self.assertEqual([], issues)

    def test_extracts_alphabetic_and_numeric_histories(self) -> None:
        records = extract_document_revisions(PASSING_EXAMPLE)

        self.assertEqual(
            [("HND-101", "Rev A"), ("HND-101", "Rev B")],
            [(item.document_id, item.revision) for item in records[:2]],
        )
        self.assertEqual("Rev 1", records[-1].revision)
        self.assertGreater(records[-1].line, records[0].line)

    def test_extraction_rejects_missing_columns_and_bad_row_width(self) -> None:
        missing_column = """# Register

Intro.

| Document ID | Revision | Approval Status |
| --- | --- | --- |
| HND-001 | Rev A | Approved |
"""
        bad_width = PASSING_EXAMPLE.read_text(encoding="utf-8").replace(
            "| HND-101 | As-built single-line diagram | Electrical |",
            "| HND-101 | As-built single-line diagram |",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            missing_path = Path(directory) / "missing.md"
            width_path = Path(directory) / "width.md"
            missing_path.write_text(missing_column, encoding="utf-8")
            width_path.write_text(bad_width, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required column"):
                extract_document_revisions(missing_path)
            with self.assertRaisesRegex(ValueError, "table row has"):
                extract_document_revisions(width_path)

    def test_generated_report_is_not_reingested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            path.write_text(
                GENERATED_MARKER
                + "\n\n| Document ID | Revision | Approval Status |\n"
                + "| --- | --- | --- |\n| HND-001 | Rev A | Approved |\n",
                encoding="utf-8",
            )

            self.assertEqual([], extract_document_revisions(path))

    def test_missing_invalid_and_duplicate_values_are_reported(self) -> None:
        records = [
            revision(
                document_id="bad id",
                revision="release-one",
                approval_status="Unknown",
                issue_date="21-07-2026",
                owner="TBD",
            ),
            revision(line=5, evidence_link=""),
            revision(line=6, revision="A"),
        ]

        kinds = {
            issue.kind
            for issue in audit_document_control(records, date(2026, 7, 21))
        }

        self.assertTrue(
            {
                "missing_required_field",
                "invalid_document_id",
                "invalid_revision",
                "invalid_issue_date",
                "invalid_approval_status",
                "missing_controlled_location",
                "duplicate_document_revision",
            }.issubset(kinds)
        )

    def test_revision_lifecycle_and_supersession_are_enforced(self) -> None:
        records = [
            revision(
                revision="Rev A",
                approval_status="Approved",
                supersedes_revision="Rev Z",
            ),
            revision(
                line=5,
                revision="Rev B",
                approval_status="Draft",
                issue_date="2026-06-30",
                supersedes_revision="Rev Z",
            ),
        ]

        kinds = {
            issue.kind
            for issue in audit_document_control(records, date(2026, 7, 21))
        }

        self.assertEqual(
            {
                "unexpected_supersedes_revision",
                "historical_revision_not_obsolete",
                "incorrect_supersedes_revision",
                "non_increasing_issue_date",
                "latest_revision_not_approved",
            },
            kinds,
        )

    def test_revision_scheme_metadata_and_future_dates_are_controlled(self) -> None:
        records = [
            revision(
                revision="Rev A",
                approval_status="Superseded",
                issue_date="2026-07-22",
            ),
            revision(
                line=5,
                revision="Rev 1",
                document_type="Protection file",
                system_area="Grid interface",
                supersedes_revision="Rev 0",
            ),
        ]

        kinds = {
            issue.kind
            for issue in audit_document_control(records, date(2026, 7, 21))
        }

        self.assertTrue(
            {
                "future_issue_date",
                "inconsistent_document_type",
                "inconsistent_system_area",
                "inconsistent_revision_scheme",
            }.issubset(kinds)
        )

    def test_missing_supersedes_revision_is_reported(self) -> None:
        records = [
            revision(approval_status="Superseded"),
            revision(
                line=5,
                revision="Rev B",
                issue_date="2026-07-02",
                supersedes_revision="-",
            ),
        ]

        kinds = [
            issue.kind
            for issue in audit_document_control(records, date(2026, 7, 21))
        ]

        self.assertEqual(["missing_supersedes_revision"], kinds)

    def test_custom_status_vocabularies_replace_defaults(self) -> None:
        record = revision(approval_status="Issued for use")

        default_kinds = {
            issue.kind
            for issue in audit_document_control([record], date(2026, 7, 21))
        }
        custom_issues = audit_document_control(
            [record],
            date(2026, 7, 21),
            accepted_statuses=("Issued for use",),
            working_statuses=("In review",),
            obsolete_statuses=("Replaced",),
        )

        self.assertIn("invalid_approval_status", default_kinds)
        self.assertEqual([], custom_issues)

    def test_overlapping_status_classifications_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not overlap"):
            audit_document_control(
                [revision()],
                date(2026, 7, 21),
                accepted_statuses=("Approved",),
                working_statuses=("Approved",),
            )

    def test_summary_and_markdown_preserve_revision_history(self) -> None:
        records = extract_document_revisions(PASSING_EXAMPLE)
        issues = audit_document_control(records, date(2026, 7, 21))

        summary = summarize_document_control(
            records, issues, date(2026, 7, 21)
        )
        markdown = render_markdown(summary)

        self.assertEqual(2, summary["document_count"])
        self.assertEqual(2, summary["status_category_counts"]["obsolete"])
        self.assertIn("| HND-102 | Rev 1 | 2026-07-18 | Rev 0 |", markdown)

    def test_cli_json_pass_and_markdown_failure_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "passing.json"
            failure_path = Path(directory) / "failure.md"
            failing_record = PASSING_EXAMPLE.read_text(encoding="utf-8").replace(
                "| Released | 2026-07-18 | Rev 0 |",
                "| Draft | 2026-07-18 | Rev 0 |",
            )
            input_path = Path(directory) / "failing.md"
            input_path.write_text(failing_record, encoding="utf-8")

            passing_code = main(
                [
                    str(PASSING_EXAMPLE),
                    "--as-of",
                    "2026-07-21",
                    "--format",
                    "json",
                    "--output",
                    str(json_path),
                ]
            )
            failing_code = main(
                [
                    str(input_path),
                    "--as-of",
                    "2026-07-21",
                    "--output",
                    str(failure_path),
                ]
            )

            self.assertEqual(0, passing_code)
            self.assertEqual(2, failing_code)
            self.assertEqual(0, json.loads(json_path.read_text())["issue_count"])
            self.assertIn("latest_revision_not_approved", failure_path.read_text())

    def test_cli_returns_one_for_empty_input_and_invalid_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            empty = Path(directory) / "empty.md"
            empty.write_text("# Empty\n\nNo register.\n", encoding="utf-8")

            self.assertEqual(1, main([str(empty), "--as-of", "2026-07-21"]))
            self.assertEqual(1, main([str(PASSING_EXAMPLE), "--as-of", "today"]))


if __name__ == "__main__":
    unittest.main()
