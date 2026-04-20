from __future__ import annotations

from cleanroom_runtime.catalogs import (
    DISCOVERY_ONLY_SOURCE_ROLES,
    EXPLICIT_ABSENCE_TYPES,
    HIGH_RISK_CLAIM_KINDS,
    REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND,
    SEARCH_SCOPED_ABSENCE_TYPES,
    WEAK_OVERVIEW_SOURCE_ROLES,
)
from cleanroom_runtime.models import CitationLedgerRow, ClaimLedgerRow, CollectedEvidence, SourceFinding, SourceStrategy

_STATUS_ORDER = {
    "supported": 0,
    "scoped_absence": 1,
    "weak": 2,
    "missing": 3,
    "out_of_scope": 4,
    "contradicted": 5,
}
_CRITICAL_PROVENANCE_FIELDS = frozenset({"source_id", "title", "source_role"})


def map_claims_to_evidence(
    claims: list[ClaimLedgerRow],
    evidence: CollectedEvidence,
    strategy: SourceStrategy,
) -> tuple[list[ClaimLedgerRow], list[CitationLedgerRow]]:
    source_lookup = {source.source_id: source for source in evidence.sources}
    finding_lookup = {finding.finding_id: finding for finding in evidence.findings}
    mapped_claims: list[ClaimLedgerRow] = []
    citations: list[CitationLedgerRow] = []
    citation_index = 1

    for claim in claims:
        required_roles = list(strategy.required_source_roles_by_claim_kind.get(claim.claim_kind, claim.required_source_roles))
        if not required_roles:
            required_roles = list(REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND.get(claim.claim_kind, ("unknown",)))

        origin_findings = [
            finding_lookup[finding_id]
            for finding_id in claim.origin_finding_ids
            if finding_id in finding_lookup
        ]
        roles = _resolve_roles(claim, source_lookup, origin_findings)
        matched_roles = sorted(set(roles) & set(required_roles))
        provenance_notes, provenance_complete = _provenance_diagnostics(claim, source_lookup)
        evaluated_status, diagnostics, required_fix = _evaluate_support(
            claim,
            roles,
            matched_roles,
            required_roles,
            origin_findings,
            source_lookup,
            provenance_complete=provenance_complete,
        )
        support_status = _merge_support_status(claim.support_status, evaluated_status)
        blocking_reasons = _dedupe([*claim.blocking_reasons, *provenance_notes, *diagnostics])
        exclusion_reasons = list(claim.exclusion_reasons)
        if claim.risk_level == "high" and support_status not in {"supported", "scoped_absence"}:
            exclusion_reasons.append("unsupported high-risk claim kept in audit only")

        trace_status = _claim_trace_status(claim, origin_findings, provenance_complete, source_lookup)
        subject_key = next((finding.subject_key for finding in origin_findings if finding.subject_key), claim.subject_key)
        freshness_tag = _freshness_tag(updated_source_ids=claim.source_ids, source_lookup=source_lookup)
        finding_span_labels, finding_span_starts, finding_span_ends = _flatten_finding_spans(origin_findings)
        grounding_marker = next((finding.grounding_marker for finding in origin_findings if finding.grounding_marker), "")
        grounding_scope_note = " ".join(
            dict.fromkeys(
                note
                for note in [
                    *(finding.grounding_scope_note for finding in origin_findings if finding.grounding_scope_note),
                    *(finding.scope_note for finding in origin_findings if finding.scope_note),
                ]
                if note
            )
        )
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
            origin_finding_ids=list(dict.fromkeys(claim.origin_finding_ids)),
            report_span_id=claim.report_span_id or claim.unit_id,
            report_line_start=claim.report_line_start,
            report_line_end=claim.report_line_end,
            claim_span_start=claim.claim_span_start,
            claim_span_end=claim.claim_span_end,
            finding_span_labels=finding_span_labels,
            finding_span_starts=finding_span_starts,
            finding_span_ends=finding_span_ends,
            grounding_marker=grounding_marker,
            grounding_scope_note=grounding_scope_note,
            trace_status=trace_status,
            included_in_report=claim.included_in_report,
            absence_type=claim.absence_type,
            absence_scope=claim.absence_scope,
            contradiction_note=claim.contradiction_note,
            jurisdiction=claim.jurisdiction,
            subject_key=subject_key,
            freshness_tag=freshness_tag or claim.freshness_tag,
            blocking_reasons=blocking_reasons,
            exclusion_reasons=_dedupe(exclusion_reasons),
            report_section_key=claim.report_section_key,
        )
        mapped_claims.append(updated)

        for source_id in updated.source_ids:
            source = source_lookup.get(source_id)
            related_findings = [finding for finding in origin_findings if source_id in finding.source_ids]
            excerpt = next((finding.source_excerpt for finding in related_findings if finding.source_excerpt), "")
            span_labels, span_starts, span_ends = _flatten_finding_spans(related_findings)
            span_label = _combined_span_label(span_labels)
            span_start = span_starts[0] if span_starts else None
            span_end = span_ends[-1] if span_ends else None
            citation_trace_status = (
                "linked"
                if source is not None
                and related_findings
                and (not _citation_requires_grounded_spans(source, related_findings) or _has_grounded_spans(related_findings))
                else "mismatch"
            )
            citation_provenance_complete = bool(
                source
                and source.provenance.metadata_consistent
                and source.provenance.citation_trace_complete
                and not source.provenance.malformed
                and source.provenance.role_inference_status != "ambiguous"
                and (not _citation_requires_grounded_spans(source, related_findings) or _has_grounded_spans(related_findings))
            )
            if _document_trace_gap(claim, related_findings, source_lookup):
                citation_trace_status = "mismatch"
                citation_provenance_complete = False
            citations.append(
                CitationLedgerRow(
                    citation_id=f"citation-{citation_index:03d}",
                    claim_id=updated.claim_id,
                    report_section=updated.report_section,
                    source_id=source_id,
                    source_role=source.source_role if source is not None else "unknown",
                    source_title=source.title if source is not None else source_id,
                    support_status=updated.support_status,
                    included_in_report=updated.included_in_report,
                    report_span_id=updated.report_span_id,
                    claim_span_start=updated.claim_span_start,
                    claim_span_end=updated.claim_span_end,
                    source_finding_ids=[finding.finding_id for finding in related_findings],
                    source_excerpt=excerpt,
                    source_span_label=span_label,
                    source_span_start=span_start,
                    source_span_end=span_end,
                    source_span_labels=span_labels,
                    source_span_starts=span_starts,
                    source_span_ends=span_ends,
                    grounding_marker=next((finding.grounding_marker for finding in related_findings if finding.grounding_marker), ""),
                    grounding_scope_note=" ".join(
                        dict.fromkeys(
                            note
                            for note in [
                                *(finding.grounding_scope_note for finding in related_findings if finding.grounding_scope_note),
                                *(finding.scope_note for finding in related_findings if finding.scope_note),
                            ]
                            if note
                        )
                    ),
                    trace_status=citation_trace_status,
                    provenance_complete=citation_provenance_complete,
                )
            )
            citation_index += 1

    return mapped_claims, citations


