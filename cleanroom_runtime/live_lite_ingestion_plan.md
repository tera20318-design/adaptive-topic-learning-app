# Live-Lite Ingestion Plan

This pass moves `cleanroom_runtime` from a packet-shape thought exercise to a bounded live-lite ingestion contract.

## Boundary

The runtime still does not perform live retrieval itself. The boundary is:

1. fetch, parse, or upload handling happens outside core
2. raw payloads are normalized into `normalized_source_packet.schema.json`
3. `src/cleanroom_runtime/ingestion/loader.py` validates the normalized packet collection
4. only validated packets become `SourcePacket` models
5. `stages/evidence_ingestion.py` consumes normalized packets plus document-grounded packets

This keeps live-lite readiness explicit without pretending the synthetic harness is already live research.

## Normalized source packet v2

The schema now preserves these topic-neutral contracts:

- `provenance`
  - packet origin
  - adapter identity
  - canonical locator data
  - retrieval and observation timestamps
  - content digest
  - metadata consistency
  - citation trace completeness
  - stale / malformed / partial state
- `role_assignment`
  - declared role
  - inferred role
  - effective role
  - assignment method and basis
  - review requirement
- `dedupe`
  - dedupe key
  - basis
  - confidence
  - cluster lineage
  - merged packet lineage
- `ingestion_health`
  - fetch status
  - parse status
  - partial failure stage / reason
  - malformed and dropped fields
- `staleness`
  - stale status
  - stale as-of point
  - supersession lineage
- finding `traceability`
  - support excerpt
  - locator type / value
  - extraction method
  - digest linkage

## Loader behavior

`load_normalized_source_packets(...)` now acts as the live-lite gate.

- malformed packet objects are rejected before runtime entry
- malformed finding rows are quarantined while salvageable packets can still pass through as partial
- inferred authoritative roles are bounded to `unknown`
- stale packets are flagged instead of silently normalized away
- dedupe lineage is retained through `dedupe_parent_ids`
- missing critical provenance for high-risk support remains visible downstream

## Document-grounded mode

`ingestion/document_grounding.py` provides the minimal document-grounded path.

- raw text and markdown excerpts become normalized packets
- findings carry direct grounding markers and source span coordinates
- document review remains scope-limited
- user-provided text does not satisfy high-risk authoritative support by itself

## Partial failure handling

The loader distinguishes:

- packet rejection
- packet salvage with malformed findings removed
- packet salvage with stale or incomplete metadata
- bounded role inference that degrades support instead of upgrading it

This is intentionally conservative. A packet may be usable for audit while still being unusable for release.

## Dedupe contract

Dedupe is still boundary-scoped, not truth-scoped.

- packet dedupe may cluster mirrors and variant URLs
- dedupe does not collapse contradictory findings into one truth claim
- merged lineage must remain inspectable
- stale/current tension must stay visible after dedupe

## Remaining boundary

Still not implemented:

- live fetching
- redirect and crawler provenance
- parser-specific extraction metadata beyond the normalized fields
- independent freshness verification
- automatic role inference from site patterns

The current runtime is therefore live-lite ready at the packet boundary, not live-retrieval complete.
