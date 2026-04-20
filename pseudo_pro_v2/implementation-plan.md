# Implementation Plan

## What Is Implemented

- A typed runtime under `src/pseudo_pro_v2/` now runs an end-to-end synthetic vertical slice.
- Validators exist for:
  - `domain-adapter.schema.json`
  - `claim-ledger.schema.tsv`
  - `citation-ledger.schema.tsv`
  - release-gate inputs
  - metrics
- The implemented stage chain is:
  - `intent_classifier`
  - `risk_tier_classifier`
  - `scope_budget_planner`
  - `domain_adapter_generator`
  - `source_strategy_builder`
  - `evidence_collector`
  - `report_planner`
  - `draft_writer`
  - `claim_extractor`
  - `evidence_mapper`
  - `contradiction_absence_guard`
  - `tone_controller`
  - `release_gate`
  - `bundle_renderer`
- A runnable harness exists at `scripts/run_vertical_slice.py`.
- Synthetic fixtures now live under `fixtures/` and are regenerated into `vertical-slice/generated/`.

## What Is Still Stubbed Or Minimal

- `intent_classifier`, `risk_tier_classifier`, and `scope_budget_planner` are heuristic, not model-driven.
- `domain_adapter_generator` is generic and dynamic, but still template-led rather than retrieval-led.
- `source_strategy_builder` is schema-based only. It does not yet adapt to actual source coverage gaps.
- `evidence_collector` is a synthetic packet loader. It does not perform live retrieval, deduplication, or freshness ranking.
- `claim_extractor` is unit-based. It does not yet do freeform span extraction from arbitrary prose.
- `contradiction_absence_guard` enforces the critical absence and scope rules, but does not yet do adversarial search or deeper contradiction mining.
- `tone_controller` applies a small set of tone modes. It is not yet style-adaptive by reader persona.
- `regression_runner` is still design-only in this implementation slice.

## What Is Synthetic In This Slice

- Input evidence is fixed JSON source packets under `fixtures/`.
- Source metadata, claims, and support hints are synthetic and intentionally generic.
- The implemented fixture genres are:
  - `technical_overview`
  - `legal_regulatory`
  - `medical_health`
  - `finance`
  - `product_comparison`

## Why This Slice Exists

- It proves that the v2 architecture can produce:
  - reader-facing `final_report.md`
  - typed ledgers
  - metrics that separate claim capture from claim support
  - gate decisions that reject unsupported high-risk claims
  - absence handling that prevents scoped search misses from becoming facts

## Exit Criteria For The Next Slice

- Replace synthetic evidence loading with a retrieval module that still preserves the same stage contracts.
- Add regression runner execution on top of the current harness.
- Upgrade claim extraction from unit-based capture to report-span extraction.
