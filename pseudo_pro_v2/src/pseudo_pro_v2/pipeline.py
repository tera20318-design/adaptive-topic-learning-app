from __future__ import annotations

import re
from pathlib import Path

from pseudo_pro_v2.catalogs import INTERNAL_HEADING_FRAGMENTS, MODE_BASELINES
from pseudo_pro_v2.models import (
    CitationLedgerRow,
    PipelineBundle,
    ReleaseContract,
    RunRequest,
    SourceFinding,
    SourcePacket,
    TargetProfile,
)
from pseudo_pro_v2.stages.bundle_renderer import render_bundle, render_report_markdown
from pseudo_pro_v2.stages.claim_extractor import extract_claims
from pseudo_pro_v2.stages.contradiction_absence_guard import apply_contradiction_absence_guard
from pseudo_pro_v2.stages.domain_adapter_generator import generate_domain_adapter
from pseudo_pro_v2.stages.draft_writer import write_draft
from pseudo_pro_v2.stages.evidence_collector import collect_evidence
from pseudo_pro_v2.stages.evidence_mapper import map_claims_to_evidence
from pseudo_pro_v2.stages.intent_classifier import classify_intent
from pseudo_pro_v2.stages.release_gate import decide_release_gate
from pseudo_pro_v2.stages.report_planner import plan_report
from pseudo_pro_v2.stages.risk_tier_classifier import classify_risk_tier
from pseudo_pro_v2.stages.scope_budget_planner import plan_scope_and_budget
from pseudo_pro_v2.stages.source_strategy_builder import build_source_strategy
from pseudo_pro_v2.stages.tone_controller import apply_tone_control
from pseudo_pro_v2.runtime_paths import normalize_path, package_root, schema_root
from pseudo_pro_v2.utils import load_json
from pseudo_pro_v2.validators import (
    validate_citation_ledger_rows,
    validate_clean_room_integrity,
    validate_claim_ledger_rows,
    validate_domain_adapter,
    validate_metrics,
    validate_release_gate_inputs,
)


def load_request(request_path: Path, source_packets_path: Path) -> RunRequest:
    request_path = normalize_path(request_path)
    source_packets_path = normalize_path(source_packets_path)
    request_payload = load_json(request_path)
    sources_payload = load_json(source_packets_path)
    target_profile = request_payload.get("target_profile", {})
    release_contract = request_payload.get("release_contract", {})
    request = RunRequest(
        topic=request_payload["topic"],
        reader=request_payload["reader"],
        use_context=request_payload["use_context"],
        desired_depth=request_payload["desired_depth"],
        jurisdiction=request_payload["jurisdiction"],
        mode=request_payload["mode"],
        evidence_mode=request_payload.get("evidence_mode", "synthetic"),
        target_profile=TargetProfile(
            min_sources=int(target_profile.get("min_sources", MODE_BASELINES.get(request_payload["mode"], MODE_BASELINES["scoped"])["min_sources"])),
            min_citations=int(target_profile.get("min_citations", MODE_BASELINES.get(request_payload["mode"], MODE_BASELINES["scoped"])["min_citations"])),
            min_report_claim_capture_ratio=float(
                target_profile.get(
                    "min_report_claim_capture_ratio",
                    MODE_BASELINES.get(request_payload["mode"], MODE_BASELINES["scoped"])["min_report_claim_capture_ratio"],
                )
            ),
        ),
        release_contract=ReleaseContract(
            allow_synthetic_complete=bool(release_contract.get("allow_synthetic_complete", False))
        ),
        waivers=request_payload.get("waivers", []),
    )
    request.source_packets = [_load_source_packet(item) for item in sources_payload["source_packets"]]
    return request


