# Scope Budget Policy

## Required Metadata

Every run must expose:

- `requested_mode`
- `effective_mode`
- `preset_baseline_budget`
- `effective_budget`
- `override_reason`
- `override_authority`
- `full_dr_equivalent`
- `report_status_implication`
- `limitations`

## Mode Semantics

### `full`

- aims to satisfy the highest configured baseline
- may be labeled full-equivalent only if the baseline and gate both pass

### `scoped`

- narrower than full
- may still be `complete`, but only as scoped complete
- must never imply full-equivalent coverage

## Output Rule

If `full_dr_equivalent` is `false`, both summary and metadata must say so explicitly.

## Target And Waiver Rules

1. Targets are not advisory if marked required by policy, adapter, or preset.
2. A target miss cannot still become `complete` without an explicit waiver.
3. The waiver must record:
   - which target missed
   - why the miss is accepted
   - who or what authorized the waiver
   - what report limitation text must be added
4. Waiver-free target misses degrade the run to `needs_revision` or `blocked`.

## Why This Exists

Budget honesty is part of report honesty.
A scoped run may be useful and even complete within its own declared frame, but it must not borrow credibility from a fuller baseline it did not actually meet.

