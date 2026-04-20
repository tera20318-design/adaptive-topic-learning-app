from __future__ import annotations

import inspect
from pathlib import Path

from cleanroom_runtime.catalogs import INTERNAL_HEADING_FRAGMENTS
from cleanroom_runtime.core.gates.decision_usable import assess_decision_usable
from cleanroom_runtime.models import MetricsSnapshot, PipelineBundle, RunRequest
from cleanroom_runtime.stage_contracts import audit_stage_output, contract_error_messages
from cleanroom_runtime.stages.bundle_renderer import render_bundle
from cleanroom_runtime.stages.claim_extractor import extract_claims
from cleanroom_runtime.stages.contradiction_absence_guard import apply_contradiction_absence_guard
from cleanroom_runtime.stages.domain_adapter_generator import generate_domain_adapter
from cleanroom_runtime.stages.draft_generator import write_draft
from cleanroom_runtime.stages.evidence_ingestion import ingest_evidence
from cleanroom_runtime.stages.evidence_mapper import map_claims_to_evidence
from cleanroom_runtime.stages.intent_classifier import classify_intent
from cleanroom_runtime.stages.release_gate import decide_release_gate
from cleanroom_runtime.stages.report_planner import plan_report
from cleanroom_runtime.stages.risk_tier_classifier import classify_risk_tier
from cleanroom_runtime.stages.scope_budget_planner import plan_scope_and_budget
from cleanroom_runtime.stages.source_strategy_builder import build_source_strategy
from cleanroom_runtime.stages.tone_control import apply_tone_control
from cleanroom_runtime.validators import validate_bundle_contracts, validate_domain_adapter, validate_metrics
from cleanroom_runtime.utils import normalize_text


def run_pipeline(request: RunRequest, output_dir: Path | None = None) -> PipelineBundle:
    stage_failures = []
    stage_snapshots = []

    def record_stage(stage_name: str, artifact, **context):
        failures, snapshot = audit_stage_output(stage_name, artifact, **context)
        stage_failures.extend(failures)
        stage_snapshots.append(snapshot)
        return artifact

    intent = classify_intent(request)
    record_stage("intent_classifier", intent, request=request)
    risk = classify_risk_tier(request, intent)
    record_stage("risk_tier_classifier", risk, request=request, intent=intent)
    budget = plan_scope_and_budget(request, intent, risk)
    record_stage("scope_budget_planner", budget, request=request, intent=intent, risk=risk)
    adapter = generate_domain_adapter(request, intent, risk, budget)
    record_stage("domain_adapter_generator", adapter, request=request, intent=intent, risk=risk, budget=budget)
    strategy = build_source_strategy(intent, risk, adapter)
    record_stage("source_strategy_builder", strategy, adapter=adapter, intent=intent, risk=risk)
    evidence = ingest_evidence(request)
    record_stage("evidence_ingestion", evidence, request=request)
    report_plan = plan_report(intent, adapter, budget, strategy)
    record_stage("report_planner", {"sections": report_plan}, adapter=adapter, budget=budget, strategy=strategy)
    draft = write_draft(request, adapter, evidence, report_plan, budget)
    record_stage(
        "draft_generator",
        draft,
        request=request,
        adapter=adapter,
        evidence=evidence,
        report_plan=report_plan,
        budget=budget,
    )
    claims = extract_claims(draft, strategy)
    record_stage("claim_extractor", {"claims": claims}, draft=draft, strategy=strategy)
    claims, citations = map_claims_to_evidence(claims, evidence, strategy)
    record_stage("evidence_mapper", {"claims": claims, "citations": citations}, evidence=evidence, strategy=strategy)
    claims, draft, contradictions, gaps = apply_contradiction_absence_guard(claims, draft, request, evidence)
    record_stage(
        "contradiction_absence_guard",
        {"claims": claims, "draft": draft, "contradictions": contradictions, "gaps": gaps},
        request=request,
    )
    draft = apply_tone_control(draft, claims)
    record_stage("tone_control", draft, request=request, evidence=evidence, claims=claims)
    citations = _sync_citations(citations, claims)
    claims, citations = _link_traceability(draft, claims, citations, evidence)
    decision_usable = _call_assess_decision_usable(
        draft=draft,
        claims=claims,
        citations=citations,
        adapter=adapter,
        budget=budget,
        request=request,
        intent=intent,
        risk=risk,
    )
    metrics = _build_metrics(request, budget, evidence, draft, claims, citations, contradictions, gaps, decision_usable, stage_snapshots)
    record_stage("metrics_builder", metrics, budget=budget)

    validation_errors = contract_error_messages(stage_failures)
    validation_errors.extend(validate_domain_adapter(adapter))
    validation_errors.extend(validate_bundle_contracts(draft, claims, citations, evidence))
    validation_errors.extend(validate_metrics(metrics))

    release_gate = decide_release_gate(
        draft=draft,
        claims=claims,
        citations=citations,
        contradictions=contradictions,
        gaps=gaps,
        budget=budget,
        adapter=adapter,
        metrics=metrics,
        validation_errors=validation_errors,
        request=request,
        intent=intent,
        risk=risk,
        decision_usable=decision_usable,
    )
    record_stage("release_gate", release_gate, budget=budget)

    bundle = PipelineBundle(
        request=request,
        intent=intent,
        risk=risk,
        budget=budget,
        strategy=strategy,
        adapter=adapter,
        evidence=evidence,
        draft=draft,
        claims=claims,
        citations=citations,
        contradictions=contradictions,
        gaps=gaps,
        release_gate=release_gate,
        metrics=metrics,
        decision_usable=decision_usable.to_dict(),
        report_plan=report_plan,
        stage_failures=stage_failures,
        stage_snapshots=stage_snapshots,
    )

    if output_dir is not None:
        render_bundle(bundle, output_dir)
    return bundle


