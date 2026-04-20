# Stage Contracts

This document defines the runtime-facing stage contracts for the MVP.
It complements `architecture.md` by making required fields, invariants, and failure codes explicit.
The machine-checkable companion lives in `src/pseudo_pro_v2/stage_contracts.py` and `src/pseudo_pro_v2/validators/stage_contract_validator.py`.

## Common Failure Codes

- `missing_required_input`
- `invalid_schema`
- `empty_output`
- `downstream_contract_violation`
- `clean_room_integrity_violation`
- `unsupported_high_risk_claim`
- `required_table_missing`
- `metadata_inconsistent`
- `target_miss_without_waiver`

## Snapshot Format

Each stage may be snapshotted as UTF-8 JSON with:

- `stage_name`
- `inputs_summary`
- `outputs_summary`
- `failure_codes`
- `invariants_checked`

The MVP does not persist every snapshot yet, but downstream validators assume this shape.
The machine-checkable required keys are also declared in `STAGE_SNAPSHOT_REQUIRED_FIELDS`.

## Stage Contracts

### `intent_classifier`

- role: classify reader-facing output intent
- required inputs: `RunRequest.topic`, `RunRequest.use_context`, `RunRequest.desired_depth`
- outputs: `IntentResult`
- invariants:
  - `intent_label` is non-empty
  - `report_shape_hints` is non-empty
- downstream required outputs:
  - `intent_label`
  - `decision_focus`
  - `reader_task`
- failure behavior:
  - `missing_required_input`
  - `empty_output`

### `risk_tier_classifier`

- role: determine run-level risk tier
- required inputs: `RunRequest`, `IntentResult.intent_label`
- outputs: `RiskTierResult`
- invariants:
  - `risk_tier in {low, medium, high}`
  - `rationale` is non-empty
- downstream required outputs:
  - `risk_tier`
  - `high_stakes_domains`
- failure behavior:
  - `missing_required_input`
  - `downstream_contract_violation`

### `scope_budget_planner`

- role: produce scope, target profile, and disclosure metadata
- required inputs: `RunRequest.mode`, `RunRequest.target_profile`, `RiskTierResult.risk_tier`
- outputs: `BudgetPlan`
- invariants:
  - `requested_mode` and `effective_mode` are non-empty
  - `full_dr_equivalent` is boolean
  - `target_profile` exists
- downstream required outputs:
  - `requested_mode`
  - `effective_mode`
  - `full_dr_equivalent`
  - `limitations`
  - `target_profile`
- failure behavior:
  - `missing_required_input`
  - `invalid_schema`

### `domain_adapter_generator`

- role: generate a run-specific domain adapter without fixture defaults
- required inputs:
  - `RunRequest.topic`
  - `RunRequest.reader`
  - `RunRequest.use_context`
  - `IntentResult.intent_label`
  - `RiskTierResult.risk_tier`
  - `BudgetPlan.limitations`
- outputs: `DomainAdapter`
- invariants:
  - all schema-required fields present
  - `source_roles_required_by_claim_kind` covers all core claim kinds used downstream
  - `domain_specific_risks` is non-empty
- downstream required outputs:
  - `output_type`
  - `risk_tier`
  - `required_tables`
  - `required_decision_layer`
  - `source_roles_required_by_claim_kind`
- failure behavior:
  - `invalid_schema`
  - `empty_output`
  - `clean_room_integrity_violation`

### `source_strategy_builder`

- role: derive claim-kind-aware source-role requirements
- required inputs: `DomainAdapter.source_priority`, `DomainAdapter.source_roles_required_by_claim_kind`
- outputs: `SourceStrategy`
- invariants:
  - every emitted claim-kind mapping has at least one source role
- downstream required outputs:
  - `required_source_roles_by_claim_kind`
  - `compatibility_notes`
- failure behavior:
  - `missing_required_input`
  - `downstream_contract_violation`

### `evidence_collector`

- role: normalize source packets into collected evidence
- required inputs: `RunRequest.source_packets`
- outputs: `CollectedEvidence`
- invariants:
  - every source has `source_id`, `source_role`, `title`
  - every finding has `finding_id`, `statement`, `claim_kind`, `risk_level`
- downstream required outputs:
  - `sources`
  - `findings`
  - `source_counts_by_role`
- failure behavior:
  - `missing_required_input`
  - `invalid_schema`
  - `empty_output`

### `report_planner`

- role: create reader-facing section plan from adapter requirements
- required inputs: `DomainAdapter.required_tables`, `DomainAdapter.required_decision_layer`, `DomainAdapter.risk_tier`
- outputs: list of `ReportSectionPlan`
- invariants:
  - required reader-facing sections are present
  - no internal headings appear in the plan
