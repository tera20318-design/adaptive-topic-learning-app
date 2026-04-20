from __future__ import annotations

from runtime_bootstrap import ensure_repo_paths


ensure_repo_paths(include_tests=True)

from scripts.runtime_entrypoints import regenerate_vertical_slices_main  # noqa: E402


if __name__ == "__main__":
    regenerate_vertical_slices_main()
