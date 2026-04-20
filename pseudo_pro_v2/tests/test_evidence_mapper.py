from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.models import ClaimLedgerRow, CollectedEvidence, SourcePacket, SourceStrategy  # noqa: E402
from pseudo_pro_v2.stages.evidence_mapper import map_claims_to_evidence  # noqa: E402


class EvidenceMapperTests(unittest.TestCase):
    def test_high_risk_role_mismatch_is_not_supported(self) -> None:
        claims = [
            ClaimLedgerRow(
                claim_id="claim-001",
                report_section="Direct answer",
                exact_text_span="Synthetic high-risk claim.",
                normalized_claim="synthetic high-risk claim.",
                claim_kind="regulatory",
                risk_level="high",
                source_ids=["SRC-001"],
                source_roles=["government_context"],
                evidence_count=1,
                required_source_role=["official_regulator", "legal_text", "court_or_authoritative_interpretation"],
                required_role_matched=False,
                role_fit_status="unknown",
                support_status="not_checked",
                confidence=0.9,
                caveat_required=False,
                suggested_tone="standard",
                required_fix="",
                origin_finding_id="FINDING-001",
            )
        ]
        evidence = CollectedEvidence(
            sources=[SourcePacket(source_id="SRC-001", title="Synthetic context", source_role="government_context")],
            findings=[],
            source_counts_by_role={"government_context": 1},
            quality_notes=[],
        )
        strategy = SourceStrategy(
            source_priority=["official_regulator", "government_context"],
            required_source_roles_by_claim_kind={
                "regulatory": ["official_regulator", "legal_text", "court_or_authoritative_interpretation"]
            },
            compatibility_notes={},
        )

        mapped_claims, _ = map_claims_to_evidence(claims, evidence, strategy)
        self.assertEqual(mapped_claims[0].support_status, "weak")
        self.assertFalse(mapped_claims[0].required_role_matched)
        self.assertEqual(mapped_claims[0].role_fit_status, "authoritative_mismatch")

    def test_high_risk_absence_requires_absence_roles(self) -> None:
        claims = [
            ClaimLedgerRow(
                claim_id="claim-001",
                report_section="Uncertainty and next research",
                exact_text_span="Synthetic absence claim.",
                normalized_claim="synthetic absence claim.",
                claim_kind="absence",
                risk_level="high",
                source_ids=["SRC-002"],
                source_roles=["academic_review"],
                evidence_count=1,
                required_source_role=["official_regulator", "legal_text", "court_or_authoritative_interpretation"],
                required_role_matched=False,
                role_fit_status="unknown",
                support_status="not_checked",
                confidence=0.85,
                caveat_required=False,
                suggested_tone="standard",
                required_fix="",
                origin_finding_id="FINDING-002",
                absence_type="explicitly_repealed",
            )
        ]
        evidence = CollectedEvidence(
            sources=[SourcePacket(source_id="SRC-002", title="Synthetic review", source_role="academic_review")],
            findings=[],
            source_counts_by_role={"academic_review": 1},
            quality_notes=[],
        )
        strategy = SourceStrategy(
            source_priority=["official_regulator", "academic_review"],
            required_source_roles_by_claim_kind={
                "absence": ["official_regulator", "legal_text", "court_or_authoritative_interpretation"]
            },
            compatibility_notes={},
        )

        mapped_claims, _ = map_claims_to_evidence(claims, evidence, strategy)
        self.assertEqual(mapped_claims[0].support_status, "missing")
        self.assertFalse(mapped_claims[0].required_role_matched)


if __name__ == "__main__":
    unittest.main()
