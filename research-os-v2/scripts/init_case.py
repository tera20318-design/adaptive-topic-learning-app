from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return slug or "research-v2-case"


def normalize_theme(theme: str) -> str:
    cleaned = " ".join(theme.strip().split())
    return cleaned or theme.strip()


def default_reader(theme: str) -> str:
    return f"Decision-maker or researcher who needs a practical first-pass report on {theme}."


def default_use_context(theme: str) -> str:
    return (
        f"Reader-facing report that explains {theme} directly, separates supported findings from open gaps, "
        "and helps the reader decide what to check next."
    )


def default_question(theme: str) -> str:
    return f"What should a non-specialist or decision-maker understand about {theme} before making a decision or recommendation?"


def default_temporal_context(today: str) -> str:
    return f"Current overview as of {today}. Call out when evidence is scoped, stale, or jurisdiction-specific."


def build_request_template(
    theme: str,
    today: str,
    *,
    reader: str = "",
    use_context: str = "",
    output_type: str = "report",
    requested_mode: str = "scoped",
    question: str = "",
    jurisdiction: str = "",
    temporal_context: str = "",
) -> dict[str, object]:
    normalized_theme = normalize_theme(theme)
    return {
        "topic": normalized_theme,
        "reader": reader or default_reader(normalized_theme),
        "use_context": use_context or default_use_context(normalized_theme),
        "output_type": output_type,
        "requested_mode": requested_mode,
        "question": question or default_question(normalized_theme),
        "jurisdiction": jurisdiction,
        "temporal_context": temporal_context or default_temporal_context(today),
        "as_of_date": today,
        "provided_document_name": "",
        "source_packets": [],
    }


def build_readme(case_dir: Path, today: str) -> str:
    request_path = case_dir / "request.json"
    bundle_dir = case_dir / "bundle"
    return f"""# Pseudo-Pro v2 Case

## Files

- `request.json`: fill the request metadata and add `source_packets`
- `notes.md`: working notes for source collection and scope decisions
- `bundle/`: rendered output bundle from the v2 pipeline

## Next Steps

1. Review `request.json` and adjust:
   - `reader`
   - `use_context`
   - `output_type`
   - `requested_mode`
   - `question`
   - `jurisdiction` if needed
2. Add `source_packets` with findings. Do not invent evidence.
3. Run:

```powershell
python research-os-v2/scripts/run_case.py "{request_path}" "{bundle_dir}" --as-of-date "{today}"
```

## Notes

- `requested_mode` should usually be `lightweight`, `scoped`, or `full`.
- `complete` only means the run gate passed for its own scope.
- A scoped run must not be presented as full Deep Research equivalent.
"""


def build_notes() -> str:
    return """# Notes

## Reader
- 

## Use Context
- 

## Scope Boundaries
- 

## Candidate Sources
- 

## Evidence Gaps
- 
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a pseudo-Pro v2 case scaffold.")
    parser.add_argument("theme", help="Working research theme.")
    parser.add_argument(
        "--base-dir",
        default="runs-v2",
        help="Base directory for the new case. Defaults to runs-v2.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite request.md, README.md, and notes.md if they already exist.",
    )
    parser.add_argument(
        "--reader",
        default="",
        help="Optional reader override for request.json.",
    )
    parser.add_argument(
        "--use-context",
        default="",
        help="Optional use context override for request.json.",
    )
    parser.add_argument(
        "--output-type",
        default="report",
        help="Optional output type override for request.json. Defaults to report.",
    )
    parser.add_argument(
        "--requested-mode",
        default="scoped",
        help="Optional requested mode override for request.json. Defaults to scoped.",
    )
    parser.add_argument(
        "--question",
        default="",
        help="Optional research question override for request.json.",
    )
    parser.add_argument(
        "--jurisdiction",
        default="",
        help="Optional jurisdiction override for request.json.",
    )
    parser.add_argument(
        "--temporal-context",
        default="",
        help="Optional temporal context override for request.json.",
    )
    parser.add_argument(
        "--as-of-date",
        default=str(date.today()),
        help="Date string stored in request.json and used in the case directory. Defaults to today.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the target paths without writing files.",
    )
    return parser.parse_args()


def write_text(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    args = parse_args()
    today = args.as_of_date
    case_dir = Path(args.base_dir).expanduser().resolve() / f"{today}-{safe_slug(args.theme)}"
    request_path = case_dir / "request.json"
    readme_path = case_dir / "README.md"
    notes_path = case_dir / "notes.md"
    bundle_dir = case_dir / "bundle"

    if args.dry_run:
        print(f"[dry-run] case_dir={case_dir}")
        print(f"[dry-run] request_json={request_path}")
        print(f"[dry-run] bundle_dir={bundle_dir}")
        return 0

    case_dir.mkdir(parents=True, exist_ok=True)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    write_text(
        request_path,
        json.dumps(
            build_request_template(
                args.theme,
                today,
                reader=args.reader,
                use_context=args.use_context,
                output_type=args.output_type,
                requested_mode=args.requested_mode,
                question=args.question,
                jurisdiction=args.jurisdiction,
                temporal_context=args.temporal_context,
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        force=args.force,
    )
    write_text(readme_path, build_readme(case_dir, today), force=args.force)
    write_text(notes_path, build_notes(), force=args.force)

    print(f"Created v2 case: {case_dir}")
    print(f"Request file: {request_path}")
    print(f"Bundle dir: {bundle_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
