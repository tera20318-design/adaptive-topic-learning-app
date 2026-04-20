from __future__ import annotations

from pseudo_pro_v2.stage_contracts import validate_stage_contract_registry, validate_stage_snapshot


def validate_stage_contract_registry_inputs() -> list[str]:
    return validate_stage_contract_registry()


def validate_stage_snapshot_payload(snapshot: dict) -> list[str]:
    return validate_stage_snapshot(snapshot)
