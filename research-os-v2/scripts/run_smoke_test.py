from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from research_os_v2.pipeline import run_pipeline


def main() -> int:
    output_dir = ROOT / "generated" / "smoke_bundle"
    bundle = run_pipeline(
        ROOT / "examples" / "smoke_request.json",
        output_dir=output_dir,
        as_of_date="2026-04-19",
        render=True,
    )
    print(f"Smoke bundle written to: {output_dir}")
    print(f"Release status: {bundle.release_gate.status}")
    print(f"Supported claim ratio: {bundle.metrics['supported_claim_ratio']}")
    print(f"Full DR equivalent: {bundle.metrics['full_dr_equivalent']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
