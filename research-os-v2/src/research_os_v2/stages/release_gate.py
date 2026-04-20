from __future__ import annotations

from research_os_v2.catalogs import HIGH_RISK_CLAIM_KINDS
from research_os_v2.models import ClaimLedgerRow, EvidenceGapEntry, ReleaseGateDecision


def decide_release_gate(
    claims: list[ClaimLedgerRow],
    gaps: list[EvidenceGapEntry],
    *,
    metadata_consistent: bool,
    has_claim_ledger: bool,
    has_citation_ledger: bool,
    high_risk_absence_supported: bool,
    reader_decision_layer_present: bool,
    uncertainty_section_present: bool,
    scoped_run_honest: bool,
) -> ReleaseGateDecision:
    blocking_reasons: list[str] = []
    revision_reasons: list[str] = []
    unresolved_gaps: list[str] = [gap.detail for gap in gaps]

    unsupported_high_risk = [
        claim for claim in claims
        if claim.risk_level == "high" and claim.support_status in {"missing", "weak", "out_of_scope"}
    ]
    critical_unsupported_high_risk = [
        claim for claim in unsupported_high_risk
        if claim.claim_kind in HIGH_RISK_CLAIM_KINDS
    ]
    missing_medium_risk = [
        claim for claim in claims
        if claim.risk_level == "medium" and claim.support_status in {"missing", "out_of_scope"}
    ]

    if not has_claim_ledger:
        blocking_reasons.append("claim-ledger is missing.")
    if not has_citation_ledger:
        blocking_reasons.append("citation-ledger is missing.")
    if critical_unsupported_high_risk:
        blocking_reasons.append("There are unsupported or unresolved high-risk claims.")
    if not high_risk_absence_supported:
        blocking_reasons.append("A high-risk absence claim is unsupported.")
    if not metadata_consistent:
        revision_reasons.append("Metadata is inconsistent.")
    if not reader_decision_layer_present:
        revision_reasons.append("Reader decision layer is missing.")
    if not uncertainty_section_present:
        revision_reasons.append("Uncertainty section is missing.")
    if not scoped_run_honest:
        revision_reasons.append("Scoped/full labeling is not honest.")
    if missing_medium_risk:
        revision_reasons.append("There are medium-risk claims that still need stronger support.")

    if blocking_reasons:
        return ReleaseGateDecision(
            status="blocked",
            reasons=blocking_reasons + revision_reasons,
            blocking_reasons=blocking_reasons,
            unresolved_gaps=unresolved_gaps,
            metadata_consistent=metadata_consistent,
        )

    if revision_reasons:
        return ReleaseGateDecision(
            status="needs_revision",
            reasons=revision_reasons,
            blocking_reasons=[],
            unresolved_gaps=unresolved_gaps,
            metadata_consistent=metadata_consistent,
        )

    has_any_weak = any(claim.support_status == "weak" for claim in claims)
    if has_any_weak:
        return ReleaseGateDecision(
            status="provisional",
            reasons=["Useful but still limited by weak claims or scoped evidence."],
            blocking_reasons=[],
            unresolved_gaps=unresolved_gaps,
            metadata_consistent=metadata_consistent,
        )

    return ReleaseGateDecision(
        status="complete",
        reasons=["The bundle meets the current run conditions without unresolved critical gaps."],
        blocking_reasons=[],
        unresolved_gaps=unresolved_gaps,
        metadata_consistent=metadata_consistent,
    )
