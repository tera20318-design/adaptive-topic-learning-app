from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from research_os_v2.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a pseudo-Pro v2 case from request.json.")
    parser.add_argument("input_json", type=Path, help="Path to request.json")
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        help="Optional output directory. Defaults to <request_dir>/bundle",
    )
    parser.add_argument(
        "--as-of-date",
        default="",
        help="Optional YYYY-MM-DD date override.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_json = args.input_json.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve() if args.output_dir else input_json.parent / "bundle"
    bundle = run_pipeline(
        input_json,
        output_dir=output_dir,
        as_of_date=args.as_of_date,
        render=True,
    )
    print(f"Bundle written to: {output_dir}")
    print(f"Release status: {bundle.release_gate.status}")
    print(f"Supported claim ratio: {bundle.metrics['supported_claim_ratio']}")
    print(f"Full DR equivalent: {bundle.metrics['full_dr_equivalent']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
