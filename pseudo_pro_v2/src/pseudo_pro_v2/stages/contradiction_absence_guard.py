from __future__ import annotations

from pseudo_pro_v2.catalogs import CRITICAL_HIGH_RISK_CLAIM_KINDS
from pseudo_pro_v2.models import ClaimLedgerRow, ContradictionEntry, EvidenceGapEntry, ReportDraft, ReportUnit, RunRequest


def apply_contradiction_absence_guard(
    claims: list[ClaimLedgerRow],
    draft: ReportDraft,
    request: RunRequest,
) -> tuple[list[ClaimLedgerRow], ReportDraft, list[ContradictionEntry], list[EvidenceGapEntry]]:
    claim_by_unit_id = {claim.claim_id: claim for claim in claims}
    contradictions: list[ContradictionEntry] = []
    gaps: list[EvidenceGapEntry] = []
    updated_claims: list[ClaimLedgerRow] = []
    updated_units: list[ReportUnit] = []

    for unit in draft.units:
        claim = claim_by_unit_id.get(unit.unit_id.replace("unit", "claim"))
        if claim is None:
            updated_units.append(unit)
            continue

        support_status = claim.support_status
        include_in_report = unit.include_in_report
        required_fix = claim.required_fix
        exclusion_reason = claim.exclusion_reason

        if claim.contradiction_note:
            contradictions.append(
                ContradictionEntry(
                    claim_id=claim.claim_id,
                    detail=claim.contradiction_note,
                    severity="critical" if claim.risk_level == "high" else "moderate",
                )
            )
            support_status = "missing" if claim.risk_level == "high" else "weak"
            required_fix = "Resolve the contradiction or remove the claim."
            if claim.risk_level == "high":
                include_in_report = False
                exclusion_reason = "Suppressed because a high-risk contradiction remains unresolved."

        if claim.claim_kind == "absence":
            gaps.append(
                EvidenceGapEntry(
                    claim_id=claim.claim_id,
                    gap_type=claim.absence_type or "absence",
                    detail="Absence claims must remain scoped and must not be rewritten as settled facts.",
                    required_fix="Keep absence scoped, limited, and non-definitive.",
                    severity="high" if claim.risk_level == "high" else "medium",
                )
            )
            if claim.absence_type == "not_found_in_scoped_search":
                support_status = "missing" if claim.risk_level == "high" else "weak"
            if claim.risk_level == "high" and support_status != "supported":
                include_in_report = False
                exclusion_reason = "Unsupported high-risk absence removed from reader-facing prose."
                required_fix = "Do not include unsupported high-risk absence in mainline prose."

        if (
            request.jurisdiction
            and unit.jurisdiction
            and request.jurisdiction != unit.jurisdiction
            and claim.claim_kind in CRITICAL_HIGH_RISK_CLAIM_KINDS
        ):
            support_status = "out_of_scope"
            include_in_report = False
            exclusion_reason = "Removed because the evidence does not match the requested jurisdiction."
            gaps.append(
                EvidenceGapEntry(
                    claim_id=claim.claim_id,
                    gap_type="scope_mismatch",
                    detail="Claim evidence does not match the requested jurisdiction.",
                    required_fix="Use jurisdiction-matched evidence or remove the claim.",
                    severity="high",
                )
            )

        if claim.risk_level == "high" and support_status != "supported":
            include_in_report = False
            if not exclusion_reason:
                exclusion_reason = "Unsupported high-risk claim removed from reader-facing prose."

        updated_claims.append(
            ClaimLedgerRow(
                claim_id=claim.claim_id,
                report_section=claim.report_section,
                exact_text_span=claim.exact_text_span,
                normalized_claim=claim.normalized_claim,
                claim_kind=claim.claim_kind,
                risk_level=claim.risk_level,
                source_ids=claim.source_ids,
                source_roles=claim.source_roles,
                evidence_count=claim.evidence_count,
                required_source_role=claim.required_source_role,
                required_role_matched=claim.required_role_matched,
                role_fit_status=claim.role_fit_status,
                support_status=support_status,
                confidence=claim.confidence,
                caveat_required=claim.caveat_required or support_status != "supported",
                suggested_tone=claim.suggested_tone,
                required_fix=required_fix,
                origin_finding_id=claim.origin_finding_id,
                absence_type=claim.absence_type,
                contradiction_note=claim.contradiction_note,
                included_in_report=include_in_report,
                exclusion_reason=exclusion_reason,
            )
        )
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
                support_status_hint=support_status,
                absence_type=unit.absence_type,
                contradiction_note=unit.contradiction_note,
                caveat=unit.caveat,
                required_fix=required_fix,
                jurisdiction=unit.jurisdiction,
                origin_finding_id=unit.origin_finding_id,
                is_claim=unit.is_claim,
                include_in_report=include_in_report,
                exclusion_reason=exclusion_reason,
            )
        )

    return updated_claims, ReportDraft(title=draft.title, sections=draft.sections, units=updated_units), contradictions, gaps
