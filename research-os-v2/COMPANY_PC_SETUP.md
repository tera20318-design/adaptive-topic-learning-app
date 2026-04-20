# research-os-v2 company PC setup

`research-os-v2` is ready to run from a cloned repo on a Windows company PC.

## Recommendation

Use `git clone` if possible.

- Recommended: `git clone`
  - You can pull updates, keep `.claude/commands/dr.md`, `dr.ps1`, fixtures, and docs in sync.
- Fallback: ZIP copy
  - It can run, but updating the workflow later is more manual.

## What is tracked in git

These files should travel with the repo:

- `.claude/commands/dr.md`
- `dr.ps1`
- `research-os-v2/src/`
- `research-os-v2/scripts/`
- `research-os-v2/examples/`
- `research-os-v2/fixtures/`
- `research-os-v2/tests/`
- `research-os-v2/README.md`
- `research-os-v2/COMPANY_PC_SETUP.md`

These stay local and are not meant for commit:

- `runs-v2/`
- `research-os-v2/generated/`
- `research-os-v2/**/__pycache__/`

## Prerequisites

- Git
- Python 3.10 or later
- On Windows, either `py -3`, `python`, or `python3`
- Codex or Claude desktop if you want to use the `/dr` slash command

No third-party Python package is required for the current v2 scaffold, smoke run, or tests.

## First-time setup

Clone the repo:

```powershell
git clone https://github.com/tera20318-design/adaptive-topic-learning-app.git
cd adaptive-topic-learning-app
```

Optional sanity check:

```powershell
git pull
python -m unittest discover -s research-os-v2/tests -p "test_*.py"
```

If `python` is not available, use:

```powershell
py -3 -m unittest discover -s research-os-v2/tests -p "test_*.py"
```

## Starting a new v2 case

Recommended on Windows:

```powershell
.\dr.ps1 v2 "industrial plating overview"
```

If PowerShell blocks local scripts, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\dr.ps1 v2 "industrial plating overview"
```

The wrapper auto-detects `py -3`, `python`, or `python3` and creates:

- `runs-v2\YYYY-MM-DD-<slug>\request.json`
- `runs-v2\YYYY-MM-DD-<slug>\README.md`
- `runs-v2\YYYY-MM-DD-<slug>\notes.md`
- `runs-v2\YYYY-MM-DD-<slug>\bundle\`

`request.json` is prefilled with a starter brief. Review it, then add only real `source_packets`.

## Running from Codex or Claude

Open the repo root as the workspace.

Then you can use:

```text
/dr v2 industrial plating overview
```

The slash command definition lives in `.claude/commands/dr.md`, so keeping the repo root open matters.

## Running the pipeline manually

After editing `request.json`:

```powershell
python research-os-v2/scripts/run_case.py "runs-v2\YYYY-MM-DD-your-theme\request.json"
```

Other useful commands:

```powershell
python research-os-v2/scripts/run_smoke_test.py
python research-os-v2/scripts/run_regression_suite.py
python -m unittest discover -s research-os-v2/tests -p "test_*.py"
```

## Team note

Commit the workflow and docs.
Do not commit ad hoc run outputs under `runs-v2/` unless you intentionally want to share a specific case artifact.
