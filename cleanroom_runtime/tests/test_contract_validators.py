from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.models import (  # noqa: E402
    CitationLedgerRow,
    ClaimLedgerRow,
    CollectedEvidence,
    BudgetPlan,
    DomainAdapter,
    DomainDecisionContext,
    MetricsSnapshot,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    RunRequest,
    SourcePacket,
)
from cleanroom_runtime.validators import (  # noqa: E402
    validate_budget_plan,
    validate_bundle_contracts,
    validate_domain_adapter,
    validate_metrics,
    validate_run_request,
)


class ContractValidatorTests(unittest.TestCase):
    def test_valid_contract_objects_pass_validation(self) -> None:
        draft = ReportDraft(
            title="Synthetic",
            sections=[ReportSectionPlan(key="findings", title="Findings", purpose="")],
            units=[
                ReportUnit(
                    unit_id="unit-001",
                    section_key="findings",
                    section_title="Findings",
                    text="Synthetic supported claim.",
                    claim_kind="fact",
                    risk_level="medium",
                    source_ids=["SRC-001"],
                    source_roles=["government_context"],
                    confidence=0.8,
                )
            ],
        )
        claims = [
            ClaimLedgerRow(
                claim_id="claim-001",
                unit_id="unit-001",
                report_section="Findings",
                exact_text_span="Synthetic supported claim.",
                normalized_claim="synthetic supported claim.",
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
        ]
        citations = [
            CitationLedgerRow(
                citation_id="citation-001",
                claim_id="claim-001",
                report_section="Findings",
                report_span_id="unit-001",
                source_id="SRC-001",
                source_role="government_context",
                source_title="Synthetic source",
                support_status="supported",
            )
        ]
        evidence = CollectedEvidence(
            sources=[SourcePacket(source_id="SRC-001", title="Synthetic source", source_role="government_context")],
            findings=[],
            source_counts_by_role={"government_context": 1},
            quality_notes=[],
        )
        adapter = DomainAdapter(
            topic="Synthetic",
            reader="reviewer",
            use_context="test validation",
            output_type="report",
            risk_tier="medium",
            temporal_sensitivity="medium",
            jurisdiction_sensitivity="medium",
            source_priority=["government_context"],
            high_risk_claim_types=["absence"],
            likely_failure_modes=["support drift"],
            domain_specific_risks=["claim/support confusion"],
            common_misunderstandings=["capture is not support"],
            boundary_concepts=["claim vs evidence"],
            decision_context=DomainDecisionContext(
                primary_decision="release or revise",
                failure_cost="moderate",
                time_horizon="near-term",
                reader_action="review support",
            ),
            required_decision_layer=["What is safe to say"],
            required_tables=["Verification checklist"],
            must_not_overgeneralize=["Do not overstate missing evidence."],
            known_limits=["Synthetic only."],
            source_roles_required_by_claim_kind={"fact": ["government_context"], "absence": ["official_regulator"]},
        )

        self.assertEqual(validate_domain_adapter(adapter), [])
        self.assertEqual(validate_bundle_contracts(draft, claims, citations, evidence), [])
        self.assertEqual(validate_metrics(_metrics()), [])

    def test_metrics_validator_rejects_inconsistent_counts(self) -> None:
        errors = validate_metrics(_metrics(total_claim_count=2, included_claim_count=1, excluded_claim_count=0))
        self.assertIn("included and excluded claim counts do not sum to total claims", errors)

    def test_budget_validator_rejects_scoped_full_equivalent_flag(self) -> None:
        plan = BudgetPlan(
            requested_mode="scoped",
            effective_mode="scoped",
            preset_baseline_budget={"min_sources": 3, "candidate_target": 18},
            effective_budget={"min_sources": 3, "candidate_target": 18},
            override_reason="No override.",
            override_authority="runtime_default",
            full_dr_equivalent=True,
            report_status_implication="Scoped run.",
        )
        errors = validate_budget_plan(plan)
        self.assertIn("budget.full_research_equivalent can only be true for effective_mode='full'", errors)


class FixtureIsolationTests(unittest.TestCase):
    def test_default_factories_are_isolated_between_instances(self) -> None:
        first = RunRequest(topic="First", reader="A", use_context="decision support", mode="scoped")
        second = RunRequest(topic="Second", reader="B", use_context="technical explainer", mode="scoped")

        first.waivers.append("waiver-one")
        first.target_profile.min_sources = 9
        first.source_packets.append(SourcePacket(source_id="SRC-900", title="Fixture", source_role="government_context"))

        self.assertEqual(second.waivers, [])
        self.assertEqual(second.target_profile.min_sources, 0)
        self.assertEqual(second.source_packets, [])

    def test_run_request_validation_accepts_cleanroom_shape(self) -> None:
        request = RunRequest(
            topic="Contracts",
            reader="Worker 1",
            use_context="validate contract completeness",
            mode="scoped",
            requested_mode="scoped",
            output_type="report",
        )
        self.assertEqual(validate_run_request(request), [])


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
        research_completeness="synthetic_validation_only",
    )
    values.update(overrides)
    return MetricsSnapshot(**values)


if __name__ == "__main__":
    unittest.main()
