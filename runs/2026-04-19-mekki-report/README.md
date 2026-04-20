# めっきレポート

This case uses the `research-os` workflow.

## Quick Start

```powershell
python research-os/scripts/init_research_project.py "C:\Users\tera2\.claude\ide\runs\2026-04-19-mekki-report" --title "めっきレポート" --force
python research-os/scripts/extract_links.py "C:\Users\tera2\.claude\ide\runs\2026-04-19-mekki-report" -o "C:\Users\tera2\.claude\ide\runs\2026-04-19-mekki-report/sources/collected_urls.txt"
python research-os/scripts/build_evidence_matrix.py "C:\Users\tera2\.claude\ide\runs\2026-04-19-mekki-report" --merge-existing
```

## Workflow Order
1. Fill `TASK.md`.
2. Fill `PLANS.md`.
3. Log candidates in `sources/source_candidates.md`.
4. Log reviewed sources in `sources/source_log.md`.
5. Extract atomic claims in `extracts/claim_table.md`.
6. Rebuild and refine `extracts/evidence_matrix.md`.
7. Run critique in `reviews/`.
8. Draft and finalize in `drafts/`.
