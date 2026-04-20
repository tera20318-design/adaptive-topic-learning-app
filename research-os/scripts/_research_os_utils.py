from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


SUPPORTED_TABLE_SUFFIXES = {".csv", ".tsv", ".json", ".jsonl"}
MARKDOWN_TABLE_SUFFIXES = {".md", ".markdown"}
TEXT_LIKE_SUFFIXES = {
    ".txt",
    ".md",
    ".markdown",
    ".html",
    ".htm",
    ".csv",
    ".tsv",
    ".json",
    ".jsonl",
}
AUTO_DISCOVERY_SUFFIXES = SUPPORTED_TABLE_SUFFIXES | MARKDOWN_TABLE_SUFFIXES | {".txt", ".html", ".htm"}


def print_err(message: str) -> None:
    print(message, file=sys.stderr)


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return slug or "research-project"


def discover_named_files(roots: Iterable[Path], stems: Iterable[str]) -> list[Path]:
    stem_set = {stem.casefold() for stem in stems}
    discovered: list[Path] = []
    seen: set[Path] = set()

    for root in roots:
        root = root.resolve()
        if root.is_file():
            if root.suffix.lower() in AUTO_DISCOVERY_SUFFIXES and root.stem.casefold() in stem_set:
                if root not in seen:
                    discovered.append(root)
                    seen.add(root)
            continue

        if not root.exists():
            continue

        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in AUTO_DISCOVERY_SUFFIXES:
                continue
            if path.stem.casefold() not in stem_set:
                continue
            resolved = path.resolve()
            if resolved not in seen:
                discovered.append(resolved)
                seen.add(resolved)

    return sorted(discovered)


def ensure_parent_dir(path: Path, dry_run: bool = False) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text_file(
    path: Path,
    content: str,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> tuple[str, Path]:
    existed_before = path.exists()
    if existed_before and not force:
        return ("skipped", path)
    ensure_parent_dir(path, dry_run=dry_run)
    if not dry_run:
        path.write_text(content, encoding="utf-8", newline="\n")
    return ("created", path)


def write_csv_rows(
    path: Path,
    fieldnames: list[str],
    rows: Iterable[dict[str, Any]],
    *,
    force: bool = False,
    dry_run: bool = False,
) -> tuple[str, Path]:
    existed_before = path.exists()
    if existed_before and not force:
        return ("skipped", path)
    ensure_parent_dir(path, dry_run=dry_run)
    if not dry_run:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow({name: row.get(name, "") for name in fieldnames})
    return ("created", path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_markdown_delimiter(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(
        bool(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")))
        for cell in cells
        if cell
    )


def load_markdown_table_rows(path: Path) -> list[dict[str, Any]]:
    block: list[str] = []
    for line in read_text(path).splitlines():
        if line.lstrip().startswith("|"):
            block.append(line)
            continue
        rows = parse_markdown_table_block(block)
        if rows:
            return rows
        block = []
    return parse_markdown_table_block(block)


def parse_markdown_table_block(lines: list[str]) -> list[dict[str, Any]]:
    if len(lines) < 2:
        return []

    headers = split_markdown_row(lines[0])
    delimiter = split_markdown_row(lines[1])
    if not headers or not is_markdown_delimiter(delimiter):
        return []

    rows: list[dict[str, Any]] = []
    for line in lines[2:]:
        cells = split_markdown_row(line)
        if not any(cell.strip() for cell in cells):
            continue
        padded = cells + [""] * max(0, len(headers) - len(cells))
        rows.append(dict(zip(headers, padded[: len(headers)])))
    return rows


def load_table_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if suffix == ".tsv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]
    if suffix == ".json":
        data = json.loads(read_text(path))
        if isinstance(data, list):
            return [row for row in data if isinstance(row, dict)]
        if isinstance(data, dict):
            for key in ("items", "rows", "claims", "sources", "data"):
                value = data.get(key)
                if isinstance(value, list):
                    return [row for row in value if isinstance(row, dict)]
    if suffix == ".jsonl":
        rows: list[dict[str, Any]] = []
        for line in read_text(path).splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            item = json.loads(stripped)
            if isinstance(item, dict):
                rows.append(item)
        return rows
    if suffix in MARKDOWN_TABLE_SUFFIXES:
        return load_markdown_table_rows(path)
    raise ValueError(f"Unsupported table format: {path}")


def collect_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, dict):
        for nested in value.values():
            yield from collect_strings(nested)
        return
    if isinstance(value, list):
        for nested in value:
            yield from collect_strings(nested)
