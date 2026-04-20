# pseudo_pro_v2

`pseudo_pro_v2` is a clean-room design space for a generic pseudo-Pro / pseudo-Deep-Research pipeline.

This directory is intentionally not a topic report.
It contains architecture, policies, schemas, fixture separation, and a hardened synthetic MVP.

## Goals

- keep core logic generic across topics
- make domain adaptation explicit and generated per run
- separate claim capture from claim support
- prevent scoped-search absence claims from turning into facts
- keep fixtures as tests, not as shared prompt behavior
- make `complete` mean "decision-usable within declared scope", not "all files rendered"

## Non-Goals

- generating a topic-specific final report
- encoding named regulations, products, chemicals, or standards into core prompts
- treating regression lessons as global truth instead of test cases

## Key Documents

- [postmortem.md](postmortem.md)
- [architecture.md](architecture.md)
- [reuse-and-discard.md](reuse-and-discard.md)
- [vertical-slice-plan.md](vertical-slice-plan.md)
- [implementation-delta.md](implementation-delta.md)
- [portability-cleanup-report.md](portability-cleanup-report.md)
- [next-implementation-priorities.md](next-implementation-priorities.md)

## Runtime Entry Points

- `scripts/run_vertical_slice.py` runs the multigenre synthetic harness.
- `fixtures/` stores synthetic test inputs only.
- `vertical-slice/generated/` stores regenerated bundle outputs for each implemented genre.
