from __future__ import annotations

import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = ROOT / "tests"


def ensure_entrypoint_paths() -> None:
    for candidate in reversed((ROOT, TESTS, SRC)):
        rendered = str(candidate)
        if rendered not in sys.path:
            sys.path.insert(0, rendered)


def regenerate_vertical_slices_main() -> None:
    ensure_entrypoint_paths()

    from multigenre_fixtures import (
        VERTICAL_SLICE_DIR,
        load_all_fixtures,
        load_mid_quality_fixtures,
        load_positive_fixtures,
        snapshot_dir,
    )
    from multigenre_runtime import run_multigenre_pipeline

    VERTICAL_SLICE_DIR.mkdir(parents=True, exist_ok=True)
    all_fixtures = load_all_fixtures() + load_positive_fixtures() + load_mid_quality_fixtures()
    for fixture in all_fixtures:
        output_dir = snapshot_dir(fixture)
        if output_dir.exists():
            shutil.rmtree(output_dir)
        run_multigenre_pipeline(fixture.request, output_dir)
        print(output_dir.relative_to(ROOT).as_posix())
