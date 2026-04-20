from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime_bootstrap import ROOT, ensure_runtime_namespace


ensure_runtime_namespace()

from cleanroom_runtime.models import (  # noqa: E402
    AbsenceScope,
    RawDocumentInput,
    ReleaseContract,
    RunRequest,
    SourceFinding,
    SourcePacket,
    SourcePacketProvenance,
    TargetProfile,
)


FIXTURE_DIR = ROOT / "fixtures"
VERTICAL_SLICE_DIR = ROOT / "generated" / "vertical_slices"
SNAPSHOT_FILES = (
    "final_report.md",
    "domain-adapter.md",
    "release-gate-summary.md",
    "metrics.json",
    "bundle.json",
    "claim-ledger.tsv",
    "included-claims.tsv",
    "excluded-claims.tsv",
    "citation-ledger.tsv",
    "gate-issues.tsv",
)
TRAP_TAGS = frozenset({"absence_trap", "overgeneralization_trap"})


@dataclass(slots=True)
class GenreFixture:
    fixture_id: str
    genre: str
    description: str
    scenario_tags: list[str]
    request: RunRequest
    expected: dict[str, Any]
    variant: str = ""


def load_all_fixtures() -> list[GenreFixture]:
    return [load_fixture(path) for path in sorted(path for path in FIXTURE_DIR.iterdir() if path.is_dir())]


def load_positive_fixtures() -> list[GenreFixture]:
    return load_variant_fixtures("positive")


def load_mid_quality_fixtures() -> list[GenreFixture]:
    return load_variant_fixtures("mid")


def load_variant_fixtures(variant: str) -> list[GenreFixture]:
    fixtures: list[GenreFixture] = []
    for path in sorted(path for path in FIXTURE_DIR.iterdir() if path.is_dir()):
        if (path / f"request_{variant}.json").is_file():
            fixtures.append(load_fixture(path, variant=variant))
    return fixtures


def load_fixture(path_or_id: str | Path, *, variant: str = "") -> GenreFixture:
    path = _resolve_fixture_path(path_or_id)
    suffix = f"_{variant}" if variant else ""
    request_payload = _read_json(path / f"request{suffix}.json")
    source_packet_path = path / f"source_packets{suffix}.json"
    if not source_packet_path.is_file():
        source_packet_path = path / ("source_packets.json" if not variant else f"synthetic_sources{suffix}.json")
    if not source_packet_path.is_file():
        source_packet_path = path / ("synthetic_sources.json" if not variant else "synthetic_sources.json")
    sources_payload = _read_json(source_packet_path)
    expected_payload = _read_json(path / f"expected{suffix}.json")
    request = _build_request(request_payload["request"], sources_payload)
    return GenreFixture(
        fixture_id=path.name,
        genre=request_payload.get("genre", path.name),
        description=request_payload.get("description", ""),
        scenario_tags=list(request_payload.get("scenario_tags", [])),
        request=request,
        expected=dict(expected_payload),
        variant=variant,
    )


def fixture_findings(fixture: GenreFixture) -> list[SourceFinding]:
    return [finding for packet in fixture.request.source_packets for finding in packet.findings]


def snapshot_dir(fixture: GenreFixture) -> Path:
    suffix = f"__{fixture.variant}" if fixture.variant else ""
    return VERTICAL_SLICE_DIR / f"{fixture.fixture_id}{suffix}"


def _resolve_fixture_path(path_or_id: str | Path) -> Path:
    path = Path(path_or_id)
    if path.is_dir():
        return path
    return FIXTURE_DIR / path.name


