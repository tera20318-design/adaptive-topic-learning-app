from __future__ import annotations

import sys
from pathlib import Path


try:
    from pseudo_pro_v2.harness import DEFAULT_CASES, run_fixture_case
except ImportError:  # pragma: no cover - local repo execution fallback
    REPO_ROOT = Path(__file__).resolve().parents[1]
    SRC_ROOT = REPO_ROOT / "src"
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))
    from pseudo_pro_v2.harness import DEFAULT_CASES, run_fixture_case  # type: ignore  # noqa: E402


def main(args: list[str]) -> int:
    case_names = _parse_case_names(args)
    output_root = _parse_output_root(args)
    for case_name in case_names:
        bundle, _ = run_fixture_case(case_name, output_root=output_root)
        print(f"{case_name}: {bundle.release_gate.status}")
    return 0


def _parse_output_root(args: list[str]) -> Path | None:
    if "--output-root" not in args:
        return None
    index = args.index("--output-root")
    if index + 1 >= len(args):
        raise ValueError("--output-root requires a path")
    return Path(args[index + 1])


def _parse_case_names(args: list[str]) -> list[str]:
    names: list[str] = []
    skip_next = False
    for index, arg in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if arg == "--output-root":
            skip_next = True
            continue
        if arg.startswith("--"):
            continue
        names.append(arg)
    return names or DEFAULT_CASES


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
