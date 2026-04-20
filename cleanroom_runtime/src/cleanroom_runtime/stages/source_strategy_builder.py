from __future__ import annotations

from cleanroom_runtime.models import DomainAdapter, IntentResult, RiskTierResult, SourceStrategy


def build_source_strategy(intent: IntentResult, risk: RiskTierResult, adapter: DomainAdapter) -> SourceStrategy:
    compatibility_notes = {
        "high_risk": "High-risk claims must satisfy claim-kind source-role requirements.",
        "absence": "Absence claims must keep typed scope and must not be rewritten as facts.",
        "research_status": "Synthetic or scoped runs cannot claim live research completeness.",
    }
    if "comparison" in intent.intent_label:
        compatibility_notes["comparison"] = "Comparisons should prefer like-for-like source roles when available."
    if risk.risk_tier == "low":
        compatibility_notes["low_risk"] = "Low-risk claims may still be weak if supported only by discovery sources."
    return SourceStrategy(
        source_priority=list(adapter.source_priority),
        required_source_roles_by_claim_kind={key: list(value) for key, value in adapter.source_roles_required_by_claim_kind.items()},
        compatibility_notes=compatibility_notes,
    )
