# Source Role And Claim Kind Schema

## Source Roles

The core source roles are:

- `official_regulator`
- `legal_text`
- `court_or_authoritative_interpretation`
- `standards_body`
- `standard_or_code`
- `academic_review`
- `academic_paper`
- `professional_body`
- `industry_association`
- `vendor_first_party`
- `government_context`
- `trade_media`
- `secondary_media`
- `user_provided_source`
- `unknown`

## Claim Kinds

The core claim kinds are:

- `definition`
- `fact`
- `mechanism`
- `temporal`
- `numeric`
- `regulatory`
- `legal`
- `medical`
- `financial`
- `market`
- `recommendation`
- `inference`
- `advice`
- `absence`
- `comparison`
- `scope_boundary`

## Role Semantics

### Source-role notes

- `official_regulator`:
  preferred for current rules, official guidance, and regulator-framed obligations
- `legal_text`:
  preferred for binding legal language
- `court_or_authoritative_interpretation`:
  preferred when legal meaning depends on interpretation, not just text
- `standards_body` and `standard_or_code`:
  preferred for specification or test-method claims
- `academic_review`:
  preferred for synthesizing evidence and explaining consensus
- `academic_paper`:
  useful for mechanism or new evidence, but scope should stay study-bounded
- `professional_body`:
  useful for field practice, applied guidance, and nonbinding standards of care
- `industry_association`:
  acceptable for overviews and market context, but neutrality caveat often required
- `vendor_first_party`:
  acceptable for implementation examples and product-specific details, not for universal claims without caveat
- `government_context`:
  useful for official explanations, definitions, and descriptive context
- `trade_media` and `secondary_media`:
  useful for discovery and triangulation, not primary support for high-risk claims
- `user_provided_source`:
  may define local scope, but does not by itself establish external fact
- `unknown`:
  discovery-only until role is clarified

### Claim-kind notes

- `regulatory`, `legal`, `medical`, `financial`, and often `absence` are high-risk
- `scope_boundary` is still auditable and cannot be auto-supported by convenience
- `inference` must be labeled as report inference
- `advice` must identify decision conditions and verification path

## Compatibility Matrix

| claim_kind | required / preferred source roles | cautions |
| --- | --- | --- |
| `definition` | `standards_body`, `academic_review`, `government_context` | avoid product-specific definitions unless explicitly scoped |
| `fact` | `government_context`, `professional_body`, `academic_review`, `standards_body` | weak when based only on media or vendor materials |
| `mechanism` | `academic_review`, `academic_paper`, `professional_body`, `standards_body` | vendor examples may illustrate but not generalize |
| `temporal` | `official_regulator`, `legal_text`, `government_context` | date-sensitive claims need date-matched sources |
| `numeric` | `official_regulator`, `academic_paper`, `government_context`, `standard_or_code` | numbers should remain scope-bounded and dated |
| `regulatory` | `official_regulator`, `legal_text`, `court_or_authoritative_interpretation` | secondary summaries are insufficient for support |
| `legal` | `legal_text`, `court_or_authoritative_interpretation`, `official_regulator` | do not infer binding meaning from media summaries |
| `medical` | `academic_review`, `academic_paper`, `professional_body`, `official_regulator` | mechanism-only papers do not by themselves justify advice |
| `financial` | `official_regulator`, `government_context`, `academic_review` | vendor brochures cannot support broad financial claims |
| `market` | `government_context`, `industry_association`, `academic_review`, `secondary_media` | market context is not a substitute for recommendation support |
| `recommendation` | `official_regulator`, `academic_review`, `professional_body`, `government_context` | must remain conditional and decision-linked |
| `inference` | `government_context`, `academic_review`, `standards_body` | mark explicitly as inference, not fact |
| `advice` | `official_regulator`, `professional_body`, `standards_body`, `government_context` | include what to verify before acting |
| `absence` | `official_regulator`, `legal_text`, `court_or_authoritative_interpretation` | scoped-search absence is never enough for high-risk claims |
| `comparison` | `standards_body`, `academic_review`, `government_context`, `professional_body` | vendor and association inputs need neutrality caveats |
| `scope_boundary` | `official_regulator`, `government_context`, `legal_text`, `user_provided_source` | boundary claims still need explicit basis and scope |

## Non-Generalization Rules

- `vendor_first_party` can support implementation examples, but any generalization needs caveat and stronger corroboration.
- `industry_association` can support overview framing, but high-risk or adversarial claims require more neutral roles.
- `trade_media` and `secondary_media` are discovery aids, not high-risk anchors.
- corpus-level source richness never overrides claim-level role mismatch.

