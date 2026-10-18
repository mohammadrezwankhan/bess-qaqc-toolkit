"""Audit readers must not discard a data row as a missing table separator."""

import contextlib
import io
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
from scripts.audit_punch_list import extract_punch_list_records
from scripts.summarize_status import extract_status_records, main


MALFORMED_RECORD = """# Review

Two items require review.

| Item | Status |
| Outstanding protection test | Open |
| Reviewed drawing | Closed |
"""


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


if __name__ == "__main__":
    unittest.main()
