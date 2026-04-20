# Migration Note

## Reused As Abstractions

- stage-based pipeline decomposition
- typed source-role and claim-kind catalogs
- explicit separation between report draft, claim ledger, citation ledger, and release decision
- dedicated contradiction/absence handling stage
- bundle rendering that emits reader-facing and audit-facing artifacts

## Intentionally Discarded

- evidence-derived domain adapters that backfill domain logic from the same evidence later used to justify claims
- self-fulfilling metrics such as capture ratios computed from the same artifact set they claim to validate
- release logic that treats artifact presence as equivalent to claim support
- report generation that duplicates the same finding across multiple sections to inflate the bundle
- any assumption that synthetic validation proves live research completeness
- brittle fixture vocabulary and named-domain behavior in core logic

## Resulting Runtime Differences

- domain adaptation is generated per run from request/risk/intent metadata, not from evidence packets
- absence claims use explicit typed scope rather than being treated as ordinary facts
- unsupported high-risk claims may be excluded from reader-facing prose, but they remain in audit artifacts
- contract completeness and research completeness are tracked separately
- release gating is centered on claim support and audit visibility, not on rendered file count
