# Plan

## Status Snapshot

- Current phase: Planning
- Overall status: In progress
- Last updated: 2026-04-19
- Parent owner: parent-orchestrator

## Milestones

| Phase | Goal | Owner | Status | Exit Criteria |
| --- | --- | --- | --- | --- |
| Intake | ユーザー依頼を研究案件へ変換 | Parent | Completed | TASK.md が埋まっている |
| Planning | 調査論点と役割分担を固定 | Parent | In progress | 子エージェントの担当と期待成果物が定義済み |
| Discovery | 出典候補と主要ソースを収集 | Child A / B / C | Not started | source_candidates.md と source_log.md に主要ソースが入る |
| Review | 各ソースの要点と信頼性を確認 | Child A / B / C | Not started | 信頼度付きで source_log.md が更新される |
| Extraction | 主張を atomic claims へ分解 | Parent + Child B | Not started | claim_table.md と evidence_matrix.md が埋まる |
| Gap analysis | 弱い根拠と未確認点を明示 | Parent | Not started | gap_analysis.md が埋まる |
| Red team | 過剰断定や抜け漏れを検査 | Child D | Not started | red_team_review.md と citation_audit.md が埋まる |
| Draft | 初稿と改稿を作成 | Parent | Not started | draft_v1.md と draft_v2.md が埋まる |
| Final | 最終レポートを確定 | Parent | Not started | final_report.md が出典整合済みで完成 |

## Workstreams

| Workstream | Question or deliverable | Owner | Depends on | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| WS1 | めっきの定義、種類、基本工程の整理 | Child A | TASK | Queued | 公的・教育・技術資料を収集 |
| WS2 | 主な用途、機能、代表材料の整理 | Child B | TASK | Queued | 産業用途と性能観点を整理 |
| WS3 | 環境・安全・品質論点の整理 | Child C | TASK | Queued | 規制と安全の概説ソースを集める |
| WS4 | 親による統合、主張表、最終稿 | Parent | WS1-WS3 | Pending | 子の結果待ち |
| WS5 | 批判レビューと引用監査 | Child D | WS4 draft_v1 | Pending | 初稿完成後に実施 |

## Child Agent Queue

| ID | Assigned question | Owner | Inputs | Expected outputs | Status |
| --- | --- | --- | --- | --- | --- |
| A | めっきの定義、分類、工程を一次・技術資料ベースで整理する | Child A | TASK.md | source candidates, source notes, key claims | Ready to assign |
| B | めっきの主用途、材料、利点と限界を整理する | Child B | TASK.md | source candidates, source notes, key claims | Ready to assign |
| C | めっきの環境・安全・品質論点を概説レベルで整理する | Child C | TASK.md | source candidates, source notes, key claims | Ready to assign |
| D | draft_v1 に対する厳しめの red-team と citation audit | Child D | draft_v1, source log, claim table | red_team_review.md, citation_audit.md | Blocked on draft |

## Decision Log

| Date | Decision | Reason | Impact |
| --- | --- | --- | --- |
| 2026-04-19 | 概説レポートとして実施 | ユーザー依頼が広く、まずは基礎全体像が必要 | 特定用途の深掘りは後続に回す |
| 2026-04-19 | サブエージェントを定義・用途・リスクで分担 | 同一ファイルの競合を避けつつ並列化するため | sources と claims を親が統合する |

## Immediate Next Steps

1. 子エージェント A/B/C に分担調査を依頼する
2. 親が source_candidates.md と source_log.md の統合器として受け皿を準備する
3. 子の結果をもとに claim_table.md と draft_v1.md を作る
