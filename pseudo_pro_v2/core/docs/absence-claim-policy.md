# Absence Claim Policy

## Purpose

Absence claims are not ordinary facts.
They need typed handling because "not found" can describe a search result without describing reality.

## Supported Absence Types

- `not_found_in_scoped_search`
- `not_found_in_official_source_checked`
- `explicitly_not_applicable`
- `explicitly_repealed`
- `replaced_by_later_rule`
- `different_subject_matter`
- `contradicted_by_source`

## Core Rules

1. `not_found_in_scoped_search` is never promoted to a fact.
2. High-risk absence claims require adversarial search before they can appear in mainline prose.
3. Legal, regulatory, medical, financial, and safety absence claims require authoritative support before they are stated substantively.
4. If an absence claim appears in the report, it must declare both scope and limitation.
5. A later source about a different subject must not negate an earlier or parallel rule unless explicit source support establishes the link.
6. Unsupported high-risk absence claims block `complete`.

## Required Handling By Severity

### Low / Medium Risk

- keep scoped
- prefer uncertainty section if reader impact is limited
- assign `weak` unless authoritative confirmation exists

### High Risk

- require authoritative source role match
- require adversarial search log
- block release if support remains `weak`, `missing`, or `out_of_scope`

## Suggested Output Language

- Scoped search result:
  "Within the checked scope, this was not found."
- Authoritatively confirmed non-applicability:
  "Based on the checked authoritative source, this appears not to apply in the stated scope."
- Never use:
  "There is no rule" or "This does not exist" unless authoritative support explicitly justifies it.

## Release Implications

- `not_found_in_scoped_search` in a high-risk area with no authoritative support:
  `blocked`
- unsupported `explicitly_repealed`:
  `blocked`
- unsupported `different_subject_matter` used to dismiss a claim:
  `needs_revision` or `blocked` depending on risk

