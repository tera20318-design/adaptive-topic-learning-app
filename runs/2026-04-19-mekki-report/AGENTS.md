# Research OS Agent Rules

This directory defines a reusable research workflow that approximates a coordinated "Pro extend" process using one parent agent and one or more child agents.

## Mission

Turn an open-ended request into a traceable, source-backed report with atomic claims, explicit uncertainty, and a durable paper trail.

## Core Rules

1. Never present an unsupported claim as fact.
2. Keep planning, source review, claim extraction, synthesis, and challenge as separate steps.
3. Every meaningful claim must be traceable to at least one logged source.
4. Distinguish observed facts, interpretations, estimates, and recommendations.
5. Prefer primary sources first, then strong secondary sources.
6. Record uncertainty early; do not hide gaps until the end.
7. Update shared artifacts continuously so another worker can resume without guesswork.
8. Preserve prior work unless it is clearly wrong; correct with notes instead of silent deletion.

## Required Project Artifacts

For each research case, create or update these files:

- `TASK.md`
- `PLANS.md`
- `sources/source_candidates.md`
- `sources/source_log.md`
- `extracts/claim_table.md`
- `extracts/quotes_table.md`
- `extracts/evidence_matrix.md`
- `reviews/gap_analysis.md`
- `reviews/red_team_review.md`
- `reviews/citation_audit.md`
- `drafts/outline.md`
- `drafts/draft_v1.md`
- `drafts/draft_v2.md`
- `drafts/final_report.md`

## Workflow Order

1. Intake
   - Create or update `TASK.md`.
   - Clarify goal, audience, decision to support, scope boundaries, and deadline.
2. Plan
   - Create or update `PLANS.md`.
   - Break work into workstreams with owners, dependencies, and exit criteria.
3. Discover
   - Populate `sources/source_candidates.md` before deep reading.
   - Rank by likely value, freshness, and credibility.
4. Review
   - Log every inspected source in `sources/source_log.md`.
   - Capture publication date, author or organization, source type, and notes.
5. Extract
   - Convert source findings into atomic claims in `extracts/claim_table.md`.
   - Save verbatim snippets only when wording matters in `extracts/quotes_table.md`.
   - Map claims into `extracts/evidence_matrix.md`.
6. Diagnose
   - Record what is still missing in `reviews/gap_analysis.md`.
   - Decide whether more search, more validation, or narrower scope is required.
7. Challenge
   - Run an internal adversarial pass in `reviews/red_team_review.md`.
   - Audit citation coverage in `reviews/citation_audit.md`.
8. Synthesize
   - Draft structure in `drafts/outline.md`.
   - Draft the narrative in `drafts/draft_v1.md`, revise in `drafts/draft_v2.md`.
9. Deliver
   - Produce `drafts/final_report.md` only after quality gates pass.

## Parent Agent Rules

The parent agent owns orchestration and quality control.

- Maintain the latest version of `TASK.md` and `PLANS.md`.
- Split work into child tasks with a narrow question, expected output, and stop condition.
- Assign children by source set, sub-question, geography, time window, or claim cluster.
- Require children to log reviewed sources and extracted claims before asking for synthesis.
- Merge child outputs into a single evidence picture and resolve duplicates.
- Stop draft writing if the evidence base is still thin or contradictory.
- Trigger a red-team pass before finalizing any recommendation-heavy report.
- Keep final ownership centralized: only the parent should finalize `drafts/final_report.md`.

Each child task should include:

- the exact research question
- scope boundaries
- source preferences and exclusions
- required artifact updates
- time or token budget
- definition of done

## Child Agent Rules

The child agent owns disciplined execution inside a narrow scope.

- Do not expand scope without writing down the reason.
- Search broadly first, then read deeply only where signal is high.
- Log source quality issues, conflicts, and freshness risk.
- Extract atomic claims, not polished prose.
- Mark each claim as supported, disputed, weak, or open.
- Escalate when the question cannot be answered credibly with available evidence.
- Return concise handoff notes so the parent can merge quickly.

## Quality Gates

Before moving from discovery to synthesis, confirm:

- Key research questions are listed.
- Major source types have been sampled.
- Important sources are logged, not just cited in prose.
- Core claims have evidence links.
- Known gaps are written down.

Before moving from draft to final, confirm:

- The answer addresses the stated decision or objective.
- Strong counterarguments were tested.
- Time-sensitive facts were checked for freshness.
- Recommendations match the confidence level of the evidence.
- Open questions are clearly labeled.
- Citation coverage is auditable.

## Evidence Handling

- Use atomic claims: one claim per row.
- Prefer direct quotes only when exact wording matters.
- Keep statistics with unit, date, geography, and source context.
- If two credible sources disagree, capture both and explain the likely reason.
- If evidence is absent, say so plainly.

## Collaboration Rules

- Work only inside your assigned files or sections unless ownership changes.
- Do not overwrite another worker's active draft without reading it first.
- If you must correct existing content, preserve the original meaning in notes.
- Favor additive edits and explicit status changes over silent rewrites.

## Definition Of Done

Research is not done when a draft exists. It is done when:

- the decision or question is answered directly
- evidence traceability is intact
- important gaps are acknowledged
- the strongest objections have been tested
- a fresh reader can audit the workflow from task intake to final report