def run_pipeline(request_path: Path, source_packets_path: Path, output_dir: Path) -> PipelineBundle:
    request_path = normalize_path(request_path)
    source_packets_path = normalize_path(source_packets_path)
    output_dir = normalize_path(output_dir)
    request = load_request(request_path, source_packets_path)
    intent = classify_intent(request)
    risk = classify_risk_tier(request, intent)
    budget = plan_scope_and_budget(request, intent, risk)
    adapter = generate_domain_adapter(request, intent, risk, budget)
    strategy = build_source_strategy(intent, risk, adapter)
    evidence = collect_evidence(request)
    report_plan = plan_report(adapter)
    draft = write_draft(request, adapter, evidence, report_plan, budget)
    claims = extract_claims(draft, strategy)
    claims, citations = map_claims_to_evidence(claims, evidence, strategy)
    claims, draft, contradictions, gaps = apply_contradiction_absence_guard(claims, draft, request)
    draft = apply_tone_control(draft, claims)
    claims, citations = _sync_claims_and_citations(claims, citations, draft)
    report_text = render_report_markdown(request.topic, draft.sections, draft.units)
    metrics = _build_metrics(request, budget, evidence, draft, claims, citations, report_text)

    schemas = schema_root(repo_root=_package_root())
    domain_errors = validate_domain_adapter(_domain_adapter_to_payload(adapter), schemas / "domain-adapter.schema.json")
    claim_errors = validate_claim_ledger_rows(_claim_rows(claims), schemas / "claim-ledger.schema.tsv")
    citation_errors = validate_citation_ledger_rows(_citation_rows(citations), schemas / "citation-ledger.schema.tsv")
    gate_input_errors = validate_release_gate_inputs(draft, claims, citations, metrics)
    metric_errors = validate_metrics(metrics)
    clean_room_errors = validate_clean_room_integrity(_package_root())

    release_gate = decide_release_gate(
        draft=draft,
        claims=claims,
        citations=citations,
        contradictions=contradictions,
        gaps=gaps,
        budget=budget,
        adapter=adapter,
        metrics=metrics,
        validation_errors=domain_errors + claim_errors + citation_errors + gate_input_errors + metric_errors + clean_room_errors,
    )

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
        metrics=metrics | {"release_status": release_gate.status},
    )
    render_bundle(bundle, output_dir)
    return bundle


def _load_source_packet(payload: dict) -> SourcePacket:
    packet = SourcePacket(
        source_id=payload["source_id"],
        title=payload["title"],
        source_role=payload["source_role"],
        citation=payload.get("citation", payload["title"]),
        summary=payload.get("summary", ""),
        quality_flags=payload.get("quality_flags", []),
        jurisdiction=payload.get("jurisdiction", ""),
        published_on=payload.get("published_on", ""),
    )
    packet.findings = [
        SourceFinding(
            finding_id=item["finding_id"],
            statement=item["statement"],
            claim_kind=item["claim_kind"],
            risk_level=item["risk_level"],
            section_hint=item["section_hint"],
            decision_note=item.get("decision_note", ""),
            support_status_hint=item.get("support_status_hint", "not_checked"),
            confidence=float(item.get("confidence", 0.8)),
            source_ids=item.get("source_ids", [payload["source_id"]]),
            source_roles=item.get("source_roles", []),
            risk_tags=item.get("risk_tags", []),
            failure_modes=item.get("failure_modes", []),
            misunderstandings=item.get("misunderstandings", []),
            boundary_concepts=item.get("boundary_concepts", []),
            caveat=item.get("caveat", ""),
            absence_type=item.get("absence_type", ""),
            contradiction_note=item.get("contradiction_note", ""),
            required_fix=item.get("required_fix", ""),
            jurisdiction=item.get("jurisdiction", payload.get("jurisdiction", "")),
            temporal_note=item.get("temporal_note", ""),
        )
        for item in payload.get("findings", [])
    ]
    return packet


