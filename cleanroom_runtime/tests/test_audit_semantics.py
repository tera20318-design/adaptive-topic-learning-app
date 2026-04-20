from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402

from support import make_finding, make_packet, make_request, make_scoped_absence  # noqa: E402


class AuditSemanticsTests(unittest.TestCase):
    def test_high_risk_source_role_mismatch_stays_in_audit_when_excluded(self) -> None:
        request = make_request(
            packets=[
                make_packet(
                    "SRC-001",
                    "trade_media",
                    findings=[
                        make_finding(
                            "finding-001",
                            "The regulation definitely applies in the checked jurisdiction.",
                            "regulatory",
                            "high",
                            "direct_answer",
                            source_ids=["SRC-001"],
                        )
                    ],
                )
            ]
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle = run_pipeline(request, Path(tmp_dir))
            report_text = Path(tmp_dir, "final_report.md").read_text(encoding="utf-8")
            excluded_text = Path(tmp_dir, "excluded-claims.tsv").read_text(encoding="utf-8")

        claim = bundle.claims[0]
        self.assertFalse(claim.included_in_report)
        self.assertEqual(claim.support_status, "weak")
        self.assertNotIn("The regulation definitely applies", report_text)
        self.assertIn(claim.claim_id, excluded_text)

    def test_unscoped_absence_is_not_treated_as_supported(self) -> None:
        request = make_request(
            packets=[
                make_packet(
                    "SRC-001",
                    "official_regulator",
                    findings=[
                        make_finding(
                            "finding-001",
                            "No evidence was found for the requirement.",
                            "absence",
                            "high",
                            "uncertainty",
                            source_ids=["SRC-001"],
                        )
                    ],
                )
            ]
        )

        bundle = run_pipeline(request)

        claim = bundle.claims[0]
        self.assertEqual(claim.support_status, "missing")
        self.assertFalse(claim.included_in_report)
        self.assertEqual(bundle.metrics.unscoped_absence_count, 1)
        self.assertTrue(any(gap.gap_type == "unscoped_absence" for gap in bundle.gaps))

    def test_scoped_absence_remains_typed_and_scoped(self) -> None:
        request = make_request(
            packets=[
                make_packet(
                    "SRC-001",
                    "official_regulator",
                    findings=[
                        make_finding(
                            "finding-001",
                            "No evidence was found for the requirement.",
                            "absence",
                            "high",
                            "uncertainty",
                            source_ids=["SRC-001"],
                            absence_scope=make_scoped_absence("the requirement", source_ids=["SRC-001"]),
                        )
                    ],
                )
            ]
        )

        bundle = run_pipeline(request)

        claim = bundle.claims[0]
        report_unit = next(unit for unit in bundle.draft.units if unit.unit_id == claim.unit_id)
        self.assertEqual(claim.support_status, "scoped_absence")
        self.assertTrue(claim.included_in_report)
        self.assertIn("Within the checked scope", report_unit.text)


if __name__ == "__main__":
    unittest.main()
