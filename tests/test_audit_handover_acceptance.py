from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from scripts.audit_handover_acceptance import (
    audit_handover,
    extract_handover_records,
    load_handover_policy,
    main,
    render_markdown,
    summarize_handover,
)


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "handover-acceptance-policy.example.json"
EXAMPLE_PATH = ROOT / "examples" / "handover-acceptance-passing.md"


class HandoverAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_handover_policy(POLICY_PATH)
        self.punch, self.risks, self.decisions = extract_handover_records(EXAMPLE_PATH)

    def kinds(self, punch=None, risks=None, decisions=None):
        issues = audit_handover(
            self.punch if punch is None else punch,
            self.risks if risks is None else risks,
            self.decisions if decisions is None else decisions,
            self.policy,
        )
        return [issue.kind for issue in issues]

    def test_extracts_all_three_registers(self):
        self.assertEqual(len(self.punch), 3)
        self.assertEqual(len(self.risks), 1)
        self.assertEqual(len(self.decisions), 1)
        self.assertEqual(self.decisions[0].residual_risk_ids, ("RR-001",))

    def test_passing_example_has_no_issues(self):
        self.assertEqual(self.kinds(), [])

    def test_deferred_item_requires_accepted_residual_risk(self):
        self.assertIn("unapproved_deferral", self.kinds(risks=[]))

    def test_active_risk_requires_registered_deferred_source(self):
        risk = replace(self.risks[0], source_item_id="PL-999")
        kinds = self.kinds(risks=[risk])
        self.assertIn("unknown_source_item", kinds)
        self.assertIn("unapproved_deferral", kinds)

    def test_active_risk_rejects_non_deferred_source(self):
        risk = replace(self.risks[0], source_item_id="PL-003")
        self.assertIn("active_risk_source_not_deferred", self.kinds(risks=[risk]))

    def test_multiple_active_risks_for_one_item_are_rejected(self):
        second = replace(self.risks[0], risk_id="RR-002")
        self.assertIn("multiple_active_risks", self.kinds(risks=[*self.risks, second]))

    def test_critical_item_cannot_be_deferred_by_default(self):
        punch = [
            replace(item, severity="Critical") if item.item_id == "PL-002" else item
            for item in self.punch
        ]
        self.assertIn("non_deferrable_item", self.kinds(punch=punch))

    def test_release_rejects_open_major_item(self):
        punch = [
            replace(item, severity="Major") if item.item_id == "PL-003" else item
            for item in self.punch
        ]
        self.assertIn("acceptance_blocker", self.kinds(punch=punch))

    def test_unknown_severity_cannot_bypass_release_blocker(self):
        punch = [
            replace(item, severity="Majro") if item.item_id == "PL-003" else item
            for item in self.punch
        ]
        self.assertIn("unknown_severity", self.kinds(punch=punch))

    def test_unconditional_acceptance_rejects_active_deferral(self):
        decision = replace(self.decisions[0], decision="Accepted", residual_risk_ids=())
        self.assertIn(
            "unconditional_acceptance_with_deferrals",
            self.kinds(decisions=[decision]),
        )

    def test_conditional_acceptance_must_list_every_active_risk(self):
        decision = replace(self.decisions[0], residual_risk_ids=())
        self.assertIn("unlisted_residual_risk", self.kinds(decisions=[decision]))

    def test_acceptance_rejects_unknown_and_duplicate_risk_references(self):
        decision = replace(
            self.decisions[0],
            residual_risk_ids=("RR-001", "RR-001", "RR-999"),
        )
        kinds = self.kinds(decisions=[decision])
        self.assertIn("duplicate_risk_reference", kinds)
        self.assertIn("unknown_risk_reference", kinds)

    def test_closed_item_requires_evidence_and_verification(self):
        punch = [
            replace(item, evidence_link="TBD", closeout_note="-")
            if item.item_id == "PL-001"
            else item
            for item in self.punch
        ]
        kinds = self.kinds(punch=punch)
        self.assertIn("missing_closeout_evidence", kinds)
        self.assertIn("missing_closeout_note", kinds)

    def test_closed_risk_requires_closed_source(self):
        risk = replace(self.risks[0], status="Closed")
        self.assertIn("closed_risk_source_not_closed", self.kinds(risks=[risk]))

    def test_duplicate_identifiers_are_case_insensitive(self):
        duplicate = replace(self.risks[0], risk_id="rr-001")
        kinds = self.kinds(risks=[*self.risks, duplicate])
        self.assertIn("invalid_risk_id", kinds)
        self.assertIn("duplicate_risk_id", kinds)

    def test_summary_and_markdown_preserve_decision(self):
        summary = summarize_handover(
            self.punch,
            self.risks,
            self.decisions,
            [],
            self.policy,
        )
        self.assertEqual(summary["deferred_item_count"], 1)
        self.assertEqual(summary["active_residual_risk_count"], 1)
        rendered = render_markdown(summary)
        self.assertIn("# Handover Acceptance Audit", rendered)
        self.assertIn("## Punch-List Items", rendered)
        self.assertIn("## Residual-Risk Register", rendered)
        self.assertIn("Conditionally accepted", rendered)

    def test_pending_decision_does_not_require_release_signatures(self):
        decision = replace(
            self.decisions[0],
            decision="Pending",
            residual_risk_ids=(),
            approved_by="",
            approval_date="",
            evidence_location="",
        )
        self.assertEqual(self.kinds(decisions=[decision]), [])

    def test_policy_rejects_overlapping_status_classifications(self):
        document = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        document["closed_punch_statuses"].append("Open")
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "policy.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "classifications overlap"):
            load_handover_policy(path)

    def test_cli_emits_json_for_passing_record(self):
        standard_output = io.StringIO()
        with contextlib.redirect_stdout(standard_output):
            exit_code = main(
                [
                    str(EXAMPLE_PATH),
                    "--policy",
                    str(POLICY_PATH),
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(exit_code, 0)
        report = json.loads(standard_output.getvalue())
        self.assertEqual(report["issue_count"], 0)

    def test_cli_writes_failure_report_and_returns_two(self):
        document = EXAMPLE_PATH.read_text(encoding="utf-8").replace(
            "| PL-003 | Minor |", "| PL-003 | Major |"
        )
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        input_path = Path(directory.name) / "record.md"
        output_path = Path(directory.name) / "reports" / "handover.md"
        input_path.write_text(document, encoding="utf-8")
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main(
                [
                    str(input_path),
                    "--policy",
                    str(POLICY_PATH),
                    "--output",
                    str(output_path),
                ]
            )
        self.assertEqual(exit_code, 2)
        self.assertTrue(output_path.is_file())
        self.assertIn("acceptance_blocker", standard_error.getvalue())

    def test_cli_returns_one_when_a_register_is_missing(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        input_path = Path(directory.name) / "record.md"
        input_path.write_text("# Empty\n", encoding="utf-8")
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main(
                [
                    str(input_path),
                    "--policy",
                    str(POLICY_PATH),
                ]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("no punch-list rows found", standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
