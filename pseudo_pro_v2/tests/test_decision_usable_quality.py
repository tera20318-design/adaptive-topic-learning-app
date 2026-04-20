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


class DecisionUsableQualityTests(unittest.TestCase):
    def test_checklist_alignment_with_reader_task_is_required(self) -> None:
        rubric = evaluate_decision_usable(_draft(checklist_text="Check: generic summary row."), _claims(), _adapter())
        self.assertIn("checklist items do not align with the reader task", rubric.failures)

    def test_specific_next_action_is_required(self) -> None:
        rubric = evaluate_decision_usable(
            _draft(
                decision_text="Consider context.",
                uncertainty_text="Limitations remain.",
                checklist_text="Check: context.",
                decision_claim_kind="fact",
            ),
            _claims(decision_claim_kind="fact"),
            _adapter(),
        )
        self.assertIn("next action is not specific enough", rubric.failures)

    def test_comparison_outputs_require_tradeoff_language(self) -> None:
        rubric = evaluate_decision_usable(
            _draft(option_a="Option A reduces setup effort.", option_b="Option B increases flexibility."),
            _claims(),
            _adapter(),
        )
        self.assertIn("comparison tradeoff structure is insufficient", rubric.failures)

    def test_recommendation_requires_visible_risk_disclosure(self) -> None:
        claims = _claims(decision_risk_level="high")
        rubric = evaluate_decision_usable(
            _draft(risks_text="Operational detail only.", uncertainty_text="General note only."),
            claims,
            _adapter(),
        )
        self.assertIn("risk disclosure is insufficient for high-risk recommendations", rubric.failures)

    def test_decision_layer_must_not_be_generic_filler(self) -> None:
        rubric = evaluate_decision_usable(_draft(decision_text="Reader-facing summary only."), _claims(), _adapter())
        self.assertIn("decision layer is generic filler", rubric.failures)


def _draft(
    *,
    checklist_text: str = "Check: verify quoted passages and role-matched support before action.",
    decision_text: str = "Verify quoted passages and role-matched support before action.",
    uncertainty_text: str = "Next research should verify the unresolved grounding condition before action.",
    risks_text: str = "Risk disclosure: acting before verification can overgeneralize a scoped packet.",
    option_a: str = "Option A reduces setup effort but adds more fixed structure.",
    option_b: str = "Option B preserves flexibility but increases verification work.",
    decision_claim_kind: str = "advice",
) -> ReportDraft:
    sections = [
        ReportSectionPlan(key="direct_answer", title="Direct answer", description=""),
        ReportSectionPlan(key="scope", title="Scope and exclusions", description=""),
        ReportSectionPlan(key="options", title="Main options/categories/mechanisms", description=""),
        ReportSectionPlan(key="risks", title="Risks and failure modes", description=""),
        ReportSectionPlan(key="decision_layer", title="Reader decision layer", description=""),
        ReportSectionPlan(key="checklist", title="Checklist or decision table", description=""),
        ReportSectionPlan(key="uncertainty", title="Uncertainty and next research", description=""),
    ]
    units = [
        ReportUnit("unit-001", "direct_answer", "Direct answer", "Use a document-bounded decision rather than a universal default.", "fact", "medium", ["SRC-001"], ["professional_body"], 0.9),
        ReportUnit("unit-002", "scope", "Scope and exclusions", "This run is scoped and excludes unresolved external applicability.", "scope_boundary", "low", [], [], 0.9, is_claim=False),
        ReportUnit("unit-003", "options", "Main options/categories/mechanisms", option_a, "comparison", "medium", ["SRC-001"], ["professional_body"], 0.9),
        ReportUnit("unit-004", "options", "Main options/categories/mechanisms", option_b, "comparison", "medium", ["SRC-001"], ["professional_body"], 0.88),
        ReportUnit("unit-005", "risks", "Risks and failure modes", risks_text, "fact", "medium", ["SRC-001"], ["professional_body"], 0.86),
        ReportUnit("unit-006", "decision_layer", "Reader decision layer", decision_text, decision_claim_kind, "high", ["SRC-001"], ["professional_body"], 0.9),
        ReportUnit("unit-007", "checklist", "Checklist or decision table", checklist_text, "scope_boundary", "low", [], [], 0.9, is_claim=False),
        ReportUnit("unit-008", "uncertainty", "Uncertainty and next research", uncertainty_text, "scope_boundary", "low", [], [], 0.9, is_claim=False),
    ]
    return ReportDraft(title="synthetic_anchor", sections=sections, units=units)


def _claims(*, decision_claim_kind: str = "advice", decision_risk_level: str = "high") -> list[ClaimLedgerRow]:
    return [
        _claim("claim-001", "Direct answer", "fact", "medium", "Use a document-bounded decision rather than a universal default."),
        _claim("claim-003", "Main options/categories/mechanisms", "comparison", "medium", "Option A reduces setup effort but adds more fixed structure."),
        _claim("claim-004", "Main options/categories/mechanisms", "comparison", "medium", "Option B preserves flexibility but increases verification work."),
        _claim("claim-005", "Risks and failure modes", "fact", "medium", "Risk disclosure: acting before verification can overgeneralize a scoped packet."),
        _claim("claim-006", "Reader decision layer", decision_claim_kind, decision_risk_level, "Verify quoted passages and role-matched support before action."),
    ]


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
        use_context="prepare a document-bounded decision review",
        output_type="comparison",
        risk_tier="high",
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="medium",
        source_priority=["professional_body"],
        high_risk_claim_types=["advice", "absence"],
        likely_failure_modes=["Scope drift."],
        domain_specific_risks=["Missing grounding."],
        common_misunderstandings=["Captured does not mean supported."],
        boundary_concepts=["fact vs inference"],
        decision_context=DomainDecisionContext(
            primary_decision="Choose the next step.",
            failure_cost="high",
            time_horizon="Immediate",
            reader_action="Verify quoted passages and role-matched support before action.",
        ),
        required_decision_layer=[
            "What the document states directly",
            "What still needs external verification",
            "What cannot be inferred from the document alone",
        ],
        required_tables=["Options or comparison table", "Checklist or decision table"],
        must_not_overgeneralize=["Scoped evidence is not universal evidence."],
        known_limits=["This run is scoped."],
        source_roles_required_by_claim_kind={"comparison": ["professional_body"], "advice": ["professional_body"], "fact": ["professional_body"]},
    )


if __name__ == "__main__":
    unittest.main()
