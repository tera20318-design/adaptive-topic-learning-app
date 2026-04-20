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


class OwnedReleaseGateTests(unittest.TestCase):
    def test_audit_only_high_risk_claim_still_blocks_with_explicit_reason(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[
                _claim(
                    claim_id="claim-001",
                    claim_kind="regulatory",
                    risk_level="high",
                    support_status="weak",
                    included_in_report=False,
                    blocking_reasons=[
                        "claim-001 `regulatory` claims require one of official_regulator, legal_text, court_or_authoritative_interpretation, but found academic_review."
                    ],
                )
            ],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "blocked")
        self.assertTrue(any("still blocks release" in reason for reason in decision.blocking_reasons))
        self.assertTrue(any(issue.blocks_release for issue in decision.claim_issues))

    def test_target_miss_without_waiver_needs_revision(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[_claim(claim_id="claim-001", claim_kind="fact", risk_level="medium", support_status="supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(target_miss_without_waiver=True, target_misses=["min_high_risk_sources"]),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "needs_revision")
        self.assertIn("min_high_risk_sources", decision.reasons[0])

    def test_synthetic_and_live_release_semantics_diverge(self) -> None:
        synthetic = decide_release_gate(
            draft=_draft(),
            claims=[_claim(claim_id="claim-001", claim_kind="fact", risk_level="medium", support_status="supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="synthetic_validation_only", evidence_mode="synthetic", full_dr_equivalent=False),
            adapter=_adapter(),
            metrics=_metrics(research_completeness="synthetic_validation_only"),
            validation_errors=[],
        )
        live = decide_release_gate(
            draft=_draft(),
            claims=[_claim(claim_id="claim-001", claim_kind="fact", risk_level="medium", support_status="supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(research_completeness="live_full_candidate"),
            validation_errors=[],
        )

        self.assertEqual(synthetic.status, "provisional")
        self.assertEqual(synthetic.research_completeness, "synthetic_validation_only")
        self.assertEqual(live.status, "complete")
        self.assertEqual(live.research_completeness, "live_full_candidate")

    def test_comparison_without_tradeoff_table_needs_revision(self) -> None:
        decision = decide_release_gate(
            draft=_draft(include_options=True),
            claims=[_claim(claim_id="claim-001", claim_kind="comparison", risk_level="medium", support_status="supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="live_scoped_only", evidence_mode="live", full_dr_equivalent=False),
            adapter=_adapter(required_tables=["Verification checklist", "Options or comparison table"]),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "needs_revision")
        self.assertTrue(any("tradeoff table" in reason for reason in decision.reasons))

    def test_high_risk_finance_guidance_without_risk_disclosure_blocks(self) -> None:
        decision = decide_release_gate(
            draft=_draft(include_risk_disclosure=False),
            claims=[_claim(claim_id="claim-001", claim_kind="financial", risk_level="high", support_status="supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "blocked")
        self.assertTrue(any("risk disclosure" in reason for reason in decision.blocking_reasons))

    def test_scoped_search_absence_in_mainline_blocks(self) -> None:
        from cleanroom_runtime.models import AbsenceScope

        decision = decide_release_gate(
            draft=_draft(),
            claims=[
                _claim(
                    claim_id="claim-001",
                    claim_kind="absence",
                    risk_level="high",
                    support_status="scoped_absence",
                    absence_scope=AbsenceScope(
                        subject="the target condition",
                        scope_label="scoped search",
                        basis="not_found_in_scoped_search",
                        checked_source_ids=["SRC-001"],
                    ),
                )
            ],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(),
            validation_errors=[],
        )

        self.assertEqual(decision.status, "blocked")
        self.assertTrue(any("scoped-search absence" in reason for reason in decision.blocking_reasons))

    def test_semantic_fixture_leakage_blocks_cleanroom_integrity(self) -> None:
        decision = decide_release_gate(
            draft=_draft(),
            claims=[_claim(claim_id="claim-001", claim_kind="fact", risk_level="medium", support_status="supported")],
            citations=[_citation("claim-001")],
            contradictions=[],
            gaps=[],
            budget=_budget(research_note="live_full_candidate", evidence_mode="live", full_dr_equivalent=True),
            adapter=_adapter(),
            metrics=_metrics(research_completeness="live_full_candidate"),
            validation_errors=["SEMANTIC_FIXTURE_NOUN_LEAK: foreign fixture noun reached reader-facing output"],
        )

        self.assertEqual(decision.status, "blocked")
        self.assertTrue(any(issue.stage == "cleanroom_integrity" for issue in decision.claim_issues))


def _draft(*, include_options: bool = False, include_risk_disclosure: bool = True) -> ReportDraft:
    units = [
        ReportUnit(
            unit_id="unit-001",
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
        ),
        ReportUnit(
            unit_id="unit-003",
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
            unit_id="unit-004",
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
            unit_id="unit-005",
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
    ]
    if include_risk_disclosure:
        units.append(
            ReportUnit(
                unit_id="unit-006",
                section_key="uncertainty",
                section_title="Limitations and uncertainty",
                text="Risk disclosure: downside and suitability still depend on the reader's constraints.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            )
        )
    if include_options:
        units.extend(
            [
                ReportUnit(
                    unit_id="unit-007",
                    section_key="options",
                    section_title="Options compared",
                    text="Option A favors lower setup cost.",
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
                    text="Option B favors lower operating overhead.",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
            ]
        )
    return ReportDraft(
        title="Synthetic draft",
        sections=[
            ReportSectionPlan(key="direct_answer", title="Direct answer", purpose=""),
            ReportSectionPlan(key="scope", title="Scope and exclusions", purpose=""),
            ReportSectionPlan(key="findings", title="What the evidence supports", purpose=""),
            ReportSectionPlan(key="decision_layer", title="Checks before you act", purpose=""),
            ReportSectionPlan(key="checklist", title="Verification checklist", purpose=""),
            ReportSectionPlan(key="uncertainty", title="Limitations and uncertainty", purpose=""),
            *([ReportSectionPlan(key="options", title="Options compared", purpose="")] if include_options else []),
        ],
        units=units,
    )


def _claim(
    *,
    claim_id: str,
    claim_kind: str,
    risk_level: str,
    support_status: str,
    included_in_report: bool = True,
    blocking_reasons: list[str] | None = None,
    absence_scope=None,
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
        matched_source_roles=["official_regulator"] if support_status == "supported" and risk_level == "high" else [],
        support_status=support_status,
        confidence=0.9,
        caveat_required=support_status != "supported",
        suggested_tone="standard",
        required_fix="",
        included_in_report=included_in_report,
        blocking_reasons=blocking_reasons or [],
        absence_scope=absence_scope,
    )


def _citation(claim_id: str):
    from cleanroom_runtime.models import CitationLedgerRow

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


def _budget(*, research_note: str, evidence_mode: str, full_dr_equivalent: bool) -> BudgetPlan:
    return BudgetPlan(
        requested_mode="full" if full_dr_equivalent else "scoped",
        effective_mode="full" if full_dr_equivalent else "scoped",
        preset_baseline_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        effective_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        override_reason="No override.",
        override_authority="runtime_default",
        full_dr_equivalent=full_dr_equivalent,
        report_status_implication="Synthetic validation proves contracts only." if evidence_mode == "synthetic" else "Live release candidate.",
        limitations=[],
        evidence_mode=evidence_mode,
        research_completeness_note=research_note,
        target_profile=TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=1),
        waivers=[],
    )


def _adapter(*, required_tables: list[str] | None = None) -> DomainAdapter:
    return DomainAdapter(
        topic="Synthetic topic",
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
