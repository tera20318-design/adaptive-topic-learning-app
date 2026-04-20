from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.models import (  # noqa: E402
    BudgetPlan,
    ClaimLedgerRow,
    DomainAdapter,
    DomainDecisionContext,
    MetricsSnapshot,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    TargetProfile,
)
from cleanroom_runtime.stages.release_gate import decide_release_gate  # noqa: E402


class ReleaseGateTests(unittest.TestCase):
    def test_included_unsupported_high_risk_claim_blocks_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[
                ClaimLedgerRow(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    report_section="Findings",
                    exact_text_span="Synthetic high-risk claim.",
                    normalized_claim="synthetic high-risk claim.",
                    claim_kind="regulatory",
                    risk_level="high",
                    source_ids=["SRC-001"],
                    source_roles=["trade_media"],
                    evidence_count=1,
                    required_source_roles=["official_regulator"],
                    matched_source_roles=[],
                    support_status="weak",
                    confidence=0.4,
                    caveat_required=True,
                    suggested_tone="tentative",
                    required_fix="Add role-matched support.",
                    included_in_report=True,
                )
            ],
            citations=[],
            contradictions=[],
            gaps=[],
            budget=_budget("live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(unresolved_high_risk_claim_count=1, high_risk_role_mismatch_count=1, included_high_risk_claim_count=1, included_unsupported_claim_count=1),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "blocked")
        self.assertTrue(any(issue.blocks_release for issue in decision.claim_issues))

    def test_synthetic_run_cannot_become_complete(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[_supported_claim()],
            citations=[],
            contradictions=[],
            gaps=[],
            budget=_budget("synthetic_validation_only", evidence_mode="synthetic", full_dr_equivalent=False),
            adapter=_adapter(),
            metrics=_metrics(
                included_supported_claim_count=1,
                included_unsupported_claim_count=0,
                included_high_risk_claim_count=0,
                unresolved_high_risk_claim_count=0,
                high_risk_role_mismatch_count=0,
                research_completeness="synthetic_validation_only",
            ),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "provisional")
        self.assertEqual(decision.research_completeness, "synthetic_validation_only")

    def test_live_full_supported_run_can_complete(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[_supported_claim()],
            citations=[],
            contradictions=[],
            gaps=[],
            budget=_budget("live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(
                included_supported_claim_count=1,
                included_unsupported_claim_count=0,
                included_high_risk_claim_count=0,
                unresolved_high_risk_claim_count=0,
                high_risk_role_mismatch_count=0,
                research_completeness="live_full_candidate",
            ),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "complete")
        self.assertEqual(decision.research_completeness, "live_full_candidate")


def _draft() -> ReportDraft:
    return ReportDraft(
        title="Synthetic draft",
        sections=[
            ReportSectionPlan(key="direct_answer", title="Direct answer", purpose=""),
            ReportSectionPlan(key="scope", title="Scope and exclusions", purpose=""),
            ReportSectionPlan(key="findings", title="Findings", purpose=""),
            ReportSectionPlan(key="decision_layer", title="Checks before you act", purpose=""),
            ReportSectionPlan(key="checklist", title="Verification checklist", purpose=""),
            ReportSectionPlan(key="uncertainty", title="Limitations and uncertainty", purpose=""),
        ],
        units=[
            ReportUnit(
                unit_id="unit-100",
                section_key="direct_answer",
                section_title="Direct answer",
                text="The checked material supports a bounded answer for the reader.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-101",
                section_key="scope",
                section_title="Scope and exclusions",
                text="Excluded from this run are unchecked jurisdictions, unchecked dates, and claims that still need stronger support.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-102",
                section_key="decision_layer",
                section_title="Checks before you act",
                text="Next action: verify support before acting.",
                claim_kind="advice",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.8,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-103",
                section_key="checklist",
                section_title="Verification checklist",
                text="Verify claim-kind source-role fit before acting on any high-risk statement.",
                claim_kind="advice",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.8,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-104",
                section_key="uncertainty",
                section_title="Limitations and uncertainty",
                text="Uncertainty remains wherever the checked materials do not establish exhaustive coverage outside the declared scope.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            ),
        ],
    )


def _supported_claim() -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id="claim-010",
        unit_id="unit-010",
        report_section="Findings",
        exact_text_span="Supported medium-risk claim.",
        normalized_claim="supported medium-risk claim.",
        claim_kind="fact",
        risk_level="medium",
        source_ids=["SRC-001"],
        source_roles=["government_context"],
        evidence_count=1,
        required_source_roles=["government_context"],
        matched_source_roles=["government_context"],
        support_status="supported",
        confidence=0.9,
        caveat_required=False,
        suggested_tone="standard",
        required_fix="",
        included_in_report=True,
    )


def _budget(research_note: str, *, evidence_mode: str, full_dr_equivalent: bool) -> BudgetPlan:
    return BudgetPlan(
        requested_mode="full",
        effective_mode="full",
        preset_baseline_budget={"min_sources": 5, "min_distinct_roles": 3, "min_high_risk_sources": 2},
        effective_budget={"min_sources": 5, "min_distinct_roles": 3, "min_high_risk_sources": 2},
        override_reason="No override.",
        override_authority="runtime_default",
        full_dr_equivalent=full_dr_equivalent,
        report_status_implication="Synthetic validation proves contracts only." if evidence_mode == "synthetic" else "Live full run.",
        limitations=[],
        evidence_mode=evidence_mode,
        research_completeness_note=research_note,
        target_profile=TargetProfile(min_sources=5, min_distinct_roles=3, min_high_risk_sources=2),
        waivers=[],
    )


def _adapter() -> DomainAdapter:
    return DomainAdapter(
        topic="Synthetic",
        reader="reviewer",
        use_context="test gate",
        output_type="report",
        risk_tier="high",
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="medium",
        source_priority=["official_regulator"],
        high_risk_claim_types=["regulatory"],
        likely_failure_modes=["role mismatch"],
        domain_specific_risks=["unsupported high-risk claim"],
        common_misunderstandings=["claim capture is not support"],
        boundary_concepts=["capture vs support"],
        decision_context=DomainDecisionContext(
            primary_decision="release or block",
            failure_cost="high",
            time_horizon="near-term",
            reader_action="verify support",
        ),
        required_decision_layer=["What is safe to say"],
        required_tables=["Verification checklist"],
        must_not_overgeneralize=["Do not treat weak support as complete."],
        known_limits=[],
        source_roles_required_by_claim_kind={"regulatory": ["official_regulator"]},
    )


def _metrics(**overrides) -> MetricsSnapshot:
    values = dict(
        total_claim_count=1,
        included_claim_count=1,
        excluded_claim_count=0,
        included_supported_claim_count=0,
        included_scoped_absence_count=0,
        included_unsupported_claim_count=1,
        included_high_risk_claim_count=1,
        excluded_high_risk_claim_count=0,
        unresolved_high_risk_claim_count=1,
        high_risk_role_mismatch_count=1,
        unscoped_absence_count=0,
        contradiction_count=0,
        evidence_gap_count=0,
        distinct_source_count=1,
        distinct_source_role_count=1,
        duplicate_claim_count=0,
        audit_complete=True,
        citation_trace_complete=True,
        uncertainty_section_present=True,
        limitations_visible=True,
        target_results={"min_sources": True, "min_distinct_roles": True, "min_high_risk_sources": True},
        target_misses=[],
        target_miss_without_waiver=False,
        research_completeness="live_full_candidate",
    )
    values.update(overrides)
    return MetricsSnapshot(**values)


if __name__ == "__main__":
    unittest.main()
