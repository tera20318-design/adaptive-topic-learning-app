# Topic Stop Profile

- Run ID: 20260419-101901-research
- Topic: めっき
- Preset: dr_ultra logic scaffold
- Topic scope: standard (manual_override, breadth score 50)
- Budget scale: 0.45
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.

## Stop posture

standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800

## Signals

- The topic is broad in vocabulary but this run is intentionally narrowed to a practical overview report.
- The user explicitly requested a fresh run with no prior-run reuse.
- The required deliverable is a Japanese narrative report, not a market-sizing dossier.
- This run uses dr_ultra logic as a checklist scaffold, but it is not intended to be dr_ultra-equivalent in search breadth, tail sweep, or deep-read volume.

## Effective controls

- Query budget: 24
- Raw hit budget: 80
- Open budget: 30
- Deep-read budget: 14
- Novelty stop threshold: 0.04
- Max same-domain ratio: 0.18

## Use

- This focused-budget run should stop once the core decision layer is evidenced; it should not try to chase full dr_ultra tail coverage.
- If weak claims appear, switch to gap-closing before widening the search again.
- Treat missing long-tail entity coverage as acceptable in this pass unless it blocks the practical overview.

## Run-specific interpretation

- Treat "めっき" as a practical surface-engineering overview topic.
- Cover four method families: electroplating, electroless plating, hot-dip plating, and dry/vacuum surface treatment as a boundary concept.
- Prioritize Japan-facing regulatory and manufacturing context over global market statistics.
- Keep entity discovery off unless a later pass explicitly expands scope.
- Consider the run complete when method definitions, major applications, plating-specific failure modes, and environmental/safety constraints are all evidenced with current sources.
