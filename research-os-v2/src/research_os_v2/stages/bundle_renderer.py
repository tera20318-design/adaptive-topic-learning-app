from __future__ import annotations

from pathlib import Path

from research_os_v2.models import PipelineBundle
from research_os_v2.utils import write_json, write_text, write_tsv


def render_bundle(bundle: PipelineBundle, output_dir: Path) -> None:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    final_report = render_report_markdown(bundle)
    write_text(output_dir / "final_report.md", final_report)
    write_json(output_dir / "metrics.json", bundle.metrics)
    write_text(output_dir / "release-gate-summary.md", render_release_gate(bundle))
    write_text(output_dir / "domain-adapter.md", render_domain_adapter(bundle))
    write_tsv(output_dir / "source-log.tsv", source_log_headers(), source_log_rows(bundle))
    write_tsv(output_dir / "citation-ledger.tsv", citation_headers(), citation_rows(bundle))
    write_tsv(output_dir / "claim-ledger.tsv", claim_headers(), claim_rows(bundle))
    write_text(output_dir / "contradiction-log.md", render_contradictions(bundle))
    write_text(output_dir / "evidence-gap-log.md", render_gaps(bundle))
    write_text(output_dir / "uncertainty-and-scope.md", render_uncertainty_scope(bundle))


def render_report_markdown(bundle: PipelineBundle) -> str:
    lines = [f"# {bundle.request.topic}", ""]
    for section in bundle.draft.sections:
        lines.append(f"## {section.title}")
        lines.append("")
        for unit in [item for item in bundle.draft.units if item.section_key == section.key]:
            citation_text = ""
            if unit.source_ids:
                citation_text = " " + " ".join(f"[{source_id}]" for source_id in unit.source_ids)
            lines.append(f"- {unit.text}{citation_text}")
        if not any(item.section_key == section.key for item in bundle.draft.units):
            lines.append("- No supported material was available for this section.")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_release_gate(bundle: PipelineBundle) -> str:
    lines = [
        "# Release Gate Summary",
        "",
        f"- Status: `{bundle.release_gate.status}`",
        f"- Reasons: {'; '.join(bundle.release_gate.reasons) if bundle.release_gate.reasons else 'None'}",
        f"- Metadata consistent: `{str(bundle.release_gate.metadata_consistent).lower()}`",
        "",
        "## Blocking Reasons",
        "",
    ]
    if bundle.release_gate.blocking_reasons:
        for reason in bundle.release_gate.blocking_reasons:
            lines.append(f"- {reason}")
    else:
        lines.append("- None")
    lines.extend(["", "## Unresolved Gaps", ""])
    if bundle.release_gate.unresolved_gaps:
        for gap in bundle.release_gate.unresolved_gaps:
            lines.append(f"- {gap}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def render_domain_adapter(bundle: PipelineBundle) -> str:
    adapter = bundle.adapter
    pairs = {
        "topic": adapter.topic,
        "reader": adapter.reader,
        "use_context": adapter.use_context,
        "output_type": adapter.output_type,
        "risk_tier": adapter.risk_tier,
        "temporal_sensitivity": adapter.temporal_sensitivity,
        "jurisdiction_sensitivity": adapter.jurisdiction_sensitivity,
        "source_priority": ", ".join(adapter.source_priority),
        "high_risk_claim_types": ", ".join(adapter.high_risk_claim_types),
        "domain_specific_risks": ", ".join(adapter.domain_specific_risks),
        "likely_failure_modes": ", ".join(adapter.likely_failure_modes),
        "common_misunderstandings": ", ".join(adapter.common_misunderstandings),
        "boundary_concepts": ", ".join(adapter.boundary_concepts),
        "required_decision_layer": ", ".join(adapter.required_decision_layer),
        "required_tables": ", ".join(adapter.required_tables),
        "must_not_overgeneralize": ", ".join(adapter.must_not_overgeneralize),
        "known_limits": ", ".join(adapter.known_limits),
    }
    lines = ["# Domain Adapter", ""]
    for key, value in pairs.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    return "\n".join(lines)


def render_contradictions(bundle: PipelineBundle) -> str:
    lines = ["# Contradiction Log", ""]
    if not bundle.contradictions:
        lines.append("- No contradictions were logged.")
    else:
        for item in bundle.contradictions:
            lines.append(f"- {item.claim_id}: {item.issue_type} / {item.severity} / {item.detail} / {item.action}")
    lines.append("")
    return "\n".join(lines)


def render_gaps(bundle: PipelineBundle) -> str:
    lines = ["# Evidence Gap Log", ""]
    if not bundle.gaps:
        lines.append("- No evidence gaps were logged.")
    else:
        for item in bundle.gaps:
            lines.append(f"- {item.claim_id}: {item.gap_type} / {item.detail} / {item.required_fix}")
    lines.append("")
    return "\n".join(lines)


def render_uncertainty_scope(bundle: PipelineBundle) -> str:
    lines = [
        "# Uncertainty And Scope",
        "",
        f"- Requested mode: `{bundle.budget.requested_mode}`",
        f"- Effective mode: `{bundle.budget.effective_mode}`",
        f"- Full DR equivalent: `{str(bundle.budget.full_dr_equivalent).lower()}`",
        f"- Report status implication: {bundle.budget.report_status_implication}",
        "",
        "## Limitations",
        "",
    ]
    for limitation in bundle.budget.limitations + bundle.adapter.known_limits:
        lines.append(f"- {limitation}")
    if not (bundle.budget.limitations or bundle.adapter.known_limits):
        lines.append("- None recorded.")
    lines.append("")
    return "\n".join(lines)


def source_log_headers() -> list[str]:
    return [
        "source_id",
        "title",
        "citation",
        "source_role",
        "published_on",
        "jurisdiction",
        "quality_flags",
        "summary",
    ]


def source_log_rows(bundle: PipelineBundle):
    for source in bundle.evidence.sources:
        yield {
            "source_id": source.source_id,
            "title": source.title,
            "citation": source.citation or source.url,
            "source_role": source.source_role,
            "published_on": source.published_on,
            "jurisdiction": source.jurisdiction,
            "quality_flags": source.quality_flags,
            "summary": source.summary,
        }


def citation_headers() -> list[str]:
    return [
        "citation_id",
        "claim_id",
        "report_section",
        "source_id",
        "source_role",
        "source_title",
        "support_status",
    ]


def citation_rows(bundle: PipelineBundle):
    for row in bundle.citations:
        yield {
            "citation_id": row.citation_id,
            "claim_id": row.claim_id,
            "report_section": row.report_section,
            "source_id": row.source_id,
            "source_role": row.source_role,
            "source_title": row.source_title,
            "support_status": row.support_status,
        }


def claim_headers() -> list[str]:
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
        "support_status",
        "confidence",
        "caveat_required",
        "suggested_tone",
        "required_fix",
    ]


def claim_rows(bundle: PipelineBundle):
    for row in bundle.claims:
        yield {
            "claim_id": row.claim_id,
            "report_section": row.report_section,
            "exact_text_span": row.exact_text_span,
            "normalized_claim": row.normalized_claim,
            "claim_kind": row.claim_kind,
            "risk_level": row.risk_level,
            "source_ids": row.source_ids,
            "source_roles": row.source_roles,
            "evidence_count": row.evidence_count,
            "required_source_role": row.required_source_role,
            "support_status": row.support_status,
            "confidence": row.confidence,
            "caveat_required": str(row.caveat_required).lower(),
            "suggested_tone": row.suggested_tone,
            "required_fix": row.required_fix,
        }
