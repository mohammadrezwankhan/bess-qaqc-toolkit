"""Audit readers must not discard a data row as a missing table separator."""

import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.audit_calibration_traceability import extract_calibration_records
from scripts.audit_completeness import extract_completeness_results, load_completeness_policy
from scripts.audit_deadlines import extract_deadline_records
from scripts.audit_document_control import extract_document_revisions
from scripts.audit_evidence_traceability import extract_traceability_records
from scripts.audit_handover_acceptance import extract_handover_records
from scripts.audit_handover_acceptance import main as handover_main
from scripts.audit_punch_list import extract_punch_list_records
from scripts.summarize_status import extract_status_records, main


MALFORMED_RECORD = """# Review

Two items require review.

| Item | Status |
| Outstanding protection test | Open |
| Reviewed drawing | Closed |
"""
HANDOVER_EXAMPLE = Path(__file__).resolve().parents[1] / "examples/handover-acceptance-passing.md"


class AuditTableStructureTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "records.md"
        self.path.write_text(MALFORMED_RECORD, encoding="utf-8")

    def test_all_audit_readers_reject_missing_separator(self):
        policy_path = (
            Path(__file__).resolve().parents[1]
            / "config/readiness-completeness-policy.example.json"
        )
        policy = load_completeness_policy(policy_path)
        readers = (
            extract_status_records,
            extract_calibration_records,
            extract_document_revisions,
            extract_traceability_records,
            extract_handover_records,
            extract_punch_list_records,
            lambda path: extract_deadline_records(path, date(2026, 7, 21)),
            lambda path: extract_completeness_results(path, policy),
        )
        for reader in readers:
            with self.subTest(reader=reader):
                with self.assertRaisesRegex(ValueError, "separator"):
                    reader(self.path)

    def test_status_gate_fails_instead_of_silently_skipping_open_item(self):
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            result = main([str(self.path), "--fail-on", "Open", "--format", "json"])
        self.assertEqual(result, 1)
        self.assertIn("separator", error.getvalue())

    def test_status_reader_rejects_separator_with_wrong_width(self):
        self.path.write_text(
            MALFORMED_RECORD.replace(
                "| Outstanding protection test | Open |", "| --- | --- | --- |"
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "separator"):
            extract_status_records(self.path)

    def test_handover_registers_accept_declared_heading_aliases(self):
        text = HANDOVER_EXAMPLE.read_text(encoding="utf-8")
        expected = extract_handover_records(HANDOVER_EXAMPLE)
        for canonical, alias in (
            ("Finding or Nonconformance", "Finding"),
            ("Source Item ID", "Source Punch ID"),
        ):
            with self.subTest(heading=alias):
                self.path.write_text(
                    text.replace(f"| {canonical} |", f"| {alias} |"), encoding="utf-8"
                )
                actual = extract_handover_records(self.path)
                self.assertEqual([len(rows) for rows in actual], [len(rows) for rows in expected])

    def test_handover_audits_supplementary_punch_table_with_finding_alias(self):
        self.path.write_text(
            "| ID | Severity | Finding | Owner | Evidence Link | Target Close Date | Status | Closeout Note |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| PL-099 | Critical | Open commissioning check | Reviewer | DMS/PL-099.pdf | 2026-07-25 | Open | Pending review |\n",
            encoding="utf-8",
        )
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            result = handover_main([str(HANDOVER_EXAMPLE), str(self.path), "--format", "json"])
        self.assertEqual(result, 2, error.getvalue())
        summary = json.loads(output.getvalue())
        self.assertEqual(summary["punch_item_count"], 4)
        self.assertEqual([issue["kind"] for issue in summary["issues"]], ["acceptance_blocker"])
        self.assertIn("PL-099", summary["issues"][0]["detail"])


    def test_handover_rejects_incomplete_supplementary_registers(self):
        example = HANDOVER_EXAMPLE.read_text(encoding="utf-8").splitlines()
        for signature, column, field in (
            ("| ID | Severity |", "Finding or Nonconformance", "finding"),
            ("| ID | Source Item ID |", "Interim Control", "interim_control"),
            ("| Acceptance ID |", "Decision", "decision"),
        ):
            with self.subTest(column=column):
                start = next(i for i, line in enumerate(example) if line.startswith(signature))
                cells = [line.strip("|").split("|") for line in example[start:start + 3]]
                missing = [cell.strip() for cell in cells[0]].index(column)
                for row in cells:
                    del row[missing]
                incomplete = "\n".join("|" + "|".join(row) + "|" for row in cells)
                self.path.write_text(incomplete + "\n", encoding="utf-8")

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    with contextlib.redirect_stderr(io.StringIO()) as stderr:
                        result = handover_main(
                            [str(HANDOVER_EXAMPLE), str(self.path), "--format", "json"]
                        )
                self.assertEqual(result, 1, stderr.getvalue())
                self.assertIn(f"missing required column for {field}", stderr.getvalue())
                self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
