from __future__ import annotations

import unittest

from runtime_bootstrap import ensure_repo_paths


ensure_repo_paths()

from cleanroom_runtime.models import (  # noqa: E402
    BudgetPlan,
    ClaimLedgerRow,
    DomainAdapter,
    DomainDecisionContext,
    MetricsSnapshot,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    SourceStrategy,
    TargetProfile,
)
from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.stage_contracts import audit_stage_output, stage_snapshot_schema  # noqa: E402
from cleanroom_runtime.utils import normalize_text  # noqa: E402

from support import make_finding, make_packet, make_request  # noqa: E402


class StageInvariantTests(unittest.TestCase):
    def test_pipeline_records_stage_snapshots_with_schema(self) -> None:
        request = make_request(
            packets=[
                make_packet(
                    "SRC-001",
                    "government_context",
                    findings=[
                        make_finding(
                            "finding-001",
                            "The runtime keeps reader-facing claims bounded to the checked evidence.",
                            "fact",
                            "medium",
                            "findings",
                            source_ids=["SRC-001"],
                        )
                    ],
                )
            ]
        )

        bundle = run_pipeline(request)
        snapshot_schema = stage_snapshot_schema()

        self.assertEqual(bundle.stage_failures, [])
        self.assertTrue(bundle.stage_snapshots)
        self.assertTrue(all(snapshot.contract_ok for snapshot in bundle.stage_snapshots))
        self.assertTrue(all(snapshot.snapshot_schema_version == snapshot_schema["snapshot_schema_version"] for snapshot in bundle.stage_snapshots))
        self.assertTrue(any(snapshot.stage == "release_gate" for snapshot in bundle.stage_snapshots))

    def test_report_plan_missing_sections_uses_schema_and_invariant_codes(self) -> None:
        failures, snapshot = audit_stage_output(
            "report_planner",
            {"sections": []},
            adapter=_adapter(),
            budget=_budget(),
            strategy=_strategy(),
        )

        codes = {failure.code for failure in failures}

        self.assertIn("SCHEMA_VALIDATION_FAILED", codes)
        self.assertIn("REPORT_PLAN_UNCERTAINTY_REQUIRED", codes)
        self.assertFalse(snapshot.contract_ok)

    def test_draft_stage_enforces_limitations_visibility(self) -> None:
        draft = ReportDraft(
            title="Synthetic draft",
            sections=[
                ReportSectionPlan(key="findings", title="What the evidence supports", purpose=""),
                ReportSectionPlan(key="uncertainty", title="Limitations and uncertainty", purpose=""),
            ],
            units=[
                ReportUnit(
                    unit_id="unit-001",
                    section_key="findings",
                    section_title="What the evidence supports",
                    text="The checked packet supports a bounded runtime statement.",
                    claim_kind="fact",
                    risk_level="medium",
                    source_ids=["SRC-001"],
                    source_roles=["government_context"],
                    confidence=0.8,
                ),
                ReportUnit(
                    unit_id="unit-002",
                    section_key="uncertainty",
                    section_title="Limitations and uncertainty",
                    text="Additional verification may still be useful.",
                    claim_kind="scope_boundary",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.9,
                    is_claim=False,
                ),
            ],
        )

        failures, _ = audit_stage_output(
            "draft_generator",
            draft,
            request=make_request(),
            adapter=_adapter(known_limits=["Only the checked packet was reviewed."]),
            evidence=_evidence(),
            report_plan=draft.sections,
            budget=_budget(limitations=["Only the checked packet was reviewed."]),
        )

        self.assertIn("DRAFT_LIMITATIONS_VISIBLE", {failure.code for failure in failures})

    def test_claim_extractor_enforces_full_claim_unit_coverage(self) -> None:
        draft = ReportDraft(
            title="Synthetic draft",
            sections=[ReportSectionPlan(key="findings", title="What the evidence supports", purpose="")],
            units=[
                _claim_unit("unit-001", "The first checked claim remains bounded."),
                _claim_unit("unit-002", "The second checked claim remains bounded."),
            ],
        )
        claims = [_claim("claim-001", "unit-001", "The first checked claim remains bounded.")]

        failures, _ = audit_stage_output(
            "claim_extractor",
            {"claims": claims},
            draft=draft,
            strategy=_strategy(),
        )

        self.assertIn("CLAIM_LEDGER_COVERAGE_MISMATCH", {failure.code for failure in failures})

    def test_metrics_stage_keeps_target_misses_aligned(self) -> None:
        failures, _ = audit_stage_output(
            "metrics_builder",
            MetricsSnapshot(
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
                target_results={"min_sources": True, "min_high_risk_sources": False},
                target_misses=[],
                target_miss_without_waiver=False,
                research_completeness="synthetic_validation_only",
            ),
            budget=_budget(),
        )

        self.assertIn("METRICS_TARGET_MISSES_ALIGN_RESULTS", {failure.code for failure in failures})


