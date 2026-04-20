# Vertical Slice Plan

## Goal

Build the smallest executable slice that proves the generic v2 contracts work without depending on any named domain.

## Input Contract

The minimal input object is:

- `topic`
- `reader`
- `use_context`
- `desired_depth`
- `jurisdiction`
- `mode`: `scoped` or `full`

No topic-specific prompt fragment is permitted in the core input template.

## Output Contract

The minimal slice must render:

- `final_report.md`
- `domain-adapter.md`
- `metrics.json`
- `claim-ledger.tsv`
- `citation-ledger.tsv`
- `release-gate-summary.md`

Optional but recommended:

- `source-log.tsv`
- `contradiction-log.md`
- `evidence-gap-log.md`
- `uncertainty-and-scope.md`

## Minimum Behavior

- high-risk claims appear in the claim ledger
- unsupported high-risk claims prevent `complete`
- scoped-search absence claims do not become facts
- scoped run is never labeled full-equivalent
- report headings remain reader-facing
- release gate honors target waivers explicitly

## Minimal Runtime Plan

1. Normalize input request.
2. Run `intent_classifier`.
3. Run `risk_tier_classifier`.
4. Run `scope_budget_planner`.
5. Run `domain_adapter_generator`.
6. Run `source_strategy_builder`.
7. Accept a small synthetic `source_packets` input for the first slice.
8. Run `report_planner`.
9. Run `draft_writer`.
10. Run `claim_extractor`.
11. Run `evidence_mapper`.
12. Run `contradiction_absence_guard`.
13. Run `tone_controller`.
14. Run `release_gate`.
15. Run `bundle_renderer`.

## Pseudocode

```python
request = normalize_request(payload)
intent = intent_classifier(request)
risk = risk_tier_classifier(request, intent)
budget = scope_budget_planner(request, intent, risk)
adapter = domain_adapter_generator(request, intent, risk, budget)
strategy = source_strategy_builder(intent, risk, adapter)
evidence = evidence_collector(request, strategy, adapter)
plan = report_planner(request, adapter, strategy, budget)
draft = draft_writer(plan, adapter, evidence, budget)
claims = claim_extractor(draft)
claims, citations = evidence_mapper(claims, evidence, strategy)
claims, contradictions, gaps = contradiction_absence_guard(
    claims, citations, evidence, budget
)
draft = tone_controller(draft, claims)
metrics = build_metrics(request, budget, claims, citations, contradictions, gaps)
gate = release_gate(claims, citations, contradictions, gaps, metrics, budget, adapter)
bundle_renderer(draft, adapter, metrics, claims, citations, gate)
```

## Acceptance Tests

### A. High-Risk Claim Blocking

- create a synthetic high-risk regulatory claim with only weak secondary support
- expected result: `blocked`

### B. Scoped Absence Claim

- create an absence claim labeled `not_found_in_scoped_search`
- expected result: claim cannot be `supported`; mainline prose must stay scoped

### C. Scoped Honesty

- run with `mode=scoped`
- expected result: `full_dr_equivalent=false` and report summary notes scoped status explicitly

### D. Reader-Facing Headings

- generated report cannot contain raw internal headings like `claim audit` or `evidence matrix`

### E. Target Miss Without Waiver

- configure a required target and fail it without waiver
- expected result: `needs_revision` or `blocked`, never `complete`

