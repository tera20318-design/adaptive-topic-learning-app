# Portability Cleanup Report

Scope reviewed:

- `cleanroom_runtime/src`
- `cleanroom_runtime/tests`
- `cleanroom_runtime/*.md`
- `cleanroom_runtime/scripts`

Summary:

- No blocking repo-local absolute paths were found in the reviewed Python and Markdown files.
- Runtime file writes stay behind `pathlib.Path` helpers in `cleanroom_runtime/src/cleanroom_runtime/utils.py`, which is portable across Windows and POSIX path handling.
- The stage-contract strictness and semantic-isolation v2 additions remain path-agnostic.
- Local regeneration entrypoints are now normalized through `cleanroom_runtime/scripts/runtime_entrypoints.py` instead of duplicating setup logic in multiple scripts.

Notes:

- `cleanroom_runtime/tests/test_contracts.py` intentionally checks both `fixtures/` and `fixtures\\` so the cleanroom leakage guard covers POSIX and Windows separators.
- `cleanroom_runtime/tests/runtime_bootstrap.py` now centralizes the shared repo/test/src bootstrap for touched test helpers and new tests.
- Several older test modules still perform local `sys.path` setup inline. That is portable, but it remains a cleanup target until the rest of the suite migrates to `cleanroom_runtime/tests/runtime_bootstrap.py`.

Cleanup action taken:

- Added `cleanroom_runtime/tests/runtime_bootstrap.py` to reduce repeated path hacks in touched helpers and tests.
- Added repo-root wrapper modules:
  - `cleanroom_runtime/runtime_bootstrap.py`
  - `cleanroom_runtime/support.py`
  - `cleanroom_runtime/multigenre_fixtures.py`
  - `cleanroom_runtime/multigenre_runtime.py`
  so direct `python -m unittest tests.test_*` execution does not depend on the tests directory already being on `sys.path`.
- Added `cleanroom_runtime/scripts/runtime_entrypoints.py` so both regeneration scripts share the same entrypoint and path setup.
- Kept all new docs and schema artifacts on repo-relative paths only:
  - `cleanroom_runtime/live_lite_ingestion_plan.md`
  - `cleanroom_runtime/next_priorities.md`
  - `cleanroom_runtime/normalized_source_packet.schema.json`
