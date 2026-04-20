from __future__ import annotations

from cleanroom_runtime.models import ClaimLedgerRow, ReportDraft, SourceStrategy
from cleanroom_runtime.utils import normalize_text


def extract_claims(draft: ReportDraft, strategy: SourceStrategy) -> list[ClaimLedgerRow]:
    claims: list[ClaimLedgerRow] = []
    claim_index = 1
    for unit in draft.units:
        if not unit.is_claim:
            continue
        required_roles = list(strategy.required_source_roles_by_claim_kind.get(unit.claim_kind, ["unknown"]))
        claim_id = f"claim-{claim_index:03d}"
        claim_index += 1
        claims.append(
            ClaimLedgerRow(
                claim_id=claim_id,
                unit_id=unit.unit_id,
                report_section=unit.section_title,
                exact_text_span=unit.text,
                normalized_claim=normalize_text(unit.text),
                claim_kind=unit.claim_kind,
                risk_level=unit.risk_level,
                source_ids=list(unit.source_ids),
                source_roles=list(unit.source_roles),
                evidence_count=len(unit.source_ids),
                required_source_roles=required_roles,
                matched_source_roles=[],
                support_status=unit.support_status_hint or ("supported" if unit.source_ids or unit.claim_kind == "scope_boundary" else "missing"),
                confidence=unit.confidence,
                caveat_required=bool(unit.caveat),
                suggested_tone="standard",
                required_fix=unit.required_fix,
                origin_finding_ids=[unit.finding_id] if unit.finding_id else [],
                report_span_id=unit.unit_id,
                trace_status="linked" if unit.finding_id or not unit.source_ids else "unmapped",
                included_in_report=unit.include_in_report,
                finding_span_labels=list(unit.source_span_labels),
                finding_span_starts=list(unit.source_span_starts),
                finding_span_ends=list(unit.source_span_ends),
                grounding_marker=unit.grounding_marker,
                grounding_scope_note=unit.grounding_scope_note,
                absence_type=getattr(unit.absence_scope, "basis", "") if unit.absence_scope is not None else "",
                absence_scope=unit.absence_scope,
                contradiction_note=unit.contradiction_note,
                jurisdiction=unit.jurisdiction,
                subject_key=unit.subject_key or normalize_text(unit.text),
                freshness_tag=unit.freshness_tag,
                report_section_key=unit.section_key,
            )
        )
    return claims
