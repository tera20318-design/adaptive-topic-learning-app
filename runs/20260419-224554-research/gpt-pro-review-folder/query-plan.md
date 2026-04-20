# Query Plan

Topic: めっき  
Preset logic milestone: `M4`  
Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170  
Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36  
Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.  
Override authority: user  
Full DR equivalent: no (scoped or lighter-than-full DR)  
Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.  
Topic scope: `standard` (`manual_override`, breadth score `50`)  
Topic stop profile: standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800  
Entity discovery: `off` (`manual_override`, score `0`)  
Discovery kind: `technology` (`manual_override`, score `0`)  
Discovery bundle: `一般トピック概説`  
Discovery family: `independent_context`  
Entity discovery profile: off / optional / kind technology / bundle 一般トピック概説; score 0; surface_floor=0, tail_queries=0

## Search intent

- 方式差と用途差を、日本語の公的/業界/標準資料でまず押さえる。
- 規制/EHS は一次情報のみで数値と日付を確定する。
- 電子・PCB・microvia は IPC と JEITA を軸に、過大一般化を避ける。
- vendor は代表例として補助的に使う。

## Required query families

- `official_primary`: original regulator, ministry, and official pages
- `regulation_standards`: laws, standards, guidelines, and regulator material
- `research_validation`: technical validation, professional or standards material
- `vendor_implementation`: vendor implementation examples
- `independent_context`: independent technical and industry context
- `japan_specific`: Japan-specific and Japanese-language sources
- `contradiction_negative`: contradictions, exclusions, and overgeneralization checks
- `upstream_downstream`: supply chain and process-flow structure
- `role_structure`: role differences across users, vendors, job platers, and OEMs
- `chronology_change`: date-sensitive changes and current-state differences

## Required report sections

- `## 1. 要約`
- `## 2. 主要な発見`
- `## 3. 主要な根拠と出典`
- `## 4. 論点別の分析`
- `## 5. 判断のために確認すべきことと追加調査`
- `## 6. 主要ソース一覧`
- `### 4.1 方式ごとの比較ポイント`
- `### 4.2 用途別・産業別に何が違うか`
- `### 4.3 工程・設備・外注先を見るポイント`
- `### 4.4 誤解しやすい点と例外`
- `### 4.5 いま変わっている制度・市場・技術`
- `### 4.6 実務判断に効くコストと品質の勘所`
- `### 4.7 見落とすと危険なドメイン固有リスク`

## Required logic artifacts

- `notes/topic-profile.md`
- `notes/contradiction-log.md`
- `notes/upstream-downstream-map.md`
- `notes/role-structure-matrix.md`
- `notes/domain-risk-map.md`

Decision layer minimum:
- Add at least one reader-facing checklist row that a decision-maker can act on directly.
- Use the checklist columns exactly as: 判断場面 / 確認すること / なぜ重要か / 失敗した場合のリスク / 根拠または確認先.
- If this run is scoped or non-full-DR-equivalent, keep that label visible in the report opening and metadata.

Status guidance: use `pending`, `in_progress`, `covered`, `covered_by_mapping`, `waived`, `not_covered`, or `blocked`.  
`covered_by_mapping` is not a manual assertion: it should survive automatic verification from `sources/citation-ledger.tsv` plus report section usage, or it will fall back to `not_covered`.

| Family ID | Required | Query family | Goal | Example queries | Status | Coverage | Coverage evidence | Waiver reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `official_primary` | required | official | 公的機関と公式本文を押さえる | `六価クロム 一般排水基準 環境省`; `OSHA chromium VI 1910.1026`; `RoHS directive official EU` | covered | covered | env.go.jp / osha.gov / environment.ec.europa.eu | - |
| `regulation_standards` | required | regulation / standards | 規制、基準、標準、規格を押さえる | `JIS K0102-3 六価クロム 2024`; `IPC 4552 ENIG`; `ECHA Annex XVII nickel release` | covered | covered | env.go.jp / ipc.org / echa.europa.eu | - |
| `research_validation` | required | validation | 技術妥当性と専門資料を押さえる | `めっき 防食 基礎 ORIST PDF`; `JEITA 信頼性評価ガイド`; `Nickel plating handbook` | covered | covered | orist / JEITA / Nickel Institute | - |
| `vendor_implementation` | required | vendor example | 代表的な実装例を押さえる | `JCU めっき 技術資料 PDF` | covered | covered | jcu-i.com | - |
| `independent_context` | required | independent context | 第三者・業界文脈を押さえる | `めっき 表面技術協会 基礎`; `JISF 亜鉛めっき`; `AMPP protective coatings` | covered | covered | sfj.or.jp / jisf.or.jp / ampp.org | - |
| `japan_specific` | required | Japan-specific | 日本語・日本制度・日本用途を押さえる | `めっき 表面技術協会 基礎`; `METI めっき 用途分類`; `JEITA 電子部品 部会` | covered | covered | sfj.or.jp / meti.go.jp / jeita.or.jp | - |
| `contradiction_negative` | required | contradiction / boundary | 例外、過大一般化、混同を防ぐ | `暫定排水基準 電気めっき 2024 環境省`; `IPC microvia reliability warning`; `下水道 除害施設 六価クロム 国交省` | covered | covered | env.go.jp / ipc.org / mlit.go.jp | - |
| `upstream_downstream` | required | upstream/downstream | 工程流れと関係者を押さえる | `METI PRTR めっき 手引き`; `JCU 表面処理技術資料`; `EPA electroplating effluent guidelines` | covered | covered | meti.go.jp / jcu-i.com / epa.gov | - |
| `role_structure` | required | role structure | 専業めっき会社、OEM、自社ライン、規制側の役割差を見る | `JEITA 電子部品 部会`; `JFS`; `JCU 表面処理技術資料` | covered | covered | jeita.or.jp / jisf.or.jp / jcu-i.com | - |
| `chronology_change` | required | chronology | 日付依存の変化を確認する | `2022-04-01 六価クロム 環境基準`; `2024-02-05 JIS K0102-3`; `2024-12-11 暫定基準延長` | covered | covered | env.go.jp | - |
