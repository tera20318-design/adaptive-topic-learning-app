from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from research_os_v2.stages.regression_runner import run_regression_suite
from research_os_v2.utils import write_json


def main() -> int:
    output_dir = ROOT / "generated" / "regression_runs"
    summary = run_regression_suite(ROOT / "fixtures", output_dir)
    write_json(ROOT / "generated" / "regression_summary.json", summary)
    print(f"Regression summary written to: {ROOT / 'generated' / 'regression_summary.json'}")
    print(f"Fixtures: {summary['fixture_count']}")
    print(f"All passed: {summary['all_passed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
