# Implementation Delta

## What Changed In This Pass

- Replaced the last Windows absolute links in repo docs with repo-relative references or plain code paths.
- Added a decision-usable rubric and wired it into the release gate as a semi-checkable requirement.
- Hardened required-table checks so they inspect populated draft units instead of section titles alone.
- Expanded synthetic fixtures from 2 genres to 5 genres:
  - `technical_overview`
  - `legal_regulatory`
  - `medical_health`
  - `finance`
  - `product_comparison`
- Added semantic clean-room leakage validation based on fixture-provided guard phrases.
- Shifted the vertical-slice harness to read from `fixtures/` so the same inputs drive both regression tests and generated bundles.

## What Was Hardened

- `release_gate` now treats decision-usable rubric failures as revision-level failures.
- `release_gate` now blocks clean-room integrity violations rather than treating them as advisory only.
- `release_gate` now blocks citation trace mismatch and carries a user-document grounding check.
- Required table checks now fail when a section is present only as a heading or placeholder.
- Multigenre fixtures now include:
  - mixed source roles
  - high-risk claims
  - scoped absence traps
  - overgeneralization traps
  - comparison weakness
  - waiver/target pressure through target profiles
  - contradiction pressure and outdated source notes

## What Remains Synthetic

- Evidence collection is still packet-based and does not do live retrieval.
- Domain adaptation is still heuristic and request-driven, not retrieval-driven.
- Claim extraction is still unit-based rather than free-span extraction from arbitrary prose.
- Contradiction handling still lacks adversarial search and deep conflict mining.
- Clean-room leakage checks are phrase-based semantic guards, not embedding-based similarity checks.
