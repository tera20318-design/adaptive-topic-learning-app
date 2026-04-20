from __future__ import annotations

from typing import Any

from cleanroom_runtime.core.gates import DecisionUsableResult, assess_decision_usable
from cleanroom_runtime.models import (
    BudgetPlan,
    ClaimLedgerRow,
    ContradictionEntry,
    DomainAdapter,
    EvidenceGapEntry,
    GateIssue,
    IntentResult,
    MetricsSnapshot,
    ReleaseGateDecision,
    ReportDraft,
    RiskTierResult,
    RunRequest,
)
from cleanroom_runtime.utils import normalize_text


def decide_release_gate(
    *,
    draft: ReportDraft,
    claims: list[ClaimLedgerRow],
    citations,
    contradictions: list[ContradictionEntry],
    gaps: list[EvidenceGapEntry],
    budget: BudgetPlan,
    adapter: DomainAdapter,
    metrics: MetricsSnapshot,
    validation_errors: list[str],
    request: RunRequest | None = None,
    intent: IntentResult | None = None,
    risk: RiskTierResult | None = None,
    decision_usable: DecisionUsableResult | None = None,
) -> ReleaseGateDecision:
    if decision_usable is None:
        decision_usable = assess_decision_usable(
            draft,
            claims,
            citations,
            adapter=adapter,
            budget=budget,
            metrics=metrics,
            request=request,
            intent=intent,
            risk=risk,
        )
    issues: list[GateIssue] = []
    reasons: list[str] = []
    blocking_reasons: list[str] = []
    revision_reasons: list[str] = []
    issue_index = 1

    if not claims:
        issues.append(_issue(issue_index, "", "release_gate", "high", "No claims were extracted for audit.", "Fix claim extraction before release.", True))
        issue_index += 1

    for error in validation_errors:
        stage = "cleanroom_integrity" if _is_semantic_leakage_error(error) else "validator"
        required_fix = (
            "Remove fixture-specific leakage from core artifacts and keep topic adaptation in per-run data only."
            if stage == "cleanroom_integrity"
            else "Fix the contract violation."
        )
        issues.append(_issue(issue_index, "", stage, "high", error, required_fix, True))
        issue_index += 1

    if not metrics.audit_complete:
        issues.append(_issue(issue_index, "", "audit", "high", "Audit coverage is incomplete.", "Every claim-bearing unit must appear in the claim ledger.", True))
        issue_index += 1
    if not metrics.citation_trace_complete:
        issues.append(_issue(issue_index, "", "audit", "high", "Citation traceability is incomplete.", "Ensure cited sources exist in the evidence inventory.", True))
        issue_index += 1
    if not metrics.traceability_complete or metrics.trace_mismatch_count > 0:
        issues.append(
            _issue(
                issue_index,
                "",
                "audit",
                "high",
                "Traceability is incomplete between reader-facing prose, claim rows, and citations.",
                "Repair report span links, claim lineage, and citation/source finding links before release.",
                True,
            )
        )
        issue_index += 1
    if metrics.high_risk_traceability_mismatch_count > 0:
        issues.append(
            _issue(
                issue_index,
                "",
                "audit",
                "high",
                "One or more high-risk mainline claims do not keep complete prose-to-claim-to-citation traceability.",
                "Repair report spans, finding lineage, and grounded citation excerpts for every high-risk mainline claim.",
                True,
            )
        )
        issue_index += 1
    if metrics.high_risk_missing_provenance_count > 0:
        issues.append(
            _issue(
                issue_index,
                "",
                "evidence_ingestion",
                "high",
                "One or more high-risk claims rely on sources with incomplete provenance or ambiguous role inference.",
                "Repair source provenance or remove the affected high-risk claim from release.",
                True,
            )
        )
        issue_index += 1
    if metrics.metadata_inconsistency_count > 0 and metrics.unresolved_high_risk_claim_count > 0:
        issues.append(
            _issue(
                issue_index,
                "",
                "audit",
                "high",
                "Metadata inconsistency coexists with unresolved high-risk claims.",
                "Repair metadata consistency before treating any remaining high-risk claim as releasable.",
                True,
            )
        )
        issue_index += 1

    for contradiction in contradictions:
        if contradiction.severity == "critical":
            issues.append(
                _issue(
                    issue_index,
                    contradiction.claim_id,
                    "contradiction_guard",
                    "high",
                    contradiction.detail,
                    "Resolve the contradiction or exclude the claim from the reader-facing report.",
                    True,
                )
            )
            issue_index += 1
        elif contradiction.contradiction_class == "stale_current_tension":
            revision_reasons.append(contradiction.detail)

    for claim in claims:
        adequate = claim.support_status in {"supported", "scoped_absence"}
        if claim.risk_level == "high" and claim.included_in_report and not adequate:
            issues.append(
                _issue(
                    issue_index,
                    claim.claim_id,
                    "evidence_mapper",
                    "high",
                    f"Included high-risk claim is not adequately supported (`{claim.support_status}`).",
                    claim.required_fix or "Remove the claim from reader-facing prose or add role-matched support.",
                    True,
                )
            )
            issue_index += 1
        elif claim.risk_level == "high" and not adequate:
            issues.append(
                _issue(
                    issue_index,
                    claim.claim_id,
                    "audit",
                    "high",
                    f"Audit-only but still blocks release: unresolved high-risk claim (`{claim.support_status}`).",
                    claim.required_fix or "Keep the claim visible in audit until resolved and do not release the bundle.",
                    True,
                )
            )
            issue_index += 1
        if claim.risk_level == "high" and claim.claim_kind != "scope_boundary" and not claim.matched_source_roles:
            issues.append(
                _issue(
                    issue_index,
                    claim.claim_id,
                    "source_strategy",
                    "high",
                    "Required source roles were not satisfied for a high-risk claim.",
                    claim.required_fix or "Add claim-kind-matched source roles.",
                    True,
                )
            )
            issue_index += 1
        if claim.claim_kind == "absence" and claim.absence_scope is None:
            issues.append(
                _issue(
                    issue_index,
                    claim.claim_id,
                    "absence_guard",
                    "high" if claim.risk_level == "high" else "medium",
                    "Absence claim is missing typed scope.",
                    claim.required_fix or "Add typed scope or keep the claim out of reader-facing prose.",
                    claim.included_in_report and claim.risk_level == "high",
                )
            )
            issue_index += 1
        if (
            claim.claim_kind == "absence"
            and claim.included_in_report
            and claim.support_status == "scoped_absence"
            and not _absence_scope_is_explicit(claim)
        ):
            issues.append(
                _issue(
                    issue_index,
                    claim.claim_id,
                    "absence_guard",
                    "medium",
                    "Checked authoritative-source absence is still missing an explicit scoped reader-facing statement.",
                    claim.required_fix or "Rewrite the absence claim so the checked subject and scope stay explicit.",
                    False,
                )
            )
            issue_index += 1
        if claim.risk_level == "high" and claim.included_in_report and not _claim_traceability_complete(claim, citations):
            issues.append(
                _issue(
                    issue_index,
                    claim.claim_id,
                    "audit",
                    "high",
                    "High-risk mainline claim is missing complete traceability to grounded source excerpts.",
                    claim.required_fix or "Keep the claim out of mainline prose until excerpt-level traceability is complete.",
                    True,
                )
            )
            issue_index += 1

    for gap in gaps:
        if gap.blocking:
            issues.append(
                _issue(
                    issue_index,
                    gap.claim_id,
                    "contradiction_guard" if "conflict" in gap.gap_type or "tension" in gap.gap_type else "absence_guard",
                    "high",
                    gap.detail,
                    gap.required_fix,
                    True,
                )
            )
            issue_index += 1
        elif gap.release_impact in {"needs_revision", "provisional"}:
            revision_reasons.append(gap.detail)

    for finding in decision_usable.findings:
        issues.append(
            _issue(
                issue_index,
                finding.claim_id,
                "decision_usable",
                finding.severity,
                finding.message,
                finding.required_fix,
                finding.blocks_release,
            )
        )
        issue_index += 1

    if any(finding.code == "missing_tradeoff_table" for finding in decision_usable.findings):
        revision_reasons.append("Comparison output must include a reader-facing tradeoff table before release.")
    if any(finding.code == "document_review_without_grounding" for finding in decision_usable.findings):
        revision_reasons.append("Document review output must stay directly grounded in the checked document text.")
    if metrics.duplicate_claim_count > 0:
        revision_reasons.append("The draft repeats claims that should remain distinct.")
    if metrics.partial_packet_count > 0 and not metrics.ingestion_audit_visible:
        revision_reasons.append("Packet salvage occurred without a visible ingestion audit summary.")
    if not metrics.uncertainty_section_present or not metrics.limitations_visible:
        revision_reasons.append("Limitations and uncertainty must remain visible in reader-facing sections.")
    if metrics.target_miss_without_waiver:
        misses = ", ".join(metrics.target_misses) or "unspecified target"
        revision_reasons.append(f"A declared target was missed without waiver: {misses}.")
    if metrics.included_unsupported_claim_count > 0 and not any(issue.blocks_release for issue in issues):
        revision_reasons.append("Some included claims remain below the support bar.")
    revision_reasons.extend(decision_usable.revision_reasons)

    blocking_reasons.extend(issue.message for issue in issues if issue.blocks_release)
    reasons.extend(blocking_reasons)
    reasons.extend(revision_reasons)
    reasons.extend(_gap_reasons(gaps))

    metadata_consistent = (
        metrics.audit_complete
        and metrics.citation_trace_complete
        and metrics.traceability_complete
        and metrics.metadata_inconsistency_count == 0
        and metrics.citation_trace_mismatch_count == 0
    )

    if blocking_reasons:
        return ReleaseGateDecision(
            status="blocked",
            reasons=_dedupe(reasons),
            blocking_reasons=blocking_reasons,
            unresolved_gaps=[gap.detail for gap in gaps],
            claim_issues=issues,
            contract_complete=False,
            research_completeness=budget.research_completeness_note,
            metadata_consistent=metadata_consistent,
            release_semantics="blocked",
        )

    if revision_reasons:
        return ReleaseGateDecision(
            status="needs_revision",
            reasons=_dedupe(reasons),
            blocking_reasons=[],
            unresolved_gaps=[gap.detail for gap in gaps],
            claim_issues=issues,
            contract_complete=True,
            research_completeness=budget.research_completeness_note,
            metadata_consistent=metadata_consistent,
            release_semantics="needs_revision",
        )

    if budget.evidence_mode == "synthetic":
        return ReleaseGateDecision(
            status="provisional",
            reasons=["Synthetic validation proves contracts, not live research completeness."],
            blocking_reasons=[],
            unresolved_gaps=[gap.detail for gap in gaps],
            claim_issues=issues,
            contract_complete=True,
            research_completeness=budget.research_completeness_note,
            metadata_consistent=metadata_consistent,
            release_semantics="synthetic_validation_only",
        )

    if not budget.full_dr_equivalent or metrics.unresolved_high_risk_claim_count > 0 or metrics.target_misses:
        return ReleaseGateDecision(
            status="provisional",
            reasons=["The run is usable within its declared scope but does not claim full research completeness."],
            blocking_reasons=[],
            unresolved_gaps=[gap.detail for gap in gaps],
            claim_issues=issues,
            contract_complete=True,
            research_completeness=budget.research_completeness_note,
            metadata_consistent=metadata_consistent,
            release_semantics="scoped_or_incomplete_live",
        )

    return ReleaseGateDecision(
        status="complete",
        reasons=["The run satisfies the current claim-level and audit contracts for a live full-equivalent run."],
        blocking_reasons=[],
        unresolved_gaps=[gap.detail for gap in gaps],
        claim_issues=issues,
        contract_complete=True,
        research_completeness=budget.research_completeness_note,
        metadata_consistent=metadata_consistent,
        release_semantics="live_full_candidate",
    )


