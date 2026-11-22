from __future__ import annotations

import contextlib
import io
import json
import unittest
from datetime import date
from pathlib import Path
from typing import Any

from scripts import (
    audit_calibration_traceability,
    audit_completeness,
    audit_deadlines,
    audit_document_control,
    audit_evidence_traceability,
    audit_handover_acceptance,
    audit_punch_list,
    audit_readiness,
    summarize_status,
)


ROOT = Path(__file__).resolve().parents[1]
AS_OF = "2026-07-21"


def _json_schema_issues(
    value: Any,
    schema: dict[str, Any],
    path: str = "$",
    root: dict[str, Any] | None = None,
) -> list[str]:
    """Validate the JSON Schema keywords used by checked-in report contracts."""

    root = schema if root is None else root
    if "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/"):
            return [f"{path}: unsupported schema reference {reference!r}"]
        target: Any = root
        for part in reference[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return _json_schema_issues(value, target, path, root)

    issues: list[str] = []
    allowed_types = schema.get("type")
    if allowed_types is not None:
        if isinstance(allowed_types, str):
            allowed_types = [allowed_types]
        type_matches = {
            "object": lambda item: isinstance(item, dict),
            "array": lambda item: isinstance(item, list),
            "string": lambda item: isinstance(item, str),
            "integer": lambda item: isinstance(item, int)
            and not isinstance(item, bool),
            "number": lambda item: isinstance(item, (int, float))
            and not isinstance(item, bool),
            "boolean": lambda item: isinstance(item, bool),
            "null": lambda item: item is None,
        }
        if not any(type_matches[kind](value) for kind in allowed_types):
            return [f"{path}: expected {allowed_types}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        issues.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        issues.append(f"{path}: value is outside the declared enum")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", value):
            issues.append(f"{path}: value is below minimum {schema['minimum']}")
    if isinstance(value, str) and schema.get("format") == "date":
        try:
            if date.fromisoformat(value).isoformat() != value:
                raise ValueError
        except ValueError:
            issues.append(f"{path}: expected an ISO calendar date")

    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                issues.append(f"{path}: missing required field {name!r}")
        properties = schema.get("properties", {})
        for name, child_schema in properties.items():
            if name in value:
                issues.extend(
                    _json_schema_issues(
                        value[name], child_schema, f"{path}.{name}", root
                    )
                )
        additional = schema.get("additionalProperties", True)
        for name in value.keys() - properties.keys():
            if additional is False:
                issues.append(f"{path}: unexpected field {name!r}")
            elif isinstance(additional, dict):
                issues.extend(
                    _json_schema_issues(value[name], additional, f"{path}.{name}", root)
                )

    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            issues.extend(
                _json_schema_issues(item, schema["items"], f"{path}[{index}]", root)
            )
    return issues


class CliJsonContractTests(unittest.TestCase):
    def test_public_json_clis_match_their_v1_contracts(self):
        cases = (
            (
                "status-summary",
                summarize_status.main,
                ["examples/readiness-gate-passing-record.md", "--format", "json"],
            ),
            (
                "deadline-audit",
                audit_deadlines.main,
                [
                    "examples/punch-list-closeout-passing.md",
                    "--as-of",
                    AS_OF,
                    "--format",
                    "json",
                ],
            ),
            (
                "completeness-audit",
                audit_completeness.main,
                [
                    "examples/readiness-gate-passing-record.md",
                    "--policy",
                    "config/readiness-completeness-policy.example.json",
                    "--format",
                    "json",
                ],
            ),
            (
                "readiness-report",
                audit_readiness.main,
                [
                    "examples/readiness-gate-passing-record.md",
                    "--status-policy",
                    "config/readiness-status-policy.example.json",
                    "--completeness-policy",
                    "config/readiness-completeness-policy.example.json",
                    "--as-of",
                    AS_OF,
                    "--require-source-coverage",
                    "--format",
                    "json",
                ],
            ),
            (
                "evidence-traceability",
                audit_evidence_traceability.main,
                [
                    "examples/commissioning-evidence-traceability-passing.md",
                    "--format",
                    "json",
                ],
            ),
            (
                "calibration-traceability",
                audit_calibration_traceability.main,
                [
                    "examples/calibration-traceability-passing.md",
                    "--format",
                    "json",
                ],
            ),
            (
                "punch-list-audit",
                audit_punch_list.main,
                [
                    "examples/punch-list-closeout-passing.md",
                    "--as-of",
                    AS_OF,
                    "--format",
                    "json",
                ],
            ),
            (
                "handover-acceptance",
                audit_handover_acceptance.main,
                [
                    "examples/handover-acceptance-passing.md",
                    "--policy",
                    "config/handover-acceptance-policy.example.json",
                    "--format",
                    "json",
                ],
            ),
            (
                "document-control",
                audit_document_control.main,
                [
                    "examples/document-control-passing.md",
                    "--as-of",
                    AS_OF,
                    "--format",
                    "json",
                ],
            ),
        )

        for contract_name, main, arguments in cases:
            with self.subTest(contract=contract_name):
                output = io.StringIO()
                errors = io.StringIO()
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(
                    errors
                ):
                    exit_code = main(arguments)

                self.assertEqual(exit_code, 0, errors.getvalue())
                self.assertEqual(errors.getvalue(), "")
                payload = json.loads(output.getvalue())
                schema_path = ROOT / "config" / f"{contract_name}-v1.schema.json"
                schema = json.loads(schema_path.read_text(encoding="utf-8"))

                self.assertTrue(schema["$id"].endswith(f"{contract_name}-v1"))
                self.assertEqual(set(schema["required"]), set(schema["properties"]))
                if contract_name == "readiness-report":
                    self.assertEqual(payload["schema_version"], 1)
                else:
                    self.assertNotIn("schema_version", payload)

                issues = _json_schema_issues(payload, schema)
                self.assertEqual(issues, [])

    def test_past_due_report_preserves_signed_offsets_and_issue_shape(self):
        deadline_output = io.StringIO()
        with contextlib.redirect_stdout(deadline_output):
            deadline_exit = audit_deadlines.main(
                [
                    "examples/punch-list-closeout-passing.md",
                    "--as-of",
                    "2026-11-22",
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(deadline_exit, 0)
        deadline_payload = json.loads(deadline_output.getvalue())
        deadline_schema = json.loads(
            (ROOT / "config" / "deadline-audit-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(
            any(item["days_to_deadline"] < 0 for item in deadline_payload["items"])
        )
        self.assertEqual(_json_schema_issues(deadline_payload, deadline_schema), [])

        punch_output = io.StringIO()
        with contextlib.redirect_stdout(punch_output), contextlib.redirect_stderr(
            io.StringIO()
        ):
            punch_exit = audit_punch_list.main(
                [
                    "examples/punch-list-closeout-passing.md",
                    "--as-of",
                    "2026-11-22",
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(punch_exit, 2)
        punch_payload = json.loads(punch_output.getvalue())
        punch_schema = json.loads(
            (ROOT / "config" / "punch-list-audit-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreater(punch_payload["issue_count"], 0)
        self.assertTrue(punch_payload["issues"])
        self.assertTrue(
            any(item["days_to_target"] < 0 for item in punch_payload["items"])
        )
        self.assertEqual(_json_schema_issues(punch_payload, punch_schema), [])


if __name__ == "__main__":
    unittest.main()
