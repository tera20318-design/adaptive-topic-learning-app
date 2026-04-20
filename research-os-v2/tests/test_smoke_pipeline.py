from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from research_os_v2.pipeline import run_pipeline, run_pipeline_from_payload


class SmokePipelineTests(unittest.TestCase):
    def test_smoke_bundle_contains_required_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "bundle"
            bundle = run_pipeline(
                ROOT / "examples" / "smoke_request.json",
                output_dir=output_dir,
                as_of_date="2026-04-19",
                render=True,
            )
            required = {
                "final_report.md",
                "metrics.json",
                "release-gate-summary.md",
                "domain-adapter.md",
                "source-log.tsv",
                "citation-ledger.tsv",
                "claim-ledger.tsv",
                "contradiction-log.md",
                "evidence-gap-log.md",
                "uncertainty-and-scope.md",
            }
            self.assertEqual(required, {path.name for path in output_dir.iterdir()})
            self.assertFalse(bundle.metrics["full_dr_equivalent"])
            self.assertEqual(bundle.release_gate.status, "provisional")

    def test_absence_claim_stays_scoped_and_prevents_complete_if_high_risk(self) -> None:
        payload = json.loads((ROOT / "examples" / "smoke_request.json").read_text(encoding="utf-8"))
        payload["topic"] = "Medication substitution policy overview"
        payload["output_type"] = "legal overview"
        payload["requested_mode"] = "scoped"
        payload["jurisdiction"] = "US"
        payload["source_packets"][2]["findings"][0]["risk_level"] = "high"
        payload["source_packets"][2]["findings"][0]["claim_kind"] = "absence"
        payload["source_packets"][2]["findings"][0]["statement"] = (
            "Within the scoped source set, no authoritative source was found confirming that substitution is always prohibited."
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle = run_pipeline_from_payload(
                payload,
                output_dir=Path(tmp_dir) / "bundle",
                as_of_date="2026-04-19",
                render=False,
            )
        self.assertNotEqual(bundle.release_gate.status, "complete")
        self.assertGreater(bundle.metrics["unsupported_high_risk_count"], 0)
        absence_claims = [claim for claim in bundle.claims if claim.claim_kind == "absence"]
        self.assertTrue(absence_claims)
        self.assertIn(absence_claims[0].support_status, {"weak", "missing"})


if __name__ == "__main__":
    unittest.main()
