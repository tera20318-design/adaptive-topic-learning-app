from __future__ import annotations

from typing import Any

from cleanroom_runtime.models import StageSnapshot
from cleanroom_runtime.stage_contracts import (
    STAGE_CONTRACTS,
    StageContractSpec as StageContract,
    audit_stage_output,
    stage_failure_codes,
    stage_snapshot_schema,
    validate_stage_contract_registry,
    validate_stage_snapshot,
    validate_stage_output as _validate_stage_output,
)
from cleanroom_runtime.types import StageFailureCode


def build_stage_snapshot(stage_name: str, payload: Any, **context: Any) -> StageSnapshot:
    _, snapshot = audit_stage_output(stage_name, _coerce_payload(stage_name, payload, context), **context)
    return snapshot


def validate_stage_output(stage_name: str, payload: Any, **context: Any) -> list[str]:
    failures = _validate_stage_output(stage_name, _coerce_payload(stage_name, payload, context), **context)
    return [f"[{failure.code}] {failure.message}" for failure in failures]


def _coerce_payload(stage_name: str, payload: Any, context: dict[str, Any]) -> Any:
    if stage_name == "report_planner" and not isinstance(payload, dict):
        return {"sections": payload}
    if stage_name == "claim_extractor" and not isinstance(payload, dict):
        return {"claims": payload}
    if stage_name == "evidence_mapper" and not isinstance(payload, dict):
        return {"claims": payload, "citations": context.get("citations", [])}
    if stage_name == "contradiction_absence_guard" and not isinstance(payload, dict):
        return {
            "claims": payload,
            "draft": context.get("draft"),
            "contradictions": context.get("contradictions", []),
            "gaps": context.get("gaps", []),
        }
    return payload


__all__ = [
    "STAGE_CONTRACTS",
    "StageFailureCode",
    "StageContract",
    "StageSnapshot",
    "build_stage_snapshot",
    "stage_failure_codes",
    "stage_snapshot_schema",
    "validate_stage_contract_registry",
    "validate_stage_snapshot",
    "validate_stage_output",
]
