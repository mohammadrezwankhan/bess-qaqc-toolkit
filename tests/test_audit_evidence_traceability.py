from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from scripts.audit_evidence_traceability import (
    GENERATED_MARKER,
    audit_traceability,
    extract_traceability_records,
    main,
    render_markdown,
    summarize_traceability,
)


PASSING_DOCUMENT = """# Commissioning Evidence Traceability

Use this completed record to audit controlled commissioning evidence.

| Check ID | Check or Test | Evidence IDs | Acceptance Reference | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| CHK-001 | Trip circuit functional test | EVD-001, EVD-002 | SAT-017 | Commissioning | Closed |
| CHK-002 | Meter scaling verification | EVD-003 | MTR-004 | Grid | Ready for verification |
| CHK-003 | SCADA label review | EVD-002 | SCADA-011 | Controls | Open |

| Evidence ID | Evidence Location | Revision | Approval Status |
| --- | --- | --- | --- |
| EVD-001 | DMS/SAT/trip-test.pdf | A | Approved |
| EVD-002 | DMS/SAT/screenshots.zip | B | Accepted |
| EVD-003 | DMS/Metering/scaling.pdf | 0 | Approved |
"""


class EvidenceTraceabilityTests(unittest.TestCase):
    def write_document(self, content: str = PASSING_DOCUMENT) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "evidence.md"
        path.write_text(content, encoding="utf-8")
        return path

    def records(self):
        return extract_traceability_records(self.write_document())

    def test_extracts_check_and_evidence_tables(self):
        checks, evidence = self.records()
        self.assertEqual(len(checks), 3)
        self.assertEqual(len(evidence), 3)
        self.assertEqual(checks[0].evidence_ids, ("EVD-001", "EVD-002"))
        self.assertEqual(evidence[1].approval_status, "Accepted")

    def test_clean_shared_evidence_traceability_passes(self):
        checks, evidence = self.records()
        issues = audit_traceability(checks, evidence)
        summary = summarize_traceability(checks, evidence, issues)
        self.assertEqual(issues, [])
        self.assertEqual(summary["check_count"], 3)
        self.assertEqual(summary["completed_check_count"], 2)
        self.assertEqual(summary["referenced_evidence_count"], 3)
        self.assertEqual(
            summary["evidence"][1]["referenced_by"], ["CHK-001", "CHK-003"]
        )

    def test_markdown_report_contains_coverage_and_register(self):
        checks, evidence = self.records()
        report = render_markdown(
            summarize_traceability(
                checks, evidence, audit_traceability(checks, evidence)
            )
        )
        self.assertTrue(report.startswith(GENERATED_MARKER))
        self.assertIn("# Commissioning Evidence Traceability Audit", report)
        self.assertIn("| CHK-001 | Trip circuit functional test |", report)
        self.assertIn("| EVD-002 | Accepted | B | CHK-001, CHK-003 |", report)

    def test_generated_report_is_not_reingested(self):
        checks, evidence = self.records()
        report = render_markdown(
            summarize_traceability(
                checks, evidence, audit_traceability(checks, evidence)
            )
        )
        generated_path = self.write_document(report)
        self.assertEqual(extract_traceability_records(generated_path), ([], []))

    def test_duplicate_check_and_evidence_ids_are_reported(self):
        checks, evidence = self.records()
        duplicate_check = replace(checks[0], line=99)
        duplicate_evidence = replace(evidence[0], line=100)
        issues = audit_traceability(
            [*checks, duplicate_check],
            [*evidence, duplicate_evidence],
        )
        kinds = {issue.kind for issue in issues}
        self.assertIn("duplicate_check_id", kinds)
        self.assertIn("duplicate_evidence_id", kinds)

    def test_invalid_and_repeated_references_are_reported(self):
        checks, evidence = self.records()
        invalid = replace(
            checks[0],
            check_id="bad-id",
            evidence_ids=("bad-evidence", "bad-evidence"),
        )
        issues = audit_traceability([invalid, *checks[1:]], evidence)
        kinds = [issue.kind for issue in issues]
        self.assertIn("invalid_check_id", kinds)
        self.assertIn("invalid_evidence_reference", kinds)
        self.assertIn("duplicate_evidence_reference", kinds)
        self.assertIn("unknown_evidence_reference", kinds)

    def test_case_variant_duplicate_is_audited_only_once(self):
        checks, evidence = self.records()
        duplicated = replace(
            checks[0],
            evidence_ids=("EVD-001", "evd-001"),
        )
        pending = replace(evidence[0], approval_status="Pending")
        issues = audit_traceability(
            [duplicated, *checks[1:]],
            [pending, *evidence[1:]],
        )
        self.assertEqual(
            sum(issue.kind == "unaccepted_evidence" for issue in issues),
            1,
        )
        self.assertEqual(
            sum(issue.kind == "duplicate_evidence_reference" for issue in issues),
            1,
        )

    def test_missing_check_and_evidence_fields_are_reported(self):
        checks, evidence = self.records()
        incomplete_check = replace(
            checks[0],
            item="",
            evidence_ids=(),
            acceptance_reference="TBD",
            owner="",
            status="-",
        )
        incomplete_evidence = replace(
            evidence[0],
            location="TBC",
            revision="",
            approval_status="N/A",
        )
        issues = audit_traceability(
            [incomplete_check, *checks[1:]],
            [incomplete_evidence, *evidence[1:]],
        )
        kinds = [issue.kind for issue in issues]
        self.assertEqual(kinds.count("missing_check_field"), 4)
        self.assertIn("missing_evidence_reference", kinds)
        self.assertEqual(kinds.count("missing_evidence_field"), 3)

    def test_unknown_references_and_orphan_evidence_are_reported(self):
        checks, evidence = self.records()
        changed_checks = [
            replace(checks[0], evidence_ids=("EVD-999",)),
            *checks[1:],
        ]
        issues = audit_traceability(changed_checks, evidence)
        kinds = [issue.kind for issue in issues]
        self.assertIn("unknown_evidence_reference", kinds)
        self.assertIn("orphan_evidence", kinds)
        orphan_ids = {
            issue.record_id for issue in issues if issue.kind == "orphan_evidence"
        }
        self.assertEqual(orphan_ids, {"EVD-001"})

    def test_completed_check_requires_accepted_evidence(self):
        checks, evidence = self.records()
        pending = replace(evidence[0], approval_status="Pending review")
        issues = audit_traceability(checks, [pending, *evidence[1:]])
        unaccepted = [issue for issue in issues if issue.kind == "unaccepted_evidence"]
        self.assertEqual(len(unaccepted), 1)
        self.assertEqual(unaccepted[0].record_id, "CHK-001")
        self.assertIn("EVD-001", unaccepted[0].detail)

    def test_open_check_can_reference_pending_evidence(self):
        checks, evidence = self.records()
        all_open = [replace(check, status="Open") for check in checks]
        pending = [replace(record, approval_status="Pending") for record in evidence]
        self.assertEqual(audit_traceability(all_open, pending), [])

    def test_custom_completed_and_accepted_statuses_are_case_insensitive(self):
        checks, evidence = self.records()
        custom_check = replace(checks[0], status="VERIFIED")
        custom_evidence = replace(evidence[0], approval_status="reviewed")
        issues = audit_traceability(
            [custom_check, *checks[1:]],
            [custom_evidence, *evidence[1:]],
            completed_statuses=("verified",),
            accepted_evidence_statuses=("REVIEWED", "Approved", "Accepted"),
        )
        self.assertEqual(issues, [])

    def test_rejects_missing_required_column_and_bad_row_width(self):
        path = self.write_document(PASSING_DOCUMENT.replace("| Owner |", "| Team |"))
        with self.assertRaisesRegex(ValueError, "missing required column for owner"):
            extract_traceability_records(path)

        path.write_text(
            PASSING_DOCUMENT.replace(
                "| CHK-003 | SCADA label review | EVD-002 | SCADA-011 | Controls | Open |",
                "| CHK-003 | SCADA label review | EVD-002 | Open |",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "expected 6"):
            extract_traceability_records(path)

    def test_cli_json_pass_reports_counts(self):
        path = self.write_document()
        standard_output = io.StringIO()
        with contextlib.redirect_stdout(standard_output):
            exit_code = main([str(path), "--format", "json"])
        report = json.loads(standard_output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["check_count"], 3)
        self.assertEqual(report["issue_count"], 0)

    def test_cli_gate_returns_two_and_writes_issue_report(self):
        path = self.write_document(PASSING_DOCUMENT.replace("Approved", "Pending", 1))
        output_path = path.parent / "reports" / "traceability.json"
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main(
                [
                    str(path),
                    "--format",
                    "json",
                    "--output",
                    str(output_path),
                ]
            )
        report = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 2)
        self.assertEqual(report["issue_count"], 1)
        self.assertIn("unaccepted_evidence", standard_error.getvalue())

    def test_cli_returns_one_when_no_traceability_tables_exist(self):
        path = self.write_document("# Notes\n\nNo evidence tables here.\n")
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main([str(path)])
        self.assertEqual(exit_code, 1)
        self.assertIn("no commissioning check rows", standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
