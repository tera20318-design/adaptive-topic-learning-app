from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.gates import evaluate_decision_usable  # noqa: E402
from pseudo_pro_v2.models import ClaimLedgerRow, DomainAdapter, DomainDecisionContext, ReportDraft, ReportSectionPlan, ReportUnit  # noqa: E402


class DecisionUsableRubricTests(unittest.TestCase):
    def test_rubric_passes_with_complete_reader_facing_structure(self) -> None:
        rubric = evaluate_decision_usable(_draft(), _claims(), _adapter())
        self.assertTrue(rubric.passed)

    def test_rubric_fails_when_next_action_is_missing(self) -> None:
        draft = _draft(
            decision_text="Reader-facing summary only.",
            checklist_text="Summary row only.",
            uncertainty_text="Limitations remain unresolved.",
            decision_claim_kind="fact",
        )
        rubric = evaluate_decision_usable(draft, _claims(decision_claim_kind="fact"), _adapter())
        self.assertIn("next action or next research missing", rubric.failures)

    def test_rubric_fails_when_internal_heading_is_present(self) -> None:
        draft = _draft(direct_title="Claim audit")
        rubric = evaluate_decision_usable(draft, _claims(), _adapter())
        self.assertIn("internal headings present", rubric.failures)

    def test_rubric_fails_when_unsupported_high_risk_claim_remains_in_mainline(self) -> None:
        claims = _claims()
        claims[0] = ClaimLedgerRow(
            **{
                **claims[0].__dict__,
                "risk_level": "high",
                "claim_kind": "medical",
                "support_status": "weak",
                "required_role_matched": False,
                "role_fit_status": "authoritative_mismatch",
            }
        )
        rubric = evaluate_decision_usable(_draft(), claims, _adapter())
        self.assertIn("unsupported high-risk claim remains in mainline prose", rubric.failures)

    def test_rubric_fails_when_comparison_structure_is_underpopulated(self) -> None:
        rubric = evaluate_decision_usable(_draft(include_second_option=False), _claims(include_second_option=False), _adapter())
        self.assertIn("comparison tradeoff structure is insufficient", rubric.failures)


def _draft(
    *,
    direct_title: str = "Direct answer",
    decision_text: str = "Verify the decision-critical condition before acting.",
    include_second_option: bool = True,
    checklist_text: str = "Check: verify scope, support, and uncertainty labels before action.",
    uncertainty_text: str = "Next research should confirm the unresolved condition before action.",
    decision_claim_kind: str = "advice",
) -> ReportDraft:
    sections = [
        ReportSectionPlan(key="direct_answer", title=direct_title, description=""),
        ReportSectionPlan(key="scope", title="Scope and exclusions", description=""),
        ReportSectionPlan(key="options", title="Main options/categories/mechanisms", description=""),
        ReportSectionPlan(key="risks", title="Risks and failure modes", description=""),
        ReportSectionPlan(key="decision_layer", title="Reader decision layer", description=""),
        ReportSectionPlan(key="checklist", title="Checklist or decision table", description=""),
        ReportSectionPlan(key="uncertainty", title="Uncertainty and next research", description=""),
    ]
    units = [
        ReportUnit(
            unit_id="unit-001",
            section_key="direct_answer",
            section_title=direct_title,
            text="Use a scope-bounded answer rather than a universal default.",
            claim_kind="fact",
            risk_level="medium",
            source_ids=["SRC-001"],
            source_roles=["professional_body"],
            confidence=0.9,
        ),
        ReportUnit(
            unit_id="unit-002",
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
            unit_id="unit-003",
            section_key="options",
            section_title="Main options/categories/mechanisms",
            text="Option A emphasizes a narrower setup path.",
            claim_kind="comparison",
            risk_level="medium",
            source_ids=["SRC-001"],
            source_roles=["professional_body"],
            confidence=0.9,
        ),
        ReportUnit(
            unit_id="unit-004",
            section_key="risks",
            section_title="Risks and failure modes",
            text="A one-size default can fail when decision constraints differ.",
            claim_kind="fact",
            risk_level="medium",
            source_ids=["SRC-001"],
            source_roles=["professional_body"],
            confidence=0.9,
        ),
        ReportUnit(
            unit_id="unit-005",
            section_key="decision_layer",
            section_title="Reader decision layer",
            text=decision_text,
            claim_kind=decision_claim_kind,
            risk_level="medium",
            source_ids=["SRC-001"],
            source_roles=["professional_body"],
            confidence=0.9,
        ),
        ReportUnit(
            unit_id="unit-006",
            section_key="checklist",
            section_title="Checklist or decision table",
            text=checklist_text,
            claim_kind="scope_boundary",
            risk_level="low",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            is_claim=False,
        ),
        ReportUnit(
            unit_id="unit-007",
            section_key="uncertainty",
            section_title="Uncertainty and next research",
            text=uncertainty_text,
            claim_kind="scope_boundary",
            risk_level="low",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            is_claim=False,
        ),
    ]
    if include_second_option:
        units.append(
            ReportUnit(
                unit_id="unit-008",
                section_key="options",
                section_title="Main options/categories/mechanisms",
                text="Option B keeps more flexibility but adds verification work.",
                claim_kind="comparison",
                risk_level="medium",
                source_ids=["SRC-001"],
                source_roles=["professional_body"],
                confidence=0.88,
            )
        )
    return ReportDraft(title="synthetic_anchor", sections=sections, units=units)


