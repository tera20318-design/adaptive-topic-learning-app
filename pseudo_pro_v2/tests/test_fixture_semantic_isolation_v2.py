from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.validators import validate_clean_room_integrity  # noqa: E402


class FixtureSemanticIsolationV2Tests(unittest.TestCase):
    def test_extended_semantic_guard_categories_do_not_leak_into_core(self) -> None:
        expected_paths = sorted((REPO_ROOT / "fixtures").glob("*/expected.json"))
        self.assertGreaterEqual(len(expected_paths), 7)
        scan_roots = [REPO_ROOT / "src" / "pseudo_pro_v2", REPO_ROOT / "core"]
        categories = (
            "synonyms",
            "category_markers",
            "structural_wording",
            "prompt_bans",
        )

        for expected_path in expected_paths:
            payload = json.loads(expected_path.read_text(encoding="utf-8"))
            guards = payload.get("semantic_guards", {})
            for category in categories:
                for phrase in guards.get(category, []):
                    normalized_phrase = _normalize(phrase)
                    for root in scan_roots:
                        for path in root.rglob("*"):
                            if not path.is_file() or path.suffix not in {".py", ".md", ".json", ".tsv"}:
                                continue
                            self.assertNotIn(normalized_phrase, _normalize(path.read_text(encoding="utf-8")), msg=f"{category} leaked into {path}")

    def test_validator_catches_normalized_paraphrase_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir)
            (package_root / "fixtures" / "product_comparison").mkdir(parents=True)
            (package_root / "src" / "pseudo_pro_v2").mkdir(parents=True)
            (package_root / "core" / "prompts").mkdir(parents=True)
            (package_root / "core" / "templates").mkdir(parents=True)
            payload = {
                "expected_statuses": ["needs_revision"],
                "semantic_guards": {
                    "nouns": [],
                    "risk_phrases": [],
                    "regulation_wording": [],
                    "overclaim_phrasing": [],
                    "synonyms": ["benchmark winner drift"],
                    "category_markers": [],
                    "structural_wording": [],
                    "prompt_bans": ["single benchmark winner defines the best fit"],
                },
            }
            (package_root / "fixtures" / "product_comparison" / "expected.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
            (package_root / "src" / "pseudo_pro_v2" / "bad.py").write_text('LEAK = "benchmark-winner drift"\n', encoding="utf-8")
            (package_root / "core" / "prompts" / "bad.md").write_text("single benchmark winner defines the best fit\n", encoding="utf-8")

            errors = validate_clean_room_integrity(package_root)

        self.assertGreaterEqual(len(errors), 2)


def _normalize(text: str) -> str:
    rendered = "".join(char.lower() if char.isalnum() else " " for char in text)
    return " ".join(rendered.split())


if __name__ == "__main__":
    unittest.main()
