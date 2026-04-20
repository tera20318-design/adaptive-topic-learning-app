from __future__ import annotations

from research_os_v2.models import ClaimLedgerRow, ReportDraft, ReportUnit


def apply_tone_control(draft: ReportDraft, claims: list[ClaimLedgerRow]) -> ReportDraft:
    claim_by_id = {claim.claim_id: claim for claim in claims}
    updated_units: list[ReportUnit] = []
    for unit in draft.units:
        claim = claim_by_id.get(unit.unit_id.replace("unit", "claim"))
        if claim is None:
            updated_units.append(unit)
            continue
        updated_units.append(
            ReportUnit(
                unit_id=unit.unit_id,
                section_key=unit.section_key,
                section_title=unit.section_title,
                text=_tone_text(unit.text, claim),
                claim_kind=unit.claim_kind,
                risk_level=unit.risk_level,
                source_ids=unit.source_ids,
                source_roles=unit.source_roles,
                confidence=unit.confidence,
                support_status_hint=unit.support_status_hint,
                absence_type=unit.absence_type,
                jurisdiction=unit.jurisdiction,
                contradiction_note=unit.contradiction_note,
                caveat=unit.caveat,
                required_fix=unit.required_fix,
                is_claim=unit.is_claim,
            )
        )
    return ReportDraft(
        title=draft.title,
        sections=draft.sections,
        units=updated_units,
        markdown=draft.markdown,
    )


def _tone_text(text: str, claim: ClaimLedgerRow) -> str:
    if claim.suggested_tone == "unverified":
        return f"未確認: {text}" if _contains_cjk(text) else f"Unverified in this run: {text}"
    if claim.suggested_tone == "tentative":
        if _contains_cjk(text):
            return f"追加確認前提で述べると、{text}"
        return f"The available evidence suggests that {text[0].lower() + text[1:] if text else text}"
    if claim.suggested_tone == "representative_public_materials":
        if _contains_cjk(text):
            return f"公開資料の範囲では、{text}"
        return f"Public materials suggest that {text[0].lower() + text[1:] if text else text}"
    if claim.suggested_tone == "explicit_inference":
        return f"本レポートの推論: {text}" if _contains_cjk(text) else f"Report inference: {text}"
    if claim.suggested_tone == "conditional_advice":
        return text
    return text


def _contains_cjk(text: str) -> bool:
    return any(
        "\u3040" <= char <= "\u30ff"
        or "\u3400" <= char <= "\u4dbf"
        or "\u4e00" <= char <= "\u9fff"
        for char in text
    )
