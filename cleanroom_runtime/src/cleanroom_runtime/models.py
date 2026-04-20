from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import Any

from .catalogs import REPORT_SECTION_CATALOG
from .types import STAGE_SNAPSHOT_SCHEMA_VERSION, StageFailureCode


@dataclass(slots=True)
class ContractRecord:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_GROUNDING_TRACE_PREFIX = "trace::"


def encode_grounding_trace(
    *,
    grounding_marker: str = "",
    grounding_scope_note: str = "",
    span_labels: list[str] | None = None,
    span_starts: list[int] | None = None,
    span_ends: list[int] | None = None,
) -> str:
    payload = {
        "grounding_marker": grounding_marker,
        "grounding_scope_note": grounding_scope_note,
        "span_labels": list(span_labels or []),
        "span_starts": list(span_starts or []),
        "span_ends": list(span_ends or []),
    }
    if not any(payload.values()):
        return ""
    return _GROUNDING_TRACE_PREFIX + json.dumps(payload, separators=(",", ":"), ensure_ascii=True)


def decode_grounding_trace(note: str) -> dict[str, Any]:
    if not note.startswith(_GROUNDING_TRACE_PREFIX):
        return {}
    try:
        payload = json.loads(note[len(_GROUNDING_TRACE_PREFIX) :])
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


@dataclass(slots=True)
class AbsenceScope(ContractRecord):
    subject: str = ""
    scope_label: str = ""
    basis: str = ""
    checked_source_ids: list[str] = field(default_factory=list)
    checked_roles: list[str] = field(default_factory=list)
    scope_note: str = ""


@dataclass(slots=True)
class ReleaseContract(ContractRecord):
    allow_synthetic_complete: bool = False


@dataclass(slots=True)
class TargetProfile(ContractRecord):
    min_sources: int = 0
    min_distinct_roles: int = 0
    min_high_risk_sources: int = 0
    min_citations: int = 0
    min_report_claim_capture_ratio: float = 0.0


