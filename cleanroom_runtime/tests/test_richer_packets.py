from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SRC = ROOT / "src"
for candidate in (TESTS, SRC):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from runtime_bootstrap import ensure_repo_paths, ensure_runtime_namespace


ensure_repo_paths(include_tests=True)
ensure_runtime_namespace()

from multigenre_fixtures import FIXTURE_DIR, load_fixture, load_all_fixtures  # noqa: E402
from multigenre_runtime import run_multigenre_pipeline  # noqa: E402


class RicherPacketTests(unittest.TestCase):
    def test_suite_represents_richer_packet_issue_taxonomy(self) -> None:
        fixture_ids = {fixture.fixture_id for fixture in load_all_fixtures()}
        self.assertTrue({"technical_overview", "legal_regulatory", "historical_cultural"} <= fixture_ids)

        covered_tags: set[str] = set()
        stale_fixture_ids: set[str] = set()
        grounding_fixture_ids: set[str] = set()
        metadata_fixture_ids: set[str] = set()
        mismatch_fixture_ids: set[str] = set()

        for fixture_dir in sorted(path for path in FIXTURE_DIR.iterdir() if path.is_dir()):
            request_payload = _read_json(fixture_dir / "request.json")
            sources_payload = _read_json(fixture_dir / "synthetic_sources.json")
            covered_tags.update(request_payload.get("scenario_tags", []))

            source_ids = {packet["source_id"] for packet in sources_payload}
            provided_source_ids = set(request_payload["request"].get("provided_source_ids", source_ids))
            if provided_source_ids != source_ids:
                metadata_fixture_ids.add(fixture_dir.name)

            years = {packet.get("published_on", "")[:4] for packet in sources_payload if packet.get("published_on")}
            if len(years) >= 2 and "stale_vs_recent_tension" in request_payload.get("scenario_tags", []):
                stale_fixture_ids.add(fixture_dir.name)

            if any(
                packet["source_role"] == "user_provided_source"
                and any(
                    marker in flag.casefold()
                    for flag in packet.get("quality_flags", [])
                    for marker in ("grounding ambiguity", "draft", "uploaded")
                )
                for packet in sources_payload
            ):
                grounding_fixture_ids.add(fixture_dir.name)

            for packet in sources_payload:
                for finding in packet.get("findings", []):
                    for source_id in finding.get("source_ids", [packet["source_id"]]):
                        if source_id not in source_ids:
                            mismatch_fixture_ids.add(fixture_dir.name)

        self.assertTrue(
            {
                "stale_vs_recent_tension",
                "metadata_inconsistency",
                "citation_trace_mismatch",
                "document_grounding_ambiguity",
                "target_miss",
                "waiver",
            }
            <= covered_tags
        )
        self.assertIn("technical_overview", metadata_fixture_ids)
        self.assertIn("technical_overview", mismatch_fixture_ids)
        self.assertGreaterEqual(len(stale_fixture_ids), 5)
        self.assertGreaterEqual(len(grounding_fixture_ids), 4)

    def test_runtime_surfaces_richer_packet_failure_modes(self) -> None:
        technical = run_multigenre_pipeline(load_fixture("technical_overview").request)
        legal = run_multigenre_pipeline(load_fixture("legal_regulatory").request)
        business = run_multigenre_pipeline(load_fixture("business_market", variant="mid").request)
        product = run_multigenre_pipeline(load_fixture("product_comparison", variant="mid").request)
        historical = run_multigenre_pipeline(load_fixture("historical_cultural").request)

        self.assertEqual(technical.release_gate.status, "blocked")
        self.assertFalse(technical.metrics.citation_trace_complete)
        self.assertIn("validator", {issue.stage for issue in technical.release_gate.claim_issues})
        self.assertIn("audit", {issue.stage for issue in technical.release_gate.claim_issues})

        self.assertEqual(legal.release_gate.status, "blocked")
        self.assertGreater(legal.metrics.contradiction_count, 0)
        self.assertIn("contradiction_guard", {issue.stage for issue in legal.release_gate.claim_issues})

        self.assertEqual(business.release_gate.status, "needs_revision")
        self.assertTrue(business.metrics.target_miss_without_waiver)
        self.assertEqual(business.metrics.target_misses, ["min_sources"])

        self.assertEqual(product.release_gate.status, "needs_revision")
        self.assertFalse(product.metrics.target_miss_without_waiver)
        self.assertEqual(product.metrics.target_misses, ["min_high_risk_sources"])

        self.assertEqual(historical.release_gate.status, "provisional")
        self.assertEqual(historical.release_gate.blocking_reasons, [])


def _read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
