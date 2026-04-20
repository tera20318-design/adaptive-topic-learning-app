# Decision-Usable Rubric

This rubric operationalizes "decision-usable" for the release gate.
It is intentionally semi-checkable rather than purely stylistic.

## Required Checks

The report fails the rubric if any of the following are false:

- direct answer present
- scope and exclusions present
- uncertainty section present
- reader decision layer present
- at least one checklist or decision table entry present
- at least one next action or next research cue present
- no internal pipeline headings are used
- no unsupported high-risk claim remains in mainline prose

## Additional Genre-Sensitive Checks

The report also fails when any applicable genre-sensitive check fails:

- comparison output requires a populated options/comparison structure
- comparison output requires explicit tradeoff language, not just two option labels
- high-risk recommendation or advice requires visible risk disclosure
- finance recommendation output requires risk/limitation disclosure
- medical advice output cannot rely on non-matching source roles
- checklist items must align with the reader task
- next action must be specific enough to guide a user
- decision layer must not collapse into generic filler

## Machine-Checkable Signals

Current MVP checks the following signals:

- `direct_answer_present`
- `scope_exclusions_present`
- `uncertainty_present`
- `reader_decision_layer_present`
- `checklist_or_decision_table_present`
- `next_action_or_next_research_present`
- `no_internal_headings`
- `no_unsupported_high_risk_in_mainline`
- `comparison_tradeoff_ready`
- `risk_disclosure_present`
- `checklist_aligned_with_reader_task`
- `specific_next_action_present`
- `decision_layer_not_generic_filler`

## Failure Mapping

- rubric failure with no blocking claim failure -> `needs_revision`
- rubric failure plus unsupported high-risk claim -> `blocked`
- rubric pass does not override claim-level blocking conditions

## Explicit Non-Rules

- citation count alone is not decision usability
- artifact count alone is not decision usability
- readable prose alone is not decision usability
- a scoped run may still fail decision usability even if all required files exist
