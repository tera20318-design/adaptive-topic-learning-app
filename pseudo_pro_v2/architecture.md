# Architecture

## Design Goal

`pseudo_pro_v2` is a clean-room architecture for a generic pseudo-Pro / pseudo-Deep-Research pipeline.

The architecture must:

- answer arbitrary topics without hard-coding topic content into core
- distinguish core rules from fixture expectations
- make the final report the primary product
- preserve evidence traceability and uncertainty honesty
- prevent scoped runs from being mislabeled as full-equivalent work
- prevent topic execution from substituting for architecture work

## Hard Separation Rules

- `core/` holds abstract rules, schemas, prompt contracts, metrics, and gate logic.
- `adapters/generated/` holds per-run domain adapters derived from the input topic.
- `fixtures/` holds regression tests and topic-shaped traps.
- `tests/` validates contracts, gates, fixtures, and the minimal vertical slice.
- No named regulation, product, material, standard number, or past-run failure text belongs in `core/`.

## Proposed Layout

```text
pseudo_pro_v2/
  README.md
  postmortem.md
  architecture.md
  reuse-and-discard.md
  vertical-slice-plan.md
  next-implementation-priorities.md
  core/
    docs/
      absence-claim-policy.md
      scope-budget-policy.md
    schemas/
      domain-adapter.schema.json
      source-role.schema.md
      claim-ledger.schema.tsv
    templates/
      report-template.md
    gates/
      release-gate.md
    metrics/
      metric-policy.md
    prompts/
      README.md
    module_interfaces/
      README.md
  adapters/
    generated/
      README.md
  fixtures/
    README.md
    technical_overview/
    legal_regulatory/
    medical_health/
    finance/
    product_comparison/
    business_market/
    historical_cultural/
    user_document_review/
  tests/
    README.md
```

## Processing Sequence

1. Intake request and normalize metadata.
2. Classify intent.
3. Classify risk tier.
4. Plan scope and budget.
5. Generate domain adapter.
6. Build source strategy from claim kinds and risk tier.
7. Collect evidence.
8. Plan the reader-facing report.
9. Draft report prose.
10. Extract claims from the draft.
11. Map claims to evidence.
12. Apply contradiction and absence guard.
13. Apply tone control.
14. Decide release gate.
15. Render bundle.
16. Run regression fixtures outside core.

The design phase ends only after steps 1 to 15 are specified abstractly. Topic execution, if any, is a later validation step and is not part of this design artifact set.

## Mandatory Modules

### 1. `intent_classifier`

- Role:
  Classify the user's requested output shape such as report, comparison, decision memo, technical explainer, legal overview, product guide, literature review, or strategy memo.
- Input:
  normalized request metadata, including topic, reader, use context, desired depth, and user phrasing.
- Output:
  `intent_label`, `decision_focus`, `reader_task`, `report_shape_hints`.
- Failure behavior:
  fall back to `report` plus an explicit ambiguity note; do not guess a domain-specific structure.
- Required downstream fields:
  `intent_label`, `decision_focus`, `report_shape_hints`.
- Genericity note:
  classify output purpose, not topic content.

### 2. `risk_tier_classifier`

- Role:
  Detect whether the run touches high-stakes domains and whether elevated evidence controls are required.
- Input:
  normalized request and coarse intent.
- Output:
  `risk_tier`, `high_stakes_domains`, `risk_rationale`.
- Failure behavior:
  fail closed toward a higher tier when ambiguity affects safety, law, medicine, finance, regulation, procurement, or technical failure.
- Required downstream fields:
  `risk_tier`, `high_stakes_domains`.
- Genericity note:
  classify classes of risk, not named regulations or products.

### 3. `scope_budget_planner`

- Role:
  Separate requested mode from effective mode, baseline budget from actual budget, and declare whether the run is full-equivalent.
- Input:
  normalized request, intent, risk tier, system defaults, optional overrides.