def _resolve_roles(
    claim: ClaimLedgerRow,
    source_lookup: dict[str, object],
    origin_findings: list[SourceFinding],
) -> list[str]:
    roles: list[str] = []
    seen: set[str] = set()
    for source_id in claim.source_ids:
        source = source_lookup.get(source_id)
        role = getattr(source, "source_role", "unknown")
        if role not in seen:
            roles.append(role)
            seen.add(role)
    for finding in origin_findings:
        for role in finding.source_roles:
            if role not in seen:
                roles.append(role)
                seen.add(role)
    for role in claim.source_roles:
        if role not in seen:
            roles.append(role)
            seen.add(role)
    return roles


def _evaluate_support(
    claim: ClaimLedgerRow,
    roles: list[str],
    matched_roles: list[str],
    required_roles: list[str],
    origin_findings: list[SourceFinding],
    source_lookup: dict[str, object],
    *,
    provenance_complete: bool,
) -> tuple[str, list[str], str]:
    if claim.contradiction_note:
        return "contradicted", [f"{claim.claim_id} carries a contradiction note and cannot be treated as supported."], "Resolve the contradiction before release."

    if claim.claim_kind == "scope_boundary":
        return "supported", [], ""

    if claim.claim_kind == "absence":
        return _evaluate_absence_claim(claim, roles, matched_roles, required_roles, provenance_complete=provenance_complete)

    document_status, document_diagnostics, document_fix = _evaluate_document_grounding(
        claim,
        roles,
        origin_findings,
        source_lookup,
    )
    if document_status is not None:
        return document_status, document_diagnostics, document_fix

    if not claim.source_ids:
        return "missing", [f"{claim.claim_id} has no cited sources."], "Add supporting sources or remove the claim."

    if claim.risk_level == "high" and not provenance_complete:
        return "missing", [f"{claim.claim_id} relies on sources without complete provenance or citation trace."], "Repair source provenance and citation trace before release."

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
    *,
    provenance_complete: bool,
) -> tuple[str, list[str], str]:
    if claim.absence_scope is None:
        return "missing", [f"{claim.claim_id} is an absence claim without an explicit scope and could hide a false negative."], "State the checked scope explicitly."

    basis = getattr(claim.absence_scope, "basis", "")
    checked_source_ids = getattr(claim.absence_scope, "checked_source_ids", [])

    if basis in SEARCH_SCOPED_ABSENCE_TYPES and not checked_source_ids:
        return "missing", [f"{claim.claim_id} is a search-based absence claim without checked source lineage."], "Record the checked source IDs or move the claim to uncertainty."

    if claim.risk_level == "high" and not provenance_complete:
        return "missing", [f"{claim.claim_id} lacks complete provenance for a high-risk absence claim."], "Repair source provenance before release."

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


