# Research Brief

- Run ID: 20260419-101901-research
- Topic: めっき
- Output language: Japanese
- Research mode: gpt-like
- Research preset: dr_ultra logic scaffold (focused-budget override; not a full dr_ultra-equivalent run)
- As-of date: 2026-04-19
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.
- Candidate collection target: focused-budget pass (raw-hit budget 80; practical floor 20 surviving candidates)
- Deep-read target: 14
- Topic breadth class: standard (manual override / focused overview)
- Topic breadth score: 50
- Topic budget scale: 0.45
- Topic stop profile: standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800
- Entity discovery mode: off
- Discovery kind: technology (`manual_override`, score 0)
- Discovery bundle: general overview
- Entity discovery profile: off / optional / kind technology / bundle general overview; score 0; surface_floor=0, tail_queries=0
- Generated at: 2026-04-19 10:19:01
- Run posture: document-first focused-budget overview; this run uses dr_ultra logic as a checklist scaffold only

## Core question

- めっきとは何かを、方式・用途・品質・環境安全の観点から、日本語で再利用しやすい概説レポートとして整理する。
- 読者が「どのめっき方式を、どんな目的で、どんな注意点と規制制約の下で採用するか」を短時間で把握できる状態を作る。

## User constraints

- 今回は再現性検証を兼ねるため、前回分や途中成果物は参照しない。
- fresh run の内部成果物だけを使って、ゼロから調査・執筆する。
- サブエージェントを使って並列調査する。
- この run は日本向け概説に絞った focused-budget pass であり、通常の dr_ultra 相当の探索量や tail sweep は実施していない。

## Must-cover angles

- めっきの定義と表面処理全体の中での位置づけ
- 主な方式: 電気めっき、無電解めっき、溶融めっき、真空めっき/乾式表面処理との境界
- 主な皮膜金属と代表機能: 防食、装飾、導電、はんだ付け性、耐摩耗、磁性など
- 主な用途: 自動車、電子部品、プリント基板、半導体周辺、建材、装飾
- 工程管理・品質指標: 密着性、膜厚、均一性、外観、耐食性、不具合
- 環境・安全・規制: 排水処理、六価クロム、ニッケル、RoHS/REACH、労働安全
- 日本の読者向けの産業・制度上の補足

## Reader decisions to support

- 概要説明資料として何を最低限押さえるべきか
- 湿式めっきと乾式表面処理をどう言い分けるべきか
- 防食・装飾・電子用途で方式選定時に何を比較すべきか
- レポート内で断定を避けるべき規制・健康影響の論点は何か

## Must-not-miss risks

- 「めっき」を電気めっきだけに狭く定義してしまうリスク
- 真空蒸着やスパッタを広義のめっきと呼ぶ文脈と、狭義では含めない文脈の混同
- 六価クロム規制やニッケル規制を、用途横断で一律に断定してしまうリスク
- 企業 marketing の主張を、一般論としてそのまま採用するリスク
- 日本の排水基準や暫定基準の時点依存性を落とすリスク

## Assumptions

- 対象読者は、材料・製造・品質・調達の初中級実務者を想定する。
- 学術レビューではなく、実務に使える概説レポートを目指す。
- 法令助言そのものではなく、規制論点の整理を行う。

## Preferred domains

- env.go.jp
- mhlw.go.jp
- epa.gov
- echa.europa.eu
- eur-lex.europa.eu
- sfj.or.jp
- mekki.sfj.or.jp
- zentoren.or.jp
- aen-mekki.or.jp
- kizaikou.or.jp
- asminternational.org

## Excluded angles

- 個別企業の売上ランキングや市場規模推計の深掘り
- 特定企業の途中資料、過去 run、既存レポートの再利用
- 量子・ナノ材料など周辺テーマへの逸脱

## Checklist ideas

- 用途に対して必要機能を先に定義したか
- 方式ごとの膜厚・均一性・密着性・量産性の違いを確認したか
- 皮膜金属と後処理の組み合わせを確認したか
- 六価クロム、ニッケル、排水、RoHS/REACH のどれが関係するか切り分けたか
- 製品接触条件と職業ばく露条件を混同していないか

## Tail sweep

- Entity discovery is off for this pass; do not reopen roster-building unless a later pass explicitly broadens scope.
- If a later pass re-enables discovery, switch to a technology/general-overview bundle rather than a company roster.

## Stop rule

Stop after the core decision layer is evidenced and newly surfaced sources add little novelty. This focused-budget pass should not chase full dr_ultra-equivalent tail coverage once the practical overview is stable.
