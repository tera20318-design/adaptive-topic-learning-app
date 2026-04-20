# Release Gate

## Allowed States

- `complete`
- `provisional`
- `needs_revision`
- `blocked`

## Global Gate Principles

- gate decisions are claim-centered, not artifact-centered
- high-risk claims are evaluated claim by claim
- aggregate metrics never override claim-level failures
- no target miss may be ignored without waiver
- "decision-usable" is evaluated with the rubric in [decision-usable-rubric.md](decision-usable-rubric.md)

## `complete`

`complete` requires all of the following:

- final report is decision-usable for the declared reader and scope
- `high_risk_supported_claim_ratio == 1.0`
- `unsupported_high_risk_count == 0`
- no critical artifact is missing
- metadata is consistent
- source-role requirements are satisfied for high-risk claims
- scoped/full labeling is honest
- reader decision layer is present
- uncertainty section is present
- no unresolved critical contradiction
- no unsupported high-risk absence claim
- no target miss without waiver

If the run is scoped and not full-equivalent, it should be described as scoped complete, not as full-equivalent complete.

## `provisional`

Use `provisional` when:

- the report is useful but limited
- the run is scoped
- only minor non-critical gaps remain
- limitations are explicit
- target misses, if any, have explicit waivers

## `needs_revision`

Use `needs_revision` when:

- medium-risk support is incomplete
- decision layer is weak
- metadata mismatches remain
- source-role mismatches remain
- a required table or checklist is missing
- a required target is missed and no waiver is approved

## `blocked`

Use `blocked` when:

- any unsupported high-risk regulatory, legal, medical, financial, or safety claim remains
- an authoritative source creates a false-negative conflict
- `claim-ledger.tsv` is missing
- `citation-ledger.tsv` is missing
- the report cites a source absent from the ledger
- `complete` is claimed despite failed metrics
- a high-risk absence claim is based only on scoped search

## Required Inputs

The gate should read at least:

- claim ledger
- citation ledger
- contradiction log
- evidence-gap log
- scope metadata
- metrics
- target/waiver state

## Explicit Non-Rules

- file count is not quality
- source count is not quality
- high global source ratio is not sufficient
- report readability alone is not sufficient