def _provenance_diagnostics(
    claim: ClaimLedgerRow,
    source_lookup: dict[str, object],
) -> tuple[list[str], bool]:
    diagnostics: list[str] = []
    complete = True
    for source_id in claim.source_ids:
        source = source_lookup.get(source_id)
        if source is None:
            diagnostics.append(f"{claim.claim_id} references unknown source `{source_id}`.")
            complete = False
            continue
        provenance = source.provenance
        critical_missing = sorted(set(provenance.metadata_missing_fields) & _CRITICAL_PROVENANCE_FIELDS)
        if critical_missing and claim.risk_level == "high":
            diagnostics.append(
                f"{claim.claim_id} uses `{source_id}` with missing provenance fields: {', '.join(critical_missing)}."
            )
            complete = False
        if not provenance.metadata_consistent:
            diagnostics.append(f"{claim.claim_id} uses `{source_id}` with inconsistent metadata.")
            complete = False
        if not provenance.citation_trace_complete:
            diagnostics.append(f"{claim.claim_id} uses `{source_id}` with incomplete citation trace.")
            complete = False
        if provenance.malformed:
            diagnostics.append(f"{claim.claim_id} uses `{source_id}` marked as malformed source input.")
            complete = False
        if provenance.role_inference_status == "ambiguous" and claim.risk_level == "high":
            diagnostics.append(f"{claim.claim_id} uses `{source_id}` with ambiguous source-role inference.")
            complete = False
    return _dedupe(diagnostics), complete


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


