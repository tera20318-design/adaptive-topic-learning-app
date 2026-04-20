from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.models import (  # noqa: E402
    AbsenceScope,
    BudgetPlan,
    ClaimLedgerRow,
    CitationLedgerRow,
    DomainAdapter,
    DomainDecisionContext,
    MetricsSnapshot,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    TargetProfile,
)
from cleanroom_runtime.stages.release_gate import decide_release_gate  # noqa: E402


class ReleaseGateQualityTests(unittest.TestCase):
    def test_document_review_without_grounding_needs_revision(self) -> None:
        decision = decide_release_gate(
            draft=_draft(direct_answer_text="The answer is mixed for the reader."),
            claims=[_claim("claim-001", "fact", "medium", "supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(use_context="review the document packet for grounded findings"),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "needs_revision")
        self.assertTrue(any("grounding statements" in reason for reason in decision.reasons))

    def test_historical_or_cultural_generic_uncertainty_needs_revision(self) -> None:
        decision = decide_release_gate(
            draft=_draft(uncertainty_text="History is complex, interpretations vary, and more research is needed."),
            claims=[_claim("claim-001", "fact", "low", "supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(topic="Historical cultural overview", use_context="summarize a historical and cultural overview"),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "needs_revision")
        self.assertTrue(any("uncertainty" in reason.casefold() for reason in decision.reasons))

    def test_technical_overview_without_scope_boundary_needs_revision(self) -> None:
        decision = decide_release_gate(
            draft=_draft(include_scope=False),
            claims=[_claim("claim-001", "fact", "medium", "supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(topic="Technical overview", use_context="explain the mechanism and limits"),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "needs_revision")
        self.assertTrue(any("scope and exclusions" in reason.casefold() for reason in decision.reasons))

    def test_legal_or_regulatory_scoped_packet_absence_blocks(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[
                _claim(
                    "claim-001",
                    "absence",
                    "high",
                    "scoped_absence",
                    absence_scope=AbsenceScope(
                        subject="the target rule",
                        scope_label="checked regulatory packet",
                        basis="not_found_in_checked_scope",
                        checked_source_ids=["SRC-001"],
                    ),
                )
            ],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(topic="Regulatory packet review", use_context="review the regulatory packet"),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "blocked")
        self.assertTrue(any("scoped-search absence" in reason for reason in decision.blocking_reasons))

    def test_finance_downside_disclosure_allows_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft(include_risk_disclosure=True),
            claims=[_claim("claim-001", "financial", "medium", "supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "complete")

    def test_product_comparison_tradeoff_table_allows_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft(include_tradeoff_table=True),
            claims=[_claim("claim-001", "comparison", "medium", "supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(required_tables=["Verification checklist", "Options or comparison table"]),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "complete")

    def test_metadata_inconsistency_plus_unsupported_high_risk_claim_blocks(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[_claim("claim-001", "regulatory", "high", "weak", matched_source_roles=[])],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(
                audit_complete=False,
                citation_trace_complete=False,
                included_supported_claim_count=0,
                included_unsupported_claim_count=1,
                included_high_risk_claim_count=1,
                unresolved_high_risk_claim_count=1,
                high_risk_role_mismatch_count=1,
            ),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "blocked")
        self.assertFalse(decision.metadata_consistent)
        self.assertTrue(any("Audit coverage is incomplete" in reason for reason in decision.blocking_reasons))
        self.assertTrue(any("Included high-risk claim is not adequately supported" in reason for reason in decision.blocking_reasons))

    def test_citation_trace_mismatch_blocks_release(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[_claim("claim-001", "fact", "medium", "supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(),
            adapter=_adapter(),
            metrics=_metrics(citation_trace_complete=False),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "blocked")
        self.assertFalse(decision.metadata_consistent)
        self.assertTrue(any(issue.stage == "audit" and "Citation traceability is incomplete." in issue.message for issue in decision.claim_issues))


def _draft(
    *,
    direct_answer_text: str = "The checked material supports a bounded answer for the reader.",
    uncertainty_text: str = "Uncertainty remains wherever the checked materials do not establish exhaustive coverage outside the declared scope.",
    include_scope: bool = True,
    include_risk_disclosure: bool = True,
    include_tradeoff_table: bool = False,
) -> ReportDraft:
    sections = [ReportSectionPlan(key="direct_answer", title="Direct answer", purpose="")]
    units = [
        ReportUnit(
            unit_id="unit-001",
            section_key="direct_answer",
            section_title="Direct answer",
            text=direct_answer_text,
            claim_kind="scope_boundary",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            is_claim=False,
        )
    ]
    if include_scope:
        sections.append(ReportSectionPlan(key="scope", title="Scope and exclusions", purpose=""))
        units.append(
            ReportUnit(
                unit_id="unit-002",
                section_key="scope",
                section_title="Scope and exclusions",
                text="Excluded from this run are unchecked jurisdictions, unchecked dates, and claims that still need stronger support.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            )
        )
    sections.extend(
        [
            ReportSectionPlan(key="decision_layer", title="Checks before you act", purpose=""),
            ReportSectionPlan(key="checklist", title="Verification checklist", purpose=""),
            ReportSectionPlan(key="uncertainty", title="Limitations and uncertainty", purpose=""),
        ]
    )
    units.extend(
        [
            ReportUnit(
                unit_id="unit-003",
                section_key="decision_layer",
                section_title="Checks before you act",
                text="Next action: verify the cited support against the reader decision before acting.",
                claim_kind="advice",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.8,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-004",
                section_key="checklist",
                section_title="Verification checklist",
                text="Verify the checked support and packet scope before deciding.",
                claim_kind="advice",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.8,
                is_claim=False,
            ),
            ReportUnit(
                unit_id="unit-005",
                section_key="uncertainty",
                section_title="Limitations and uncertainty",
                text=uncertainty_text,
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            ),
        ]
    )
    if include_risk_disclosure:
        units.append(
            ReportUnit(
                unit_id="unit-006",
                section_key="uncertainty",
                section_title="Limitations and uncertainty",
                text="Risk disclosure: the downside and suitability still depend on the reader's constraints and tolerance for loss.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            )
        )
    if include_tradeoff_table:
        sections.append(ReportSectionPlan(key="options", title="Options compared", purpose=""))
        units.extend(
            [
                ReportUnit(
                    unit_id="unit-007",
                    section_key="options",
                    section_title="Options compared",
                    text="Option | Main tradeoff | Downside",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
                ReportUnit(
                    unit_id="unit-008",
                    section_key="options",
                    section_title="Options compared",
                    text="Option A | Lower setup cost tradeoff | Higher maintenance downside",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
                ReportUnit(
                    unit_id="unit-009",
                    section_key="options",
                    section_title="Options compared",
                    text="Option B | Higher setup cost tradeoff | Lower maintenance downside",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
            ]
        )
    return ReportDraft(title="Synthetic quality gate draft", sections=sections, units=units)


def _claim(
    claim_id: str,
    claim_kind: str,
    risk_level: str,
    support_status: str,
    *,
    absence_scope=None,
    matched_source_roles: list[str] | None = None,
) -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id=claim_id,
        unit_id=claim_id.replace("claim", "unit"),
        report_section="What the evidence supports",
        exact_text_span="Synthetic claim text.",
        normalized_claim="synthetic claim text.",
        claim_kind=claim_kind,
        risk_level=risk_level,
        source_ids=["SRC-001"],
        source_roles=["official_regulator" if risk_level == "high" else "government_context"],
        evidence_count=1,
        required_source_roles=["official_regulator"] if risk_level == "high" else ["government_context"],
        matched_source_roles=matched_source_roles if matched_source_roles is not None else (["official_regulator"] if risk_level == "high" else ["government_context"]),
        support_status=support_status,
        confidence=0.9,
        caveat_required=support_status != "supported",
        suggested_tone="standard",
        required_fix="",
        included_in_report=True,
        absence_scope=absence_scope,
    )


def _citation(claim_id: str) -> CitationLedgerRow:
    return CitationLedgerRow(
        citation_id="citation-001",
        claim_id=claim_id,
        report_section="What the evidence supports",
        source_id="SRC-001",
        source_role="official_regulator",
        source_title="Synthetic source",
        support_status="supported",
        included_in_report=True,
    )


def _budget() -> BudgetPlan:
    return BudgetPlan(
        requested_mode="full",
        effective_mode="full",
        preset_baseline_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        effective_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        override_reason="No override.",
        override_authority="runtime_default",
        full_dr_equivalent=True,
        report_status_implication="Live release candidate.",
        limitations=[],
        evidence_mode="live",
        research_completeness_note="live_full_candidate",
        target_profile=TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=1),
        waivers=[],
    )


def _adapter(*, topic: str = "Synthetic topic", use_context: str = "test release gate quality", required_tables: list[str] | None = None) -> DomainAdapter:
    return DomainAdapter(
        topic=topic,
        reader="reviewer",
        use_context=use_context,
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
            primary_decision="support a bounded decision",
            failure_cost="high",
            time_horizon="near-term",
            reader_action="verify the checked support before deciding",
        ),
        required_decision_layer=["What is safe to say"],
        required_tables=required_tables or ["Verification checklist"],
        must_not_overgeneralize=["Do not treat weak support as complete."],
        known_limits=[],
        source_roles_required_by_claim_kind={"regulatory": ["official_regulator"]},
    )


def _metrics(**overrides) -> MetricsSnapshot:
    values = dict(
        total_claim_count=1,
        included_claim_count=1,
        excluded_claim_count=0,
        included_supported_claim_count=1,
        included_scoped_absence_count=0,
        included_unsupported_claim_count=0,
        included_high_risk_claim_count=0,
        excluded_high_risk_claim_count=0,
        unresolved_high_risk_claim_count=0,
        high_risk_role_mismatch_count=0,
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
