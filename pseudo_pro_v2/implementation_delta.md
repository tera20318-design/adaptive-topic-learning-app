# Implementation Delta

## What Changed In This Pass

- Hardened the runtime from a simple synthetic MVP into a richer synthetic, semi-realistic MVP.
- Expanded fixture coverage to 8 genres and regenerated bundle outputs for all of them.
- Added decision-usable rubric v2 checks for checklist alignment, specific next action, explicit comparison tradeoffs, visible risk disclosure, and non-generic decision layers.
- Added machine-checkable stage contract definitions and validators.
- Added portability helpers for repo-root resolution, path normalization, tempdir output roots, and reusable fixture harness execution.
- Added richer-packet tests for contradiction pressure, weak evidence, waiver scenarios, citation trace mismatch, and metadata inconsistency.

## What Was Hardened

- `release_gate` now blocks citation trace mismatch and still blocks unsupported high-risk claims under metadata inconsistency.
- `draft_writer` now keeps unused findings visible in the audit ledger as excluded claims instead of dropping them silently.
- `clean_room_validator` now checks normalized phrase leakage across richer guard categories and prompt-specific bans.
- `run_vertical_slice.py` now delegates to a reusable harness and supports a custom output root.
- `pyproject.toml` was added so the package has a clean installable shape instead of being only a repo-local layout.

## What Remains Synthetic

- Evidence still comes from curated JSON packets rather than live retrieval.
- Contradiction handling is still packet-limited and not adversarial-search backed.
- Claim extraction is still unit-driven rather than span extraction over arbitrary prose.
- User-document review is still synthetic packet based, not raw document ingestion.
