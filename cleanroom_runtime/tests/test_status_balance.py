from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SRC = ROOT / "src"
for candidate in (TESTS, SRC):
    rendered = str(candidate)
    if rendered not in sys.path:
        sys.path.insert(0, rendered)

from multigenre_fixtures import load_all_fixtures, load_mid_quality_fixtures, load_positive_fixtures  # noqa: E402
from multigenre_runtime import run_multigenre_pipeline  # noqa: E402


class StatusBalanceTests(unittest.TestCase):
    def test_suite_keeps_positive_negative_and_mid_quality_controls(self) -> None:
        default_results = {
            fixture.fixture_id: run_multigenre_pipeline(fixture.request).release_gate.status
            for fixture in load_all_fixtures()
        }
        positive_results = {
            fixture.fixture_id: run_multigenre_pipeline(fixture.request).release_gate.status
            for fixture in load_positive_fixtures()
        }
        mid_results = {
            fixture.fixture_id: run_multigenre_pipeline(fixture.request).release_gate.status
            for fixture in load_mid_quality_fixtures()
        }

        blocked_defaults = {fixture_id for fixture_id, status in default_results.items() if status == "blocked"}
        complete_positives = {fixture_id for fixture_id, status in positive_results.items() if status == "complete"}
        mid_quality_controls = {fixture_id for fixture_id, status in mid_results.items() if status in {"needs_revision", "provisional"}}

        self.assertGreaterEqual(len(complete_positives), 3)
        self.assertGreaterEqual(len(blocked_defaults), 3)
        self.assertGreaterEqual(len(mid_quality_controls), 2)
        self.assertTrue({"technical_overview", "business_market", "historical_cultural"} <= complete_positives)
        self.assertTrue({"business_market", "product_comparison"} <= mid_quality_controls)
        self.assertFalse(all(status in {"blocked", "needs_revision"} for status in positive_results.values()))


if __name__ == "__main__":
    unittest.main()
