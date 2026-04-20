# Fixtures

## Purpose

Fixtures are regression tests.
They are not shared prompt behavior and not default domain policy.

## Fixture Schema

Each fixture should provide:

- `request.json`
- `source_packets.json`
- `expected.json`

## Required Genre Buckets

- `technical_overview/`
- `legal_regulatory/`
- `medical_health/`
- `finance/`
- `product_comparison/`
- `business_market/`
- `historical_cultural/`
- `user_document_review/`

## Core Separation Rule

Fixture words stay out of core prompts.
Fixtures exist to verify whether the generic core adapts correctly to many topics without inheriting any one topic's vocabulary.

## Example Fixture Shape

```yaml
request.json:
  topic: "<fixture topic placeholder>"
  reader: "<reader>"
  use_context: "<reader task>"
  desired_depth: "<shape hint>"
  jurisdiction: "<generic jurisdiction>"
  mode: scoped

source_packets.json:
  source_packets:
    - source_id: "SRC-001"
      source_role: official_regulator
      findings:
        - finding_id: "F-001"
          statement: "<claim>"
          claim_kind: regulatory
          risk_level: high

expected.json:
  expected_statuses:
    - blocked
  semantic_guards:
    nouns:
      - "<fixture noun>"
    risk_phrases:
      - "<fixture risk phrase>"
    regulation_wording:
      - "<fixture wording>"
    overclaim_phrasing:
      - "<fixture overclaim>"
```