def _issue(
    index: int,
    claim_id: str,
    stage: str,
    severity: str,
    message: str,
    required_fix: str,
    blocks_release: bool,
) -> GateIssue:
    return GateIssue(
        reason_id=f"gate-issue-{index:03d}",
        claim_id=claim_id,
        stage=stage,
        severity=severity,
        message=message,
        required_fix=required_fix,
        blocks_release=blocks_release,
    )


def _gap_reasons(gaps: list[EvidenceGapEntry]) -> list[str]:
    return [gap.detail for gap in gaps if gap.severity == "high"]
def _is_semantic_leakage_error(error: str) -> bool:
    normalized = error.casefold()
    return normalized.startswith("semantic_") or "semantic leakage" in normalized or "clean-room integrity" in normalized


def _dedupe(values: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def _absence_scope_is_explicit(claim: ClaimLedgerRow) -> bool:
    if claim.absence_scope is None:
        return False
    scope_label = normalize_text(getattr(claim.absence_scope, "scope_label", ""))
    subject = normalize_text(getattr(claim.absence_scope, "subject", ""))
    text = normalize_text(claim.exact_text_span)
    if not scope_label or not subject:
        return False
    return (
        scope_label in text
        and subject in text
        and ("within the checked scope" in text or "scoped absence" in text or "checked authoritative sources" in text)
    )


def _claim_traceability_complete(claim: ClaimLedgerRow, citations) -> bool:
    if (
        claim.trace_status != "linked"
        or not claim.report_span_id
        or claim.claim_span_start is None
        or claim.claim_span_end is None
        or not claim.origin_finding_ids
    ):
        return False
    related_citations = [citation for citation in citations if citation.claim_id == claim.claim_id and citation.included_in_report]
    if not related_citations:
        return False
    return any(_citation_trace_is_complete(citation) for citation in related_citations)


def _citation_trace_is_complete(citation) -> bool:
    if citation.trace_status != "linked" or not citation.provenance_complete or not citation.source_finding_ids:
        return False
    if citation.source_role == "user_provided_source" or citation.grounding_marker:
        return bool(
            citation.source_excerpt
            and (
                (citation.source_span_start is not None and citation.source_span_end is not None)
                or citation.source_span_starts
            )
        )
    return True
