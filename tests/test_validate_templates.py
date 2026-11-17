from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_templates import (
    is_table_row,
    table_cells,
    validate_template,
)


VALID_TEMPLATE = """# FAT Evidence Log

Use this template to record controlled FAT evidence.

## Evidence

| Item | Owner | Status |
|---|---|---|
| Test report | QA/QC | Open |
"""


class TemplateValidatorTests(unittest.TestCase):
    def validate_text(self, content: str) -> list[tuple[int, str]]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "template.md"
            path.write_text(content, encoding="utf-8")
            return validate_template(path)

    def test_accepts_well_formed_template(self):
        self.assertEqual(self.validate_text(VALID_TEMPLATE), [])

    def test_requires_single_h1(self):
        content = VALID_TEMPLATE + "\n# Duplicate title\n"
        errors = self.validate_text(content)
        self.assertTrue(any("exactly one H1" in message for _, message in errors))

    def test_requires_introductory_paragraph(self):
        content = VALID_TEMPLATE.replace(
            "Use this template to record controlled FAT evidence.\n\n", ""
        )
        errors = self.validate_text(content)
        self.assertTrue(
            any("introductory paragraph" in message for _, message in errors)
        )

    def test_rejects_invalid_separator(self):
        content = VALID_TEMPLATE.replace("|---|---|---|", "|--|---|---|")
        errors = self.validate_text(content)
        self.assertTrue(any("table separator" in message for _, message in errors))

    def test_rejects_inconsistent_row_width(self):
        content = VALID_TEMPLATE.replace(
            "| Test report | QA/QC | Open |", "| Test report | Open |"
        )
        errors = self.validate_text(content)
        self.assertTrue(any("expected 3" in message for _, message in errors))

    def test_requires_at_least_one_table(self):
        content = """# FAT Evidence Log

Use this template to record controlled FAT evidence.

## Evidence

- Test report
"""
        errors = self.validate_text(content)
        self.assertTrue(
            any("at least one Markdown table" in message for _, message in errors)
        )

    def test_table_cells_supports_escaped_pipe(self):
        line = r"| Item | Inverter AC \| DC check | Open |"
        cells = table_cells(line)
        self.assertEqual(len(cells), 3)
        self.assertEqual(cells[1], r"Inverter AC \| DC check")

    def test_is_table_row_ignores_escaped_pipe(self):
        line = r"| this is not a table row \|"
        self.assertFalse(is_table_row(line))
        valid_row = r"| valid | row |"
        self.assertTrue(is_table_row(valid_row))

    def test_strict_governance_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "template.md"
            path.write_text(VALID_TEMPLATE, encoding="utf-8")
            errors = validate_template(path, strict_governance=True)
            self.assertTrue(any("strict governance requires" in msg for _, msg in errors))

            governed = (
                VALID_TEMPLATE
                + "\n## Closeout Prompts\n\n"
                "- What evidence would defend this decision in a later audit?\n"
                "- Does the finding affect safety, energization, warranty, grid compliance, or documentation?\n"
                "- Who owns the next action and when is it reviewed again under the review cadence?\n"
                "- Which unresolved residual risk should be visible in the final acceptance package?\n"
            )
            path.write_text(governed, encoding="utf-8")
            clean_errors = validate_template(path, strict_governance=True)
            self.assertEqual(clean_errors, [])


if __name__ == "__main__":
    unittest.main()