def _sync_citations(citations, claims):
    included_by_claim = {claim.claim_id: claim.included_in_report for claim in claims}
    span_by_claim = {claim.claim_id: claim.report_span_id for claim in claims}
    claim_span_start_by_claim = {claim.claim_id: claim.claim_span_start for claim in claims}
    claim_span_end_by_claim = {claim.claim_id: claim.claim_span_end for claim in claims}
    synced = []
    for citation in citations:
        synced.append(
            type(citation)(
                citation_id=citation.citation_id,
                claim_id=citation.claim_id,
                report_section=citation.report_section,
                source_id=citation.source_id,
                source_role=citation.source_role,
                source_title=citation.source_title,
                support_status=citation.support_status,
                included_in_report=included_by_claim.get(citation.claim_id, citation.included_in_report),
                report_span_id=span_by_claim.get(citation.claim_id, citation.report_span_id),
                claim_span_start=claim_span_start_by_claim.get(citation.claim_id, citation.claim_span_start),
                claim_span_end=claim_span_end_by_claim.get(citation.claim_id, citation.claim_span_end),
                source_finding_ids=list(citation.source_finding_ids),
                source_excerpt=citation.source_excerpt,
                source_span_label=citation.source_span_label,
                source_span_start=citation.source_span_start,
                source_span_end=citation.source_span_end,
                source_span_labels=list(citation.source_span_labels),
                source_span_starts=list(citation.source_span_starts),
                source_span_ends=list(citation.source_span_ends),
                grounding_marker=citation.grounding_marker,
                grounding_scope_note=citation.grounding_scope_note,
                trace_status=citation.trace_status,
                provenance_complete=citation.provenance_complete,
            )
        )
    return synced


def _link_traceability(draft, claims, citations, evidence):
    unit_by_id = {unit.unit_id: unit for unit in draft.units}
    line_ranges = _report_line_ranges(draft)
    finding_lookup = {finding.finding_id: finding for finding in evidence.findings}
    source_lookup = {source.source_id: source for source in evidence.sources}
    updated_claims = []
    for claim in claims:
        unit = unit_by_id.get(claim.unit_id)
        origin_findings = [finding_lookup[finding_id] for finding_id in claim.origin_finding_ids if finding_id in finding_lookup]
        line_start, line_end = line_ranges.get(claim.unit_id, (0, 0))
        trace_status = claim.trace_status
        exact_text_span = claim.exact_text_span
        normalized_claim = claim.normalized_claim
        report_span_id = claim.report_span_id or claim.unit_id
        claim_span_start = claim.claim_span_start
        claim_span_end = claim.claim_span_end
        finding_span_labels, finding_span_starts, finding_span_ends = _flatten_finding_spans(origin_findings)
        grounding_marker = next((finding.grounding_marker for finding in origin_findings if finding.grounding_marker), claim.grounding_marker)
        grounding_scope_note = " ".join(
            dict.fromkeys(
                note
                for note in [
                    *(finding.grounding_scope_note for finding in origin_findings if finding.grounding_scope_note),
                    *(finding.scope_note for finding in origin_findings if finding.scope_note),
                    claim.grounding_scope_note,
                ]
                if note
            )
        )
        if unit is None:
            trace_status = "mismatch" if claim.included_in_report else "audit_only"
        else:
            exact_text_span = unit.text
            normalized_claim = normalize_text(unit.text)
            claim_span_start = 0
            claim_span_end = len(unit.text)
            if claim.included_in_report and line_start == 0:
                trace_status = "mismatch"
            elif claim.origin_finding_ids and not origin_findings:
                trace_status = "mismatch"
            elif _claim_requires_span_grounding(claim, origin_findings, source_lookup) and not _has_grounded_finding_spans(origin_findings):
                trace_status = "mismatch"
            elif _document_trace_gap(claim, origin_findings, source_lookup):
                trace_status = "mismatch"
            elif claim.included_in_report:
                trace_status = "linked"
            else:
                trace_status = "audit_only"
        updated_claims.append(
            type(claim)(
                claim_id=claim.claim_id,
                unit_id=claim.unit_id,
                report_section=claim.report_section,
                exact_text_span=exact_text_span,
                normalized_claim=normalized_claim,
                claim_kind=claim.claim_kind,
                risk_level=claim.risk_level,
                source_ids=list(claim.source_ids),
                source_roles=list(claim.source_roles),
                evidence_count=claim.evidence_count,
                required_source_roles=list(claim.required_source_roles),
                matched_source_roles=list(claim.matched_source_roles),
                support_status=claim.support_status,
                confidence=claim.confidence,
                caveat_required=claim.caveat_required,
                suggested_tone=claim.suggested_tone,
                required_fix=claim.required_fix,
                origin_finding_ids=list(claim.origin_finding_ids),
                report_span_id=report_span_id,
                report_line_start=line_start,
                report_line_end=line_end,
                claim_span_start=claim_span_start,
                claim_span_end=claim_span_end,
                finding_span_labels=finding_span_labels,
                finding_span_starts=finding_span_starts,
                finding_span_ends=finding_span_ends,
                grounding_marker=grounding_marker,
                grounding_scope_note=grounding_scope_note,
                trace_status=trace_status,
                included_in_report=claim.included_in_report,
                absence_type=claim.absence_type,
                absence_scope=claim.absence_scope,
                contradiction_note=claim.contradiction_note,
                jurisdiction=claim.jurisdiction,
                subject_key=claim.subject_key,
                freshness_tag=claim.freshness_tag,
                blocking_reasons=list(claim.blocking_reasons),
                exclusion_reasons=list(claim.exclusion_reasons),
                report_section_key=claim.report_section_key,
            )
        )

    updated_claim_by_id = {claim.claim_id: claim for claim in updated_claims}
    updated_citations = []
    for citation in citations:
        claim = updated_claim_by_id.get(citation.claim_id)
        trace_status = citation.trace_status
        provenance_complete = citation.provenance_complete
        related_findings = [finding_lookup[finding_id] for finding_id in citation.source_finding_ids if finding_id in finding_lookup]
        source_span_labels, source_span_starts, source_span_ends = _flatten_finding_spans(related_findings)
        if claim is None:
            trace_status = "mismatch"
            provenance_complete = False
        else:
            if not claim.included_in_report:
                trace_status = "audit_only"
            elif not citation.source_finding_ids or any(finding_id not in finding_lookup for finding_id in citation.source_finding_ids):
                trace_status = "mismatch"
            elif _claim_requires_span_grounding(claim, related_findings, source_lookup) and not _has_grounded_finding_spans(related_findings):
                trace_status = "mismatch"
            elif _document_trace_gap(claim, related_findings, source_lookup):
                trace_status = "mismatch"
            else:
                trace_status = "linked"
        requires_span_trace = citation.source_role == "user_provided_source" or any(
            getattr(finding, "grounding_marker", "") for finding in related_findings
        )
        provenance_complete = provenance_complete and (not requires_span_trace or _has_grounded_finding_spans(related_findings))
        updated_citations.append(
            type(citation)(
                citation_id=citation.citation_id,
                claim_id=citation.claim_id,
                report_section=citation.report_section,
                source_id=citation.source_id,
                source_role=citation.source_role,
                source_title=citation.source_title,
                support_status=citation.support_status,
                included_in_report=claim.included_in_report if claim is not None else citation.included_in_report,
                report_span_id=claim.report_span_id if claim is not None else citation.report_span_id,
                claim_span_start=claim.claim_span_start if claim is not None else citation.claim_span_start,
                claim_span_end=claim.claim_span_end if claim is not None else citation.claim_span_end,
                source_finding_ids=list(citation.source_finding_ids),
                source_excerpt=citation.source_excerpt or _combined_excerpt(related_findings),
                source_span_label=_combined_span_label(source_span_labels) or citation.source_span_label,
                source_span_start=source_span_starts[0] if source_span_starts else citation.source_span_start,
                source_span_end=source_span_ends[-1] if source_span_ends else citation.source_span_end,
                source_span_labels=source_span_labels or list(citation.source_span_labels),
                source_span_starts=source_span_starts or list(citation.source_span_starts),
                source_span_ends=source_span_ends or list(citation.source_span_ends),
                grounding_marker=next((finding.grounding_marker for finding in related_findings if finding.grounding_marker), citation.grounding_marker),
                grounding_scope_note=" ".join(
                    dict.fromkeys(
                        note
                        for note in [
                            *(finding.grounding_scope_note for finding in related_findings if finding.grounding_scope_note),
                            *(finding.scope_note for finding in related_findings if finding.scope_note),
                            citation.grounding_scope_note,
                        ]
                        if note
                    )
                ),
                trace_status=trace_status,
                provenance_complete=provenance_complete,
            )
        )
    return updated_claims, updated_citations


