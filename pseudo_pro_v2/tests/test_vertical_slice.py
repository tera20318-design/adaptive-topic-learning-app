from __future__ import annotations

import shutil
import sys
import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.pipeline import run_pipeline  # noqa: E402


class VerticalSliceFixtureTests(unittest.TestCase):
    def test_technical_overview_fixture_runs_end_to_end(self) -> None:
        bundle, output_dir = _run_case("technical_overview")
        report_text = (output_dir / "final_report.md").read_text(encoding="utf-8")
        claim_rows = _read_tsv(output_dir / "claim-ledger.tsv")

        self.assertEqual(bundle.release_gate.status, "complete")
        self.assertIn("## Direct answer", report_text)
        self.assertIn("## Scope and exclusions", report_text)
        self.assertIn("## Reader decision layer", report_text)
        self.assertNotIn("## Claim audit", report_text)
        self.assertEqual(bundle.metrics["report_claim_capture_ratio"], 1.0)
        self.assertGreaterEqual(bundle.metrics["supported_claim_ratio"], 0.8)
        self.assertEqual(bundle.metrics["unsupported_high_risk_count"], 0)
        self.assertFalse(bundle.metrics["full_dr_equivalent"])
        self.assertEqual(
            len([row for row in claim_rows if row["included_in_report"] == "true"]),
            bundle.metrics["included_claim_count"],
        )
        normalized_claims = [row["normalized_claim"] for row in claim_rows if row["included_in_report"] == "true"]
        self.assertEqual(len(normalized_claims), len(set(normalized_claims)))
        self.assertFalse(_core_contains_token("technical_overview_anchor_alpha"))

    def test_legal_regulatory_fixture_blocks_scoped_absence(self) -> None:
        bundle, output_dir = _run_case("legal_regulatory")
        report_text = (output_dir / "final_report.md").read_text(encoding="utf-8")
        summary_text = (output_dir / "release-gate-summary.md").read_text(encoding="utf-8")
        claim_rows = _read_tsv(output_dir / "claim-ledger.tsv")

        self.assertEqual(bundle.release_gate.status, "blocked")
        self.assertGreater(bundle.metrics["unsupported_high_risk_absence_count"], 0)
        self.assertNotIn("No authoritative exception was found within the scoped search packet.", report_text)
        self.assertIn("blocked", summary_text.lower())
        excluded_high_risk = [
            row for row in claim_rows if row["claim_kind"] == "absence" and row["included_in_report"] == "false"
        ]
        self.assertTrue(excluded_high_risk)
        self.assertTrue(excluded_high_risk[0]["exclusion_reason"])
        self.assertFalse(_core_contains_token("legal_regulatory_anchor_beta"))


def _run_case(case_name: str):
    case_dir = REPO_ROOT / "fixtures" / case_name
    output_dir = REPO_ROOT / "vertical-slice" / "generated-tests" / case_name
    if output_dir.exists():
        shutil.rmtree(output_dir)
    bundle = run_pipeline(case_dir / "request.json", case_dir / "source_packets.json", output_dir)
    return bundle, output_dir


def _core_contains_token(token: str) -> bool:
    search_roots = [REPO_ROOT / "src" / "pseudo_pro_v2", REPO_ROOT / "core"]
    for root in search_roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in {".py", ".md", ".json", ".tsv"}:
                continue
            if token in path.read_text(encoding="utf-8"):
                return True
    return False


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


if __name__ == "__main__":
    unittest.main()