def _claim_trace_status(
    claim: ClaimLedgerRow,
    origin_findings: list[SourceFinding],
    provenance_complete: bool,
    source_lookup: dict[str, object],
) -> str:
    if not claim.included_in_report:
        return "audit_only"
    if not claim.report_span_id:
        return "mismatch"
    if claim.source_ids and not origin_findings:
        return "mismatch"
    if _claim_needs_grounded_spans(claim, origin_findings) and not _has_grounded_spans(origin_findings):
        return "mismatch"
    if _document_trace_gap(claim, origin_findings, source_lookup):
        return "mismatch"
    if claim.risk_level == "high" and not provenance_complete:
        return "mismatch"
    return "linked"


def _freshness_tag(updated_source_ids: list[str], source_lookup: dict[str, object]) -> str:
    if not updated_source_ids:
        return ""
    stale_values = [
        getattr(getattr(source_lookup.get(source_id), "provenance", None), "stale", False)
        for source_id in updated_source_ids
        if source_lookup.get(source_id) is not None
    ]
    if stale_values and all(stale_values):
        return "stale"
    if stale_values and any(value is False for value in stale_values):
        return "fresh"
    return ""


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item and item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


def _evaluate_document_grounding(
    claim: ClaimLedgerRow,
    roles: list[str],
    origin_findings: list[SourceFinding],
    source_lookup: dict[str, object],
) -> tuple[str | None, list[str], str]:
    document_findings = [finding for finding in origin_findings if _uses_user_document(finding.source_ids, finding.source_roles, source_lookup)]
    if not document_findings and "user_provided_source" not in roles:
        return None, [], ""
    if not document_findings and "user_provided_source" in roles:
        status = "missing" if claim.risk_level == "high" else "weak"
        return status, [f"{claim.claim_id} cites a user document without inspectable finding lineage."], "Restore direct grounded finding lineage before release."
    if any(finding.grounding_marker == "unsupported_span_synthesis" for finding in document_findings):
        status = "missing" if claim.risk_level == "high" else "weak"
        return (
            status,
            [f"{claim.claim_id} synthesizes separate document spans without direct grounding."],
            "Keep separate checked spans separate, or rewrite the claim as bounded uncertainty.",
        )
    if len(document_findings) > 1 and claim.claim_kind != "scope_boundary":
        status = "missing" if claim.risk_level == "high" else "weak"
        return (
            status,
            [f"{claim.claim_id} combines separate checked document findings into one reader-facing claim."],
            "Split the claim by grounded document span, or keep the synthesis out of reader-facing prose.",
        )
    if not _has_grounded_spans(document_findings):
        status = "missing" if claim.risk_level == "high" else "weak"
        return (
            status,
            [f"{claim.claim_id} lacks complete document excerpt span grounding."],
            "Add grounded excerpt spans before treating the document claim as supported.",
        )
    if not all(_is_scope_limited_document_finding(finding) for finding in document_findings):
        status = "missing" if claim.risk_level == "high" else "weak"
        return (
            status,
            [f"{claim.claim_id} is not visibly limited to the checked document scope."],
            "Keep the claim limited to what the checked document says directly.",
        )
    if set(roles) == {"user_provided_source"} and (
        claim.claim_kind in HIGH_RISK_CLAIM_KINDS or claim.claim_kind in {"advice", "recommendation"}
    ):
        return (
            "missing",
            [f"{claim.claim_id} treats a checked document excerpt as broader high-risk authority."],
            "Keep the claim at 'the checked document states ...' scope, or add external role-matched support.",
        )
    if set(roles) == {"user_provided_source"} and claim.claim_kind != "scope_boundary" and not _has_direct_grounding_language(claim.exact_text_span):
        status = "missing" if claim.risk_level == "high" else "weak"
        return (
            status,
            [f"{claim.claim_id} summary prose outruns the grounded document span."],
            "Use direct grounding language and stay within the checked document span.",
        )
    return None, [], ""


def _uses_user_document(source_ids: list[str], source_roles: list[str], source_lookup: dict[str, object]) -> bool:
    if "user_provided_source" in source_roles:
        return True
    for source_id in source_ids:
        source = source_lookup.get(source_id)
        if source is not None and getattr(source, "source_role", "") == "user_provided_source":
            return True
    return False


