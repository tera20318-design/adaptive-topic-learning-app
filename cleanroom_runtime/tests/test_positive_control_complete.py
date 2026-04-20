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

from multigenre_fixtures import load_positive_fixtures  # noqa: E402
from multigenre_runtime import run_multigenre_pipeline  # noqa: E402


class PositiveControlCompleteTests(unittest.TestCase):
    def test_required_positive_controls_reach_complete(self) -> None:
        fixtures = load_positive_fixtures()
        fixture_ids = {fixture.fixture_id for fixture in fixtures}
        required = {"technical_overview", "business_market", "historical_cultural"}

        self.assertTrue(required <= fixture_ids)

        complete_ids: set[str] = set()
        for fixture in fixtures:
            bundle = run_multigenre_pipeline(fixture.request)
            if bundle.release_gate.status == "complete":
                complete_ids.add(fixture.fixture_id)
            if fixture.fixture_id not in required:
                continue
            with self.subTest(fixture=fixture.fixture_id):
                self.assertEqual(bundle.release_gate.status, "complete")
                self.assertEqual(bundle.release_gate.research_completeness, "live_full_candidate")
                self.assertFalse(bundle.release_gate.blocking_reasons)
                self.assertFalse(bundle.metrics.target_misses)
                self.assertEqual(bundle.metrics.unresolved_high_risk_claim_count, 0)
                self.assertTrue(bundle.metrics.reader_decision_layer_present)
                self.assertTrue(bundle.metrics.specific_next_action_present)
                for claim in bundle.claims:
                    if claim.included_in_report and claim.claim_kind == "absence":
                        self.assertIn("Within the checked scope", claim.exact_text_span)
                        self.assertIsNotNone(claim.absence_scope)
                        self.assertIn(claim.absence_scope.subject, claim.exact_text_span)

        self.assertGreaterEqual(len(complete_ids), 3)


if __name__ == "__main__":
    unittest.main()
