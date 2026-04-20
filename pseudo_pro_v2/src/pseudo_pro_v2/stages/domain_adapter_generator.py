from __future__ import annotations

from pseudo_pro_v2.catalogs import HIGH_RISK_CLAIM_KINDS, REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND, SOURCE_ROLES
from pseudo_pro_v2.models import BudgetPlan, DomainAdapter, DomainDecisionContext, IntentResult, RiskTierResult, RunRequest


def generate_domain_adapter(
    request: RunRequest,
    intent: IntentResult,
    risk: RiskTierResult,
    budget: BudgetPlan,
) -> DomainAdapter:
    source_priority = _source_priority(risk.risk_tier)
    high_risk_claim_types = sorted(HIGH_RISK_CLAIM_KINDS) if risk.risk_tier == "high" else ["absence"]
    required_tables = ["Checklist or decision table"]
    if intent.intent_label in {"comparison", "decision memo"}:
        required_tables.insert(0, "Options or comparison table")
    else:
        required_tables.insert(0, "Evidence-backed findings table")
    required_decision_layer = _required_decision_layer(intent.intent_label)

    return DomainAdapter(
        topic=request.topic,
        reader=request.reader,
        use_context=request.use_context,
        output_type=intent.intent_label,
        risk_tier=risk.risk_tier,
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="high" if request.jurisdiction else "medium",
        source_priority=source_priority,
        high_risk_claim_types=high_risk_claim_types,
        likely_failure_modes=[
            f"Overgeneralizing evidence about {request.topic}.",
            "Confusing scoped findings with universal conclusions.",
        ],
        domain_specific_risks=[
            f"Missing decision-critical constraints for {request.topic}.",
            f"Treating an overview of {request.topic} as if it settled implementation or compliance detail.",
        ],
        common_misunderstandings=[
            "A scoped run is equivalent to a full investigation.",
            "A captured claim is necessarily a supported claim.",
        ],
        boundary_concepts=[
            "fact vs inference",
            "scope vs universal claim",
            "captured vs supported",
        ],
        decision_context=DomainDecisionContext(
            primary_decision="What the reader should decide or verify next.",
            failure_cost=risk.risk_tier,
            time_horizon="Immediate next-step decision support.",
            reader_action="Use the report to decide what needs deeper confirmation before action.",
        ),
        required_decision_layer=required_decision_layer,
        required_tables=required_tables,
        must_not_overgeneralize=[
            "Scoped evidence should not be presented as universal coverage.",
            "Weak or role-mismatched sources should not carry high-risk conclusions.",
        ],
        known_limits=list(budget.limitations),
        source_roles_required_by_claim_kind={key: list(value) for key, value in REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND.items()},
    )


def _source_priority(risk_tier: str) -> list[str]:
    if risk_tier == "high":
        return [
            "official_regulator",
            "legal_text",
            "court_or_authoritative_interpretation",
            "standards_body",
            "standard_or_code",
            "academic_review",
            "academic_paper",
            "professional_body",
            "government_context",
            "industry_association",
            "vendor_first_party",
            "trade_media",
            "secondary_media",
            "user_provided_source",
            "unknown",
        ]
    return list(SOURCE_ROLES)


def _required_decision_layer(intent_label: str) -> list[str]:
    if intent_label == "user document review":
        return [
            "What the provided document states directly",
            "What still needs external verification",
            "What cannot be inferred from the document alone",
        ]
    if intent_label == "market/business analysis":
        return [
            "What appears stable versus volatile",
            "What assumption most changes the decision",
            "What decision should wait for fresher evidence",
        ]
    return [
        "What is already safe to say",
        "What still needs verification",
        "What decision should wait for stronger evidence",
    ]
