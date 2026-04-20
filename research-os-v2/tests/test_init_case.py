from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_case.py"


class InitCaseScriptTests(unittest.TestCase):
    def test_init_case_scaffolds_prefilled_request(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "Company PC readiness",
                    "--base-dir",
                    tmp_dir,
                    "--as-of-date",
                    "2026-04-20",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            case_dir = Path(tmp_dir) / "2026-04-20-Company-PC-readiness"
            request_path = case_dir / "request.json"
            readme_path = case_dir / "README.md"
            notes_path = case_dir / "notes.md"
            bundle_dir = case_dir / "bundle"

            self.assertTrue(request_path.exists())
            self.assertTrue(readme_path.exists())
            self.assertTrue(notes_path.exists())
            self.assertTrue(bundle_dir.is_dir())

            payload = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["topic"], "Company PC readiness")
            self.assertIn("Company PC readiness", payload["reader"])
            self.assertIn("Company PC readiness", payload["use_context"])
            self.assertIn("Company PC readiness", payload["question"])
            self.assertEqual(payload["requested_mode"], "scoped")
            self.assertEqual(payload["output_type"], "report")
            self.assertEqual(payload["as_of_date"], "2026-04-20")
            self.assertEqual(payload["source_packets"], [])


if __name__ == "__main__":
    unittest.main()
