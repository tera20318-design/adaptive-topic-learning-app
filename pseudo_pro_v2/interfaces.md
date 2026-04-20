# Interfaces

## Stage Contracts

| Stage | Inputs | Outputs | Failure Behavior |
| --- | --- | --- | --- |
| `intent_classifier` | `RunRequest` | `IntentResult` | Falls back to generic `report` intent if no strong cue is present. |
| `risk_tier_classifier` | `RunRequest`, `IntentResult` | `RiskTierResult` | Falls back to `medium` or `low` based on generic heuristics; does not guess domain-specific risk lists. |
| `scope_budget_planner` | `RunRequest`, `IntentResult`, `RiskTierResult` | `BudgetPlan` | Defaults unknown mode to `scoped`; preserves target profile and waiver inputs. |
| `domain_adapter_generator` | `RunRequest`, `IntentResult`, `RiskTierResult`, `BudgetPlan` | `DomainAdapter` | Generates only generic abstract fields; validation errors are surfaced downstream. |
| `source_strategy_builder` | `IntentResult`, `RiskTierResult`, `DomainAdapter` | `SourceStrategy` | Falls back to schema-defined source-role requirements by `claim_kind`. |
| `evidence_collector` | `RunRequest` | `CollectedEvidence` | Loads synthetic packets as-is; missing source role metadata is normalized to packet defaults. |
| `report_planner` | `DomainAdapter` | `list[ReportSectionPlan]` | Uses fixed reader-facing section plan if no narrower shape is available. |
| `draft_writer` | `RunRequest`, `DomainAdapter`, `CollectedEvidence`, `list[ReportSectionPlan]`, `BudgetPlan` | `ReportDraft` | Produces a report-first draft even with sparse evidence; unsupported material is handled later by guards. |
| `claim_extractor` | `ReportDraft`, `SourceStrategy` | `list[ClaimLedgerRow]` | Captures every claim unit; does not infer support on its own. |
| `evidence_mapper` | `list[ClaimLedgerRow]`, `CollectedEvidence`, `SourceStrategy` | `list[ClaimLedgerRow]`, `list[CitationLedgerRow]` | Downgrades support when roles are weak, missing, or mismatched. |
| `contradiction_absence_guard` | `list[ClaimLedgerRow]`, `ReportDraft`, `RunRequest` | guarded claims, guarded draft, contradictions, evidence gaps | Removes unsupported high-risk absence claims from mainline prose and marks scope mismatches `out_of_scope`. |
| `tone_controller` | `ReportDraft`, `list[ClaimLedgerRow]` | `ReportDraft` | Softens or marks text when support is weak, inferred, or unverified. |
| `release_gate` | draft, claims, citations, contradictions, gaps, budget, adapter, metrics, validation errors | `ReleaseGateDecision` | Returns `blocked`, `needs_revision`, `provisional`, or `complete`; never upgrades unsupported high-risk claims. |
| `bundle_renderer` | `PipelineBundle`, output path | files on disk | Writes required artifacts only; does not mutate gate decisions. |

## Required Downstream Fields

| From Stage | Required Downstream Fields |
| --- | --- |
| `intent_classifier` | `intent_label`, `decision_focus`, `reader_task` |
| `risk_tier_classifier` | `risk_tier`, `high_stakes_domains`, `rationale` |
| `scope_budget_planner` | `requested_mode`, `effective_mode`, `target_profile`, `waivers`, `full_dr_equivalent`, `limitations` |
| `domain_adapter_generator` | `risk_tier`, `source_priority`, `required_tables`, `known_limits`, `source_roles_required_by_claim_kind` |
| `source_strategy_builder` | `required_source_roles_by_claim_kind`, `compatibility_notes` |
| `evidence_collector` | `sources`, `findings`, `source_counts_by_role` |
| `report_planner` | `section.key`, `section.title` |
| `draft_writer` | `unit_id`, `section_key`, `section_title`, `text`, `claim_kind`, `risk_level`, `source_ids`, `include_in_report` |
| `claim_extractor` | `claim_id`, `exact_text_span`, `normalized_claim`, `claim_kind`, `risk_level`, `support_status` |
| `evidence_mapper` | `source_roles`, `evidence_count`, `required_source_role`, `support_status`, `suggested_tone`, `required_fix` |
| `contradiction_absence_guard` | `included_in_report`, `support_status`, contradiction log, evidence gap log |
| `tone_controller` | updated reader-facing prose text |
| `release_gate` | `status`, `reasons`, `blocking_reasons`, `unresolved_gaps` |
| `bundle_renderer` | emitted artifact set and serialized ledgers |

## Validation Boundary

- `domain_adapter_validator` runs before gate evaluation.
- ledger validators check typed rows before rendering.
- `gate_input_validator` checks that metrics, claims, and citations stay aligned.
- `metrics_validator` ensures that capture/support ratios remain numeric and bounded.

## Current Non-Goals

- No live retrieval.
- No domain-specific prompt branches in core.
- No attempt to infer real-world topic facts.