def _sync_claims_and_citations(claims, citations, draft):
    unit_by_claim_id = {unit.unit_id.replace("unit", "claim"): unit for unit in draft.units if unit.is_claim}
    synced_claims = []
    for claim in claims:
        unit = unit_by_claim_id[claim.claim_id]
        synced_claims.append(
            type(claim)(
                claim_id=claim.claim_id,
                report_section=claim.report_section,
                exact_text_span=unit.text,
                normalized_claim=claim.normalized_claim,
                claim_kind=claim.claim_kind,
                risk_level=claim.risk_level,
                source_ids=claim.source_ids,
                source_roles=claim.source_roles,
                evidence_count=claim.evidence_count,
                required_source_role=claim.required_source_role,
                required_role_matched=claim.required_role_matched,
                role_fit_status=claim.role_fit_status,
                support_status=claim.support_status,
                confidence=claim.confidence,
                caveat_required=claim.caveat_required,
                suggested_tone=claim.suggested_tone,
                required_fix=claim.required_fix,
                origin_finding_id=claim.origin_finding_id,
                absence_type=claim.absence_type,
                contradiction_note=claim.contradiction_note,
                included_in_report=unit.include_in_report,
                exclusion_reason=unit.exclusion_reason,
            )
        )

    claim_lookup = {claim.claim_id: claim for claim in synced_claims}
    deduped: dict[tuple[str, str, str, str], CitationLedgerRow] = {}
    index = 1
    for citation in citations:
        claim = claim_lookup[citation.claim_id]
        key = (citation.claim_id, citation.source_id, citation.source_role, citation.source_title)
        deduped[key] = CitationLedgerRow(
            citation_id=f"citation-{index:03d}",
            claim_id=citation.claim_id,
            report_section=claim.report_section,
            source_id=citation.source_id,
            source_role=citation.source_role,
            source_title=citation.source_title,
            support_status=claim.support_status,
            included_in_report=claim.included_in_report,
            origin_finding_id=claim.origin_finding_id,
        )
        index += 1
    return synced_claims, list(deduped.values())


