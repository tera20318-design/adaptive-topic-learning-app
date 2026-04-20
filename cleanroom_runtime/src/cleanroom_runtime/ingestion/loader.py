from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

from cleanroom_runtime.catalogs import AUTHORITATIVE_SOURCE_ROLES, SOURCE_ROLES
from cleanroom_runtime.ingestion_boundary import normalize_source_packet
from cleanroom_runtime.models import AbsenceScope, SourceFinding, SourcePacket, SourcePacketProvenance
from cleanroom_runtime.utils import uniq_preserve_order
from cleanroom_runtime.validators import validate_source_record


SCHEMA_PATH = Path(__file__).resolve().parents[3] / "core" / "schemas" / "normalized_source_packet.schema.json"
_STALE_DAYS = 365


@dataclass(slots=True)
class PacketLoadIssue:
    code: str
    message: str
    packet_index: int = 0
    source_id: str = ""
    blocking: bool = True


@dataclass(slots=True)
class PacketLoadResult:
    packets: list[SourcePacket] = field(default_factory=list)
    issues: list[PacketLoadIssue] = field(default_factory=list)
    rejected_packets: list[Any] = field(default_factory=list)
    accepted_packet_indices: list[int] = field(default_factory=list)
    schema_path: str = str(SCHEMA_PATH)

    @property
    def blocking_issues(self) -> list[PacketLoadIssue]:
        return [issue for issue in self.issues if issue.blocking]

    def to_audit_summary(self) -> dict[str, Any]:
        packet_issue_map = _issues_by_packet_index(self.issues)
        packet_summaries: list[dict[str, Any]] = []
        for packet_index, packet in zip(self.accepted_packet_indices, self.packets):
            issues = packet_issue_map.get(packet_index, [])
            disposition = "salvaged" if (packet.provenance.partial or packet.provenance.malformed) else "accepted"
            collision_with = sorted(
                parent_id
                for parent_id in packet.provenance.dedupe_parent_ids
                if parent_id and parent_id != packet.source_id
            )
            packet_summaries.append(
                {
                    "packet_index": packet_index,
                    "source_id": packet.source_id,
                    "title": packet.title,
                    "disposition": disposition,
                    "stale": packet.provenance.stale,
                    "partial": packet.provenance.partial,
                    "malformed": packet.provenance.malformed,
                    "dedupe_key": packet.provenance.dedupe_key,
                    "dedupe_collision_with": collision_with,
                    "quality_flags": list(packet.quality_flags),
                    "issue_codes": [issue.code for issue in issues],
                    "issue_messages": [issue.message for issue in issues],
                }
            )

        rejected_by_index = _rejection_summaries(self.rejected_packets, packet_issue_map)
        packet_summaries.extend(rejected_by_index)
        packet_summaries.sort(key=lambda item: (int(item.get("packet_index", 0)), str(item.get("source_id", ""))))

        stale_count = sum(1 for item in packet_summaries if item.get("stale"))
        salvaged_count = sum(1 for item in packet_summaries if item.get("disposition") == "salvaged")
        rejected_count = sum(1 for item in packet_summaries if item.get("disposition") == "rejected")
        collision_count = sum(1 for item in packet_summaries if item.get("dedupe_collision_with"))
        return {
            "input_count": len(self.accepted_packet_indices) + len(self.rejected_packets),
            "accepted_count": len(self.packets),
            "rejected_count": rejected_count,
            "salvaged_count": salvaged_count,
            "stale_count": stale_count,
            "dedupe_collision_count": collision_count,
            "blocking_issue_count": len(self.blocking_issues),
            "issue_count": len(self.issues),
            "packet_summaries": packet_summaries,
        }


def load_normalized_packet_schema(path: Path | None = None) -> dict[str, Any]:
    target = path or SCHEMA_PATH
    return json.loads(target.read_text(encoding="utf-8"))


