# Research Brief

- Run ID: 20260419-224554-research
- Topic: めっき
- Output language: Japanese
- Research mode: gpt-like
- Research preset: dr_ultra
- As-of date: 2026-04-19
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.
- Candidate collection target: 20
- Deep-read target: 10
- Topic breadth class: standard (manual_override, breadth score 50)
- Topic budget scale: 0.45
- Topic stop profile: standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800
- Entity discovery mode: off
- Discovery kind: technology (`manual_override`, score 0)
- Discovery bundle: 一般トピック概説
- Entity discovery profile: off / optional / kind technology / bundle 一般トピック概説; score 0; surface_floor=0, tail_queries=0
- Generated at: 2026-04-19 22:45:54

## Core question

- めっきとは何かを、方式差、用途差、品質・不良・工程管理、規制/EHS、実務判断の観点から日本語で俯瞰し、読者が何を確認すべきかまで落とし込む。

## User constraints

- 既存の調査、過去 run、途中成果は参考・引用しない。
- 新規に調査し、新規ソースだけで report を構成する。
- サブエージェントを使って並列調査する。

## Must-cover angles

- 定義と境界: 湿式/乾式、電気めっき、無電解めっき、溶融めっき。
- 用途: 自動車、電子部品、PCB、半導体周辺、建材、装飾。
- 品質: 前処理、密着、膜厚不均一、ピット、ブリスター、接触抵抗、はんだ付け性、microvia。
- リスク: 水素脆化、ベーキング、浴管理、歩留まり、外注先管理。
- 規制: 日本の六価クロム、OSHA Chromium(VI)、US EPA、EU RoHS、REACH Annex XVII、ニッケル放出条件、PFAS 関連。

## Reader decisions to support

- 方式名だけでなく、用途・基材・要求性能から適切なめっきを選べるか。
- 工程・設備・外注先のどこを確認すべきか。
- 品質不良と規制/EHS のどちらが主要なボトルネックになるかを見分けられるか。
- 規制の数値や適用範囲を混同せずに説明できるか。

## Must-not-miss risks

- 高強度鋼やばね材での水素脆化。
- PCB/HDI 文脈に限定すべき microvia warning の過大一般化。
- 六価クロムの環境基準、一般排水基準、測定法改正、暫定基準の取り違え。
- RoHS の含有制限と REACH Annex XVII の放出条件の混線。
- vendor/industry association 情報を一般化しすぎること。

## Assumptions

- 今回は focused overview であり、個別製品の受入規格値や各社固有の工程窓までは踏み込まない。
- 技術・規制の骨格は一次情報と公的/標準系資料で押さえ、vendor 資料は代表例として扱う。

## Preferred domains

- `env.go.jp`
- `mlit.go.jp`
- `meti.go.jp`
- `osha.gov`
- `epa.gov`
- `environment.ec.europa.eu`
- `echa.europa.eu`
- `ipc.org`
- `jeita.or.jp`
- `jisf.or.jp`
- `sfj.or.jp`
- `orist.jp`
- `nickelinstitute.org`

## Excluded angles

- 個別メーカー比較を主題にすること。
- 既存 run や過去成果物の要約・流用。

## Checklist ideas

- 基材と要求性能から方式を逆算する。
- 前処理、膜厚、密着、浴管理、ベーキングの確認点を分ける。
- 排水・ばく露・RoHS/REACH の確認窓口を分ける。

Decision layer minimum:
- At least one reader-facing checklist row before delivery.
- Use the checklist columns exactly as: 判断場面 / 確認すること / なぜ重要か / 失敗した場合のリスク / 根拠または確認先.
- If this run is not full DR-equivalent, say so in the summary and metadata block.

## Tail sweep

- Discovery is not the primary task for this run.
- Use concept coverage rather than company roster breadth.

## Stop rule

Stop after the deep-read target is met and newly surfaced sources add little novelty. Because this is a focused overview run, prefer source-class diversity and decision usefulness over raw search volume.
