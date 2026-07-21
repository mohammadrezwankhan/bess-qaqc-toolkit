from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

from scripts.audit_calibration_traceability import (
    audit_calibration_traceability,
    extract_calibration_records,
    main,
    render_markdown,
    summarize_calibration_traceability,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "examples" / "calibration-traceability-passing.md"


class CalibrationTraceabilityTests(unittest.TestCase):
    def setUp(self):
        self.measurements, self.calibrations = extract_calibration_records(
            EXAMPLE_PATH
        )

    def kinds(self, measurements=None, calibrations=None, **options):
        issues = audit_calibration_traceability(
            self.measurements if measurements is None else measurements,
            self.calibrations if calibrations is None else calibrations,
            **options,
        )
        return [issue.kind for issue in issues]

    def test_extracts_measurements_and_recalibration_history(self):
        self.assertEqual(len(self.measurements), 3)
        self.assertEqual(len(self.calibrations), 4)
        self.assertEqual(
            self.measurements[1].instrument_ids,
            ("INS-002", "INS-003"),
        )
        self.assertEqual(
            [
                record.calibration_id
                for record in self.calibrations
                if record.instrument_id == "INS-001"
            ],
            ["CAL-001", "CAL-002"],
        )

    def test_passing_example_has_no_issues(self):
        self.assertEqual(self.kinds(), [])

    def test_planned_measurement_can_fall_outside_calibration_history(self):
        self.assertEqual(self.measurements[2].status, "Planned")
        self.assertEqual(self.measurements[2].test_date, "2028-02-10")
        self.assertNotIn("no_calibration_at_test_date", self.kinds())

    def test_audit_date_rejects_only_future_completed_measurements(self):
        measurements = [
            replace(self.measurements[0], test_date="2026-07-22"),
            *self.measurements[1:],
        ]
        kinds = self.kinds(measurements=measurements, as_of=date(2026, 7, 21))

        self.assertIn("future_completed_measurement", kinds)
        self.assertEqual(
            self.kinds(as_of=date(2026, 7, 21)).count(
                "future_completed_measurement"
            ),
            0,
        )

    def test_completed_measurement_requires_covering_calibration(self):
        measurements = [
            replace(self.measurements[0], test_date="2025-01-15"),
            *self.measurements[1:],
        ]
        self.assertIn(
            "no_calibration_at_test_date",
            self.kinds(measurements=measurements),
        )

    def test_calibration_period_boundaries_are_inclusive(self):
        for test_date in ("2025-12-01", "2026-11-30"):
            with self.subTest(test_date=test_date):
                measurements = [
                    replace(self.measurements[0], test_date=test_date),
                    *self.measurements[1:],
                ]
                self.assertEqual(self.kinds(measurements=measurements), [])

    def test_completed_measurement_requires_accepted_calibration(self):
        calibrations = [
            replace(self.calibrations[0], approval_status="Pending review"),
            *self.calibrations[1:],
        ]
        self.assertIn(
            "unaccepted_calibration",
            self.kinds(calibrations=calibrations),
        )

    def test_overlapping_periods_are_rejected_at_test_date(self):
        overlap = replace(
            self.calibrations[0],
            calibration_id="CAL-005",
            valid_from="2026-01-01",
            valid_through="2026-12-31",
        )
        self.assertIn(
            "overlapping_calibrations",
            self.kinds(calibrations=[*self.calibrations, overlap]),
        )

    def test_unknown_and_repeated_instrument_references_are_reported(self):
        measurements = [
            replace(
                self.measurements[0],
                instrument_ids=("INS-999", "INS-999"),
            ),
            *self.measurements[1:],
        ]
        kinds = self.kinds(measurements=measurements)
        self.assertIn("duplicate_instrument_reference", kinds)
        self.assertIn("unknown_instrument_reference", kinds)

    def test_invalid_identifiers_and_case_insensitive_duplicates_are_reported(self):
        duplicate = replace(
            self.calibrations[0],
            calibration_id="cal-001",
        )
        kinds = self.kinds(calibrations=[*self.calibrations, duplicate])
        self.assertIn("invalid_calibration_id", kinds)
        self.assertIn("duplicate_calibration_id", kinds)

    def test_duplicate_ids_do_not_share_date_cache_entries(self):
        duplicate_measurement = replace(
            self.measurements[0],
            measurement_id="MEAS-001",
            test_date="2025-01-15",
        )
        duplicate_calibration = replace(
            self.calibrations[0],
            calibration_id="CAL-001",
            valid_from="2027-01-01",
            valid_through="2027-12-31",
        )
        kinds = self.kinds(
            measurements=[*self.measurements, duplicate_measurement],
            calibrations=[*self.calibrations, duplicate_calibration],
        )
        self.assertIn("duplicate_measurement_id", kinds)
        self.assertIn("duplicate_calibration_id", kinds)
        self.assertIn("no_calibration_at_test_date", kinds)
        self.assertNotIn("overlapping_calibrations", kinds)

    def test_invalid_test_and_calibration_dates_are_reported(self):
        measurements = [
            replace(self.measurements[0], test_date="21-07-2026"),
            *self.measurements[1:],
        ]
        calibrations = [
            replace(
                self.calibrations[0],
                valid_from="2026-12-01",
                valid_through="2026-01-01",
            ),
            replace(self.calibrations[1], valid_through="2027/11/30"),
            *self.calibrations[2:],
        ]
        kinds = self.kinds(
            measurements=measurements,
            calibrations=calibrations,
        )
        self.assertIn("invalid_test_date", kinds)
        self.assertIn("invalid_calibration_period", kinds)
        self.assertIn("invalid_valid_through", kinds)

    def test_missing_required_fields_are_reported(self):
        measurements = [
            replace(
                self.measurements[0],
                owner="TBD",
                instrument_ids=(),
            ),
            *self.measurements[1:],
        ]
        calibrations = [
            replace(self.calibrations[0], certificate_location="-"),
            *self.calibrations[1:],
        ]
        kinds = self.kinds(
            measurements=measurements,
            calibrations=calibrations,
        )
        self.assertIn("missing_measurement_field", kinds)
        self.assertIn("missing_instrument_reference", kinds)
        self.assertIn("missing_calibration_field", kinds)

    def test_project_status_vocabularies_can_replace_defaults(self):
        measurements = [
            replace(self.measurements[0], status="Verified"),
            *self.measurements[1:],
        ]
        calibrations = [
            replace(self.calibrations[0], approval_status="Released"),
            *self.calibrations[1:],
        ]
        kinds = self.kinds(
            measurements=measurements,
            calibrations=calibrations,
            completed_statuses=("Verified",),
            accepted_calibration_statuses=("Released",),
        )
        self.assertNotIn("unaccepted_calibration", kinds)

    def test_summary_and_markdown_preserve_date_coverage(self):
        summary = summarize_calibration_traceability(
            self.measurements,
            self.calibrations,
            [],
            as_of=date(2026, 7, 21),
        )
        self.assertEqual(summary["as_of"], "2026-07-21")
        self.assertEqual(summary["instrument_count"], 3)
        self.assertEqual(
            summary["measurements"][0]["covering_calibration_ids"],
            ["CAL-001"],
        )
        self.assertEqual(
            summary["calibrations"][0]["instrument_used_by"],
            ["MEAS-001", "MEAS-003"],
        )
        rendered = render_markdown(summary)
        self.assertIn("# Instrument Calibration Traceability Audit", rendered)
        self.assertIn("As of: 2026-07-21", rendered)
        self.assertIn("## Measurement Coverage", rendered)
        self.assertIn("## Calibration History", rendered)

    def test_generated_report_is_not_ingested_on_repeat_scan(self):
        summary = summarize_calibration_traceability(
            self.measurements,
            self.calibrations,
            [],
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            path.write_text(render_markdown(summary), encoding="utf-8")
            measurements, calibrations = extract_calibration_records(path)
        self.assertEqual(measurements, [])
        self.assertEqual(calibrations, [])

    def test_extraction_rejects_missing_columns_and_bad_row_width(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.md"
            path.write_text(
                "# Record\n\nIntro.\n\n"
                "| Measurement ID | Check ID | Measurement or Test | "
                "Instrument IDs | Test Date | Status |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| MEAS-001 | CHK-001 | Test | INS-001 | 2026-01-01 | "
                "Completed |\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing required column"):
                extract_calibration_records(path)

            path.write_text(
                "# Record\n\nIntro.\n\n"
                "| Measurement ID | Check ID | Measurement or Test | "
                "Instrument IDs | Test Date | Owner | Status |\n"
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                "| MEAS-001 | CHK-001 | Test | INS-001 | 2026-01-01 | "
                "Completed |\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "table row has 6 cells"):
                extract_calibration_records(path)

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
        self.assertEqual(report["as_of"], "2026-07-21")
        self.assertEqual(report["issue_count"], 0)
        self.assertEqual(report["completed_measurement_count"], 2)

    def test_cli_writes_failure_report_and_returns_two(self):
        document = EXAMPLE_PATH.read_text(encoding="utf-8").replace(
            "| CAL-001 | INS-001 | 2025-12-01 |",
            "| CAL-001 | INS-001 | 2026-02-01 |",
        )
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "record.md"
            output_path = Path(directory) / "reports" / "calibration.md"
            input_path.write_text(document, encoding="utf-8")
            standard_error = io.StringIO()
            with contextlib.redirect_stderr(standard_error):
                exit_code = main(
                    [str(input_path), "--output", str(output_path)]
                )
            self.assertEqual(exit_code, 2)
            self.assertTrue(output_path.is_file())
            self.assertIn("no_calibration_at_test_date", standard_error.getvalue())

    def test_cli_returns_one_when_a_register_is_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "record.md"
            input_path.write_text("# Empty\n", encoding="utf-8")
            standard_error = io.StringIO()
            with contextlib.redirect_stderr(standard_error):
                exit_code = main([str(input_path)])
        self.assertEqual(exit_code, 1)
        self.assertIn("no measurement-use rows found", standard_error.getvalue())

    def test_cli_rejects_duplicate_option_values(self):
        standard_error = io.StringIO()
        with contextlib.redirect_stderr(standard_error):
            exit_code = main(
                [
                    str(EXAMPLE_PATH),
                    "--completed-status",
                    "Complete",
                    "--completed-status",
                    "complete",
                ]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("case-insensitive duplicates", standard_error.getvalue())


if __name__ == "__main__":
    unittest.main()
