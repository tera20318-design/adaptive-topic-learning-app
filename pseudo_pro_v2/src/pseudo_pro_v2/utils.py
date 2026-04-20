from __future__ import annotations

import csv
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.expanduser().resolve(strict=False).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_tsv(path: Path, headers: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, delimiter="\t")
        writer.writeheader()
        for row in rows:
            rendered = {}
            for key in headers:
                value = row.get(key, "")
                if isinstance(value, list):
                    rendered[key] = " | ".join(str(item) for item in value)
                else:
                    rendered[key] = value
            writer.writerow(rendered)


def uniq(values):
    seen = set()
    ordered = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered
