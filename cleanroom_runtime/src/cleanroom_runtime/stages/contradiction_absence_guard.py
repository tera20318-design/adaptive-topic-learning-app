from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

from cleanroom_runtime.catalogs import (
    AUTHORITATIVE_SOURCE_ROLES,
    CRITICAL_HIGH_RISK_CLAIM_KINDS,
    EXPLICIT_ABSENCE_TYPES,
    SEARCH_SCOPED_ABSENCE_TYPES,
    UNSUPPORTED_SUPPORT_STATUSES,
)
from cleanroom_runtime.models import (
    ClaimLedgerRow,
    CollectedEvidence,
    ContradictionEntry,
    EvidenceGapEntry,
    ReportDraft,
    ReportUnit,
    RunRequest,
    SourceFinding,
)
from cleanroom_runtime.utils import normalize_text

_CURRENTNESS_MARKERS = (
    " currently ",
    " current ",
    " today ",
    " now ",
    " as of ",
    " remains ",
    " still ",
    " in force ",
    " latest ",
    " present-day ",
)


def apply_contradiction_absence_guard(
    claims: list[ClaimLedgerRow],
    draft: ReportDraft,
    request: RunRequest,
    evidence: CollectedEvidence | None = None,
) -> tuple[list[ClaimLedgerRow], ReportDraft, list[ContradictionEntry], list[EvidenceGapEntry]]:
    claim_by_unit_id = {claim.unit_id: claim for claim in claims}
    source_lookup = {source.source_id: source for source in (evidence.sources if evidence is not None else [])}
    finding_lookup = {finding.finding_id: finding for finding in (evidence.findings if evidence is not None else [])}
    subject_conflicts = _subject_conflict_map(claims, finding_lookup, source_lookup)
    freshness_gaps = _freshness_tension_map(claims, finding_lookup, source_lookup)
    currentness_gaps = _historical_currentness_map(claims, source_lookup)

    contradictions: list[ContradictionEntry] = []
    gaps: list[EvidenceGapEntry] = []
    updated_claims: list[ClaimLedgerRow] = []
    updated_units: list[ReportUnit] = []

    for unit in draft.units:
        claim = claim_by_unit_id.get(unit.unit_id)
        if claim is None:
            updated_units.append(unit)
            continue

        support_status = claim.support_status
        include_in_report = claim.included_in_report
        caveat_required = claim.caveat_required
        required_fix = claim.required_fix or unit.required_fix
        rendered_text = unit.text
        blocking_reasons = list(claim.blocking_reasons)
        exclusion_reasons = list(claim.exclusion_reasons)
        contradiction_note = claim.contradiction_note or unit.contradiction_note

        if contradiction_note:
            entry = ContradictionEntry(
                issue_id=f"contradiction-{len(contradictions) + 1:03d}",
                claim_id=claim.claim_id,
                detail=contradiction_note,
                severity="critical" if claim.risk_level == "high" else "moderate",
                source_ids=list(claim.source_ids),
                action="resolve_or_exclude",
                contradiction_class="claim_level_note",
                subject_relation="unknown",
                severity_score=90 if claim.risk_level == "high" else 55,
            )
            contradictions.append(entry)
            support_status = "contradicted" if claim.risk_level == "high" else "weak"
            caveat_required = True
            blocking_reasons.append(f"{claim.claim_id} has contradictory evidence: {contradiction_note}")
            required_fix = required_fix or "Resolve the contradiction or remove the claim."

        for entry in subject_conflicts.get(claim.claim_id, []):
            renumbered = _renumber_contradiction(entry, len(contradictions) + 1)
            contradictions.append(renumbered)
            contradiction_class = renumbered.contradiction_class
            if contradiction_class == "same_subject_authoritative_conflict":
                support_status = "contradicted"
                include_in_report = False
                caveat_required = True
                blocking_reasons.append(renumbered.detail)
                required_fix = required_fix or "Resolve the same-subject authoritative contradiction before release."
            elif contradiction_class == "fresh_authoritative_override":
                caveat_required = True
                blocking_reasons.append(renumbered.detail)
                required_fix = required_fix or "Prefer the fresher authoritative source and keep the stale conflicting source in audit."
                if _claim_has_stale_authoritative_source(claim, source_lookup):
                    support_status = "weak"
                    include_in_report = False
                    exclusion_reasons.append(
                        "Stale conflicting support was removed from the reader-facing report after fresher authoritative evidence overrode it."
                    )
            elif contradiction_class == "stale_authoritative_vs_fresh_lower_role_tension":
                caveat_required = True
                blocking_reasons.append(renumbered.detail)
                required_fix = required_fix or "Keep the older authoritative statement caveated until a current authoritative source resolves the tension."
                if not _claim_has_authoritative_source(claim, source_lookup):
                    support_status = "weak"

        if claim.claim_kind == "absence":
            support_status, required_fix, force_exclude, rendered_text = _apply_absence_guard(
                claim=claim,
                unit=unit,
                request=request,
                source_lookup=source_lookup,
                current_support_status=support_status,
                current_required_fix=required_fix,
                current_include_in_report=include_in_report,
                current_text=rendered_text,
                blocking_reasons=blocking_reasons,
                exclusion_reasons=exclusion_reasons,
                gaps=gaps,
            )
            include_in_report = include_in_report and not force_exclude

        excerpt_gap = _user_excerpt_extrapolation_gap(claim, source_lookup)
        if excerpt_gap is not None:
            gaps.append(_renumber_gap(excerpt_gap, len(gaps) + 1))
            support_status = "missing" if claim.risk_level == "high" else "weak"
            caveat_required = True
            if claim.risk_level == "high":
                include_in_report = False
            blocking_reasons.append(excerpt_gap.detail)
            required_fix = required_fix or excerpt_gap.required_fix

        for gap in [*freshness_gaps.get(claim.claim_id, []), *currentness_gaps.get(claim.claim_id, [])]:
            gaps.append(_renumber_gap(gap, len(gaps) + 1))
            blocking_reasons.append(gap.detail)
            required_fix = required_fix or gap.required_fix
            caveat_required = True

        claim_jurisdictions = _claim_jurisdiction_tokens(claim, unit, source_lookup)
        if (
            request.jurisdiction
            and claim_jurisdictions
            and request.jurisdiction.casefold() not in claim_jurisdictions
            and claim.claim_kind in CRITICAL_HIGH_RISK_CLAIM_KINDS
        ):
            support_status = "out_of_scope"
            include_in_report = False
            detail = (
                f"{claim.claim_id} evidence is tied to {', '.join(sorted(claim_jurisdictions))}, "
                f"not {request.jurisdiction}."
            )
            blocking_reasons.append(detail)
            gaps.append(
                EvidenceGapEntry(
                    issue_id=f"gap-{len(gaps) + 1:03d}",
                    claim_id=claim.claim_id,
                    gap_type="scope_mismatch",
                    detail=detail,
                    required_fix="Use jurisdiction-matched evidence or remove the claim.",
                    severity="high",
                    blocking=True,
                    release_impact="blocked",
                )
            )
            required_fix = "Use jurisdiction-matched evidence or remove the claim."
        elif len(claim_jurisdictions) > 1 and claim.claim_kind in CRITICAL_HIGH_RISK_CLAIM_KINDS:
            support_status = "out_of_scope"
            include_in_report = False
            detail = (
                f"{claim.claim_id} collapses mixed-jurisdiction evidence ({', '.join(sorted(claim_jurisdictions))}) into one rule."
            )
            blocking_reasons.append(detail)
            exclusion_reasons.append("Mixed-jurisdiction evidence cannot be collapsed into one reader-facing rule.")
            gaps.append(
                EvidenceGapEntry(
                    issue_id=f"gap-{len(gaps) + 1:03d}",
                    claim_id=claim.claim_id,
                    gap_type="mixed_jurisdiction_scope_collapse",
                    detail=detail,
                    required_fix="Split the claim by jurisdiction or remove the mixed-jurisdiction synthesis.",
                    severity="high",
                    blocking=True,
                    release_impact="blocked",
                )
            )
            required_fix = "Split the claim by jurisdiction or remove the mixed-jurisdiction synthesis."

        if claim.risk_level == "high" and support_status in UNSUPPORTED_SUPPORT_STATUSES:
            include_in_report = False
            caveat_required = True
            exclusion_reasons.append(
                "Unsupported high-risk claim moved to audit-only until the blocking issue is resolved."
            )

        absence_scope = claim.absence_scope or unit.absence_scope
        claim_subject_key = claim.subject_key or unit.subject_key or _claim_group_key(claim, finding_lookup)
        claim_freshness_tag = claim.freshness_tag or unit.freshness_tag or _derived_freshness_tag(claim, source_lookup)

        updated_claims.append(
            ClaimLedgerRow(
                claim_id=claim.claim_id,
                unit_id=claim.unit_id,
                report_section=claim.report_section,
                exact_text_span=claim.exact_text_span,
                normalized_claim=claim.normalized_claim,
                claim_kind=claim.claim_kind,
                risk_level=claim.risk_level,
                source_ids=list(claim.source_ids),
                source_roles=list(claim.source_roles),
                evidence_count=claim.evidence_count,
                required_source_roles=list(claim.required_source_roles),
                matched_source_roles=list(claim.matched_source_roles),
                support_status=support_status,
                confidence=claim.confidence,
                caveat_required=caveat_required or support_status not in {"supported", "scoped_absence"},
                suggested_tone=claim.suggested_tone,
                required_fix=required_fix,
                origin_finding_ids=list(claim.origin_finding_ids),
                report_span_id=claim.report_span_id,
                report_line_start=claim.report_line_start,
                report_line_end=claim.report_line_end,
                claim_span_start=claim.claim_span_start,
                claim_span_end=claim.claim_span_end,
                finding_span_labels=list(claim.finding_span_labels),
                finding_span_starts=list(claim.finding_span_starts),
                finding_span_ends=list(claim.finding_span_ends),
                grounding_marker=claim.grounding_marker,
                grounding_scope_note=claim.grounding_scope_note,
                trace_status=claim.trace_status,
                included_in_report=include_in_report,
                absence_type=claim.absence_type or getattr(absence_scope, "basis", ""),
                absence_scope=absence_scope,
                subject_key=claim_subject_key,
                freshness_tag=claim_freshness_tag,
                contradiction_note=contradiction_note,
                jurisdiction=claim.jurisdiction or unit.jurisdiction,
                blocking_reasons=_dedupe(blocking_reasons),
                exclusion_reasons=_dedupe(exclusion_reasons),
                report_section_key=claim.report_section_key or unit.section_key,
            )
        )
        updated_units.append(
            ReportUnit(
                unit_id=unit.unit_id,
                section_key=unit.section_key,
                section_title=unit.section_title,
                text=rendered_text,
                claim_kind=unit.claim_kind,
                risk_level=unit.risk_level,
                source_ids=list(unit.source_ids),
                source_roles=list(unit.source_roles),
                confidence=unit.confidence,
                finding_id=unit.finding_id,
                support_status_hint=support_status,
                caveat=unit.caveat,
                required_fix=required_fix,
                contradiction_note=contradiction_note,
                jurisdiction=unit.jurisdiction,
                absence_type=unit.absence_type,
                absence_scope=absence_scope,
                subject_key=claim_subject_key,
                freshness_tag=claim_freshness_tag,
                is_claim=unit.is_claim,
                include_in_report=include_in_report,
            )
        )

    return updated_claims, ReportDraft(title=draft.title, sections=draft.sections, units=updated_units), contradictions, gaps


