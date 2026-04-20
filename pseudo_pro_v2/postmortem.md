# Postmortem

## Summary

The prior response failed as pipeline architecture work, not merely as report work.
The work drifted into topic execution because the workflow optimized for visible output artifacts instead of enforcing a design-first phase boundary.
A stronger topic report is not proof of a stronger generic pipeline.

## Why It Became a Theme Re-Run

- There was no hard stop between "design the generic system" and "execute a sample topic."
- The existing codebase already centered report production, so the easiest path was to improve a report rather than redesign the architecture.
- Success was measured by produced artifacts instead of by clean separation among core rules, domain adaptation, fixture testing, and gate logic.

## Why Generic v2 Design Did Not Start First

- Core schemas, module contracts, and release semantics were not made mandatory before execution.
- The design effort lacked a clean-room target directory and therefore defaulted to extending execution behavior around an existing production-like flow.
- The work treated a concrete run as a proxy for architecture validation instead of building generic contracts first and validating them later with fixtures.

## Where Core and Regression Fixture Logic Mixed

- Domain-specific failure stories were allowed to influence shared behavior too early.
- Topic-shaped source preferences and failure angles leaked into design reasoning instead of being isolated as fixture expectations.
- The pipeline implicitly learned "what mattered last time" rather than expressing only abstract rules such as claim typing, source-role matching, scoped honesty, and absence handling.

## Why Release Gate Allowed Major False Negatives

- Gate logic was more artifact-centered than claim-centered.
- The presence of ledgers and aggregate metrics could mask unsupported or weakly supported high-risk claims.
- The gate did not treat all target misses as blocking unless explicitly waived.
- Contradiction handling was shallow and did not assume that missing disconfirming evidence is itself a release risk in high-stakes contexts.

## Why Primary-Source Ratio Misses Could Still Pass

- Ratio-style metrics were treated as corpus diagnostics rather than claim-level adequacy checks.
- A run could improve global source mix while leaving the most important claims supported only indirectly.
- No explicit waiver requirement prevented `complete` from surviving a target miss.
- Claim-level source-role satisfaction was not the dominant release control.

## Why Absence Claims Were Dangerous

- "Not found" was allowed to behave too much like "not true."
- Scoped retrieval results can only justify scoped statements, not universal factual conclusions.
- High-risk domains need authoritative support and often adversarial search before absence can appear in mainline prose.
- Later sources about a different subject can create false negation if subject-matter matching is not enforced.

## Abstract Rules That Belong in Core

- Keep fact, inference, advice, and absence as distinct claim classes.
- Require claim-level source-role compatibility, especially for high-risk claims.
- Keep scoped/full labeling honest and explicit in metrics and report metadata.
- Treat absence as typed, scoped, and potentially blocking.
- Make release decisions depend on high-risk support quality, not artifact count.
- Use tone control to reflect support quality and source role.
- Require explicit waivers for target misses before `complete`.

## Concrete Concerns That Belong in Fixtures

- Named regulations, standards, jurisdictions, substances, products, and technology families.
- Topic-specific must-cover angles and known failure stories.
- Regression examples that came from one historical run.
- Special-case prompt fragments created to rescue one topic class.
- Domain-specific risk inventories copied from earlier cases.

## What Changes in v2

1. Define core schemas and policies before any topic execution.
2. Generate a domain adapter per topic instead of copying remembered domain logic into core.
3. Keep fixtures as tests that exercise the generic core.
4. Make release gate claim-centered, waiver-aware, and explicit about scope.
5. Treat report generation as downstream of evidence semantics, not as a substitute for architecture.

