from __future__ import annotations

import csv
import json
import shutil
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.harness import run_fixture_case  # noqa: E402


CASES = {
    "technical_overview": "complete",
    "legal_regulatory": "blocked",
    "medical_health": "blocked",
    "finance": "blocked",
    "product_comparison": "needs_revision",
    "business_market": "provisional",
    "user_document_review": "needs_revision",
    "historical_cultural": "complete",
}


class MultiGenreVerticalSliceTests(unittest.TestCase):
    def test_multigenre_fixtures_cover_expected_release_behaviors(self) -> None:
        for case_name, expected_status in CASES.items():
            with self.subTest(case_name=case_name):
                bundle, output_dir = _run_case(case_name)
                expected_payload = json.loads((REPO_ROOT / "fixtures" / case_name / "expected.json").read_text(encoding="utf-8"))
                claim_rows = _read_tsv(output_dir / "claim-ledger.tsv")
                report_text = (output_dir / "final_report.md").read_text(encoding="utf-8")

                self.assertEqual(bundle.release_gate.status, expected_status)
                self.assertIn(expected_status, expected_payload["expected_statuses"])
                self.assertIn("## Direct answer", report_text)
                self.assertIn("## Scope and exclusions", report_text)
                self.assertIn("## Reader decision layer", report_text)
                self.assertNotIn("## Claim audit", report_text)
                self.assertGreaterEqual(len(claim_rows), 1)

                if case_name == "technical_overview":
                    self.assertEqual(bundle.metrics["unsupported_high_risk_count"], 0)
                    self.assertFalse(bundle.metrics["full_dr_equivalent"])
                elif case_name == "legal_regulatory":
                    self.assertGreater(bundle.metrics["unsupported_high_risk_absence_count"], 0)
                elif case_name == "medical_health":
                    self.assertTrue(
                        any(
                            row["claim_kind"] == "advice"
                            and row["risk_level"] == "high"
                            and row["support_status"] != "supported"
                            for row in claim_rows
                        )
                    )
                elif case_name == "finance":
                    self.assertTrue(
                        any(
                            row["claim_kind"] in {"recommendation", "financial", "absence"}
                            and row["risk_level"] == "high"
                            and row["support_status"] != "supported"
                            for row in claim_rows
                        )
                    )
                elif case_name == "product_comparison":
                    self.assertIn("comparison tradeoff structure is insufficient", " ".join(bundle.release_gate.reasons))
                elif case_name == "business_market":
                    self.assertIn("Useful but limited within the declared scope.", " ".join(bundle.release_gate.reasons))
                elif case_name == "user_document_review":
                    self.assertEqual(bundle.release_gate.status, "needs_revision")
                elif case_name == "historical_cultural":
                    self.assertEqual(bundle.metrics["unsupported_high_risk_count"], 0)


def _run_case(case_name: str):
    output_root = REPO_ROOT / "vertical-slice" / "generated-tests-multigenre"
    output_dir = output_root / case_name
    if output_dir.exists():
        shutil.rmtree(output_dir)
    return run_fixture_case(case_name, repo_root=REPO_ROOT, output_root=output_root)


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


if __name__ == "__main__":
    unittest.main()
