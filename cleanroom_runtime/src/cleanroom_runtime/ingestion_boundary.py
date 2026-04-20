from __future__ import annotations

from dataclasses import replace
from typing import Protocol

from cleanroom_runtime.models import RunRequest, SourcePacket, SourcePacketProvenance
from cleanroom_runtime.utils import normalize_text


class IngestionAdapter(Protocol):
    adapter_name: str

    def collect(self, request: RunRequest) -> list[SourcePacket]:
        ...


def normalize_source_packet(packet: SourcePacket) -> SourcePacket:
    provenance = packet.provenance
    canonical_url = provenance.canonical_url or packet.url
    canonical_id = provenance.canonical_id or packet.source_id
    dedupe_key = provenance.dedupe_key or _packet_dedupe_key(packet, canonical_url, canonical_id)
    packet_origin = provenance.packet_origin or "synthetic"
    grounding_status = provenance.grounding_status or "grounded"
    metadata_fields_present, metadata_missing_fields = _metadata_fields(packet)
    role_inference_status = provenance.role_inference_status or ("ambiguous" if packet.source_role == "unknown" else "declared")
    source_locator = provenance.source_locator or packet.url or packet.citation or packet.source_id
    normalized_provenance = replace(
        provenance,
        packet_origin=packet_origin,
        canonical_url=canonical_url,
        canonical_id=canonical_id,
        dedupe_key=dedupe_key,
        source_locator=source_locator,
        original_url=provenance.original_url or packet.url,
        normalized_at=provenance.normalized_at or provenance.collected_at or provenance.retrieved_at,
        metadata_fields_present=provenance.metadata_fields_present or metadata_fields_present,
        metadata_missing_fields=provenance.metadata_missing_fields or metadata_missing_fields,
        role_inference_status=role_inference_status,
        grounding_status=grounding_status,
    )
    normalized_findings = []
    for finding in packet.findings:
        source_ids = list(dict.fromkeys(finding.source_ids or [packet.source_id]))
        source_roles = list(dict.fromkeys(finding.source_roles or [packet.source_role]))
        source_excerpt = finding.source_excerpt or _default_source_excerpt(finding.statement, finding.grounding_kind)
        subject_key = finding.subject_key or normalize_text(source_excerpt or finding.statement)
        subject_scope_key = finding.subject_scope_key or normalize_text(
            "|".join(
                filter(
                    None,
                    [
                        subject_key,
                        finding.jurisdiction or packet.jurisdiction,
                        getattr(finding.absence_scope, "scope_label", ""),
                    ],
                )
            )
        )
        normalized_findings.append(
            replace(
                finding,
                source_ids=source_ids,
                source_roles=source_roles,
                source_excerpt=source_excerpt,
                subject_key=subject_key,
                subject_scope_key=subject_scope_key,
            )
        )
    return replace(
        packet,
        citation=packet.citation or packet.title,
        findings=normalized_findings,
        provenance=normalized_provenance,
    )


def normalize_source_packets(packets: list[SourcePacket]) -> list[SourcePacket]:
    merged_by_key: dict[str, SourcePacket] = {}
    for packet in packets:
        normalized = normalize_source_packet(packet)
        dedupe_key = normalized.provenance.dedupe_key or normalized.source_id
        existing = merged_by_key.get(dedupe_key)
        if existing is None:
            merged_by_key[dedupe_key] = normalized
            continue
        merged_by_key[dedupe_key] = _merge_packets(existing, normalized)
    return list(merged_by_key.values())


def packet_integrity_notes(packet: SourcePacket) -> list[str]:
    notes = list(packet.quality_flags)
    if not packet.provenance.metadata_consistent:
        notes.append("metadata inconsistency is present in this packet.")
    if not packet.provenance.citation_trace_complete:
        notes.append("citation trace is incomplete for this packet.")
    if packet.provenance.partial and packet.provenance.partial_reason:
        notes.append(f"partial evidence packet: {packet.provenance.partial_reason}")
    if packet.provenance.stale and packet.provenance.stale_reason:
        notes.append(f"stale source caution: {packet.provenance.stale_reason}")
    if packet.provenance.malformed and packet.provenance.malformed_reason:
        notes.append(f"malformed source caution: {packet.provenance.malformed_reason}")
    if packet.provenance.metadata_missing_fields:
        notes.append(
            "missing metadata fields: " + ", ".join(packet.provenance.metadata_missing_fields)
        )
    if packet.provenance.role_inference_status == "ambiguous":
        notes.append("source-role inference is ambiguous for this packet.")
    if packet.provenance.grounding_status == "ambiguous":
        notes.append("document grounding is ambiguous in this packet.")
    return list(dict.fromkeys(note for note in notes if note))