def _has_direct_grounding_language(text: str) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in ("checked document", "checked excerpt", "checked materials", "uploaded document"))


def _is_scope_limited_document_finding(finding: SourceFinding) -> bool:
    if "scope_limited_document" in finding.tags:
        return True
    scope_note = " ".join([finding.scope_note, getattr(finding, "grounding_scope_note", "")]).casefold()
    return "checked document" in scope_note or "checked excerpt" in scope_note or "scope" in scope_note


def _claim_needs_grounded_spans(claim: ClaimLedgerRow, origin_findings: list[SourceFinding]) -> bool:
    if any("user_provided_source" in finding.source_roles for finding in origin_findings):
        return True
    return any(getattr(finding, "grounding_marker", "") for finding in origin_findings)


def _has_grounded_spans(findings: list[SourceFinding]) -> bool:
    if not findings:
        return False
    for finding in findings:
        labels = list(getattr(finding, "source_span_labels", []))
        starts = list(getattr(finding, "source_span_starts", []))
        ends = list(getattr(finding, "source_span_ends", []))
        if not labels and finding.source_span_label:
            labels = [finding.source_span_label]
        if not starts and finding.source_span_start is not None:
            starts = [finding.source_span_start]
        if not ends and finding.source_span_end is not None:
            ends = [finding.source_span_end]
        if not finding.source_excerpt.strip():
            return False
        if not starts or not ends or len(starts) != len(ends):
            return False
        if labels and len(labels) != len(starts):
            return False
    return True


def _document_trace_gap(
    claim: ClaimLedgerRow,
    origin_findings: list[SourceFinding],
    source_lookup: dict[str, object],
) -> bool:
    document_findings = [
        finding for finding in origin_findings if _uses_user_document(finding.source_ids, finding.source_roles, source_lookup)
    ]
    if not document_findings:
        return False
    if any(finding.grounding_marker == "unsupported_span_synthesis" for finding in document_findings):
        return True
    if len(document_findings) > 1 and claim.claim_kind != "scope_boundary":
        return True
    if not _has_grounded_spans(document_findings):
        return True
    if set(claim.source_roles) == {"user_provided_source"} and claim.claim_kind != "scope_boundary" and not _has_direct_grounding_language(claim.exact_text_span):
        return True
    return False


def _citation_requires_grounded_spans(source, related_findings: list[SourceFinding]) -> bool:
    if getattr(source, "source_role", "") == "user_provided_source":
        return True
    return any(getattr(finding, "grounding_marker", "") for finding in related_findings)


def _flatten_finding_spans(findings: list[SourceFinding]) -> tuple[list[str], list[int], list[int]]:
    labels: list[str] = []
    starts: list[int] = []
    ends: list[int] = []
    for finding in findings:
        local_labels = list(getattr(finding, "source_span_labels", [])) or ([finding.source_span_label] if finding.source_span_label else [])
        local_starts = list(getattr(finding, "source_span_starts", [])) or ([finding.source_span_start] if finding.source_span_start is not None else [])
        local_ends = list(getattr(finding, "source_span_ends", [])) or ([finding.source_span_end] if finding.source_span_end is not None else [])
        if local_labels and len(local_labels) == len(local_starts) == len(local_ends):
            labels.extend(local_labels)
            starts.extend(local_starts)
            ends.extend(local_ends)
        elif local_starts and len(local_starts) == len(local_ends):
            labels.extend(f"{finding.source_span_label or 'span'} {index + 1}" for index in range(len(local_starts)))
            starts.extend(local_starts)
            ends.extend(local_ends)
    return labels, starts, ends


def _combined_span_label(labels: list[str]) -> str:
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    return ", ".join(dict.fromkeys(labels))


__all__ = ["map_claims_to_evidence"]