- Output:
  `requested_mode`, `effective_mode`, `preset_baseline_budget`, `effective_budget`, `override_reason`, `override_authority`, `full_dr_equivalent`, `report_status_implication`, `limitations`, `target_waivers`.
- Failure behavior:
  if mode or target settings are inconsistent, downgrade release eligibility and emit limitation notes.
- Required downstream fields:
  all of the above.
- Genericity note:
  budget logic must not depend on topic-specific must-cover angles.

### 4. `domain_adapter_generator`

- Role:
  Generate a per-topic adapter that expresses likely failure modes, source priorities, decision context, misunderstandings, boundary concepts, and table requirements before any report plan is written.
- Input:
  normalized request, intent, risk tier, scope budget, and optionally early evidence signals.
- Output:
  a `domain_adapter` object conforming to `core/schemas/domain-adapter.schema.json`.
- Failure behavior:
  if adapter quality is low, block downstream report planning and emit `adapter_incomplete`.
- Required downstream fields:
  `topic`, `reader`, `use_context`, `output_type`, `risk_tier`, `temporal_sensitivity`, `jurisdiction_sensitivity`, `source_priority`, `high_risk_claim_types`, `likely_failure_modes`, `domain_specific_risks`, `common_misunderstandings`, `boundary_concepts`, `decision_context`, `required_decision_layer`, `required_tables`, `must_not_overgeneralize`, `known_limits`, `source_roles_required_by_claim_kind`.
- Genericity note:
  topic-shaped risks are generated per run and stored in adapters, never promoted into core defaults.

### 5. `source_strategy_builder`

- Role:
  Convert claim-kind expectations and risk tier into source-role requirements and retrieval priorities.
- Input:
  intent, risk tier, domain adapter.
- Output:
  `source_priority`, `required_source_roles_by_claim_kind`, `compatibility_notes`, optional `diagnostic_targets`.
- Failure behavior:
  if claim kinds lack source-role mapping, mark the run as `needs_revision` before drafting.
- Required downstream fields:
  `source_priority`, `required_source_roles_by_claim_kind`.
- Genericity note:
  source strategy is keyed by claim kind and risk, not by named domains.

### 6. `evidence_collector`

- Role:
  gather sources, assign source roles, record quality flags, and preserve scoped-search limitations.
- Input:
  request, domain adapter, source strategy, selected retrieval budget.
- Output:
  `source_packets`, `source_log`, `retrieval_log`, `source_quality_notes`.
- Failure behavior:
  if required source roles are missing for high-risk claim classes, record a blocking gap instead of silently continuing.
- Required downstream fields:
  `source_packets`, `source_log`, `source_quality_notes`.
- Genericity note:
  collection policy must remain role-based; named source lists belong in fixtures or adapters, not core.

### 7. `report_planner`

- Role:
  design the report structure from reader needs and decision context, not from pipeline internals.
- Input:
  intent, domain adapter, source strategy, scope budget.
- Output:
  ordered report sections, section goals, required tables, and section-level guardrails.
- Failure behavior:
  if required decision layer or tables are missing, stop before drafting.
- Required downstream fields:
  `section_plan`, `required_tables`, `decision_layer_requirements`.
- Genericity note:
  plan semantic sections, not internal headings such as "evidence matrix" or "upstream/downstream".

### 8. `draft_writer`

- Role:
  write the first reader-facing draft using the section plan and evidence packets.
- Input:
  report plan, domain adapter, source packets, scope metadata.
- Output:
  `draft_units`, `draft_markdown`, `section_source_references`.
- Failure behavior:
  if evidence is insufficient for a required section, mark the section as uncertain or omit the claim; do not invent filler.
- Required downstream fields:
  `draft_units`, `draft_markdown`.
- Genericity note:
  prose templates must remain abstract and section-semantic.

### 9. `claim_extractor`

- Role:
  extract every report claim from final prose, preserve the exact text span, and normalize claims for auditing.
- Input:
  final draft and claim-kind policy.
- Output:
  `claim_ledger_rows` with required schema fields.
