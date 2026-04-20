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
    CitationLedgerRow,
    ClaimLedgerRow,
    DomainAdapter,
    DomainDecisionContext,
    EvidenceGapEntry,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    TargetProfile,
)
from pseudo_pro_v2.stages.release_gate import decide_release_gate  # noqa: E402


class ReleaseGateTests(unittest.TestCase):
    def test_unsupported_high_risk_claim_blocks_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft("Direct answer"),
            claims=[
                _claim(
                    claim_id="claim-001",
                    claim_kind="regulatory",
                    risk_level="high",
                    support_status="weak",
                    required_role_matched=False,
                    role_fit_status="authoritative_mismatch",
                )
            ],
            citations=[_citation()],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(unsupported_high_risk_count=1, high_risk_supported_claim_ratio=0.0),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "blocked")

    def test_scoped_absence_claim_blocks_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft("Uncertainty and next research"),
            claims=[
                _claim(
                    claim_id="claim-001",
                    claim_kind="advice",
                    risk_level="medium",
                    support_status="supported",
                    report_section="Reader decision layer",
                    required_role_matched=True,
                    role_fit_status="required_match",
                ),
                _claim(
                    claim_id="claim-002",
                    claim_kind="absence",
                    risk_level="high",
                    support_status="missing",
                    included_in_report=False,
                    report_section="Uncertainty and next research",
                    required_role_matched=False,
                    role_fit_status="authoritative_mismatch",
                    exclusion_reason="Unsupported high-risk absence removed from reader-facing prose.",
                ),
            ],
            citations=[_citation(claim_id="claim-002", included_in_report=False)],
            contradictions=[],
            gaps=[_gap("claim-002", "absence")],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(
                claim_count=2,
                included_claim_count=1,
                excluded_claim_count=1,
                citation_count=1,
                included_citation_count=0,
                unsupported_high_risk_absence_count=1,
                supported_claim_ratio=0.5,
                high_risk_supported_claim_ratio=0.0,
            ),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "blocked")

    def test_target_miss_without_waiver_needs_revision(self) -> None:
        decision = decide_release_gate(
            draft=_draft("Direct answer"),
            claims=[_claim()],
            citations=[_citation()],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(target_miss_without_waiver=True, target_misses=["min_citations"]),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "needs_revision")

    def test_internal_heading_needs_revision(self) -> None:
        decision = decide_release_gate(
            draft=_draft("Claim audit"),
            claims=[_claim()],
            citations=[_citation()],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(internal_heading_present=True),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "needs_revision")

    def test_missing_claim_ledger_blocks_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft("Direct answer"),
            claims=[],
            citations=[_citation()],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(claim_count=0, included_claim_count=0),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "blocked")

    def test_synthetic_run_without_contract_is_provisional(self) -> None:
        decision = decide_release_gate(
            draft=_draft("Direct answer"),
            claims=[_claim(required_role_matched=True, role_fit_status="required_match")],
            citations=[_citation()],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(synthetic_inputs=True, synthetic_complete_allowed=False),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "provisional")

    def test_citation_trace_mismatch_blocks_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft("Direct answer"),
            claims=[_claim(required_role_matched=True, role_fit_status="required_match")],
            citations=[_citation()],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(metadata_consistent=False, citation_trace_consistent=False, rendered_citation_trace_consistent=False, citation_trace_mismatch_count=1),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "blocked")

    def test_user_document_review_without_grounding_needs_revision(self) -> None:
        adapter = _adapter()
        adapter.output_type = "user document review"
        decision = decide_release_gate(
            draft=_draft("Direct answer"),
            claims=[_claim(required_role_matched=True, role_fit_status="required_match")],
            citations=[_citation()],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=adapter,
            metrics=_metrics(document_grounding_present=False),
            validation_errors=[],
        )
        self.assertEqual(decision.status, "needs_revision")


def _draft(section_title: str) -> ReportDraft:
    return ReportDraft(
        title="Synthetic title",
        sections=[
            ReportSectionPlan(key="direct_answer", title=section_title, description=""),
            ReportSectionPlan(key="scope", title="Scope and exclusions", description="", target_claim_count=0),
            ReportSectionPlan(key="decision_layer", title="Reader decision layer", description="", target_claim_count=1),
            ReportSectionPlan(key="uncertainty", title="Uncertainty and next research", description="", target_claim_count=0),
            ReportSectionPlan(key="checklist", title="Checklist or decision table", description="", target_claim_count=0),
        ],
        units=[
            ReportUnit(
                unit_id="unit-000",
                section_key="direct_answer",
                section_title=section_title,
                text="Direct answer text.",
                claim_kind="fact",
                risk_level="medium",
                source_ids=["SRC-001"],
                source_roles=["professional_body"],
                confidence=0.9,
            ),
            ReportUnit(
                unit_id="unit-000a",
                section_key="scope",
                section_title="Scope and exclusions",
                text="This run is scoped and excludes unresolved edge cases.",
                claim_kind="scope_boundary",
                risk_level="low",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-001",
                section_key="decision_layer",
                section_title="Reader decision layer",
                text="Verify the decision-critical condition before acting.",
                claim_kind="advice",
                risk_level="medium",
                source_ids=["SRC-001"],
                source_roles=["professional_body"],
                confidence=0.9,
            ),
            ReportUnit(
                unit_id="unit-002",
                section_key="uncertainty",
                section_title="Uncertainty and next research",
                text="This run is scoped and not a full Deep Research equivalent.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-003",
                section_key="checklist",
                section_title="Checklist or decision table",
                text="Check: verify scope, support, and uncertainty labels.",
                claim_kind="scope_boundary",
                risk_level="low",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            ),
        ],
    )


