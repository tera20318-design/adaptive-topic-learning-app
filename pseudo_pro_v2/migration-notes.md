# Migration Notes

## Good Candidates To Migrate Next

- Generic dataclass shapes and schema-validation helpers from the existing clean-room work where they remain topic-neutral.
- Bundle rendering patterns for `metrics.json`, ledgers, and release summaries.
- Path-resolution helpers and fixture harness structure, as long as fixture content stays outside core.
- Stage contract validation patterns that stay machine-checkable and topic-neutral.

## Not Yet Migrated

- Any live retrieval flow, because this slice is intentionally synthetic-first.
- Any contradiction miner that depends on topic-specific search families.
- Any citation-span or table parser that assumes a legacy report format.
- Any document ingestion path that assumes a particular file format or named connector.

## Still Intentionally Discarded

- Topic-shaped required angles in core prompts or templates.
- Artifact-first success criteria that can mask weak report quality.
- Gates that redefine success targets after the run.
- Any rule that turns “not found in scoped search” into a factual absence.
- Any logic that blurs `claim captured` with `claim supported`.

## Migration Rule

- Move only abstractions, validators, and neutral rendering utilities.
- Do not move topic nouns, topic risk lists, legacy failure wording, or old search-specific heuristics into `core/`.
- Preserve the separation between generated domain adapters, fixture packets, and core runtime policy.
