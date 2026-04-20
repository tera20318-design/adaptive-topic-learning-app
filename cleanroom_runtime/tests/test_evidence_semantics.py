from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.catalogs import REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND  # noqa: E402
from cleanroom_runtime.models import ClaimLedgerRow, CollectedEvidence, SourcePacket, SourceStrategy  # noqa: E402
from cleanroom_runtime.stages.evidence_semantics import map_claims_to_evidence  # noqa: E402


class EvidenceSemanticsTests(unittest.TestCase):
    def test_high_risk_claim_role_mismatch_stays_unsupported(self) -> None:
        claims, citations = map_claims_to_evidence(
            claims=[
                ClaimLedgerRow(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    report_section="Direct answer",
                    exact_text_span="Synthetic claim text.",
                    normalized_claim="synthetic claim text.",
                    claim_kind="regulatory",
                    risk_level="high",
                    source_ids=["SRC-001"],
                    source_roles=[],
                    evidence_count=1,
                    required_source_roles=[],
                    matched_source_roles=[],
                    support_status="supported",
                    confidence=0.9,
                    caveat_required=False,
                    suggested_tone="standard",
                    required_fix="",
                )
            ],
            evidence=CollectedEvidence(
                sources=[SourcePacket(source_id="SRC-001", title="Academic review summary", source_role="academic_review")],
                findings=[],
                source_counts_by_role={"academic_review": 1},
                quality_notes=[],
            ),
            strategy=SourceStrategy(
                source_priority=["official_regulator", "legal_text", "academic_review"],
                required_source_roles_by_claim_kind=REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND,
                compatibility_notes={},
            ),
        )

        self.assertEqual(len(citations), 1)
        self.assertEqual(claims[0].support_status, "weak")
        self.assertEqual(claims[0].required_source_roles, REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND["regulatory"])
        self.assertTrue(any("academic_review" in reason for reason in claims[0].blocking_reasons))
        self.assertTrue(any("official_regulator" in reason for reason in claims[0].blocking_reasons))


if __name__ == "__main__":
    unittest.main()
