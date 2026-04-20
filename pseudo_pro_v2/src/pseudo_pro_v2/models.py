from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceFinding:
    finding_id: str
    statement: str
    claim_kind: str
    risk_level: str
    section_hint: str
    decision_note: str = ""
    support_status_hint: str = "not_checked"
    confidence: float = 0.8
    source_ids: list[str] = field(default_factory=list)
    source_roles: list[str] = field(default_factory=list)
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


@dataclass
class SourcePacket:
    source_id: str
    title: str
    source_role: str
    citation: str = ""
    summary: str = ""
    quality_flags: list[str] = field(default_factory=list)
    findings: list[SourceFinding] = field(default_factory=list)
    jurisdiction: str = ""
    published_on: str = ""


@dataclass
class TargetProfile:
    min_sources: int = 0
    min_citations: int = 0
    min_report_claim_capture_ratio: float = 0.0


@dataclass
class ReleaseContract:
    allow_synthetic_complete: bool = False


@dataclass
class RunRequest:
    topic: str
    reader: str
    use_context: str
    desired_depth: str
    jurisdiction: str
    mode: str
    evidence_mode: str = "synthetic"
    source_packets: list[SourcePacket] = field(default_factory=list)
    target_profile: TargetProfile = field(default_factory=TargetProfile)
    release_contract: ReleaseContract = field(default_factory=ReleaseContract)
    waivers: list[str] = field(default_factory=list)


@dataclass
class IntentResult:
    intent_label: str
    decision_focus: str
    reader_task: str
    report_shape_hints: list[str]


@dataclass
class RiskTierResult:
    risk_tier: str
    high_stakes_domains: list[str]
    rationale: str


@dataclass
class BudgetPlan:
    requested_mode: str
    effective_mode: str
    preset_baseline_budget: dict[str, Any]
    effective_budget: dict[str, Any]
    override_reason: str
    override_authority: str
    full_dr_equivalent: bool
    report_status_implication: str
    limitations: list[str]
    target_profile: TargetProfile
    waivers: list[str] = field(default_factory=list)


@dataclass
class SourceStrategy:
    source_priority: list[str]
    required_source_roles_by_claim_kind: dict[str, list[str]]
    compatibility_notes: dict[str, str]


@dataclass
class DomainDecisionContext:
    primary_decision: str
    failure_cost: str
    time_horizon: str
    reader_action: str


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
    likely_failure_modes: list[str]
    domain_specific_risks: list[str]
    common_misunderstandings: list[str]
    boundary_concepts: list[str]
    decision_context: DomainDecisionContext
    required_decision_layer: list[str]
    required_tables: list[str]
    must_not_overgeneralize: list[str]
    known_limits: list[str]
    source_roles_required_by_claim_kind: dict[str, list[str]]


@dataclass
class CollectedEvidence:
    sources: list[SourcePacket]
    findings: list[SourceFinding]
    source_counts_by_role: dict[str, int]
    quality_notes: list[str]


@dataclass
class ReportSectionPlan:
    key: str
    title: str
    description: str
    target_claim_count: int = 0
    adapter_prompts: list[str] = field(default_factory=list)
    required: bool = True


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
    support_status_hint: str = "not_checked"
    absence_type: str = ""
    contradiction_note: str = ""
    caveat: str = ""
    required_fix: str = ""
    jurisdiction: str = ""
    origin_finding_id: str = ""
    is_claim: bool = True
    include_in_report: bool = True
    exclusion_reason: str = ""


@dataclass
class ReportDraft:
    title: str
    sections: list[ReportSectionPlan]
    units: list[ReportUnit]


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
    required_role_matched: bool
    role_fit_status: str
    support_status: str
    confidence: float
    caveat_required: bool
    suggested_tone: str
    required_fix: str
    origin_finding_id: str = ""
    absence_type: str = ""
    contradiction_note: str = ""
    included_in_report: bool = True
    exclusion_reason: str = ""


@dataclass
class CitationLedgerRow:
    citation_id: str
    claim_id: str
    report_section: str
    source_id: str
    source_role: str
    source_title: str
    support_status: str
    included_in_report: bool = True
    origin_finding_id: str = ""


@dataclass
class ContradictionEntry:
    claim_id: str
    detail: str
    severity: str


@dataclass
class EvidenceGapEntry:
    claim_id: str
    gap_type: str
    detail: str
    required_fix: str
    severity: str


@dataclass
class ReleaseGateDecision:
    status: str
    reasons: list[str]
    blocking_reasons: list[str]
    unresolved_gaps: list[str]
    metadata_consistent: bool


@dataclass
class PipelineBundle:
    request: RunRequest
    intent: IntentResult
    risk: RiskTierResult
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
