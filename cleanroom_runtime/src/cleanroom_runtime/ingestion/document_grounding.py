from __future__ import annotations

import hashlib
import re

from cleanroom_runtime.models import (
    RawDocumentInput,
    SourceFinding,
    SourcePacket,
    SourcePacketProvenance,
    encode_grounding_trace,
)
from cleanroom_runtime.utils import normalize_text


def document_packets_from_raw_documents(documents: list[RawDocumentInput]) -> list[SourcePacket]:
    packets: list[SourcePacket] = []
    for document in documents:
        packets.append(_packet_from_document(document))
    return packets


def _packet_from_document(document: RawDocumentInput) -> SourcePacket:
    blocks = _grounded_blocks(document.content, review_mode=document.review_mode)
    findings: list[SourceFinding] = []
    quality_flags = [
        "Document grounding remains limited to the checked excerpt spans.",
        "Checked document excerpts do not become topic-wide authority by themselves.",
    ]
    if document.review_mode == "document_review":
        quality_flags.append("Document-review mode keeps checked blocks separate and does not allow cross-block synthesis.")
    grounding_status = "grounded"
    partial = False
    malformed = False
    partial_reason = ""
    malformed_reason = ""

    if not blocks:
        grounding_status = "partial"
        partial = True
        malformed = True
        partial_reason = "No grounded excerpt lines were extracted from the provided document."
        malformed_reason = partial_reason
        quality_flags.append("The provided document did not yield grounded excerpt lines.")
    else:
        if any(len(block["spans"]) > 1 for block in blocks):
            quality_flags.append("Multi-span grounding is limited to a single checked block at a time.")
        if len(blocks) > 1:
            quality_flags.append("Separate checked blocks remain separate evidence units and are not merged into one summary claim.")
        for index, block in enumerate(blocks[:8], start=1):
            span_labels = [span["label"] for span in block["spans"]]
            span_starts = [span["start"] for span in block["spans"]]
            span_ends = [span["end"] for span in block["spans"]]
            grounding_marker = "direct_document_multispan" if len(block["spans"]) > 1 else "direct_document_span"
            scope_note = "Grounding is limited to the checked document excerpt span(s) and does not settle broader facts."
            findings.append(
                SourceFinding(
                    finding_id=f"{document.document_id}-finding-{index:03d}",
                    statement=f"The checked document states: {block['excerpt']}",
                    claim_kind="fact",
                    risk_level="medium",
                    section_hint="direct_answer" if index == 1 else "findings",
                    support_status_hint="supported",
                    confidence=0.8 if len(block["spans"]) == 1 else 0.76,
                    source_ids=[document.document_id],
                    source_roles=[document.source_role],
                    scope_note=scope_note,
                    source_excerpt=block["excerpt"],
                    source_span_label=block["label"],
                    source_span_start=span_starts[0],
                    source_span_end=span_ends[-1],
                    grounding_kind="direct_quote",
                    grounding_marker=grounding_marker,
                    grounding_scope_note=scope_note,
                    subject_key=normalize_text(block["excerpt"]),
                    subject_scope_key=normalize_text(f"{document.document_id}|{block['label']}|{block['excerpt']}"),
                    source_trust_note=encode_grounding_trace(
                        grounding_marker=grounding_marker,
                        grounding_scope_note=scope_note,
                        span_labels=span_labels,
                        span_starts=span_starts,
                        span_ends=span_ends,
                    ),
                    tags=_tags_for_block(block),
                )
            )

    provenance = SourcePacketProvenance(
        packet_origin="raw_document",
        adapter_name="document_grounding",
        canonical_id=document.document_id,
        dedupe_key=normalize_text(f"{document.document_id}|{document.title}"),
        source_locator=document.excerpt_label or document.document_id,
        content_digest=hashlib.sha256(document.content.encode("utf-8")).hexdigest(),
        observed_at=document.provided_at,
        metadata_consistent=True,
        citation_trace_complete=bool(findings),
        partial=partial,
        partial_reason=partial_reason,
        malformed=malformed,
        malformed_reason=malformed_reason,
        grounding_status=grounding_status,
        grounding_notes=[
            "Grounding is derived from direct document excerpts.",
            "Separate checked blocks remain separate evidence units unless a single block directly spans multiple lines.",
            (
                "Document-review mode is limited to the checked paragraphs and does not justify cross-block synthesis."
                if document.review_mode == "document_review"
                else "Excerpt mode remains limited to the checked excerpt text."
            ),
        ],
        metadata_fields_present=["document_id", "title", "content", "source_role", "review_mode"],
        metadata_missing_fields=_missing_metadata_fields(document),
        role_inference_status="declared",
    )
    summary = blocks[0]["spans"][0]["text"] if blocks else ""
    if blocks:
        summary = str(blocks[0]["spans"][0].get("raw_text", summary))
    return SourcePacket(
        source_id=document.document_id,
        title=document.title,
        source_role=document.source_role,
        citation=document.title,
        publisher="user_document",
        published_on=document.provided_at,
        jurisdiction=document.jurisdiction,
        content_type=document.content_type,
        quality_flags=quality_flags,
        summary=summary,
        findings=findings,
        provenance=provenance,
    )


