from __future__ import annotations

from cleanroom_runtime.catalogs import (
    DISCOVERY_ONLY_SOURCE_ROLES,
    EXPLICIT_ABSENCE_TYPES,
    HIGH_RISK_CLAIM_KINDS,
    REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND,
    SEARCH_SCOPED_ABSENCE_TYPES,
    WEAK_OVERVIEW_SOURCE_ROLES,
)
from cleanroom_runtime.models import (
    ClaimAuditRow,
    ClaimLedgerRow,
    CitationLedgerRow,
    CollectedEvidence,
    SourceStrategy,
)

_STATUS_ORDER = {
    "supported": 0,
    "scoped_absence": 1,
    "weak": 2,
    "missing": 3,
    "out_of_scope": 4,
    "contradicted": 5,
}


def map_claims_to_evidence(
    claims: list[ClaimLedgerRow],
    evidence: CollectedEvidence,
    strategy: SourceStrategy,
) -> tuple[list[ClaimLedgerRow], list[CitationLedgerRow]]:
    role_lookup = {source.source_id: source.source_role for source in evidence.sources}
    title_lookup = {source.source_id: source.title for source in evidence.sources}
    mapped_claims: list[ClaimLedgerRow] = []
    citations: list[CitationLedgerRow] = []
    citation_index = 1

    for claim in claims:
        roles = _resolve_roles(claim, role_lookup)
        required_roles = list(strategy.required_source_roles_by_claim_kind.get(claim.claim_kind, claim.required_source_roles))
        if not required_roles:
            required_roles = list(REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND.get(claim.claim_kind, ("unknown",)))
        matched_roles = sorted(set(roles) & set(required_roles))

        evaluated_status, diagnostics, required_fix = _evaluate_support(claim, roles, matched_roles, required_roles)
        support_status = _merge_support_status(claim.support_status, evaluated_status)

        updated = ClaimLedgerRow(
            claim_id=claim.claim_id,
            unit_id=claim.unit_id,
            report_section=claim.report_section,
            exact_text_span=claim.exact_text_span,
            normalized_claim=claim.normalized_claim,
            claim_kind=claim.claim_kind,
            risk_level=claim.risk_level,
            source_ids=list(claim.source_ids),
            source_roles=roles,
            evidence_count=max(claim.evidence_count, len(claim.source_ids)),
            required_source_roles=list(required_roles),
            matched_source_roles=matched_roles,
            support_status=support_status,
            confidence=_confidence(claim.confidence, support_status, max(claim.evidence_count, len(claim.source_ids))),
            caveat_required=claim.caveat_required or support_status not in {"supported", "scoped_absence"},
            suggested_tone=_suggested_tone(claim.claim_kind, support_status, roles),
            required_fix=claim.required_fix or required_fix,
            included_in_report=claim.included_in_report,
            absence_scope=claim.absence_scope,
            contradiction_note=claim.contradiction_note,
            jurisdiction=claim.jurisdiction,
            blocking_reasons=_dedupe(list(claim.blocking_reasons) + diagnostics),
            exclusion_reasons=list(claim.exclusion_reasons),
        )
        mapped_claims.append(updated)

        for source_id in updated.source_ids:
            citations.append(
                CitationLedgerRow(
                    citation_id=f"citation-{citation_index:03d}",
                    claim_id=updated.claim_id,
                    report_section=updated.report_section,
                    source_id=source_id,
                    source_role=role_lookup.get(source_id, "unknown"),
                    source_title=title_lookup.get(source_id, source_id),
                    support_status=updated.support_status,
                    included_in_report=updated.included_in_report,
                )
            )
            citation_index += 1

    return mapped_claims, citations


def build_claim_audit_rows(claims: list[ClaimLedgerRow]) -> list[ClaimAuditRow]:
    return [
        ClaimAuditRow(
            claim_id=claim.claim_id,
            report_section=claim.report_section,
            claim_kind=claim.claim_kind,
            risk_level=claim.risk_level,
            support_status=claim.support_status,
            included_in_report=claim.included_in_report,
            blocking_reasons=list(claim.blocking_reasons),
            exclusion_reasons=list(claim.exclusion_reasons),
        )
        for claim in claims
    ]


def _resolve_roles(claim: ClaimLedgerRow, role_lookup: dict[str, str]) -> list[str]:
    roles = set(claim.source_roles)
    if not roles:
        roles = {role_lookup.get(source_id, "unknown") for source_id in claim.source_ids}
    return sorted(roles)


