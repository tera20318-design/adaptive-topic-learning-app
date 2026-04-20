from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class CleanRoomIsolationTests(unittest.TestCase):
    def test_fixture_anchor_tokens_do_not_leak_into_core(self) -> None:
        core_roots = [REPO_ROOT / "src" / "pseudo_pro_v2", REPO_ROOT / "core"]
        forbidden_tokens = {
            json.loads(path.read_text(encoding="utf-8"))["topic"]
            for path in (REPO_ROOT / "fixtures").glob("*/request.json")
        }

        for root in core_roots:
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix not in {".py", ".md", ".json", ".tsv"}:
                    continue
                text = path.read_text(encoding="utf-8")
                for token in forbidden_tokens:
                    self.assertNotIn(token, text, msg=f"{token} leaked into {path}")


if __name__ == "__main__":
    unittest.main()
