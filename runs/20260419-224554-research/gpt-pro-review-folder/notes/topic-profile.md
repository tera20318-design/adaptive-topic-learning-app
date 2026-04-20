# Topic Stop Profile

- Run ID: 20260419-224554-research
- Topic: めっき
- Preset: dr_ultra
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.
- Topic scope: standard (manual_override, breadth score 50)
- Budget scale: 0.45

## Stop posture

standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800

## Signals

- manual_override:focused_overview_report
- manual_override:no_prior_run_reuse
- manual_override:technology_overview

## Effective controls

- Query budget: 24
- Raw hit budget: 80
- Open budget: 30
- Deep-read budget: 14
- Novelty stop threshold: 0.04
- Max same-domain ratio: 0.18

## Use

- Stop widening once official, standards/professional, industry, vendor, and regulatory classes are all represented.
- Prefer closing high-risk claim gaps over adding more same-domain sources.
- Keep the run scoped: it is a focused overview, not a full DR-equivalent saturation pass.