def _report_line_ranges(draft):
    line_number = 1
    ranges = {}
    line_number += 2
    for section in draft.sections:
        line_number += 2
        section_units = [unit for unit in draft.units if unit.section_key == section.key and unit.include_in_report]
        if not section_units:
            line_number += 2
            continue
        for unit in section_units:
            ranges[unit.unit_id] = (line_number, line_number)
            line_number += 1
        line_number += 1
    return ranges


def _call_assess_decision_usable(**available_args):
    signature = inspect.signature(assess_decision_usable)
    compatible_args = {name: value for name, value in available_args.items() if name in signature.parameters}
    return assess_decision_usable(**compatible_args)


def _build_metrics(request, budget, evidence, draft, claims, citations, contradictions, gaps, decision_usable, stage_snapshots) -> MetricsSnapshot:
    total_claims = len(claims)
    included_claims = [claim for claim in claims if claim.included_in_report]
    excluded_claims = [claim for claim in claims if not claim.included_in_report]
    included_supported = [claim for claim in included_claims if claim.support_status == "supported"]
    included_scoped_absence = [claim for claim in included_claims if claim.support_status == "scoped_absence"]
    included_unsupported = [claim for claim in included_claims if claim.support_status not in {"supported", "scoped_absence"}]
    included_high_risk = [claim for claim in included_claims if claim.risk_level == "high"]
    excluded_high_risk = [claim for claim in excluded_claims if claim.risk_level == "high"]
    unresolved_high_risk = [claim for claim in claims if claim.risk_level == "high" and claim.support_status not in {"supported", "scoped_absence"}]
    high_risk_role_mismatch = [claim for claim in claims if claim.risk_level == "high" and claim.claim_kind != "scope_boundary" and not claim.matched_source_roles]
    unscoped_absence = [claim for claim in claims if claim.claim_kind == "absence" and claim.absence_scope is None]
    duplicate_claim_count = total_claims - len({claim.normalized_claim for claim in claims})
    sources = list(evidence.sources)
    source_lookup = {source.source_id: source for source in sources}
    source_ids = {source.source_id for source in sources}
    source_roles = {source.source_role for source in sources}
    claim_unit_ids = {claim.unit_id for claim in claims}
    draft_claim_unit_ids = {unit.unit_id for unit in draft.units if unit.is_claim}
    included_citations = [citation for citation in citations if citation.included_in_report]
    claim_by_id = {claim.claim_id: claim for claim in claims}
    referenced_source_ids = {source_id for claim in claims for source_id in claim.source_ids}
    metadata_inconsistency_count = sum(
        1 for source in sources if source.source_id in referenced_source_ids and not source.provenance.metadata_consistent
    )
    citation_trace_mismatch_count = sum(
        1 for source in sources if source.source_id in referenced_source_ids and not source.provenance.citation_trace_complete
    )
    citation_trace_mismatch_count += sum(
        1
        for citation in citations
        if citation.included_in_report and (citation.source_id not in source_ids or citation.trace_status != "linked")
    )
    citation_trace_mismatch_count += sum(
        1
        for citation in citations
        if citation.included_in_report
        and claim_by_id.get(citation.claim_id) is not None
        and claim_by_id[citation.claim_id].risk_level == "high"
        and _citation_requires_span_trace(citation)
        and not _citation_has_span_trace(citation)
    )
    partial_packet_count = sum(1 for source in sources if source.provenance.partial)
    high_risk_traceability_mismatch_count = sum(
        1
        for claim in claims
        if claim.risk_level == "high"
        and claim.included_in_report
        and (
            claim.trace_status != "linked"
            or claim.claim_span_start is None
            or claim.claim_span_end is None
            or not claim.origin_finding_ids
            or not any(
                citation.claim_id == claim.claim_id and _citation_supports_high_risk_trace(citation)
                for citation in citations
            )
        )
    )
    high_risk_missing_provenance_count = sum(
        1
        for claim in claims
        if claim.risk_level == "high"
        and any(
            source_id not in source_ids
            or not source_lookup[source_id].provenance.metadata_consistent
            or source_lookup[source_id].provenance.malformed
            or source_lookup[source_id].provenance.role_inference_status == "ambiguous"
            or bool(set(source_lookup[source_id].provenance.metadata_missing_fields) & {"source_id", "title", "source_role"})
            for source_id in claim.source_ids
        )
    )
    trace_mismatch_count = sum(1 for claim in claims if claim.trace_status != ("audit_only" if not claim.included_in_report else "linked"))
    trace_mismatch_count += sum(1 for citation in citations if citation.trace_status != ("audit_only" if not citation.included_in_report else "linked"))
    stale_current_tension_count = sum(1 for gap in gaps if gap.gap_type == "stale_current_tension")
    document_grounded_claim_count = sum(
        1
        for claim in claims
        if any(
            finding.finding_id in claim.origin_finding_ids and finding.grounding_kind in {"direct_quote", "paraphrase"} and _has_grounded_finding_spans([finding])
            for finding in evidence.findings
        )
    )
    target_results = {
        "min_sources": len(source_ids) >= budget.target_profile.min_sources,
        "min_distinct_roles": len(source_roles) >= budget.target_profile.min_distinct_roles,
        "min_high_risk_sources": len({source_id for claim in claims if claim.risk_level == "high" for source_id in claim.source_ids}) >= budget.target_profile.min_high_risk_sources,
    }
    target_misses = [key for key, passed in target_results.items() if not passed]
    target_miss_without_waiver = any(target not in budget.waivers for target in target_misses)
    limitations_visible = any(unit.section_key in {"scope", "uncertainty"} and unit.include_in_report for unit in draft.units)
    uncertainty_section_present = any(section.key == "uncertainty" for section in draft.sections)
    direct_answer_present = any(unit.section_key == "direct_answer" and unit.include_in_report for unit in draft.units)
    scope_and_exclusions_present = any(unit.section_key == "scope" and unit.include_in_report for unit in draft.units)
    checklist_present = any(unit.section_key == "checklist" and unit.include_in_report for unit in draft.units)
    next_action_or_next_research_present = any(
        unit.section_key in {"decision_layer", "checklist", "uncertainty"}
        and any(marker in unit.text.casefold() for marker in ("next", "check", "verify", "follow-up", "follow up", "research"))
        and unit.include_in_report
        for unit in draft.units
    )
    internal_heading_present = any(
        any(fragment in value.casefold() for fragment in INTERNAL_HEADING_FRAGMENTS)
        for value in [*(section.title for section in draft.sections), *(unit.text for unit in draft.units if unit.include_in_report)]
    )
    tradeoff_table_present = _has_tradeoff_table(draft)
    finance_risk_disclosure_present = _has_finance_risk_disclosure(draft)
    ingestion_audit_visible = any(
        getattr(snapshot, "artifact_type", "") == "packet_ingestion_audit"
        for snapshot in stage_snapshots
    )

    return MetricsSnapshot(
        total_claim_count=total_claims,
        included_claim_count=len(included_claims),
        excluded_claim_count=len(excluded_claims),
        included_supported_claim_count=len(included_supported),
        included_scoped_absence_count=len(included_scoped_absence),
        included_unsupported_claim_count=len(included_unsupported),
        included_high_risk_claim_count=len(included_high_risk),
        excluded_high_risk_claim_count=len(excluded_high_risk),
        unresolved_high_risk_claim_count=len(unresolved_high_risk),
        high_risk_role_mismatch_count=len(high_risk_role_mismatch),
        unscoped_absence_count=len(unscoped_absence),
        contradiction_count=len(contradictions),
        evidence_gap_count=len(gaps),
        distinct_source_count=len(source_ids),
        distinct_source_role_count=len(source_roles),
        duplicate_claim_count=duplicate_claim_count,
        audit_complete=claim_unit_ids == draft_claim_unit_ids,
        citation_trace_complete=all(citation.trace_status == "linked" and citation.provenance_complete for citation in included_citations) and citation_trace_mismatch_count == 0,
        traceability_complete=trace_mismatch_count == 0,
        uncertainty_section_present=uncertainty_section_present,
        limitations_visible=limitations_visible,
        direct_answer_present=direct_answer_present,
        scope_and_exclusions_present=scope_and_exclusions_present,
        checklist_present=checklist_present,
        next_action_or_next_research_present=next_action_or_next_research_present,
        internal_heading_present=internal_heading_present,
        tradeoff_table_present=tradeoff_table_present,
        finance_risk_disclosure_present=finance_risk_disclosure_present,
        checklist_aligned_to_reader_task=decision_usable.checks.get("checklist_aligned_to_reader_task", False),
        specific_next_action_present=decision_usable.checks.get("specific_next_action_present", False),
        explicit_tradeoff_language_present=decision_usable.checks.get("explicit_tradeoff_language_present", False),
        document_grounding_present=decision_usable.checks.get("direct_document_grounding_present", False),
        non_generic_uncertainty_present=decision_usable.checks.get("non_generic_uncertainty_present", False),
        metadata_inconsistency_count=metadata_inconsistency_count,
        citation_trace_mismatch_count=citation_trace_mismatch_count,
        partial_packet_count=partial_packet_count,
        trace_mismatch_count=trace_mismatch_count,
        high_risk_traceability_mismatch_count=high_risk_traceability_mismatch_count,
        high_risk_missing_provenance_count=high_risk_missing_provenance_count,
        stale_current_tension_count=stale_current_tension_count,
        document_grounded_claim_count=document_grounded_claim_count,
        ingestion_audit_visible=ingestion_audit_visible,
        target_results=target_results,
        target_misses=target_misses,
        target_miss_without_waiver=target_miss_without_waiver,
        research_completeness=budget.research_completeness_note,
        reader_decision_layer_present=decision_usable.checks.get(
            "reader_decision_layer_present",
            any(unit.section_key == "decision_layer" and unit.include_in_report for unit in draft.units),
        ),
    )


