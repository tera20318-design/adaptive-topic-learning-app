from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable, Sequence

from .catalogs import (
    ABSENCE_TYPES,
    AUDIT_SEVERITIES,
    CLAIM_KINDS,
    EVIDENCE_LINK_RELATIONS,
    HIGH_RISK_CLAIM_KINDS,
    INTENT_LABELS,
    MODE_BASELINES,
    RELEASE_STATUSES,
    RISK_LEVELS,
    SOURCE_ROLES,
    SUPPORT_STATUSES,
)
from .models import (
    AuditArtifacts,
    BudgetPlan,
    CitationLedgerRow,
    ClaimLedgerRow,
    CollectedEvidence,
    ContradictionEntry,
    DomainAdapter,
    EvidenceGapEntry,
    EvidenceMap,
    EvidenceLink,
    Finding,
    IntentResult,
    MetricsSnapshot,
    PipelineBundle,
    RawDocumentInput,
    ReleaseGateDecision,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    RiskTierResult,
    RunRequest,
    SourcePacket,
    SourcePacketProvenance,
    SourceStrategy,
    TargetProfile,
)


def validate_target_profile(profile: TargetProfile) -> list[str]:
    errors: list[str] = []
    if profile.min_sources < 0:
        errors.append("target_profile.min_sources must be zero or greater")
    if profile.min_distinct_roles < 0:
        errors.append("target_profile.min_distinct_roles must be zero or greater")
    if profile.min_high_risk_sources < 0:
        errors.append("target_profile.min_high_risk_sources must be zero or greater")
    if profile.min_citations < 0:
        errors.append("target_profile.min_citations must be zero or greater")
    if not 0 <= profile.min_report_claim_capture_ratio <= 1:
        errors.append("target_profile.min_report_claim_capture_ratio must be between 0 and 1")
    return errors


def validate_run_request(request: RunRequest) -> list[str]:
    errors: list[str] = []
    _require_text("request.topic", request.topic, errors)
    _require_text("request.reader", request.reader, errors)
    _require_text("request.use_context", request.use_context, errors)
    _require_choice("request.requested_mode", request.requested_mode, MODE_BASELINES.keys(), errors)
    _require_choice("request.output_type", request.output_type, INTENT_LABELS, errors)
    _validate_unique_strings("request.waivers", request.waivers, errors)
    _validate_unique_strings(
        "request.provided_source_ids",
        request.provided_source_ids or [source.source_id for source in request.source_packets],
        errors,
    )
    document_ids = [document.document_id for document in request.raw_documents]
    _validate_unique_strings("request.raw_documents.document_id", document_ids, errors)
    for document in request.raw_documents:
        errors.extend(validate_raw_document_input(document))
    errors.extend(validate_target_profile(request.target_profile))
    return errors


def validate_raw_document_input(document: RawDocumentInput) -> list[str]:
    errors: list[str] = []
    _require_text("document.document_id", document.document_id, errors)
    _require_text("document.title", document.title, errors)
    _require_text("document.content", document.content, errors)
    if document.source_role:
        _require_choice("document.source_role", document.source_role, SOURCE_ROLES, errors)
    if document.review_mode:
        _require_choice("document.review_mode", document.review_mode, ("excerpt", "document_review"), errors)
    return errors


def validate_intent_classification(intent: IntentResult) -> list[str]:
    errors: list[str] = []
    _require_choice("intent.intent_label", intent.intent_label, INTENT_LABELS, errors)
    _require_text("intent.decision_focus", intent.decision_focus, errors)
    _require_text("intent.reader_task", intent.reader_task, errors)
    _validate_unique_strings("intent.report_shape_hints", intent.report_shape_hints, errors)
    return errors


def validate_risk_classification(risk: RiskTierResult) -> list[str]:
    errors: list[str] = []
    _require_choice("risk.risk_tier", risk.risk_tier, RISK_LEVELS, errors)
    _require_text("risk.rationale", risk.rationale, errors)
    _validate_unique_strings("risk.high_stakes_domains", risk.high_stakes_domains, errors)
    return errors


def validate_budget_plan(budget: BudgetPlan) -> list[str]:
    errors: list[str] = []
    _require_choice("budget.requested_mode", budget.requested_mode, MODE_BASELINES.keys(), errors)
    _require_choice("budget.effective_mode", budget.effective_mode, MODE_BASELINES.keys(), errors)
    errors.extend(_validate_budget_shape("budget.preset_baseline_budget", budget.preset_baseline_budget))
    errors.extend(_validate_budget_shape("budget.effective_budget", budget.effective_budget))
    errors.extend(validate_target_profile(budget.target_profile))
    _validate_unique_strings("budget.limitations", budget.limitations, errors)
    _validate_unique_strings("budget.waivers", budget.waivers, errors)
    _require_text("budget.report_status_implication", budget.report_status_implication, errors)
    if budget.effective_mode != budget.requested_mode:
        _require_text("budget.override_reason", budget.override_reason, errors)
        _require_text("budget.override_authority", budget.override_authority, errors)
    if budget.full_dr_equivalent and budget.effective_mode != "full":
        errors.append("budget.full_research_equivalent can only be true for effective_mode='full'")
    return errors


