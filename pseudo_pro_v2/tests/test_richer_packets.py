from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.pipeline import run_pipeline  # noqa: E402


class RicherPacketsTests(unittest.TestCase):
    def test_fixture_packets_cover_richer_synthetic_patterns(self) -> None:
        fixture_root = REPO_ROOT / "fixtures"
        packets = [json.loads(path.read_text(encoding="utf-8")) for path in fixture_root.glob("*/source_packets.json")]
        all_sources = [source for payload in packets for source in payload["source_packets"]]
        all_findings = [finding for source in all_sources for finding in source.get("findings", [])]

        self.assertTrue(any(source.get("quality_flags") for source in all_sources))
        self.assertTrue(any(source["source_role"] == "vendor_first_party" for source in all_sources))
        self.assertTrue(any(source["source_role"] == "trade_media" for source in all_sources))
        self.assertTrue(any(finding["risk_level"] == "high" for finding in all_findings))
        self.assertTrue(any(finding["claim_kind"] == "absence" and finding.get("absence_type") == "not_found_in_scoped_search" for finding in all_findings))
        self.assertTrue(any(finding.get("contradiction_note") for finding in all_findings))
        self.assertTrue(any(finding.get("support_status_hint") == "weak" for finding in all_findings))
        self.assertTrue(any((fixture_root / name / "request.json").exists() and "waivers" in json.loads((fixture_root / name / "request.json").read_text(encoding="utf-8")) for name in ["business_market"]))

    def test_citation_trace_mismatch_blocks_release(self) -> None:
        bundle = _run_mutated_case(
            "technical_overview",
            lambda payload: payload["source_packets"][0]["findings"][0].update({"source_ids": ["MISSING-SRC"]}),
        )
        self.assertEqual(bundle.release_gate.status, "blocked")
        self.assertIn("Citation trace mismatch remains unresolved.", bundle.release_gate.blocking_reasons)

    def test_metadata_inconsistency_with_unsupported_high_risk_blocks(self) -> None:
        def mutate(payload):
            payload["source_packets"][2]["findings"][0]["source_ids"] = ["MISSING-SRC"]

        bundle = _run_mutated_case("medical_health", mutate)
        self.assertEqual(bundle.release_gate.status, "blocked")
        joined = " ".join(bundle.release_gate.blocking_reasons)
        self.assertIn("unsupported high-risk", joined.lower())
        self.assertIn("metadata inconsistency", joined.lower())


def _run_mutated_case(case_name: str, mutator):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        case_dir = temp_root / case_name
        case_dir.mkdir(parents=True)
        request_path = REPO_ROOT / "fixtures" / case_name / "request.json"
        source_packets_path = REPO_ROOT / "fixtures" / case_name / "source_packets.json"
        shutil.copy2(request_path, case_dir / "request.json")
        payload = json.loads(source_packets_path.read_text(encoding="utf-8"))
        mutator(payload)
        (case_dir / "source_packets.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        output_dir = temp_root / "out"
        return run_pipeline(case_dir / "request.json", case_dir / "source_packets.json", output_dir)


if __name__ == "__main__":
    unittest.main()