def _has_tradeoff_table(draft) -> bool:
    option_units = [unit for unit in draft.units if unit.section_key == "options" and unit.include_in_report]
    if len(option_units) < 2:
        return False
    table_like = [unit.text.casefold() for unit in option_units if unit.text.count("|") >= 2]
    if len(table_like) < 2:
        return False
    joined = " ".join(table_like)
    return any(marker in joined for marker in ("tradeoff", "tradeoffs", "advantage", "limitation", "cost"))


def _has_finance_risk_disclosure(draft) -> bool:
    strong_markers = ("risk disclosure", "downside", "loss", "lose", "volatility", "not guaranteed", "suitability")
    contextual_markers = ("constraint", "constraints", "tolerance", "reader", "depends", "tradeoff", "tradeoffs")
    for unit in draft.units:
        if not unit.include_in_report:
            continue
        if unit.section_key not in {"uncertainty", "checklist", "decision_layer"}:
            continue
        lowered = unit.text.casefold()
        if any(marker in lowered for marker in strong_markers):
            return True
        if "risk" in lowered and "high-risk" not in lowered and any(marker in lowered for marker in contextual_markers):
            return True
    return False


def _flatten_finding_spans(findings):
    labels = []
    starts = []
    ends = []
    for finding in findings:
        local_labels = list(getattr(finding, "source_span_labels", [])) or ([finding.source_span_label] if finding.source_span_label else [])
        local_starts = list(getattr(finding, "source_span_starts", [])) or ([finding.source_span_start] if finding.source_span_start is not None else [])
        local_ends = list(getattr(finding, "source_span_ends", [])) or ([finding.source_span_end] if finding.source_span_end is not None else [])
        if local_starts and local_ends and len(local_starts) == len(local_ends):
            labels.extend(local_labels if local_labels and len(local_labels) == len(local_starts) else [f"span {index + 1}" for index in range(len(local_starts))])
            starts.extend(local_starts)
            ends.extend(local_ends)
    return labels, starts, ends