def validate_domain_adapter(adapter: DomainAdapter) -> list[str]:
    errors: list[str] = []
    if adapter.topic and not adapter.topic.strip():
        errors.append("domain adapter missing topic")
    if adapter.reader and not adapter.reader.strip():
        errors.append("domain adapter missing reader")
    if adapter.use_context and not adapter.use_context.strip():
        errors.append("domain adapter missing use context")
    if adapter.output_type:
        _require_choice("adapter.output_type", adapter.output_type, INTENT_LABELS, errors)
    if adapter.risk_tier:
        _require_choice("adapter.risk_tier", adapter.risk_tier, RISK_LEVELS, errors)
    if adapter.temporal_sensitivity:
        _require_choice("adapter.temporal_sensitivity", adapter.temporal_sensitivity, RISK_LEVELS, errors)
    if adapter.jurisdiction_sensitivity:
        _require_choice("adapter.jurisdiction_sensitivity", adapter.jurisdiction_sensitivity, RISK_LEVELS, errors)
    _validate_choice_list("adapter.source_priority", adapter.source_priority, SOURCE_ROLES, errors)
    _validate_choice_list("adapter.high_risk_claim_types", adapter.high_risk_claim_types, CLAIM_KINDS, errors)
    unexpected = sorted(set(adapter.high_risk_claim_types) - HIGH_RISK_CLAIM_KINDS)
    if unexpected:
        errors.append(
            "adapter.high_risk_claim_types contains non-high-risk claim kinds: " + ", ".join(unexpected)
        )
    _validate_unique_strings("adapter.required_decision_layer", adapter.required_decision_layer, errors)
    _validate_unique_strings("adapter.required_tables", adapter.required_tables, errors)
    _validate_unique_strings("adapter.known_limits", adapter.known_limits, errors)
    _validate_unique_strings("adapter.must_not_overgeneralize", adapter.must_not_overgeneralize, errors)
    if adapter.decision_context.primary_decision:
        _require_text("adapter.decision_context.primary_decision", adapter.decision_context.primary_decision, errors)
    if adapter.decision_context.failure_cost:
        _require_choice(
            "adapter.decision_context.failure_cost",
            adapter.decision_context.failure_cost,
            ("low", "medium", "moderate", "high"),
            errors,
        )
    if adapter.decision_context.time_horizon:
        _require_text("adapter.decision_context.time_horizon", adapter.decision_context.time_horizon, errors)
    if adapter.decision_context.reader_action:
        _require_text("adapter.decision_context.reader_action", adapter.decision_context.reader_action, errors)
    for claim_kind, roles in adapter.source_roles_required_by_claim_kind.items():
        if claim_kind not in CLAIM_KINDS:
            errors.append(f"domain adapter uses unknown claim kind `{claim_kind}`")
        _validate_choice_list(f"adapter.source_roles_required_by_claim_kind['{claim_kind}']", roles, SOURCE_ROLES, errors, min_items=1)
    return errors


def validate_source_strategy(strategy: SourceStrategy) -> list[str]:
    errors: list[str] = []
    _validate_choice_list("strategy.source_priority", strategy.source_priority, SOURCE_ROLES, errors, min_items=1)
    for claim_kind, roles in strategy.required_source_roles_by_claim_kind.items():
        if claim_kind not in CLAIM_KINDS:
            errors.append(f"strategy.required_source_roles_by_claim_kind has unknown claim kind '{claim_kind}'")
        _validate_choice_list(
            f"strategy.required_source_roles_by_claim_kind['{claim_kind}']",
            roles,
            SOURCE_ROLES,
            errors,
            min_items=1,
        )
    for claim_kind, note in strategy.compatibility_notes.items():
        if not note.strip():
            errors.append(f"strategy.compatibility_notes['{claim_kind}'] must be non-empty")
    return errors


def validate_source_record(source: SourcePacket) -> list[str]:
    errors: list[str] = []
    _require_text("source.source_id", source.source_id, errors)
    _require_text("source.title", source.title, errors)
    _require_choice("source.source_role", source.source_role, SOURCE_ROLES, errors)
    _validate_unique_strings("source.quality_flags", source.quality_flags, errors)
    errors.extend(validate_source_provenance(source.provenance))
    return errors


def validate_source_provenance(provenance: SourcePacketProvenance) -> list[str]:
    errors: list[str] = []
    if provenance.packet_origin and not provenance.packet_origin.strip():
        errors.append("source.provenance.packet_origin must be non-empty when provided")
    _validate_unique_strings("source.provenance.trace_notes", provenance.trace_notes, errors)
    _validate_unique_strings("source.provenance.grounding_notes", provenance.grounding_notes, errors)
    _validate_unique_strings("source.provenance.metadata_fields_present", provenance.metadata_fields_present, errors)
    _validate_unique_strings("source.provenance.metadata_missing_fields", provenance.metadata_missing_fields, errors)
    _validate_unique_strings("source.provenance.normalization_errors", provenance.normalization_errors, errors)
    _validate_unique_strings("source.provenance.dedupe_parent_ids", provenance.dedupe_parent_ids, errors)
    if provenance.partial and not provenance.partial_reason.strip():
        errors.append("source.provenance.partial_reason must be populated when provenance.partial is true")
    if provenance.stale and not provenance.stale_reason.strip():
        errors.append("source.provenance.stale_reason must be populated when provenance.stale is true")
    if provenance.malformed and not provenance.malformed_reason.strip():
        errors.append("source.provenance.malformed_reason must be populated when provenance.malformed is true")
    if provenance.grounding_status and provenance.grounding_status not in {"grounded", "partial", "ambiguous"}:
        errors.append("source.provenance.grounding_status must be one of grounded, partial, ambiguous")
    if provenance.role_inference_status and provenance.role_inference_status not in {"declared", "inferred", "ambiguous"}:
        errors.append("source.provenance.role_inference_status must be one of declared, inferred, ambiguous")
    if not isinstance(provenance.metadata_consistent, bool):
        errors.append("source.provenance.metadata_consistent must be boolean")
    if not isinstance(provenance.citation_trace_complete, bool):
        errors.append("source.provenance.citation_trace_complete must be boolean")
    overlap = set(provenance.metadata_fields_present) & set(provenance.metadata_missing_fields)
    if overlap:
        errors.append(
            "source.provenance.metadata_fields_present and metadata_missing_fields must not overlap: "
            + ", ".join(sorted(overlap))
        )
    return errors