def _grounded_blocks(content: str, *, review_mode: str = "excerpt") -> list[dict[str, object]]:
    lines = list(_line_segments(content))
    blocks: list[dict[str, object]] = []
    current: list[dict[str, object]] = []
    block_index = 0
    for line in lines:
        if line["blank"]:
            if current:
                block_index += 1
                block = _build_block(current, block_index=block_index, review_mode=review_mode)
                if block is not None:
                    blocks.append(block)
                current = []
            continue
        if line["standalone"] and current:
            block_index += 1
            block = _build_block(current, block_index=block_index, review_mode=review_mode)
            if block is not None:
                blocks.append(block)
            current = []
        if line["text"]:
            current.append(line)
        if line["standalone"] and current:
            block_index += 1
            block = _build_block(current, block_index=block_index, review_mode=review_mode)
            if block is not None:
                blocks.append(block)
            current = []
    if current:
        block_index += 1
        block = _build_block(current, block_index=block_index, review_mode=review_mode)
        if block is not None:
            blocks.append(block)
    return blocks


def _build_block(
    lines: list[dict[str, object]],
    *,
    block_index: int,
    review_mode: str,
) -> dict[str, object] | None:
    spans = [line for line in lines if len(str(line["text"])) >= 12]
    if not spans:
        return None
    start_line = int(spans[0]["line_number"])
    end_line = int(spans[-1]["line_number"])
    label = f"line {start_line}" if start_line == end_line else f"lines {start_line}-{end_line}"
    if review_mode == "document_review":
        label = f"paragraph {block_index} ({label})"
    excerpt = "\n".join(str(span["text"]) for span in spans)
    return {
        "label": label,
        "excerpt": excerpt,
        "spans": spans,
    }


def _line_segments(content: str):
    line_start = 0
    for line_number, raw_line in enumerate(content.splitlines(keepends=True), start=1):
        stripped = raw_line.rstrip("\r\n")
        text = stripped.strip()
        clean_text = re.sub(r"^\s*[-*]\s+", "", text)
        clean_text = re.sub(r"^\s*#+\s*", "", clean_text)
        yield {
            "line_number": line_number,
            "label": f"line {line_number}",
            "raw_text": text,
            "text": clean_text,
            "start": line_start + stripped.find(clean_text) if clean_text else line_start,
            "end": line_start + stripped.find(clean_text) + len(clean_text) if clean_text else line_start + len(stripped),
            "blank": not bool(text),
            "standalone": bool(re.match(r"^\s*[-*]\s+", stripped)),
        }
        line_start += len(raw_line)


def _tags_for_block(block: dict[str, object]) -> list[str]:
    tags = ["document_grounded", "direct_document_grounding", "scope_limited_document"]
    spans = block.get("spans", [])
    if isinstance(spans, list) and len(spans) > 1:
        tags.append("multi_span_grounding")
    if str(block.get("label", "")).startswith("paragraph "):
        tags.append("document_review_mode")
    return tags


def _missing_metadata_fields(document: RawDocumentInput) -> list[str]:
    missing: list[str] = []
    if not document.jurisdiction:
        missing.append("jurisdiction")
    missing.append("url")
    return missing


__all__ = ["document_packets_from_raw_documents"]