def extract_packet_payload(payload: Any) -> list[Any]:
    hydrated = _read_payload(payload)
    if isinstance(hydrated, Mapping):
        packets = hydrated.get("packets")
        if isinstance(packets, Sequence) and not isinstance(packets, (str, bytes, bytearray)):
            return list(packets)
        return [dict(hydrated)]
    if isinstance(hydrated, Sequence) and not isinstance(hydrated, (str, bytes, bytearray)):
        return list(hydrated)
    raise ValueError("packet payload must be a list or an object with a `packets` list")


def validate_normalized_source_packet(
    payload: Mapping[str, Any],
    *,
    schema: Mapping[str, Any] | None = None,
) -> list[str]:
    active_schema = dict(schema or load_normalized_packet_schema())
    errors: list[str] = []
    _collect_schema_errors(payload, active_schema, root=active_schema, path="$", errors=errors)
    return errors


def validate_normalized_source_packet_collection(
    payloads: Any,
    *,
    schema: Mapping[str, Any] | None = None,
) -> list[str]:
    active_schema = dict(schema or load_normalized_packet_schema())
    try:
        items = extract_packet_payload(payloads)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    for index, payload in enumerate(items):
        if not isinstance(payload, Mapping):
            errors.append(f"$[{index}] must be an object")
            continue
        for error in validate_normalized_source_packet(payload, schema=active_schema):
            errors.append(error.replace("$", f"$[{index}]"))
    return errors


def load_normalized_source_packet(
    payload: Mapping[str, Any] | str | Path,
    *,
    packet_index: int = 0,
    adapter_name: str = "live_lite_loader",
    as_of_date: str = "",
) -> SourcePacket:
    result = load_normalized_source_packets(payload, adapter_name=adapter_name, as_of_date=as_of_date)
    if not result.packets:
        message = "; ".join(issue.message for issue in result.issues if issue.packet_index == packet_index)
        raise ValueError(message or "packet could not be loaded")
    return result.packets[0]


def load_normalized_source_packets(
    payloads: Any,
    *,
    adapter_name: str = "live_lite_loader",
    as_of_date: str = "",
) -> PacketLoadResult:
    schema = load_normalized_packet_schema()
    try:
        items = extract_packet_payload(payloads)
    except ValueError as exc:
        return PacketLoadResult(
            issues=[PacketLoadIssue(code="PACKET_COLLECTION_INVALID", message=str(exc), blocking=True)],
            rejected_packets=[payloads],
        )

    packets: list[SourcePacket] = []
    issues: list[PacketLoadIssue] = []
    rejected_packets: list[Any] = []
    accepted_packet_indices: list[int] = []

    for index, payload in enumerate(items):
        source_id = str(payload.get("source_id", "")) if isinstance(payload, Mapping) else ""
        if not isinstance(payload, Mapping):
            issues.append(
                PacketLoadIssue(
                    code="MALFORMED_PACKET",
                    message="packet payload must be an object",
                    packet_index=index,
                    source_id=source_id,
                    blocking=True,
                )
            )
            rejected_packets.append(payload)
            continue

        schema_errors = validate_normalized_source_packet(payload, schema=schema)
        blocking_schema_errors = [error for error in schema_errors if not error.startswith("$.findings[")]
        finding_schema_errors = [error for error in schema_errors if error.startswith("$.findings[")]
        if blocking_schema_errors:
            issues.extend(
                PacketLoadIssue(
                    code="SCHEMA_VALIDATION_FAILED",
                    message=error,
                    packet_index=index,
                    source_id=source_id,
                    blocking=True,
                )
                for error in blocking_schema_errors
            )
            rejected_packets.append(dict(payload))
            continue

        packet, packet_issues = _packet_from_payload(
            payload,
            packet_index=index,
            adapter_name=adapter_name,
            as_of_date=as_of_date,
        )
        issues.extend(
            PacketLoadIssue(
                code="SCHEMA_VALIDATION_NOTE",
                message=error,
                packet_index=index,
                source_id=source_id,
                blocking=False,
            )
            for error in finding_schema_errors
        )
        issues.extend(packet_issues)
        if packet is None:
            rejected_packets.append(dict(payload))
            continue
        packets.append(packet)
        accepted_packet_indices.append(index)

    _annotate_dedupe_collisions(packets, accepted_packet_indices, issues)

    return PacketLoadResult(
        packets=packets,
        issues=issues,
        rejected_packets=rejected_packets,
        accepted_packet_indices=accepted_packet_indices,
    )