def _budget(*, limitations: list[str] | None = None) -> BudgetPlan:
    return BudgetPlan(
        requested_mode="scoped",
        effective_mode="scoped",
        preset_baseline_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        effective_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        override_reason="No override.",
        override_authority="runtime_default",
        full_dr_equivalent=False,
        report_status_implication="Synthetic validation proves contracts only.",
        limitations=limitations or ["Synthetic validation proves contracts only."],
        evidence_mode="synthetic",
        research_completeness_note="synthetic_validation_only",
        target_profile=TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=1),
        waivers=[],
    )


def _adapter(*, known_limits: list[str] | None = None) -> DomainAdapter:
    return DomainAdapter(
        topic="Stage invariant runtime",
        reader="runtime reviewers",
        use_context="validate stage invariants",
        output_type="report",
        risk_tier="medium",
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="medium",
        source_priority=["government_context"],
        high_risk_claim_types=["absence"],
        likely_failure_modes=["claim coverage drift"],
        domain_specific_risks=["bounded evidence overstated as complete"],
        common_misunderstandings=["claim capture is not support"],
        boundary_concepts=["claim vs evidence"],
        decision_context=DomainDecisionContext(
            primary_decision="validate stage invariants",
            failure_cost="moderate",
            time_horizon="near-term",
            reader_action="review bounded output",
        ),
        required_decision_layer=["What is safe to say"],
        required_tables=["Verification checklist"],
        must_not_overgeneralize=["Do not treat bounded evidence as exhaustive."],
        known_limits=known_limits or ["Synthetic validation proves contracts only."],
        source_roles_required_by_claim_kind={"fact": ["government_context"], "absence": ["official_regulator"]},
    )


def _strategy() -> SourceStrategy:
    return SourceStrategy(
        source_priority=["government_context"],
        required_source_roles_by_claim_kind={"fact": ["government_context"], "absence": ["official_regulator"]},
        compatibility_notes={"absence": "Absence must remain scoped."},
    )


def _evidence():
    from cleanroom_runtime.models import CollectedEvidence, SourcePacket

    return CollectedEvidence(
        sources=[SourcePacket(source_id="SRC-001", title="Checked source", source_role="government_context")],
        findings=[],
        source_counts_by_role={"government_context": 1},
        quality_notes=[],
    )


def _claim_unit(unit_id: str, text: str) -> ReportUnit:
    return ReportUnit(
        unit_id=unit_id,
        section_key="findings",
        section_title="What the evidence supports",
        text=text,
        claim_kind="fact",
        risk_level="medium",
        source_ids=["SRC-001"],
        source_roles=["government_context"],
        confidence=0.8,
    )


def _claim(claim_id: str, unit_id: str, text: str) -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id=claim_id,
        unit_id=unit_id,
        report_section="What the evidence supports",
        exact_text_span=text,
        normalized_claim=normalize_text(text),
        claim_kind="fact",
        risk_level="medium",
        source_ids=["SRC-001"],
        source_roles=["government_context"],
        evidence_count=1,
        required_source_roles=["government_context"],
        matched_source_roles=["government_context"],
        support_status="supported",
        confidence=0.8,
        caveat_required=False,
        suggested_tone="standard",
        required_fix="",
    )


if __name__ == "__main__":
    unittest.main()
