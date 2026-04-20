from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.harness import run_fixture_case  # noqa: E402
from pseudo_pro_v2.runtime_paths import fixture_case_dir, generated_case_dir, normalize_path, package_root  # noqa: E402


class PortabilityRuntimeTests(unittest.TestCase):
    def test_runtime_supports_temp_output_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            bundle, output_dir = run_fixture_case("technical_overview", repo_root=REPO_ROOT, output_root=Path(temp_dir))
            self.assertEqual(bundle.release_gate.status, "complete")
            self.assertTrue((output_dir / "final_report.md").exists())
            self.assertTrue(str(output_dir).startswith(temp_dir))

    def test_path_helpers_normalize_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            normalized = normalize_path(Path("nested") / ".." / "nested" / "out", base_dir=Path(temp_dir))
            self.assertEqual(normalized, (Path(temp_dir) / "nested" / "out").resolve(strict=False))

    def test_fixture_and_generated_dir_helpers_are_repo_independent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_dir = fixture_case_dir("finance", repo_root=REPO_ROOT)
            generated_dir = generated_case_dir("finance", repo_root=REPO_ROOT, output_root=Path(temp_dir))
            self.assertTrue((fixture_dir / "request.json").exists())
            self.assertEqual(generated_dir.parent, Path(temp_dir).resolve(strict=False))
            self.assertEqual(package_root(REPO_ROOT / "src" / "pseudo_pro_v2" / "pipeline.py"), REPO_ROOT.resolve(strict=False))


if __name__ == "__main__":
    unittest.main()
