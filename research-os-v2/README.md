# research-os-v2

`research-os-v2` is a clean-room redesign of the local pseudo-Pro research pipeline.

It is intentionally stdlib-only today, so a Windows machine with Git plus Python 3.10+ is enough to run it.

Its goal is not to accumulate more intermediate artifacts.
Its goal is to reliably produce a reader-facing final report that is:

- directly responsive to the question
- decision-useful
- explicit about scope and uncertainty
- traceable back to source evidence
- honest about what was and was not validated

## Design Principles

- Report-first: the final report is the primary product.
- Clean separation: regression fixtures and domain-specific failures stay outside the core rules.
- Honest metrics: claim capture and evidence support are tracked separately.
- Scoped honesty: scoped runs are never mislabeled as full Deep Research equivalents.
- High-stakes caution: unsupported high-risk claims block release.

## Layout

```text
research-os-v2/
  ARCHITECTURE.md
  README.md
  V1_DIFF.md
  examples/
  fixtures/
  generated/
  scripts/
  src/
    research_os_v2/
      ...
  tests/
```

## Quick Start

Recommended on Windows or a company PC:

```powershell
.\dr.ps1 v2 "your theme"
```

The PowerShell wrapper auto-detects `py -3`, `python`, or `python3` and scaffolds a starter `request.json`.

Generate the smoke-test bundle:

```powershell
python research-os-v2/scripts/run_smoke_test.py
```

Bootstrap a new v2 case:

```powershell
python research-os-v2/scripts/init_case.py "your theme"
```

Run a case from `request.json`:

```powershell
python research-os-v2/scripts/run_case.py "runs-v2\\YYYY-MM-DD-your-theme\\request.json"
```

Run the regression suite:

```powershell
python research-os-v2/scripts/run_regression_suite.py
```

Run unit tests:

```powershell
python -m unittest discover -s research-os-v2/tests -p "test_*.py"
```

For a Japanese step-by-step setup guide, see [COMPANY_PC_SETUP.md](COMPANY_PC_SETUP.md).
