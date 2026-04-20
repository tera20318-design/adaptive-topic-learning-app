# Pseudo-Pro v2 Architecture

## Core Modules

1. `intent_classifier`
   Classifies the user request into report shape and decision intent.
2. `risk_tier_classifier`
   Detects high-stakes domains and sets the risk tier.
3. `scope_budget_planner`
   Separates requested mode, effective mode, original budget, and effective budget.
4. `domain_adapter_generator`
   Discovers topic-specific risk and explanation needs without hard-coding topic words in the core.
5. `source_strategy_builder`
   Maps claim kinds to required source roles.
6. `evidence_collector`
   Normalizes source packets and records weakness, staleness, and vendor dependence.
7. `report_planner`
   Designs the reader-facing structure before drafting.
8. `draft_writer`
   Writes a first reader-facing report without internal pipeline headings.
9. `claim_extractor`
   Extracts claims from the final report units and preserves exact text spans.
10. `evidence_mapper`
    Scores support status claim-by-claim.
11. `contradiction_absence_guard`
    Handles contradictions, absence claims, negative evidence, and scope mismatch.
12. `tone_controller`
    Adjusts assertion strength to the support state.
13. `release_gate`
    Produces `complete`, `provisional`, `needs_revision`, or `blocked`.
14. `bundle_renderer`
    Writes the report bundle consistently.
15. `regression_runner`
    Runs fixture-based checks without contaminating the core rules.

## Vertical Slice

The implemented vertical slice accepts a structured local request plus structured source packets.
It produces:

- `final_report.md`
- `metrics.json`
- `release-gate-summary.md`
- `domain-adapter.md`
- `source-log.tsv`
- `citation-ledger.tsv`
- `claim-ledger.tsv`
- `contradiction-log.md`
- `evidence-gap-log.md`
- `uncertainty-and-scope.md`

## Why This Is Clean-Room

- No imports from `research-os/`
- No dependency on the old prompt files
- No hard-coded topic families in release logic
- No theme-specific required headings in the core
- Regression fixtures live under `fixtures/` and are evaluated separately
