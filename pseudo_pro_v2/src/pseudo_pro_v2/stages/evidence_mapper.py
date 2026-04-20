from __future__ import annotations

from pseudo_pro_v2.catalogs import AUTHORITATIVE_SOURCE_ROLES, CRITICAL_HIGH_RISK_CLAIM_KINDS, DISCOVERY_ONLY_SOURCE_ROLES, WEAK_OVERVIEW_SOURCE_ROLES
from pseudo_pro_v2.models import CitationLedgerRow, ClaimLedgerRow, CollectedEvidence, SourceStrategy


EXPLICIT_ABSENCE_TYPES = {
    "explicitly_not_applicable",
    "explicitly_repealed",
    "replaced_by_later_rule",
    "different_subject_matter",
    "contradicted_by_source",
}


def map_claims_to_evidence(
    claims: list[ClaimLedgerRow],
    evidence: CollectedEvidence,
    strategy: SourceStrategy,
) -> tuple[list[ClaimLedgerRow], list[CitationLedgerRow]]:
    title_lookup = {source.source_id: source.title for source in evidence.sources}
    role_lookup = {source.source_id: source.source_role for source in evidence.sources}
    mapped_claims: list[ClaimLedgerRow] = []
    citations: list[CitationLedgerRow] = []

    for claim in claims:
        roles = set(claim.source_roles)
        if not roles:
            roles = {role_lookup.get(source_id, "unknown") for source_id in claim.source_ids}
        required_roles = set(strategy.required_source_roles_by_claim_kind.get(claim.claim_kind, ["unknown"]))
        role_fit_status = _classify_role_fit(claim, roles, required_roles)
        required_role_matched = role_fit_status == "required_match"

        support_status = _support_status(claim, roles, required_role_matched, role_fit_status)
        confidence = _confidence(claim.confidence, support_status, claim.evidence_count)
        suggested_tone = _suggested_tone(claim.claim_kind, support_status, role_fit_status)
        required_fix = claim.required_fix or _required_fix(support_status, claim.claim_kind, role_fit_status)

        updated = ClaimLedgerRow(
            claim_id=claim.claim_id,
            report_section=claim.report_section,
            exact_text_span=claim.exact_text_span,
            normalized_claim=claim.normalized_claim,
            claim_kind=claim.claim_kind,
            risk_level=claim.risk_level,
            source_ids=claim.source_ids,
            source_roles=sorted(roles),
            evidence_count=claim.evidence_count,
            required_source_role=sorted(required_roles),
            required_role_matched=required_role_matched,
            role_fit_status=role_fit_status,
            support_status=support_status,
            confidence=confidence,
            caveat_required=claim.caveat_required or support_status != "supported",
            suggested_tone=suggested_tone,
            required_fix=required_fix,
            origin_finding_id=claim.origin_finding_id,
            absence_type=claim.absence_type,
            contradiction_note=claim.contradiction_note,
            included_in_report=claim.included_in_report,
            exclusion_reason=claim.exclusion_reason,
        )
        mapped_claims.append(updated)

        for source_id in updated.source_ids:
            citations.append(
                CitationLedgerRow(
                    citation_id="pending",
                    claim_id=updated.claim_id,
                    report_section=updated.report_section,
                    source_id=source_id,
                    source_role=role_lookup.get(source_id, "unknown"),
                    source_title=title_lookup.get(source_id, source_id),
                    support_status=updated.support_status,
                    included_in_report=updated.included_in_report,
                    origin_finding_id=updated.origin_finding_id,
                )
            )

    return mapped_claims, citations


def _classify_role_fit(claim: ClaimLedgerRow, roles: set[str], required_roles: set[str]) -> str:
    if not claim.source_ids or not roles:
        return "no_evidence"
    if roles & required_roles:
        return "required_match"
    if roles & AUTHORITATIVE_SOURCE_ROLES:
        return "authoritative_mismatch"
    if roles <= WEAK_OVERVIEW_SOURCE_ROLES or roles <= DISCOVERY_ONLY_SOURCE_ROLES:
        return "weak_only"
    return "unknown"


def _support_status(
    claim: ClaimLedgerRow,
    roles: set[str],
    required_role_matched: bool,
    role_fit_status: str,
) -> str:
    hint = claim.support_status
    if hint == "missing":
        return "missing"
    if hint == "weak":
        return "weak"
    if claim.claim_kind == "scope_boundary":
        return "supported"
    if claim.claim_kind == "absence":
        if claim.absence_type == "not_found_in_scoped_search":
            return "missing" if claim.risk_level == "high" else "weak"
        if not required_role_matched:
            return "missing" if claim.risk_level == "high" else "weak"
        if claim.absence_type in EXPLICIT_ABSENCE_TYPES:
            return "supported"
        return "weak"

    if claim.claim_kind in CRITICAL_HIGH_RISK_CLAIM_KINDS or claim.risk_level == "high":
        if role_fit_status == "no_evidence":
            return "missing"
        if not required_role_matched:
            return "weak"
        return "supported"

    if role_fit_status == "no_evidence":
        return "missing"
    if required_role_matched:
        return "supported"
    if roles <= DISCOVERY_ONLY_SOURCE_ROLES:
        return "weak"
    if roles <= WEAK_OVERVIEW_SOURCE_ROLES and claim.claim_kind not in {"comparison", "market"}:
        return "weak"
    if role_fit_status in {"authoritative_mismatch", "weak_only"}:
        return "weak"
    return "supported"


def _confidence(base: float, support_status: str, evidence_count: int) -> float:
    multiplier = {
        "supported": 1.0,
        "weak": 0.72,
        "missing": 0.45,
        "out_of_scope": 0.4,
        "not_checked": 0.5,
    }[support_status]
    bonus = 0.05 if evidence_count >= 2 else 0.0
    return round(min(0.99, max(0.1, base * multiplier + bonus)), 2)


def _suggested_tone(claim_kind: str, support_status: str, role_fit_status: str) -> str:
    if claim_kind == "inference":
        return "explicit_inference"
    if claim_kind in {"advice", "recommendation"}:
        return "conditional_advice"
    if support_status == "missing":
        return "unverified"
    if support_status == "weak":
        if role_fit_status in {"weak_only", "authoritative_mismatch"}:
            return "representative_public_materials"
        return "tentative"
    return "standard"


def _required_fix(support_status: str, claim_kind: str, role_fit_status: str) -> str:
    if support_status == "missing":
        return "Remove from mainline prose or add stronger support."
    if support_status == "weak" and role_fit_status == "authoritative_mismatch":
        return "Add claim-kind-appropriate source roles before relying on this claim."
    if support_status == "weak":
        return "Soften the wording or add stronger support."
    if claim_kind == "absence":
        return "Keep the absence scoped and explicitly limited."
    return ""