def _has_grounded_finding_spans(findings):
    if not findings:
        return False
    for finding in findings:
        starts = list(getattr(finding, "source_span_starts", [])) or ([finding.source_span_start] if finding.source_span_start is not None else [])
        ends = list(getattr(finding, "source_span_ends", [])) or ([finding.source_span_end] if finding.source_span_end is not None else [])
        if not finding.source_excerpt.strip():
            return False
        if not starts or not ends or len(starts) != len(ends):
            return False
    return True


def _claim_requires_span_grounding(claim, origin_findings, source_lookup):
    if any("user_provided_source" in finding.source_roles for finding in origin_findings):
        return True
    if any(getattr(finding, "grounding_marker", "") for finding in origin_findings):
        return True
    return any(getattr(source_lookup.get(source_id), "source_role", "") == "user_provided_source" for source_id in claim.source_ids)


def _combined_span_label(labels):
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    return ", ".join(dict.fromkeys(labels))


def _combined_excerpt(findings):
    excerpts = [finding.source_excerpt for finding in findings if finding.source_excerpt]
    if not excerpts:
        return ""
    return "\n...\n".join(dict.fromkeys(excerpts))


def _citation_has_span_trace(citation):
    starts = list(citation.source_span_starts) or ([citation.source_span_start] if citation.source_span_start is not None else [])
    ends = list(citation.source_span_ends) or ([citation.source_span_end] if citation.source_span_end is not None else [])
    return bool(citation.claim_span_start is not None and citation.claim_span_end is not None and starts and ends and len(starts) == len(ends))


