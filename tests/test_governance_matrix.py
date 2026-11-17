from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.audit_calibration_traceability import (
    CalibrationRecord,
    MeasurementRecord,
    audit_calibration_traceability,
)
from scripts.audit_completeness import (
    extract_completeness_results,
    load_completeness_policy,
)
from scripts.audit_evidence_traceability import (
    CheckRecord,
    EvidenceRecord,
    audit_traceability,
)
from scripts.audit_handover_acceptance import (
    AcceptanceDecision,
    PunchItem,
    ResidualRisk,
    audit_handover,
    load_handover_policy,
)
from scripts.audit_punch_list import (
    PunchListRecord,
    audit_punch_list,
    summarize_punch_list,
)
from scripts.summarize_status import (
    expand_paths,
    load_status_policy,
)
from scripts.validate_templates import (
    table_cells,
    validate_template,
)


ROOT = Path(__file__).resolve().parents[1]
AS_OF = date(2026, 7, 21)


class GovernanceMatrixTests(unittest.TestCase):
    """Exhaustive negative and invariant tests matching Master Mission Phase 4."""

    def test_critical_defect_remains_open_blocks_release(self):
        record = PunchListRecord(
            source="test.md",
            line=10,
            item_id="NCR-001",
            severity="Critical",
            finding="Trip circuit failsafe unverified",
            system_area="Fire safety interface",
            owner="Commissioning lead",
            evidence_link="-",
            target_close_date="2026-07-25",
            status="Open",
            closeout_note="-",
        )
        issues = audit_punch_list([record], AS_OF)
        self.assertTrue(any(issue.kind == "unresolved_critical_item" for issue in issues))

    def test_critical_defect_marked_deferred_cannot_bypass_blocking(self):
        record = PunchListRecord(
            source="test.md",
            line=10,
            item_id="NCR-001",
            severity="Critical",
            finding="Trip circuit failsafe unverified",
            system_area="Fire safety interface",
            owner="Commissioning lead",
            evidence_link="records/RRA-001.pdf",
            target_close_date="2026-08-01",
            status="Deferred",
            closeout_note="Approved interim control.",
        )
        issues = audit_punch_list([record], AS_OF)
        self.assertTrue(any(issue.kind == "critical_item_deferred" for issue in issues))

    def test_critical_defect_closed_without_approved_verification_rejected(self):
        record = PunchListRecord(
            source="test.md",
            line=10,
            item_id="NCR-001",
            severity="Critical",
            finding="Trip circuit failsafe unverified",
            system_area="Fire safety interface",
            owner="Commissioning lead",
            evidence_link="records/retest.pdf",
            target_close_date="2026-07-20",
            status="Closed",
            closeout_note="completed",
        )
        issues = audit_punch_list([record], AS_OF)
        self.assertTrue(any(issue.kind == "unverified_critical_closeout" for issue in issues))

    def test_major_defect_incomplete_corrective_evidence(self):
        record = PunchListRecord(
            source="test.md",
            line=10,
            item_id="PL-002",
            severity="Major",
            finding="Inverter grounding label missing",
            system_area="PCS",
            owner="Electrical supervisor",
            evidence_link="-",  # missing evidence
            target_close_date="2026-07-25",
            status="Ready for verification",
            closeout_note="Replacement ordered.",
        )
        issues = audit_punch_list([record], AS_OF)
        self.assertTrue(any(issue.kind == "missing_closeout_evidence" for issue in issues))

    def test_owner_field_missing(self):
        record = PunchListRecord(
            source="test.md",
            line=10,
            item_id="PL-003",
            severity="Minor",
            finding="Cabinet door latch loose",
            system_area="Enclosure",
            owner="TBD",
            evidence_link="-",
            target_close_date="2026-07-25",
            status="Open",
            closeout_note="-",
        )
        issues = audit_punch_list([record], AS_OF)
        self.assertTrue(any(issue.kind == "missing_required_field" for issue in issues))

    def test_required_evidence_id_missing(self):
        check = CheckRecord(
            source="test.md",
            line=10,
            check_id="CHK-001",
            item="Trip test",
            evidence_ids=(),  # missing evidence IDs
            acceptance_reference="ITP-001",
            owner="Engineer",
            status="Ready for verification",
        )
        issues = audit_traceability([check], [])
        self.assertTrue(any(issue.kind == "missing_evidence_reference" for issue in issues))

    def test_referenced_evidence_revision_is_inconsistent(self):
        check = CheckRecord(
            source="test.md",
            line=10,
            check_id="CHK-001",
            item="Trip test",
            evidence_ids=("EVD-001",),
            acceptance_reference="ITP-001",
            owner="Engineer",
            status="Open",
        )
        evidence = EvidenceRecord(
            source="test.md",
            line=20,
            evidence_id="EVD-001",
            location="DMS/test.pdf",
            revision="bad revision syntax %!",
            approval_status="Approved",
        )
        issues = audit_traceability([check], [evidence])
        self.assertTrue(any(issue.kind == "invalid_revision" for issue in issues))

    def test_unauthorized_deferral_rejected(self):
        policy = load_handover_policy(ROOT / "config" / "handover-acceptance-policy.example.json")
        punch = PunchItem(
            source="test.md",
            line=10,
            item_id="PL-001",
            severity="Minor",
            finding="Painting scratch",
            owner="Painter",
            evidence_link="records/touchup.pdf",
            target_close_date="2026-08-01",
            status="Deferred",
            closeout_note="Touchup scheduled.",
        )
        # No residual risk record provided for this deferred item
        issues = audit_handover([punch], [], [], policy)
        self.assertTrue(any(issue.kind == "unapproved_deferral" for issue in issues))

    def test_duplicate_finding_identifiers_detected(self):
        rec1 = PunchListRecord(
            source="test.md",
            line=10,
            item_id="PL-001",
            severity="Minor",
            finding="Issue 1",
            system_area="PCS",
            owner="Tech 1",
            evidence_link="-",
            target_close_date="2026-07-25",
            status="Open",
            closeout_note="-",
        )
        rec2 = PunchListRecord(
            source="test.md",
            line=11,
            item_id="PL-001",  # duplicate
            severity="Minor",
            finding="Issue 2",
            system_area="PCS",
            owner="Tech 2",
            evidence_link="-",
            target_close_date="2026-07-25",
            status="Open",
            closeout_note="-",
        )
        issues = audit_punch_list([rec1, rec2], AS_OF)
        self.assertTrue(any(issue.kind == "duplicate_item_id" for issue in issues))

    def test_invalid_status_value_rejected(self):
        record = PunchListRecord(
            source="test.md",
            line=10,
            item_id="PL-001",
            severity="Minor",
            finding="Issue",
            system_area="PCS",
            owner="Tech",
            evidence_link="-",
            target_close_date="2026-07-25",
            status="WaitingOnReviewer",  # not in vocabulary
            closeout_note="-",
        )
        issues = audit_punch_list([record], AS_OF)
        self.assertTrue(any(issue.kind == "invalid_status" for issue in issues))

    def test_invalid_target_date_detected(self):
        record = PunchListRecord(
            source="test.md",
            line=10,
            item_id="PL-001",
            severity="Minor",
            finding="Issue",
            system_area="PCS",
            owner="Tech",
            evidence_link="-",
            target_close_date="2026-13-45",  # invalid date
            status="Open",
            closeout_note="-",
        )
        issues = audit_punch_list([record], AS_OF)
        self.assertTrue(any(issue.kind == "invalid_target_close_date" for issue in issues))

    def test_overdue_active_critical_and_major_escalation(self):
        crit = PunchListRecord(
            source="test.md",
            line=10,
            item_id="NCR-001",
            severity="Critical",
            finding="Critical safety bug",
            system_area="Fire safety",
            owner="Lead",
            evidence_link="-",
            target_close_date="2026-07-10",  # overdue as of 2026-07-21
            status="In progress",
            closeout_note="-",
        )
        maj = PunchListRecord(
            source="test.md",
            line=11,
            item_id="PL-002",
            severity="Major",
            finding="Inverter trip timing",
            system_area="PCS",
            owner="Lead",
            evidence_link="-",
            target_close_date="2026-07-10",  # overdue as of 2026-07-21
            status="In progress",
            closeout_note="-",
        )
        issues = audit_punch_list([crit, maj], AS_OF)
        self.assertTrue(any(issue.kind == "overdue_critical_item" for issue in issues))
        self.assertTrue(any(issue.kind == "overdue_major_item" for issue in issues))

    def test_repeated_defects_trend_aggregation(self):
        records = [
            PunchListRecord(
                source="test.md",
                line=10 + i,
                item_id=f"PL-00{i+1}",
                severity="Major",
                finding=f"Defect {i+1}",
                system_area="Fire safety interface",
                owner="Lead",
                evidence_link="-",
                target_close_date="2026-07-25",
                status="Open",
                closeout_note="-",
            )
            for i in range(3)
        ]
        summary = summarize_punch_list(records, [], AS_OF)
        self.assertEqual(summary["system_area_counts"]["Fire safety interface"], 3)
        self.assertIn("Fire safety interface", summary["recurring_areas"])

    def test_calibration_expired_or_invalid(self):
        meas = MeasurementRecord(
            source="test.md",
            line=10,
            measurement_id="MEAS-001",
            check_id="CHK-001",
            item="Current test",
            instrument_ids=("INS-001",),
            test_date="2026-07-21",
            owner="Tech",
            status="Completed",
        )
        # Calibration expired on 2026-06-30
        cal = CalibrationRecord(
            source="test.md",
            line=20,
            calibration_id="CAL-001",
            instrument_id="INS-001",
            valid_from="2025-07-01",
            valid_through="2026-06-30",
            approval_status="Approved",
            certificate_location="DMS/cal.pdf",
        )
        issues = audit_calibration_traceability([meas], [cal], as_of=AS_OF)
        self.assertTrue(any(issue.kind == "no_calibration_at_test_date" for issue in issues))

    def test_completed_record_with_tbd_not_accepted(self):
        policy = load_completeness_policy(ROOT / "config" / "readiness-completeness-policy.example.json")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.md"
            path.write_text(
                "# Test\n\n"
                "| Item | Owner | Target Close Date | Evidence Link | Status |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| Battery inspection | TBD | 2026-08-01 | photo.jpg | In progress |\n",
                encoding="utf-8",
            )
            matches, violations = extract_completeness_results(path, policy)
            self.assertEqual(len(matches), 1)
            self.assertEqual(len(violations), 1)
            self.assertEqual(violations[0].field, "accountable owner")

    def test_blank_reusable_template_structurally_valid(self):
        templates = sorted((ROOT / "templates").glob("*.md"))
        self.assertGreater(len(templates), 30)
        for template in templates:
            errors = validate_template(template, strict_governance=True)
            self.assertEqual(errors, [], f"Template {template.name} failed validation: {errors}")

    def test_malformed_markdown_table_controlled_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "malformed.md"
            path.write_text(
                "# Malformed\n\n"
                "| Col1 | Col2 | Col3 |\n"
                "| --- | --- | --- |\n"
                "| Val1 | Val2 |\n",  # 2 cells vs 3 header columns
                encoding="utf-8",
            )
            errors = validate_template(path)
            self.assertTrue(any("expected 3" in msg for _, msg in errors))

    def test_escaped_pipe_in_cell_parsed_without_column_corruption(self):
        line = r"| Item | Inverter AC \| DC interface | Open |"
        cells = table_cells(line)
        self.assertEqual(len(cells), 3)
        self.assertEqual(cells[1], r"Inverter AC \| DC interface")

    def test_invalid_configuration_json_clear_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_policy.json"
            path.write_text('{"unknown_key": 123}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown fields"):
                load_status_policy(path)

    def test_unsafe_input_path_rejected(self):
        with tempfile.TemporaryDirectory() as base_dir:
            base_path = Path(base_dir)
            with tempfile.TemporaryDirectory() as outside_dir:
                outside_file = Path(outside_dir) / "outside.md"
                outside_file.write_text("# Outside\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "escapes allowed boundary"):
                    expand_paths([outside_file], base_boundary=base_path)

    def test_deterministic_reproducible_evaluation(self):
        rec = PunchListRecord(
            source="test.md",
            line=10,
            item_id="PL-001",
            severity="Minor",
            finding="Workmanship",
            system_area="PCS",
            owner="Tech",
            evidence_link="photo.jpg",
            target_close_date="2026-07-25",
            status="Ready for verification",
            closeout_note="Installed.",
        )
        res1 = audit_punch_list([rec], AS_OF)
        res2 = audit_punch_list([rec], AS_OF)
        self.assertEqual(res1, res2)

    def test_synthetic_dashboard_result_distinguished_from_field_evidence(self):
        lesson_config_path = ROOT / "docs" / "lesson-config.json"
        self.assertTrue(lesson_config_path.is_file())
        config = json.loads(lesson_config_path.read_text(encoding="utf-8"))
        # Verify educational and synthetic nature is explicitly declared
        self.assertIn("modules", config)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("teaching simulations", readme)


if __name__ == "__main__":
    unittest.main()
