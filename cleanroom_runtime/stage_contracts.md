# Stage Contracts

`cleanroom_runtime/src/cleanroom_runtime/stage_contracts.py` is the source of truth for stage handoff rules.

Current strictness model:

- every registered stage contract is marked `strict`
- failure codes come from the enum in `cleanroom_runtime/src/cleanroom_runtime/types.py`
- `validate_stage_contract_registry()` checks registry completeness and enum coverage
- `validate_stage_snapshot()` checks emitted snapshots against the declared schema and per-stage summary coverage

Each stage contract defines:

- required fields that must be populated before handoff
- downstream must-have fields keyed by consumer stage
- explicit failure codes for missing fields, schema failures, semantic leakage, and invariant breaks
- snapshot fields that must be summarized in the emitted stage snapshot
- stage invariants for claim coverage, limitation visibility, target accounting, tone rules, and release semantics
- source-strategy alignment invariants for both source priority and claim-kind role maps

Stage snapshot schema:

- version: `stage_contract.v2`
- required fields:
  - `stage`
  - `artifact_type`
  - `required_fields`
  - `downstream_must_have_fields`
  - `invariant_codes`
  - `contract_ok`
  - `failure_codes`
  - `summary`
  - `snapshot_schema_version`
- `summary` must cover every field declared in the stage contract's `snapshot_fields`

Semantic isolation is enforced at the contract layer for reader-facing text. The current semantic leakage failure codes are:

- `SEMANTIC_FIXTURE_NOUN_LEAK`
- `SEMANTIC_RISK_PHRASE_LEAK`
- `SEMANTIC_REGULATION_WORDING_LEAK`
- `SEMANTIC_OVERCLAIM_PHRASING_LEAK`

Generic contract failures use:

- `REQUIRED_FIELD_MISSING`
- `DOWNSTREAM_FIELD_MISSING`
- `SCHEMA_VALIDATION_FAILED`

`cleanroom_runtime/src/cleanroom_runtime/core/stage_contracts.py` remains as a compatibility wrapper around the same contract registry and validators.
