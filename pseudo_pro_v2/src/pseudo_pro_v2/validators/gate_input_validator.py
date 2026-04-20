from __future__ import annotations

from pseudo_pro_v2.models import ClaimLedgerRow, CitationLedgerRow, ReportDraft


def validate_release_gate_inputs(
    draft: ReportDraft,
    claims: list[ClaimLedgerRow],
    citations: list[CitationLedgerRow],
    metrics: dict,
) -> list[str]:
    errors: list[str] = []
    included_claim_count = len([claim for claim in claims if claim.included_in_report])
    included_citation_count = len([citation for citation in citations if citation.included_in_report])
    if not draft.sections:
        errors.append("draft has no sections")
    if metrics.get("claim_count") != len(claims):
        errors.append("claim_count metric does not match claim ledger length")
    if metrics.get("included_claim_count") != included_claim_count:
        errors.append("included_claim_count metric does not match included claims")
    if metrics.get("citation_count") != len(citations):
        errors.append("citation_count metric does not match citation ledger length")
    if metrics.get("included_citation_count") != included_citation_count:
        errors.append("included_citation_count metric does not match included citations")
    if "citation_trace_consistent" not in metrics:
        errors.append("metrics missing citation_trace_consistent")
    if "document_grounding_present" not in metrics:
        errors.append("metrics missing document_grounding_present")
    if "release_status_candidate" not in metrics:
        errors.append("metrics missing release_status_candidate")
    return errors
