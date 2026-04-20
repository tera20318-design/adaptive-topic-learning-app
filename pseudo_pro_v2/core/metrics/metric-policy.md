# Metric Policy

## Purpose

Metrics exist to expose coverage and support truthfully.
They are not allowed to disguise weak high-risk support behind aggregate counts.

## Core Metrics

These metrics are mandatory:

- `report_claim_capture_ratio`
- `supported_claim_ratio`
- `high_risk_claim_capture_ratio`
- `high_risk_supported_claim_ratio`
- `weak_claim_ratio`
- `missing_claim_ratio`
- `out_of_scope_claim_ratio`
- `unsupported_high_risk_count`

## Metric Meanings

- `report_claim_capture_ratio`:
  how much of the final report text became ledger rows
- `supported_claim_ratio`:
  the share of all captured claims marked `supported`
- `high_risk_claim_capture_ratio`:
  whether high-risk claims in the report were captured by the ledger
- `high_risk_supported_claim_ratio`:
  the share of high-risk claims that are actually supported
- `weak_claim_ratio`:
  the share of claims still dependent on weak evidence
- `missing_claim_ratio`:
  the share of claims without sufficient evidence
- `out_of_scope_claim_ratio`:
  the share of claims whose evidence does not match scope
- `unsupported_high_risk_count`:
  count of high-risk claims not in `supported`

## Mandatory Separation

Never treat these as equivalent:

- "the claim was captured in the ledger"
- "the claim is supported by evidence"

Capture is an audit property.
Support is an evidentiary property.

## Optional Diagnostic Metrics

Optional diagnostics may include:

- `primary_source_ratio`
- `authoritative_source_ratio`
- `unique_cited_source_count`
- `citation_instance_count`
- `adversarial_search_count`

These are useful diagnostics, but they do not by themselves authorize `complete`.
If any optional metric is elevated to a required target for a run, a miss needs an explicit waiver.

