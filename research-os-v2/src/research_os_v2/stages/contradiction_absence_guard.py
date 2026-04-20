from __future__ import annotations

from research_os_v2.catalogs import AUTHORITATIVE_SOURCE_ROLES
from research_os_v2.models import ClaimLedgerRow, ContradictionEntry, EvidenceGapEntry, ReportDraft, ResearchRequest


def apply_contradiction_and_absence_guard(
    claims: list[ClaimLedgerRow],
    draft: ReportDraft,
    request: ResearchRequest,
) -> tuple[list[ClaimLedgerRow], list[ContradictionEntry], list[EvidenceGapEntry]]:
    unit_by_claim_id = {
        unit.unit_id.replace("unit", "claim"): unit
        for unit in draft.units
    }
    contradictions: list[ContradictionEntry] = []
    gaps: list[EvidenceGapEntry] = []
    updated: list[ClaimLedgerRow] = []

    for claim in claims:
        unit = unit_by_claim_id[claim.claim_id]
        support_status = claim.support_status
        required_fix = claim.required_fix

        if unit.contradiction_note:
            contradictions.append(
                ContradictionEntry(
                    claim_id=claim.claim_id,
                    issue_type="contradiction",
                    severity="critical" if claim.risk_level == "high" else "moderate",
                    detail=unit.contradiction_note,
                    action="Resolve the conflict or weaken the claim.",
                )
            )
            if claim.risk_level == "high":
                support_status = "weak"

        if unit.absence_type:
            gaps.append(
                EvidenceGapEntry(
                    claim_id=claim.claim_id,
                    gap_type=unit.absence_type,
                    detail="Absence findings must stay scoped and should not be rewritten as settled facts.",
                    release_impact="high" if claim.risk_level == "high" else "medium",
                    required_fix="State the search scope and limitation explicitly.",
                )
            )
            authoritative_present = bool(set(claim.source_roles) & AUTHORITATIVE_SOURCE_ROLES)
            if claim.risk_level == "high" and not authoritative_present:
                support_status = "missing"
                required_fix = "High-risk absence claims need authoritative confirmation or removal."
            elif unit.absence_type == "not_found_in_scoped_search":
                support_status = "weak"
                required_fix = "Keep this as a scoped search result, not a fact."

        if (
            request.jurisdiction
            and unit.jurisdiction
            and unit.jurisdiction.lower() != request.jurisdiction.lower()
            and claim.claim_kind in {"regulatory", "legal", "medical", "financial"}
        ):
            support_status = "out_of_scope"
            gaps.append(
                EvidenceGapEntry(
                    claim_id=claim.claim_id,
                    gap_type="scope_mismatch",
                    detail=f"Claim evidence is tied to {unit.jurisdiction}, not {request.jurisdiction}.",
                    release_impact="high",
                    required_fix="Re-scope the claim or find jurisdiction-matched evidence.",
                )
            )

        updated.append(
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
                support_status=support_status,
                confidence=claim.confidence,
                caveat_required=claim.caveat_required or support_status != "supported",
                suggested_tone=claim.suggested_tone,
                required_fix=required_fix,
            )
        )

    return updated, contradictions, gaps
