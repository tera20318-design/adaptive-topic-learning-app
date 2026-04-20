from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from cleanroom_runtime.models import PipelineBundle
from cleanroom_runtime.utils import write_json, write_text, write_tsv


def render_bundle(bundle: PipelineBundle, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_text(output_dir / "final_report.md", _render_report(bundle))
    write_text(output_dir / "domain-adapter.md", _render_adapter(bundle))
    write_text(output_dir / "release-gate-summary.md", _render_release_summary(bundle))
    write_json(output_dir / "metrics.json", bundle.metrics.to_dict())
    write_json(output_dir / "bundle.json", bundle.to_dict())
    write_tsv(output_dir / "claim-ledger.tsv", _claim_headers(), _claim_rows(bundle.claims))
    write_tsv(output_dir / "included-claims.tsv", _claim_headers(), _claim_rows([claim for claim in bundle.claims if claim.included_in_report]))
    write_tsv(output_dir / "excluded-claims.tsv", _claim_headers(), _claim_rows([claim for claim in bundle.claims if not claim.included_in_report]))
    write_tsv(output_dir / "citation-ledger.tsv", _citation_headers(), _citation_rows(bundle))
    write_tsv(output_dir / "gate-issues.tsv", _gate_issue_headers(), _gate_issue_rows(bundle))
    packet_audit = _packet_ingestion_audit(bundle)
    if packet_audit:
        write_json(output_dir / "packet-ingestion-audit.json", packet_audit)
        write_tsv(output_dir / "packet-ingestion-audit.tsv", _packet_audit_headers(), _packet_audit_rows(packet_audit))


def _render_report(bundle: PipelineBundle) -> str:
    lines = [f"# {bundle.request.topic}", ""]
    for section in bundle.draft.sections:
        lines.append(f"## {section.title}")
        lines.append("")
        section_units = [unit for unit in bundle.draft.units if unit.section_key == section.key and unit.include_in_report]
        if not section_units:
            lines.append("- No releasable material was available for this section.")
            lines.append("")
            continue
        for unit in section_units:
            citation_text = ""
            if unit.source_ids:
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
        f"- risk_tier: {adapter.risk_tier}",
        f"- source_priority: {', '.join(adapter.source_priority)}",
        f"- high_risk_claim_types: {', '.join(adapter.high_risk_claim_types)}",
        f"- likely_failure_modes: {', '.join(adapter.likely_failure_modes)}",
        f"- common_misunderstandings: {', '.join(adapter.common_misunderstandings)}",
        f"- boundary_concepts: {', '.join(adapter.boundary_concepts)}",
        f"- required_tables: {', '.join(adapter.required_tables)}",
        "",
    ]
    return "\n".join(lines)


def _render_release_summary(bundle: PipelineBundle) -> str:
    lines = [
        "# Release Gate Summary",
        "",
        f"- Status: `{bundle.release_gate.status}`",
        f"- Contract complete: `{str(bundle.release_gate.contract_complete).lower()}`",
        f"- Research completeness: `{bundle.release_gate.research_completeness}`",
        "",
        "## Reasons",
        "",
    ]
    if bundle.release_gate.reasons:
        lines.extend(f"- {reason}" for reason in bundle.release_gate.reasons)
    else:
        lines.append("- None")
    lines.extend(["", "## Blocking Reasons", ""])
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


def _claim_headers() -> list[str]:
    return [
        "claim_id",
        "unit_id",
        "origin_finding_ids",
        "report_section",
        "report_section_key",
        "report_span_id",
        "normalized_claim",
        "report_line_start",
        "report_line_end",
        "claim_span_start",
        "claim_span_end",
        "trace_status",
        "claim_kind",
        "risk_level",
        "support_status",
        "included_in_report",
        "audit_display_state",
        "source_ids",
        "source_roles",
        "required_source_roles",
        "matched_source_roles",
        "finding_span_labels",
        "finding_span_starts",
        "finding_span_ends",
        "grounding_marker",
        "grounding_scope_note",
        "blocking_reasons",
        "exclusion_reasons",
        "required_fix",
        "exact_text_span",
    ]


def _claim_rows(claims) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for claim in claims:
        rows.append(
            {
                "claim_id": claim.claim_id,
                "unit_id": claim.unit_id,
                "origin_finding_ids": claim.origin_finding_ids,
                "report_section": claim.report_section,
                "report_section_key": claim.report_section_key,
                "report_span_id": claim.report_span_id,
                "normalized_claim": claim.normalized_claim,
                "report_line_start": claim.report_line_start,
                "report_line_end": claim.report_line_end,
                "claim_span_start": claim.claim_span_start,
                "claim_span_end": claim.claim_span_end,
                "trace_status": claim.trace_status,
                "claim_kind": claim.claim_kind,
                "risk_level": claim.risk_level,
                "support_status": claim.support_status,
                "included_in_report": str(claim.included_in_report).lower(),
                "audit_display_state": claim.audit_display_state,
                "source_ids": claim.source_ids,
                "source_roles": claim.source_roles,
                "required_source_roles": claim.required_source_roles,
                "matched_source_roles": claim.matched_source_roles,
                "finding_span_labels": claim.finding_span_labels,
                "finding_span_starts": claim.finding_span_starts,
                "finding_span_ends": claim.finding_span_ends,
                "grounding_marker": claim.grounding_marker,
                "grounding_scope_note": claim.grounding_scope_note,
                "blocking_reasons": claim.blocking_reasons,
                "exclusion_reasons": claim.exclusion_reasons,
                "required_fix": claim.required_fix,
                "exact_text_span": claim.exact_text_span,
            }
        )
    return rows


