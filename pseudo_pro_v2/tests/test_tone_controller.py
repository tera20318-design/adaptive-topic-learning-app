from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.models import ClaimLedgerRow, ReportDraft, ReportSectionPlan, ReportUnit  # noqa: E402
from pseudo_pro_v2.stages.tone_controller import apply_tone_control  # noqa: E402


class ToneControllerTests(unittest.TestCase):
    def test_all_tone_modes_are_applied(self) -> None:
        draft = ReportDraft(
            title="Synthetic title",
            sections=[ReportSectionPlan(key="findings", title="Evidence-backed findings", description="")],
            units=[
                _unit("unit-001", "Standard tone"),
                _unit("unit-002", "Tentative tone"),
                _unit("unit-003", "Representative tone"),
                _unit("unit-004", "Unverified tone"),
                _unit("unit-005", "Inference tone"),
                _unit("unit-006", "Advice tone"),
            ],
        )
        claims = [
            _claim("claim-001", "standard"),
            _claim("claim-002", "tentative"),
            _claim("claim-003", "representative_public_materials"),
            _claim("claim-004", "unverified"),
            _claim("claim-005", "explicit_inference"),
            _claim("claim-006", "conditional_advice"),
        ]

        toned = apply_tone_control(draft, claims)
        texts = [unit.text for unit in toned.units]

        self.assertEqual(texts[0], "Standard tone")
        self.assertTrue(texts[1].startswith("The available evidence suggests that"))
        self.assertTrue(texts[2].startswith("Representative public materials suggest that"))
        self.assertTrue(texts[3].startswith("This run did not verify the following claim:"))
        self.assertTrue(texts[4].startswith("Report inference:"))
        self.assertTrue(texts[5].startswith("Decision guidance, subject to verification:"))


def _unit(unit_id: str, text: str) -> ReportUnit:
    return ReportUnit(
        unit_id=unit_id,
        section_key="findings",
        section_title="Evidence-backed findings",
        text=text,
        claim_kind="fact",
        risk_level="medium",
        source_ids=["SRC-001"],
        source_roles=["professional_body"],
        confidence=0.8,
    )


def _claim(claim_id: str, tone: str) -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id=claim_id,
        report_section="Evidence-backed findings",
        exact_text_span="Synthetic text",
        normalized_claim="synthetic text",
        claim_kind="advice" if tone == "conditional_advice" else ("inference" if tone == "explicit_inference" else "fact"),
        risk_level="medium",
        source_ids=["SRC-001"],
        source_roles=["professional_body"],
        evidence_count=1,
        required_source_role=["professional_body"],
        required_role_matched=True,
        role_fit_status="required_match",
        support_status="supported" if tone == "standard" else ("missing" if tone == "unverified" else "weak"),
        confidence=0.8,
        caveat_required=tone != "standard",
        suggested_tone=tone,
        required_fix="",
        origin_finding_id="FINDING-001",
    )


if __name__ == "__main__":
    unittest.main()
