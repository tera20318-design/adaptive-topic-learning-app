# Release Gate Summary

- Status: `blocked`
- Contract complete: `false`
- Research completeness: `synthetic_validation_only`

## Reasons

- [evidence_ingestion:SCHEMA_VALIDATION_FAILED] finding tech-finding-001 references unknown source_ids: TECH-MISSING-999
- [evidence_ingestion:EVIDENCE_FINDING_SOURCE_LINEAGE] evidence findings must only reference ingested source IDs.
- [evidence_mapper:SCHEMA_VALIDATION_FAILED] citation citation-002 references unknown source_id 'TECH-MISSING-999'
- citation `citation-002` points to unknown source `TECH-MISSING-999`
- Citation traceability is incomplete.
- Traceability is incomplete between reader-facing prose, claim rows, and citations.
- One or more high-risk claims rely on sources with incomplete provenance or ambiguous role inference.
- Metadata inconsistency coexists with unresolved high-risk claims.
- Audit-only but still blocks release: unresolved high-risk claim (`missing`).
- Required source roles were not satisfied for a high-risk claim.

## Blocking Reasons

- [evidence_ingestion:SCHEMA_VALIDATION_FAILED] finding tech-finding-001 references unknown source_ids: TECH-MISSING-999
- [evidence_ingestion:EVIDENCE_FINDING_SOURCE_LINEAGE] evidence findings must only reference ingested source IDs.
- [evidence_mapper:SCHEMA_VALIDATION_FAILED] citation citation-002 references unknown source_id 'TECH-MISSING-999'
- citation `citation-002` points to unknown source `TECH-MISSING-999`
- Citation traceability is incomplete.
- Traceability is incomplete between reader-facing prose, claim rows, and citations.
- One or more high-risk claims rely on sources with incomplete provenance or ambiguous role inference.
- Metadata inconsistency coexists with unresolved high-risk claims.
- Audit-only but still blocks release: unresolved high-risk claim (`missing`).
- Required source roles were not satisfied for a high-risk claim.

## Unresolved Gaps

- None