def _packet_from_payload(
    payload: Mapping[str, Any],
    *,
    packet_index: int,
    adapter_name: str,
    as_of_date: str,
) -> tuple[SourcePacket | None, list[PacketLoadIssue]]:
    issues: list[PacketLoadIssue] = []
    source_id = str(payload.get("source_id", "")).strip()
    provenance_payload = dict(payload.get("provenance", {}))
    role_assignment_payload = dict(payload.get("role_assignment", {}))
    dedupe_payload = dict(payload.get("dedupe", {}))
    health_payload = dict(payload.get("ingestion_health", {}))
    staleness_payload = dict(payload.get("staleness", {}))
    findings_payloads = list(payload.get("findings", []))
    metadata_present, metadata_missing = _metadata_fields(payload)
    role, role_status, role_issue = _bounded_source_role(
        payload.get("source_role", ""),
        provenance_payload,
        role_assignment_payload,
    )
    if role_issue is not None:
        issues.append(
            PacketLoadIssue(
                code=role_issue[0],
                message=role_issue[1],
                packet_index=packet_index,
                source_id=source_id,
                blocking=False,
            )
        )

    stale, stale_reason = _stale_status(
        str(payload.get("published_on", "")).strip(),
        as_of_date
        or str(provenance_payload.get("retrieved_at", "")).strip()
        or str(provenance_payload.get("observed_at", "")).strip(),
        staleness_payload,
    )

    findings: list[SourceFinding] = []
    partial = False
    malformed = False
    partial_reason = ""
    malformed_reason = ""
    normalization_errors: list[str] = []
    trace_notes = list(_string_list(provenance_payload.get("trace_notes", [])))
    grounding_notes = list(_string_list(provenance_payload.get("grounding_notes", [])))

    for finding_payload in findings_payloads:
        if not isinstance(finding_payload, Mapping):
            issues.append(
                PacketLoadIssue(
                    code="MALFORMED_FINDING",
                    message=f"packet {source_id or packet_index} contains a non-object finding entry",
                    packet_index=packet_index,
                    source_id=source_id,
                    blocking=False,
                )
            )
            partial = True
            malformed = True
            normalization_errors.append("non-object finding entry")
            continue

        finding, finding_issue = _finding_from_payload(
            finding_payload,
            source_id=source_id,
            source_role=role,
        )
        if finding_issue is not None:
            issues.append(
                PacketLoadIssue(
                    code="MALFORMED_FINDING",
                    message=finding_issue,
                    packet_index=packet_index,
                    source_id=source_id,
                    blocking=False,
                )
            )
            partial = True
            malformed = True
            normalization_errors.append(finding_issue)
            continue
        findings.append(finding)

    if findings_payloads and not findings:
        partial = True
        malformed = True
        partial_reason = "No finding rows survived normalization."
        malformed_reason = partial_reason
    elif partial and not partial_reason:
        partial_reason = "Some finding rows were dropped during normalization."
        malformed_reason = malformed_reason or partial_reason

    citation_trace_complete = True
    for finding in findings:
        if any(identifier != source_id for identifier in finding.source_ids):
            citation_trace_complete = False
            trace_notes.append("finding references source IDs outside the containing packet")
            break
        if finding.grounding_kind in {"direct_quote", "paraphrase"}:
            if not finding.source_excerpt or finding.source_span_start is None or finding.source_span_end is None:
                citation_trace_complete = False
                partial = True
                malformed = True
                partial_reason = partial_reason or "Citation trace is incomplete for grounded findings."
                malformed_reason = malformed_reason or partial_reason
                trace_notes.append("grounded finding is missing excerpt text or span coordinates")
                break

    provenance = SourcePacketProvenance(
        packet_origin=str(provenance_payload.get("packet_origin") or "live_lite"),
        adapter_name=str(provenance_payload.get("adapter_name") or adapter_name),
        canonical_url=str(provenance_payload.get("canonical_url") or dedupe_payload.get("canonical_url") or payload.get("url", "")),
        canonical_id=str(provenance_payload.get("canonical_id") or dedupe_payload.get("canonical_id") or source_id),
        dedupe_key=str(provenance_payload.get("dedupe_key") or dedupe_payload.get("dedupe_key", "")),
        source_locator=str(
            provenance_payload.get("source_locator")
            or provenance_payload.get("source_locator_resolved")
            or provenance_payload.get("source_locator_requested")
            or payload.get("url")
            or payload.get("citation")
            or source_id
        ),
        original_url=str(provenance_payload.get("original_url") or payload.get("url", "")),
        content_digest=str(
            provenance_payload.get("content_digest")
            or dedupe_payload.get("content_fingerprint")
            or ""
        ),
        retrieval_scope=str(provenance_payload.get("retrieval_scope", "")),
        collected_at=str(provenance_payload.get("collected_at", "")),
        retrieved_at=str(provenance_payload.get("retrieved_at", "")),
        observed_at=str(provenance_payload.get("observed_at", "") or provenance_payload.get("modified_at", "")),
        normalized_at=str(provenance_payload.get("normalized_at") or (as_of_date or date.today().isoformat())),
        trace_notes=list(dict.fromkeys(trace_notes)),
        metadata_consistent=bool(
            provenance_payload.get("metadata_consistent", health_payload.get("metadata_consistent", not metadata_missing))
        ),
        citation_trace_complete=bool(
            provenance_payload.get("citation_trace_complete", health_payload.get("citation_trace_complete", citation_trace_complete))
        ),
        partial=bool(provenance_payload.get("partial", health_payload.get("partial", partial))),
        partial_reason=str(
            provenance_payload.get("partial_reason")
            or health_payload.get("partial_failure_reason")
            or partial_reason
        ),
        metadata_fields_present=list(dict.fromkeys(metadata_present)),
        metadata_missing_fields=list(dict.fromkeys(metadata_missing)),
        stale=bool(provenance_payload.get("stale", stale)),
        stale_reason=str(provenance_payload.get("stale_reason") or stale_reason),
        malformed=bool(provenance_payload.get("malformed", health_payload.get("malformed", malformed))),
        malformed_reason=str(
            provenance_payload.get("malformed_reason")
            or health_payload.get("partial_failure_reason")
            or malformed_reason
        ),
        normalization_errors=list(
            dict.fromkeys(
                [
                    *normalization_errors,
                    *_string_list(provenance_payload.get("normalization_errors", [])),
                    *_string_list(health_payload.get("dropped_fields", [])),
                    *_string_list(health_payload.get("malformed_fields", [])),
                ]
            )
        ),
        dedupe_parent_ids=list(
            dict.fromkeys(
                [
                    *_string_list(provenance_payload.get("dedupe_parent_ids", [])),
                    *_string_list(dedupe_payload.get("merged_from_packet_ids", [])),
                    *([str(dedupe_payload.get("duplicate_of_packet_id")).strip()] if str(dedupe_payload.get("duplicate_of_packet_id", "")).strip() else []),
                ]
            )
        ),
        role_inference_status=str(provenance_payload.get("role_inference_status") or role_status),
        role_inference_note=str(
            provenance_payload.get("role_inference_note")
            or role_assignment_payload.get("assignment_basis")
            or (role_issue[1] if role_issue is not None else "")
        ),
        grounding_status=str(
            provenance_payload.get("grounding_status")
            or health_payload.get("grounding_status")
            or ("partial" if partial else "grounded")
        ),
        grounding_notes=list(dict.fromkeys(grounding_notes)),
    )

    packet = normalize_source_packet(
        SourcePacket(
            source_id=source_id,
            title=str(payload.get("title", "")).strip(),
            source_role=role,
            citation=str(payload.get("citation", "")).strip(),
            url=str(payload.get("url", "")).strip(),
            publisher=str(payload.get("publisher", "")).strip(),
            published_on=str(payload.get("published_on", "")).strip(),
            jurisdiction=str(payload.get("jurisdiction", "")).strip(),
            content_type=str(payload.get("content_type", "")).strip(),
            quality_flags=list(_string_list(payload.get("quality_flags", []))),
            summary=str(payload.get("summary", "")).strip(),
            findings=findings,
            provenance=provenance,
        )
    )
    if stale and "stale source" not in packet.quality_flags:
        packet.quality_flags.append("stale source")
    if partial and "partial evidence packet" not in packet.quality_flags:
        packet.quality_flags.append("partial evidence packet")
    if malformed and "malformed packet" not in packet.quality_flags:
        packet.quality_flags.append("malformed packet")

    record_errors = validate_source_record(packet)
    blocking_errors = [error for error in record_errors if "must be one of" in error or "must be non-empty" in error]
    if blocking_errors:
        issues.extend(
            PacketLoadIssue(
                code="PACKET_VALIDATION_FAILED",
                message=error,
                packet_index=packet_index,
                source_id=source_id,
                blocking=True,
            )
            for error in blocking_errors
        )
        return None, issues
    issues.extend(
        PacketLoadIssue(
            code="PACKET_VALIDATION_NOTE",
            message=error,
            packet_index=packet_index,
            source_id=source_id,
            blocking=False,
        )
        for error in record_errors
        if error not in blocking_errors
    )
    if stale:
        issues.append(
            PacketLoadIssue(
                code="STALE_SOURCE_FLAGGED",
                message=stale_reason,
                packet_index=packet_index,
                source_id=source_id,
                blocking=False,
            )
        )
    return packet, issues


