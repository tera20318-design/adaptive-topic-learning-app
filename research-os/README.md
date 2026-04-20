# research-os

`research-os` is a reusable pseudo-Pro research scaffold for Codex.
It is designed to produce reader-facing reports that stay auditable, source-backed, and explicit about uncertainty.

## Canonical Prompt

This workspace now keeps only one reusable prompt:

- `prompts/parent_agent_prompt.md`

That file is the single master prompt for the workflow. It includes:

- intake and planning rules
- delegation rules for child agents
- domain-risk discovery
- evidence-gap resolution
- release-blocking quality gates
- final report structure and anti-thin-report rules

## Layout

```text
research-os/
  AGENTS.md
  README.md
  prompts/
    parent_agent_prompt.md
  templates/
    TASK.md
    PLANS.md
    source_candidates.md
    source_log.md
    claim_table.md
    quotes_table.md
    evidence_matrix.md
    gap_analysis.md
    red_team_review.md
    citation_audit.md
    reviewer_notes.md
    outline.md
    draft_v1.md
    draft_v2.md
    final_report.md
  scripts/
    init_research_project.py
    extract_links.py
    build_evidence_matrix.py
```

## Workflow

1. Create a case scaffold with `init_research_project.py`.
2. Use `prompts/parent_agent_prompt.md` as the only reusable prompt.
3. Fill `TASK.md` and `PLANS.md`.
4. Build source logs, claim tables, and the evidence matrix.
5. Draft, red-team, audit, and finalize.

## Notes

- `drafts/final_report.md` is the main product.
- `reviews/reviewer_notes.md` is the release gate record.
- If blockers or unresolved critical gaps remain, the report should not be labeled complete.