@dataclass(slots=True)
class SourcePacketProvenance(ContractRecord):
    packet_origin: str = "synthetic"
    adapter_name: str = ""
    canonical_url: str = ""
    canonical_id: str = ""
    dedupe_key: str = ""
    source_locator: str = ""
    original_url: str = ""
    content_digest: str = ""
    retrieval_scope: str = ""
    collected_at: str = ""
    retrieved_at: str = ""
    observed_at: str = ""
    normalized_at: str = ""
    trace_notes: list[str] = field(default_factory=list)
    metadata_consistent: bool = True
    citation_trace_complete: bool = True
    partial: bool = False
    partial_reason: str = ""
    metadata_fields_present: list[str] = field(default_factory=list)
    metadata_missing_fields: list[str] = field(default_factory=list)
    stale: bool = False
    stale_reason: str = ""
    malformed: bool = False
    malformed_reason: str = ""
    normalization_errors: list[str] = field(default_factory=list)
    dedupe_parent_ids: list[str] = field(default_factory=list)
    role_inference_status: str = "declared"
    role_inference_note: str = ""
    grounding_status: str = "grounded"
    grounding_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SourceFinding(ContractRecord):
    finding_id: str
    statement: str
    claim_kind: str
    risk_level: str
    section_hint: str = ""
    support_status_hint: str = "supported"
    confidence: float = 0.8
    source_ids: list[str] = field(default_factory=list)
    source_roles: list[str] = field(default_factory=list)
    decision_note: str = ""
    caveat: str = ""
    scope_note: str = ""
    contradiction_note: str = ""
    required_fix: str = ""
    jurisdiction: str = ""
    temporal_note: str = ""
    tags: list[str] = field(default_factory=list)
    absence_type: str = ""
    absence_scope: AbsenceScope | str | None = None
    source_excerpt: str = ""
    source_span_label: str = ""
    source_span_start: int | None = None
    source_span_end: int | None = None
    source_span_labels: list[str] = field(default_factory=list)
    source_span_starts: list[int] = field(default_factory=list)
    source_span_ends: list[int] = field(default_factory=list)
    grounding_kind: str = "summary"
    grounding_marker: str = ""
    grounding_scope_note: str = ""
    subject_key: str = ""
    subject_scope_key: str = ""
    source_trust_note: str = ""

    def __post_init__(self) -> None:
        if self.absence_type and (self.absence_scope is None or self.absence_scope == ""):
            self.absence_scope = AbsenceScope(basis=self.absence_type)
        elif isinstance(self.absence_scope, str) and self.absence_scope.strip():
            self.absence_scope = AbsenceScope(
                basis=self.absence_type,
                scope_label=self.absence_scope.strip(),
                scope_note=self.absence_scope.strip(),
            )
        trace_payload = decode_grounding_trace(self.source_trust_note)
        if trace_payload:
            if not self.grounding_marker:
                self.grounding_marker = str(trace_payload.get("grounding_marker", "")).strip()
            if not self.grounding_scope_note:
                self.grounding_scope_note = str(trace_payload.get("grounding_scope_note", "")).strip()
            if not self.source_span_labels:
                self.source_span_labels = [str(item) for item in trace_payload.get("span_labels", []) if str(item).strip()]
            if not self.source_span_starts:
                self.source_span_starts = [
                    int(item) for item in trace_payload.get("span_starts", []) if isinstance(item, int)
                ]
            if not self.source_span_ends:
                self.source_span_ends = [
                    int(item) for item in trace_payload.get("span_ends", []) if isinstance(item, int)
                ]
        if self.source_span_label and not self.source_span_labels:
            self.source_span_labels = [self.source_span_label]
        if self.source_span_start is not None and self.source_span_end is not None and not self.source_span_starts and not self.source_span_ends:
            self.source_span_starts = [self.source_span_start]
            self.source_span_ends = [self.source_span_end]
        if self.source_span_labels and not self.source_span_label:
            self.source_span_label = self.source_span_labels[0]
        if self.source_span_starts and self.source_span_start is None:
            self.source_span_start = self.source_span_starts[0]
        if self.source_span_ends and self.source_span_end is None:
            self.source_span_end = self.source_span_ends[-1]

    @property
    def risk_tags(self) -> list[str]:
        return self.tags

    @risk_tags.setter
    def risk_tags(self, value: list[str]) -> None:
        self.tags = value


Finding = SourceFinding
EvidenceRecord = SourceFinding


@dataclass(slots=True)
class SourcePacket(ContractRecord):
    source_id: str
    title: str
    source_role: str
    citation: str = ""
    url: str = ""
    publisher: str = ""
    published_on: str = ""
    jurisdiction: str = ""
    content_type: str = ""
    quality_flags: list[str] = field(default_factory=list)
    summary: str = ""
    findings: list[SourceFinding] = field(default_factory=list)
    provenance: SourcePacketProvenance = field(default_factory=SourcePacketProvenance)


SourceRecord = SourcePacket


@dataclass(slots=True)
class RawDocumentInput(ContractRecord):
    document_id: str
    title: str
    content: str
    content_type: str = "text/plain"
    source_role: str = "user_provided_source"
    jurisdiction: str = ""
    provided_at: str = ""
    excerpt_label: str = ""
    review_mode: str = "excerpt"


@dataclass(slots=True)
class RunRequest(ContractRecord):
    topic: str
    reader: str
    use_context: str
    desired_depth: str = ""
    jurisdiction: str = ""
    mode: str = "scoped"
    evidence_mode: str = "synthetic"
    as_of_date: str = ""
    output_type: str = "report"
    question: str = ""
    temporal_context: str = ""
    source_packets: list[SourcePacket] = field(default_factory=list)
    raw_documents: list[RawDocumentInput] = field(default_factory=list)
    target_profile: TargetProfile = field(default_factory=TargetProfile)
    waivers: list[str] = field(default_factory=list)
    release_contract: ReleaseContract = field(default_factory=ReleaseContract)
    requested_mode: str = ""
    provided_source_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.requested_mode:
            self.requested_mode = self.mode or "scoped"
        if not self.mode:
            self.mode = self.requested_mode or "scoped"
        if not self.desired_depth:
            self.desired_depth = self.requested_mode
        if not self.provided_source_ids and self.source_packets:
            self.provided_source_ids = [source.source_id for source in self.source_packets]