def validate_finding(record: Finding) -> list[str]:
    errors: list[str] = []
    _require_text("finding.finding_id", record.finding_id, errors)
    _require_text("finding.statement", record.statement, errors)
    if record.section_hint:
        _require_text("finding.section_hint", record.section_hint, errors)
    _require_choice("finding.claim_kind", record.claim_kind, CLAIM_KINDS, errors)
    _require_choice("finding.risk_level", record.risk_level, RISK_LEVELS, errors)
    _require_choice("finding.support_status_hint", record.support_status_hint, SUPPORT_STATUSES, errors)
    _validate_unique_strings("finding.source_ids", record.source_ids, errors)
    _validate_choice_list("finding.source_roles", record.source_roles, SOURCE_ROLES, errors)
    _validate_unique_strings("finding.tags", record.tags, errors)
    _require_ratio("finding.confidence", record.confidence, errors)
    if record.grounding_kind not in {"summary", "direct_quote", "paraphrase"}:
        errors.append("finding.grounding_kind must be one of summary, direct_quote, paraphrase")
    if record.grounding_kind in {"direct_quote", "paraphrase"} and not record.source_excerpt.strip():
        errors.append("finding.source_excerpt must be populated for direct_quote or paraphrase grounding")
    if (record.source_span_start is None) ^ (record.source_span_end is None):
        errors.append("finding.source_span_start and source_span_end must both be populated or both be omitted")
    if record.source_span_start is not None and record.source_span_end is not None and record.source_span_end < record.source_span_start:
        errors.append("finding.source_span_end must be greater than or equal to source_span_start")
    if record.source_span_labels and len(record.source_span_labels) != len(set(record.source_span_labels)):
        errors.append("finding.source_span_labels must not contain duplicates")
    if record.source_span_starts and len(record.source_span_starts) != len(record.source_span_ends):
        errors.append("finding.source_span_starts and source_span_ends must have the same length")
    if record.source_span_labels and record.source_span_starts and len(record.source_span_labels) != len(record.source_span_starts):
        errors.append("finding.source_span_labels must align with source_span_starts/source_span_ends")
    if any(
        end < start
        for start, end in zip(record.source_span_starts, record.source_span_ends, strict=False)
    ):
        errors.append("finding.source_span_ends must be greater than or equal to source_span_starts")
    if record.grounding_kind in {"direct_quote", "paraphrase"} and not (
        (record.source_span_start is not None and record.source_span_end is not None) or record.source_span_starts
    ):
        errors.append("finding direct grounding requires at least one inspectable span")
    if record.support_status_hint == "supported" and not record.source_ids:
        errors.append("finding.source_ids must be populated when support_status_hint='supported'")
    if record.absence_type:
        _require_choice("finding.absence_type", record.absence_type, ABSENCE_TYPES, errors)
    if record.claim_kind != "absence" and record.absence_type:
        errors.append("finding.absence_type is only valid when claim_kind='absence'")
    return errors


def validate_evidence_collection(evidence: CollectedEvidence) -> list[str]:
    errors: list[str] = []
    source_ids = [source.source_id for source in evidence.sources]
    if len(source_ids) != len(set(source_ids)):
        errors.append("evidence.sources contains duplicate source_id values")
    for source in evidence.sources:
        errors.extend(validate_source_record(source))
    for finding in evidence.findings:
        errors.extend(validate_finding(finding))
        missing_sources = sorted(set(finding.source_ids) - set(source_ids))
        if missing_sources:
            errors.append(
                f"finding {finding.finding_id} references unknown source_ids: " + ", ".join(missing_sources)
            )
    actual_counts = Counter(source.source_role for source in evidence.sources)
    for role, count in evidence.source_counts_by_role.items():
        if role not in SOURCE_ROLES:
            errors.append(f"evidence.source_counts_by_role has unknown source role '{role}'")
        elif not isinstance(count, int) or count < 0:
            errors.append(f"evidence.source_counts_by_role['{role}'] must be a non-negative integer")
    if evidence.source_counts_by_role and dict(actual_counts) != evidence.source_counts_by_role:
        errors.append("evidence.source_counts_by_role must match the actual source role counts")
    _validate_unique_strings("evidence.quality_notes", evidence.quality_notes, errors)
    return errors


