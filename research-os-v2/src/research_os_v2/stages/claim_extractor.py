from __future__ import annotations

from research_os_v2.models import ClaimLedgerRow, ReportDraft, SourceStrategy


def extract_claims(draft: ReportDraft, strategy: SourceStrategy) -> list[ClaimLedgerRow]:
    rows: list[ClaimLedgerRow] = []
    for unit in draft.units:
        if not unit.is_claim or unit.section_key == "sources":
            continue
        required_roles = strategy.required_source_roles.get(unit.claim_kind, ["unknown"])
        rows.append(
            ClaimLedgerRow(
                claim_id=unit.unit_id.replace("unit", "claim"),
                report_section=unit.section_title,
                exact_text_span=unit.text,
                normalized_claim=_normalize_claim(unit.text),
                claim_kind=unit.claim_kind,
                risk_level=unit.risk_level,
                source_ids=unit.source_ids,
                source_roles=unit.source_roles,
                evidence_count=len(unit.source_ids),
                required_source_role=required_roles,
                support_status="not_checked",
                confidence=unit.confidence,
                caveat_required=bool(unit.caveat or not unit.source_ids),
                suggested_tone="pending",
                required_fix=unit.required_fix,
            )
        )
    return rows


def _normalize_claim(text: str) -> str:
    return " ".join(text.lower().split())