def _claim(
    *,
    claim_id: str = "claim-001",
    claim_kind: str = "fact",
    risk_level: str = "medium",
    support_status: str = "supported",
    included_in_report: bool = True,
    report_section: str = "Direct answer",
    required_role_matched: bool = True,
    role_fit_status: str = "required_match",
    exclusion_reason: str = "",
) -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id=claim_id,
        report_section=report_section,
        exact_text_span="Synthetic claim text.",
        normalized_claim="synthetic claim text.",
        claim_kind=claim_kind,
        risk_level=risk_level,
        source_ids=["SRC-001"],
        source_roles=["official_regulator" if risk_level == "high" else "professional_body"],
        evidence_count=1,
        required_source_role=["official_regulator"] if risk_level == "high" else ["professional_body"],
        required_role_matched=required_role_matched,
        role_fit_status=role_fit_status,
        support_status=support_status,
        confidence=0.9,
        caveat_required=support_status != "supported",
        suggested_tone="standard",
        required_fix="",
        origin_finding_id="FINDING-001",
        included_in_report=included_in_report,
        exclusion_reason=exclusion_reason,
    )


def _citation(*, claim_id: str = "claim-001", included_in_report: bool = True) -> CitationLedgerRow:
    return CitationLedgerRow(
        citation_id="citation-001",
        claim_id=claim_id,
        report_section="Direct answer",
        source_id="SRC-001",
        source_role="official_regulator",
        source_title="Synthetic source",
        support_status="supported",
        included_in_report=included_in_report,
        origin_finding_id="FINDING-001",
    )


def _gap(claim_id: str, gap_type: str) -> EvidenceGapEntry:
    return EvidenceGapEntry(
        claim_id=claim_id,
        gap_type=gap_type,
        detail="Synthetic evidence gap.",
        required_fix="Synthetic fix.",
        severity="high",
    )


def _budget() -> BudgetPlan:
    return BudgetPlan(
        requested_mode="scoped",
        effective_mode="scoped",
        preset_baseline_budget={"min_sources": 3, "min_citations": 5, "min_report_claim_capture_ratio": 0.9},
        effective_budget={"min_sources": 3, "min_citations": 5, "min_report_claim_capture_ratio": 0.9},
        override_reason="No override.",
        override_authority="user_request",
        full_dr_equivalent=False,
        report_status_implication="This is a scoped run and not a full Deep Research equivalent.",
        limitations=["This run is scoped and not a full Deep Research equivalent."],
        target_profile=TargetProfile(min_sources=3, min_citations=5, min_report_claim_capture_ratio=0.9),
        waivers=[],
    )


def _adapter() -> DomainAdapter:
    return DomainAdapter(
        topic="synthetic_anchor",
        reader="Synthetic reader",
        use_context="Synthetic use context",
        output_type="report",
        risk_tier="medium",
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="medium",
        source_priority=["official_regulator", "professional_body"],
        high_risk_claim_types=["absence", "regulatory"],
        likely_failure_modes=["Scope drift."],
        domain_specific_risks=["Missing decision-critical constraint."],
        common_misunderstandings=["Captured does not mean supported."],
        boundary_concepts=["fact vs inference"],
        decision_context=DomainDecisionContext(
            primary_decision="What to do next.",
            failure_cost="medium",
            time_horizon="Immediate",
            reader_action="Verify before action.",
        ),
        required_decision_layer=[
            "What is already safe to say",
            "What still needs verification",
            "What decision should wait",
        ],
        required_tables=["Checklist or decision table"],
        must_not_overgeneralize=["Scoped evidence is not universal evidence."],
        known_limits=["This run is scoped."],
        source_roles_required_by_claim_kind={"fact": ["professional_body"], "regulatory": ["official_regulator"]},
    )


def _metrics(**overrides) -> dict:
    metrics = {
        "requested_mode": "scoped",
        "effective_mode": "scoped",
        "preset_baseline_budget": {"min_sources": 3, "min_citations": 5, "min_report_claim_capture_ratio": 0.9},
        "effective_budget": {"min_sources": 3, "min_citations": 5, "min_report_claim_capture_ratio": 0.9},
        "override_reason": "No override.",
        "override_authority": "user_request",
        "full_dr_equivalent": False,
        "report_status_implication": "This is a scoped run and not a full Deep Research equivalent.",
        "limitations": ["This run is scoped and not a full Deep Research equivalent."],
        "report_claim_capture_ratio": 1.0,
        "supported_claim_ratio": 1.0,
        "high_risk_claim_capture_ratio": 1.0,
        "high_risk_supported_claim_ratio": 1.0,
        "weak_claim_ratio": 0.0,
        "missing_claim_ratio": 0.0,
        "out_of_scope_claim_ratio": 0.0,
        "unsupported_high_risk_count": 0,
        "unsupported_high_risk_absence_count": 0,
        "claim_count": 1,
        "included_claim_count": 1,
        "excluded_claim_count": 0,
        "citation_count": 1,
        "included_citation_count": 1,
        "source_finding_count": 1,
        "captured_source_finding_count": 1,
        "source_finding_ledger_coverage_ratio": 1.0,
        "reader_decision_layer_present": True,
        "uncertainty_section_present": True,
        "metadata_consistent": True,
        "citation_trace_consistent": True,
        "rendered_citation_trace_consistent": True,
        "citation_trace_mismatch_count": 0,
        "document_grounding_present": True,
        "internal_heading_present": False,
        "target_results": {"min_sources": True, "min_citations": True, "min_report_claim_capture_ratio": True},
        "target_misses": [],
        "target_miss_without_waiver": False,
        "synthetic_inputs": True,
        "synthetic_complete_allowed": True,
        "release_status_candidate": "pending",
    }
    metrics.update(overrides)
    return metrics


if __name__ == "__main__":
    unittest.main()