def _build_metrics(request, budget, evidence, draft, claims, citations, report_text):
    included_claims = [claim for claim in claims if claim.included_in_report]
    excluded_claims = [claim for claim in claims if not claim.included_in_report]
    high_risk_claims = [claim for claim in claims if claim.risk_level == "high"]
    included_high_risk_claims = [claim for claim in included_claims if claim.risk_level == "high"]
    supported_claims = [claim for claim in claims if claim.support_status == "supported"]
    high_risk_supported = [claim for claim in high_risk_claims if claim.support_status == "supported"]
    weak_claims = [claim for claim in claims if claim.support_status == "weak"]
    missing_claims = [claim for claim in claims if claim.support_status == "missing"]
    out_of_scope_claims = [claim for claim in claims if claim.support_status == "out_of_scope"]
    included_citations = [citation for citation in citations if citation.included_in_report]
    rendered_entries = _rendered_report_entries(report_text)
    rendered_claim_entries = {(item["section"], item["text"]) for item in rendered_entries}
    matched_included_claims = [claim for claim in included_claims if (claim.report_section, claim.exact_text_span) in rendered_claim_entries]
    matched_high_risk_claims = [
        claim for claim in included_high_risk_claims if (claim.report_section, claim.exact_text_span) in rendered_claim_entries
    ]

    valid_source_ids = {source.source_id for source in evidence.sources}
    title_lookup = {source.source_id: source.title for source in evidence.sources}
    role_lookup = {source.source_id: source.source_role for source in evidence.sources}
    included_claim_source_ids = {source_id for claim in included_claims for source_id in claim.source_ids}
    expected_included_citation_tuples = {
        (claim.claim_id, source_id, role_lookup.get(source_id, "unknown"), title_lookup.get(source_id, source_id))
        for claim in included_claims
        for source_id in claim.source_ids
    }
    actual_included_citation_tuples = {
        (citation.claim_id, citation.source_id, citation.source_role, citation.source_title)
        for citation in included_citations
    }
    rendered_source_refs = {ref for item in rendered_entries for ref in item["refs"]}
    citation_trace_consistent = (
        expected_included_citation_tuples == actual_included_citation_tuples
        and included_claim_source_ids <= valid_source_ids
        and all(citation.source_id in valid_source_ids for citation in included_citations)
    )
    rendered_citation_trace_consistent = (
        rendered_source_refs == {citation.source_id for citation in included_citations}
        and rendered_source_refs <= valid_source_ids
    )
    citation_trace_mismatch_count = len(expected_included_citation_tuples ^ actual_included_citation_tuples)
    rendered_trace_mismatch_count = len(rendered_source_refs ^ {citation.source_id for citation in included_citations})
    metadata_consistent = (
        all(citation.source_id in valid_source_ids for citation in citations)
        and all(citation.claim_id in {claim.claim_id for claim in claims} for citation in citations)
        and citation_trace_consistent
        and rendered_citation_trace_consistent
    )
    document_grounding_present = any(citation.source_role == "user_provided_source" for citation in included_citations)

    source_finding_ids = {finding.finding_id for finding in evidence.findings}
    captured_source_finding_ids = {claim.origin_finding_id for claim in claims if claim.origin_finding_id}
    source_finding_ledger_coverage_ratio = round(
        (len(captured_source_finding_ids & source_finding_ids) / len(source_finding_ids)) if source_finding_ids else 1.0,
        2,
    )

    report_claim_capture_ratio = round(
        (len(matched_included_claims) / len(included_claims)) if included_claims else 1.0,
        2,
    )
    high_risk_claim_capture_ratio = round(
        (len(matched_high_risk_claims) / len(included_high_risk_claims)) if included_high_risk_claims else 1.0,
        2,
    )
    target_results = {
        "min_sources": len({citation.source_id for citation in included_citations}) >= budget.target_profile.min_sources,
        "min_citations": len(included_citations) >= budget.target_profile.min_citations,
        "min_report_claim_capture_ratio": report_claim_capture_ratio >= budget.target_profile.min_report_claim_capture_ratio,
    }
    target_misses = [key for key, passed in target_results.items() if not passed]
    waiver_hits = set(budget.waivers)
    target_miss_without_waiver = any(target not in waiver_hits for target in target_misses)

    return {
        "requested_mode": budget.requested_mode,
        "effective_mode": budget.effective_mode,
        "preset_baseline_budget": budget.preset_baseline_budget,
        "effective_budget": budget.effective_budget,
        "override_reason": budget.override_reason,
        "override_authority": budget.override_authority,
        "full_dr_equivalent": budget.full_dr_equivalent,
        "report_status_implication": budget.report_status_implication,
        "limitations": budget.limitations,
        "report_claim_capture_ratio": report_claim_capture_ratio,
        "supported_claim_ratio": round((len(supported_claims) / len(claims)) if claims else 1.0, 2),
        "high_risk_claim_capture_ratio": high_risk_claim_capture_ratio,
        "high_risk_supported_claim_ratio": round((len(high_risk_supported) / len(high_risk_claims)) if high_risk_claims else 1.0, 2),
        "weak_claim_ratio": round((len(weak_claims) / len(claims)) if claims else 0.0, 2),
        "missing_claim_ratio": round((len(missing_claims) / len(claims)) if claims else 0.0, 2),
        "out_of_scope_claim_ratio": round((len(out_of_scope_claims) / len(claims)) if claims else 0.0, 2),
        "unsupported_high_risk_count": len([claim for claim in high_risk_claims if claim.support_status != "supported"]),
        "unsupported_high_risk_absence_count": len(
            [
                claim
                for claim in claims
                if claim.risk_level == "high"
                and claim.claim_kind == "absence"
                and claim.support_status != "supported"
            ]
        ),
        "claim_count": len(claims),
        "included_claim_count": len(included_claims),
        "excluded_claim_count": len(excluded_claims),
        "citation_count": len(citations),
        "included_citation_count": len(included_citations),
        "source_finding_count": len(source_finding_ids),
        "captured_source_finding_count": len(captured_source_finding_ids),
        "source_finding_ledger_coverage_ratio": source_finding_ledger_coverage_ratio,
        "reader_decision_layer_present": any(unit.section_key == "decision_layer" and unit.include_in_report for unit in draft.units),
        "uncertainty_section_present": any(unit.section_key == "uncertainty" and unit.include_in_report for unit in draft.units),
        "metadata_consistent": metadata_consistent,
        "citation_trace_consistent": citation_trace_consistent,
        "rendered_citation_trace_consistent": rendered_citation_trace_consistent,
        "citation_trace_mismatch_count": citation_trace_mismatch_count + rendered_trace_mismatch_count,
        "document_grounding_present": document_grounding_present,
        "internal_heading_present": any(
            any(fragment in unit.section_title.lower() for fragment in INTERNAL_HEADING_FRAGMENTS)
            for unit in draft.units
            if unit.include_in_report
        ),
        "target_results": target_results,
        "target_misses": target_misses,
        "target_miss_without_waiver": target_miss_without_waiver,
        "synthetic_inputs": request.evidence_mode == "synthetic",
        "synthetic_complete_allowed": request.release_contract.allow_synthetic_complete,
        "release_status_candidate": "pending",
    }


