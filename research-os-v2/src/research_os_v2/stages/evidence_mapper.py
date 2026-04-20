from __future__ import annotations

from research_os_v2.catalogs import AUTHORITATIVE_SOURCE_ROLES, HIGH_RISK_CLAIM_KINDS
from research_os_v2.models import ClaimLedgerRow, ReportDraft


def map_claims_to_evidence(
    claims: list[ClaimLedgerRow],
    draft: ReportDraft,
) -> list[ClaimLedgerRow]:
    unit_by_claim_id = {
        unit.unit_id.replace("unit", "claim"): unit
        for unit in draft.units
    }

    mapped: list[ClaimLedgerRow] = []
    for claim in claims:
        unit = unit_by_claim_id[claim.claim_id]
        claim_roles = set(claim.source_roles)
        required_roles = set(claim.required_source_role)
        authoritative_present = bool(claim_roles & AUTHORITATIVE_SOURCE_ROLES)
        vendor_or_industry_only = bool(claim_roles) and claim_roles <= {
            "vendor_first_party",
            "industry_association",
            "secondary_media",
            "trade_media",
            "unknown",
        }

        support_status = _derive_support_status(
            unit.support_status_hint,
            claim,
            authoritative_present,
            required_roles,
            claim_roles,
            vendor_or_industry_only,
        )
        confidence = _derive_confidence(claim.confidence, support_status, claim.evidence_count)
        suggested_tone = _suggested_tone(claim.claim_kind, support_status, authoritative_present, vendor_or_industry_only)
        required_fix = claim.required_fix or _required_fix(support_status, claim.claim_kind)

        mapped.append(
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
                confidence=confidence,
                caveat_required=claim.caveat_required or support_status != "supported",
                suggested_tone=suggested_tone,
                required_fix=required_fix,
            )
        )
    return mapped


def _derive_support_status(
    support_hint: str,
    claim: ClaimLedgerRow,
    authoritative_present: bool,
    required_roles: set[str],
    claim_roles: set[str],
    vendor_or_industry_only: bool,
) -> str:
    if support_hint == "missing":
        return "missing"
    if support_hint == "weak":
        return "weak"
    if claim.claim_kind == "scope_boundary":
        return "supported"
    if claim.claim_kind == "absence":
        if claim.risk_level == "high" and not authoritative_present:
            return "missing"
        if not claim.source_ids:
            return "missing"
        return "weak"
    if claim.claim_kind in HIGH_RISK_CLAIM_KINDS or claim.risk_level == "high":
        if not claim.source_ids:
            return "missing"
        if not (claim_roles & required_roles or authoritative_present):
            return "weak"
        if vendor_or_industry_only and not authoritative_present:
            return "weak"
        return "supported"
    if not claim.source_ids:
        return "missing"
    if vendor_or_industry_only:
        return "weak"
    return "supported"


def _derive_confidence(base: float, support_status: str, evidence_count: int) -> float:
    multiplier = {
        "supported": 1.0,
        "weak": 0.72,
        "missing": 0.45,
        "out_of_scope": 0.4,
        "not_checked": 0.5,
    }.get(support_status, 0.5)
    evidence_bonus = 0.05 if evidence_count >= 2 else 0.0
    return round(min(0.99, max(0.1, base * multiplier + evidence_bonus)), 2)


def _suggested_tone(
    claim_kind: str,
    support_status: str,
    authoritative_present: bool,
    vendor_only: bool,
) -> str:
    if claim_kind == "inference":
        return "explicit_inference"
    if claim_kind in {"advice", "recommendation"}:
        return "conditional_advice"
    if support_status == "missing":
        return "unverified"
    if support_status == "weak":
        return "tentative"
    if vendor_only and not authoritative_present:
        return "representative_public_materials"
    return "standard"


def _required_fix(support_status: str, claim_kind: str) -> str:
    if support_status == "missing":
        return "Remove from the mainline report or mark as unverified."
    if support_status == "weak":
        return "Soften the wording or add stronger sources."
    if claim_kind == "absence":
        return "Keep the absence scoped and non-definitive."
    return ""
