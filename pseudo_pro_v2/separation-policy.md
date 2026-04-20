# Separation Policy

## Purpose

`pseudo_pro_v2` must keep core logic generic.
Regression knowledge is useful, but only when it stays in fixtures and tests instead of leaking into shared runtime behavior.

## Core May Contain

- abstract rules
- schemas
- `source_role`
- `claim_kind`
- release-gate logic
- metadata consistency rules
- negative-evidence and absence handling
- report-first principles
- scope and budget honesty rules
- tone-control rules keyed by support quality and source role

## Core May Not Contain

- specific technologies
- specific products
- specific chemical substances
- specific standard numbers
- specific country-regime names as permanent defaults
- wording copied from historical failures
- must-cover angles learned from one regression topic
- special-case gate exceptions created to rescue one topic class

## Fixtures Must Contain

- topic-specific risks
- known failure modes
- prohibited overclaims for that topic
- authoritative-source traps
- absence-claim traps
- expected gate behavior for that topic class

## Adapter Boundary

- `core/` defines how a domain adapter should be generated.
- `adapters/generated/` stores the per-run adapter output.
- generated adapters may contain topic-shaped risks and boundaries for one run.
- generated adapters must never be imported back into `core/` as defaults.

## Report Boundary

- reports are run artifacts, not design assets
- a rendered report never becomes a core template
- a strong report does not prove a strong architecture

## Migration Rule

When reusing from an older pipeline:

- migrate only abstractions, schemas, and contracts
- do not migrate topic-shaped prompt fragments, source packets, or failure vocabulary

## Enforcement Ideas

- add a fixture-isolation test that rejects fixture strings in core prompt files
- add schema checks that keep fixture fields out of core contracts
- require code review for any change that adds named domain nouns to `core/`

