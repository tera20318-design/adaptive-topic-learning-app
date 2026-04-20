from __future__ import annotations

from pathlib import Path

from research_os_v2.pipeline import run_pipeline_from_payload
from research_os_v2.utils import load_json


def run_regression_suite(fixtures_dir: Path, output_dir: Path) -> dict[str, object]:
    fixtures_dir = fixtures_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []

    for path in sorted(fixtures_dir.glob("*.json")):
        payload = load_json(path)
        bundle = run_pipeline_from_payload(
            payload,
            output_dir=output_dir / path.stem,
            as_of_date="2026-04-19",
            render=True,
        )
        expected = payload.get("expected_gate_behavior", "review")
        actual = bundle.release_gate.status
        matches = _gate_matches(expected, actual)
        results.append(
            {
                "fixture": path.stem,
                "expected_gate_behavior": expected,
                "actual_status": actual,
                "matches_expectation": matches,
            }
        )

    return {
        "fixture_count": len(results),
        "results": results,
        "all_passed": all(item["matches_expectation"] for item in results),
    }


def _gate_matches(expected: str, actual: str) -> bool:
    mapping = {
        "allow": {"complete", "provisional"},
        "review": {"needs_revision", "provisional"},
        "block": {"blocked"},
    }
    return actual in mapping.get(expected, {actual})
