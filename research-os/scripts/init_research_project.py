#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _research_os_utils import print_err, write_text_file


README_TEMPLATE = """# {project_title}

This case uses the `research-os` workflow.

## Canonical Prompt

Only one reusable prompt is scaffolded for this case:

- `prompts/parent_agent_prompt.md`

That file is the single pseudo-Pro master prompt. It contains:

- intake rules
- delegation rules
- evidence-gap handling
- release-blocking quality gates
- final report requirements

## Quick Start

```powershell
python research-os/scripts/init_research_project.py "{project_dir}" --title "{project_title}" --force
python research-os/scripts/extract_links.py "{project_dir}" -o "{project_dir}/sources/collected_urls.txt"
python research-os/scripts/build_evidence_matrix.py "{project_dir}" --merge-existing
```

## Workflow Order
1. Fill `TASK.md`.
2. Fill `PLANS.md`.
3. Log candidates in `sources/source_candidates.md`.
4. Log reviewed sources in `sources/source_log.md`.
5. Extract atomic claims in `extracts/claim_table.md`.
6. Rebuild and refine `extracts/evidence_matrix.md`.
7. Run critique in `reviews/`.
8. Record release readiness in `reviews/reviewer_notes.md`.
9. Draft and finalize in `drafts/`.
"""


NOTES_TEMPLATE = """# Working Notes

## Search Threads
- 

## Emerging Findings
- 

## Risks / Unknowns
- 
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a research project scaffold for the research-os workflow."
    )
    parser.add_argument(
        "project_path",
        type=Path,
        help="Folder to create, for example .\\research-projects\\market-map",
    )
    parser.add_argument(
        "--title",
        help="Optional human-friendly project title. Defaults to the folder name.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite seed files if they already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_dir = args.project_path.expanduser().resolve()
    project_title = args.title or project_dir.name.replace("-", " ").replace("_", " ").title()
    package_dir = Path(__file__).resolve().parent.parent
    templates_dir = package_dir / "templates"
    prompts_dir = package_dir / "prompts"

    directories = [
        project_dir,
        project_dir / "sources",
        project_dir / "sources" / "snapshots",
        project_dir / "extracts",
        project_dir / "reviews",
        project_dir / "drafts",
        project_dir / "prompts",
        project_dir / "notes",
    ]

    for directory in directories:
        if args.dry_run:
            print(f"[dry-run] mkdir {directory}")
        else:
            directory.mkdir(parents=True, exist_ok=True)

    file_map = {
        project_dir / "AGENTS.md": package_dir / "AGENTS.md",
        project_dir / "TASK.md": templates_dir / "TASK.md",
        project_dir / "PLANS.md": templates_dir / "PLANS.md",
        project_dir / "sources" / "source_candidates.md": templates_dir / "source_candidates.md",
        project_dir / "sources" / "source_log.md": templates_dir / "source_log.md",
        project_dir / "extracts" / "claim_table.md": templates_dir / "claim_table.md",
        project_dir / "extracts" / "quotes_table.md": templates_dir / "quotes_table.md",
        project_dir / "extracts" / "evidence_matrix.md": templates_dir / "evidence_matrix.md",
        project_dir / "reviews" / "gap_analysis.md": templates_dir / "gap_analysis.md",
        project_dir / "reviews" / "red_team_review.md": templates_dir / "red_team_review.md",
        project_dir / "reviews" / "citation_audit.md": templates_dir / "citation_audit.md",
        project_dir / "reviews" / "reviewer_notes.md": templates_dir / "reviewer_notes.md",
        project_dir / "drafts" / "outline.md": templates_dir / "outline.md",
        project_dir / "drafts" / "draft_v1.md": templates_dir / "draft_v1.md",
        project_dir / "drafts" / "draft_v2.md": templates_dir / "draft_v2.md",
        project_dir / "drafts" / "final_report.md": templates_dir / "final_report.md",
        project_dir / "prompts" / "parent_agent_prompt.md": prompts_dir / "parent_agent_prompt.md",
    }

    actions: list[tuple[str, Path]] = []
    actions.append(
        write_text_file(
            project_dir / "README.md",
            README_TEMPLATE.format(project_title=project_title, project_dir=project_dir),
            force=args.force,
            dry_run=args.dry_run,
        )
    )
    actions.append(
        write_text_file(
            project_dir / "notes" / "working_notes.md",
            NOTES_TEMPLATE,
            force=args.force,
            dry_run=args.dry_run,
        )
    )
    actions.append(
        write_text_file(
            project_dir / ".gitignore",
            "__pycache__/\n*.tmp\n*.bak\nThumbs.db\nsources/snapshots/\n",
            force=args.force,
            dry_run=args.dry_run,
        )
    )
    for destination, source in file_map.items():
        actions.append(
            write_text_file(
                destination,
                source.read_text(encoding="utf-8"),
                force=args.force,
                dry_run=args.dry_run,
            )
        )

    created = [path for status, path in actions if status == "created"]
    skipped = [path for status, path in actions if status == "skipped"]

    print(f"Project scaffold ready: {project_dir}")
    print(f"Created files: {len(created)}")
    for path in created:
        print(f"  + {path}")
    if skipped:
        print_err(f"Skipped existing files: {len(skipped)}")
        for path in skipped:
            print_err(f"  = {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
