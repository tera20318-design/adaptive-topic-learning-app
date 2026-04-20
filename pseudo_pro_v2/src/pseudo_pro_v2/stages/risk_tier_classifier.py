from __future__ import annotations

from pseudo_pro_v2.models import IntentResult, RiskTierResult, RunRequest


HIGH_RISK_KEYWORDS = {
    "legal": "legal",
    "regulatory": "regulatory",
    "medical": "medical",
    "financial": "financial",
    "safety": "safety",
    "procurement": "procurement",
    "compliance": "regulatory",
}


def classify_risk_tier(request: RunRequest, intent: IntentResult) -> RiskTierResult:
    text = " ".join([request.topic, request.use_context, intent.intent_label]).lower()
    domains = sorted({domain for token, domain in HIGH_RISK_KEYWORDS.items() if token in text})
    if domains:
        return RiskTierResult(
            risk_tier="high",
            high_stakes_domains=domains,
            rationale="The request touches at least one high-stakes domain class.",
        )
    if intent.intent_label in {"comparison", "decision memo", "technical explainer", "legal overview"}:
        return RiskTierResult(
            risk_tier="medium",
            high_stakes_domains=[],
            rationale="The request appears decision-relevant but not dominated by explicit high-stakes signals.",
        )
    return RiskTierResult(
        risk_tier="low",
        high_stakes_domains=[],
        rationale="The request appears informational and low-stakes.",
    )