@dataclass(slots=True)
class IntentResult(ContractRecord):
    intent_label: str
    decision_focus: str
    reader_task: str
    report_shape_hints: list[str] = field(default_factory=list)
    rationale: str = ""

    @property
    def label(self) -> str:
        return self.intent_label


IntentClassification = IntentResult


@dataclass(slots=True)
class RiskTierResult(ContractRecord):
    risk_tier: str
    high_stakes_domains: list[str]
    rationale: str


RiskClassification = RiskTierResult


@dataclass(slots=True)
class BudgetPlan(ContractRecord):
    requested_mode: str
    effective_mode: str
    preset_baseline_budget: dict[str, int | float] = field(default_factory=dict)
    effective_budget: dict[str, int | float] = field(default_factory=dict)
    override_reason: str = ""
    override_authority: str = ""
    full_dr_equivalent: bool = False
    report_status_implication: str = ""
    limitations: list[str] = field(default_factory=list)
    evidence_mode: str = ""
    research_completeness_note: str = ""
    target_profile: TargetProfile = field(default_factory=TargetProfile)
    waivers: list[str] = field(default_factory=list)

    @property
    def preset_budget(self) -> dict[str, int | float]:
        return self.preset_baseline_budget

    @preset_budget.setter
    def preset_budget(self, value: dict[str, int | float]) -> None:
        self.preset_baseline_budget = value

    @property
    def full_research_equivalent(self) -> bool:
        return self.full_dr_equivalent

    @full_research_equivalent.setter
    def full_research_equivalent(self, value: bool) -> None:
        self.full_dr_equivalent = value


@dataclass(slots=True)
class SourceStrategy(ContractRecord):
    source_priority: list[str]
    required_source_roles_by_claim_kind: dict[str, list[str]]
    compatibility_notes: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class DomainDecisionContext(ContractRecord):
    primary_decision: str = ""
    failure_cost: str = "medium"
    time_horizon: str = ""
    reader_action: str = ""


@dataclass(slots=True)
class DomainAdapter(ContractRecord):
    topic: str = ""
    reader: str = ""
    use_context: str = ""
    output_type: str = "report"
    risk_tier: str = "medium"
    temporal_sensitivity: str = "medium"
    jurisdiction_sensitivity: str = "medium"
    source_priority: list[str] = field(default_factory=list)
    high_risk_claim_types: list[str] = field(default_factory=list)
    likely_failure_modes: list[str] = field(default_factory=list)
    domain_specific_risks: list[str] = field(default_factory=list)
    common_misunderstandings: list[str] = field(default_factory=list)
    boundary_concepts: list[str] = field(default_factory=list)
    decision_context: DomainDecisionContext = field(default_factory=DomainDecisionContext)
    required_decision_layer: list[str] = field(default_factory=list)
    required_tables: list[str] = field(default_factory=list)
    must_not_overgeneralize: list[str] = field(default_factory=list)
    known_limits: list[str] = field(default_factory=list)
    source_roles_required_by_claim_kind: dict[str, list[str]] = field(default_factory=dict)


@dataclass(slots=True)
class CollectedEvidence(ContractRecord):
    sources: list[SourcePacket] = field(default_factory=list)
    findings: list[SourceFinding] = field(default_factory=list)
    source_counts_by_role: dict[str, int] = field(default_factory=dict)
    quality_notes: list[str] = field(default_factory=list)

    @property
    def records(self) -> list[SourceFinding]:
        return self.findings


