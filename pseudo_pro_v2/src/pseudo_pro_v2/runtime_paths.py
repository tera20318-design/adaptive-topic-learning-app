from __future__ import annotations

from pathlib import Path


def package_root(anchor: Path | None = None) -> Path:
    base = anchor or Path(__file__)
    return base.resolve().parents[2]


def normalize_path(path: str | Path, *, base_dir: Path | None = None) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = (base_dir or Path.cwd()) / candidate
    return candidate.expanduser().resolve(strict=False)


def fixture_case_dir(case_name: str, *, repo_root: Path | None = None) -> Path:
    root = repo_root or package_root()
    return normalize_path(root / "fixtures" / case_name)


def generated_case_dir(
    case_name: str,
    *,
    repo_root: Path | None = None,
    output_root: Path | None = None,
) -> Path:
    root = repo_root or package_root()
    base = output_root or (root / "vertical-slice" / "generated")
    return normalize_path(Path(base) / case_name)


def schema_root(*, repo_root: Path | None = None) -> Path:
    root = repo_root or package_root()
    return normalize_path(root / "core" / "schemas")