def _apply_absence_guard(
    *,
    claim: ClaimLedgerRow,
    unit: ReportUnit,
    request: RunRequest,
    source_lookup: dict[str, object],
    current_support_status: str,
    current_required_fix: str,
    current_include_in_report: bool,
    current_text: str,
    blocking_reasons: list[str],
    exclusion_reasons: list[str],
    gaps: list[EvidenceGapEntry],
) -> tuple[str, str, bool, str]:
    absence_scope = claim.absence_scope or unit.absence_scope
    basis = getattr(absence_scope, "basis", "") if absence_scope is not None else ""
    support_status = current_support_status
    required_fix = current_required_fix or "Keep the absence scoped and explicitly limited."
    include_in_report = current_include_in_report
    rendered_text = current_text
    authoritative_checked = _absence_has_authoritative_checked_scope(claim, absence_scope, source_lookup)
    can_state_scope = _can_state_absence_scope(absence_scope)
    explicit_scope_in_text = _absence_scope_statement_is_explicit(rendered_text, absence_scope)
    generated_scope_text = _absence_scope_statement(claim, absence_scope, authoritative_checked)
    if generated_scope_text and not explicit_scope_in_text:
        rendered_text = generated_scope_text
        explicit_scope_in_text = True

    def append_gap(gap_type: str, detail: str, *, blocking: bool, release_impact: str) -> None:
        if any(existing.claim_id == claim.claim_id and existing.gap_type == gap_type for existing in gaps):
            return
        gaps.append(
            EvidenceGapEntry(
                issue_id=f"gap-{len(gaps) + 1:03d}",
                claim_id=claim.claim_id,
                gap_type=gap_type,
                detail=detail,
                required_fix="Keep absence claims typed, scoped, and explicitly limited.",
                severity="high" if claim.risk_level == "high" else "medium",
                blocking=blocking,
                release_impact=release_impact,
            )
        )

    if not _has_absence_scope(absence_scope):
        support_status = "missing"
        blocking_reasons.append(
            f"{claim.claim_id} is an absence claim without a typed scope statement and could hide a false negative."
        )
        for gap_type_name in ("unscoped_absence", "absence_false_negative_risk"):
            gaps.append(
                EvidenceGapEntry(
                    issue_id=f"gap-{len(gaps) + 1:03d}",
                    claim_id=claim.claim_id,
                    gap_type=gap_type_name,
                    detail=f"{claim.claim_id} is missing a search scope, so the absence could be a false negative.",
                    required_fix="State the searched corpus, timeframe, and limitation explicitly.",
                    severity="high" if claim.risk_level == "high" else "medium",
                    blocking=claim.risk_level == "high",
                    release_impact="blocked" if claim.risk_level == "high" else "needs_revision",
                )
            )
        required_fix = "State the checked corpus, timeframe, and limitation explicitly."
        if claim.risk_level == "high":
            include_in_report = False
            exclusion_reasons.append("The absence claim stayed audit-only because its scope could not be stated safely.")
        return support_status, required_fix, not include_in_report, rendered_text

    if basis == "not_found_in_scoped_search":
        support_status = "missing" if claim.risk_level == "high" else "weak"
        blocking_reasons.append(
            f"{claim.claim_id} is based only on a scoped search result and cannot be promoted to a settled absence claim."
        )
        required_fix = "Keep the claim in uncertainty and do not present it as a fact."
        append_gap(
            "scoped_search_absence",
            _absence_gap_detail(claim.claim_id, "scoped_search_absence", authoritative_checked=authoritative_checked),
            blocking=claim.risk_level == "high",
            release_impact="blocked" if claim.risk_level == "high" else "needs_revision",
        )
        if claim.risk_level == "high":
            include_in_report = False
    elif basis == "not_found_in_checked_scope":
        gap_type = "authoritative_checked_absence" if authoritative_checked else "checked_scope_absence"
        if can_state_scope and explicit_scope_in_text:
            support_status = "scoped_absence"
            caveat_message = f"{claim.claim_id} remains a scoped absence claim and must not be read as a global fact."
            if caveat_message not in blocking_reasons:
                blocking_reasons.append(caveat_message)
            required_fix = ""
        else:
            support_status = "missing" if claim.risk_level == "high" else "weak"
            include_in_report = False
            blocking_reasons.append(
                f"{claim.claim_id} uses checked-scope absence evidence but the checked subject and scope are not explicit enough for reader-facing prose."
            )
            exclusion_reasons.append("The absence claim stayed audit-only because the checked scope could not be stated safely.")
            append_gap(
                gap_type,
                f"{claim.claim_id} uses checked-scope absence evidence without a safe explicit scope statement.",
                blocking=False,
                release_impact="needs_revision",
            )
            required_fix = "State the checked subject and scope explicitly or keep the claim audit-only."
    elif basis == "not_found_in_official_source_checked":
        if authoritative_checked and can_state_scope and explicit_scope_in_text:
            support_status = "scoped_absence"
            caveat_message = f"{claim.claim_id} remains a scoped absence claim tied to checked authoritative sources."
            if caveat_message not in blocking_reasons:
                blocking_reasons.append(caveat_message)
            required_fix = ""
        else:
            support_status = "missing" if claim.risk_level == "high" else "weak"
            include_in_report = False
            blocking_reasons.append(
                f"{claim.claim_id} uses checked authoritative-source absence evidence without a safe explicit scope statement."
            )
            exclusion_reasons.append("The authoritative absence claim stayed audit-only because the checked scope was not explicit enough.")
            append_gap(
                "authoritative_absence_missing_scope_statement",
                f"{claim.claim_id} is based on checked authoritative-source absence evidence and could not be rewritten with an explicit scope statement.",
                blocking=True,
                release_impact="blocked",
            )
            required_fix = "State the checked authoritative scope explicitly or keep the claim audit-only."
    elif basis in EXPLICIT_ABSENCE_TYPES and authoritative_checked and current_support_status == "supported":
        support_status = "supported"
        required_fix = "Keep the explicit absence tied to the cited authoritative source."

    if request.jurisdiction and not unit.jurisdiction and claim.risk_level == "high":
        blocking_reasons.append(
            f"{claim.claim_id} is high-risk and lacks a jurisdiction marker for its absence handling."
        )

    return support_status, required_fix, not include_in_report, rendered_text