def _evaluate_support(
    claim: ClaimLedgerRow,
    roles: list[str],
    matched_roles: list[str],
    required_roles: list[str],
) -> tuple[str, list[str], str]:
    if claim.contradiction_note:
        return "contradicted", [f"{claim.claim_id} carries a contradiction note and cannot be treated as supported."], "Resolve the contradiction before release."

    if claim.claim_kind == "scope_boundary":
        return "supported", [], ""

    if claim.claim_kind == "absence":
        return _evaluate_absence_claim(claim, roles, matched_roles, required_roles)

    if not claim.source_ids:
        return "missing", [f"{claim.claim_id} has no cited sources."], "Add supporting sources or remove the claim."

    if not matched_roles:
        return "weak", [_role_mismatch_reason(claim, required_roles, roles)], _missing_role_fix(claim)

    role_set = set(roles)
    if role_set and role_set <= DISCOVERY_ONLY_SOURCE_ROLES:
        return "weak", [f"{claim.claim_id} relies only on discovery roles ({', '.join(roles)})."], "Replace discovery-only support with claim-kind-matched sources."

    if role_set and role_set <= WEAK_OVERVIEW_SOURCE_ROLES and claim.claim_kind not in {"market", "comparison"}:
        return "weak", [f"{claim.claim_id} relies only on weak overview roles ({', '.join(roles)})."], "Add a stronger role-matched source before treating the claim as settled."

    return "supported", [], ""


def _evaluate_absence_claim(
    claim: ClaimLedgerRow,
    roles: list[str],
    matched_roles: list[str],
    required_roles: list[str],
) -> tuple[str, list[str], str]:
    if claim.absence_scope is None:
        return "missing", [f"{claim.claim_id} is an absence claim without an explicit scope and could hide a false negative."], "State the checked scope explicitly."

    basis = getattr(claim.absence_scope, "basis", "")
    checked_source_ids = getattr(claim.absence_scope, "checked_source_ids", [])

    if basis in SEARCH_SCOPED_ABSENCE_TYPES and not checked_source_ids:
        return "missing", [f"{claim.claim_id} is a search-based absence claim without checked source lineage."], "Record the checked source IDs or move the claim to uncertainty."

    if basis in EXPLICIT_ABSENCE_TYPES and matched_roles:
        return "supported", [], "Keep the absence scoped to the cited authoritative source."

    if basis in SEARCH_SCOPED_ABSENCE_TYPES:
        if claim.risk_level == "high" and not matched_roles:
            return "missing", [_role_mismatch_reason(claim, required_roles, roles)], _missing_role_fix(claim)
        if not matched_roles:
            return "weak", [_role_mismatch_reason(claim, required_roles, roles)], _missing_role_fix(claim)
        return "scoped_absence", [f"{claim.claim_id} remains a scoped absence claim, not a settled fact."], "Keep the absence scoped and non-definitive."

    if claim.risk_level == "high":
        return "missing", [f"{claim.claim_id} uses an untyped high-risk absence basis and cannot clear release."], "Assign a supported absence basis before release."
    return "weak", [f"{claim.claim_id} uses an untyped absence basis."], "Assign a supported absence basis before release."


def _merge_support_status(existing: str, evaluated: str) -> str:
    return existing if _STATUS_ORDER.get(existing, 0) >= _STATUS_ORDER.get(evaluated, 0) else evaluated


def _confidence(base: float, support_status: str, evidence_count: int) -> float:
    multiplier = {
        "supported": 1.0,
        "scoped_absence": 0.88,
        "weak": 0.72,
        "missing": 0.45,
        "out_of_scope": 0.4,
        "contradicted": 0.35,
    }[support_status]
    bonus = 0.05 if evidence_count >= 2 else 0.0
    return round(min(0.99, max(0.1, base * multiplier + bonus)), 2)


def _suggested_tone(claim_kind: str, support_status: str, roles: list[str]) -> str:
    if support_status == "scoped_absence":
        return "scoped_absence"
    if claim_kind == "inference":
        return "explicit_inference"
    if claim_kind in {"advice", "recommendation"}:
        return "conditional_advice"
    if support_status == "weak":
        return "tentative"
    if support_status in {"missing", "out_of_scope", "contradicted"}:
        return "withhold"
    if set(roles) and set(roles) <= WEAK_OVERVIEW_SOURCE_ROLES:
        return "representative_public_materials"
    return "standard"


def _role_mismatch_reason(claim: ClaimLedgerRow, required_roles: list[str], roles: list[str]) -> str:
    return (
        f"{claim.claim_id} `{claim.claim_kind}` claims require one of "
        f"{', '.join(sorted(required_roles))}, but found {', '.join(sorted(roles)) or 'no source roles'}."
    )


def _missing_role_fix(claim: ClaimLedgerRow) -> str:
    if claim.claim_kind in HIGH_RISK_CLAIM_KINDS or claim.risk_level == "high":
        return "Replace with a claim-kind-matched high-risk source or remove the claim."
    return "Soften the wording or add a claim-kind-matched source."


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item and item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


__all__ = ["build_claim_audit_rows", "map_claims_to_evidence"]
