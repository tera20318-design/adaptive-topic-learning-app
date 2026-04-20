argument-hint: [v2] [research theme]
description: Kick off a research case for research-os v1 or pseudo-Pro v2
---

If `$ARGUMENTS` starts with `v2 `, use the pseudo-Pro v2 workflow in @research-os-v2/README.md and @research-os-v2/ARCHITECTURE.md.
Otherwise, use the existing research workflow in @research-os/AGENTS.md, @research-os/prompts/parent_agent_prompt.md, and @research-os/README.md.

If `$ARGUMENTS` is empty, ask the user for the research theme and stop.

## v2 Mode

When `$ARGUMENTS` starts with `v2 `:

- Treat the remainder after the `v2` prefix as the working theme.
- If the remainder is empty, ask the user for the theme and stop.
- Your job is to bootstrap a new pseudo-Pro v2 case, not to answer the research question yet.

Required steps for v2:

1. Create a new case directory under `runs-v2/` using today's date and a safe slug.
2. From the repo root, run `.\dr.ps1 v2 "<theme>"` so the wrapper can pick `py -3`, `python`, or `python3` automatically.
   - If the PowerShell wrapper is unavailable, run `python research-os-v2/scripts/init_case.py "<theme>" --base-dir "runs-v2"` or `py -3 research-os-v2/scripts/init_case.py "<theme>" --base-dir "runs-v2"`.
3. Confirm that the new case contains:
   - `request.json`
   - `README.md`
   - `notes.md`
   - `bundle/`
4. Confirm that `request.json` already has a concrete starter brief, then adjust it if needed:
   - `topic`
   - `reader`
   - `use_context`
   - `output_type`
   - `requested_mode`
   - `question`
   - `jurisdiction` if needed
   - `as_of_date`
5. Do not invent or prefill `source_packets` with fake evidence.
6. Stop after the v2 case is scaffolded and the starter `request.json` is ready.

Guardrails for v2:

- Do not fabricate sources or findings.
- Do not run the full pipeline unless the user explicitly asks you to.
- Keep the scaffold honest about scoped versus full runs.
- Treat `request.json` as the canonical input contract for v2.

Return format for v2:

- Created case path
- Request file path
- Working title
- Suggested next step

## v1 Mode

Otherwise, treat `$ARGUMENTS` as the working theme for a new research-os case.

Your job is to start a new research-os case in the canonical pseudo-Pro mode, not to answer the research question yet.

Required steps:

1. Create a new case directory under `runs/` using today's date and a safe slug.
2. Run `python research-os/scripts/init_research_project.py <case-dir> --title "<theme>"` to scaffold the case.
3. Fill the new `TASK.md` with:
   - the working title
   - the primary question
   - the decision this research should support
   - topic classification
   - audience
   - scope and non-scope
   - constraints
   - success criteria
   - must-cover topics and risk lenses
4. Fill the new `PLANS.md` with:
   - current phase
   - milestones
   - workstreams
   - an initial delegated work queue
   - immediate next steps
5. Do not draft `final_report.md`.
6. Stop after the case is scaffolded and the initial planning artifacts are ready.

Guardrails:

- Do not jump into final prose.
- Do not invent citations or reviewed sources.
- Do not fill `source_log.md` with placeholder evidence.
- Keep the initial plan concrete and auditable.
- Treat `prompts/parent_agent_prompt.md` as the only reusable prompt for this case.

Return format:

- Created case path
- Working title
- Primary question
- Suggested work split
- Immediate next step
