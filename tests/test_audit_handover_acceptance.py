from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from scripts.audit_handover_acceptance import (
    HandoverPolicy,
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

    def test_custom_missing_markers_keep_standard_release_placeholders(self):
        policy = replace(self.policy, missing_values=("Not recorded",))
        for approver in ("tBd", "Not recorded"):
            with self.subTest(approver=approver):
                decision = replace(
                    self.decisions[0], approved_by=approver, evidence_location="-"
                )
                issues = audit_handover(self.punch, self.risks, [decision], policy)
                self.assertEqual(
                    {issue.detail for issue in issues if issue.kind == "missing_acceptance_field"},
                    {
                        "approved by is required for a release decision",
                        "evidence location is required for a release decision",
                    },
                )

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

    def test_accepted_decision_rejects_open_critical_item(self):
        item = replace(self.punch[0], severity="Critical", status="Open")
        decision = replace(self.decisions[0], decision="Accepted", residual_risk_ids=())
        self.assertIn("acceptance_blocker", self.kinds(punch=[item], risks=[], decisions=[decision]))

    def test_audit_rejects_direct_policy_missing_critical_safety_membership(self):
        item = replace(self.punch[0], severity="Critical", status="Open")
        decision = replace(self.decisions[0], decision="Accepted", residual_risk_ids=())
        for field in (
            "severities",
            "blocking_severities",
            "non_deferrable_severities",
        ):
            with self.subTest(field=field):
                policy = replace(self.policy, **{field: ("Major",)})
                with self.assertRaisesRegex(
                    ValueError, f"policy {field} must include Critical"
                ):
                    audit_handover([item], [], [decision], policy)

    def test_audit_rejects_direct_policy_missing_critical_deferral_protection(self):
        item = replace(self.punch[1], severity="Critical")
        policy = replace(self.policy, non_deferrable_severities=("Major",))
        with self.assertRaisesRegex(
            ValueError, "policy non_deferrable_severities must include Critical"
        ):
            audit_handover(
                [self.punch[0], item, self.punch[2]],
                self.risks,
                self.decisions,
                policy,
            )

    def test_summary_rejects_direct_policy_missing_critical_safety_membership(self):
        for field in (
            "severities",
            "blocking_severities",
            "non_deferrable_severities",
        ):
            with self.subTest(field=field):
                policy = replace(self.policy, **{field: ("Major",)})
                with self.assertRaisesRegex(
                    ValueError, f"policy {field} must include Critical"
                ):
                    summarize_handover(
                        self.punch, self.risks, self.decisions, [], policy
                    )

    def test_direct_critical_only_rules_preserve_custom_major_behavior(self):
        policy = replace(
            self.policy,
            blocking_severities=("CRITICAL",),
            non_deferrable_severities=("critical",),
        )
        major_open = replace(
            self.punch[2], severity="Major", status="Open"
        )
        major_deferred = replace(self.punch[1], severity="Major")
        issues = audit_handover(
            [self.punch[0], major_deferred, major_open],
            self.risks,
            self.decisions,
            policy,
        )
        self.assertNotIn("acceptance_blocker", [issue.kind for issue in issues])
        self.assertNotIn("non_deferrable_item", [issue.kind for issue in issues])

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

    def test_closed_critical_item_rejects_self_assertion(self):
        item = replace(self.punch[0], severity="Critical", closeout_note="completed")
        self.assertIn("unverified_critical_closeout", self.kinds(punch=[item, *self.punch[1:]]))

    def test_closed_critical_item_rejects_owner_verification(self):
        item = replace(self.punch[0], severity="Critical", closeout_note="Verified by: Electrical supervisor; Result: Passed")
        self.assertIn("unverified_critical_closeout", self.kinds(punch=[item, *self.punch[1:]]))

    def test_closed_critical_item_accepts_independent_verification(self):
        item = replace(self.punch[0], severity="Critical", closeout_note="Verified by: Independent QA reviewer; Result: Passed")
        self.assertEqual(self.kinds(punch=[item, *self.punch[1:]]), [])

    def test_closed_major_item_rejects_self_assertion(self):
        item = replace(self.punch[0], severity="Major", closeout_note="completed")
        self.assertIn("unverified_closeout", self.kinds(punch=[item, *self.punch[1:]]))

    def test_punch_and_risk_dates_require_valid_calendar_dates(self):
        item = replace(self.punch[0], target_close_date="2026-02-30")
        risk = replace(self.risks[0], target_close_date="2026-13-15")
        self.assertEqual(
            self.kinds(punch=[item, *self.punch[1:]], risks=[risk]),
            ["invalid_target_close_date", "invalid_target_close_date"],
        )

    def test_release_approval_date_requires_valid_calendar_date(self):
        decision = replace(self.decisions[0], approval_date="2026-02-30")
        self.assertIn("invalid_approval_date", self.kinds(decisions=[decision]))

    def test_pending_approval_date_is_optional_but_must_be_valid_if_present(self):
        pending = replace(self.decisions[0], decision="Pending", approval_date="")
        self.assertNotIn("invalid_approval_date", self.kinds(decisions=[pending]))
        invalid = replace(pending, approval_date="20260228")
        self.assertIn("invalid_approval_date", self.kinds(decisions=[invalid]))

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

    def test_policy_requires_critical_in_each_safety_list(self):
        original = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"
            for field in ("severities", "blocking_severities", "non_deferrable_severities"):
                with self.subTest(field=field):
                    document = {**original, field: ["Major"]}
                    path.write_text(json.dumps(document), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, f"{field} must include Critical"):
                        load_handover_policy(path)
            document = {**original, "blocking_severities": ["Major"], "non_deferrable_severities": ["Major"]}
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must include Critical"):
                load_handover_policy(path)

    def test_policy_allows_custom_major_severity_rules(self):
        document = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        document.update(blocking_severities=["CRITICAL"], non_deferrable_severities=["critical"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            policy = load_handover_policy(path)
        self.assertEqual(policy.blocking_severities, ("CRITICAL",))

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

    def test_cli_requires_a_release_decision(self):
        example = EXAMPLE_PATH.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "handover.md"
            for decision in ("Pending", "Rejected"):
                with self.subTest(decision=decision):
                    path.write_text(
                        example.replace("Conditionally accepted", decision),
                        encoding="utf-8",
                    )
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                        result = main([str(path), "--format", "json"])
                    self.assertEqual(result, 2, stderr.getvalue())
                    report = json.loads(stdout.getvalue())
                    self.assertEqual(report["acceptance_decision_count"], 1)
                    self.assertEqual([issue["kind"] for issue in report["issues"]], [
                        "missing_release_decision",
                    ])

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

    def test_policy_requires_canonical_decisions(self):
        original = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"

            # Accepted moved to pending
            mutated = {
                **original,
                "release_decisions": ["Conditionally accepted"],
                "pending_decisions": ["Accepted", "Pending", "Rejected"],
            }
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "release_decisions must include Accepted"):
                load_handover_policy(path)

            # Conditionally accepted omitted from release_decisions
            mutated = {
                **original,
                "release_decisions": ["Accepted", "Special release"],
                "conditional_decisions": ["Special release"],
            }
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must include Conditionally accepted"):
                load_handover_policy(path)

            # Pending placed in release_decisions
            mutated = {
                **original,
                "release_decisions": ["Accepted", "Conditionally accepted", "Pending"],
                "pending_decisions": ["Rejected"],
            }
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "release_decisions cannot include Pending"):
                load_handover_policy(path)

    def test_policy_requires_canonical_punch_statuses(self):
        original = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"

            # Open omitted from open_punch_statuses and placed in closed_punch_statuses
            mutated = {
                **original,
                "open_punch_statuses": ["In progress", "Ready for verification"],
                "closed_punch_statuses": ["Closed", "Open"],
            }
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "open_punch_statuses must include Open"):
                load_handover_policy(path)

            # Deferred placed in open_punch_statuses
            mutated = {
                **original,
                "open_punch_statuses": ["Open", "In progress", "Ready for verification", "Deferred"],
                "deferred_punch_statuses": ["Hold"],
                "punch_statuses": ["Open", "In progress", "Ready for verification", "Deferred", "Closed", "Hold"],
            }
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "deferred_punch_statuses must include Deferred"):
                load_handover_policy(path)

    def test_direct_handover_policy_rejects_reclassified_semantics(self):
        original = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        mutated = {
            **original,
            "release_decisions": ["Conditionally accepted"],
            "pending_decisions": ["Accepted", "Pending", "Rejected"],
        }
        policy_obj = HandoverPolicy(**{k: tuple(v) for k, v in mutated.items()})
        with self.assertRaisesRegex(ValueError, "release_decisions must include Accepted"):
            audit_handover(self.punch, self.risks, self.decisions, policy_obj)

    def test_documented_open_statuses_cannot_be_reclassified(self):
        document = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"
            for status in ("In progress", "Ready for verification"):
                for category in ("closed_punch_statuses", "deferred_punch_statuses"):
                    changes = {
                        "open_punch_statuses": [
                            value for value in document["open_punch_statuses"] if value != status
                        ],
                        category: [*document[category], status],
                    }
                    path.write_text(json.dumps({**document, **changes}), encoding="utf-8")
                    policy = replace(self.policy, **{key: tuple(value) for key, value in changes.items()})
                    for entry, invoke in (
                        ("loader", lambda: load_handover_policy(path)),
                        ("audit", lambda: audit_handover(self.punch, self.risks, self.decisions, policy)),
                        ("summary", lambda: summarize_handover([], [], [], [], policy)),
                    ):
                        with self.subTest(status=status, category=category, entry=entry):
                            with self.assertRaisesRegex(ValueError, f"{status} must be an open punch status"):
                                invoke()

    def test_policy_allows_site_open_alias_without_optional_default_statuses(self):
        policy = replace(
            self.policy,
            punch_statuses=("Open", "Awaiting witness", "Closed", "Deferred"),
            open_punch_statuses=("Open", "Awaiting witness"),
        )
        punch = [
            replace(item, severity="Critical", status="Awaiting witness")
            if item.item_id == "PL-003" else item for item in self.punch
        ]
        issues = audit_handover(punch, self.risks, self.decisions, policy)
        self.assertEqual([issue.kind for issue in issues], ["acceptance_blocker"])

    def test_policy_classification_rules_apply_to_every_entry_point(self):
        original = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        mutations = (
            (
                {"closed_punch_statuses": ["Closed", "In progress"]},
                "classifications overlap",
            ),
            (
                {"punch_statuses": [*original["punch_statuses"], "Waiting"]},
                "exactly one classification",
            ),
            (
                {"blocking_severities": ["Critical", "Unknown"]},
                "contains an unknown severity",
            ),
            (
                {"closed_risk_statuses": original["accepted_risk_statuses"]},
                "risk statuses must not overlap",
            ),
            (
                {
                    "accepted_risk_statuses": ["Approved deferral"],
                    "closed_risk_statuses": ["Closed", "Accepted for deferred closeout"],
                },
                "Accepted for deferred closeout must be an active residual-risk status",
            ),
            (
                {
                    "accepted_risk_statuses": ["Accepted for deferred closeout", "Closed"],
                    "closed_risk_statuses": ["Verified complete"],
                },
                "Closed must be a closed residual-risk status",
            ),
            (
                {"conditional_decisions": ["Conditionally accepted", "Accepted"]},
                "Accepted cannot be conditional",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"
            for changes, message in mutations:
                document = {**original, **changes}
                path.write_text(json.dumps(document), encoding="utf-8")
                policy = replace(self.policy, **{key: tuple(value) for key, value in changes.items()})
                for entry, invoke in (
                    ("loader", lambda: load_handover_policy(path)),
                    ("audit", lambda: audit_handover([], [], [], policy)),
                    ("summary", lambda: summarize_handover([], [], [], [], policy)),
                ):
                    with self.subTest(changes=changes, entry=entry):
                        with self.assertRaisesRegex(ValueError, message):
                            invoke()


    def test_policy_allows_site_risk_status_aliases(self):
        policy = replace(
            self.policy,
            accepted_risk_statuses=("Approved deferral",),
            closed_risk_statuses=("Verified complete",),
        )
        risk = replace(self.risks[0], status="Approved deferral")
        self.assertEqual(audit_handover(self.punch, [risk], self.decisions, policy), [])

        closed_item = replace(
            self.punch[1],
            status="Closed",
            closeout_note="Verified by: Independent QA reviewer; Result: Passed",
        )
        decision = replace(self.decisions[0], decision="Accepted", residual_risk_ids=())
        closed_risk = replace(risk, status="Verified complete")
        self.assertEqual(
            audit_handover([self.punch[0], closed_item, self.punch[2]], [closed_risk], [decision], policy),
            [],
        )

    def test_open_critical_item_always_blocks_accepted_handover(self):
        item = replace(self.punch[0], severity="Critical", status="Open")
        decision = replace(self.decisions[0], decision="Accepted", residual_risk_ids=())
        issues = self.kinds(punch=[item, *self.punch[1:]], decisions=[decision])
        self.assertIn("acceptance_blocker", issues)


if __name__ == "__main__":
    unittest.main()
