from __future__ import annotations

from collections import Counter

from cleanroom_runtime.ingestion import document_packets_from_raw_documents
from cleanroom_runtime.ingestion_boundary import normalize_source_packets, packet_integrity_notes
from cleanroom_runtime.models import CollectedEvidence, RunRequest, SourceFinding


def ingest_evidence(request: RunRequest) -> CollectedEvidence:
    findings: list[SourceFinding] = []
    source_counts: Counter[str] = Counter()
    quality_notes: list[str] = []
    inbound_packets = [*request.source_packets, *document_packets_from_raw_documents(request.raw_documents)]
    normalized_sources = normalize_source_packets(inbound_packets)

    for source in normalized_sources:
        source_counts[source.source_role] += 1
        for quality_flag in packet_integrity_notes(source):
            quality_notes.append(f"{source.source_id}: {quality_flag}")
        for finding in source.findings:
            findings.append(
                SourceFinding(
                    finding_id=finding.finding_id,
                    statement=finding.statement,
                    claim_kind=finding.claim_kind,
                    risk_level=finding.risk_level,
                    section_hint=finding.section_hint,
                    support_status_hint=finding.support_status_hint,
                    confidence=finding.confidence,
                    source_ids=finding.source_ids or [source.source_id],
                    decision_note=finding.decision_note,
                    caveat=finding.caveat,
                    scope_note=finding.scope_note,
                    contradiction_note=finding.contradiction_note,
                    required_fix=finding.required_fix,
                    jurisdiction=finding.jurisdiction or source.jurisdiction,
                    temporal_note=finding.temporal_note,
                    tags=list(finding.tags),
                    source_excerpt=finding.source_excerpt,
                    source_span_label=finding.source_span_label,
                    source_span_start=finding.source_span_start,
                    source_span_end=finding.source_span_end,
                    source_span_labels=list(finding.source_span_labels),
                    source_span_starts=list(finding.source_span_starts),
                    source_span_ends=list(finding.source_span_ends),
                    grounding_kind=finding.grounding_kind,
                    grounding_marker=finding.grounding_marker,
                    grounding_scope_note=finding.grounding_scope_note,
                    subject_key=finding.subject_key,
                    subject_scope_key=finding.subject_scope_key,
                    source_trust_note=finding.source_trust_note,
                    source_roles=list(finding.source_roles),
                    absence_type=finding.absence_type,
                    absence_scope=finding.absence_scope,
                )
            )

    return CollectedEvidence(
        sources=normalized_sources,
        findings=findings,
        source_counts_by_role=dict(source_counts),
        quality_notes=quality_notes,
    )