def _build_request(payload: dict[str, Any], packet_payloads: list[dict[str, Any]]) -> RunRequest:
    packets = [_build_packet(packet_payload) for packet_payload in packet_payloads]
    return RunRequest(
        topic=payload["topic"],
        reader=payload["reader"],
        use_context=payload["use_context"],
        desired_depth=payload.get("desired_depth", ""),
        jurisdiction=payload.get("jurisdiction", ""),
        mode=payload.get("mode", "scoped"),
        evidence_mode=payload.get("evidence_mode", "synthetic"),
        as_of_date=payload.get("as_of_date", ""),
        output_type=payload.get("output_type", "report"),
        question=payload.get("question", ""),
        temporal_context=payload.get("temporal_context", ""),
        source_packets=packets,
        raw_documents=[RawDocumentInput(**item) for item in payload.get("raw_documents", [])],
        target_profile=TargetProfile(**payload.get("target_profile", {})),
        waivers=list(payload.get("waivers", [])),
        release_contract=ReleaseContract(**payload.get("release_contract", {})),
        requested_mode=payload.get("requested_mode", ""),
        provided_source_ids=list(payload.get("provided_source_ids", [])),
    )


def _build_packet(payload: dict[str, Any]) -> SourcePacket:
    jurisdiction = payload.get("jurisdiction", "")
    return SourcePacket(
        source_id=payload["source_id"],
        title=payload["title"],
        source_role=payload["source_role"],
        citation=payload.get("citation", ""),
        url=payload.get("url", ""),
        publisher=payload.get("publisher", ""),
        published_on=payload.get("published_on", ""),
        jurisdiction=jurisdiction,
        content_type=payload.get("content_type", ""),
        quality_flags=list(payload.get("quality_flags", [])),
        summary=payload.get("summary", ""),
        findings=[
            _build_finding(finding_payload, default_source_id=payload["source_id"], default_jurisdiction=jurisdiction)
            for finding_payload in payload.get("findings", [])
        ],
        provenance=SourcePacketProvenance(**payload.get("provenance", {})),
    )


def _build_finding(payload: dict[str, Any], *, default_source_id: str, default_jurisdiction: str) -> SourceFinding:
    absence_scope = payload.get("absence_scope")
    if isinstance(absence_scope, dict):
        absence_scope = AbsenceScope(**absence_scope)
    return SourceFinding(
        finding_id=payload["finding_id"],
        statement=payload["statement"],
        claim_kind=payload["claim_kind"],
        risk_level=payload["risk_level"],
        section_hint=payload.get("section_hint", ""),
        support_status_hint=payload.get("support_status_hint", "supported"),
        confidence=float(payload.get("confidence", 0.8)),
        source_ids=list(payload.get("source_ids", [default_source_id])),
        source_roles=list(payload.get("source_roles", [])),
        decision_note=payload.get("decision_note", ""),
        caveat=payload.get("caveat", ""),
        scope_note=payload.get("scope_note", ""),
        contradiction_note=payload.get("contradiction_note", ""),
        required_fix=payload.get("required_fix", ""),
        jurisdiction=payload.get("jurisdiction", default_jurisdiction),
        temporal_note=payload.get("temporal_note", ""),
        tags=list(payload.get("tags", [])),
        absence_type=payload.get("absence_type", ""),
        absence_scope=absence_scope,
        source_excerpt=payload.get("source_excerpt", ""),
        source_span_label=payload.get("source_span_label", ""),
        source_span_start=payload.get("source_span_start"),
        source_span_end=payload.get("source_span_end"),
        source_span_labels=list(payload.get("source_span_labels", [])),
        source_span_starts=list(payload.get("source_span_starts", [])),
        source_span_ends=list(payload.get("source_span_ends", [])),
        grounding_kind=payload.get("grounding_kind", "summary"),
        grounding_marker=payload.get("grounding_marker", ""),
        grounding_scope_note=payload.get("grounding_scope_note", ""),
        subject_key=payload.get("subject_key", ""),
        subject_scope_key=payload.get("subject_scope_key", ""),
        source_trust_note=payload.get("source_trust_note", ""),
    )


def _read_json(path: Path) -> dict[str, Any] | list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))