EvidenceCollection = CollectedEvidence


@dataclass(slots=True)
class ReportSectionPlan(ContractRecord):
    key: str
    title: str
    purpose: str = ""
    description: str = ""
    guardrails: list[str] = field(default_factory=list)
    max_units: int = 3

    def __post_init__(self) -> None:
        if not self.description and self.purpose:
            self.description = self.purpose
        if not self.purpose and self.description:
            self.purpose = self.description


@dataclass(slots=True)
class ReportUnit(ContractRecord):
    unit_id: str
    section_key: str
    section_title: str
    text: str
    claim_kind: str
    risk_level: str
    source_ids: list[str]
    source_roles: list[str]
    confidence: float
    finding_id: str = ""
    support_status_hint: str = "supported"
    caveat: str = ""
    required_fix: str = ""
    contradiction_note: str = ""
    jurisdiction: str = ""
    absence_type: str = ""
    absence_scope: AbsenceScope | str | None = None
    source_span_label: str = ""
    source_span_start: int | None = None
    source_span_end: int | None = None
    source_span_labels: list[str] = field(default_factory=list)
    source_span_starts: list[int] = field(default_factory=list)
    source_span_ends: list[int] = field(default_factory=list)
    grounding_marker: str = ""
    grounding_scope_note: str = ""
    subject_key: str = ""
    freshness_tag: str = ""
    is_claim: bool = True
    include_in_report: bool = True

    def __post_init__(self) -> None:
        if self.absence_type and (self.absence_scope is None or self.absence_scope == ""):
            self.absence_scope = AbsenceScope(basis=self.absence_type)
        elif isinstance(self.absence_scope, str) and self.absence_scope.strip():
            self.absence_scope = AbsenceScope(
                basis=self.absence_type,
                scope_label=self.absence_scope.strip(),
                scope_note=self.absence_scope.strip(),
            )
        if self.source_span_label and not self.source_span_labels:
            self.source_span_labels = [self.source_span_label]
        if (
            self.source_span_start is not None
            and self.source_span_end is not None
            and not self.source_span_starts
            and not self.source_span_ends
        ):
            self.source_span_starts = [self.source_span_start]
            self.source_span_ends = [self.source_span_end]
        if self.source_span_labels and not self.source_span_label:
            self.source_span_label = self.source_span_labels[0]
        if self.source_span_starts and self.source_span_start is None:
            self.source_span_start = self.source_span_starts[0]
        if self.source_span_ends and self.source_span_end is None:
            self.source_span_end = self.source_span_ends[-1]

    @property
    def support_status(self) -> str:
        return self.support_status_hint

    @support_status.setter
    def support_status(self, value: str) -> None:
        self.support_status_hint = value


@dataclass(slots=True)
class ReportDraft(ContractRecord):
    title: str
    sections: list[ReportSectionPlan]
    units: list[ReportUnit]
    markdown: str = ""


