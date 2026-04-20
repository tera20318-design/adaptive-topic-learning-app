from __future__ import annotations

from cleanroom_runtime.models import ClaimLedgerRow, ReportDraft, ReportUnit


def apply_tone_control(draft: ReportDraft, claims: list[ClaimLedgerRow]) -> ReportDraft:
    claim_by_unit_id = {claim.unit_id: claim for claim in claims}
    updated_units: list[ReportUnit] = []

    for unit in draft.units:
        claim = claim_by_unit_id.get(unit.unit_id)
        if claim is None or not unit.include_in_report or not unit.is_claim:
            updated_units.append(unit)
            continue

        updated_units.append(
            ReportUnit(
                unit_id=unit.unit_id,
                section_key=unit.section_key,
                section_title=unit.section_title,
                text=_apply_tone(unit.text, claim),
                claim_kind=unit.claim_kind,
                risk_level=unit.risk_level,
                source_ids=list(unit.source_ids),
                source_roles=list(unit.source_roles),
                confidence=unit.confidence,
                support_status_hint=claim.support_status,
                caveat=unit.caveat,
                required_fix=unit.required_fix,
                contradiction_note=unit.contradiction_note,
                jurisdiction=unit.jurisdiction,
                absence_scope=unit.absence_scope,
                is_claim=unit.is_claim,
                include_in_report=unit.include_in_report,
            )
        )

    return ReportDraft(title=draft.title, sections=draft.sections, units=updated_units)


def _apply_tone(text: str, claim: ClaimLedgerRow) -> str:
    if claim.support_status == "weak":
        return _prefix(text, "Current checked materials suggest")
    if claim.support_status == "scoped_absence" and claim.absence_scope:
        return f"Within the checked scope ({claim.absence_scope.scope_label}), no evidence was found for {claim.absence_scope.subject}."
    if claim.claim_kind == "inference":
        return _prefix(text, "The checked materials support the following inference")
    if claim.claim_kind in {"advice", "recommendation"}:
        return _prefix(text, "Before acting")
    return text


def _prefix(text: str, prefix: str) -> str:
    lowered = text.lower()
    if lowered.startswith(prefix.lower()):
        return text
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return f"{prefix}: {text}"