- Failure behavior:
  if extraction misses sections or yields malformed rows, the run cannot be `complete`.
- Required downstream fields:
  the full claim ledger schema.
- Genericity note:
  extraction rules should operate on claim semantics, not topic keywords.

### 10. `evidence_mapper`

- Role:
  map each extracted claim to cited sources, derive required source roles, and assign support status.
- Input:
  claim ledger draft, source packets, source strategy.
- Output:
  updated claim ledger, citation ledger, support diagnostics.
- Failure behavior:
  unsupported high-risk claims remain explicit and block release.
- Required downstream fields:
  `source_ids`, `source_roles`, `evidence_count`, `required_source_role`, `support_status`, `confidence`, `caveat_required`, `suggested_tone`, `required_fix`.
- Genericity note:
  support logic must remain claim-centered and role-based.

### 11. `contradiction_absence_guard`

- Role:
  handle contradiction signals, negative evidence, typed absence claims, and scope mismatches.
- Input:
  claim ledger, citation ledger, source packets, scope metadata.
- Output:
  updated support statuses, contradiction log, evidence-gap log.
- Failure behavior:
  unresolved high-risk contradictions and unsupported high-risk absence claims block release.
- Required downstream fields:
  `contradiction_log`, `evidence_gap_log`, updated `support_status`, updated `required_fix`.
- Genericity note:
  absence policy is abstract and typed; topic-specific traps stay in fixtures.

### 12. `tone_controller`

- Role:
  adjust certainty and wording based on claim support and source role.
- Input:
  claim ledger and draft units.
- Output:
  toned draft plus tone annotations.
- Failure behavior:
  if tone cannot be made honest, the claim must be removed or marked unverified.
- Required downstream fields:
  `suggested_tone`, `caveat_required`, updated `exact_text_span`.
- Genericity note:
  tone policy depends on support semantics, not on named domains.

### 13. `release_gate`

- Role:
  decide `complete`, `provisional`, `needs_revision`, or `blocked` from claim support, scope honesty, artifact completeness, and target/waiver state.
- Input:
  claim ledger, citation ledger, contradiction log, evidence-gap log, metrics, scope metadata.
- Output:
  `release_status`, `blocking_reasons`, `unresolved_gaps`, `waiver_notes`.
- Failure behavior:
  fail closed for unsupported high-risk claims and unsupported high-risk absence claims.
- Required downstream fields:
  `release_status`, `blocking_reasons`, `unresolved_gaps`.
- Genericity note:
  gate conditions are abstract and claim-level; fixture-specific expectations are tested separately.

### 14. `bundle_renderer`

- Role:
  render the final report and audit artifacts as a coherent bundle.
- Input:
  approved draft, metrics, ledgers, logs, domain adapter, release status.
- Output:
  `final_report.md`, `domain-adapter.md`, `metrics.json`, `claim-ledger.tsv`, `citation-ledger.tsv`, `release-gate-summary.md`, plus optional logs.
- Failure behavior:
  missing critical artifacts automatically prevent `complete`.
- Required downstream fields:
  artifact manifest and metadata consistency summary.
- Genericity note:
  renderer formats outputs; it never upgrades release state.

### 15. `regression_runner`

- Role:
  execute fixture-driven checks across genres and known failure modes without contaminating core logic.
- Input:
  fixture definitions, vertical slice harness, gate outputs, adapter outputs.
- Output:
  fixture results, failure diffs, regression summary.
- Failure behavior:
  regression failures do not rewrite core rules automatically; they trigger review.
- Required downstream fields:
  `fixture_name`, `expected_behavior`, `actual_behavior`, `pass_fail`, `notes`.
- Genericity note:
  fixtures are tests, not global prompts or silent gate patches.

## Cross-Cutting Invariants

- No report draft before adapter and source strategy exist.
- No `complete` without claim ledger and citation ledger.
- No high-risk claim can inherit support from corpus-level source ratios.
- No target miss can be ignored without an explicit waiver.
- No scoped search absence can become a mainline fact.