def _subject_conflict_map(
    claims: list[ClaimLedgerRow],
    finding_lookup: dict[str, SourceFinding],
    source_lookup: dict[str, object],
) -> dict[str, list[ContradictionEntry]]:
    groups: dict[str, list[ClaimLedgerRow]] = defaultdict(list)
    for claim in claims:
        groups[_claim_group_key(claim, finding_lookup)].append(claim)

    conflicts: dict[str, list[ContradictionEntry]] = defaultdict(list)
    for group_key, grouped_claims in groups.items():
        if not group_key or len(grouped_claims) < 2:
            continue
        if _group_has_mixed_subject_boundaries(grouped_claims, finding_lookup):
            continue
        if _group_has_mixed_jurisdictions(grouped_claims, source_lookup):
            continue
        same_subject_conflict = _group_has_mixed_polarity(grouped_claims) or any(
            claim.contradiction_note for claim in grouped_claims
        )
        if not same_subject_conflict:
            continue
        severity, severity_score, contradiction_class, action = _contradiction_profile(grouped_claims, source_lookup)
        detail = _same_subject_detail(grouped_claims, contradiction_class)
        source_ids = list(dict.fromkeys(source_id for claim in grouped_claims for source_id in claim.source_ids))
        for claim in grouped_claims:
            conflicts[claim.claim_id].append(
                ContradictionEntry(
                    claim_id=claim.claim_id,
                    detail=detail,
                    severity=severity,
                    source_ids=source_ids,
                    action=action,
                    contradiction_class=contradiction_class,
                    subject_relation="same_subject",
                    severity_score=severity_score,
                )
            )
    return conflicts


