from __future__ import annotations

from pathlib import Path

from research_os_v2.input_loader import load_request
from research_os_v2.models import CitationLedgerRow, PipelineBundle
from research_os_v2.stages.bundle_renderer import render_bundle
from research_os_v2.stages.claim_extractor import extract_claims
from research_os_v2.stages.contradiction_absence_guard import apply_contradiction_and_absence_guard
from research_os_v2.stages.domain_adapter_generator import generate_domain_adapter
from research_os_v2.stages.draft_writer import write_initial_draft
from research_os_v2.stages.evidence_collector import collect_evidence
from research_os_v2.stages.evidence_mapper import map_claims_to_evidence
from research_os_v2.stages.intent_classifier import classify_intent
from research_os_v2.stages.release_gate import decide_release_gate
from research_os_v2.stages.report_planner import build_report_plan
from research_os_v2.stages.risk_tier_classifier import classify_risk_tier
from research_os_v2.stages.scope_budget_planner import plan_scope_and_budget
from research_os_v2.stages.source_strategy_builder import build_source_strategy
from research_os_v2.stages.tone_controller import apply_tone_control
from research_os_v2.utils import load_json


def run_pipeline(input_path: Path, output_dir: Path, *, as_of_date: str = "", render: bool = True) -> PipelineBundle:
    payload = load_json(input_path)
    return run_pipeline_from_payload(payload, output_dir=output_dir, as_of_date=as_of_date, render=render)


def run_pipeline_from_payload(
    payload: dict,
    *,
    output_dir: Path,
    as_of_date: str = "",
    render: bool = True,
) -> PipelineBundle:
    request = load_request(payload, as_of_date=as_of_date)
    intent = classify_intent(request)
    risk = classify_risk_tier(request)
    budget = plan_scope_and_budget(request, intent, risk)
    strategy = build_source_strategy(intent, risk)
    evidence = collect_evidence(request)
    adapter = generate_domain_adapter(request, intent, risk, budget, strategy, evidence)
    report_plan = build_report_plan(adapter)
    draft = write_initial_draft(request, adapter, evidence, report_plan)
    claims = extract_claims(draft, strategy)
    claims = map_claims_to_evidence(claims, draft)
    claims, contradictions, gaps = apply_contradiction_and_absence_guard(claims, draft, request)
    toned_draft = apply_tone_control(draft, claims)
    claims = _sync_claim_text_spans(claims, toned_draft)
    citations = _build_citation_ledger(claims, evidence)
    metrics = _build_metrics(request, budget, claims, citations, toned_draft, contradictions, gaps)
    release_gate = decide_release_gate(
        claims,
        gaps,
        metadata_consistent=metrics["metadata_consistent"],
        has_claim_ledger=bool(claims),
        has_citation_ledger=bool(citations),
        high_risk_absence_supported=metrics["unsupported_high_risk_absence_count"] == 0,
        reader_decision_layer_present=metrics["reader_decision_layer_present"],
        uncertainty_section_present=metrics["uncertainty_section_present"],
        scoped_run_honest=not (budget.effective_mode != "full" and budget.full_dr_equivalent),
    )
    bundle = PipelineBundle(
        request=request,
        intent=intent,
        risk=risk,
        budget=budget,
        strategy=strategy,
        adapter=adapter,
        evidence=evidence,
        draft=toned_draft,
        claims=claims,
        citations=citations,
        contradictions=contradictions,
        gaps=gaps,
        release_gate=release_gate,
        metrics=metrics | {"release_status": release_gate.status},
    )
    if render:
        render_bundle(bundle, output_dir)
    return bundle


def _sync_claim_text_spans(claims, draft):
    unit_by_claim_id = {
        unit.unit_id.replace("unit", "claim"): unit
        for unit in draft.units
    }
    synced = []
    for claim in claims:
        unit = unit_by_claim_id[claim.claim_id]
        synced.append(
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
                support_status=claim.support_status,
                confidence=claim.confidence,
                caveat_required=claim.caveat_required,
                suggested_tone=claim.suggested_tone,
                required_fix=claim.required_fix,
            )
        )
    return synced


def _build_citation_ledger(claims, evidence) -> list[CitationLedgerRow]:
    source_title_lookup = {source.source_id: source.title for source in evidence.sources}
    source_role_lookup = {source.source_id: source.source_role for source in evidence.sources}
    rows: list[CitationLedgerRow] = []
    index = 1
    for claim in claims:
        for source_id in claim.source_ids:
            rows.append(
                CitationLedgerRow(
                    citation_id=f"citation-{index:03d}",
                    claim_id=claim.claim_id,
                    report_section=claim.report_section,
                    source_id=source_id,
                    source_role=source_role_lookup.get(source_id, "unknown"),
                    source_title=source_title_lookup.get(source_id, source_id),
                    support_status=claim.support_status,
                )
            )
            index += 1
    return rows


def _build_metrics(request, budget, claims, citations, draft, contradictions, gaps):
    report_claim_count = len([unit for unit in draft.units if unit.is_claim and unit.section_key != "sources"])
    supported = [claim for claim in claims if claim.support_status == "supported"]
    weak = [claim for claim in claims if claim.support_status == "weak"]
    missing = [claim for claim in claims if claim.support_status == "missing"]
    out_of_scope = [claim for claim in claims if claim.support_status == "out_of_scope"]
    high_risk = [claim for claim in claims if claim.risk_level == "high"]
    high_risk_supported = [claim for claim in high_risk if claim.support_status == "supported"]
    high_risk_absence_unsupported = [
        claim for claim in high_risk
        if claim.claim_kind == "absence" and claim.support_status != "supported"
    ]
    cited_source_ids = {citation.source_id for citation in citations}
    metadata_consistent = all(source_id in cited_source_ids or not source_id for claim in claims for source_id in claim.source_ids)
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
        "report_claim_capture_ratio": round(len(claims) / report_claim_count, 2) if report_claim_count else 0.0,
        "supported_claim_ratio": round(len(supported) / len(claims), 2) if claims else 0.0,
        "high_risk_claim_capture_ratio": round(len(high_risk) / len(high_risk), 2) if high_risk else 1.0,
        "high_risk_supported_claim_ratio": round(len(high_risk_supported) / len(high_risk), 2) if high_risk else 1.0,
        "weak_claim_ratio": round(len(weak) / len(claims), 2) if claims else 0.0,
        "missing_claim_ratio": round(len(missing) / len(claims), 2) if claims else 0.0,
        "out_of_scope_claim_ratio": round(len(out_of_scope) / len(claims), 2) if claims else 0.0,
        "unsupported_high_risk_count": len([claim for claim in high_risk if claim.support_status != "supported"]),
        "unsupported_high_risk_absence_count": len(high_risk_absence_unsupported),
        "reader_decision_layer_present": any(unit.section_key == "decision_layer" for unit in draft.units),
        "uncertainty_section_present": any(unit.section_key == "uncertainty" for unit in draft.units),
        "metadata_consistent": metadata_consistent,
        "claim_count": len(claims),
        "citation_count": len(citations),
        "contradiction_count": len(contradictions),
        "gap_count": len(gaps),
        "as_of_date": request.as_of_date,
    }
