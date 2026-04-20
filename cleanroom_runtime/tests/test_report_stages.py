from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.models import (  # noqa: E402
    BudgetPlan,
    ClaimLedgerRow,
    CollectedEvidence,
    DomainAdapter,
    DomainDecisionContext,
    RiskTierResult,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    RunRequest,
    SourceFinding,
    SourcePacket,
    SourceStrategy,
    TargetProfile,
)
from cleanroom_runtime.stages.bundle_renderer import render_bundle  # noqa: E402
from cleanroom_runtime.stages.draft_generator import write_draft  # noqa: E402
from cleanroom_runtime.stages.report_planner import plan_report  # noqa: E402
from cleanroom_runtime.stages.tone_control import apply_tone_control  # noqa: E402
from cleanroom_runtime.utils import normalize_text  # noqa: E402


class ReportStageTests(unittest.TestCase):
    def test_plan_report_is_adapter_aware_and_reader_facing(self) -> None:
        sections = plan_report(_intent("comparison_report"), _adapter(required_tables=["Options or comparison table"]), _budget(), _strategy())
        titles = [section.title for section in sections]

        self.assertIn("Options compared", titles)
        self.assertIn("Checks before you act", titles)
        self.assertIn("Limitations and uncertainty", titles)
        for title in titles:
            lowered = title.casefold()
            self.assertNotIn("audit", lowered)
            self.assertNotIn("pipeline", lowered)
            self.assertNotIn("matrix", lowered)

    def test_write_draft_keeps_limitations_visible_and_deduplicates_findings(self) -> None:
        request = _request()
        adapter = _adapter(required_tables=["Options or comparison table"], known_limits=["Only a small checked packet was available."])
        evidence = CollectedEvidence(
            sources=[SourcePacket(source_id="SRC-001", title="Checked source", source_role="government_context")],
            findings=[
                SourceFinding(
                    finding_id="finding-001",
                    statement="Adapter generation should happen before report planning.",
                    claim_kind="fact",
                    risk_level="medium",
                    section_hint="direct_answer",
                    source_ids=["SRC-001"],
                ),
                SourceFinding(
                    finding_id="finding-002",
                    statement="Adapter generation should happen before report planning.",
                    claim_kind="fact",
                    risk_level="medium",
                    section_hint="findings",
                    source_ids=["SRC-001"],
                ),
                SourceFinding(
                    finding_id="finding-003",
                    statement="The checked packet does not establish rollout timing.",
                    claim_kind="absence",
                    risk_level="medium",
                    section_hint="uncertainty",
                    source_ids=["SRC-001"],
                ),
            ],
            source_counts_by_role={"government_context": 1},
            quality_notes=[],
        )

        draft = write_draft(request, adapter, evidence, plan_report(_intent("comparison_report"), adapter, _budget(), _strategy()), _budget())

        claim_units = [unit for unit in draft.units if unit.is_claim]
        normalized = [normalize_text(unit.text) for unit in claim_units]
        uncertainty_units = [unit for unit in draft.units if unit.section_key == "uncertainty"]

        self.assertEqual(len(normalized), len(set(normalized)))
        self.assertTrue(any("Only a small checked packet was available." in unit.text for unit in uncertainty_units))
        self.assertTrue(any(section.key == "options" for section in draft.sections))

    def test_tone_control_marks_weak_claims_and_hides_excluded_units(self) -> None:
        draft = ReportDraft(
            title="Synthetic report",
            sections=[ReportSectionPlan(key="findings", title="Key evidence-backed findings", purpose="")],
            units=[
                ReportUnit(
                    unit_id="unit-001",
                    section_key="findings",
                    section_title="Key evidence-backed findings",
                    text="Adapters reduce accidental scope drift.",
                    claim_kind="fact",
                    risk_level="medium",
                    source_ids=["SRC-001"],
                    source_roles=["government_context"],
                    confidence=0.8,
                ),
                ReportUnit(
                    unit_id="unit-002",
                    section_key="findings",
                    section_title="Key evidence-backed findings",
                    text="Internal rollout timing is confirmed.",
                    claim_kind="fact",
                    risk_level="high",
                    source_ids=["SRC-001"],
                    source_roles=["trade_media"],
                    confidence=0.4,
                    include_in_report=False,
                ),
            ],
        )
        claims = [
            ClaimLedgerRow(
                claim_id="claim-001",
                unit_id="unit-001",
                report_section="Key evidence-backed findings",
                exact_text_span="Adapters reduce accidental scope drift.",
                normalized_claim="adapters reduce accidental scope drift.",
                claim_kind="fact",
                risk_level="medium",
                source_ids=["SRC-001"],
                source_roles=["government_context"],
                evidence_count=1,
                required_source_roles=["government_context"],
                matched_source_roles=["government_context"],
                support_status="weak",
                confidence=0.8,
                caveat_required=True,
                suggested_tone="tentative",
                required_fix="Add stronger support.",
                included_in_report=True,
            ),
            ClaimLedgerRow(
                claim_id="claim-002",
                unit_id="unit-002",
                report_section="Key evidence-backed findings",
                exact_text_span="Internal rollout timing is confirmed.",
                normalized_claim="internal rollout timing is confirmed.",
                claim_kind="fact",
                risk_level="high",
                source_ids=["SRC-001"],
                source_roles=["trade_media"],
                evidence_count=1,
                required_source_roles=["official_regulator"],
                matched_source_roles=[],
                support_status="missing",
                confidence=0.4,
                caveat_required=True,
                suggested_tone="withhold",
                required_fix="Exclude from reader-facing prose.",
                included_in_report=False,
            ),
        ]

        toned = apply_tone_control(draft, claims)

        unit_one = next(unit for unit in toned.units if unit.unit_id == "unit-001")
        unit_two = next(unit for unit in toned.units if unit.unit_id == "unit-002")

        self.assertTrue(unit_one.text.startswith("Current checked materials suggest"))
        self.assertFalse(unit_two.include_in_report)

    def test_render_bundle_lists_included_and_excluded_claims(self) -> None:
        bundle = _bundle_for_render()

        with tempfile.TemporaryDirectory() as tmp_dir:
            render_bundle(bundle, Path(tmp_dir))
            report_text = Path(tmp_dir, "final_report.md").read_text(encoding="utf-8")
            included_text = Path(tmp_dir, "included-claims.tsv").read_text(encoding="utf-8")
            excluded_text = Path(tmp_dir, "excluded-claims.tsv").read_text(encoding="utf-8")

        self.assertIn("Adapters reduce accidental scope drift.", report_text)
        self.assertNotIn("Internal rollout timing is confirmed.", report_text)
        self.assertIn("claim-001", included_text)
        self.assertIn("claim-002", excluded_text)


