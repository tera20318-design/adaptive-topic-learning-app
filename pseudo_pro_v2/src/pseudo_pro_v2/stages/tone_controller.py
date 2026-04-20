from __future__ import annotations

from pseudo_pro_v2.models import ClaimLedgerRow, ReportDraft, ReportUnit


def apply_tone_control(draft: ReportDraft, claims: list[ClaimLedgerRow]) -> ReportDraft:
    claim_by_id = {claim.claim_id: claim for claim in claims}
    updated_units: list[ReportUnit] = []
    for unit in draft.units:
        claim = claim_by_id.get(unit.unit_id.replace("unit", "claim"))
        if claim is None or not unit.is_claim:
            updated_units.append(unit)
            continue
        if not claim.included_in_report:
            updated_units.append(
                ReportUnit(
                    unit_id=unit.unit_id,
                    section_key=unit.section_key,
                    section_title=unit.section_title,
                    text=unit.text,
                    claim_kind=unit.claim_kind,
                    risk_level=unit.risk_level,
                    source_ids=unit.source_ids,
                    source_roles=unit.source_roles,
                    confidence=unit.confidence,
                    support_status_hint=unit.support_status_hint,
                    absence_type=unit.absence_type,
                    contradiction_note=unit.contradiction_note,
                    caveat=unit.caveat,
                    required_fix=unit.required_fix,
                    jurisdiction=unit.jurisdiction,
                    origin_finding_id=unit.origin_finding_id,
                    is_claim=unit.is_claim,
                    include_in_report=False,
                    exclusion_reason=claim.exclusion_reason,
                )
            )
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
                contradiction_note=unit.contradiction_note,
                caveat=unit.caveat,
                required_fix=unit.required_fix,
                jurisdiction=unit.jurisdiction,
                origin_finding_id=unit.origin_finding_id,
                is_claim=unit.is_claim,
                include_in_report=True,
                exclusion_reason=claim.exclusion_reason,
            )
        )
    return ReportDraft(title=draft.title, sections=draft.sections, units=updated_units)


def _tone_text(text: str, claim: ClaimLedgerRow) -> str:
    if claim.suggested_tone == "standard":
        return text
    if claim.suggested_tone == "explicit_inference":
        return f"Report inference: {text}"
    if claim.suggested_tone == "tentative":
        return f"The available evidence suggests that {_sentence_case_tail(text)}"
    if claim.suggested_tone == "representative_public_materials":
        return f"Representative public materials suggest that {_sentence_case_tail(text)}"
    if claim.suggested_tone == "unverified":
        return f"This run did not verify the following claim: {text}"
    if claim.suggested_tone == "conditional_advice":
        return f"Decision guidance, subject to verification: {text}"
    raise ValueError(f"Unknown tone mode `{claim.suggested_tone}`.")


def _sentence_case_tail(text: str) -> str:
    if not text:
        return text
    return text[0].lower() + text[1:]