def _claims(*, include_second_option: bool = True, decision_claim_kind: str = "advice") -> list[ClaimLedgerRow]:
    claims = [
        _claim("claim-001", "Direct answer", "fact", "medium", "Use a scope-bounded answer rather than a universal default."),
        _claim("claim-003", "Main options/categories/mechanisms", "comparison", "medium", "Option A emphasizes a narrower setup path."),
        _claim("claim-004", "Risks and failure modes", "fact", "medium", "A one-size default can fail when decision constraints differ."),
        _claim("claim-005", "Reader decision layer", decision_claim_kind, "medium", "Verify the decision-critical condition before acting."),
    ]
    if include_second_option:
        claims.append(
            _claim(
                "claim-008",
                "Main options/categories/mechanisms",
                "comparison",
                "medium",
                "Option B keeps more flexibility but adds verification work.",
            )
        )
    return claims


def _claim(claim_id: str, report_section: str, claim_kind: str, risk_level: str, exact_text_span: str) -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id=claim_id,
        report_section=report_section,
        exact_text_span=exact_text_span,
        normalized_claim=exact_text_span.lower(),
        claim_kind=claim_kind,
        risk_level=risk_level,
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
        origin_finding_id=f"F-{claim_id}",
        included_in_report=True,
        exclusion_reason="",
    )


def _adapter() -> DomainAdapter:
    return DomainAdapter(
        topic="synthetic_anchor",
        reader="Synthetic reader",
        use_context="Synthetic use context",
        output_type="comparison",
        risk_tier="medium",
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="medium",
        source_priority=["professional_body"],
        high_risk_claim_types=["absence"],
        likely_failure_modes=["Scope drift."],
        domain_specific_risks=["Missing decision-critical constraint."],
        common_misunderstandings=["Captured does not mean supported."],
        boundary_concepts=["fact vs inference"],
        decision_context=DomainDecisionContext(
            primary_decision="Choose the next step.",
            failure_cost="medium",
            time_horizon="Immediate",
            reader_action="Verify before action.",
        ),
        required_decision_layer=["What is already safe to say", "What still needs verification"],
        required_tables=["Options or comparison table", "Checklist or decision table"],
        must_not_overgeneralize=["Scoped evidence is not universal evidence."],
        known_limits=["This run is scoped."],
        source_roles_required_by_claim_kind={"comparison": ["professional_body"], "advice": ["professional_body"], "fact": ["professional_body"]},
    )


if __name__ == "__main__":
    unittest.main()