def validate_report_plan(sections: Sequence[ReportSectionPlan]) -> list[str]:
    errors: list[str] = []
    if not sections:
        errors.append("report plan must contain at least one section")
        return errors
    seen_keys: set[str] = set()
    for section in sections:
        _require_text("section.key", section.key, errors)
        _require_text("section.title", section.title, errors)
        if not (section.description or section.purpose).strip():
            errors.append(f"section {section.key} must describe its purpose")
        if section.key in seen_keys:
            errors.append(f"report plan contains duplicate section key '{section.key}'")
        seen_keys.add(section.key)
    return errors


def validate_report_draft(draft: ReportDraft) -> list[str]:
    errors: list[str] = []
    _require_text("draft.title", draft.title, errors)
    errors.extend(validate_report_plan(draft.sections))
    section_title_by_key = {section.key: section.title for section in draft.sections}
    unit_ids = [unit.unit_id for unit in draft.units]
    if len(unit_ids) != len(set(unit_ids)):
        errors.append("draft.units contains duplicate unit_id values")
    for unit in draft.units:
        errors.extend(validate_report_unit(unit, section_title_by_key))
    return errors


def validate_report_unit(unit: ReportUnit, section_title_by_key: dict[str, str]) -> list[str]:
    errors: list[str] = []
    _require_text("unit.unit_id", unit.unit_id, errors)
    _require_text("unit.section_key", unit.section_key, errors)
    _require_text("unit.section_title", unit.section_title, errors)
    _require_text("unit.text", unit.text, errors)
    _require_choice("unit.claim_kind", unit.claim_kind, CLAIM_KINDS, errors)
    _require_choice("unit.risk_level", unit.risk_level, RISK_LEVELS, errors)
    _require_choice("unit.support_status_hint", unit.support_status_hint, SUPPORT_STATUSES, errors)
    _validate_unique_strings("unit.source_ids", unit.source_ids, errors)
    _validate_choice_list("unit.source_roles", unit.source_roles, SOURCE_ROLES, errors)
    _require_ratio("unit.confidence", unit.confidence, errors)
    if unit.section_key not in section_title_by_key:
        errors.append(f"unit {unit.unit_id} references unknown section_key '{unit.section_key}'")
    elif section_title_by_key[unit.section_key] != unit.section_title:
        errors.append(f"unit {unit.unit_id} section_title does not match report plan for '{unit.section_key}'")
    if unit.include_in_report and unit.is_claim and unit.support_status_hint == "supported" and not unit.source_ids:
        errors.append(f"unit {unit.unit_id} needs source_ids when included supported claim text is present")
    if unit.absence_type:
        _require_choice("unit.absence_type", unit.absence_type, ABSENCE_TYPES, errors)
    if unit.claim_kind != "absence" and unit.absence_type:
        errors.append(f"unit {unit.unit_id} has absence_type but claim_kind is not 'absence'")
    return errors