def _finding_from_payload(
    payload: Mapping[str, Any],
    *,
    source_id: str,
    source_role: str,
) -> tuple[SourceFinding | None, str | None]:
    required = ("finding_id", "statement", "claim_kind", "risk_level")
    missing = [field for field in required if not str(payload.get(field, "")).strip()]
    if missing:
        return None, f"finding {payload.get('finding_id', '<unknown>')} is missing required fields: {', '.join(missing)}"

    absence_scope_value = payload.get("absence_scope")
    if isinstance(absence_scope_value, Mapping):
        absence_scope = AbsenceScope(
            subject=str(absence_scope_value.get("subject", "")).strip(),
            scope_label=str(absence_scope_value.get("scope_label", "")).strip(),
            basis=str(absence_scope_value.get("basis", "")).strip(),
            checked_source_ids=list(_string_list(absence_scope_value.get("checked_source_ids", []))),
            checked_roles=list(_string_list(absence_scope_value.get("checked_roles", []))),
            scope_note=str(absence_scope_value.get("scope_note", "")).strip(),
        )
    else:
        absence_scope = absence_scope_value

    traceability_payload = payload.get("traceability", {})
    traceability = traceability_payload if isinstance(traceability_payload, Mapping) else {}
    locator_value = str(traceability.get("locator_value", "")).strip()
    support_excerpt = str(traceability.get("support_excerpt", "")).strip()
    extraction_method = str(traceability.get("extraction_method", "")).strip()
    return (
        SourceFinding(
            finding_id=str(payload.get("finding_id", "")).strip(),
            statement=str(payload.get("statement", "")).strip(),
            claim_kind=str(payload.get("claim_kind", "")).strip(),
            risk_level=str(payload.get("risk_level", "")).strip(),
            section_hint=str(payload.get("section_hint", "")).strip(),
            support_status_hint=str(payload.get("support_status_hint", "supported")).strip() or "supported",
            confidence=_float_or_default(payload.get("confidence"), 0.8),
            source_ids=list(_string_list(payload.get("source_ids", []))) or [source_id],
            source_roles=list(_string_list(payload.get("source_roles", []))) or [source_role],
            decision_note=str(payload.get("decision_note", "")).strip(),
            caveat=str(payload.get("caveat", "")).strip(),
            scope_note=str(payload.get("scope_note", "")).strip(),
            contradiction_note=str(payload.get("contradiction_note", "")).strip(),
            required_fix=str(payload.get("required_fix", "")).strip(),
            jurisdiction=str(payload.get("jurisdiction", "")).strip(),
            temporal_note=str(payload.get("temporal_note", "")).strip(),
            tags=list(_string_list(payload.get("tags", []))),
            absence_type=str(payload.get("absence_type", "")).strip(),
            absence_scope=absence_scope,
            source_excerpt=str(payload.get("source_excerpt", "")).strip() or support_excerpt,
            source_span_label=str(payload.get("source_span_label", "")).strip() or locator_value,
            source_span_start=_int_or_none(payload.get("source_span_start")),
            source_span_end=_int_or_none(payload.get("source_span_end")),
            grounding_kind=str(payload.get("grounding_kind", "")).strip() or extraction_method or "summary",
            subject_key=str(payload.get("subject_key", "")).strip(),
            subject_scope_key=str(payload.get("subject_scope_key", "")).strip(),
            source_trust_note=str(payload.get("source_trust_note", "")).strip()
            or str(traceability.get("derived_from_content_digest", "")).strip(),
        ),
        None,
    )