def _merge_packets(left: SourcePacket, right: SourcePacket) -> SourcePacket:
    merged_findings = list(left.findings)
    seen_finding_ids = {finding.finding_id for finding in merged_findings}
    for finding in right.findings:
        if finding.finding_id not in seen_finding_ids:
            merged_findings.append(finding)
            seen_finding_ids.add(finding.finding_id)

    merged_quality_flags = list(dict.fromkeys([*left.quality_flags, *right.quality_flags]))
    merged_trace_notes = list(dict.fromkeys([*left.provenance.trace_notes, *right.provenance.trace_notes]))
    merged_grounding_notes = list(dict.fromkeys([*left.provenance.grounding_notes, *right.provenance.grounding_notes]))
    merged_metadata_fields_present = list(
        dict.fromkeys([*left.provenance.metadata_fields_present, *right.provenance.metadata_fields_present])
    )
    merged_metadata_fields_missing = list(
        dict.fromkeys([*left.provenance.metadata_missing_fields, *right.provenance.metadata_missing_fields])
    )
    merged_normalization_errors = list(
        dict.fromkeys([*left.provenance.normalization_errors, *right.provenance.normalization_errors])
    )
    merged_dedupe_parent_ids = list(
        dict.fromkeys(
            [
                *left.provenance.dedupe_parent_ids,
                *right.provenance.dedupe_parent_ids,
                *(value for value in (left.source_id, right.source_id) if value and value != left.source_id),
            ]
        )
    )
    metadata_consistent = left.provenance.metadata_consistent and right.provenance.metadata_consistent
    citation_trace_complete = left.provenance.citation_trace_complete and right.provenance.citation_trace_complete
    partial = left.provenance.partial or right.provenance.partial
    partial_reason = left.provenance.partial_reason or right.provenance.partial_reason
    grounding_status = _grounding_status(left.provenance.grounding_status, right.provenance.grounding_status)
    published_on = max(left.published_on, right.published_on)
    stale = left.provenance.stale or right.provenance.stale
    malformed = left.provenance.malformed or right.provenance.malformed

    return replace(
        left,
        title=left.title or right.title,
        citation=left.citation or right.citation,
        url=left.url or right.url,
        publisher=left.publisher or right.publisher,
        published_on=published_on,
        jurisdiction=left.jurisdiction or right.jurisdiction,
        quality_flags=merged_quality_flags,
        summary=left.summary or right.summary,
        findings=merged_findings,
        provenance=replace(
            left.provenance,
            adapter_name=left.provenance.adapter_name or right.provenance.adapter_name,
            canonical_url=left.provenance.canonical_url or right.provenance.canonical_url,
            canonical_id=left.provenance.canonical_id or right.provenance.canonical_id,
            dedupe_key=left.provenance.dedupe_key or right.provenance.dedupe_key,
            source_locator=left.provenance.source_locator or right.provenance.source_locator,
            original_url=left.provenance.original_url or right.provenance.original_url,
            content_digest=left.provenance.content_digest or right.provenance.content_digest,
            retrieval_scope=left.provenance.retrieval_scope or right.provenance.retrieval_scope,
            collected_at=left.provenance.collected_at or right.provenance.collected_at,
            retrieved_at=left.provenance.retrieved_at or right.provenance.retrieved_at,
            observed_at=left.provenance.observed_at or right.provenance.observed_at,
            normalized_at=left.provenance.normalized_at or right.provenance.normalized_at,
            trace_notes=merged_trace_notes,
            metadata_consistent=metadata_consistent,
            citation_trace_complete=citation_trace_complete,
            partial=partial,
            partial_reason=partial_reason,
            metadata_fields_present=merged_metadata_fields_present,
            metadata_missing_fields=merged_metadata_fields_missing,
            stale=stale,
            stale_reason=left.provenance.stale_reason or right.provenance.stale_reason,
            malformed=malformed,
            malformed_reason=left.provenance.malformed_reason or right.provenance.malformed_reason,
            normalization_errors=merged_normalization_errors,
            dedupe_parent_ids=merged_dedupe_parent_ids,
            role_inference_status=_role_inference_status(
                left.provenance.role_inference_status,
                right.provenance.role_inference_status,
            ),
            role_inference_note=left.provenance.role_inference_note or right.provenance.role_inference_note,
            grounding_status=grounding_status,
            grounding_notes=merged_grounding_notes,
        ),
    )


def _grounding_status(left: str, right: str) -> str:
    states = {left or "grounded", right or "grounded"}
    if "ambiguous" in states:
        return "ambiguous"
    if "partial" in states:
        return "partial"
    return "grounded"


def _packet_dedupe_key(packet: SourcePacket, canonical_url: str, canonical_id: str) -> str:
    seed = canonical_url or canonical_id or "|".join([packet.publisher, packet.title, packet.source_role])
    return normalize_text(seed) or packet.source_id


def _metadata_fields(packet: SourcePacket) -> tuple[list[str], list[str]]:
    tracked = {
        "source_id": packet.source_id,
        "title": packet.title,
        "source_role": packet.source_role,
        "publisher": packet.publisher,
        "published_on": packet.published_on,
        "jurisdiction": packet.jurisdiction,
        "url": packet.url,
    }
    present = [key for key, value in tracked.items() if value]
    missing = [key for key, value in tracked.items() if not value]
    return present, missing


def _default_source_excerpt(statement: str, grounding_kind: str) -> str:
    if grounding_kind in {"direct_quote", "paraphrase"}:
        return statement
    return ""


def _role_inference_status(left: str, right: str) -> str:
    states = {left or "declared", right or "declared"}
    if "ambiguous" in states:
        return "ambiguous"
    if "inferred" in states:
        return "inferred"
    return "declared"
