from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class PortabilityCleanupTests(unittest.TestCase):
    def test_repo_contains_no_windows_absolute_paths(self) -> None:
        forward_user_home = "C:" + "/Users/"
        backslash_user_home = "C:" + "\\Users\\"
        hits: list[str] = []
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py", ".json", ".tsv"}:
                continue
            text = path.read_text(encoding="utf-8")
            if forward_user_home in text or backslash_user_home in text:
                hits.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
