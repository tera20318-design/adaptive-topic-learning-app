from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Finding:
    finding_id: str
    statement: str
    claim_kind: str
    risk_level: str
    section_hint: str
    decision_note: str = ""
    support_status_hint: str = "supported"
    confidence: float = 0.8
    source_ids: list[str] = field(default_factory=list)
    risk_tags: list[str] = field(default_factory=list)
    failure_modes: list[str] = field(default_factory=list)
    misunderstandings: list[str] = field(default_factory=list)
    boundary_concepts: list[str] = field(default_factory=list)
    caveat: str = ""
    absence_type: str = ""
    contradiction_note: str = ""
    required_fix: str = ""
    jurisdiction: str = ""
    temporal_note: str = ""
    scope_note: str = ""


@dataclass
class SourcePacket:
    source_id: str
    title: str
    source_role: str
    citation: str = ""
    url: str = ""
    publisher: str = ""
    published_on: str = ""
    jurisdiction: str = ""
    quality_flags: list[str] = field(default_factory=list)
    summary: str = ""
    findings: list[Finding] = field(default_factory=list)


@dataclass
class ResearchRequest:
    topic: str
    reader: str
    use_context: str
    requested_mode: str
    output_type: str = ""
    question: str = ""
    jurisdiction: str = ""
    temporal_context: str = ""
    as_of_date: str = ""
    provided_document_name: str = ""
    source_packets: list[SourcePacket] = field(default_factory=list)


@dataclass
class IntentClassification:
    label: str
    rationale: str
    decision_focus: str


@dataclass
class RiskTierAssessment:
    risk_tier: str
    high_stakes_domains: list[str]
    rationale: str


@dataclass
class BudgetPlan:
    requested_mode: str
    effective_mode: str
    preset_baseline_budget: dict[str, int]
    effective_budget: dict[str, int]
    override_reason: str
    override_authority: str
    full_dr_equivalent: bool
    report_status_implication: str
    limitations: list[str]


@dataclass
class SourceStrategy:
    source_priority: list[str]
    required_source_roles: dict[str, list[str]]
    compatibility_notes: dict[str, str]


@dataclass
class DomainAdapter:
    topic: str
    reader: str
    use_context: str
    output_type: str
    risk_tier: str
    temporal_sensitivity: str
    jurisdiction_sensitivity: str
    source_priority: list[str]
    high_risk_claim_types: list[str]
    domain_specific_risks: list[str]
    likely_failure_modes: list[str]
    common_misunderstandings: list[str]
    boundary_concepts: list[str]
    required_decision_layer: list[str]
    required_tables: list[str]
    must_not_overgeneralize: list[str]
    known_limits: list[str]


@dataclass
class CollectedEvidence:
    sources: list[SourcePacket]
    findings: list[Finding]
    source_counts_by_role: dict[str, int]
    source_quality_notes: list[str]


@dataclass
class ReportSectionPlan:
    key: str
    title: str
    description: str


@dataclass
class ReportUnit:
    unit_id: str
    section_key: str
    section_title: str
    text: str
    claim_kind: str
    risk_level: str
    source_ids: list[str]
    source_roles: list[str]
    confidence: float
    support_status_hint: str = "supported"
    absence_type: str = ""
    jurisdiction: str = ""
    contradiction_note: str = ""
    caveat: str = ""
    required_fix: str = ""
    is_claim: bool = True


@dataclass
class ReportDraft:
    title: str
    sections: list[ReportSectionPlan]
    units: list[ReportUnit]
    markdown: str = ""


@dataclass
class ClaimLedgerRow:
    claim_id: str
    report_section: str
    exact_text_span: str
    normalized_claim: str
    claim_kind: str
    risk_level: str
    source_ids: list[str]
    source_roles: list[str]
    evidence_count: int
    required_source_role: list[str]
    support_status: str
    confidence: float
    caveat_required: bool
    suggested_tone: str
    required_fix: str


@dataclass
class CitationLedgerRow:
    citation_id: str
    claim_id: str
    report_section: str
    source_id: str
    source_role: str
    source_title: str
    support_status: str


@dataclass
class ContradictionEntry:
    claim_id: str
    issue_type: str
    severity: str
    detail: str
    action: str


@dataclass
class EvidenceGapEntry:
    claim_id: str
    gap_type: str
    detail: str
    release_impact: str
    required_fix: str


@dataclass
class ReleaseGateDecision:
    status: str
    reasons: list[str]
    blocking_reasons: list[str]
    unresolved_gaps: list[str]
    metadata_consistent: bool


@dataclass
class PipelineBundle:
    request: ResearchRequest
    intent: IntentClassification
    risk: RiskTierAssessment
    budget: BudgetPlan
    strategy: SourceStrategy
    adapter: DomainAdapter
    evidence: CollectedEvidence
    draft: ReportDraft
    claims: list[ClaimLedgerRow]
    citations: list[CitationLedgerRow]
    contradictions: list[ContradictionEntry]
    gaps: list[EvidenceGapEntry]
    release_gate: ReleaseGateDecision
    metrics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
