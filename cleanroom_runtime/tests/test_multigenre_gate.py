from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SRC = ROOT / "src"
for candidate in (TESTS, SRC):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from multigenre_fixtures import FIXTURE_DIR, TRAP_TAGS, fixture_findings, load_all_fixtures  # noqa: E402
from multigenre_runtime import run_multigenre_pipeline  # noqa: E402


class MultigenreGateTests(unittest.TestCase):
    def test_fixture_directories_cover_required_genres_and_packet_breadth(self) -> None:
        fixtures = load_all_fixtures()
        fixture_ids = {fixture.fixture_id for fixture in fixtures}

        self.assertGreaterEqual(len(fixtures), 8)
        self.assertTrue(
            {
                "medical_health",
                "finance",
                "product_comparison",
                "business_market",
                "user_document_review",
                "technical_overview",
                "legal_regulatory",
                "historical_cultural",
            }
            <= fixture_ids
        )

        covered_tags = {tag for fixture in fixtures for tag in fixture.scenario_tags}
        self.assertTrue(
            {
                "conflicting_sources",
                "mixed_roles",
                "weak_evidence",
                "high_risk_claim",
                "absence_trap",
                "overgeneralization_trap",
                "scoped_vs_full_ambiguity",
                "target_miss",
                "waiver",
                "stale_vs_recent_tension",
                "metadata_inconsistency",
                "citation_trace_mismatch",
                "document_grounding_ambiguity",
            }
            <= covered_tags
        )

        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                fixture_dir = FIXTURE_DIR / fixture.fixture_id
                self.assertTrue((fixture_dir / "request.json").is_file())
                self.assertTrue((fixture_dir / "synthetic_sources.json").is_file())
                self.assertTrue((fixture_dir / "expected.json").is_file())
                self.assertGreaterEqual(len({packet.source_role for packet in fixture.request.source_packets}), 3)
                self.assertTrue(any(packet.quality_flags for packet in fixture.request.source_packets))
                self.assertTrue(any(finding.risk_level == "high" for finding in fixture_findings(fixture)))
                self.assertTrue(any(TRAP_TAGS & set(finding.tags) for finding in fixture_findings(fixture)))

    def test_multigenre_gate_outputs_match_expected_statuses(self) -> None:
        for fixture in load_all_fixtures():
            with self.subTest(fixture=fixture.fixture_id):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle = run_multigenre_pipeline(fixture.request, Path(tmp_dir))
                    report_text = Path(tmp_dir, "final_report.md").read_text(encoding="utf-8")

                expected = fixture.expected
                self.assertEqual(bundle.release_gate.status, expected["gate_status"])
                self.assertEqual(bundle.release_gate.research_completeness, expected["research_completeness"])
                self.assertEqual(bundle.metrics.target_misses, expected["target_misses"])
                self.assertEqual(bundle.budget.waivers, expected["waived_targets"])
                self.assertTrue(set(expected["required_gap_types"]) <= {gap.gap_type for gap in bundle.gaps})
                self.assertTrue(set(expected["required_issue_stages"]) <= {issue.stage for issue in bundle.release_gate.claim_issues})

                for fragment in expected["required_report_fragments"]:
                    self.assertIn(fragment, report_text)
                for fragment in expected["blocked_report_fragments"]:
                    self.assertNotIn(fragment, report_text)


if __name__ == "__main__":
    unittest.main()
