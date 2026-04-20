# Next Implementation Priorities

1. Add live-lite ingestion that maps external sources or user documents into the existing `SourcePacket` contract without changing gate semantics.
2. Add citation-span alignment so rendered prose, claim ledger rows, and citation ledger rows can be traced at span granularity.
3. Add deeper contradiction mining and adversarial absence checks on top of the current packet-based guard.
4. Add direct user-document ingestion that preserves the same document-grounding release checks.
5. Add fixture execution for runtime-mutated scenarios such as citation trace mismatch, stale-source pressure, and waiver-free target misses.
6. Reduce remaining repo-local bootstrap fallbacks once the installable package path is exercised more often.