def _freshness_tension_map(
    claims: list[ClaimLedgerRow],
    finding_lookup: dict[str, SourceFinding],
    source_lookup: dict[str, object],
) -> dict[str, list[EvidenceGapEntry]]:
    gaps: dict[str, list[EvidenceGapEntry]] = defaultdict(list)
    groups: dict[str, list[ClaimLedgerRow]] = defaultdict(list)
    for claim in claims:
        groups[_claim_group_key(claim, finding_lookup)].append(claim)

    for grouped_claims in groups.values():
        if len(grouped_claims) < 2:
            continue
        if _group_has_mixed_subject_boundaries(grouped_claims, finding_lookup):
            continue
        if _group_has_mixed_jurisdictions(grouped_claims, source_lookup):
            continue
        if len({_claim_polarity(claim) for claim in grouped_claims}) < 2:
            continue

        stale_authoritative_claims = [
            claim for claim in grouped_claims if _claim_has_stale_authoritative_source(claim, source_lookup)
        ]
        fresh_authoritative_claims = [
            claim for claim in grouped_claims if _claim_has_fresh_authoritative_source(claim, source_lookup)
        ]
        fresh_lower_claims = [
            claim
            for claim in grouped_claims
            if not _claim_has_authoritative_source(claim, source_lookup) and _claim_is_fresh(claim, source_lookup)
        ]
        if not stale_authoritative_claims:
            continue
        if fresh_authoritative_claims or fresh_lower_claims:
            detail = (
                "The checked subject mixes stale authoritative support with fresher conflicting support and requires an explicit freshness caveat."
            )
            for claim in grouped_claims:
                gaps[claim.claim_id].append(
                    EvidenceGapEntry(
                        claim_id=claim.claim_id,
                        gap_type="stale_current_tension",
                        detail=detail,
                        required_fix="Add a freshness caveat and prefer a current authoritative source before release.",
                        severity="high" if claim.risk_level == "high" else "medium",
                        blocking=False,
                        release_impact="needs_revision",
                    )
                )
    return gaps