def validate_claim_records(claims: Sequence[ClaimLedgerRow]) -> list[str]:
    errors: list[str] = []
    claim_ids = [claim.claim_id for claim in claims]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("claims contain duplicate claim_id values")
    for claim in claims:
        _require_text("claim.claim_id", claim.claim_id, errors)
        _require_text("claim.report_section", claim.report_section, errors)
        _require_text("claim.exact_text_span", claim.exact_text_span, errors)
        _require_text("claim.normalized_claim", claim.normalized_claim, errors)
        _require_choice("claim.claim_kind", claim.claim_kind, CLAIM_KINDS, errors)
        _require_choice("claim.risk_level", claim.risk_level, RISK_LEVELS, errors)
        _require_choice("claim.support_status", claim.support_status, SUPPORT_STATUSES, errors)
        _validate_unique_strings("claim.source_ids", claim.source_ids, errors)
        _validate_choice_list("claim.source_roles", claim.source_roles, SOURCE_ROLES, errors)
        _validate_choice_list("claim.required_source_roles", claim.required_source_roles, SOURCE_ROLES, errors, min_items=1)
        _validate_choice_list("claim.matched_source_roles", claim.matched_source_roles, SOURCE_ROLES, errors)
        _validate_unique_strings("claim.origin_finding_ids", claim.origin_finding_ids, errors)
        _require_ratio("claim.confidence", claim.confidence, errors)
        if claim.trace_status not in {"unmapped", "linked", "mismatch", "audit_only"}:
            errors.append(f"claim {claim.claim_id} trace_status must be one of unmapped, linked, mismatch, audit_only")
        if claim.included_in_report and not claim.report_span_id:
            errors.append(f"claim {claim.claim_id} requires report_span_id when included_in_report is true")
        if (claim.claim_span_start is None) ^ (claim.claim_span_end is None):
            errors.append(f"claim {claim.claim_id} claim_span_start and claim_span_end must both be populated or both be omitted")
        if (
            claim.claim_span_start is not None
            and claim.claim_span_end is not None
            and claim.claim_span_end < claim.claim_span_start
        ):
            errors.append(f"claim {claim.claim_id} claim_span_end must be greater than or equal to claim_span_start")
        if claim.finding_span_starts and len(claim.finding_span_starts) != len(claim.finding_span_ends):
            errors.append(f"claim {claim.claim_id} finding_span_starts and finding_span_ends must have the same length")
        if claim.finding_span_labels and claim.finding_span_starts and len(claim.finding_span_labels) != len(claim.finding_span_starts):
            errors.append(f"claim {claim.claim_id} finding_span_labels must align with finding spans")
        if claim.included_in_report and claim.trace_status == "linked" and (claim.claim_span_start is None or claim.claim_span_end is None):
            errors.append(f"claim {claim.claim_id} must keep an inspectable claim span when trace_status is linked")
        if (
            claim.included_in_report
            and claim.risk_level == "high"
            and "user_provided_source" in claim.source_roles
            and claim.trace_status == "linked"
            and (not claim.origin_finding_ids or not claim.finding_span_starts or not claim.grounding_marker)
        ):
            errors.append(
                f"claim {claim.claim_id} high-risk document-grounded claims require finding spans and a grounding marker"
            )
        if claim.report_line_start < 0 or claim.report_line_end < 0:
            errors.append(f"claim {claim.claim_id} report line numbers must be non-negative")
        if claim.report_line_end and claim.report_line_start and claim.report_line_end < claim.report_line_start:
            errors.append(f"claim {claim.claim_id} report_line_end must be greater than or equal to report_line_start")
        if not isinstance(claim.evidence_count, int) or claim.evidence_count < 0:
            errors.append(f"claim {claim.claim_id} evidence_count must be a non-negative integer")
        if claim.support_status in {"supported", "weak", "scoped_absence"} and claim.evidence_count == 0:
            errors.append(f"claim {claim.claim_id} must count evidence when support_status is '{claim.support_status}'")
        if claim.support_status in {"supported", "scoped_absence"} and not claim.source_ids:
            errors.append(f"claim {claim.claim_id} needs source_ids when support_status='{claim.support_status}'")
        if claim.absence_type:
            _require_choice("claim.absence_type", claim.absence_type, ABSENCE_TYPES, errors)
        if claim.claim_kind == "absence" and claim.support_status != "supported" and not claim.absence_type:
            errors.append(f"claim {claim.claim_id} needs absence_type when absence support is incomplete")
        if claim.claim_kind != "absence" and claim.absence_type:
            errors.append(f"claim {claim.claim_id} has absence_type but claim_kind is not 'absence'")
    return errors


def validate_evidence_map(
    evidence_map: EvidenceMap,
    claims: Sequence[ClaimLedgerRow] | None = None,
    evidence: CollectedEvidence | None = None,
) -> list[str]:
    errors: list[str] = []
    claim_ids = {claim.claim_id for claim in claims or []}
    finding_lookup = {finding.finding_id: finding for finding in (evidence.findings if evidence else [])}
    source_ids = {source.source_id for source in (evidence.sources if evidence else [])}
    link_ids = [link.link_id for link in evidence_map.links]
    citation_ids = [citation.citation_id for citation in evidence_map.citations]
    if len(link_ids) != len(set(link_ids)):
        errors.append("evidence_map.links contains duplicate link_id values")
    if len(citation_ids) != len(set(citation_ids)):
        errors.append("evidence_map.citations contains duplicate citation_id values")
    for link in evidence_map.links:
        errors.extend(validate_evidence_link(link, claim_ids, finding_lookup))
    for citation in evidence_map.citations:
        errors.extend(validate_citation_record(citation, claim_ids, source_ids))
    return errors


def validate_evidence_link(
    link: EvidenceLink,
    claim_ids: set[str],
    finding_lookup: dict[str, Finding],
) -> list[str]:
    errors: list[str] = []
    _require_text("link.link_id", link.link_id, errors)
    _require_choice("link.source_role", link.source_role, SOURCE_ROLES, errors)
    _require_choice("link.relation", link.relation, EVIDENCE_LINK_RELATIONS, errors)
    if claim_ids and link.claim_id not in claim_ids:
        errors.append(f"link {link.link_id} references unknown claim_id '{link.claim_id}'")
    if finding_lookup:
        if link.evidence_id not in finding_lookup:
            errors.append(f"link {link.link_id} references unknown evidence_id '{link.evidence_id}'")
        elif link.source_id not in finding_lookup[link.evidence_id].source_ids:
            errors.append(
                f"link {link.link_id} source_id '{link.source_id}' is not part of evidence '{link.evidence_id}'"
            )
    return errors


