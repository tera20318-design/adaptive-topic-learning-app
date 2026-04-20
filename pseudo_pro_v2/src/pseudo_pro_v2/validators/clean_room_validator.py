from __future__ import annotations

from pathlib import Path

from pseudo_pro_v2.utils import load_json


def validate_clean_room_integrity(package_root: Path) -> list[str]:
    fixture_root = package_root / "fixtures"
    core_roots = [package_root / "src" / "pseudo_pro_v2", package_root / "core"]
    errors: list[str] = []

    for expected_path in fixture_root.glob("*/expected.json"):
        payload = load_json(expected_path)
        semantic_guards = payload.get("semantic_guards", {})
        for key, phrases in semantic_guards.items():
            for phrase in phrases:
                normalized_phrase = _normalize(phrase)
                scan_roots = core_roots
                if key == "prompt_bans":
                    scan_roots = [package_root / "core" / "prompts", package_root / "core" / "templates"]
                if not normalized_phrase:
                    continue
                for root in scan_roots:
                    if not root.exists():
                        continue
                    for path in root.rglob("*"):
                        if not path.is_file() or path.suffix not in {".py", ".md", ".json", ".tsv"}:
                            continue
                        if normalized_phrase in _normalize(path.read_text(encoding="utf-8")):
                            rel = path.relative_to(package_root).as_posix()
                            errors.append(f"clean-room integrity violation: `{phrase}` leaked into `{rel}`")
    return errors


def _normalize(text: str) -> str:
    rendered = "".join(char.lower() if char.isalnum() else " " for char in text)
    return " ".join(rendered.split())
