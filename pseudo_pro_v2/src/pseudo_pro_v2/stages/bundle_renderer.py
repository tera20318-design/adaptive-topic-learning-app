from __future__ import annotations

from pathlib import Path

from pseudo_pro_v2.models import PipelineBundle
from pseudo_pro_v2.utils import write_json, write_text, write_tsv


def render_bundle(bundle: PipelineBundle, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_text(output_dir / "final_report.md", render_report_markdown(bundle.request.topic, bundle.draft.sections, bundle.draft.units))
    write_text(output_dir / "domain-adapter.md", _render_adapter(bundle))
    write_json(output_dir / "metrics.json", bundle.metrics)
    write_text(output_dir / "release-gate-summary.md", _render_release_summary(bundle))
    write_tsv(output_dir / "claim-ledger.tsv", _claim_headers(), _claim_rows(bundle))
    write_tsv(output_dir / "citation-ledger.tsv", _citation_headers(), _citation_rows(bundle))


def render_report_markdown(title: str, sections, units) -> str:
    lines = [f"# {title}", ""]
    for section in sections:
        lines.append(f"## {section.title}")
        lines.append("")
        section_units = [unit for unit in units if unit.section_key == section.key and unit.include_in_report]
        if not section_units:
            lines.append("- No supported material was available for this section.")
            lines.append("")
            continue
        for unit in section_units:
            citation_text = ""
            if unit.is_claim and unit.source_ids:
                citation_text = " " + " ".join(f"[{source_id}]" for source_id in unit.source_ids)
            lines.append(f"- {unit.text}{citation_text}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def _render_adapter(bundle: PipelineBundle) -> str:
    adapter = bundle.adapter
    lines = [
        "# Domain Adapter",
        "",
        f"- topic: {adapter.topic}",
        f"- reader: {adapter.reader}",
        f"- use_context: {adapter.use_context}",
        f"- output_type: {adapter.output_type}",
        f"- risk_tier: {adapter.risk_tier}",
        f"- temporal_sensitivity: {adapter.temporal_sensitivity}",
        f"- jurisdiction_sensitivity: {adapter.jurisdiction_sensitivity}",
        f"- source_priority: {', '.join(adapter.source_priority)}",
        f"- high_risk_claim_types: {', '.join(adapter.high_risk_claim_types)}",
        f"- likely_failure_modes: {', '.join(adapter.likely_failure_modes)}",
        f"- domain_specific_risks: {', '.join(adapter.domain_specific_risks)}",
        f"- common_misunderstandings: {', '.join(adapter.common_misunderstandings)}",
        f"- boundary_concepts: {', '.join(adapter.boundary_concepts)}",
        f"- decision_context.primary_decision: {adapter.decision_context.primary_decision}",
        f"- decision_context.failure_cost: {adapter.decision_context.failure_cost}",
        f"- decision_context.time_horizon: {adapter.decision_context.time_horizon}",
        f"- decision_context.reader_action: {adapter.decision_context.reader_action}",
        f"- required_decision_layer: {', '.join(adapter.required_decision_layer)}",
        f"- required_tables: {', '.join(adapter.required_tables)}",
        f"- must_not_overgeneralize: {', '.join(adapter.must_not_overgeneralize)}",
        f"- known_limits: {', '.join(adapter.known_limits)}",
        "",
    ]
    return "\n".join(lines)


def _render_release_summary(bundle: PipelineBundle) -> str:
    scoped_note = ""
    if not bundle.budget.full_dr_equivalent:
        scoped_note = " (scoped run; not full Deep Research equivalent)"
    lines = [
        "# Release Gate Summary",
        "",
        f"- Status: `{bundle.release_gate.status}`{scoped_note}",
        f"- Reasons: {'; '.join(bundle.release_gate.reasons) if bundle.release_gate.reasons else 'None'}",
        f"- Full DR equivalent: `{str(bundle.budget.full_dr_equivalent).lower()}`",
        f"- Report status implication: {bundle.budget.report_status_implication}",
        f"- Included claims: `{bundle.metrics.get('included_claim_count', 0)}` / all claims: `{bundle.metrics.get('claim_count', 0)}`",
        f"- Unsupported high-risk claims: `{bundle.metrics.get('unsupported_high_risk_count', 0)}`",
        "",
        "## Blocking Reasons",
        "",
    ]
    if bundle.release_gate.blocking_reasons:
        lines.extend(f"- {reason}" for reason in bundle.release_gate.blocking_reasons)
    else:
        lines.append("- None")
    lines.extend(["", "## Unresolved Gaps", ""])
    if bundle.release_gate.unresolved_gaps:
        lines.extend(f"- {gap}" for gap in bundle.release_gate.unresolved_gaps)
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def _claim_headers():
    return [
        "claim_id",
        "report_section",
        "exact_text_span",
        "normalized_claim",
        "claim_kind",
        "risk_level",
        "source_ids",
        "source_roles",
        "evidence_count",
        "required_source_role",
        "required_role_matched",
        "role_fit_status",
        "support_status",
        "confidence",
        "caveat_required",
        "suggested_tone",
        "required_fix",
        "origin_finding_id",
        "included_in_report",
        "exclusion_reason",
    ]


def _claim_rows(bundle: PipelineBundle):
    rows = []
    for claim in bundle.claims:
        rows.append(
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
                "required_role_matched": str(claim.required_role_matched).lower(),
                "role_fit_status": claim.role_fit_status,
                "support_status": claim.support_status,
                "confidence": claim.confidence,
                "caveat_required": str(claim.caveat_required).lower(),
                "suggested_tone": claim.suggested_tone,
                "required_fix": claim.required_fix,
                "origin_finding_id": claim.origin_finding_id,
                "included_in_report": str(claim.included_in_report).lower(),
                "exclusion_reason": claim.exclusion_reason,
            }
        )
    return rows


def _citation_headers():
    return [
        "citation_id",
        "claim_id",
        "report_section",
        "source_id",
        "source_role",
        "source_title",
        "support_status",
        "included_in_report",
        "origin_finding_id",
    ]


def _citation_rows(bundle: PipelineBundle):
    rows = []
    for citation in bundle.citations:
        rows.append(
            {
                "citation_id": citation.citation_id,
                "claim_id": citation.claim_id,
                "report_section": citation.report_section,
                "source_id": citation.source_id,
                "source_role": citation.source_role,
                "source_title": citation.source_title,
                "support_status": citation.support_status,
                "included_in_report": str(citation.included_in_report).lower(),
                "origin_finding_id": citation.origin_finding_id,
            }
        )
    return rows