def _historical_currentness_map(
    claims: list[ClaimLedgerRow],
    source_lookup: dict[str, object],
) -> dict[str, list[EvidenceGapEntry]]:
    gaps: dict[str, list[EvidenceGapEntry]] = defaultdict(list)
    for claim in claims:
        if claim.claim_kind in {"absence", "scope_boundary"}:
            continue
        if claim.caveat_required:
            continue
        if not _claim_uses_currentness_language(claim):
            continue
        if _claim_is_fresh(claim, source_lookup):
            continue
        if not any(_source_is_stale(source_lookup.get(source_id)) for source_id in claim.source_ids):
            continue
        gaps[claim.claim_id].append(
            EvidenceGapEntry(
                claim_id=claim.claim_id,
                gap_type="historical_source_used_as_current",
                detail=f"{claim.claim_id} uses stale source material as if it settled the current state without a freshness caveat.",
                required_fix="Add a freshness caveat or replace the claim with current source support.",
                severity="high" if claim.risk_level == "high" else "medium",
                blocking=False,
                release_impact="needs_revision",
            )
        )
    return gaps


def _user_excerpt_extrapolation_gap(
    claim: ClaimLedgerRow,
    source_lookup: dict[str, object],
) -> EvidenceGapEntry | None:
    if not claim.source_ids:
        return None
    roles = {getattr(source_lookup.get(source_id), "source_role", "unknown") for source_id in claim.source_ids}
    if roles != {"user_provided_source"}:
        return None
    if claim.claim_kind in {"scope_boundary", "fact"} and claim.risk_level != "high":
        return None
    return EvidenceGapEntry(
        claim_id=claim.claim_id,
        gap_type="user_excerpt_extrapolation",
        detail=f"{claim.claim_id} extrapolates beyond the checked user excerpt without external grounding.",
        required_fix="Keep the statement tied to the checked excerpt text or add external role-matched support.",
        severity="high" if claim.risk_level == "high" else "medium",
        blocking=claim.risk_level == "high",
        release_impact="blocked" if claim.risk_level == "high" else "needs_revision",
    )


def _claim_group_key(claim: ClaimLedgerRow, finding_lookup: dict[str, SourceFinding]) -> str:
    if claim.subject_key:
        return normalize_text("|".join(filter(None, [claim.subject_key, claim.jurisdiction])))
    for finding_id in claim.origin_finding_ids:
        finding = finding_lookup.get(finding_id)
        if finding is None:
            continue
        if finding.subject_scope_key:
            return finding.subject_scope_key
        if finding.subject_key:
            return normalize_text("|".join(filter(None, [finding.subject_key, finding.jurisdiction or claim.jurisdiction])))
    if claim.absence_scope is not None:
        return normalize_text(
            "|".join(
                filter(
                    None,
                    [
                        getattr(claim.absence_scope, "subject", ""),
                        getattr(claim.absence_scope, "scope_label", ""),
                        claim.jurisdiction,
                    ],
                )
            )
        )
    return normalize_text("|".join(filter(None, [claim.normalized_claim, claim.jurisdiction])))