def _bounded_source_role(
    source_role: Any,
    provenance_payload: Mapping[str, Any],
    role_assignment_payload: Mapping[str, Any],
) -> tuple[str, str, tuple[str, str] | None]:
    role = str(
        role_assignment_payload.get("effective_source_role")
        or source_role
        or role_assignment_payload.get("declared_source_role")
        or role_assignment_payload.get("inferred_source_role")
        or ""
    ).strip()
    assignment_method = str(role_assignment_payload.get("assignment_method", "")).strip()
    inference_status = str(provenance_payload.get("role_inference_status", "")).strip()
    if not inference_status and assignment_method and assignment_method != "declared":
        inference_status = "inferred"
    inference_status = inference_status or "declared"
    packet_origin = str(provenance_payload.get("packet_origin", "")).strip()
    if not role and packet_origin == "raw_document":
        return (
            "user_provided_source",
            "inferred",
            ("ROLE_INFERENCE_NOTE", "missing source_role was bounded to `user_provided_source` for a raw document packet"),
        )
    if role not in SOURCE_ROLES:
        return "unknown", "ambiguous", ("ROLE_INFERENCE_BOUNDARY", "source role was not usable and was bounded to `unknown`")
    if inference_status == "inferred" and role in AUTHORITATIVE_SOURCE_ROLES:
        return (
            "unknown",
            "ambiguous",
            ("ROLE_INFERENCE_BOUNDARY", "loader will not infer authoritative source roles from packet metadata alone"),
        )
    return role, inference_status if inference_status in {"declared", "inferred", "ambiguous"} else "declared", None


