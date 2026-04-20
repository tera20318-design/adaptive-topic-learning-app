# Reuse And Discard

## Reuse From Existing Pipeline

These are reusable as abstract ideas or partial implementations:

- stage-based pipeline decomposition
- typed catalogs for `source_role`, `claim_kind`, `absence_type`, and release statuses
- separate ledgers for claims and citations
- explicit scope/budget metadata with `requested_mode` and `effective_mode`
- contradiction and absence handling as a dedicated stage
- rendering a bundle with report plus audit artifacts

These are the best file-level candidates for careful migration by abstraction, not direct copy:

- `research-os-v2/src/research_os_v2/catalogs.py`
- `research-os-v2/src/research_os_v2/models.py`
- `research-os-v2/src/research_os_v2/stages/scope_budget_planner.py`
- `research-os-v2/src/research_os_v2/stages/claim_extractor.py`
- `research-os-v2/src/research_os_v2/stages/evidence_mapper.py`
- `research-os-v2/src/research_os_v2/stages/contradiction_absence_guard.py`

## Discard From Existing Pipeline

These patterns should not be migrated as-is:

- evidence-derived domain adapter defaults that backfill missing topic analysis too easily
- release gating that treats aggregate artifact presence as near-sufficient
- any logic path where target misses do not require waiver handling
- any tone or template behavior that adds generic filler rather than evidence-aware wording
- fixture execution that maps broad expected states like `allow/review/block` instead of claim-centered assertions
- any implicit assumption that a run with all rendered files is architecture-valid

## Legacy False-Negative Risks To Correct

These are not migration targets; they are warning signs for the clean-room rewrite:

- alias-heavy input normalization lets fixture vocabulary leak into core parsing
  - see `research-os-v2/src/research_os_v2/input_loader.py`
- adapter generation currently aggregates evidence annotations instead of generating topic needs from abstract policy
  - see `research-os-v2/src/research_os_v2/stages/domain_adapter_generator.py`
- draft writing is too close to packet-first rendering and can inherit fixture annotation structure
  - see `research-os-v2/src/research_os_v2/stages/draft_writer.py`
- current `high_risk_claim_capture_ratio` is effectively tautological and does not detect missed high-risk claims
  - see `research-os-v2/src/research_os_v2/pipeline.py`
- current metadata consistency is too close to a self-check because citations are built from the same mapped source IDs
  - see `research-os-v2/src/research_os_v2/pipeline.py`
- contradiction logging and source quality notes are not strong enough as direct release controls
  - see `research-os-v2/src/research_os_v2/stages/contradiction_absence_guard.py`
  - see `research-os-v2/src/research_os_v2/stages/evidence_collector.py`

## Migration Principle

Migrate only abstractions.
Do not migrate topic-shaped source packets, report text, fixture vocabularies, or rescue heuristics that came from a single historical run.
