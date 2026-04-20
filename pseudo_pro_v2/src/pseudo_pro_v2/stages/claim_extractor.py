from __future__ import annotations

from pseudo_pro_v2.models import ClaimLedgerRow, ReportDraft, SourceStrategy


def extract_claims(draft: ReportDraft, strategy: SourceStrategy) -> list[ClaimLedgerRow]:
    rows: list[ClaimLedgerRow] = []
    for unit in draft.units:
        if not unit.is_claim:
            continue
        rows.append(
            ClaimLedgerRow(
                claim_id=unit.unit_id.replace("unit", "claim"),
                report_section=unit.section_title,
                exact_text_span=unit.text,
                normalized_claim=" ".join(unit.text.lower().split()),
                claim_kind=unit.claim_kind,
                risk_level=unit.risk_level,
                source_ids=unit.source_ids,
                source_roles=unit.source_roles,
                evidence_count=len(unit.source_ids),
                required_source_role=strategy.required_source_roles_by_claim_kind.get(unit.claim_kind, ["unknown"]),
                required_role_matched=False,
                role_fit_status="unknown",
                support_status=unit.support_status_hint,
                confidence=unit.confidence,
                caveat_required=bool(unit.caveat),
                suggested_tone="standard",
                required_fix=unit.required_fix,
                origin_finding_id=unit.origin_finding_id,
                absence_type=unit.absence_type,
                contradiction_note=unit.contradiction_note,
                included_in_report=unit.include_in_report,
                exclusion_reason=unit.exclusion_reason,
            )
        )
    return rows
