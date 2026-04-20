# Tests

## Test Categories

- contract tests:
  validate schema shape and required fields
- gate tests:
  validate `complete`, `provisional`, `needs_revision`, and `blocked` behavior
- absence tests:
  verify scoped-search absence cannot become supported fact
- scope tests:
  verify scoped runs are never mislabeled full-equivalent
- fixture regression tests:
  verify genre-specific traps stay outside core while still being caught by the generic architecture

## First Acceptance Cases

- unsupported high-risk claim blocks `complete`
- missing claim ledger blocks release
- citation ledger missing or inconsistent blocks release
- waiver-free target miss cannot become `complete`
- internal headings do not appear in the report

