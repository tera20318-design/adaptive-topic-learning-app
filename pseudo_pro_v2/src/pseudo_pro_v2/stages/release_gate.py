from __future__ import annotations

from pseudo_pro_v2.gates import evaluate_decision_usable
from pseudo_pro_v2.models import BudgetPlan, ClaimLedgerRow, CitationLedgerRow, ContradictionEntry, DomainAdapter, EvidenceGapEntry, ReleaseGateDecision, ReportDraft


def decide_release_gate(
    *,
    draft: ReportDraft,
    claims: list[ClaimLedgerRow],
    citations: list[CitationLedgerRow],
    contradictions: list[ContradictionEntry],
    gaps: list[EvidenceGapEntry],
    budget: BudgetPlan,
    adapter: DomainAdapter,
    metrics: dict,
    validation_errors: list[str],
) -> ReleaseGateDecision:
    blocking_reasons: list[str] = []
    revision_reasons: list[str] = []
    unresolved_gaps = [gap.detail for gap in gaps]
    included_claims = [claim for claim in claims if claim.included_in_report]
    high_risk_claims = [claim for claim in claims if claim.risk_level == "high"]
    rubric = evaluate_decision_usable(draft, claims, adapter)

    if not claims:
        blocking_reasons.append("claim-ledger is missing.")
    if not citations:
        blocking_reasons.append("citation-ledger is missing.")
    clean_room_errors = [item for item in validation_errors if item.startswith("clean-room integrity violation:")]
    other_validation_errors = [item for item in validation_errors if not item.startswith("clean-room integrity violation:")]
    if clean_room_errors:
        blocking_reasons.extend(clean_room_errors)
    if other_validation_errors:
        revision_reasons.extend(other_validation_errors)

    unsupported_high_risk = [claim for claim in high_risk_claims if claim.support_status != "supported"]
    if unsupported_high_risk:
        blocking_reasons.append("There are unsupported high-risk claims.")

    role_mismatch_high_risk = [
        claim
        for claim in high_risk_claims
        if claim.support_status == "supported" and not claim.required_role_matched
    ]
    if role_mismatch_high_risk:
        blocking_reasons.append("A supported high-risk claim lacks claim-kind-appropriate source-role support.")

    if metrics.get("unsupported_high_risk_absence_count", 0) > 0:
        blocking_reasons.append("A high-risk absence claim is unsupported.")

    if any(item.severity == "critical" for item in contradictions):
        blocking_reasons.append("There is an unresolved critical contradiction.")

    if not metrics.get("citation_trace_consistent", True) or not metrics.get("rendered_citation_trace_consistent", True):
        blocking_reasons.append("Citation trace mismatch remains unresolved.")

    if not metrics.get("metadata_consistent", False) and unsupported_high_risk:
        blocking_reasons.append("Unsupported high-risk claims exist alongside metadata inconsistency.")

    if not metrics.get("metadata_consistent", False):
        revision_reasons.append("Metadata is inconsistent.")
    if adapter.output_type == "user document review" and not metrics.get("document_grounding_present", False):
        revision_reasons.append("User document review is missing direct document grounding.")
    if not rubric.passed:
        revision_reasons.extend(rubric.failures)
    if metrics.get("target_miss_without_waiver", False):
        revision_reasons.append("A required target missed without waiver.")
    if not _required_tables_present(adapter, draft):
        revision_reasons.append("A required table or checklist is missing.")
    if metrics.get("source_finding_ledger_coverage_ratio", 1.0) < 1.0:
        revision_reasons.append("Not all source findings remain visible in the claim ledger.")
    if any(claim.risk_level == "medium" and claim.support_status in {"missing", "out_of_scope"} for claim in claims):
        revision_reasons.append("There are medium-risk claims with incomplete support.")

    if blocking_reasons:
        return ReleaseGateDecision(
            status="blocked",
            reasons=blocking_reasons + revision_reasons,
            blocking_reasons=blocking_reasons,
            unresolved_gaps=unresolved_gaps,
            metadata_consistent=metrics.get("metadata_consistent", False),
        )

    if revision_reasons:
        return ReleaseGateDecision(
            status="needs_revision",
            reasons=revision_reasons,
            blocking_reasons=[],
            unresolved_gaps=unresolved_gaps,
            metadata_consistent=metrics.get("metadata_consistent", False),
        )

    if metrics.get("synthetic_inputs", False) and not metrics.get("synthetic_complete_allowed", False):
        return ReleaseGateDecision(
            status="provisional",
            reasons=["Synthetic evidence cannot claim complete without explicit contract allowance."],
            blocking_reasons=[],
            unresolved_gaps=unresolved_gaps,
            metadata_consistent=metrics.get("metadata_consistent", False),
        )

    if any(claim.support_status == "weak" for claim in included_claims) or metrics.get("target_misses"):
        return ReleaseGateDecision(
            status="provisional",
            reasons=["Useful but limited within the declared scope."],
            blocking_reasons=[],
            unresolved_gaps=unresolved_gaps,
            metadata_consistent=metrics.get("metadata_consistent", False),
        )

    return ReleaseGateDecision(
        status="complete",
        reasons=["The run is decision-useful within its declared scope."],
        blocking_reasons=[],
        unresolved_gaps=unresolved_gaps,
        metadata_consistent=metrics.get("metadata_consistent", False),
    )


def _required_tables_present(adapter: DomainAdapter, draft: ReportDraft) -> bool:
    included_units = [unit for unit in draft.units if unit.include_in_report]
    checklist_units = [unit for unit in included_units if unit.section_key == "checklist"]
    finding_units = [unit for unit in included_units if unit.section_key == "findings" and unit.is_claim]
    option_units = [unit for unit in included_units if unit.section_key == "options" and unit.is_claim]
    comparison_units = [unit for unit in option_units if unit.claim_kind == "comparison"]

    checks = {
        "Checklist or decision table": bool(checklist_units),
        "Evidence-backed findings table": bool(finding_units),
        "Options or comparison table": len(option_units) >= 2 and bool(comparison_units),
    }
    return all(checks.get(item, False) for item in adapter.required_tables)