def _rendered_report_entries(report_text: str) -> list[dict]:
    section = ""
    entries: list[dict] = []
    for raw_line in report_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            section = line[3:]
            continue
        if not line.startswith("- "):
            continue
        body = line[2:].strip()
        refs = re.findall(r"\[([^\]]+)\]", body)
        text = re.sub(r"(?:\s+\[[^\]]+\])+$", "", body).strip()
        if section == "Sources":
            continue
        entries.append({"section": section, "text": text, "refs": refs})
    return entries


def _domain_adapter_to_payload(adapter) -> dict:
    return {
        "topic": adapter.topic,
        "reader": adapter.reader,
        "use_context": adapter.use_context,
        "output_type": adapter.output_type,
        "risk_tier": adapter.risk_tier,
        "temporal_sensitivity": adapter.temporal_sensitivity,
        "jurisdiction_sensitivity": adapter.jurisdiction_sensitivity,
        "source_priority": adapter.source_priority,
        "high_risk_claim_types": adapter.high_risk_claim_types,
        "likely_failure_modes": adapter.likely_failure_modes,
        "domain_specific_risks": adapter.domain_specific_risks,
        "common_misunderstandings": adapter.common_misunderstandings,
        "boundary_concepts": adapter.boundary_concepts,
        "decision_context": {
            "primary_decision": adapter.decision_context.primary_decision,
            "failure_cost": adapter.decision_context.failure_cost,
            "time_horizon": adapter.decision_context.time_horizon,
            "reader_action": adapter.decision_context.reader_action,
        },
        "required_decision_layer": adapter.required_decision_layer,
        "required_tables": adapter.required_tables,
        "must_not_overgeneralize": adapter.must_not_overgeneralize,
        "known_limits": adapter.known_limits,
        "source_roles_required_by_claim_kind": adapter.source_roles_required_by_claim_kind,
    }


def _claim_rows(claims):
    return [
        {
            "claim_id": claim.claim_id,
            "report_section": claim.report_section,
            "exact_text_span": claim.exact_text_span,
            "normalized_claim": claim.normalized_claim,
            "claim_kind": claim.claim_kind,
            "risk_level": claim.risk_level,
            "source_ids": claim.source_ids,
            "source_roles": claim.source_roles,
            "evidence_count": claim.evidence_count,
            "required_source_role": claim.required_source_role,
            "required_role_matched": claim.required_role_matched,
            "role_fit_status": claim.role_fit_status,
            "support_status": claim.support_status,
            "confidence": claim.confidence,
            "caveat_required": claim.caveat_required,
            "suggested_tone": claim.suggested_tone,
            "required_fix": claim.required_fix,
            "origin_finding_id": claim.origin_finding_id,
            "included_in_report": claim.included_in_report,
            "exclusion_reason": claim.exclusion_reason,
        }
        for claim in claims
    ]


def _citation_rows(citations):
    return [
        {
            "citation_id": citation.citation_id,
            "claim_id": citation.claim_id,
            "report_section": citation.report_section,
            "source_id": citation.source_id,
            "source_role": citation.source_role,
            "source_title": citation.source_title,
            "support_status": citation.support_status,
            "included_in_report": citation.included_in_report,
            "origin_finding_id": citation.origin_finding_id,
        }
        for citation in citations
    ]


def _package_root() -> Path:
    return package_root(Path(__file__))
