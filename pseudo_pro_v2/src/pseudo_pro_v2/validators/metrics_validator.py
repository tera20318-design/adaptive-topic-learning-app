from __future__ import annotations


REQUIRED_METRICS = [
    "requested_mode",
    "effective_mode",
    "preset_baseline_budget",
    "effective_budget",
    "override_reason",
    "override_authority",
    "full_dr_equivalent",
    "report_status_implication",
    "limitations",
    "report_claim_capture_ratio",
    "supported_claim_ratio",
    "high_risk_claim_capture_ratio",
    "high_risk_supported_claim_ratio",
    "unsupported_high_risk_count",
    "claim_count",
    "included_claim_count",
    "excluded_claim_count",
    "citation_count",
    "included_citation_count",
    "source_finding_count",
    "captured_source_finding_count",
    "source_finding_ledger_coverage_ratio",
    "metadata_consistent",
    "citation_trace_consistent",
    "rendered_citation_trace_consistent",
    "citation_trace_mismatch_count",
    "document_grounding_present",
    "synthetic_inputs",
    "synthetic_complete_allowed",
    "release_status_candidate",
]


def validate_metrics(metrics: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_METRICS:
        if key not in metrics:
            errors.append(f"metrics missing `{key}`")

    for ratio_key in [
        "report_claim_capture_ratio",
        "supported_claim_ratio",
        "high_risk_claim_capture_ratio",
        "high_risk_supported_claim_ratio",
        "source_finding_ledger_coverage_ratio",
    ]:
        value = metrics.get(ratio_key)
        if value is None:
            continue
        if not isinstance(value, (int, float)):
            errors.append(f"`{ratio_key}` should be numeric")
        elif value < 0 or value > 1:
            errors.append(f"`{ratio_key}` should be between 0 and 1")

    if not isinstance(metrics.get("unsupported_high_risk_count", 0), int):
        errors.append("`unsupported_high_risk_count` should be integer")
    if not isinstance(metrics.get("citation_trace_mismatch_count", 0), int):
        errors.append("`citation_trace_mismatch_count` should be integer")

    return errors