def _claim_boundary_tokens(claim: ClaimLedgerRow, finding_lookup: dict[str, SourceFinding]) -> set[str]:
    tokens: set[str] = set()
    if claim.subject_key:
        tokens.add(normalize_text(claim.subject_key))
    for finding_id in claim.origin_finding_ids:
        finding = finding_lookup.get(finding_id)
        if finding is None:
            continue
        if finding.subject_scope_key:
            tokens.add(normalize_text(finding.subject_scope_key))
        elif finding.subject_key:
            tokens.add(normalize_text(finding.subject_key))
    if claim.absence_scope is not None:
        subject = getattr(claim.absence_scope, "subject", "")
        scope_label = getattr(claim.absence_scope, "scope_label", "")
        if subject or scope_label:
            tokens.add(normalize_text("|".join(filter(None, [subject, scope_label]))))
    return {token for token in tokens if token}


def _group_has_mixed_subject_boundaries(
    grouped_claims: list[ClaimLedgerRow],
    finding_lookup: dict[str, SourceFinding],
) -> bool:
    boundary_sets = [
        _claim_boundary_tokens(claim, finding_lookup)
        for claim in grouped_claims
        if _claim_boundary_tokens(claim, finding_lookup)
    ]
    if len(boundary_sets) < 2:
        return False
    shared = set.intersection(*(set(tokens) for tokens in boundary_sets))
    if shared:
        return False
    return len({tuple(sorted(tokens)) for tokens in boundary_sets}) > 1


def _group_has_mixed_jurisdictions(
    grouped_claims: list[ClaimLedgerRow],
    source_lookup: dict[str, object],
) -> bool:
    jurisdiction_sets = {
        tuple(sorted(tokens))
        for claim in grouped_claims
        for tokens in [_claim_jurisdiction_tokens(claim, None, source_lookup)]
        if tokens
    }
    return len(jurisdiction_sets) > 1


def _claim_state(claim: ClaimLedgerRow) -> str:
    return "absence" if claim.claim_kind == "absence" else "presence"


def _claim_polarity(claim: ClaimLedgerRow) -> str:
    if claim.claim_kind == "absence":
        return "negative"
    text = normalize_text(claim.normalized_claim or claim.exact_text_span)
    padded = f" {text} "
    negative_markers = (
        " does not ",
        " do not ",
        " did not ",
        " not ",
        " no ",
        " without ",
        " cannot ",
        " can not ",
        " repealed ",
        " outside ",
        " absent ",
        " missing ",
    )
    if any(marker in padded for marker in negative_markers):
        return "negative"
    return "positive"


def _group_has_mixed_polarity(grouped_claims: list[ClaimLedgerRow]) -> bool:
    return len({_claim_polarity(claim) for claim in grouped_claims}) > 1


def _contradiction_profile(
    grouped_claims: list[ClaimLedgerRow],
    source_lookup: dict[str, object],
) -> tuple[str, int, str, str]:
    authoritative_claims = [claim for claim in grouped_claims if _claim_has_authoritative_source(claim, source_lookup)]
    fresh_authoritative_claims = [claim for claim in authoritative_claims if _claim_has_fresh_authoritative_source(claim, source_lookup)]
    stale_authoritative_claims = [claim for claim in authoritative_claims if _claim_has_stale_authoritative_source(claim, source_lookup)]
    fresh_lower_claims = [
        claim
        for claim in grouped_claims
        if not _claim_has_authoritative_source(claim, source_lookup) and _claim_is_fresh(claim, source_lookup)
    ]
    any_high_risk = any(claim.risk_level == "high" for claim in grouped_claims)

    if len(fresh_authoritative_claims) >= 2:
        return "critical", 95 if any_high_risk else 85, "same_subject_authoritative_conflict", "blocked"
    if fresh_authoritative_claims and stale_authoritative_claims:
        return "moderate", 60 if any_high_risk else 50, "fresh_authoritative_override", "needs_revision"
    if stale_authoritative_claims and fresh_lower_claims and not fresh_authoritative_claims:
        return (
            "high" if any_high_risk else "moderate",
            82 if any_high_risk else 62,
            "stale_authoritative_vs_fresh_lower_role_tension",
            "needs_revision",
        )
    if len(authoritative_claims) >= 2:
        return "critical", 90 if any_high_risk else 80, "same_subject_authoritative_conflict", "blocked"
    if authoritative_claims:
        return "high" if any_high_risk else "moderate", 75 if any_high_risk else 55, "same_subject_conflict", "needs_revision"
    return "moderate", 45, "same_subject_conflict", "needs_revision"


