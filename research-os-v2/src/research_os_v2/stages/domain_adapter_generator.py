from __future__ import annotations

from research_os_v2.catalogs import HIGH_RISK_CLAIM_KINDS
from research_os_v2.models import (
    BudgetPlan,
    CollectedEvidence,
    DomainAdapter,
    IntentClassification,
    ResearchRequest,
    RiskTierAssessment,
    SourceStrategy,
)
from research_os_v2.utils import uniq


def generate_domain_adapter(
    request: ResearchRequest,
    intent: IntentClassification,
    risk: RiskTierAssessment,
    budget: BudgetPlan,
    strategy: SourceStrategy,
    evidence: CollectedEvidence,
) -> DomainAdapter:
    domain_specific_risks = uniq(
        tag for finding in evidence.findings for tag in finding.risk_tags
    )
    likely_failure_modes = uniq(
        failure for finding in evidence.findings for failure in finding.failure_modes
    )
    misunderstandings = uniq(
        misunderstanding
        for finding in evidence.findings
        for misunderstanding in finding.misunderstandings
    )
    boundary_concepts = uniq(
        concept for finding in evidence.findings for concept in finding.boundary_concepts
    )
    claim_kinds = uniq(finding.claim_kind for finding in evidence.findings if finding.claim_kind in HIGH_RISK_CLAIM_KINDS)

    known_limits = list(budget.limitations)
    if not evidence.sources:
        known_limits.append("No evidence was provided, so the run cannot support factual release.")
    if any("outdated" in source.quality_flags for source in evidence.sources):
        known_limits.append("Some inputs are explicitly marked outdated.")
    if not boundary_concepts:
        boundary_concepts = ["Scope boundaries must be discovered during evidence review."]
    if not misunderstandings:
        misunderstandings = ["Readers may overgeneralize scoped findings into universal guidance."]
    if not domain_specific_risks:
        domain_specific_risks = ["Topic-specific risks still need to be discovered from better evidence."]

    return DomainAdapter(
        topic=request.topic,
        reader=request.reader,
        use_context=request.use_context,
        output_type=intent.label,
        risk_tier=risk.risk_tier,
        temporal_sensitivity=_temporal_sensitivity(request, evidence),
        jurisdiction_sensitivity="high" if request.jurisdiction or any(f.jurisdiction for f in evidence.findings) else "medium",
        source_priority=strategy.source_priority,
        high_risk_claim_types=claim_kinds or sorted(HIGH_RISK_CLAIM_KINDS),
        domain_specific_risks=domain_specific_risks,
        likely_failure_modes=likely_failure_modes or ["Failure modes still need deeper topic-specific discovery."],
        common_misunderstandings=misunderstandings,
        boundary_concepts=boundary_concepts,
        required_decision_layer=_decision_layer(intent.label),
        required_tables=_required_tables(intent.label),
        must_not_overgeneralize=_must_not_overgeneralize(evidence),
        known_limits=known_limits,
    )


def _temporal_sensitivity(request: ResearchRequest, evidence: CollectedEvidence) -> str:
    if request.temporal_context:
        return "high"
    if any(finding.claim_kind == "temporal" for finding in evidence.findings):
        return "high"
    return "medium"


def _decision_layer(intent_label: str) -> list[str]:
    mapping = {
        "comparison": ["Fit conditions", "Tradeoffs", "Best next check"],
        "decision memo": ["Decision criteria", "Conditions to proceed", "Escalation point"],
        "technical explainer": ["What to understand", "What changes outcomes", "What to verify before implementation"],
        "legal overview": ["Binding text", "Interpretation boundary", "Local counsel or regulator check"],
        "product guide": ["Selection criteria", "Operational burden", "Evidence gaps before purchase"],
        "literature review": ["Consensus level", "Where evidence diverges", "What remains uncertain"],
        "strategy memo": ["Priority choices", "Scenario triggers", "Recommended next move"],
    }
    return mapping.get(intent_label, ["Direct answer", "What the reader should decide", "What to verify next"])


def _required_tables(intent_label: str) -> list[str]:
    tables = ["Checklist or decision table"]
    if intent_label in {"comparison", "product guide", "decision memo"}:
        tables.insert(0, "Options or comparison table")
    else:
        tables.insert(0, "Evidence-backed findings table")
    return tables


def _must_not_overgeneralize(evidence: CollectedEvidence) -> list[str]:
    items = []
    if any(source.source_role == "vendor_first_party" for source in evidence.sources):
        items.append("Vendor claims should not be generalized into universal market facts.")
    if any(source.jurisdiction for source in evidence.sources):
        items.append("Jurisdiction-specific findings should not be treated as globally applicable.")
    if any(finding.claim_kind == "absence" for finding in evidence.findings):
        items.append("Absence findings should not be rewritten as settled facts.")
    if not items:
        items.append("Scoped evidence should not be overstated beyond the sampled sources.")
    return items
