from __future__ import annotations

from runtime_bootstrap import ensure_repo_paths


ensure_repo_paths()

from cleanroom_runtime.models import (  # noqa: E402
    AbsenceScope,
    RawDocumentInput,
    RunRequest,
    SourceFinding,
    SourcePacket,
    SourcePacketProvenance,
    TargetProfile,
)


def make_packet(
    source_id: str,
    source_role: str,
    *,
    title: str | None = None,
    findings: list[SourceFinding] | None = None,
    jurisdiction: str = "JP",
    provenance: SourcePacketProvenance | None = None,
    quality_flags: list[str] | None = None,
    published_on: str = "",
) -> SourcePacket:
    return SourcePacket(
        source_id=source_id,
        title=title or source_id,
        source_role=source_role,
        jurisdiction=jurisdiction,
        quality_flags=quality_flags or [],
        published_on=published_on,
        findings=findings or [],
        provenance=provenance or SourcePacketProvenance(),
    )


def make_finding(
    finding_id: str,
    statement: str,
    claim_kind: str,
    risk_level: str,
    section_hint: str,
    *,
    source_ids: list[str] | None = None,
    absence_scope: AbsenceScope | None = None,
    jurisdiction: str = "JP",
    contradiction_note: str = "",
    source_excerpt: str = "",
    grounding_kind: str = "summary",
    source_span_start: int | None = None,
    source_span_end: int | None = None,
    subject_key: str = "",
) -> SourceFinding:
    return SourceFinding(
        finding_id=finding_id,
        statement=statement,
        claim_kind=claim_kind,
        risk_level=risk_level,
        section_hint=section_hint,
        source_ids=source_ids or [],
        absence_scope=absence_scope,
        jurisdiction=jurisdiction,
        contradiction_note=contradiction_note,
        source_excerpt=source_excerpt,
        grounding_kind=grounding_kind,
        source_span_start=source_span_start,
        source_span_end=source_span_end,
        subject_key=subject_key,
    )


def make_request(
    *,
    topic: str = "Clean-room runtime behavior",
    use_context: str = "evaluate claim-centered runtime behavior",
    desired_depth: str = "medium",
    jurisdiction: str = "JP",
    mode: str = "scoped",
    evidence_mode: str = "synthetic",
    packets: list[SourcePacket] | None = None,
    raw_documents: list[RawDocumentInput] | None = None,
) -> RunRequest:
    return RunRequest(
        topic=topic,
        reader="runtime reviewers",
        use_context=use_context,
        desired_depth=desired_depth,
        jurisdiction=jurisdiction,
        mode=mode,
        evidence_mode=evidence_mode,
        source_packets=packets or [],
        raw_documents=raw_documents or [],
        target_profile=TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=1),
    )


def make_scoped_absence(subject: str, *, scope_label: str = "checked official materials", source_ids: list[str] | None = None) -> AbsenceScope:
    ids = source_ids or []
    return AbsenceScope(
        subject=subject,
        scope_label=scope_label,
        basis="not_found_in_checked_scope",
        checked_source_ids=ids,
        checked_roles=["official_regulator"],
        scope_note="Absence is limited to the checked scope.",
    )


def make_live_full_request() -> RunRequest:
    packets = [
        make_packet(
            "SRC-001",
            "official_regulator",
            findings=[
                make_finding(
                    "finding-001",
                    "The rule remains in force for the checked jurisdiction.",
                    "regulatory",
                    "high",
                    "direct_answer",
                    source_ids=["SRC-001", "SRC-002"],
                )
            ],
        ),
        make_packet("SRC-002", "legal_text"),
        make_packet(
            "SRC-003",
            "government_context",
            findings=[
                make_finding(
                    "finding-002",
                    "The public guidance explains the implementation path.",
                    "fact",
                    "medium",
                    "findings",
                    source_ids=["SRC-003"],
                )
            ],
        ),
        make_packet("SRC-004", "professional_body"),
        make_packet("SRC-005", "academic_review"),
    ]
    return RunRequest(
        topic="Regulatory completeness check",
        reader="runtime reviewers",
        use_context="decide whether a live full run can clear release",
        desired_depth="high",
        jurisdiction="JP",
        mode="full",
        evidence_mode="live",
        source_packets=packets,
        target_profile=TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=1),
    )


def make_raw_document(
    document_id: str,
    *,
    title: str = "Uploaded memo",
    content: str = "Clause 1: the checked document states a bounded fact.",
    jurisdiction: str = "JP",
) -> RawDocumentInput:
    return RawDocumentInput(
        document_id=document_id,
        title=title,
        content=content,
        jurisdiction=jurisdiction,
    )
