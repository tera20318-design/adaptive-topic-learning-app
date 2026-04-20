# Implementation Delta

This pass moves `cleanroom_runtime` from a live-lite readiness boundary toward a minimal live-lite execution path.

## Live-lite execution path

- Kept normalized packet ingestion executable instead of boundary-only.
- Preserved packet validation ahead of runtime entry.
- Kept malformed packet rejection, partial salvage, stale warnings, and dedupe collision notes visible in the ingestion audit.
- Regenerated packet-ingestion audit artifacts so rejection and salvage summaries remain inspectable after runtime execution.

## Document grounding v3

- Extended raw document handling from bounded excerpt mode into `document_review` mode for checked multi-paragraph text.
- Preserved direct grounding markers, span labels, and span offsets from:
  - grounded findings
  - report units
  - claim ledger rows
  - citation ledger rows
- Kept separate checked document spans separate so unsupported synthesis across distinct blocks cannot silently clear support.
- Blocked or revised summary prose that outruns the grounded checked spans.

## Traceability v3

- Tightened span-based lineage across:
  - prose -> claim
  - claim -> finding
  - finding -> source excerpt/span
- Added report-unit carriage for grounding markers and finding span metadata so claim extraction no longer drops document traceability.
- Kept high-risk mainline prose blocked when inspectable provenance or span lineage is missing.
- Updated rendered ledgers to include the newer span and grounding columns consistently.

## Contradiction and freshness handling

- Preserved same-subject authoritative contradiction as release-blocking.
- Kept mixed-jurisdiction collapse separate from true same-subject contradiction.
- Preserved authoritative checked absence as scoped and typed, with revision pressure when scope remains implicit.
- Kept stale/current tension visible instead of letting freshness shortcuts silently resolve support.

## Fixtures and packet realism

- Synced runtime-used `source_packets.json` fixtures with the richer grounding fields already present in synthetic packet variants.
- Updated default multigenre expectations where the hardened runtime now honestly lands at `needs_revision` rather than `blocked` or `provisional`.
- Regenerated live-lite and multigenre outputs after the contract changes.

## Tests covered in this pass

- `tests/test_live_lite_execution.py`
- `tests/test_user_document_grounding_v3.py`
- `tests/test_traceability_v3.py`
- `tests/test_contradiction_hardening_v3.py`
- `tests/test_realish_packets_v3.py`
- updated multigenre / richer-packet / realish-packet expectation coverage

## Still intentionally synthetic

- No live web retrieval
- No OCR or parser-mediated file extraction
- No independent timestamp verification
- No claim that synthetic passage through the runtime proves real-world research completeness
