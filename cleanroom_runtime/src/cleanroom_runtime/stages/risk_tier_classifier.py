from __future__ import annotations

from cleanroom_runtime.models import IntentResult, RiskTierResult, RunRequest
from cleanroom_runtime.utils import normalize_text


HIGH_STAKES_TOKENS = {
    "legal": ("law", "legal", "regulation", "regulatory", "compliance", "court"),
    "medical": ("medical", "health", "clinical", "treatment", "diagnosis"),
    "financial": ("financial", "finance", "investment", "banking", "securities"),
}

MEDIUM_STAKES_TOKENS = ("policy", "procurement", "contract", "safety", "security")


def classify_risk_tier(request: RunRequest, intent: IntentResult) -> RiskTierResult:
    haystack = normalize_text(" ".join([request.topic, request.use_context, request.reader, intent.intent_label]))
    high_stakes_domains = [domain for domain, tokens in HIGH_STAKES_TOKENS.items() if any(token in haystack for token in tokens)]
    if high_stakes_domains:
        return RiskTierResult(
            risk_tier="high",
            high_stakes_domains=high_stakes_domains,
            rationale="The request touches a high-stakes domain that needs stricter source-role matching.",
        )
    if any(token in haystack for token in MEDIUM_STAKES_TOKENS):
        return RiskTierResult(
            risk_tier="medium",
            high_stakes_domains=[],
            rationale="The request looks decision-relevant even if it is not clearly high stakes.",
        )
    return RiskTierResult(
        risk_tier="low",
        high_stakes_domains=[],
        rationale="No clear high-stakes signal was detected in the request metadata.",
    )
