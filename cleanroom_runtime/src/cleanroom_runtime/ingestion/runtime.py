from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from cleanroom_runtime.models import PipelineBundle, RunRequest, StageSnapshot
from cleanroom_runtime.pipeline import run_pipeline
from cleanroom_runtime.stages.release_gate import decide_release_gate
from cleanroom_runtime.stages.bundle_renderer import render_bundle

from .loader import PacketLoadResult, load_normalized_source_packets


def prepare_live_lite_request(
    request: RunRequest,
    packet_payloads: Any,
    *,
    adapter_name: str = "live_lite_loader",
    as_of_date: str = "",
) -> tuple[RunRequest, PacketLoadResult]:
    effective_as_of_date = request.as_of_date or as_of_date
    load_result = load_normalized_source_packets(
        packet_payloads,
        adapter_name=adapter_name,
        as_of_date=effective_as_of_date,
    )
    prepared_request = replace(
        request,
        source_packets=list(load_result.packets),
        evidence_mode="live" if request.evidence_mode == "synthetic" else request.evidence_mode,
        as_of_date=effective_as_of_date,
    )
    return prepared_request, load_result


def execute_live_lite_request(
    request: RunRequest,
    packet_payloads: Any,
    *,
    adapter_name: str = "live_lite_loader",
    as_of_date: str = "",
    output_dir: str | Path | None = None,
) -> PipelineBundle:
    prepared_request, load_result = prepare_live_lite_request(
        request,
        packet_payloads,
        adapter_name=adapter_name,
        as_of_date=as_of_date,
    )
    bundle = run_pipeline(prepared_request)
    bundle.metrics.ingestion_audit_visible = True
    bundle.release_gate = decide_release_gate(
        draft=bundle.draft,
        claims=bundle.claims,
        citations=bundle.citations,
        contradictions=bundle.contradictions,
        gaps=bundle.gaps,
        budget=bundle.budget,
        adapter=bundle.adapter,
        metrics=bundle.metrics,
        validation_errors=[],
        request=bundle.request,
        intent=bundle.intent,
        risk=bundle.risk,
    )
    _attach_ingestion_audit(bundle, load_result)
    bundle.release = bundle.release_gate
    if output_dir is not None:
        render_bundle(bundle, Path(output_dir))
    return bundle


def _attach_ingestion_audit(bundle: PipelineBundle, load_result: PacketLoadResult) -> None:
    audit_summary = load_result.to_audit_summary()
    bundle.stage_snapshots = [
        snapshot
        for snapshot in bundle.stage_snapshots
        if not (snapshot.stage == "live_lite_ingestion" and snapshot.artifact_type == "packet_ingestion_audit")
    ]
    bundle.stage_snapshots.append(
        StageSnapshot(
            stage="live_lite_ingestion",
            artifact_type="packet_ingestion_audit",
            required_fields=["source_id", "title", "provenance"],
            downstream_must_have_fields={"evidence_ingestion": ["sources", "findings"]},
            contract_ok=not bool(load_result.blocking_issues and not bundle.request.source_packets),
            summary=audit_summary,
        )
    )
    if bundle.evidence is not None:
        _append_unique(
            bundle.evidence.quality_notes,
            [
                _summary_reason(audit_summary.get("rejected_count", 0), "packet(s) were rejected before runtime entry"),
                _summary_reason(audit_summary.get("salvaged_count", 0), "packet(s) were salvaged after dropping malformed content"),
                _summary_reason(audit_summary.get("stale_count", 0), "accepted packet(s) carry stale-source warnings"),
                _summary_reason(audit_summary.get("dedupe_collision_count", 0), "accepted packet(s) share a dedupe collision note"),
            ],
        )
    if bundle.release_gate is not None:
        _append_unique(
            bundle.release_gate.reasons,
            [
                _summary_reason(audit_summary.get("rejected_count", 0), "live-lite packets were rejected before runtime entry"),
                _summary_reason(audit_summary.get("salvaged_count", 0), "live-lite packets were salvaged after dropping malformed content"),
                _summary_reason(audit_summary.get("stale_count", 0), "live-lite stale packet warnings remain in scope"),
            ],
        )


def _summary_reason(count: int, detail: str) -> str:
    if count <= 0:
        return ""
    return f"Live-lite ingestion: {count} {detail}."


def _append_unique(target: list[str], items: list[str]) -> None:
    seen = {entry.casefold() for entry in target if entry}
    for item in items:
        if not item:
            continue
        key = item.casefold()
        if key in seen:
            continue
        target.append(item)
        seen.add(key)


__all__ = ["execute_live_lite_request", "prepare_live_lite_request"]