def _citation_supports_high_risk_trace(citation):
    if not citation.included_in_report or citation.trace_status != "linked" or not citation.provenance_complete or not citation.source_finding_ids:
        return False
    if _citation_requires_span_trace(citation):
        starts = list(citation.source_span_starts) or ([citation.source_span_start] if citation.source_span_start is not None else [])
        ends = list(citation.source_span_ends) or ([citation.source_span_end] if citation.source_span_end is not None else [])
        return bool(citation.source_excerpt and starts and ends and len(starts) == len(ends))
    return True


def _citation_requires_span_trace(citation):
    return citation.source_role == "user_provided_source" or bool(citation.grounding_marker)


def _document_trace_gap(claim, origin_findings, source_lookup):
    document_findings = [
        finding for finding in origin_findings if _uses_user_document(finding.source_ids, finding.source_roles, source_lookup)
    ]
    if not document_findings:
        return False
    if any(getattr(finding, "grounding_marker", "") == "unsupported_span_synthesis" for finding in document_findings):
        return True
    if len(document_findings) > 1 and claim.claim_kind != "scope_boundary":
        return True
    if not _has_grounded_finding_spans(document_findings):
        return True
    lowered = (claim.exact_text_span or "").casefold()
    if set(claim.source_roles) == {"user_provided_source"} and claim.claim_kind != "scope_boundary":
        return not any(marker in lowered for marker in ("checked document", "checked excerpt", "uploaded document", "checked materials"))
    return False


def _uses_user_document(source_ids, source_roles, source_lookup):
    if "user_provided_source" in source_roles:
        return True
    return any(getattr(source_lookup.get(source_id), "source_role", "") == "user_provided_source" for source_id in source_ids)