- downstream required outputs:
  - section keys
  - titles
  - target claim counts
  - adapter prompts
- failure behavior:
  - `missing_required_input`
  - `downstream_contract_violation`

### `draft_writer`

- role: write reader-facing draft units from section plan and evidence
- required inputs:
  - `RunRequest`
  - `DomainAdapter`
  - `CollectedEvidence`
  - `ReportSectionPlan[]`
  - `BudgetPlan`
- outputs: `ReportDraft`
- invariants:
  - section titles remain reader-facing
  - every claim unit preserves `origin_finding_id`
  - unsupported material is not silently dropped before ledgering
- downstream required outputs:
  - `sections`
  - `units`
  - `title`
- failure behavior:
  - `missing_required_input`
  - `empty_output`
  - `downstream_contract_violation`

### `claim_extractor`

- role: convert claim units into ledger rows
- required inputs: `ReportDraft.units`, `SourceStrategy.required_source_roles_by_claim_kind`
- outputs: `ClaimLedgerRow[]`
- invariants:
  - every claim unit becomes exactly one claim row
  - `included_in_report` is preserved
  - `origin_finding_id` is preserved
- downstream required outputs:
  - `claim_id`
  - `claim_kind`
  - `risk_level`
  - `support_status`
- failure behavior:
  - `empty_output`
  - `downstream_contract_violation`

### `evidence_mapper`

- role: map claim rows to source-role-aware support judgments
- required inputs:
  - `ClaimLedgerRow[]`
  - `CollectedEvidence`
  - `SourceStrategy.required_source_roles_by_claim_kind`
- outputs:
  - updated `ClaimLedgerRow[]`
  - `CitationLedgerRow[]`
- invariants:
  - high-risk support requires claim-kind-appropriate role match
  - every cited source exists in collected evidence
  - excluded claims remain in the ledger
- downstream required outputs:
  - `required_role_matched`
  - `role_fit_status`
  - `support_status`
  - citation rows
- failure behavior:
  - `missing_required_input`
  - `metadata_inconsistent`
  - `unsupported_high_risk_claim`

### `contradiction_absence_guard`

- role: suppress unsafe mainline claims while preserving them in audit artifacts
- required inputs: `ClaimLedgerRow[]`, `ReportDraft`, `RunRequest`
- outputs:
  - updated `ClaimLedgerRow[]`
  - updated `ReportDraft`
  - `ContradictionEntry[]`
  - `EvidenceGapEntry[]`
- invariants:
  - high-risk scoped absence is not left in mainline prose
  - excluded claims still remain in the ledger
  - scope mismatch downgrades support appropriately
- downstream required outputs:
  - `included_in_report`
  - `exclusion_reason`
  - contradiction log
  - evidence gap log
- failure behavior:
  - `unsupported_high_risk_claim`
  - `downstream_contract_violation`

### `tone_controller`

- role: adjust assertion strength based on support and claim type
- required inputs: `ReportDraft`, `ClaimLedgerRow[]`
- outputs: updated `ReportDraft`
- invariants:
  - excluded claims stay excluded
  - every tone mode is explicit and known
- downstream required outputs:
  - toned `ReportUnit.text`
- failure behavior:
  - `downstream_contract_violation`

### `release_gate`

- role: decide `complete`, `provisional`, `needs_revision`, or `blocked`
- required inputs:
  - `ReportDraft`
  - `ClaimLedgerRow[]`
  - `CitationLedgerRow[]`
  - contradictions and gaps
  - `BudgetPlan`
  - `DomainAdapter`
  - metrics
  - validation errors
- outputs: `ReleaseGateDecision`
- invariants:
  - blocking claim failures override aggregate metrics
  - rubric failures cannot become `complete`
  - clean-room integrity failure blocks release
- downstream required outputs:
  - `status`
  - `reasons`
  - `blocking_reasons`
- failure behavior:
  - `unsupported_high_risk_claim`
  - `metadata_inconsistent`
  - `target_miss_without_waiver`
  - `required_table_missing`
  - `clean_room_integrity_violation`

### `bundle_renderer`

- role: render reader-facing report plus audit artifacts
- required inputs: `PipelineBundle`
- outputs:
  - `final_report.md`
  - `domain-adapter.md`
  - `metrics.json`
  - `claim-ledger.tsv`
  - `citation-ledger.tsv`
  - `release-gate-summary.md`
- invariants:
  - included and excluded claims are rendered consistently into ledgers
  - release summary reflects actual gate status
  - report headings remain reader-facing
- failure behavior:
  - `downstream_contract_violation`
  - `metadata_inconsistent`