def validate_citation_record(
    citation: CitationLedgerRow,
    claim_ids: set[str],
    source_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    _require_text("citation.citation_id", citation.citation_id, errors)
    _require_text("citation.report_section", citation.report_section, errors)
    _require_text("citation.source_title", citation.source_title, errors)
    _require_choice("citation.source_role", citation.source_role, SOURCE_ROLES, errors)
    _require_choice("citation.support_status", citation.support_status, SUPPORT_STATUSES, errors)
    _validate_unique_strings("citation.source_finding_ids", citation.source_finding_ids, errors)
    if citation.trace_status not in {"unmapped", "linked", "mismatch", "audit_only"}:
        errors.append("citation.trace_status must be one of unmapped, linked, mismatch, audit_only")
    if citation.included_in_report and not citation.report_span_id:
        errors.append(f"citation {citation.citation_id} requires report_span_id when included_in_report is true")
    if (citation.claim_span_start is None) ^ (citation.claim_span_end is None):
        errors.append("citation.claim_span_start and claim_span_end must both be populated or both be omitted")
    if (
        citation.claim_span_start is not None
        and citation.claim_span_end is not None
        and citation.claim_span_end < citation.claim_span_start
    ):
        errors.append("citation.claim_span_end must be greater than or equal to claim_span_start")
    if (citation.source_span_start is None) ^ (citation.source_span_end is None):
        errors.append("citation.source_span_start and source_span_end must both be populated or both be omitted")
    if (
        citation.source_span_start is not None
        and citation.source_span_end is not None
        and citation.source_span_end < citation.source_span_start
    ):
        errors.append("citation.source_span_end must be greater than or equal to source_span_start")
    if citation.source_span_starts and len(citation.source_span_starts) != len(citation.source_span_ends):
        errors.append("citation.source_span_starts and source_span_ends must have the same length")
    if citation.source_span_labels and citation.source_span_starts and len(citation.source_span_labels) != len(citation.source_span_starts):
        errors.append("citation.source_span_labels must align with source_span_starts/source_span_ends")
    if not isinstance(citation.provenance_complete, bool):
        errors.append("citation.provenance_complete must be boolean")
    if citation.trace_status == "linked" and not citation.source_finding_ids:
        errors.append(f"citation {citation.citation_id} must keep source_finding_ids when trace_status is linked")
    if citation.trace_status == "linked" and citation.source_role == "user_provided_source":
        has_span = bool(
            (citation.source_span_start is not None and citation.source_span_end is not None)
            or citation.source_span_starts
        )
        if not citation.source_excerpt.strip() or not has_span:
            errors.append(f"citation {citation.citation_id} must keep grounded excerpt span data for linked document citations")
    if claim_ids and citation.claim_id not in claim_ids:
        errors.append(f"citation {citation.citation_id} references unknown claim_id '{citation.claim_id}'")
    if source_ids and citation.source_id not in source_ids:
        errors.append(f"citation {citation.citation_id} references unknown source_id '{citation.source_id}'")
    return errors


def validate_audit_artifacts(
    audits: AuditArtifacts,
    claims: Sequence[ClaimLedgerRow] | None = None,
) -> list[str]:
    errors: list[str] = []
    claim_ids = {claim.claim_id for claim in claims or []}
    for contradiction in audits.contradictions:
        errors.extend(validate_contradiction_record(contradiction, claim_ids if claims is not None else None))
    for gap in audits.gaps:
        errors.extend(validate_evidence_gap_record(gap, claim_ids if claims is not None else None))
    return errors


def validate_contradiction_record(
    contradiction: ContradictionEntry,
    claim_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    _require_text("contradiction.claim_id", contradiction.claim_id, errors)
    _require_text("contradiction.detail", contradiction.detail, errors)
    _require_choice("contradiction.severity", contradiction.severity, AUDIT_SEVERITIES, errors)
    if contradiction.severity_score < 0:
        errors.append("contradiction.severity_score must be zero or greater")
    if claim_ids is not None and contradiction.claim_id not in claim_ids:
        errors.append(f"contradiction references unknown claim_id '{contradiction.claim_id}'")
    return errors


def validate_evidence_gap_record(
    gap: EvidenceGapEntry,
    claim_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    _require_text("gap.claim_id", gap.claim_id, errors)
    _require_text("gap.gap_type", gap.gap_type, errors)
    _require_text("gap.detail", gap.detail, errors)
    _require_text("gap.required_fix", gap.required_fix, errors)
    _require_choice("gap.severity", gap.severity, AUDIT_SEVERITIES, errors)
    if claim_ids is not None and gap.claim_id not in claim_ids:
        errors.append(f"gap references unknown claim_id '{gap.claim_id}'")
    return errors


def validate_release_decision(release: ReleaseGateDecision) -> list[str]:
    errors: list[str] = []
    _require_choice("release.status", release.status, RELEASE_STATUSES, errors)
    _validate_unique_strings("release.reasons", release.reasons, errors, min_items=1)
    _validate_unique_strings("release.blocking_reasons", release.blocking_reasons, errors)
    _validate_unique_strings("release.unresolved_gaps", release.unresolved_gaps, errors)
    if release.status == "blocked" and not release.blocking_reasons:
        errors.append("release.blocking_reasons must be populated when status='blocked'")
    if release.status != "blocked" and release.blocking_reasons:
        errors.append("release.blocking_reasons must be empty unless status='blocked'")
    if release.status == "complete" and release.unresolved_gaps:
        errors.append("release.unresolved_gaps must be empty when status='complete'")
    return errors


def validate_contract_bundle(bundle: PipelineBundle) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_run_request(bundle.request))
    if bundle.intent is not None:
        errors.extend(validate_intent_classification(bundle.intent))
    if bundle.risk is not None:
        errors.extend(validate_risk_classification(bundle.risk))
    if bundle.budget is not None:
        errors.extend(validate_budget_plan(bundle.budget))
    if bundle.adapter is not None:
        errors.extend(validate_domain_adapter(bundle.adapter))
    if bundle.strategy is not None:
        errors.extend(validate_source_strategy(bundle.strategy))
    if bundle.evidence is not None:
        errors.extend(validate_evidence_collection(bundle.evidence))
    if bundle.report_plan:
        errors.extend(validate_report_plan(bundle.report_plan))
    if bundle.draft is not None:
        errors.extend(validate_report_draft(bundle.draft))
    if bundle.claims:
        errors.extend(validate_claim_records(bundle.claims))
    if bundle.evidence_map is not None:
        errors.extend(validate_evidence_map(bundle.evidence_map, bundle.claims, bundle.evidence))
    if bundle.release is not None:
        errors.extend(validate_release_decision(bundle.release))
    errors.extend(validate_bundle_contracts(bundle.draft, bundle.claims, bundle.citations, bundle.evidence) if bundle.draft and bundle.evidence else [])

    if bundle.report_plan and bundle.draft is not None:
        plan_keys = [section.key for section in bundle.report_plan]
        draft_keys = [section.key for section in bundle.draft.sections]
        if plan_keys != draft_keys:
            errors.append("bundle.report_plan must match draft.sections in order and membership")

    if bundle.release is not None and bundle.gaps:
        known_gap_details = {gap.detail for gap in bundle.gaps}
        missing_gap_details = sorted(set(bundle.release.unresolved_gaps) - known_gap_details)
        if missing_gap_details:
            errors.append("release.unresolved_gaps must come from audit gaps: " + ", ".join(missing_gap_details))

    if bundle.claims and bundle.evidence_map is not None:
        evidence_counts: dict[str, set[str]] = defaultdict(set)
        for link in bundle.evidence_map.links:
            evidence_counts[link.claim_id].add(link.evidence_id)
        for claim in bundle.claims:
            linked_count = len(evidence_counts.get(claim.claim_id, set()))
            if linked_count and claim.evidence_count != linked_count:
                errors.append(
                    f"claim {claim.claim_id} evidence_count={claim.evidence_count} does not match "
                    f"{linked_count} linked evidence records"
                )
    return errors


def validate_bundle_contracts(
    draft: ReportDraft,
    claims: list[ClaimLedgerRow],
    citations: list[CitationLedgerRow],
    evidence: CollectedEvidence,
) -> list[str]:
    errors: list[str] = []
    unit_ids = {unit.unit_id for unit in draft.units if unit.is_claim}
    unit_by_id = {unit.unit_id: unit for unit in draft.units}
    finding_ids = {finding.finding_id for finding in evidence.findings}
    claim_ids = set()
    evidence_source_ids = {source.source_id for source in evidence.sources}
    for claim in claims:
        if claim.claim_id in claim_ids:
            errors.append(f"duplicate claim id `{claim.claim_id}`")
        claim_ids.add(claim.claim_id)
        if claim.unit_id and claim.unit_id not in unit_ids:
            errors.append(f"claim `{claim.claim_id}` points to missing unit `{claim.unit_id}`")
        if claim.claim_kind not in CLAIM_KINDS:
            errors.append(f"claim `{claim.claim_id}` uses unknown claim kind `{claim.claim_kind}`")
        if claim.risk_level not in RISK_LEVELS:
            errors.append(f"claim `{claim.claim_id}` uses unknown risk level `{claim.risk_level}`")
        if claim.support_status not in SUPPORT_STATUSES:
            errors.append(f"claim `{claim.claim_id}` uses unknown support status `{claim.support_status}`")
        for role in claim.source_roles + claim.required_source_roles + claim.matched_source_roles:
            if role not in SOURCE_ROLES:
                errors.append(f"claim `{claim.claim_id}` uses unknown source role `{role}`")
        if claim.absence_type and claim.absence_type not in ABSENCE_TYPES:
            errors.append(f"claim `{claim.claim_id}` uses unknown absence type `{claim.absence_type}`")
        if claim.included_in_report and claim.report_span_id != claim.unit_id:
            errors.append(f"claim `{claim.claim_id}` report_span_id must track its unit_id in the current runtime")
        if claim.origin_finding_ids and sorted(set(claim.origin_finding_ids) - finding_ids):
            errors.append(
                f"claim `{claim.claim_id}` points to unknown origin finding IDs: "
                + ", ".join(sorted(set(claim.origin_finding_ids) - finding_ids))
            )
        unit = unit_by_id.get(claim.unit_id)
        if unit is not None and claim.included_in_report and unit.text != claim.exact_text_span:
            errors.append(f"claim `{claim.claim_id}` exact_text_span must match the final draft unit text")
        if claim.included_in_report and claim.claim_span_end != len(claim.exact_text_span):
            errors.append(f"claim `{claim.claim_id}` claim span must cover the exact_text_span in the current runtime")
    draft_claim_unit_ids = {unit.unit_id for unit in draft.units if unit.is_claim}
    if len(claims) != len(draft_claim_unit_ids):
        errors.append("claim ledger does not cover every claim-bearing draft unit")
    for citation in citations:
        if citation.source_id not in evidence_source_ids:
            errors.append(f"citation `{citation.citation_id}` points to unknown source `{citation.source_id}`")
        if citation.source_role not in SOURCE_ROLES:
            errors.append(f"citation `{citation.citation_id}` uses unknown source role `{citation.source_role}`")
        if citation.claim_id not in claim_ids:
            errors.append(f"citation `{citation.citation_id}` points to unknown claim `{citation.claim_id}`")
            continue
        claim = next(claim for claim in claims if claim.claim_id == citation.claim_id)
        if citation.included_in_report and citation.report_span_id != claim.report_span_id:
            errors.append(f"citation `{citation.citation_id}` report_span_id must match claim `{claim.claim_id}`")
        if (
            citation.included_in_report
            and citation.claim_span_start is not None
            and citation.claim_span_end is not None
            and (citation.claim_span_start != claim.claim_span_start or citation.claim_span_end != claim.claim_span_end)
        ):
            errors.append(f"citation `{citation.citation_id}` claim span must match claim `{claim.claim_id}`")
        if citation.trace_status == "linked" and not citation.source_finding_ids:
            errors.append(f"citation `{citation.citation_id}` must retain source_finding_ids when trace_status is linked")
        if (
            citation.trace_status == "linked"
            and (citation.source_role == "user_provided_source" or citation.grounding_marker)
            and not ((citation.source_span_start is not None and citation.source_span_end is not None) or citation.source_span_starts)
        ):
            errors.append(f"citation `{citation.citation_id}` must retain source span data when trace_status is linked")
    return errors


def validate_metrics(metrics: MetricsSnapshot | dict[str, Any]) -> list[str]:
    if isinstance(metrics, dict):
        metrics = MetricsSnapshot(**metrics)
    errors: list[str] = []
    numeric_fields = [
        metrics.total_claim_count,
        metrics.included_claim_count,
        metrics.excluded_claim_count,
        metrics.included_supported_claim_count,
        metrics.included_scoped_absence_count,
        metrics.included_unsupported_claim_count,
        metrics.included_high_risk_claim_count,
        metrics.excluded_high_risk_claim_count,
        metrics.unresolved_high_risk_claim_count,
        metrics.high_risk_role_mismatch_count,
        metrics.unscoped_absence_count,
        metrics.contradiction_count,
        metrics.evidence_gap_count,
        metrics.distinct_source_count,
        metrics.distinct_source_role_count,
        metrics.duplicate_claim_count,
        metrics.metadata_inconsistency_count,
        metrics.citation_trace_mismatch_count,
        metrics.partial_packet_count,
        metrics.trace_mismatch_count,
        metrics.high_risk_traceability_mismatch_count,
        metrics.high_risk_missing_provenance_count,
        metrics.stale_current_tension_count,
        metrics.document_grounded_claim_count,
    ]
    if any(value < 0 for value in numeric_fields):
        errors.append("metrics contain a negative count")
    if metrics.included_claim_count + metrics.excluded_claim_count != metrics.total_claim_count:
        errors.append("included and excluded claim counts do not sum to total claims")
    if not isinstance(metrics.audit_complete, bool):
        errors.append("audit_complete must be boolean")
    if not isinstance(metrics.citation_trace_complete, bool):
        errors.append("citation_trace_complete must be boolean")
    if not isinstance(metrics.traceability_complete, bool):
        errors.append("traceability_complete must be boolean")
    if not isinstance(metrics.ingestion_audit_visible, bool):
        errors.append("ingestion_audit_visible must be boolean")
    return errors


def _validate_budget_shape(field_name: str, budget: dict[str, int | float]) -> list[str]:
    errors: list[str] = []
    if not budget:
        errors.append(f"{field_name} must not be empty")
        return errors
    recognized = {
        "min_sources",
        "min_distinct_roles",
        "min_high_risk_sources",
        "min_citations",
        "candidate_target",
        "deep_read_target",
        "query_budget",
        "open_budget",
        "unique_cited_source_target",
        "citation_instance_target",
    }
    if not (set(budget.keys()) & recognized):
        errors.append(f"{field_name} does not contain any recognized budget keys")
    for key, value in budget.items():
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{field_name}['{key}'] must be numeric")
        elif value < 0:
            errors.append(f"{field_name}['{key}'] must be zero or greater")
    return errors


def _require_text(field_name: str, value: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field_name} must be a non-empty string")


def _require_choice(field_name: str, value: str, allowed: Iterable[str], errors: list[str]) -> None:
    allowed_set = set(allowed)
    if value not in allowed_set:
        errors.append(f"{field_name} must be one of: {', '.join(sorted(allowed_set))}")


def _require_ratio(field_name: str, value: float, errors: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append(f"{field_name} must be numeric")
    elif value < 0 or value > 1:
        errors.append(f"{field_name} must be between 0 and 1")


def _validate_unique_strings(
    field_name: str,
    values: Sequence[str],
    errors: list[str],
    *,
    min_items: int = 0,
) -> None:
    if len(values) < min_items:
        errors.append(f"{field_name} must contain at least {min_items} item(s)")
    if len(values) != len(set(values)):
        errors.append(f"{field_name} must not contain duplicates")
    for value in values:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name} must contain only non-empty strings")
            break


def _validate_choice_list(
    field_name: str,
    values: Sequence[str],
    allowed: Sequence[str],
    errors: list[str],
    *,
    min_items: int = 0,
) -> None:
    _validate_unique_strings(field_name, values, errors, min_items=min_items)
    allowed_set = set(allowed)
    invalid = sorted({value for value in values if value not in allowed_set})
    if invalid:
        errors.append(f"{field_name} contains unsupported values: {', '.join(invalid)}")
