"""Run the browser export contract against the same helper used by the live page."""

import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TelemetryExportContractTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "Node.js is required for the dashboard export contract")
    def test_csv_and_context_metadata_contract(self):
        result = subprocess.run(
            [shutil.which("node"), str(ROOT / "tests" / "test_dashboard_export.js")],
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Telemetry CSV and context contract assertions passed.", result.stdout)


if __name__ == "__main__":
    unittest.main()