@dataclass(slots=True)
class ClaimLedgerRow(ContractRecord):
    claim_id: str
    report_section: str
    exact_text_span: str
    normalized_claim: str
    claim_kind: str
    risk_level: str
    source_ids: list[str]
    source_roles: list[str]
    evidence_count: int = 0
    required_source_roles: list[str] = field(default_factory=list)
    matched_source_roles: list[str] = field(default_factory=list)
    support_status: str = "supported"
    confidence: float = 0.0
    caveat_required: bool = False
    suggested_tone: str = "standard"
    required_fix: str = ""
    unit_id: str = ""
    origin_finding_ids: list[str] = field(default_factory=list)
    report_span_id: str = ""
    report_line_start: int = 0
    report_line_end: int = 0
    claim_span_start: int | None = None
    claim_span_end: int | None = None
    finding_span_labels: list[str] = field(default_factory=list)
    finding_span_starts: list[int] = field(default_factory=list)
    finding_span_ends: list[int] = field(default_factory=list)
    grounding_marker: str = ""
    grounding_scope_note: str = ""
    trace_status: str = "unmapped"
    included_in_report: bool = True
    absence_type: str = ""
    absence_scope: AbsenceScope | str | None = None
    subject_key: str = ""
    freshness_tag: str = ""
    contradiction_note: str = ""
    jurisdiction: str = ""
    blocking_reasons: list[str] = field(default_factory=list)
    exclusion_reasons: list[str] = field(default_factory=list)
    audit_display_state: str = "report_and_audit"
    required_source_role: list[str] = field(default_factory=list)
    exclusion_reason: str = ""
    report_section_key: str = ""

    def __post_init__(self) -> None:
        if self.required_source_role and not self.required_source_roles:
            self.required_source_roles = list(self.required_source_role)
        if self.required_source_roles and not self.required_source_role:
            self.required_source_role = list(self.required_source_roles)
        if self.absence_type and (self.absence_scope is None or self.absence_scope == ""):
            self.absence_scope = AbsenceScope(basis=self.absence_type)
        elif isinstance(self.absence_scope, str) and self.absence_scope.strip():
            self.absence_scope = AbsenceScope(
                basis=self.absence_type,
                scope_label=self.absence_scope.strip(),
                scope_note=self.absence_scope.strip(),
            )
        if self.exclusion_reason and not self.exclusion_reasons:
            self.exclusion_reasons = [self.exclusion_reason]
        if self.exclusion_reasons and not self.exclusion_reason:
            self.exclusion_reason = self.exclusion_reasons[0]
        if not self.report_section_key:
            self.report_section_key = self.report_section
        if not self.report_span_id and self.unit_id:
            self.report_span_id = self.unit_id
        if self.claim_span_start is None and self.exact_text_span:
            self.claim_span_start = 0
        if self.claim_span_end is None and self.exact_text_span:
            self.claim_span_end = len(self.exact_text_span)
        if not self.included_in_report and self.audit_display_state == "report_and_audit":
            self.audit_display_state = "audit_only"


ClaimRecord = ClaimLedgerRow


@dataclass(slots=True)
class ClaimAuditRow(ContractRecord):
    claim_id: str
    report_section: str
    claim_kind: str
    risk_level: str
    support_status: str
    included_in_report: bool
    audit_display_state: str = "report_and_audit"
    blocking_reasons: list[str] = field(default_factory=list)
    exclusion_reasons: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.included_in_report and self.audit_display_state == "report_and_audit":
            self.audit_display_state = "audit_only"


@dataclass(slots=True)
class CitationLedgerRow(ContractRecord):
    citation_id: str
    claim_id: str
    report_section: str
    source_id: str
    source_role: str
    source_title: str
    support_status: str
    included_in_report: bool = True
    report_span_id: str = ""
    claim_span_start: int | None = None
    claim_span_end: int | None = None
    source_finding_ids: list[str] = field(default_factory=list)
    source_excerpt: str = ""
    source_span_label: str = ""
    source_span_start: int | None = None
    source_span_end: int | None = None
    source_span_labels: list[str] = field(default_factory=list)
    source_span_starts: list[int] = field(default_factory=list)
    source_span_ends: list[int] = field(default_factory=list)
    grounding_marker: str = ""
    grounding_scope_note: str = ""
    trace_status: str = "unmapped"
    provenance_complete: bool = True

    def __post_init__(self) -> None:
        if self.source_span_label and not self.source_span_labels:
            self.source_span_labels = [self.source_span_label]
        if self.source_span_start is not None and self.source_span_end is not None and not self.source_span_starts and not self.source_span_ends:
            self.source_span_starts = [self.source_span_start]
            self.source_span_ends = [self.source_span_end]
        if self.source_span_labels and not self.source_span_label:
            self.source_span_label = self.source_span_labels[0]
        if self.source_span_starts and self.source_span_start is None:
            self.source_span_start = self.source_span_starts[0]
        if self.source_span_ends and self.source_span_end is None:
            self.source_span_end = self.source_span_ends[-1]


