# Portability Cleanup Report

## Scope

This pass removed environment-specific path assumptions from repo documentation and verification tests.

## Changes

- Replaced machine-specific user-home links in top-level docs with repo-relative links or plain code paths.
- Added `src/pseudo_pro_v2/runtime_paths.py` so repo root, schema root, fixture paths, and output paths are normalized in one place.
- Added `src/pseudo_pro_v2/harness.py` so fixture execution can target repo-default outputs or tempdir outputs without rewriting path logic.
- Added `pyproject.toml` so the package has a stable `src/` layout contract rather than only ad hoc repo-local execution.

## Verification

The cleanup is verified by a repository test that scans text files for:

- forward-slash Windows user-home prefixes
- backslash Windows user-home prefixes

The scan covers `.md`, `.py`, `.json`, and `.tsv` files under `pseudo_pro_v2/`.
Runtime portability is also verified by tempdir execution tests that run the harness with a temporary output root.

## Remaining Portable Assumptions

- The synthetic harness still expects fixture JSON to be present in the repository checkout.
- Some scripts and tests still keep a local import fallback for non-installed repo execution.
- Generated bundles still write to the local filesystem rather than an abstract storage layer.

These are repository-relative assumptions, not machine-specific path assumptions.
