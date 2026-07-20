from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_templates import validate_template


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


if __name__ == "__main__":
    unittest.main()
