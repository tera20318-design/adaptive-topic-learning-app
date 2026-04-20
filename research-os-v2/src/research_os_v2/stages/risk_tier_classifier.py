from __future__ import annotations

from research_os_v2.catalogs import HIGH_STAKES_DOMAINS
from research_os_v2.models import ResearchRequest, RiskTierAssessment
from research_os_v2.utils import uniq


KEYWORD_TO_DOMAIN = {
    "legal": ["legal", "contractual", "liability", "law", "法", "訴訟"],
    "regulatory": ["regulatory", "compliance", "regulation", "規制", "compliance"],
    "medical": ["medical", "clinical", "patient", "health", "drug", "医療", "健康"],
    "financial": ["financial", "investment", "portfolio", "pricing", "loan", "金融", "投資"],
    "safety": ["safety", "hazard", "injury", "fire", "exposure", "安全", "危険"],
    "procurement": ["procurement", "vendor selection", "rfp", "purchase", "調達"],
    "technical_failure": ["failure", "reliability", "quality escape", "outage", "故障", "信頼性"],
}


def classify_risk_tier(request: ResearchRequest) -> RiskTierAssessment:
    haystack = " ".join(
        [request.topic, request.use_context, request.question, request.output_type]
    ).lower()

    domains = uniq(
        domain
        for domain, keywords in KEYWORD_TO_DOMAIN.items()
        if any(keyword in haystack for keyword in keywords)
    )

    finding_claim_kinds = {finding.claim_kind for source in request.source_packets for finding in source.findings}
    if {"legal", "medical", "financial", "regulatory"} & finding_claim_kinds:
        domains.extend(kind for kind in finding_claim_kinds if kind in HIGH_STAKES_DOMAINS)
        domains = uniq(domains)

    if any(domain in HIGH_STAKES_DOMAINS for domain in domains):
        return RiskTierAssessment(
            risk_tier="high",
            high_stakes_domains=domains,
            rationale="Detected high-stakes keywords or claim kinds that require stricter evidence handling.",
        )

    if "comparison" in request.output_type.lower() or any(finding.risk_level == "high" for source in request.source_packets for finding in source.findings):
        return RiskTierAssessment(
            risk_tier="medium",
            high_stakes_domains=domains,
            rationale="No hard high-stakes domain dominated the request, but the topic still has decision-relevant risk.",
        )

    return RiskTierAssessment(
        risk_tier="low",
        high_stakes_domains=domains,
        rationale="The request appears informational and not dominated by high-stakes failure modes.",
    )