CitationRecord = CitationLedgerRow


@dataclass(slots=True)
class EvidenceLink(ContractRecord):
    link_id: str
    claim_id: str
    evidence_id: str
    source_id: str
    source_role: str
    relation: str = "supports"


@dataclass(slots=True)
class EvidenceMap(ContractRecord):
    links: list[EvidenceLink] = field(default_factory=list)
    citations: list[CitationLedgerRow] = field(default_factory=list)


@dataclass(slots=True)
class ContradictionEntry(ContractRecord):
    claim_id: str
    detail: str
    severity: str
    issue_id: str = ""
    source_ids: list[str] = field(default_factory=list)
    action: str = ""
    contradiction_class: str = ""
    subject_relation: str = ""
    severity_score: int = 0


ContradictionRecord = ContradictionEntry


@dataclass(slots=True)
class EvidenceGapEntry(ContractRecord):
    claim_id: str
    gap_type: str
    detail: str
    required_fix: str
    severity: str
    issue_id: str = ""
    blocking: bool = False
    release_impact: str = ""


EvidenceGapRecord = EvidenceGapEntry


@dataclass(slots=True)
class ReleaseIssue(ContractRecord):
    reason_id: str
    claim_id: str
    stage: str
    severity: str
    message: str
    required_fix: str
    blocks_release: bool


GateIssue = ReleaseIssue
ClaimIssue = ReleaseIssue


@dataclass(slots=True)
class AuditArtifacts(ContractRecord):
    contradictions: list[ContradictionEntry] = field(default_factory=list)
    gaps: list[EvidenceGapEntry] = field(default_factory=list)


@dataclass(slots=True)
class ReleaseGateDecision(ContractRecord):
    status: str
    reasons: list[str]
    blocking_reasons: list[str] = field(default_factory=list)
    unresolved_gaps: list[str] = field(default_factory=list)
    claim_issues: list[ReleaseIssue] = field(default_factory=list)
    contract_complete: bool = True
    research_completeness: str = ""
    metadata_consistent: bool = True
    release_semantics: str = ""


ReleaseDecision = ReleaseGateDecision


@dataclass(slots=True)
class StageContractFailure(ContractRecord):
    stage: str
    code: StageFailureCode
    message: str
    field: str = ""
    downstream_stage: str = ""


@dataclass(slots=True)
class StageSnapshot(ContractRecord):
    stage: str
    artifact_type: str
    required_fields: list[str] = field(default_factory=list)
    downstream_must_have_fields: dict[str, list[str]] = field(default_factory=dict)
    invariant_codes: list[StageFailureCode] = field(default_factory=list)
    contract_ok: bool = True
    failure_codes: list[StageFailureCode] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    snapshot_schema_version: str = STAGE_SNAPSHOT_SCHEMA_VERSION