def _same_subject_detail(grouped_claims: list[ClaimLedgerRow], contradiction_class: str) -> str:
    claim_ids = ", ".join(claim.claim_id for claim in grouped_claims)
    if contradiction_class == "fresh_authoritative_override":
        return f"Claims {claim_ids} point at the same checked subject, but a fresher authoritative source overrides stale conflicting support."
    if contradiction_class == "stale_authoritative_vs_fresh_lower_role_tension":
        return (
            f"Claims {claim_ids} point at the same checked subject, but only fresher lower-role support conflicts with stale authoritative support."
        )
    if contradiction_class == "same_subject_authoritative_conflict":
        return f"Claims {claim_ids} contain an unresolved same-subject authoritative contradiction."
    return f"Claims {claim_ids} point at the same checked subject but support incompatible conclusions."


def _absence_has_authoritative_checked_scope(claim: ClaimLedgerRow, absence_scope, source_lookup: dict[str, object]) -> bool:
    checked_source_ids = set(getattr(absence_scope, "checked_source_ids", []) or [])
    checked_roles = set(getattr(absence_scope, "checked_roles", []) or [])
    for source_id in set(claim.source_ids) | checked_source_ids:
        source = source_lookup.get(source_id)
        role = getattr(source, "source_role", "")
        if role in AUTHORITATIVE_SOURCE_ROLES:
            return True
    return bool(checked_roles & AUTHORITATIVE_SOURCE_ROLES)


def _absence_gap_type(basis: str, authoritative_checked: bool) -> str:
    if basis == "not_found_in_scoped_search":
        return "scoped_search_absence"
    if basis == "not_found_in_official_source_checked":
        return "authoritative_checked_absence"
    if basis == "not_found_in_checked_scope":
        return "authoritative_checked_absence" if authoritative_checked else "checked_scope_absence"
    return basis or "absence"


def _absence_gap_detail(claim_id: str, gap_type: str, *, authoritative_checked: bool) -> str:
    if gap_type == "checked_scope_absence":
        if authoritative_checked:
            return f"{claim_id} reflects a checked authoritative absence and must remain explicitly scoped."
        return f"{claim_id} reflects a checked-scope absence and must remain explicitly scoped."
    if gap_type == "scoped_search_absence":
        return f"{claim_id} is only a scoped-search absence and must not be rewritten as a settled fact."
    if gap_type == "authoritative_checked_absence":
        return f"{claim_id} is based on checked authoritative-source absence evidence and still needs an explicit scope statement."
    return f"{claim_id} is an absence claim of type `{gap_type}` and must stay typed and scoped."


def _has_absence_scope(absence_scope) -> bool:
    if absence_scope is None:
        return False
    if isinstance(absence_scope, str):
        return bool(absence_scope.strip())
    return bool(
        getattr(absence_scope, "scope_label", "")
        or getattr(absence_scope, "subject", "")
        or getattr(absence_scope, "checked_source_ids", [])
    )


def _can_state_absence_scope(absence_scope) -> bool:
    if absence_scope is None:
        return False
    if isinstance(absence_scope, str):
        return bool(absence_scope.strip())
    return bool(getattr(absence_scope, "scope_label", "").strip() and getattr(absence_scope, "subject", "").strip())


def _absence_scope_statement_is_explicit(text: str, absence_scope) -> bool:
    if not text or absence_scope is None:
        return False
    if isinstance(absence_scope, str):
        return absence_scope.strip().casefold() in normalize_text(text)
    scope_label = normalize_text(getattr(absence_scope, "scope_label", ""))
    subject = normalize_text(getattr(absence_scope, "subject", ""))
    lowered = normalize_text(text)
    if not scope_label or not subject:
        return False
    return (
        scope_label in lowered
        and subject in lowered
        and ("within the checked scope" in lowered or "checked authoritative" in lowered or "scoped absence" in lowered)
    )


def _absence_scope_statement(
    claim: ClaimLedgerRow,
    absence_scope,
    authoritative_checked: bool,
) -> str:
    if not _can_state_absence_scope(absence_scope):
        return ""
    scope_label = getattr(absence_scope, "scope_label", "").strip()
    subject = getattr(absence_scope, "subject", "").strip()
    if not scope_label or not subject:
        return ""
    source_frame = "checked authoritative sources" if authoritative_checked else "checked sources"
    if claim.risk_level == "high":
        return (
            f"Within the checked scope ({scope_label}), the {source_frame} do not show {subject}. "
            f"This is a scoped absence for the checked materials only, not a global finding."
        )
    return (
        f"Within the checked scope ({scope_label}), the checked materials do not show {subject}. "
        f"This remains a scoped absence, not a global finding."
    )


