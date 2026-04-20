from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from runtime_bootstrap import ROOT, ensure_repo_paths


ensure_repo_paths(include_tests=True)

from multigenre_fixtures import FIXTURE_DIR, load_fixture  # noqa: E402
from multigenre_runtime import run_multigenre_pipeline  # noqa: E402


class RealishPacketTests(unittest.TestCase):
    def test_fixture_packets_cover_realish_provenance_scenarios(self) -> None:
        duplicate_canonical = False
        stale_present = False
        missing_metadata_present = False
        partial_present = False
        ambiguous_grounding_present = False

        for fixture_dir in sorted(path for path in FIXTURE_DIR.iterdir() if path.is_dir()):
            packet_path = fixture_dir / "source_packets.json"
            packets = json.loads(packet_path.read_text(encoding="utf-8"))
            canonical_ids: dict[str, int] = {}
            for packet in packets:
                provenance = packet.get("provenance", {})
                canonical_id = provenance.get("canonical_id", "")
                if canonical_id:
                    canonical_ids[canonical_id] = canonical_ids.get(canonical_id, 0) + 1
                stale_present = stale_present or bool(provenance.get("stale"))
                missing_metadata_present = missing_metadata_present or bool(provenance.get("metadata_missing_fields"))
                partial_present = partial_present or bool(provenance.get("partial"))
                ambiguous_grounding_present = ambiguous_grounding_present or provenance.get("grounding_status") == "ambiguous"
            duplicate_canonical = duplicate_canonical or any(count > 1 for count in canonical_ids.values())

        self.assertTrue(duplicate_canonical)
        self.assertTrue(stale_present)
        self.assertTrue(missing_metadata_present)
        self.assertTrue(partial_present)
        self.assertTrue(ambiguous_grounding_present)

    def test_multigenre_outputs_remain_differentiated_under_realish_packets(self) -> None:
        technical = load_fixture("technical_overview")
        legal = load_fixture("legal_regulatory")
        business = load_fixture("business_market", variant="mid")
        user_document = load_fixture("user_document_review")

        with tempfile.TemporaryDirectory() as tmp_dir:
            statuses = {
                "technical": run_multigenre_pipeline(technical.request, Path(tmp_dir) / "technical").release_gate.status,
                "legal": run_multigenre_pipeline(legal.request, Path(tmp_dir) / "legal").release_gate.status,
                "business": run_multigenre_pipeline(business.request, Path(tmp_dir) / "business").release_gate.status,
                "user_document": run_multigenre_pipeline(user_document.request, Path(tmp_dir) / "user_document").release_gate.status,
            }

        self.assertEqual(statuses["technical"], "blocked")
        self.assertEqual(statuses["legal"], "blocked")
        self.assertEqual(statuses["business"], "needs_revision")
        self.assertIn(statuses["user_document"], {"needs_revision", "blocked"})
        self.assertGreaterEqual(len(set(statuses.values())), 2)


if __name__ == "__main__":
    unittest.main()
