# Contradiction Policy

cleanroom_runtime treats contradiction handling as a claim-centered release concern, not as a prose cleanup step.

## Core rules

- Same-subject contradictions are evaluated separately from different-subject disagreement.
- Subject-boundary evidence outranks surface wording overlap.
- Mixed-jurisdiction disagreement must not be flattened into a same-subject contradiction.
- Mixed-jurisdiction evidence must not be collapsed into one high-risk rule.
- Absence claims stay typed and scoped.
- Freshness handling is asymmetric:
  - fresh authoritative evidence can override stale authoritative evidence for the same subject
  - fresh lower-role evidence cannot silently override stale authoritative evidence

## Contradiction classes

- `same_subject_authoritative_conflict`
  - unresolved same-subject authoritative conflict
  - release-blocking
- `fresh_authoritative_override`
  - fresher authoritative support displaces stale authoritative support
  - stale support stays visible in audit
- `stale_authoritative_vs_fresh_lower_role_tension`
  - fresher lower-role support conflicts with stale authoritative support
  - requires caveat and current authoritative confirmation
- `mixed_jurisdiction_scope_delta`
  - jurisdiction differs
  - must not be treated as a same-subject contradiction
- `mixed_jurisdiction_scope_collapse`
  - one high-risk claim collapses evidence from multiple jurisdictions into one rule
  - release-blocking
- `user_excerpt_extrapolation`
  - checked excerpt is stretched beyond its visible scope
  - treated as a grounding and scope failure

## Authority and freshness

- Unresolved same-subject authoritative contradiction is blocking.
- A fresher authoritative source can override stale authoritative support for the same subject.
- A fresher lower-role source does not settle the issue against stale authoritative support.
- Historical or stale source material used as if it proves the current state requires revision unless a freshness caveat is visible.
- High-risk claims weakened by contradiction or freshness handling must move to audit-only until support is repaired.

## Absence handling

- `scoped_search_absence` remains the weakest absence form.
- `checked_scope_absence` can remain only as scoped absence.
- `authoritative_checked_absence` is stronger than scoped search but still does not prove global absence.
- Authoritative absence without an explicit scope statement is blocking.
- Checked source IDs alone are not enough.

## Current boundary

- The guard reasons over bundle metadata already present in the runtime:
  - subject keys
  - source roles
  - jurisdictions
  - absence typing
  - provenance stale flags
  - freshness tags
- The guard does not fetch live sources or independently verify timestamps.
- Freshness remains only as strong as the packet metadata supplied to the runtime.