def _claim_has_authoritative_source(claim: ClaimLedgerRow, source_lookup: dict[str, object]) -> bool:
    if any(role in AUTHORITATIVE_SOURCE_ROLES for role in claim.source_roles):
        return True
    return any(
        getattr(source_lookup.get(source_id), "source_role", "") in AUTHORITATIVE_SOURCE_ROLES
        for source_id in claim.source_ids
    )


def _claim_has_fresh_authoritative_source(claim: ClaimLedgerRow, source_lookup: dict[str, object]) -> bool:
    if claim.freshness_tag == "fresh" and _claim_has_authoritative_source(claim, source_lookup):
        return True
    return any(
        getattr(source_lookup.get(source_id), "source_role", "") in AUTHORITATIVE_SOURCE_ROLES
        and not _source_is_stale(source_lookup.get(source_id))
        for source_id in claim.source_ids
    )


def _claim_has_stale_authoritative_source(claim: ClaimLedgerRow, source_lookup: dict[str, object]) -> bool:
    if claim.freshness_tag == "stale" and _claim_has_authoritative_source(claim, source_lookup):
        return True
    return any(
        getattr(source_lookup.get(source_id), "source_role", "") in AUTHORITATIVE_SOURCE_ROLES
        and _source_is_stale(source_lookup.get(source_id))
        for source_id in claim.source_ids
    )


def _claim_is_fresh(claim: ClaimLedgerRow, source_lookup: dict[str, object]) -> bool:
    if claim.freshness_tag == "fresh":
        return True
    if claim.freshness_tag == "stale":
        return False
    known_sources = [source_lookup.get(source_id) for source_id in claim.source_ids if source_lookup.get(source_id) is not None]
    return bool(known_sources) and any(not _source_is_stale(source) for source in known_sources)


def _derived_freshness_tag(claim: ClaimLedgerRow, source_lookup: dict[str, object]) -> str:
    if claim.freshness_tag:
        return claim.freshness_tag
    if claim.source_ids and all(_source_is_stale(source_lookup.get(source_id)) for source_id in claim.source_ids):
        return "stale"
    if any(not _source_is_stale(source_lookup.get(source_id)) for source_id in claim.source_ids):
        return "fresh"
    return ""


def _claim_uses_currentness_language(claim: ClaimLedgerRow) -> bool:
    text = normalize_text(claim.exact_text_span or claim.normalized_claim)
    padded = f" {text} "
    return any(marker in padded for marker in _CURRENTNESS_MARKERS)


def _claim_jurisdiction_tokens(
    claim: ClaimLedgerRow,
    unit: ReportUnit | None,
    source_lookup: dict[str, object],
) -> set[str]:
    tokens: set[str] = set()
    for value in (claim.jurisdiction, getattr(unit, "jurisdiction", "")):
        if value:
            tokens.add(value.casefold())
    for source_id in claim.source_ids:
        source = source_lookup.get(source_id)
        source_jurisdiction = getattr(source, "jurisdiction", "")
        if source_jurisdiction:
            tokens.add(source_jurisdiction.casefold())
    if claim.absence_scope is not None:
        for source_id in getattr(claim.absence_scope, "checked_source_ids", []) or []:
            source = source_lookup.get(source_id)
            source_jurisdiction = getattr(source, "jurisdiction", "")
            if source_jurisdiction:
                tokens.add(source_jurisdiction.casefold())
    return tokens


def _source_is_stale(source) -> bool:
    if source is None:
        return False
    provenance = getattr(source, "provenance", None)
    if getattr(provenance, "stale", False):
        return True
    published_on = getattr(source, "published_on", "")
    if not published_on:
        return False
    published_date = _parse_date(published_on)
    if published_date is None:
        return False
    return (date.today() - published_date).days > 365


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    for candidate in (value, value[:10]):
        try:
            return datetime.fromisoformat(candidate).date()
        except ValueError:
            continue
    return None


def _renumber_contradiction(entry: ContradictionEntry, index: int) -> ContradictionEntry:
    return ContradictionEntry(
        issue_id=f"contradiction-{index:03d}",
        claim_id=entry.claim_id,
        detail=entry.detail,
        severity=entry.severity,
        source_ids=list(entry.source_ids),
        action=entry.action,
        contradiction_class=entry.contradiction_class,
        subject_relation=entry.subject_relation,
        severity_score=entry.severity_score,
    )


def _renumber_gap(entry: EvidenceGapEntry, index: int) -> EvidenceGapEntry:
    return EvidenceGapEntry(
        issue_id=f"gap-{index:03d}",
        claim_id=entry.claim_id,
        gap_type=entry.gap_type,
        detail=entry.detail,
        required_fix=entry.required_fix,
        severity=entry.severity,
        blocking=entry.blocking,
        release_impact=entry.release_impact,
    )


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item and item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


__all__ = ["apply_contradiction_absence_guard"]
