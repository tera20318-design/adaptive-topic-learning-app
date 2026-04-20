from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.validators import validate_clean_room_integrity  # noqa: E402


class FixtureSemanticIsolationTests(unittest.TestCase):
    def test_fixture_semantic_guards_do_not_leak_into_core(self) -> None:
        core_roots = [REPO_ROOT / "src" / "pseudo_pro_v2", REPO_ROOT / "core"]
        expected_paths = sorted((REPO_ROOT / "fixtures").glob("*/expected.json"))
        self.assertGreaterEqual(len(expected_paths), 7)

        for expected_path in expected_paths:
            payload = json.loads(expected_path.read_text(encoding="utf-8"))
            guards = payload.get("semantic_guards", {})
            for category in ("nouns", "risk_phrases", "regulation_wording", "overclaim_phrasing"):
                for phrase in guards.get(category, []):
                    for root in core_roots:
                        for path in root.rglob("*"):
                            if not path.is_file() or path.suffix not in {".py", ".md", ".json", ".tsv"}:
                                continue
                            text = path.read_text(encoding="utf-8")
                            self.assertNotIn(phrase, text, msg=f"{category} phrase leaked into {path}")

    def test_clean_room_validator_flags_semantic_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir)
            (package_root / "fixtures" / "finance").mkdir(parents=True)
            (package_root / "src" / "pseudo_pro_v2").mkdir(parents=True)
            (package_root / "core").mkdir(parents=True)

            expected_payload = {
                "expected_statuses": ["blocked"],
                "semantic_guards": {
                    "nouns": ["loss-tolerance ladder"],
                    "risk_phrases": [],
                    "regulation_wording": [],
                    "overclaim_phrasing": [],
                    "synonyms": [],
                    "category_markers": [],
                    "structural_wording": [],
                    "prompt_bans": [],
                },
            }
            (package_root / "fixtures" / "finance" / "expected.json").write_text(
                json.dumps(expected_payload, indent=2),
                encoding="utf-8",
            )
            (package_root / "src" / "pseudo_pro_v2" / "bad.py").write_text(
                'LEAK = "loss-tolerance ladder"\n',
                encoding="utf-8",
            )
            (package_root / "core" / "placeholder.md").write_text("# placeholder\n", encoding="utf-8")

            errors = validate_clean_room_integrity(package_root)

        self.assertTrue(errors)
        self.assertIn("clean-room integrity violation", errors[0])


if __name__ == "__main__":
    unittest.main()
