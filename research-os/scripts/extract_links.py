#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from _research_os_utils import collect_strings, discover_named_files, print_err, read_text


URL_PATTERN = re.compile(r"https?://[^\s<>'\"`]+", re.IGNORECASE)
DEFAULT_STEMS = ("source_log", "source_candidates")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract URLs from source_log/source_candidates files or directories."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Files or folders to scan. Defaults to the current folder.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write results to a file instead of stdout.",
    )
    parser.add_argument(
        "--format",
        choices=("txt", "csv", "json"),
        help="Output format. Defaults to txt, or inferred from --output.",
    )
    parser.add_argument(
        "--keep-fragments",
        action="store_true",
        help="Keep URL fragments such as #section instead of stripping them.",
    )
    parser.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Do not deduplicate URLs.",
    )
    return parser.parse_args()


def normalize_url(url: str, keep_fragments: bool) -> str:
    cleaned = url.rstrip(".,);]}>")
    parts = urlsplit(cleaned)
    fragment = parts.fragment if keep_fragments else ""
    normalized = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, parts.query, fragment))
    return normalized


def find_input_files(paths: list[Path]) -> list[Path]:
    explicit_files = [path.expanduser().resolve() for path in paths if path.expanduser().is_file()]
    directories = [path.expanduser().resolve() for path in paths if path.expanduser().is_dir()]
    discovered = discover_named_files(directories, DEFAULT_STEMS)

    seen: set[Path] = set()
    merged: list[Path] = []
    for path in explicit_files + discovered:
        if path not in seen:
            merged.append(path)
            seen.add(path)
    return merged


def extract_from_csv_like(path: Path) -> list[str]:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    urls: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        for row in reader:
            for cell in row:
                urls.extend(URL_PATTERN.findall(cell))
    return urls


def extract_from_json(path: Path) -> list[str]:
    urls: list[str] = []
    if path.suffix.lower() == ".jsonl":
        values: list[Any] = []
        for line in read_text(path).splitlines():
            stripped = line.strip()
            if stripped:
                values.append(json.loads(stripped))
    else:
        values = [json.loads(read_text(path))]

    for value in values:
        for item in collect_strings(value):
            urls.extend(URL_PATTERN.findall(item))
    return urls


def extract_urls(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        return extract_from_csv_like(path)
    if suffix in {".json", ".jsonl"}:
        return extract_from_json(path)
    return URL_PATTERN.findall(read_text(path))


def infer_output_format(output: Path | None, requested: str | None) -> str:
    if requested:
        return requested
    if output is None:
        return "txt"
    suffix = output.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".json":
        return "json"
    return "txt"


def serialize_txt(urls: list[str]) -> str:
    return "".join(f"{url}\n" for url in urls)


def serialize_csv(urls: list[str], counts: Counter[str]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["url", "count"])
    for url in urls:
        writer.writerow([url, counts[url]])
    return buffer.getvalue()


def serialize_json(urls: list[str], counts: Counter[str]) -> str:
    payload = [{"url": url, "count": counts[url]} for url in urls]
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    args = parse_args()
    input_files = find_input_files(args.paths)
    if not input_files:
        print_err("No matching files found. Pass a file explicitly or point to a folder containing source_log/source_candidates.")
        return 1

    counts: Counter[str] = Counter()
    ordered_urls: list[str] = []

    for path in input_files:
        for raw_url in extract_urls(path):
            normalized = normalize_url(raw_url, keep_fragments=args.keep_fragments)
            if not normalized:
                continue
            counts[normalized] += 1
            if args.allow_duplicates or counts[normalized] == 1:
                ordered_urls.append(normalized)

    output_format = infer_output_format(args.output, args.format)
    if output_format == "csv":
        rendered = serialize_csv(ordered_urls, counts)
    elif output_format == "json":
        rendered = serialize_json(ordered_urls, counts)
    else:
        rendered = serialize_txt(ordered_urls)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"Wrote {len(ordered_urls)} URLs to {args.output.resolve()}")
    else:
        sys.stdout.write(rendered)

    print_err(f"Scanned files: {len(input_files)}")
    print_err(f"Unique URLs: {len(counts)}")
    print_err(f"Returned rows: {len(ordered_urls)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
