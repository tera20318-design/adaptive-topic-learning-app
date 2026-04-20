from __future__ import annotations

from cleanroom_runtime.catalogs import DEFAULT_SOURCE_ROLE_REQUIREMENTS, HIGH_RISK_CLAIM_KINDS
from cleanroom_runtime.models import (
    BudgetPlan,
    DomainAdapter,
    DomainDecisionContext,
    IntentResult,
    RiskTierResult,
    RunRequest,
)
from cleanroom_runtime.utils import normalize_text


def generate_domain_adapter(
    request: RunRequest,
    intent: IntentResult,
    risk: RiskTierResult,
    budget: BudgetPlan,
) -> DomainAdapter:
    haystack = normalize_text(" ".join([request.topic, request.use_context, request.desired_depth]))
    temporal_sensitivity = "high" if any(token in haystack for token in ("current", "latest", "today", "recent", "timeline")) else "medium"
    jurisdiction_sensitivity = "high" if request.jurisdiction else "medium"
    source_priority = _source_priority_for_risk(risk.risk_tier)
    required_tables = ["Verification checklist"]
    if "options" in intent.report_shape_hints or "comparison" in intent.intent_label:
        required_tables.append("Options or comparison table")
    if intent.intent_label == "document_review":
        required_tables.append("Document grounding checklist")

    likely_failure_modes = [
        "Claim support inferred from generic authority instead of claim-kind requirements.",
        "Scoped absence rewritten as a settled fact.",
        "Repeated findings used to make the bundle look richer than the evidence is.",
    ]
    domain_specific_risks = [
        "The answer may need different source roles for different claim kinds.",
        "The reader may act on scoped research as if it were exhaustive.",
    ]
    if risk.risk_tier == "high":
        domain_specific_risks.append("High-risk claims need role-matched support rather than general credibility.")
    if intent.intent_label == "document_review":
        domain_specific_risks.append("Single-document grounding can be mistaken for external authority.")

    return DomainAdapter(
        topic=request.topic,
        reader=request.reader,
        use_context=request.use_context,
        output_type=request.output_type or "report",
        risk_tier=risk.risk_tier,
        temporal_sensitivity=temporal_sensitivity,
        jurisdiction_sensitivity=jurisdiction_sensitivity,
        source_priority=source_priority,
        high_risk_claim_types=sorted(HIGH_RISK_CLAIM_KINDS if risk.risk_tier == "high" else {"absence"}),
        likely_failure_modes=likely_failure_modes,
        domain_specific_risks=domain_specific_risks,
        common_misunderstandings=[
            "Claim capture is not the same thing as claim support.",
            "Scoped absence does not prove global absence.",
            "Synthetic validation does not imply live research completeness.",
        ],
        boundary_concepts=[
            "evidence vs inference",
            "scoped absence vs settled fact",
            "contract completeness vs research completeness",
        ],
        decision_context=DomainDecisionContext(
            primary_decision=intent.decision_focus,
            failure_cost="high" if risk.risk_tier == "high" else "moderate" if risk.risk_tier == "medium" else "low",
            time_horizon="near-term",
            reader_action=request.use_context or intent.reader_task,
        ),
        required_decision_layer=_required_decision_layer(intent),
        required_tables=required_tables,
        must_not_overgeneralize=[
            "Do not treat missing evidence in checked scope as universal absence.",
            "Do not convert synthetic evidence into live-completeness claims.",
            *(
                ["Do not treat a checked document as law, policy, or general proof beyond its own text."]
                if intent.intent_label == "document_review"
                else []
            ),
        ],
        known_limits=list(budget.limitations),
        source_roles_required_by_claim_kind={key: list(value) for key, value in DEFAULT_SOURCE_ROLE_REQUIREMENTS.items()},
    )


def _source_priority_for_risk(risk_tier: str) -> list[str]:
    if risk_tier == "high":
        return [
            "official_regulator",
            "legal_text",
            "court_or_authoritative_interpretation",
            "academic_review",
            "professional_body",
            "government_context",
        ]
    if risk_tier == "medium":
        return ["professional_body", "government_context", "academic_review", "standards_body", "industry_association"]
    return ["government_context", "professional_body", "academic_review", "industry_association", "trade_media"]


def _required_decision_layer(intent: IntentResult) -> list[str]:
    if intent.intent_label == "document_review":
        return [
            "What the checked document states directly",
            "What still needs external verification",
            "What must not be inferred beyond the document text",
        ]
    return [
        "What is currently safe to say",
        "What still needs stronger support",
        "What should not be treated as complete research",
    ]
