#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from _research_os_utils import discover_named_files, load_table_rows, print_err


CLAIM_ID_KEYS = ("claim_id", "claim id", "id", "claimid")
CLAIM_TEXT_KEYS = ("claim", "statement", "assertion", "hypothesis")
THEME_KEYS = ("theme", "topic", "category")
PRIORITY_KEYS = ("priority", "severity", "importance")
STATUS_KEYS = ("status", "claim_status", "claim status", "support_status", "support status")
SOURCE_ID_KEYS = ("source_ids", "source ids", "sources", "source_id", "source id")
EVIDENCE_KEYS = ("evidence", "basis", "rationale")
NOTES_KEYS = ("notes", "counterpoints / caveats", "counterpoints", "caveats")

OUTPUT_HEADERS = [
    "claim_id",
    "claim",
    "theme",
    "priority",
    "claim_status",
    "verification_status",
    "evidence_summary",
    "supporting_source_ids",
    "contradicting_source_ids",
    "evidence_gap",
    "next_action",
    "notes",
]

MARKDOWN_OUTPUT_COLUMNS = [
    ("Claim ID", "claim_id"),
    ("Claim", "claim"),
    ("Theme", "theme"),
    ("Priority", "priority"),
    ("Claim status", "claim_status"),
    ("Verification status", "verification_status"),
    ("Supporting source IDs", "supporting_source_ids"),
    ("Contradicting source IDs", "contradicting_source_ids"),
    ("Evidence summary", "evidence_summary"),
    ("Evidence gap", "evidence_gap"),
    ("Next action", "next_action"),
    ("Notes", "notes"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an evidence_matrix template from claim_table data."
    )
    parser.add_argument(
        "input_path",
        nargs="?",
        type=Path,
        default=Path("."),
        help="A claim_table file or a folder that contains claim_table.*",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the evidence matrix. Defaults next to claim_table.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    parser.add_argument(
        "--merge-existing",
        action="store_true",
        help="If the output already exists, keep editable fields for matching claim_id rows.",
    )
    return parser.parse_args()


def pick_first(row: dict[str, object], keys: tuple[str, ...], default: str = "") -> str:
    lowered = {str(key).casefold(): value for key, value in row.items()}
    for key in keys:
        value = lowered.get(key.casefold())
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return default


def find_claim_table(path: Path) -> Path:
    candidate = path.expanduser().resolve()
    if candidate.is_file():
        return candidate

    matches = discover_named_files([candidate], ("claim_table",))
    supported = [
        match for match in matches if match.suffix.lower() in {".csv", ".tsv", ".json", ".jsonl", ".md", ".markdown"}
    ]
    if not supported:
        raise SystemExit(
            "No claim_table file found. Point to a file directly or a folder containing claim_table.md / .csv / .tsv / .json / .jsonl."
        )
    return supported[0]


def default_output_path(claim_table_path: Path) -> Path:
    if claim_table_path.suffix.lower() in {".md", ".markdown"}:
        return claim_table_path.with_name("evidence_matrix.md")
    return claim_table_path.with_name("evidence_matrix.csv")


def load_existing_rows(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    existing_rows = load_table_rows(path)
    loaded: dict[str, dict[str, str]] = {}
    for row in existing_rows:
        claim_id = pick_first(row, CLAIM_ID_KEYS)
        if claim_id:
            loaded[claim_id] = {str(key): str(value) for key, value in row.items()}
    return loaded


def build_rows(claim_rows: list[dict[str, object]], existing_rows: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    generated_index = 1

    for claim_row in claim_rows:
        claim_text = pick_first(claim_row, CLAIM_TEXT_KEYS)
        if not claim_text:
            continue

        claim_id = pick_first(claim_row, CLAIM_ID_KEYS) or f"claim-{generated_index:03d}"
        generated_index += 1

        base_row = {
            "claim_id": claim_id,
            "claim": claim_text,
            "theme": pick_first(claim_row, THEME_KEYS),
            "priority": pick_first(claim_row, PRIORITY_KEYS, default="medium"),
            "claim_status": pick_first(claim_row, STATUS_KEYS, default="open"),
            "verification_status": "not_started",
            "evidence_summary": pick_first(claim_row, EVIDENCE_KEYS),
            "supporting_source_ids": pick_first(claim_row, SOURCE_ID_KEYS),
            "contradicting_source_ids": "",
            "evidence_gap": "",
            "next_action": "",
            "notes": pick_first(claim_row, NOTES_KEYS),
        }

        if claim_id in existing_rows:
            preserved = existing_rows[claim_id]
            for key in (
                "verification_status",
                "evidence_summary",
                "supporting_source_ids",
                "contradicting_source_ids",
                "evidence_gap",
                "next_action",
                "notes",
            ):
                preserved_value = pick_first(preserved, (key, key.replace("_", " "), key.replace("_", "-")))
                if preserved_value:
                    base_row[key] = preserved_value.strip()

        output_rows.append(base_row)

    return output_rows


def format_markdown_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>").strip()


def write_rows(path: Path, rows: list[dict[str, str]], force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Output already exists: {path}. Re-run with --force or --merge-existing.")

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".md", ".markdown"}:
        lines = [
            "# Evidence Matrix",
            "",
            "## Claim Verification Matrix",
            "",
            "| " + " | ".join(column for column, _ in MARKDOWN_OUTPUT_COLUMNS) + " |",
            "| " + " | ".join("---" for _ in MARKDOWN_OUTPUT_COLUMNS) + " |",
        ]
        for row in rows:
            rendered_cells = [format_markdown_cell(row.get(key, "")) for _, key in MARKDOWN_OUTPUT_COLUMNS]
            lines.append("| " + " | ".join(rendered_cells) + " |")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        return

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    claim_table_path = find_claim_table(args.input_path)
    output_path = args.output.expanduser().resolve() if args.output else default_output_path(claim_table_path)

    claim_rows = load_table_rows(claim_table_path)
    existing_rows = load_existing_rows(output_path) if args.merge_existing else {}
    built_rows = build_rows(claim_rows, existing_rows)

    if not built_rows:
        print_err(f"No claim rows with text were found in {claim_table_path}")
        return 1

    write_rows(output_path, built_rows, force=(args.force or args.merge_existing))

    print(f"Built evidence matrix: {output_path}")
    print(f"Claim rows written: {len(built_rows)}")
    print(f"Source claim table: {claim_table_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