def _request() -> RunRequest:
    return RunRequest(
        topic="Adapter-aware runtime",
        reader="team leads",
        use_context="compare runtime trustworthiness",
        desired_depth="medium",
        jurisdiction="JP",
        mode="scoped",
        evidence_mode="synthetic",
    )


def _intent(label: str):
    from cleanroom_runtime.models import IntentResult

    return IntentResult(
        intent_label=label,
        decision_focus="compare bounded tradeoffs",
        reader_task="decide what to verify next",
        report_shape_hints=["options", "decision_layer"],
    )


def _budget() -> BudgetPlan:
    return BudgetPlan(
        requested_mode="scoped",
        effective_mode="scoped",
        preset_baseline_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        effective_budget={"min_sources": 3, "min_distinct_roles": 2, "min_high_risk_sources": 1},
        override_reason="No override.",
        override_authority="runtime_default",
        full_dr_equivalent=False,
        report_status_implication="This run is useful within scope but is not full-equivalent research.",
        limitations=["Synthetic validation proves contracts only."],
        evidence_mode="synthetic",
        research_completeness_note="synthetic_validation_only",
        target_profile=TargetProfile(),
        waivers=[],
    )


def _adapter(*, required_tables: list[str] | None = None, known_limits: list[str] | None = None) -> DomainAdapter:
    return DomainAdapter(
        topic="Adapter-aware runtime",
        reader="team leads",
        use_context="compare runtime trustworthiness",
        output_type="comparison memo",
        risk_tier="medium",
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="medium",
        source_priority=["government_context", "professional_body"],
        high_risk_claim_types=["absence"],
        likely_failure_modes=["Claim capture treated as support."],
        domain_specific_risks=["Scoped absence overstated as global absence."],
        common_misunderstandings=["Synthetic validation is not live completeness."],
        boundary_concepts=["claim capture vs support"],
        decision_context=DomainDecisionContext(
            primary_decision="compare bounded tradeoffs",
            failure_cost="moderate",
            time_horizon="near-term",
            reader_action="decide what to verify next",
        ),
        required_decision_layer=["What is safe to say", "What still needs stronger support"],
        required_tables=required_tables or ["Verification checklist"],
        must_not_overgeneralize=["Do not treat scoped absence as fact."],
        known_limits=known_limits or [],
        source_roles_required_by_claim_kind={"fact": ["government_context"], "absence": ["official_regulator"]},
    )