@dataclass(slots=True)
class MetricsSnapshot(ContractRecord):
    total_claim_count: int = 0
    included_claim_count: int = 0
    excluded_claim_count: int = 0
    included_supported_claim_count: int = 0
    included_scoped_absence_count: int = 0
    included_unsupported_claim_count: int = 0
    included_high_risk_claim_count: int = 0
    excluded_high_risk_claim_count: int = 0
    unresolved_high_risk_claim_count: int = 0
    high_risk_role_mismatch_count: int = 0
    unscoped_absence_count: int = 0
    contradiction_count: int = 0
    evidence_gap_count: int = 0
    distinct_source_count: int = 0
    distinct_source_role_count: int = 0
    duplicate_claim_count: int = 0
    audit_complete: bool = False
    citation_trace_complete: bool = False
    traceability_complete: bool = True
    uncertainty_section_present: bool = False
    limitations_visible: bool = False
    direct_answer_present: bool = False
    scope_and_exclusions_present: bool = False
    checklist_present: bool = False
    next_action_or_next_research_present: bool = False
    internal_heading_present: bool = False
    tradeoff_table_present: bool = False
    finance_risk_disclosure_present: bool = False
    checklist_aligned_to_reader_task: bool = False
    specific_next_action_present: bool = False
    explicit_tradeoff_language_present: bool = False
    document_grounding_present: bool = False
    non_generic_uncertainty_present: bool = False
    metadata_inconsistency_count: int = 0
    citation_trace_mismatch_count: int = 0
    partial_packet_count: int = 0
    trace_mismatch_count: int = 0
    high_risk_traceability_mismatch_count: int = 0
    high_risk_missing_provenance_count: int = 0
    stale_current_tension_count: int = 0
    document_grounded_claim_count: int = 0
    ingestion_audit_visible: bool = False
    target_results: dict[str, bool] = field(default_factory=dict)
    target_misses: list[str] = field(default_factory=list)
    target_miss_without_waiver: bool = False
    research_completeness: str = ""
    reader_decision_layer_present: bool = True

    def get(self, key: str, default: Any = None) -> Any:
        if key == "metadata_consistent":
            return self.audit_complete and self.citation_trace_complete and self.traceability_complete
        if hasattr(self, key):
            return getattr(self, key)
        return default


@dataclass(slots=True)
class PipelineBundle(ContractRecord):
    request: RunRequest
    intent: IntentResult | None = None
    risk: RiskTierResult | None = None
    budget: BudgetPlan | None = None
    strategy: SourceStrategy | None = None
    adapter: DomainAdapter | None = None
    evidence: CollectedEvidence | None = None
    draft: ReportDraft | None = None
    claims: list[ClaimLedgerRow] = field(default_factory=list)
    citations: list[CitationLedgerRow] = field(default_factory=list)
    contradictions: list[ContradictionEntry] = field(default_factory=list)
    gaps: list[EvidenceGapEntry] = field(default_factory=list)
    release_gate: ReleaseGateDecision | None = None
    metrics: MetricsSnapshot | dict[str, Any] = field(default_factory=MetricsSnapshot)
    decision_usable: dict[str, Any] = field(default_factory=dict)
    stage_snapshots: list[StageSnapshot] | list[dict[str, Any]] = field(default_factory=list)
    report_plan: list[ReportSectionPlan] = field(default_factory=list)
    evidence_map: EvidenceMap | None = None
    audits: AuditArtifacts | None = None
    release: ReleaseGateDecision | None = None
    stage_failures: list[StageContractFailure] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.report_plan and self.draft is not None:
            self.report_plan = list(self.draft.sections)
        if isinstance(self.metrics, dict):
            self.metrics = MetricsSnapshot(**self.metrics)
        if self.release is None:
            self.release = self.release_gate
        if self.release_gate is None:
            self.release_gate = self.release
        if self.audits is None:
            self.audits = AuditArtifacts(contradictions=list(self.contradictions), gaps=list(self.gaps))
        if not self.contradictions:
            self.contradictions = list(self.audits.contradictions)
        if not self.gaps:
            self.gaps = list(self.audits.gaps)
        normalized_stage_snapshots: list[StageSnapshot] | list[dict[str, Any]] = []
        for snapshot in self.stage_snapshots:
            if isinstance(snapshot, StageSnapshot):
                normalized_stage_snapshots.append(snapshot)
            elif isinstance(snapshot, dict) and {"stage", "artifact_type"} <= set(snapshot):
                normalized_stage_snapshots.append(StageSnapshot(**snapshot))
            else:
                normalized_stage_snapshots.append(snapshot)
        self.stage_snapshots = normalized_stage_snapshots


ContractBundle = PipelineBundle


def default_report_plan() -> list[ReportSectionPlan]:
    return [
        ReportSectionPlan(key=key, title=title, description=description, purpose=description)
        for key, title, description in REPORT_SECTION_CATALOG
    ]
