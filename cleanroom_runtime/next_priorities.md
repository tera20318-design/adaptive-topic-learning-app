# Next Priorities

- add a real fetch adapter that emits normalized packets from external inputs before runtime construction
- preserve redirect lineage, parser identity, fetch timestamps, locator fidelity, and raw artifact handles without leaking local absolute paths
- move document grounding from checked raw text into parser-mediated excerpts while keeping inspectable span lineage in findings, claims, and citations
- surface rejection, salvage, dedupe, and stale-source summaries directly in rendered reader-facing release artifacts, not only in stage snapshots
- harden canonical URL normalization for duplicate packets with partial metadata and mixed stale/current clusters
- add packet-inventory mismatch metrics between requested inputs, ingested packets, cited evidence, audit-only claims, and excluded evidence
- add live-lite regression fixtures that combine fetch failure, provenance gaps, stale authority, mixed-jurisdiction tension, and document-grounding pressure in one run
