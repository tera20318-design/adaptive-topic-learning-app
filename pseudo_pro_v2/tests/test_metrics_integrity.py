from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.models import (  # noqa: E402
    BudgetPlan,
    ClaimLedgerRow,
    CitationLedgerRow,
    CollectedEvidence,
    ReleaseContract,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    RunRequest,
    SourceFinding,
    SourcePacket,
    TargetProfile,
)
from pseudo_pro_v2.pipeline import _build_metrics  # noqa: E402


class MetricsIntegrityTests(unittest.TestCase):
    def test_metrics_detect_missing_lineage_and_metadata_mismatch(self) -> None:
        request = RunRequest(
            topic="synthetic_anchor",
            reader="reader",
            use_context="use context",
            desired_depth="technical overview",
            jurisdiction="Generic Global",
            mode="scoped",
            evidence_mode="synthetic",
            release_contract=ReleaseContract(allow_synthetic_complete=False),
        )
        budget = BudgetPlan(
            requested_mode="scoped",
            effective_mode="scoped",
            preset_baseline_budget={"min_sources": 1, "min_citations": 1, "min_report_claim_capture_ratio": 0.9},
            effective_budget={"min_sources": 1, "min_citations": 1, "min_report_claim_capture_ratio": 0.9},
            override_reason="No override.",
            override_authority="user_request",
            full_dr_equivalent=False,
            report_status_implication="Scoped only.",
            limitations=["Scoped only."],
            target_profile=TargetProfile(min_sources=1, min_citations=1, min_report_claim_capture_ratio=0.9),
        )
        evidence = CollectedEvidence(
            sources=[
                SourcePacket(source_id="SRC-001", title="Synthetic source one", source_role="professional_body"),
                SourcePacket(source_id="SRC-002", title="Synthetic source two", source_role="professional_body"),
            ],
            findings=[
                SourceFinding(finding_id="FINDING-001", statement="First claim.", claim_kind="fact", risk_level="medium", section_hint="findings"),
                SourceFinding(finding_id="FINDING-002", statement="Second claim.", claim_kind="fact", risk_level="medium", section_hint="findings"),
            ],
            source_counts_by_role={"professional_body": 2},
            quality_notes=[],
        )
        draft = ReportDraft(
            title="synthetic_anchor",
            sections=[ReportSectionPlan(key="findings", title="Evidence-backed findings", description="")],
            units=[
                ReportUnit(
                    unit_id="unit-001",
                    section_key="findings",
                    section_title="Evidence-backed findings",
                    text="First claim.",
                    claim_kind="fact",
                    risk_level="medium",
                    source_ids=["SRC-001"],
                    source_roles=["professional_body"],
                    confidence=0.9,
                )
            ],
        )
        claims = [
            ClaimLedgerRow(
                claim_id="claim-001",
                report_section="Evidence-backed findings",
                exact_text_span="First claim.",
                normalized_claim="first claim.",
                claim_kind="fact",
                risk_level="medium",
                source_ids=["SRC-001"],
                source_roles=["professional_body"],
                evidence_count=1,
                required_source_role=["professional_body"],
                required_role_matched=True,
                role_fit_status="required_match",
                support_status="supported",
                confidence=0.9,
                caveat_required=False,
                suggested_tone="standard",
                required_fix="",
                origin_finding_id="FINDING-001",
            )
        ]
        citations = [
            CitationLedgerRow(
                citation_id="citation-001",
                claim_id="claim-001",
                report_section="Evidence-backed findings",
                source_id="SRC-002",
                source_role="professional_body",
                source_title="Synthetic source two",
                support_status="supported",
                included_in_report=True,
                origin_finding_id="FINDING-001",
            )
        ]
        report_text = "# synthetic_anchor\n\n## Evidence-backed findings\n\n- First claim. [SRC-001]\n"

        metrics = _build_metrics(request, budget, evidence, draft, claims, citations, report_text)

        self.assertLess(metrics["source_finding_ledger_coverage_ratio"], 1.0)
        self.assertFalse(metrics["metadata_consistent"])
        self.assertLess(metrics["supported_claim_ratio"], 1.01)


if __name__ == "__main__":
    unittest.main()
