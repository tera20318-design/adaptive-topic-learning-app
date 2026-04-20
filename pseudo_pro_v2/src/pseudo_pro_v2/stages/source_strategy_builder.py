from __future__ import annotations

from pseudo_pro_v2.models import DomainAdapter, IntentResult, RiskTierResult, SourceStrategy


def build_source_strategy(intent: IntentResult, risk: RiskTierResult, adapter: DomainAdapter) -> SourceStrategy:
    compatibility_notes = {
        claim_kind: f"{claim_kind} claims prefer: {', '.join(roles)}."
        for claim_kind, roles in adapter.source_roles_required_by_claim_kind.items()
    }
    return SourceStrategy(
        source_priority=adapter.source_priority,
        required_source_roles_by_claim_kind=adapter.source_roles_required_by_claim_kind,
        compatibility_notes=compatibility_notes,
    )