def _strategy() -> SourceStrategy:
    return SourceStrategy(
        source_priority=["government_context"],
        required_source_roles_by_claim_kind={"fact": ["government_context"], "absence": ["official_regulator"]},
        compatibility_notes={"absence": "Absence must remain scoped."},
    )


def _bundle_for_render():
    from cleanroom_runtime.models import MetricsSnapshot, PipelineBundle, ReleaseGateDecision

    request = _request()
    draft = ReportDraft(
        title=request.topic,
        sections=[ReportSectionPlan(key="findings", title="Key evidence-backed findings", purpose="")],
        units=[
            ReportUnit(
                unit_id="unit-001",
                section_key="findings",
                section_title="Key evidence-backed findings",
                text="Adapters reduce accidental scope drift.",
                claim_kind="fact",
                risk_level="medium",
                source_ids=["SRC-001"],
                source_roles=["government_context"],
                confidence=0.8,
            ),
            ReportUnit(
                unit_id="unit-002",
                section_key="findings",
                section_title="Key evidence-backed findings",
                text="Internal rollout timing is confirmed.",
                claim_kind="fact",
                risk_level="high",
                source_ids=["SRC-002"],
                source_roles=["trade_media"],
                confidence=0.4,
                include_in_report=False,
            ),
        ],
    )
    claims = [
        ClaimLedgerRow(
            claim_id="claim-001",
            unit_id="unit-001",
            report_section="Key evidence-backed findings",
            exact_text_span="Adapters reduce accidental scope drift.",
            normalized_claim="adapters reduce accidental scope drift.",
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
            included_in_report=True,
        ),
        ClaimLedgerRow(
            claim_id="claim-002",
            unit_id="unit-002",
            report_section="Key evidence-backed findings",
            exact_text_span="Internal rollout timing is confirmed.",
            normalized_claim="internal rollout timing is confirmed.",
            claim_kind="fact",
            risk_level="high",
            source_ids=["SRC-002"],
            source_roles=["trade_media"],
            evidence_count=1,
            required_source_roles=["official_regulator"],
            matched_source_roles=[],
            support_status="missing",
            confidence=0.4,
            caveat_required=True,
            suggested_tone="withhold",
            required_fix="Exclude from reader-facing prose.",
            included_in_report=False,
        ),
    ]
    return PipelineBundle(
        request=request,
        intent=_intent("comparison_report"),
        risk=RiskTierResult(risk_tier="medium", high_stakes_domains=[], rationale=""),
        budget=_budget(),
        strategy=_strategy(),
        adapter=_adapter(),
        evidence=CollectedEvidence(
            sources=[
                SourcePacket(source_id="SRC-001", title="Source 1", source_role="government_context"),
                SourcePacket(source_id="SRC-002", title="Source 2", source_role="trade_media"),
            ],
            findings=[],
            source_counts_by_role={"government_context": 1, "trade_media": 1},
            quality_notes=[],
        ),
        draft=draft,
        claims=claims,
        citations=[],
        contradictions=[],
        gaps=[],
        release_gate=ReleaseGateDecision(
            status="provisional",
            reasons=["Synthetic validation only."],
            blocking_reasons=[],
            unresolved_gaps=[],
            claim_issues=[],
            contract_complete=True,
            research_completeness="synthetic_validation_only",
        ),
        metrics=MetricsSnapshot(
            total_claim_count=2,
            included_claim_count=1,
            excluded_claim_count=1,
            included_supported_claim_count=1,
            included_scoped_absence_count=0,
            included_unsupported_claim_count=0,
            included_high_risk_claim_count=0,
            excluded_high_risk_claim_count=1,
            unresolved_high_risk_claim_count=1,
            high_risk_role_mismatch_count=1,
            unscoped_absence_count=0,
            contradiction_count=0,
            evidence_gap_count=0,
            distinct_source_count=2,
            distinct_source_role_count=2,
            duplicate_claim_count=0,
            audit_complete=True,
            citation_trace_complete=True,
            uncertainty_section_present=False,
            limitations_visible=False,
            target_results={"min_sources": False, "min_distinct_roles": True, "min_high_risk_sources": False},
            target_misses=["min_sources", "min_high_risk_sources"],
            target_miss_without_waiver=True,
            research_completeness="synthetic_validation_only",
        ),
    )


if __name__ == "__main__":
    unittest.main()