def _citation_headers() -> list[str]:
    return [
        "citation_id",
        "claim_id",
        "report_section",
        "report_span_id",
        "claim_span_start",
        "claim_span_end",
        "source_id",
        "source_role",
        "source_title",
        "source_finding_ids",
        "source_excerpt",
        "source_span_label",
        "source_span_start",
        "source_span_end",
        "source_span_labels",
        "source_span_starts",
        "source_span_ends",
        "grounding_marker",
        "grounding_scope_note",
        "trace_status",
        "provenance_complete",
        "support_status",
        "included_in_report",
    ]


def _citation_rows(bundle: PipelineBundle) -> list[dict[str, object]]:
    return [
        asdict(citation)
        | {
            "included_in_report": str(citation.included_in_report).lower(),
            "provenance_complete": str(citation.provenance_complete).lower(),
        }
        for citation in bundle.citations
    ]


def _gate_issue_headers() -> list[str]:
    return ["reason_id", "claim_id", "stage", "severity", "blocks_release", "message", "required_fix"]


def _gate_issue_rows(bundle: PipelineBundle) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for issue in bundle.release_gate.claim_issues:
        rows.append(
            {
                "reason_id": issue.reason_id,
                "claim_id": issue.claim_id,
                "stage": issue.stage,
                "severity": issue.severity,
                "blocks_release": str(issue.blocks_release).lower(),
                "message": issue.message,
                "required_fix": issue.required_fix,
            }
        )
    return rows


def _packet_ingestion_audit(bundle: PipelineBundle) -> dict[str, object]:
    for snapshot in bundle.stage_snapshots:
        stage = getattr(snapshot, "stage", "")
        artifact_type = getattr(snapshot, "artifact_type", "")
        summary = getattr(snapshot, "summary", {})
        if artifact_type == "packet_ingestion_audit" and isinstance(summary, dict):
            return summary

    if bundle.request is None:
        return {}
    packet_summaries = []
    for index, packet in enumerate(bundle.request.source_packets):
        disposition = "salvaged" if (packet.provenance.partial or packet.provenance.malformed) else "accepted"
        packet_summaries.append(
            {
                "packet_index": index,
                "source_id": packet.source_id,
                "title": packet.title,
                "disposition": disposition,
                "stale": packet.provenance.stale,
                "partial": packet.provenance.partial,
                "malformed": packet.provenance.malformed,
                "dedupe_key": packet.provenance.dedupe_key,
                "dedupe_collision_with": list(packet.provenance.dedupe_parent_ids),
                "quality_flags": list(packet.quality_flags),
                "issue_codes": [],
                "issue_messages": list(packet.provenance.trace_notes),
            }
        )
    if not packet_summaries:
        return {}
    return {
        "input_count": len(packet_summaries),
        "accepted_count": len(packet_summaries),
        "rejected_count": 0,
        "salvaged_count": sum(1 for item in packet_summaries if item["disposition"] == "salvaged"),
        "stale_count": sum(1 for item in packet_summaries if item["stale"]),
        "dedupe_collision_count": sum(1 for item in packet_summaries if item["dedupe_collision_with"]),
        "blocking_issue_count": 0,
        "issue_count": 0,
        "packet_summaries": packet_summaries,
    }


def _packet_audit_headers() -> list[str]:
    return [
        "packet_index",
        "source_id",
        "title",
        "disposition",
        "stale",
        "partial",
        "malformed",
        "dedupe_key",
        "dedupe_collision_with",
        "quality_flags",
        "issue_codes",
        "issue_messages",
    ]


def _packet_audit_rows(packet_audit: dict[str, object]) -> list[dict[str, object]]:
    summaries = packet_audit.get("packet_summaries", [])
    if not isinstance(summaries, list):
        return []
    rows: list[dict[str, object]] = []
    for summary in summaries:
        if not isinstance(summary, dict):
            continue
        rows.append(
            {
                "packet_index": summary.get("packet_index", ""),
                "source_id": summary.get("source_id", ""),
                "title": summary.get("title", ""),
                "disposition": summary.get("disposition", ""),
                "stale": str(bool(summary.get("stale", False))).lower(),
                "partial": str(bool(summary.get("partial", False))).lower(),
                "malformed": str(bool(summary.get("malformed", False))).lower(),
                "dedupe_key": summary.get("dedupe_key", ""),
                "dedupe_collision_with": summary.get("dedupe_collision_with", []),
                "quality_flags": summary.get("quality_flags", []),
                "issue_codes": summary.get("issue_codes", []),
                "issue_messages": summary.get("issue_messages", []),
            }
        )
    return rows