def _metadata_fields(payload: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    tracked = {
        "source_id": payload.get("source_id"),
        "title": payload.get("title"),
        "source_role": payload.get("source_role"),
        "publisher": payload.get("publisher"),
        "published_on": payload.get("published_on"),
        "jurisdiction": payload.get("jurisdiction"),
        "url": payload.get("url"),
        "provenance": payload.get("provenance"),
    }
    present = [key for key, value in tracked.items() if value]
    missing = [key for key, value in tracked.items() if not value]
    return present, missing


def _stale_status(
    published_on: str,
    reference_date: str,
    staleness_payload: Mapping[str, Any],
) -> tuple[bool, str]:
    stale_status = str(staleness_payload.get("stale_status", "")).strip()
    stale_reason = str(staleness_payload.get("stale_reason", "")).strip()
    if stale_status in {"stale", "superseded"}:
        return True, stale_reason or "staleness metadata marked the packet as stale"
    published = _parse_date(published_on)
    reference = _parse_date(reference_date) or date.today()
    if published is None:
        return False, ""
    age_days = (reference - published).days
    if age_days > _STALE_DAYS:
        return True, f"published material is {age_days} days older than the reference date"
    return False, ""


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    candidate = value.strip()
    for rendered in (candidate, candidate[:10]):
        try:
            return datetime.fromisoformat(rendered.replace("Z", "+00:00")).date()
        except ValueError:
            continue
    return None


def _float_or_default(value: Any, default: float) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return default


def _int_or_none(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return uniq_preserve_order([str(item).strip() for item in value if str(item).strip()])


def _read_payload(payload: Any) -> Any:
    if isinstance(payload, Path):
        return json.loads(payload.read_text(encoding="utf-8"))
    if isinstance(payload, str):
        candidate = Path(payload)
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return payload


def _collect_schema_errors(
    value: Any,
    schema: Mapping[str, Any],
    *,
    root: Mapping[str, Any],
    path: str,
    errors: list[str],
) -> None:
    if "$ref" in schema:
        _collect_schema_errors(value, _resolve_ref(str(schema["$ref"]), root), root=root, path=path, errors=errors)
        return
    if "anyOf" in schema:
        branch_errors: list[list[str]] = []
        for branch in schema["anyOf"]:
            candidate_errors: list[str] = []
            _collect_schema_errors(value, branch, root=root, path=path, errors=candidate_errors)
            if not candidate_errors:
                return
            branch_errors.append(candidate_errors)
        errors.append(branch_errors[0][0] if branch_errors else f"{path} did not satisfy any schema branch")
        return

    expected_type = schema.get("type")
    if expected_type is not None and not _matches_type(value, expected_type):
        errors.append(f"{path} must be of type {expected_type}")
        return

    if "enum" in schema and value not in schema["enum"]:
        rendered = ", ".join(repr(item) for item in schema["enum"])
        errors.append(f"{path} must be one of {rendered}")

    if isinstance(value, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            errors.append(f"{path} must have length >= {min_length}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        if isinstance(minimum, (int, float)) and value < minimum:
            errors.append(f"{path} must be >= {minimum}")
        maximum = schema.get("maximum")
        if isinstance(maximum, (int, float)) and value > maximum:
            errors.append(f"{path} must be <= {maximum}")

    if isinstance(value, Mapping):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}.{key} is required")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            for key in extras:
                errors.append(f"{path}.{key} is not allowed by the normalized packet schema")
        for key, property_schema in properties.items():
            if key in value:
                _collect_schema_errors(value[key], property_schema, root=root, path=f"{path}.{key}", errors=errors)
        return

    if isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema is None:
            return
        for index, item in enumerate(value):
            _collect_schema_errors(item, item_schema, root=root, path=f"{path}[{index}]", errors=errors)


def _resolve_ref(reference: str, root: Mapping[str, Any]) -> Mapping[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported schema reference: {reference}")
    value: Any = root
    for token in reference[2:].split("/"):
        if not isinstance(value, Mapping) or token not in value:
            raise ValueError(f"unresolved schema reference: {reference}")
        value = value[token]
    if not isinstance(value, Mapping):
        raise ValueError(f"schema reference does not point to an object: {reference}")
    return value


def _matches_type(value: Any, expected_type: Any) -> bool:
    if isinstance(expected_type, list):
        return any(_matches_type(value, item) for item in expected_type)
    if expected_type == "object":
        return isinstance(value, Mapping)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def _annotate_dedupe_collisions(
    packets: list[SourcePacket],
    accepted_packet_indices: list[int],
    issues: list[PacketLoadIssue],
) -> None:
    packets_by_key: dict[str, list[tuple[int, SourcePacket]]] = {}
    for packet_index, packet in zip(accepted_packet_indices, packets):
        dedupe_key = packet.provenance.dedupe_key or packet.provenance.canonical_url or packet.provenance.canonical_id or packet.source_id
        if not dedupe_key:
            continue
        packets_by_key.setdefault(dedupe_key, []).append((packet_index, packet))

    for dedupe_key, grouped_packets in packets_by_key.items():
        if len(grouped_packets) < 2:
            continue
        grouped_ids = [packet.source_id for _, packet in grouped_packets if packet.source_id]
        for packet_index, packet in grouped_packets:
            peers = [source_id for source_id in grouped_ids if source_id != packet.source_id]
            if peers:
                packet.provenance.dedupe_parent_ids = uniq_preserve_order([*packet.provenance.dedupe_parent_ids, *peers])
            note = f"dedupe collision detected for key `{dedupe_key}`"
            if peers:
                note += f" with packets: {', '.join(peers)}"
            packet.provenance.trace_notes = uniq_preserve_order([*packet.provenance.trace_notes, note])
            if "dedupe collision noted" not in packet.quality_flags:
                packet.quality_flags.append("dedupe collision noted")
            issues.append(
                PacketLoadIssue(
                    code="DEDUPE_COLLISION_NOTE",
                    message=note,
                    packet_index=packet_index,
                    source_id=packet.source_id,
                    blocking=False,
                )
            )


def _issues_by_packet_index(issues: list[PacketLoadIssue]) -> dict[int, list[PacketLoadIssue]]:
    packet_issue_map: dict[int, list[PacketLoadIssue]] = {}
    for issue in issues:
        packet_issue_map.setdefault(issue.packet_index, []).append(issue)
    return packet_issue_map


def _rejection_summaries(
    rejected_packets: list[Any],
    packet_issue_map: dict[int, list[PacketLoadIssue]],
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    rejected_indices = sorted(index for index, issues in packet_issue_map.items() if any(issue.blocking for issue in issues))
    for offset, packet in enumerate(rejected_packets):
        packet_index = rejected_indices[offset] if offset < len(rejected_indices) else offset
        payload = packet if isinstance(packet, Mapping) else {}
        issues = packet_issue_map.get(packet_index, [])
        summaries.append(
            {
                "packet_index": packet_index,
                "source_id": str(payload.get("source_id", "")) if isinstance(payload, Mapping) else "",
                "title": str(payload.get("title", "")) if isinstance(payload, Mapping) else "",
                "disposition": "rejected",
                "stale": False,
                "partial": False,
                "malformed": True,
                "dedupe_key": str(payload.get("dedupe", {}).get("dedupe_key", "")) if isinstance(payload, Mapping) and isinstance(payload.get("dedupe"), Mapping) else "",
                "dedupe_collision_with": [],
                "quality_flags": list(_string_list(payload.get("quality_flags", []))) if isinstance(payload, Mapping) else [],
                "issue_codes": [issue.code for issue in issues],
                "issue_messages": [issue.message for issue in issues],
            }
        )
    return summaries


__all__ = [
    "PacketLoadIssue",
    "PacketLoadResult",
    "SCHEMA_PATH",
    "extract_packet_payload",
    "load_normalized_packet_schema",
    "load_normalized_source_packet",
    "load_normalized_source_packets",
    "validate_normalized_source_packet",
    "validate_normalized_source_packet_collection",
]
