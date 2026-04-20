# GPT Pro Review Bundle

??????? `20260419-224554-research` run ?????? bundle ?????????????????????????????????

---

## FILE: `brief.md`

```text
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
```

---

## FILE: `query-plan.md`

```text
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
```

---

## FILE: `run-config.toml`

```text
run_id = "20260419-224554-research"
topic = "めっき"
mode = "gpt-like"
preset = "dr_ultra"
output_language = "Japanese"
as_of_date = "2026-04-19"
generated_at = "2026-04-19 22:45:54"

[preset_baseline]
query_budget = 88
raw_hit_budget = 1040
open_budget = 280
deep_read_budget = 84
candidate_target = 1040
deep_read_target = 84
unique_cited_source_target = 52
citation_instance_target = 170

[override]
original_budget = "candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170"
effective_budget = "candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36"
override_reason = "Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target."
override_authority = "user"
full_dr_equivalent = false
report_status_implication = "A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent."

[metadata_override]
override_reason = "Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target."
override_authority = "user"
full_dr_equivalent = false
report_status_implication = "A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent."

[metadata_override.original_budget]
query_budget = 88
raw_hit_budget = 1040
open_budget = 280
deep_read_budget = 84
candidate_target = 1040
deep_read_target = 84
unique_cited_source_target = 52
citation_instance_target = 170

[metadata_override.effective_budget]
query_budget = 24
raw_hit_budget = 80
open_budget = 30
deep_read_budget = 14
candidate_target = 20
deep_read_target = 10
unique_cited_source_target = 14
citation_instance_target = 36

[budgets]
query_budget = 24
raw_hit_budget = 80
open_budget = 30
deep_read_budget = 14

[citations]
unique_cited_source_target = 14
citation_instance_target = 36
min_citations_per_major_section = 3
primary_source_ratio_min = 0.70

[stopping]
novelty_stop_threshold = 0.04
max_same_domain_ratio = 0.18
recency_bias_days = 1460

[source_scope]
web_mode = "full_web"
allowed_domains = []
file_inputs = []

[topic_scope]
breadth_class = "standard"
breadth_label = "標準"
breadth_score = 50
classification_source = "manual_override"
note_required = true
budget_scale = 0.45
signals = ["manual_override:focused_overview_report", "manual_override:no_prior_run_reuse"]
minimum_query_floor = 12
minimum_candidate_floor = 20
minimum_deep_read_floor = 10
novelty_stop_multiplier = 1.0
max_same_domain_ratio_multiplier = 1.0
effective_novelty_stop_threshold = 0.04
effective_max_same_domain_ratio = 0.18
stop_summary = "standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800"

[entity_scope]
mode = "off"
required = false
score = 0
kind = "technology"
kind_source = "manual_override"
kind_score = 0
bundle_id = "general-overview"
bundle_label = "一般トピック概説"
family_id = "independent_context"
surface_label = "must-find concepts"
classification_source = "manual_override"
minimum_surface_floor = 0
minimum_entity_floor = 0
minimum_tail_query_floor = 0
signals = ["manual_override:technology_overview"]
summary = "off / optional / kind technology / bundle 一般トピック概説; score 0; surface_floor=0, tail_queries=0"

[coverage]
logic_milestone = "M4"
required_query_families = ["official_primary", "regulation_standards", "research_validation", "vendor_implementation", "independent_context", "japan_specific", "contradiction_negative", "upstream_downstream", "role_structure", "chronology_change"]
required_report_sections = ["## 1. 要約", "## 2. 主要な発見", "## 3. 主要な根拠と出典", "## 4. 論点別の分析", "## 5. 判断のために確認すべきことと追加調査", "## 6. 主要ソース一覧", "### 4.1 方式ごとの比較ポイント", "### 4.2 用途別・産業別に何が違うか", "### 4.3 工程・設備・外注先を見るポイント", "### 4.4 誤解しやすい点と例外", "### 4.5 いま変わっている制度・市場・技術", "### 4.6 実務判断に効くコストと品質の勘所", "### 4.7 見落とすと危険なドメイン固有リスク"]

[evidence_audit]
enabled = true
min_fact_evidence_count = 2
min_fact_primary_count = 1
min_inference_evidence_count = 2
min_inference_primary_count = 1

[advanced_logic]
required_note_artifacts = ["notes/topic-profile.md", "notes/contradiction-log.md", "notes/upstream-downstream-map.md", "notes/role-structure-matrix.md", "notes/domain-risk-map.md"]
requires_gap_followup_when_claims_fail = true
followup_query_family_targets = ["contradiction_negative", "upstream_downstream", "role_structure"]

[quality_gate]
strict = true
require_domain_risk_section = true
require_checklist_section = true
require_uncertainty_section = true
require_decision_section = true
decision_layer_minimum = [
  "At least one reader-facing checklist row before delivery.",
  "Checklist columns: 判断場面 / 確認すること / なぜ重要か / 失敗した場合のリスク / 根拠または確認先.",
  "Keep a separate uncertainty and follow-up subsection.",
]
non_full_dr_requires_explicit_label = true
```

---

## FILE: `metrics.json`

```text
{
  "run_id": "20260419-224554-research",
  "topic": "めっき",
  "mode": "gpt-like",
  "preset": "dr_ultra",
  "as_of_date": "2026-04-19",
  "updated_at": "2026-04-19 23:15:28",
  "phase": "complete",
  "status": "complete",
  "topic_scope": {
    "breadth_class": "standard",
    "breadth_label": "標準",
    "breadth_score": 50,
    "classification_source": "manual_override",
    "note_required": true,
    "budget_scale": 0.45,
    "signals": [
      "manual_override:focused_overview_report",
      "manual_override:no_prior_run_reuse"
    ],
    "minimum_query_floor": 12,
    "minimum_candidate_floor": 20,
    "minimum_deep_read_floor": 10,
    "novelty_stop_multiplier": 1.0,
    "max_same_domain_ratio_multiplier": 1.0,
    "effective_novelty_stop_threshold": 0.04,
    "effective_max_same_domain_ratio": 0.18,
    "stop_summary": "standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800"
  },
  "entity_scope": {
    "mode": "off",
    "required": false,
    "score": 0,
    "kind": "technology",
    "kind_source": "manual_override",
    "kind_score": 0,
    "bundle_id": "general-overview",
    "bundle_label": "一般トピック概説",
    "family_id": "independent_context",
    "surface_label": "must-find concepts",
    "classification_source": "manual_override",
    "minimum_surface_floor": 0,
    "minimum_entity_floor": 0,
    "minimum_tail_query_floor": 0,
    "signals": [
      "manual_override:technology_overview"
    ],
    "summary": "off / optional / kind technology / bundle 一般トピック概説; score 0; surface_floor=0, tail_queries=0"
  },
  "logic": {
    "milestone": "M4",
    "requires_claim_ledger": true,
    "required_report_sections": [
      "## 1. 要約",
      "## 2. 主要な発見",
      "## 3. 主要な根拠と出典",
      "## 4. 論点別の分析",
      "## 5. 判断のために確認すべきことと追加調査",
      "## 6. 主要ソース一覧",
      "### 4.1 方式ごとの比較ポイント",
      "### 4.2 用途別・産業別に何が違うか",
      "### 4.3 工程・設備・外注先を見るポイント",
      "### 4.4 誤解しやすい点と例外",
      "### 4.5 いま変わっている制度・市場・技術",
      "### 4.6 実務判断に効くコストと品質の勘所",
      "### 4.7 見落とすと危険なドメイン固有リスク"
    ],
    "required_note_artifacts": [
      "notes/topic-profile.md",
      "notes/contradiction-log.md",
      "notes/upstream-downstream-map.md",
      "notes/role-structure-matrix.md",
      "notes/domain-risk-map.md"
    ],
    "requires_gap_followup_when_claims_fail": true
  },
  "quality_gate": {
    "strict": true,
    "require_domain_risk_section": true,
    "require_checklist_section": true,
    "require_uncertainty_section": true,
    "require_decision_section": true
  },
  "run_profile": {
    "original_budget": {
      "candidate_target": 1040,
      "deep_read_target": 84,
      "query_budget": 88,
      "raw_hit_budget": 1040,
      "open_budget": 280,
      "deep_read_budget": 84,
      "unique_cited_source_target": 52,
      "citation_instance_target": 170
    },
    "effective_budget": {
      "candidate_target": 20,
      "deep_read_target": 10,
      "query_budget": 24,
      "raw_hit_budget": 80,
      "open_budget": 30,
      "deep_read_budget": 14,
      "unique_cited_source_target": 14,
      "citation_instance_target": 36
    },
    "override_reason": "Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.",
    "override_authority": "user",
    "full_dr_equivalent": false,
    "full_dr_equivalent_label": "no (scoped or lighter-than-full DR)",
    "report_status_implication": "A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent."
  },
  "metadata_override": {
    "original_budget": {
      "candidate_target": 1040,
      "deep_read_target": 84,
      "query_budget": 88,
      "raw_hit_budget": 1040,
      "open_budget": 280,
      "deep_read_budget": 84,
      "unique_cited_source_target": 52,
      "citation_instance_target": 170
    },
    "effective_budget": {
      "candidate_target": 20,
      "deep_read_target": 10,
      "query_budget": 24,
      "raw_hit_budget": 80,
      "open_budget": 30,
      "deep_read_budget": 14,
      "unique_cited_source_target": 14,
      "citation_instance_target": 36
    },
    "override_reason": "Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.",
    "override_authority": "user",
    "full_dr_equivalent": false,
    "full_dr_equivalent_label": "no (scoped or lighter-than-full DR)",
    "report_status_implication": "A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent."
  },
  "budgets": {
    "query_budget": 24,
    "raw_hit_budget": 80,
    "open_budget": 30,
    "deep_read_budget": 14
  },
  "citation_targets": {
    "unique_cited_source_target": 14,
    "citation_instance_target": 36,
    "min_citations_per_major_section": 3,
    "primary_source_ratio_min": 0.7
  },
  "counts": {
    "executed_queries": 25,
    "raw_hits": 25,
    "unique_urls": 25,
    "deep_read_selected": 22,
    "opened_sources": 22,
    "unique_cited_sources": 29,
    "citation_instances": 167,
    "primary_cited_sources": 20
  },
  "ratios": {
    "query_budget_utilization": 1.0417,
    "raw_hit_budget_utilization": 0.3125,
    "open_budget_utilization": 0.7333,
    "deep_read_budget_utilization": 1.5714,
    "unique_cited_source_target_utilization": 2.0714,
    "citation_instance_target_utilization": 4.6389,
    "primary_source_ratio": 0.6897,
    "official_regulator_ratio": 0.2814,
    "standards_or_academic_ratio": 0.3653,
    "vendor_dependency_ratio": 0.0599,
    "industry_association_dependency_ratio": 0.1617
  },
  "evidence_audit": {
    "enabled": true,
    "thresholds": {
      "min_fact_evidence_count": 2,
      "min_fact_primary_count": 1,
      "min_inference_evidence_count": 2,
      "min_inference_primary_count": 1
    },
    "counts": {
      "total_claims": 95,
      "fact_claims": 31,
      "inference_claims": 0,
      "open_question_claims": 0,
      "advice_claims": 44,
      "regulatory_claims": 12,
      "numeric_claims": 0,
      "temporal_claims": 8,
      "scope_claims": 0,
      "out_of_scope_claims": 0,
      "passing_claims": 95,
      "weak_claims": 0,
      "missing_claims": 0,
      "auditable_claims": 95
    },
    "ratios": {
      "passing_ratio": 1.0
    },
    "regulatory_numeric_temporal_gaps": []
  },
  "claim_coverage": {
    "extracted_report_claims_count": 95,
    "ledger_claims_count": 95,
    "captured_report_claims_count": 95,
    "supported_report_claims_count": 95,
    "out_of_scope_report_claims_count": 0,
    "mainline_out_of_scope_claims_count": 0,
    "appendix_out_of_scope_claims_count": 0,
    "high_risk_report_claims_count": 70,
    "high_risk_claims_in_ledger_count": 70,
    "high_risk_supported_claims_count": 70,
    "high_risk_out_of_scope_claims_count": 0,
    "high_risk_mainline_out_of_scope_claims_count": 0,
    "high_risk_appendix_out_of_scope_claims_count": 0,
    "report_claim_capture_ratio": 1.0,
    "supported_claim_ratio": 1.0,
    "high_risk_supported_claim_ratio": 1.0,
    "out_of_scope_claim_ratio": 0.0,
    "claim_coverage_ratio": 1.0,
    "high_risk_claim_coverage_ratio": 1.0,
    "missing_claims_from_ledger": [],
    "out_of_scope_claims": [],
    "regulatory_numeric_temporal_missing": []
  },
  "metadata_consistency": {
    "status": "consistent",
    "files": {
      "brief": {
        "present": true,
        "consistent": true,
        "missing_lines": []
      },
      "query_plan": {
        "present": true,
        "consistent": true,
        "missing_lines": []
      },
      "topic_profile": {
        "present": true,
        "consistent": true,
        "missing_lines": []
      },
      "report": {
        "present": true,
        "consistent": true,
        "missing_lines": []
      }
    },
    "mismatches": [],
    "expected": {
      "original_budget": {
        "candidate_target": 1040,
        "deep_read_target": 84,
        "query_budget": 88,
        "raw_hit_budget": 1040,
        "open_budget": 280,
        "deep_read_budget": 84,
        "unique_cited_source_target": 52,
        "citation_instance_target": 170
      },
      "effective_budget": {
        "candidate_target": 20,
        "deep_read_target": 10,
        "query_budget": 24,
        "raw_hit_budget": 80,
        "open_budget": 30,
        "deep_read_budget": 14,
        "unique_cited_source_target": 14,
        "citation_instance_target": 36
      },
      "metadata_override": {
        "original_budget": {
          "candidate_target": 1040,
          "deep_read_target": 84,
          "query_budget": 88,
          "raw_hit_budget": 1040,
          "open_budget": 280,
          "deep_read_budget": 84,
          "unique_cited_source_target": 52,
          "citation_instance_target": 170
        },
        "effective_budget": {
          "candidate_target": 20,
          "deep_read_target": 10,
          "query_budget": 24,
          "raw_hit_budget": 80,
          "open_budget": 30,
          "deep_read_budget": 14,
          "unique_cited_source_target": 14,
          "citation_instance_target": 36
        },
        "override_reason": "Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.",
        "override_authority": "user",
        "full_dr_equivalent": false,
        "full_dr_equivalent_label": "no (scoped or lighter-than-full DR)",
        "report_status_implication": "A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.",
        "summary": "user: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target."
      },
      "expected_lines": {
        "Preset baseline budget": "Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170",
        "Effective run budget": "Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36",
        "Override reason": "Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.",
        "Override authority": "Override authority: user",
        "Full DR equivalent": "Full DR equivalent: no (scoped or lighter-than-full DR)",
        "Report status implication": "Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent."
      }
    },
    "metadata_block_present": true
  },
  "timings": {
    "search_duration_seconds": 0,
    "search_duration_human": "0s",
    "total_elapsed_seconds": 1709,
    "total_elapsed_human": "28m 29s",
    "phase_durations_seconds": {
      "planning": 1709
    }
  },
  "coverage": {
    "run_id": "20260419-224554-research",
    "preset": "dr_ultra",
    "logic_milestone": "M4",
    "entity_scope": {
      "required": false,
      "mode": "off",
      "score": 0,
      "kind": "technology",
      "kind_score": 0,
      "bundle_id": "general-overview",
      "bundle_label": "一般トピック概説",
      "family_id": "independent_context",
      "family_id_matches_kind": true,
      "summary": "off / optional / kind technology / bundle 一般トピック概説; score 0; surface_floor=0, tail_queries=0"
    },
    "required_query_families": [
      {
        "family_id": "official_primary",
        "label": "一次・公式",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered",
        "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ## 1. 要約 (2); standards_body ipc.org @ ## 2. 主要な発見 (2); standards_body ipc.org @ ## 3. 主要な根拠と出典 (1); +102 more",
        "requested_coverage_evidence": "env.go.jp / osha.gov / environment.ec.europa.eu",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
            "domain": "epa.gov",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
            "domain": "epa.gov",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
            "domain": "epa.gov",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
            "domain": "epa.gov",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
            "domain": "epa.gov",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
            "domain": "meti.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          }
        ],
        "mapping_evidence_count": 105,
        "waiver_reason": "-",
        "matched_query_count": 4,
        "minimum_query_matches_required": 1,
        "sample_queries": [
          "めっき 防食 基礎 ORIST PDF",
          "JCU 表面処理技術 事業戦略 PDF",
          "METI めっき 用途分類 PDF"
        ],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "query_matches",
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "regulation_standards",
        "label": "規制・標準",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered",
        "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ## 1. 要約 (2); standards_body ipc.org @ ## 2. 主要な発見 (2); standards_body ipc.org @ ## 3. 主要な根拠と出典 (1); +86 more",
        "requested_coverage_evidence": "env.go.jp / ipc.org / echa.europa.eu",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
            "domain": "epa.gov",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
            "domain": "epa.gov",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
            "domain": "epa.gov",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          }
        ],
        "mapping_evidence_count": 89,
        "waiver_reason": "-",
        "matched_query_count": 1,
        "minimum_query_matches_required": 1,
        "sample_queries": [
          "EPA electroplating effluent guidelines"
        ],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "query_matches",
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "research_validation",
        "label": "研究・検証",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ## 1. 要約 (2); standards_body ipc.org @ ## 2. 主要な発見 (2); standards_body ipc.org @ ## 3. 主要な根拠と出典 (1); +62 more",
        "requested_coverage_evidence": "orist / JEITA / Nickel Institute",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
            "domain": "epa.gov",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
            "domain": "epa.gov",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
            "domain": "meti.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          }
        ],
        "mapping_evidence_count": 65,
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "vendor_implementation",
        "label": "ベンダー実装",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "auto-verified from citation-ledger: vendor_first_party jcu-i.com @ ## 2. 主要な発見 (2); vendor_first_party jcu-i.com @ ## 3. 主要な根拠と出典 (1); vendor_first_party jcu-i.com @ ### 4.2 用途別・産業別に何が違うか (1); +4 more",
        "requested_coverage_evidence": "jcu-i.com",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          }
        ],
        "mapping_evidence_count": 7,
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "independent_context",
        "label": "独立コンテキスト",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "auto-verified from citation-ledger: government_context www2.orist.jp @ ## 1. 要約 (2); government_context www2.orist.jp @ ## 3. 主要な根拠と出典 (2); government_context www2.orist.jp @ ### 4.1 方式ごとの比較ポイント (2); +45 more",
        "requested_coverage_evidence": "sfj.or.jp / jisf.or.jp / ampp.org",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 3,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 2,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://jisf.or.jp/business/standard/jfs",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://jisf.or.jp/business/standard/jfs",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://jisf.or.jp/business/standard/jfs",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
            "domain": "semicon.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
            "domain": "semicon.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
            "domain": "semicon.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
            "domain": "epa.gov",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
            "domain": "epa.gov",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
            "domain": "meti.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role"
            ]
          }
        ],
        "mapping_evidence_count": 48,
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "japan_specific",
        "label": "日本語・国内",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered",
        "coverage_evidence": "auto-verified from citation-ledger: government_context www2.orist.jp @ ## 1. 要約 (2); government_context www2.orist.jp @ ## 3. 主要な根拠と出典 (2); government_context www2.orist.jp @ ### 4.1 方式ごとの比較ポイント (2); +62 more",
        "requested_coverage_evidence": "sfj.or.jp / meti.go.jp / jeita.or.jp",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 3,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 2,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 2,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 2,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 1. 要約",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.7 見落とすと危険なドメイン固有リスク",
            "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.1 実務チェックリスト",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.3 不確実性と追加調査",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
            "domain": "home.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 2. 主要な発見",
            "source_url": "https://jisf.or.jp/business/standard/jfs",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "## 3. 主要な根拠と出典",
            "source_url": "https://jisf.or.jp/business/standard/jfs",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://jisf.or.jp/business/standard/jfs",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.1 方式ごとの比較ポイント",
            "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
            "domain": "semicon.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
            "domain": "semicon.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 5.2 追加で確認したい主張と調査の向き",
            "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
            "domain": "semicon.jeita.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.2 用途別・産業別に何が違うか",
            "source_url": "https://jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf",
            "domain": "jisf.or.jp",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
            "domain": "meti.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "domain"
            ]
          }
        ],
        "mapping_evidence_count": 65,
        "waiver_reason": "-",
        "matched_query_count": 1,
        "minimum_query_matches_required": 1,
        "sample_queries": [
          "溶融亜鉛めっき 日本鉄鋼連盟"
        ],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "query_matches",
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "contradiction_negative",
        "label": "反証・不在確認",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "auto-verified from citation-ledger: legal_text echa.europa.eu @ ### 4.5 いま変わっている制度・市場・技術 (1); legal_text environment.ec.europa.eu @ ### 4.5 いま変わっている制度・市場・技術 (1); legal_text osha.gov @ ### 4.5 いま変わっている制度・市場・技術 (1); +5 more",
        "requested_coverage_evidence": "env.go.jp / ipc.org / mlit.go.jp",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/110052.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_02720.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
            "domain": "epa.gov",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.5 いま変わっている制度・市場・技術",
            "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
            "domain": "epa.gov",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          }
        ],
        "mapping_evidence_count": 8,
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "upstream_downstream",
        "label": "上流/下流",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "auto-verified from citation-ledger: government_context www2.orist.jp @ ### 4.4 誤解しやすい点と例外 (1); official_regulator env.go.jp @ ### 4.4 誤解しやすい点と例外 (1); professional_body mekki.sfj.or.jp @ ### 4.4 誤解しやすい点と例外 (1); +6 more",
        "requested_coverage_evidence": "meti.go.jp / jcu-i.com / epa.gov",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
            "domain": "echa.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
            "domain": "environment.ec.europa.eu",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://env.go.jp/press/press_03960.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.4 誤解しやすい点と例外",
            "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
            "domain": "mlit.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          }
        ],
        "mapping_evidence_count": 9,
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "role_structure",
        "label": "役割差・類型",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ### 4.3 工程・設備・外注先を見るポイント (1); government_context www2.orist.jp @ ### 4.3 工程・設備・外注先を見るポイント (1); standards_body astm.org @ ### 4.3 工程・設備・外注先を見るポイント (1); +10 more",
        "requested_coverage_evidence": "jeita.or.jp / jisf.or.jp / jcu-i.com",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
            "domain": "astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
            "domain": "jcu-i.com",
            "source_role": "vendor_first_party",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://env.go.jp/water/impure/haisui.html",
            "domain": "env.go.jp",
            "source_role": "official_regulator",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://mekki.sfj.or.jp/",
            "domain": "mekki.sfj.or.jp",
            "source_role": "professional_body",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
            "domain": "osha.gov",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/Standards/B849.htm",
            "domain": "store.astm.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://store.astm.org/f0519-17a.html",
            "domain": "store.astm.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.3 工程・設備・外注先を見るポイント",
            "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
            "domain": "nickelinstitute.org",
            "source_role": "industry_association",
            "citation_instances": 1,
            "matched_by": [
              "section_heading"
            ]
          }
        ],
        "mapping_evidence_count": 13,
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "mapping_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "chronology_change",
        "label": "時系列・変化点",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ### 4.6 実務判断に効くコストと品質の勘所 (1); government_context www2.orist.jp @ ### 4.6 実務判断に効くコストと品質の勘所 (1); standard_or_code electronics.org @ ### 4.6 実務判断に効くコストと品質の勘所 (1); +2 more",
        "requested_coverage_evidence": "env.go.jp",
        "mapping_evidence_items": [
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
            "domain": "ipc.org",
            "source_role": "standards_body",
            "citation_instances": 1,
            "matched_by": [
              "source_role",
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
            "domain": "www2.orist.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role",
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
            "domain": "electronics.org",
            "source_role": "standard_or_code",
            "citation_instances": 1,
            "matched_by": [
              "source_role",
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
            "domain": "meti.go.jp",
            "source_role": "legal_text",
            "citation_instances": 1,
            "matched_by": [
              "source_role",
              "section_heading"
            ]
          },
          {
            "origin": "citation_ledger",
            "section": "### 4.6 実務判断に効くコストと品質の勘所",
            "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
            "domain": "meti.go.jp",
            "source_role": "government_context",
            "citation_instances": 1,
            "matched_by": [
              "source_role",
              "section_heading"
            ]
          }
        ],
        "mapping_evidence_count": 5,
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "has_mapping_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "mapping_evidence"
        ],
        "covered": true
      }
    ],
    "required_report_sections": [
      {
        "section": "## 1. 要約",
        "matched_heading": "## 1. 要約",
        "present": true
      },
      {
        "section": "## 2. 主要な発見",
        "matched_heading": "## 2. 主要な発見",
        "present": true
      },
      {
        "section": "## 3. 主要な根拠と出典",
        "matched_heading": "## 3. 主要な根拠と出典",
        "present": true
      },
      {
        "section": "## 4. 論点別の分析",
        "matched_heading": "## 4. 論点別の分析",
        "present": true
      },
      {
        "section": "## 5. 判断のために確認すべきことと追加調査",
        "matched_heading": "## 5. 判断のために確認すべきことと追加調査",
        "present": true
      },
      {
        "section": "## 6. 主要ソース一覧",
        "matched_heading": "## 6. 主要ソース一覧",
        "present": true
      },
      {
        "section": "### 4.1 方式ごとの比較ポイント",
        "matched_heading": "### 4.1 方式ごとの比較ポイント",
        "present": true
      },
      {
        "section": "### 4.2 用途別・産業別に何が違うか",
        "matched_heading": "### 4.2 用途別・産業別に何が違うか",
        "present": true
      },
      {
        "section": "### 4.3 工程・設備・外注先を見るポイント",
        "matched_heading": "### 4.3 工程・設備・外注先を見るポイント",
        "present": true
      },
      {
        "section": "### 4.4 誤解しやすい点と例外",
        "matched_heading": "### 4.4 誤解しやすい点と例外",
        "present": true
      },
      {
        "section": "### 4.5 いま変わっている制度・市場・技術",
        "matched_heading": "### 4.5 いま変わっている制度・市場・技術",
        "present": true
      },
      {
        "section": "### 4.6 実務判断に効くコストと品質の勘所",
        "matched_heading": "### 4.6 実務判断に効くコストと品質の勘所",
        "present": true
      },
      {
        "section": "### 4.7 見落とすと危険なドメイン固有リスク",
        "matched_heading": "### 4.7 見落とすと危険なドメイン固有リスク",
        "present": true
      }
    ],
    "required_note_artifacts": [
      {
        "artifact": "notes/topic-profile.md",
        "required": true,
        "present": true
      },
      {
        "artifact": "notes/contradiction-log.md",
        "required": true,
        "present": true
      },
      {
        "artifact": "notes/upstream-downstream-map.md",
        "required": true,
        "present": true
      },
      {
        "artifact": "notes/role-structure-matrix.md",
        "required": true,
        "present": true
      },
      {
        "artifact": "notes/domain-risk-map.md",
        "required": true,
        "present": true
      }
    ],
    "gap_followup_artifact": null,
    "overall_complete": true,
    "coverage_status": "complete",
    "coverage_counts": {
      "query_families_covered": 10,
      "query_families_total": 10,
      "query_families_waived": 0,
      "report_sections_present": 13,
      "report_sections_total": 13,
      "note_artifacts_present": 5,
      "note_artifacts_total": 5
    },
    "missing_query_families": [],
    "missing_report_sections": [],
    "missing_note_artifacts": [],
    "missing_conditional_artifacts": []
  },
  "report_quality": {
    "has_checklist_section": true,
    "has_uncertainty_section": true,
    "has_decision_section": true,
    "has_domain_risk_section": true,
    "has_sources_section": true,
    "has_reader_decision_layer": true,
    "internal_pipeline_headings": [],
    "headings": [
      "1. 要約",
      "2. 主要な発見",
      "0. Research Metadata",
      "3. 主要な根拠と出典",
      "4. 論点別の分析",
      "4.1 方式ごとの比較ポイント",
      "4.2 用途別・産業別に何が違うか",
      "4.3 工程・設備・外注先を見るポイント",
      "4.4 誤解しやすい点と例外",
      "4.5 いま変わっている制度・市場・技術",
      "4.6 実務判断に効くコストと品質の勘所",
      "4.7 見落とすと危険なドメイン固有リスク",
      "5. 判断のために確認すべきことと追加調査",
      "5.1 実務チェックリスト",
      "5.2 追加で確認したい主張と調査の向き",
      "5.3 不確実性と追加調査",
      "6. 主要ソース一覧"
    ]
  },
  "citation_integrity": {
    "report_citation_count": 29,
    "citation_ledger_count": 29,
    "missing_report_citations": []
  },
  "release_gate": {
    "strict": true,
    "finalization_requested": true,
    "status": "complete",
    "blocking_reasons": [],
    "revision_reasons": [],
    "provisional_reasons": [],
    "unresolved_gaps": [],
    "next_required_actions": []
  }
}
```

---

## FILE: `progress.log`

```text
[2026-04-19 22:45:54] phase=planning status=created message=Run initialized with preset dr_ultra and mode gpt-like.
[2026-04-19 23:14:23] phase=complete status=provisional message=Fresh plating report is ready for final gating after all claim and metadata checks passed.
```

---

## FILE: `report/report-ja.md`

```text
# めっきレポート

## 1. 要約

- めっきは装飾だけの話ではなく、実務では防食、導電、接触信頼性、はんだ付け性、拡散バリア、耐摩耗などの機能付与が中心です。[表面技術協会](https://mekki.sfj.or.jp/) [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08)
- 読み手が最初に切り分けるべきなのは「電気めっき」「無電解めっき」「溶融めっき」と、隣接する乾式表面処理を同じものとして扱わないことです。要求性能、基材、量産条件、規制対応がそれぞれ違います。[ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [日本鉄鋼連盟](https://www.jisf.or.jp/business/tech/aen/index.html) [Nickel Institute](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/)
- 品質面で見落としやすいのは、前処理、膜厚不均一、密着不良、ピット/ブリスター、水素脆化、接触抵抗、はんだ付け性、PCB/HDI に限定される microvia reliability です。[ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) [IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 規制面では、日本の六価クロム関連だけでも「環境基準」「一般排水基準」「測定法改正」「暫定排水基準」「公共用水域と下水道の区別」を分けて説明する必要があります。海外では OSHA の作業者ばく露、EPA の electroplating/chromium rules、EU の RoHS と REACH を混同しないことが重要です。[環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html) [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html) [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html) [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
- 今回は個別製品の受入規格値や各社固有の工程窓ではなく、方式差、用途差、品質/EHS リスク、実務判断の共通論点を先に整理します。[ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)

## 2. 主要な発見

- 方式選定は「めっき種の名前」ではなく、基材、要求性能、使用環境、量産条件、EHS 条件から逆算した方が失敗しにくいです。[ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [Nickel Plating Handbook](https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/)
- 自動車や建材では防食と耐久が先に来やすく、電子部品や PCB では接触抵抗、はんだ付け性、微細配線対応が先に来ます。同じ「めっき」でも評価軸が違います。[JFS](https://www.jisf.or.jp/business/standard/jfs/) [JEITA 電子部品部会](https://home.jeita.or.jp/ecb/about/part.html) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- 公開資料の範囲では、job plater、OEM の自社ライン、薬品メーカー、装置メーカー、規制当局、標準団体はそれぞれ見ている指標が違います。情報の立場を混ぜると判断を誤りやすいです。[METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf) [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [JEITA 信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)
- 高強度鋼、ばね材、締結部品では、水素脆化とベーキング条件の確認を抜くと重大事故につながります。これは装飾用途の話ではありません。[JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [ASTM B849](https://store.astm.org/Standards/B849.htm) [ASTM F519](https://store.astm.org/f0519-17a.html)
- PCB/HDI 文脈では、surface finish の選択と microvia reliability を別に考えず、finish、穴埋め、銅めっき、実装条件を一体で見た方が安全です。[IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed) [IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 日本の六価クロムは、`2022-04-01` の環境基準改正、`2024-02-05` 公布・`2024-04-01` 施行の測定法改正、一般排水基準 `0.2 mg Cr(VI)/L` を分けて理解する必要があります。[環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html) [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html) [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
- `2024-12-11` 時点の一次情報では、暫定排水基準の延長対象は亜鉛の電気めっき業であり、六価クロムの暫定基準をそのまま説明するのは不正確です。[環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- EU の RoHS は含有制限、REACH Annex XVII の nickel は主に放出条件で見るため、同じ「材料規制」として一括説明しない方が安全です。[European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)

<!-- BEGIN:RESEARCH-METADATA -->
## 0. Research Metadata

- Research date: 2026-04-19
- Mode / Preset: gpt-like / dr_ultra
- Current phase: complete
- Delivery status: complete
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.
- Query volume: 25 / 24
- Unique URLs: 25
- Deep reads: 22 / 14
- Citation instances: 167 / 36
- Primary-source ratio: 69.0% (target 70.0%)
- Report claim coverage: 95 / 95 (100.0%)
- Supported claim ratio: 95 / 95 (100.0%)
- High-risk claim coverage: 70 / 70 (100.0%)
- High-risk supported claim ratio: 70 / 70 (100.0%)
- Out-of-scope claim ratio: 0 / 95 (0.0%)
- Source role mix: official/legal 28.1%, standards/academic 36.5%, vendor 6.0%, industry association 16.2%
- Coverage gate: complete
  - Query families: 10 / 10
  - Report sections: 13 / 13
  - Logic artifacts: 5 / 5
  - Flow: query coverage -> report sections -> logic artifacts -> overall gate
- Report checks:
  - Checklist section: present
  - Uncertainty section: present
  - Decision layer: present
  - Domain risk section: present
  - Internal pipeline headings removed: yes

<!-- END:RESEARCH-METADATA -->

## 3. 主要な根拠と出典

| 主張 | 根拠の要旨 | 出典 |
| --- | --- | --- |
| [fact] めっきは装飾だけでなく、防食、導電、接触、はんだ付け性、拡散バリアなどの機能付与として広く使われる。 | 日本の学協会・公設試験機関・国際標準の範囲説明が、機能用途を一貫して示している。 | [表面技術協会](https://mekki.sfj.or.jp/) [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) |
| [fact] 電気めっき、無電解めっき、溶融めっきは形成機構も用途も違い、乾式表面処理は隣接概念として分けて扱う方が安全である。 | ASTM B08 の範囲と JISF/Nickel Institute の用途説明が、方式差を別物として扱っている。 | [ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [日本鉄鋼連盟](https://www.jisf.or.jp/business/tech/aen/index.html) [Nickel Institute](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/) |
| [advice] 自動車と建材は防食・耐久、電子部品と PCB は接触抵抗・はんだ付け性・微細配線対応を優先軸として見た方がよい。 | JFS/JISF、JEITA、IPC が用途別の評価軸を分けている。 | [JFS](https://www.jisf.or.jp/business/standard/jfs/) [JEITA 電子部品部会](https://home.jeita.or.jp/ecb/about/part.html) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) |
| [advice] 外注先評価では、めっき種だけでなく前処理、膜厚、後処理、検査、ベーキング、排水/EHS 条件まで確認した方がよい。 | PRTR 手引き、ORIST、JCU が工程一連での確認を示している。 | [METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf) [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) |
| [fact] PCB/HDI の microvia reliability warning は、電子用途全般ではなく microvia-to-target plating reliability の文脈で読むべきである。 | IPC warning と IPC-6012F の対象範囲が PCB/rigid board qualification に置かれている。 | [IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high) [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed) |
| [temporal] 日本では `2022-04-01` に公共用水域の六価クロム環境基準が `0.05 mg/L` から `0.02 mg/L` に改正された。 | 環境省告示の改正日と数値。 | [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html) |
| [temporal] 日本の六価クロム測定法は `2024-02-05` 公布、`2024-04-01` 施行で JIS K 0102-3 ベースに改められた。 | 環境省の公布日、施行日、JIS K0102-3 記載。 | [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html) |
| [regulatory] 日本の一般排水基準では六価クロム化合物は `0.2 mg Cr(VI)/L` と整理されている。 | 環境省の一般排水基準一覧。 | [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html) |
| [regulatory] `2024-12-11` 時点の暫定排水基準延長対象は亜鉛の電気めっき業で、六価クロムの暫定基準とは確認できない。 | 環境省の延長告示が対象業種を明示している。 | [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html) |
| [regulatory] OSHA の作業者ばく露に関する Chromium(VI) standard は `5 µg/m3` の 8-hour TWA を PEL としている。 | OSHA 本文に PEL を明記。 | [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) |
| [regulatory] EU RoHS は含有制限、REACH Annex XVII の nickel は主に放出条件でみる。 | EC と ECHA の公式説明が異なるロジックを採る。 | [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) |
| [fact] EPA は electroplating effluent guidelines と chromium finishing questionnaire を通じて、排水/EHS と chrome finishing/PFAS 文脈を別々の regulatory track として扱っている。 | effluent guidelines と questionnaire の対象が分かれている。 | [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines) [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire) |

## 4. 論点別の分析

### 4.1 方式ごとの比較ポイント

| 方式 | 形成のしかた | 強み | 向いている例 | 主な注意点 |
| --- | --- | --- | --- | --- |
| 電気めっき | 電流で金属を析出させる | 導電、接触、耐食、外観、量産性の調整幅が広い | コネクタ、機械部品、装飾、一般部品 | 前処理、膜厚分布、水素脆化を外せない。[表面技術協会](https://mekki.sfj.or.jp/) [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) |
| 無電解めっき | 化学還元で析出させる | 複雑形状でも比較的均一、電流分布に依らない | 無電解 Ni-P、電子部品、機能性表面 | 浴管理、析出速度、りん含有率、はんだ付け性や熱処理条件の確認が重要。[Nickel Institute](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/) [Nickel Plating Handbook](https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/) [ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) |
| 溶融めっき | 溶融金属浴に浸漬して被覆する | 厚い防食層、鋼材用途に強い | 建材、自動車用鋼板、鋼構造物 | 鋼板・鋼材中心で、湿式めっきと同じ比較軸で語らない方が安全。[日本鉄鋼連盟](https://www.jisf.or.jp/business/tech/aen/index.html) [ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) |
| 乾式/真空系表面処理 | 蒸着、スパッタ等で薄膜形成 | 微細・高機能薄膜、半導体周辺で有効 | 半導体、真空プロセス用途 | 広義の表面処理としては近いが、狭義の湿式めっきとは工程・設備・規制軸が違う。[ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [JEITA/ITRS 2007](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf) |

方式名から入るより、「基材は何か」「防食か接点か実装か」「厚めの防食層が必要か、薄い機能層でよいか」を先に決めた方が比較しやすいです。[ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [Nickel Plating Handbook](https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/)

### 4.2 用途別・産業別に何が違うか

- 自動車では、防食、耐久、量産安定性、サプライヤー管理が中心です。鋼板系では溶融亜鉛めっきや関連鋼板規格が強く、締結部品やばね材では水素脆化対策を外せません。[JFS](https://www.jisf.or.jp/business/standard/jfs/) [日本鉄鋼連盟](https://www.jisf.or.jp/business/tech/aen/index.html) [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [ASTM B849](https://store.astm.org/Standards/B849.htm) [ASTM F519](https://store.astm.org/f0519-17a.html)
- 電子部品やコネクタでは、接触抵抗、耐食、はんだ付け性、信頼性試験の条件が先に来ます。JEITA の信頼性評価観点は、用途別の試験や環境条件を意識させる材料として有用です。[表面技術協会](https://mekki.sfj.or.jp/) [JEITA 電子部品部会](https://home.jeita.or.jp/ecb/about/part.html) [JEITA 信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)
- PCB/HDI では、OSP、ENIG、ENEPIG、IAg、ISn、HASL などの surface finish を、実装条件、微細配線、接点利用の有無と一緒に見ます。ENIG は便利ですが万能ではなく、finish だけで microvia 問題が解けるわけでもありません。[IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed) [IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 半導体周辺や先端パッケージングでは、公開資料の範囲では finer pitch と高密度化に合わせて finish と配線・接続の同時最適化が重要です。ここは一般的な機械部品めっきの延長ではなく、JEITA/ITRS 系の実装・パッケージ議論に寄せて見る方が自然です。[JEITA/ITRS 2007](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- 建材や鋼板では、外観よりも長期防食、耐候、保守性、適用環境が強い判断軸になります。塗装亜鉛系めっき鋼板のように、後工程と一体で見た方がよい分野です。[ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [日本鉄鋼連盟](https://www.jisf.or.jp/business/tech/aen/index.html) [塗装亜鉛系めっき鋼板の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)
- 装飾用途でも、公開資料の範囲では bright/decorative plating と実用的な耐食・外観維持が一緒に語られます。装飾でも前処理と耐食評価を軽く見ない方が安全です。[ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [表面技術協会](https://mekki.sfj.or.jp/)

### 4.3 工程・設備・外注先を見るポイント

- まず前処理です。脱脂、酸洗、活性化のどこかが弱いと、後段で密着不良、ピット、ブリスター、膜厚不均一が出やすくなります。[ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [表面技術協会](https://mekki.sfj.or.jp/)
- 次に浴管理です。無電解 Ni-P のような化学浴では、浴組成、析出速度、りん含有率、熱処理条件が性能に効きます。公開資料の範囲では、化学浴は「均一だから楽」ではなく「管理条件が別軸で重い」と見た方が安全です。[Nickel Institute](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/) [Nickel Plating Handbook](https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/) [ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08)
- 高強度鋼、ばね材、締結部品では、めっき後ベーキングの有無と試験条件を確認しないと、水素脆化の議論が抜けます。[JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [ASTM B849](https://store.astm.org/Standards/B849.htm) [ASTM F519](https://store.astm.org/f0519-17a.html)
- PCB/HDI では、finish の種類だけでなく、穴埋め、銅めっき、実装、qualification を分けずに確認した方が安全です。microvia warning を読むときも同じです。[IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) [IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 外注先評価では、めっき種、膜厚、後処理、検査、規格適合、排水処理、作業者ばく露管理まで含めて確認する必要があります。PRTR や排水対応は工程の周辺論点ではなく、量産可否に効く本体条件です。[METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf) [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html) [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)

### 4.4 誤解しやすい点と例外

- 「めっきは装飾中心」は誤解です。機能用途の説明を抜くと、自動車、電子、PCB、接点の議論が全部薄くなります。[表面技術協会](https://mekki.sfj.or.jp/) [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)
- 「公共用水域向け排水基準」と「下水道への排除基準」は同じではありません。report では公共用水域/下水道を分けて書く必要があります。[環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html) [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)
- 「六価クロムに暫定排水基準がある」と一括で言うのも危険です。今回確認できた現行一次情報では、`2024-12-11` 時点の暫定排水基準延長対象は亜鉛の電気めっき業です。[環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- 「microvia の警告」は電子一般ではなく、PCB/HDI の限定文脈です。電子部品一般の finish 議論へそのまま広げない方が安全です。[IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high) [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
- 「RoHS と REACH は同じ材料規制」でもありません。RoHS は含有制限、REACH Annex XVII の nickel は主に release 条件です。[European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)

### 4.5 いま変わっている制度・市場・技術

- 日本の六価クロム関連では、`2022-04-01` に環境基準が改正され、`2024-02-05` 公布・`2024-04-01` 施行で測定法も改められました。report では改正日と施行日を分けて書くべきです。[環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html) [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
- `2024-12-11` の暫定排水基準延長は、少なくとも今回確認した official source では亜鉛の電気めっき業が対象です。六価クロムの暫定基準として書くと誤りやすいです。[環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- 米国では OSHA が Chromium(VI) ばく露、EPA が electroplating effluent guidelines と chrome finishing 文脈を別トラックで扱っています。PFAS も chrome plating の fume suppressant 文脈で見られており、単に「クロム工程だから PFAS」ではなく、用途と薬剤文脈を限定して読む必要があります。[OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines) [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
- EU 側では、RoHS の hexavalent chromium と REACH Annex XVII の nickel release 条件を別々に確認する必要があります。ここは国・制度・製品カテゴリで話が分かれます。[European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)

### 4.6 実務判断に効くコストと品質の勘所

- 最安の表面処理を選ぶより、再加工、歩留まり、field failure、EHS 対応コストまで見た方が実務では安くなることが多いです。[ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf)
- PCB では finish の単価差だけでなく、実装条件、ぬれ性、接点利用、qualification を一緒に見ないと比較を誤りやすいです。[IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
- 公開資料の範囲では、自社ラインと専業めっき会社では最適化対象が違います。自社ラインは製品統合、専業めっき会社は量産性や浴安定に寄りやすく、薬品/装置メーカーは標準プロセス側の最適化を示しやすいです。[METI](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf) [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [JEITA 信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)

### 4.7 見落とすと危険なドメイン固有リスク

- 前処理不良:
  後段の密着不良、ピット、ブリスター、膜厚不均一に直結します。[ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf)
- 水素脆化:
  高強度鋼、ばね材、締結部品ではベーキングと試験条件の確認が必須です。[JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [ASTM B849](https://store.astm.org/Standards/B849.htm) [ASTM F519](https://store.astm.org/f0519-17a.html)
- 接触抵抗とはんだ付け性:
  コネクタや PCB finish は同じではなく、接点利用か実装中心かで見方が変わります。[JEITA 信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- microvia 潜在不良:
  PCB/HDI 文脈に限定して重く見るべきリスクで、電子一般へ広げすぎない方が安全です。[IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high) [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
- 排水・ばく露:
  製品性能の良し悪しとは別に、量産可否を止めるリスクです。[環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html) [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- RoHS / REACH / nickel release:
  含有量と放出条件を混同すると説明も設計判断も崩れます。[European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)

## 5. 判断のために確認すべきことと追加調査

### 5.1 実務チェックリスト

| 判断場面 | 確認すること | なぜ重要か | 失敗した場合のリスク | 根拠または確認先 |
| --- | --- | --- | --- | --- |
| 方式を選ぶ | 基材、要求性能、使用環境、厚み要求をまず固定する | 同じ「めっき」でも比較軸が違うため | 不適切な方式比較、過剰品質、性能不足 | [ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) |
| 外注先を選ぶ | 前処理、膜厚、後処理、検査、ベーキング条件を確認する | めっき種だけでは品質が決まらないため | 密着不良、水素脆化、再加工増加 | [ORIST](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) |
| PCB finish を選ぶ | finish と microvia/実装条件を分けずに確認する | finish 単体比較では不十分だから | field failure、実装不良、過大一般化 | [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed) |
| EHS を見る | 公共用水域か下水道か、六価クロムか nickel/release かを分ける | 規制ロジックが制度ごとに違うため | 誤説明、許認可/運用ミス | [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html) [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html) [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) |
| 高強度鋼に使う | 水素脆化対策とベーキング条件を確認する | 遅れ破壊リスクがあるため | 重大破損、事故、責任問題 | [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [ASTM B849](https://store.astm.org/Standards/B849.htm) [ASTM F519](https://store.astm.org/f0519-17a.html) |
| コストを比較する | 単価だけでなく歩留まり、再加工、field failure、EHS 対応費を含める | 実際の総コストは後工程で決まりやすいため | 見かけ安価だが総コスト高 | [METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) |

### 5.2 追加で確認したい主張と調査の向き

- 個別製品の膜厚値、合否判定、顧客固有規格は、ASTM/JIS/IPC や顧客図面に降りて確認した方が安全です。[ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- 下水道接続の実務判断では、自治体・下水道管理者の排除基準や受入条件に加え、公共用水域向け基準との違いも別途確認すべきです。[国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html) [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
- ENIG/ENEPIG、microvia、RDL のような細部は、製品カテゴリ別の IPC/JEITA/顧客規格へ進んだ方が安全です。[IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf) [JEITA/ITRS 2007](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf)

### 5.3 不確実性と追加調査

- 今回は共通論点の整理を優先しており、個別の JIS / ASTM / IPC 要求値や顧客図面ベースの受入規格は、案件別に追加確認した方が安全です。[ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- vendor や industry association の資料は代表例として使っているため、個別ラインや個別製品へ一般化する前に、該当規格と実工程を確認する必要があります。[METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf) [表面技術協会](https://mekki.sfj.or.jp/)
- 日本の下水道側条件、顧客固有の膜厚・試験条件、特定 finish の詳細比較は、自治体、管理者、顧客図面の三つで追加確認が必要です。[国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html) [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)

## 6. 主要ソース一覧

- [表面技術協会](https://mekki.sfj.or.jp/)
- [防錆・防食のための めっきの基礎知識（ORIST）](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)
- [ASTM Committee B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08)
- [Nickel Plating Handbook](https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/)
- [Properties and Applications of Electroless Nickel](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/)
- [日本鉄鋼連盟 亜鉛めっき鋼板](https://www.jisf.or.jp/business/tech/aen/index.html)
- [JFS](https://www.jisf.or.jp/business/standard/jfs/)
- [JEITA 電子部品部会](https://home.jeita.or.jp/ecb/about/part.html)
- [JEITA 信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)
- [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
- [IPC microvia warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- [JCU 表面処理技術資料](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf)
- [METI めっき用途分類](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf)
- [METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf)
- [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html)
- [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
- [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
- [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)
- [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
- [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
- [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en)
- [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
```

---

## FILE: `sources/search-results.tsv`

```text
query	title	url	snippet	published_at
めっき 表面技術協会 基礎	めっき部会｜表面技術協会	https://mekki.sfj.or.jp/	めっきとは何か、対象材料、電気的または化学的手法の概説。	
めっき 防食 基礎 ORIST PDF	防錆・防食のための めっきの基礎知識	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	防食めっき、膜厚、防錆挙動の基礎。	
plating ASTM B08 scope	ASTM Committee B08 Scope	https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08	電気めっき、無電解、浸せき、ホットディップ、拡散コーティング等の範囲。	
nickel plating handbook Nickel Institute	Nickel Plating Handbook	https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/	ニッケルめっきの用途、性能、工程管理の総説。	
electroless nickel properties applications	Properties and Applications of Electroless Nickel	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/	無電解ニッケルの特性と用途。	
溶融亜鉛めっき 日本鉄鋼連盟	日本鉄鋼連盟 亜鉛めっき鋼板	https://www.jisf.or.jp/business/tech/aen/index.html	溶融亜鉛めっき鋼板の基礎と用途。	
JFS 自動車 防錆 規格	JFS	https://www.jisf.or.jp/business/standard/jfs/	自動車向け防錆鋼板規格の紹介。	
JEITA 電子部品 部会	JEITA 電子部品部会	https://home.jeita.or.jp/ecb/about/part.html	電子部品分野の対象範囲と構成。	
JEITA 信頼性評価 ガイド	JEITA 信頼性評価ガイド	https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	電子部品の信頼性評価で確認する観点。	
IPC 4552 ENIG	IPC-4552	https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf	ENIG の要求事項、膜厚、品質評価。	
IPC 6012F rigid printed boards	IPC-6012F release	https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	リジッド基板の qualification/performance 仕様改訂。	
IPC microvia reliability warning	IPC issues electronics industry warning on microvia reliability	https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	microvia reliability の業界警告。	
JCU 表面処理技術 事業戦略 PDF	表面処理技術から未来を創造する	https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	自動車、電子、建築など用途別の薬品・工程例。	
METI めっき 用途分類 PDF	METI	https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf	用途分類としてのめっき・表面処理。	
METI PRTR めっき 手引き	METI PRTR 手引き	https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf	PRTR 集計時のめっき工程の扱い。	
六価クロム 環境基準 2022 環境省	環境省 2022-04-01 告示	https://www.env.go.jp/press/110052.html	公共用水域の六価クロム環境基準改正。	2022-04-01
六価クロム 一般排水基準 環境省	環境省 一般排水基準	https://www.env.go.jp/water/impure/haisui.html	一般排水基準の一覧。	
JIS K0102-3 六価クロム 2024 環境省	環境省 2024-02-05 公布	https://www.env.go.jp/press/press_02720.html	六価クロム測定法見直し。	2024-02-05
暫定排水基準 電気めっき 2024 環境省	環境省 2024-12-11 暫定基準延長	https://www.env.go.jp/press/press_03960.html	亜鉛の電気めっき業の暫定排水基準延長。	2024-12-11
下水道 除害施設 六価クロム 国交省	国交省 除害施設	https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html	下水道への排除基準と除害施設の考え方。	
OSHA chromium VI 1910.1026	OSHA 29 CFR 1910.1026	https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	Chromium(VI) standard, PEL, action level, exposure control.	
EPA electroplating effluent guidelines	EPA Electroplating Effluent Guidelines	https://www.epa.gov/eg/electroplating-effluent-guidelines	40 CFR Part 413/433 の概要。	
EPA chromium finishing questionnaire PFAS	EPA Chromium Finishing Questionnaire	https://www.epa.gov/eg/chromium-finishing-questionnaire	chrome finishing facilities 向け質問票。	
RoHS directive official EU	European Commission RoHS Directive	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en	RoHS の official overview。	
ECHA Annex XVII nickel release	ECHA Annex XVII conditions	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	nickel release 条件と制限。	

```

---

## FILE: `sources/triaged-sources.tsv`

```text
rank_hint	score_hint	source_flags	dup_count	query_count	domain	title	canonical_url	queries	original_urls	sample_snippet	published_at
1	11	preferred-domain,institutional-domain,official-looking-path	1	1	env.go.jp	環境省 2022-04-01 告示	https://env.go.jp/press/110052.html	六価クロム 環境基準 2022 環境省	https://www.env.go.jp/press/110052.html	公共用水域の六価クロム環境基準改正。	2022-04-01
2	11	preferred-domain,institutional-domain,official-looking-path	1	1	env.go.jp	環境省 2024-02-05 公布	https://env.go.jp/press/press_02720.html	JIS K0102-3 六価クロム 2024 環境省	https://www.env.go.jp/press/press_02720.html	六価クロム測定法見直し。	2024-02-05
3	11	preferred-domain,institutional-domain,official-looking-path	1	1	env.go.jp	環境省 2024-12-11 暫定基準延長	https://env.go.jp/press/press_03960.html	暫定排水基準 電気めっき 2024 環境省	https://www.env.go.jp/press/press_03960.html	亜鉛の電気めっき業の暫定排水基準延長。	2024-12-11
4	11	preferred-domain,institutional-domain,pdf	1	1	meti.go.jp	METI	https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf	METI めっき 用途分類 PDF	https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf	用途分類としてのめっき・表面処理。	
5	11	preferred-domain,institutional-domain,pdf	1	1	meti.go.jp	METI PRTR 手引き	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf	METI PRTR めっき 手引き	https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf	PRTR 集計時のめっき工程の扱い。	
6	11	preferred-domain,institutional-domain,official-looking-path	1	1	osha.gov	OSHA 29 CFR 1910.1026	https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	OSHA chromium VI 1910.1026	https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	Chromium(VI) standard, PEL, action level, exposure control.	
7	9	preferred-domain,institutional-domain	1	1	env.go.jp	環境省 一般排水基準	https://env.go.jp/water/impure/haisui.html	六価クロム 一般排水基準 環境省	https://www.env.go.jp/water/impure/haisui.html	一般排水基準の一覧。	
8	9	preferred-domain,institutional-domain	1	1	epa.gov	EPA Chromium Finishing Questionnaire	https://epa.gov/eg/chromium-finishing-questionnaire	EPA chromium finishing questionnaire PFAS	https://www.epa.gov/eg/chromium-finishing-questionnaire	chrome finishing facilities 向け質問票。	
9	9	preferred-domain,institutional-domain	1	1	epa.gov	EPA Electroplating Effluent Guidelines	https://epa.gov/eg/electroplating-effluent-guidelines	EPA electroplating effluent guidelines	https://www.epa.gov/eg/electroplating-effluent-guidelines	40 CFR Part 413/433 の概要。	
10	9	preferred-domain,institutional-domain	1	1	mlit.go.jp	国交省 除害施設	https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html	下水道 除害施設 六価クロム 国交省	https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html	下水道への排除基準と除害施設の考え方。	
11	8	preferred-domain,pdf	1	1	home.jeita.or.jp	JEITA 信頼性評価ガイド	https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	JEITA 信頼性評価 ガイド	https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	電子部品の信頼性評価で確認する観点。	
12	8	preferred-domain,pdf	1	1	ipc.org	IPC-4552	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	IPC 4552 ENIG	https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf	ENIG の要求事項、膜厚、品質評価。	
13	8	preferred-domain,official-looking-path	1	1	jisf.or.jp	JFS	https://jisf.or.jp/business/standard/jfs	JFS 自動車 防錆 規格	https://www.jisf.or.jp/business/standard/jfs/	自動車向け防錆鋼板規格の紹介。	
14	8	preferred-domain,pdf	1	1	www2.orist.jp	防錆・防食のための めっきの基礎知識	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	めっき 防食 基礎 ORIST PDF	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	防食めっき、膜厚、防錆挙動の基礎。	
15	6	preferred-domain	1	1	echa.europa.eu	ECHA Annex XVII conditions	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	ECHA Annex XVII nickel release	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	nickel release 条件と制限。	
16	6	preferred-domain	1	1	environment.ec.europa.eu	European Commission RoHS Directive	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en	RoHS directive official EU	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en	RoHS の official overview。	
17	6	preferred-domain	1	1	home.jeita.or.jp	JEITA 電子部品部会	https://home.jeita.or.jp/ecb/about/part.html	JEITA 電子部品 部会	https://home.jeita.or.jp/ecb/about/part.html	電子部品分野の対象範囲と構成。	
18	6	preferred-domain	1	1	ipc.org	IPC issues electronics industry warning on microvia reliability	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	IPC microvia reliability warning	https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	microvia reliability の業界警告。	
19	6	preferred-domain	1	1	jisf.or.jp	日本鉄鋼連盟 亜鉛めっき鋼板	https://jisf.or.jp/business/tech/aen/index.html	溶融亜鉛めっき 日本鉄鋼連盟	https://www.jisf.or.jp/business/tech/aen/index.html	溶融亜鉛めっき鋼板の基礎と用途。	
20	6	preferred-domain	1	1	mekki.sfj.or.jp	めっき部会｜表面技術協会	https://mekki.sfj.or.jp/	めっき 表面技術協会 基礎	https://mekki.sfj.or.jp/	めっきとは何か、対象材料、電気的または化学的手法の概説。	
21	6	preferred-domain	1	1	nickelinstitute.org	Nickel Plating Handbook	https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en	nickel plating handbook Nickel Institute	https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/	ニッケルめっきの用途、性能、工程管理の総説。	
22	6	preferred-domain	1	1	nickelinstitute.org	Properties and Applications of Electroless Nickel	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081	electroless nickel properties applications	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/	無電解ニッケルの特性と用途。	
23	2	pdf	1	1	jcu-i.com	表面処理技術から未来を創造する	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	JCU 表面処理技術 事業戦略 PDF	https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	自動車、電子、建築など用途別の薬品・工程例。	
24	0	neutral	1	1	astm.org	ASTM Committee B08 Scope	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	plating ASTM B08 scope	https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08	電気めっき、無電解、浸せき、ホットディップ、拡散コーティング等の範囲。	
25	0	neutral	1	1	electronics.org	IPC-6012F release	https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	IPC 6012F rigid printed boards	https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	リジッド基板の qualification/performance 仕様改訂。	
```

---

## FILE: `sources/deep-read-queue.tsv`

```text
priority	status	reason	title	url	notes_file
1	read	regulatory date and limit	環境省 2022-04-01 告示	https://www.env.go.jp/press/110052.html	notes/subagent-regulatory-ehs.md
1	read	regulatory current limit	環境省 一般排水基準	https://www.env.go.jp/water/impure/haisui.html	notes/subagent-regulatory-ehs.md
1	read	regulatory method revision	環境省 2024-02-05 公布	https://www.env.go.jp/press/press_02720.html	notes/subagent-regulatory-ehs.md
1	read	regulatory temporary standard	環境省 2024-12-11 暫定基準延長	https://www.env.go.jp/press/press_03960.html	notes/subagent-regulatory-ehs.md
1	read	sewer distinction	国交省 除害施設	https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html	notes/subagent-regulatory-ehs.md
1	read	occupational exposure	OSHA 29 CFR 1910.1026	https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	notes/subagent-regulatory-ehs.md
1	read	us wastewater rule	EPA Electroplating Effluent Guidelines	https://www.epa.gov/eg/electroplating-effluent-guidelines	notes/subagent-regulatory-ehs.md
2	read	pfas relation	EPA Chromium Finishing Questionnaire	https://www.epa.gov/eg/chromium-finishing-questionnaire	notes/subagent-regulatory-ehs.md
2	read	rohs overview	European Commission RoHS Directive	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en	notes/subagent-regulatory-ehs.md
2	read	reach nickel release	ECHA Annex XVII conditions	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	notes/subagent-regulatory-ehs.md
1	read	japanese basics	めっき部会｜表面技術協会	https://mekki.sfj.or.jp/	notes/subagent-tech-foundations.md
1	read	corrosion basics	防錆・防食のための めっきの基礎知識	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	notes/subagent-tech-foundations.md
2	read	technical scope	ASTM Committee B08 Scope	https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08	notes/subagent-tech-foundations.md
2	read	electroless nickel	Properties and Applications of Electroless Nickel	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/	notes/subagent-tech-foundations.md
2	read	pcb finish spec	IPC-4552	https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf	notes/subagent-tech-foundations.md
2	read	microvia warning	IPC issues electronics industry warning on microvia reliability	https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	notes/subagent-tech-foundations.md
2	read	industry use cases	JCU 表面処理技術資料	https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	notes/subagent-applications.md
2	read	automotive corrosion use	日本鉄鋼連盟 亜鉛めっき鋼板	https://www.jisf.or.jp/business/tech/aen/index.html	notes/subagent-applications.md
2	read	automotive spec	JFS	https://www.jisf.or.jp/business/standard/jfs/	notes/subagent-applications.md
2	read	component reliability	JEITA 信頼性評価ガイド	https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	notes/subagent-applications.md
2	read	rigid board qualification	IPC-6012F release	https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	notes/subagent-applications.md
2	read	process classification	METI	https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf	notes/subagent-applications.md

```

---

## FILE: `sources/citation-ledger.tsv`

```text
source_url	domain	citation_instances	sections	leaf_sections	section_citation_counts	is_primary	source_role	title	source_flags
https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	ipc.org	16	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.2 用途別・産業別に何が違うか | ### 4.3 工程・設備・外注先を見るポイント | ### 4.6 実務判断に効くコストと品質の勘所 | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト | ### 5.2 追加で確認したい主張と調査の向き | ### 5.3 不確実性と追加調査	"{""## 1. 要約"":2,""## 2. 主要な発見"":2,""## 3. 主要な根拠と出典"":1,""### 4.2 用途別・産業別に何が違うか"":2,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.6 実務判断に効くコストと品質の勘所"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1,""### 5.1 実務チェックリスト"":2,""### 5.2 追加で確認したい主張と調査の向き"":2,""### 5.3 不確実性と追加調査"":2}"	true	standards_body	IPC-4552	preferred-domain,pdf
https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	www2.orist.jp	15	1. 要約 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 1. 要約 | ## 3. 主要な根拠と出典 | ### 4.1 方式ごとの比較ポイント | ### 4.2 用途別・産業別に何が違うか | ### 4.3 工程・設備・外注先を見るポイント | ### 4.4 誤解しやすい点と例外 | ### 4.6 実務判断に効くコストと品質の勘所 | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト	"{""## 1. 要約"":2,""## 3. 主要な根拠と出典"":2,""### 4.1 方式ごとの比較ポイント"":2,""### 4.2 用途別・産業別に何が違うか"":3,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.4 誤解しやすい点と例外"":1,""### 4.6 実務判断に効くコストと品質の勘所"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1,""### 5.1 実務チェックリスト"":2}"	true	government_context	防錆・防食のための めっきの基礎知識	preferred-domain,pdf
https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	astm.org	13	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.1 方式ごとの比較ポイント | ### 4.3 工程・設備・外注先を見るポイント | ### 5.1 実務チェックリスト | ### 5.2 追加で確認したい主張と調査の向き | ### 5.3 不確実性と追加調査	"{""## 1. 要約"":3,""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":2,""### 4.1 方式ごとの比較ポイント"":3,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 5.1 実務チェックリスト"":1,""### 5.2 追加で確認したい主張と調査の向き"":1,""### 5.3 不確実性と追加調査"":1}"	true	standards_body	ASTM Committee B08 Scope	neutral
https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	jcu-i.com	10	2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.2 用途別・産業別に何が違うか | ### 4.3 工程・設備・外注先を見るポイント | ### 4.6 実務判断に効くコストと品質の勘所 | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト	"{""## 2. 主要な発見"":2,""## 3. 主要な根拠と出典"":1,""### 4.2 用途別・産業別に何が違うか"":1,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.6 実務判断に効くコストと品質の勘所"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":2,""### 5.1 実務チェックリスト"":2}"	false	vendor_first_party	表面処理技術から未来を創造する	pdf
https://env.go.jp/water/impure/haisui.html	env.go.jp	8	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.3 工程・設備・外注先を見るポイント | ### 4.4 誤解しやすい点と例外 | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト | ### 5.2 追加で確認したい主張と調査の向き	"{""## 1. 要約"":1,""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.4 誤解しやすい点と例外"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1,""### 5.1 実務チェックリスト"":1,""### 5.2 追加で確認したい主張と調査の向き"":1}"	true	official_regulator	環境省 一般排水基準	preferred-domain,institutional-domain
https://mekki.sfj.or.jp/	mekki.sfj.or.jp	8	1. 要約 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 1. 要約 | ## 3. 主要な根拠と出典 | ### 4.1 方式ごとの比較ポイント | ### 4.2 用途別・産業別に何が違うか | ### 4.3 工程・設備・外注先を見るポイント | ### 4.4 誤解しやすい点と例外 | ### 5.3 不確実性と追加調査	"{""## 1. 要約"":1,""## 3. 主要な根拠と出典"":1,""### 4.1 方式ごとの比較ポイント"":1,""### 4.2 用途別・産業別に何が違うか"":2,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.4 誤解しやすい点と例外"":1,""### 5.3 不確実性と追加調査"":1}"	true	professional_body	めっき部会｜表面技術協会	preferred-domain
https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	echa.europa.eu	7	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.4 誤解しやすい点と例外 | ### 4.5 いま変わっている制度・市場・技術 | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト	"{""## 1. 要約"":1,""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.4 誤解しやすい点と例外"":1,""### 4.5 いま変わっている制度・市場・技術"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1,""### 5.1 実務チェックリスト"":1}"	true	legal_text	ECHA Annex XVII conditions	preferred-domain
https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	electronics.org	7	2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.2 用途別・産業別に何が違うか | ### 4.4 誤解しやすい点と例外 | ### 4.6 実務判断に効くコストと品質の勘所 | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト	"{""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.2 用途別・産業別に何が違うか"":1,""### 4.4 誤解しやすい点と例外"":1,""### 4.6 実務判断に効くコストと品質の勘所"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1,""### 5.1 実務チェックリスト"":1}"	true	standard_or_code	IPC-6012F release	neutral
https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	ipc.org	7	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.2 用途別・産業別に何が違うか | ### 4.3 工程・設備・外注先を見るポイント | ### 4.4 誤解しやすい点と例外 | ### 4.7 見落とすと危険なドメイン固有リスク	"{""## 1. 要約"":1,""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.2 用途別・産業別に何が違うか"":1,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.4 誤解しやすい点と例外"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1}"	true	standards_body	IPC issues electronics industry warning on microvia reliability	preferred-domain
https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en	environment.ec.europa.eu	6	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.4 誤解しやすい点と例外 | ### 4.5 いま変わっている制度・市場・技術 | ### 4.7 見落とすと危険なドメイン固有リスク	"{""## 1. 要約"":1,""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.4 誤解しやすい点と例外"":1,""### 4.5 いま変わっている制度・市場・技術"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1}"	true	legal_text	European Commission RoHS Directive	preferred-domain
https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf	meti.go.jp	6	2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.3 工程・設備・外注先を見るポイント | ### 4.6 実務判断に効くコストと品質の勘所 | ### 5.1 実務チェックリスト | ### 5.3 不確実性と追加調査	"{""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.6 実務判断に効くコストと品質の勘所"":1,""### 5.1 実務チェックリスト"":1,""### 5.3 不確実性と追加調査"":1}"	true	legal_text	METI PRTR 手引き	preferred-domain,institutional-domain,pdf
https://jisf.or.jp/business/tech/aen/index.html	jisf.or.jp	5	1. 要約 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 1. 要約 | ## 3. 主要な根拠と出典 | ### 4.1 方式ごとの比較ポイント | ### 4.2 用途別・産業別に何が違うか	"{""## 1. 要約"":1,""## 3. 主要な根拠と出典"":1,""### 4.1 方式ごとの比較ポイント"":1,""### 4.2 用途別・産業別に何が違うか"":2}"	false	industry_association	日本鉄鋼連盟 亜鉛めっき鋼板	preferred-domain
https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	osha.gov	5	1. 要約 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 1. 要約 | ## 3. 主要な根拠と出典 | ### 4.3 工程・設備・外注先を見るポイント | ### 4.5 いま変わっている制度・市場・技術 | ### 4.7 見落とすと危険なドメイン固有リスク	"{""## 1. 要約"":1,""## 3. 主要な根拠と出典"":1,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.5 いま変わっている制度・市場・技術"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1}"	true	legal_text	OSHA 29 CFR 1910.1026	preferred-domain,institutional-domain,official-looking-path
https://store.astm.org/Standards/B849.htm	store.astm.org	5	2. 主要な発見 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 2. 主要な発見 | ### 4.2 用途別・産業別に何が違うか | ### 4.3 工程・設備・外注先を見るポイント | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト	"{""## 2. 主要な発見"":1,""### 4.2 用途別・産業別に何が違うか"":1,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1,""### 5.1 実務チェックリスト"":1}"	true	standard_or_code	ASTM B849	
https://store.astm.org/f0519-17a.html	store.astm.org	5	2. 主要な発見 | 4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	## 2. 主要な発見 | ### 4.2 用途別・産業別に何が違うか | ### 4.3 工程・設備・外注先を見るポイント | ### 4.7 見落とすと危険なドメイン固有リスク | ### 5.1 実務チェックリスト	"{""## 2. 主要な発見"":1,""### 4.2 用途別・産業別に何が違うか"":1,""### 4.3 工程・設備・外注先を見るポイント"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1,""### 5.1 実務チェックリスト"":1}"	true	standards_body	ASTM F519	
https://env.go.jp/press/110052.html	env.go.jp	4	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.5 いま変わっている制度・市場・技術	"{""## 1. 要約"":1,""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.5 いま変わっている制度・市場・技術"":1}"	true	official_regulator	環境省 2022-04-01 告示	preferred-domain,institutional-domain,official-looking-path
https://env.go.jp/press/press_02720.html	env.go.jp	4	1. 要約 | 2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 1. 要約 | ## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.5 いま変わっている制度・市場・技術	"{""## 1. 要約"":1,""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.5 いま変わっている制度・市場・技術"":1}"	true	official_regulator	環境省 2024-02-05 公布	preferred-domain,institutional-domain,official-looking-path
https://env.go.jp/press/press_03960.html	env.go.jp	4	2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.4 誤解しやすい点と例外 | ### 4.5 いま変わっている制度・市場・技術	"{""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.4 誤解しやすい点と例外"":1,""### 4.5 いま変わっている制度・市場・技術"":1}"	true	official_regulator	環境省 2024-12-11 暫定基準延長	preferred-domain,institutional-domain,official-looking-path
https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	home.jeita.or.jp	4	2. 主要な発見 | 4. 論点別の分析	## 2. 主要な発見 | ### 4.2 用途別・産業別に何が違うか | ### 4.6 実務判断に効くコストと品質の勘所 | ### 4.7 見落とすと危険なドメイン固有リスク	"{""## 2. 主要な発見"":1,""### 4.2 用途別・産業別に何が違うか"":1,""### 4.6 実務判断に効くコストと品質の勘所"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1}"	false	industry_association	JEITA 信頼性評価ガイド	preferred-domain,pdf
https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html	mlit.go.jp	4	4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	### 4.4 誤解しやすい点と例外 | ### 5.1 実務チェックリスト | ### 5.2 追加で確認したい主張と調査の向き | ### 5.3 不確実性と追加調査	"{""### 4.4 誤解しやすい点と例外"":1,""### 5.1 実務チェックリスト"":1,""### 5.2 追加で確認したい主張と調査の向き"":1,""### 5.3 不確実性と追加調査"":1}"	true	government_context	国交省 除害施設	preferred-domain,institutional-domain
https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en	nickelinstitute.org	4	2. 主要な発見 | 4. 論点別の分析	## 2. 主要な発見 | ### 4.1 方式ごとの比較ポイント | ### 4.3 工程・設備・外注先を見るポイント	"{""## 2. 主要な発見"":1,""### 4.1 方式ごとの比較ポイント"":2,""### 4.3 工程・設備・外注先を見るポイント"":1}"	false	industry_association	Nickel Plating Handbook	preferred-domain
https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081	nickelinstitute.org	4	1. 要約 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 1. 要約 | ## 3. 主要な根拠と出典 | ### 4.1 方式ごとの比較ポイント | ### 4.3 工程・設備・外注先を見るポイント	"{""## 1. 要約"":1,""## 3. 主要な根拠と出典"":1,""### 4.1 方式ごとの比較ポイント"":1,""### 4.3 工程・設備・外注先を見るポイント"":1}"	false	industry_association	Properties and Applications of Electroless Nickel	preferred-domain
https://epa.gov/eg/electroplating-effluent-guidelines	epa.gov	3	3. 主要な根拠と出典 | 4. 論点別の分析	## 3. 主要な根拠と出典 | ### 4.5 いま変わっている制度・市場・技術 | ### 4.7 見落とすと危険なドメイン固有リスク	"{""## 3. 主要な根拠と出典"":1,""### 4.5 いま変わっている制度・市場・技術"":1,""### 4.7 見落とすと危険なドメイン固有リスク"":1}"	true	official_regulator	EPA Electroplating Effluent Guidelines	preferred-domain,institutional-domain
https://home.jeita.or.jp/ecb/about/part.html	home.jeita.or.jp	3	2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.2 用途別・産業別に何が違うか	"{""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.2 用途別・産業別に何が違うか"":1}"	false	industry_association	JEITA 電子部品部会	preferred-domain
https://jisf.or.jp/business/standard/jfs	jisf.or.jp	3	2. 主要な発見 | 3. 主要な根拠と出典 | 4. 論点別の分析	## 2. 主要な発見 | ## 3. 主要な根拠と出典 | ### 4.2 用途別・産業別に何が違うか	"{""## 2. 主要な発見"":1,""## 3. 主要な根拠と出典"":1,""### 4.2 用途別・産業別に何が違うか"":1}"	false	industry_association	JFS	preferred-domain,official-looking-path
https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	semicon.jeita.or.jp	3	4. 論点別の分析 | 5. 判断のために確認すべきことと追加調査	### 4.1 方式ごとの比較ポイント | ### 4.2 用途別・産業別に何が違うか | ### 5.2 追加で確認したい主張と調査の向き	"{""### 4.1 方式ごとの比較ポイント"":1,""### 4.2 用途別・産業別に何が違うか"":1,""### 5.2 追加で確認したい主張と調査の向き"":1}"	false	industry_association	JEITA/ITRS 2007	
https://epa.gov/eg/chromium-finishing-questionnaire	epa.gov	2	3. 主要な根拠と出典 | 4. 論点別の分析	## 3. 主要な根拠と出典 | ### 4.5 いま変わっている制度・市場・技術	"{""## 3. 主要な根拠と出典"":1,""### 4.5 いま変わっている制度・市場・技術"":1}"	true	government_context	EPA Chromium Finishing Questionnaire	preferred-domain,institutional-domain
https://jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf	jisf.or.jp	1	4. 論点別の分析	### 4.2 用途別・産業別に何が違うか	"{""### 4.2 用途別・産業別に何が違うか"":1}"	false	industry_association	塗装亜鉛系めっき鋼板の手引き	
https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf	meti.go.jp	1	4. 論点別の分析	### 4.6 実務判断に効くコストと品質の勘所	"{""### 4.6 実務判断に効くコストと品質の勘所"":1}"	true	government_context	METI	preferred-domain,institutional-domain,pdf
```

---

## FILE: `sources/claim-ledger.tsv`

```text
claim_id	section	claim_kind	risk_level	claim_text	evidence_summary	evidence_urls	source_urls	source_domains	evidence_count	primary_source_count	source_role	confidence	status	required_fix	required_evidence_count	required_primary_count	gap_note	exact_date	jurisdiction	regulated_subject	scope	effective_date	transition_period	tone_guidance	tone_reason	caveat
claim-001	## 1. 要約	fact	high	めっきは装飾だけの話ではなく、実務では防食、導電、接触信頼性、はんだ付け性、拡散バリア、耐摩耗などの機能付与が中心です。表面技術協会 ORIST ASTM B08 Scope	inline citation context	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	mekki.sfj.or.jp | www2.orist.jp | astm.org	3	3	professional_body | government_context | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-002	## 1. 要約	advice	high	読み手が最初に切り分けるべきなのは「電気めっき」「無電解めっき」「溶融めっき」と、隣接する乾式表面処理を同じものとして扱わないことです。要求性能、基材、量産条件、規制対応がそれぞれ違います。ASTM B08 Scope 日本鉄鋼連盟 Nickel Institute	inline citation context	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://jisf.or.jp/business/tech/aen/index.html | https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://jisf.or.jp/business/tech/aen/index.html | https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081	astm.org | jisf.or.jp | nickelinstitute.org	3	1	standards_body | industry_association	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-003	## 1. 要約	fact	high	品質面で見落としやすいのは、前処理、膜厚不均一、密着不良、ピット/ブリスター、水素脆化、接触抵抗、はんだ付け性、PCB/HDI に限定される microvia reliability です。ORIST IPC-4552 IPC microvia warning	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	www2.orist.jp | ipc.org	3	3	government_context | standards_body	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	scope-limited claim
claim-004	## 1. 要約	temporal	high	規制面では、日本の六価クロム関連だけでも「環境基準」「一般排水基準」「測定法改正」「暫定排水基準」「公共用水域と下水道の区別」を分けて説明する必要があります。海外では OSHA の作業者ばく露、EPA の electroplating/chromium rules、EU の RoHS と REACH を混同しないことが重要です。環境省 2022-04-01 告示 環境省 一般排水基準 環境省 2024-02-05 公布 OSHA 29 CFR 1910.1026 European Commission RoHS Directive ECHA Annex XVII conditions	inline citation context	https://env.go.jp/press/110052.html | https://env.go.jp/water/impure/haisui.html | https://env.go.jp/press/press_02720.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/press/110052.html | https://env.go.jp/water/impure/haisui.html | https://env.go.jp/press/press_02720.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | osha.gov | environment.ec.europa.eu | echa.europa.eu	6	6	official_regulator | legal_text	0.95	ok		2	1		2022-04-01 | 2024-02-05	EU	hexavalent chromium	public water bodies	2022-04-01	temporary transitional measure	standard	official, legal, standards, academic, or public-context support is present	
claim-005	## 1. 要約	advice	medium	今回は個別製品の受入規格値や各社固有の工程窓ではなく、方式差、用途差、品質/EHS リスク、実務判断の共通論点を先に整理します。ASTM B08 Scope IPC-4552	inline citation context	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	astm.org | ipc.org	2	2	standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-006	## 2. 主要な発見	fact	medium	方式選定は「めっき種の名前」ではなく、基材、要求性能、使用環境、量産条件、EHS 条件から逆算した方が失敗しにくいです。ASTM B08 Scope Nickel Plating Handbook	inline citation context	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en	astm.org | nickelinstitute.org	2	1	standards_body | industry_association	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-007	## 2. 主要な発見	fact	high	自動車や建材では防食と耐久が先に来やすく、電子部品や PCB では接触抵抗、はんだ付け性、微細配線対応が先に来ます。同じ「めっき」でも評価軸が違います。JFS JEITA 電子部品部会 IPC-4552	inline citation context	https://jisf.or.jp/business/standard/jfs | https://home.jeita.or.jp/ecb/about/part.html | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://jisf.or.jp/business/standard/jfs | https://home.jeita.or.jp/ecb/about/part.html | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	jisf.or.jp | home.jeita.or.jp | ipc.org	3	1	industry_association | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-008	## 2. 主要な発見	advice	high	公開資料の範囲では、job plater、OEM の自社ライン、薬品メーカー、装置メーカー、規制当局、標準団体はそれぞれ見ている指標が違います。情報の立場を混ぜると判断を誤りやすいです。METI PRTR 手引き JCU 表面処理技術資料 JEITA 信頼性評価ガイド	inline citation context	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	meti.go.jp | jcu-i.com | home.jeita.or.jp	3	1	legal_text | vendor_first_party | industry_association	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-009	## 2. 主要な発見	advice	high	高強度鋼、ばね材、締結部品では、水素脆化とベーキング条件の確認を抜くと重大事故につながります。これは装飾用途の話ではありません。JCU 表面処理技術資料 ASTM B849 ASTM F519	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	jcu-i.com | store.astm.org	3	2	vendor_first_party | standard_or_code | standards_body	0.95	ok		2	1					high-strength steel components			standard	official, legal, standards, academic, or public-context support is present	
claim-010	## 2. 主要な発見	fact	high	PCB/HDI 文脈では、surface finish の選択と microvia reliability を別に考えず、finish、穴埋め、銅めっき、実装条件を一体で見た方が安全です。IPC-4552 IPC-6012F IPC microvia warning	inline citation context	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	ipc.org | electronics.org	3	3	standards_body | standard_or_code	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	scope-limited claim
claim-011	## 2. 主要な発見	temporal	high	日本の六価クロムは、2022-04-01 の環境基準改正、2024-02-05 公布・2024-04-01 施行の測定法改正、一般排水基準 0.2 mg Cr(VI)/L を分けて理解する必要があります。環境省 2022-04-01 告示 環境省 2024-02-05 公布 環境省 一般排水基準	inline citation context	https://env.go.jp/press/110052.html | https://env.go.jp/press/press_02720.html | https://env.go.jp/water/impure/haisui.html	https://env.go.jp/press/110052.html | https://env.go.jp/press/press_02720.html | https://env.go.jp/water/impure/haisui.html	env.go.jp	3	3	official_regulator	0.95	ok		2	1		2022-04-01 | 2024-02-05 | 2024-04-01	Japan	hexavalent chromium		2022-04-01		standard	official, legal, standards, academic, or public-context support is present	
claim-012	## 2. 主要な発見	temporal	high	2024-12-11 時点の一次情報では、暫定排水基準の延長対象は亜鉛の電気めっき業であり、六価クロムの暫定基準をそのまま説明するのは不正確です。環境省 2024-12-11 暫定基準延長	inline citation context	https://env.go.jp/press/press_03960.html	https://env.go.jp/press/press_03960.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1		2024-12-11	Japan	hexavalent chromium		2024-12-11	temporary transitional measure	standard	official, legal, standards, academic, or public-context support is present	
claim-013	## 2. 主要な発見	regulatory	high	EU の RoHS は含有制限、REACH Annex XVII の nickel は主に放出条件で見るため、同じ「材料規制」として一括説明しない方が安全です。European Commission RoHS Directive ECHA Annex XVII conditions	inline citation context	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	environment.ec.europa.eu | echa.europa.eu	2	2	legal_text	0.95	ok		2	1			EU	hazardous substances in EEE	skin-contact release condition			standard	official, legal, standards, academic, or public-context support is present	
claim-014	## 3. 主要な根拠と出典	fact	high	めっきは装飾だけでなく、防食、導電、接触、はんだ付け性、拡散バリアなどの機能付与として広く使われる。	日本の学協会・公設試験機関・国際標準の範囲説明が、機能用途を一貫して示している。	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	mekki.sfj.or.jp | www2.orist.jp | astm.org	3	3	professional_body | government_context | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-015	## 3. 主要な根拠と出典	fact	low	電気めっき、無電解めっき、溶融めっきは形成機構も用途も違い、乾式表面処理は隣接概念として分けて扱う方が安全である。	ASTM B08 の範囲と JISF/Nickel Institute の用途説明が、方式差を別物として扱っている。	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://jisf.or.jp/business/tech/aen/index.html | https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://jisf.or.jp/business/tech/aen/index.html | https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081	astm.org | jisf.or.jp | nickelinstitute.org	3	1	standards_body | industry_association	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-016	## 3. 主要な根拠と出典	advice	high	自動車と建材は防食・耐久、電子部品と PCB は接触抵抗・はんだ付け性・微細配線対応を優先軸として見た方がよい。	JFS/JISF、JEITA、IPC が用途別の評価軸を分けている。	https://jisf.or.jp/business/standard/jfs | https://home.jeita.or.jp/ecb/about/part.html | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://jisf.or.jp/business/standard/jfs | https://home.jeita.or.jp/ecb/about/part.html | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	jisf.or.jp | home.jeita.or.jp | ipc.org	3	1	industry_association | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-017	## 3. 主要な根拠と出典	advice	high	外注先評価では、めっき種だけでなく前処理、膜厚、後処理、検査、ベーキング、排水/EHS 条件まで確認した方がよい。	PRTR 手引き、ORIST、JCU が工程一連での確認を示している。	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	meti.go.jp | www2.orist.jp | jcu-i.com	3	2	legal_text | government_context | vendor_first_party	0.95	ok		2	1			Japan	wastewater discharge				standard	official, legal, standards, academic, or public-context support is present	
claim-018	## 3. 主要な根拠と出典	fact	high	PCB/HDI の microvia reliability warning は、電子用途全般ではなく microvia-to-target plating reliability の文脈で読むべきである。	IPC warning と IPC-6012F の対象範囲が PCB/rigid board qualification に置かれている。	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	ipc.org | electronics.org	2	2	standards_body | standard_or_code	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	scope-limited claim
claim-019	## 3. 主要な根拠と出典	temporal	high	日本では 2022-04-01 に公共用水域の六価クロム環境基準が 0.05 mg/L から 0.02 mg/L に改正された。	環境省告示の改正日と数値。	https://env.go.jp/press/110052.html	https://env.go.jp/press/110052.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1		2022-04-01	Japan	hexavalent chromium	public water bodies	2022-04-01		standard	official, legal, standards, academic, or public-context support is present	
claim-020	## 3. 主要な根拠と出典	temporal	high	日本の六価クロム測定法は 2024-02-05 公布、2024-04-01 施行で JIS K 0102-3 ベースに改められた。	環境省の公布日、施行日、JIS K0102-3 記載。	https://env.go.jp/press/press_02720.html	https://env.go.jp/press/press_02720.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1		2024-02-05 | 2024-04-01	Japan	hexavalent chromium		2024-02-05		standard	official, legal, standards, academic, or public-context support is present	
claim-021	## 3. 主要な根拠と出典	regulatory	high	日本の一般排水基準では六価クロム化合物は 0.2 mg Cr(VI)/L と整理されている。	環境省の一般排水基準一覧。	https://env.go.jp/water/impure/haisui.html	https://env.go.jp/water/impure/haisui.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1			Japan	hexavalent chromium				standard	official, legal, standards, academic, or public-context support is present	
claim-022	## 3. 主要な根拠と出典	regulatory	high	2024-12-11 時点の暫定排水基準延長対象は亜鉛の電気めっき業で、六価クロムの暫定基準とは確認できない。	環境省の延長告示が対象業種を明示している。	https://env.go.jp/press/press_03960.html	https://env.go.jp/press/press_03960.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1		2024-12-11	Japan	hexavalent chromium		2024-12-11	temporary transitional measure	standard	official, legal, standards, academic, or public-context support is present	
claim-023	## 3. 主要な根拠と出典	regulatory	high	OSHA の作業者ばく露に関する Chromium(VI) standard は 5 µg/m3 の 8-hour TWA を PEL としている。	OSHA 本文に PEL を明記。	https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	osha.gov	1	1	legal_text	0.85	ok		2	1			United States	worker exposure				standard	official, legal, standards, academic, or public-context support is present	
claim-024	## 3. 主要な根拠と出典	regulatory	high	EU RoHS は含有制限、REACH Annex XVII の nickel は主に放出条件でみる。	EC と ECHA の公式説明が異なるロジックを採る。	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	environment.ec.europa.eu | echa.europa.eu	2	2	legal_text	0.95	ok		2	1			EU	hazardous substances in EEE	skin-contact release condition			standard	official, legal, standards, academic, or public-context support is present	
claim-025	## 3. 主要な根拠と出典	fact	high	EPA は electroplating effluent guidelines と chromium finishing questionnaire を通じて、排水/EHS と chrome finishing/PFAS 文脈を別々の regulatory track として扱っている。	effluent guidelines と questionnaire の対象が分かれている。	https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/eg/chromium-finishing-questionnaire	https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/eg/chromium-finishing-questionnaire	epa.gov	2	2	official_regulator | government_context	0.95	ok		2	1			United States	wastewater discharge				standard	official, legal, standards, academic, or public-context support is present	scope-limited claim
claim-026	### 4.1 方式ごとの比較ポイント	fact	low	電気めっき - 形成のしかた: 電流で金属を析出させる	table cell	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	mekki.sfj.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-027	### 4.1 方式ごとの比較ポイント	fact	low	電気めっき - 強み: 導電、接触、耐食、外観、量産性の調整幅が広い	table cell	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	mekki.sfj.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-028	### 4.1 方式ごとの比較ポイント	fact	low	電気めっき - 向いている例: コネクタ、機械部品、装飾、一般部品	table cell	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	mekki.sfj.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-029	### 4.1 方式ごとの比較ポイント	fact	high	電気めっき - 主な注意点: 前処理、膜厚分布、水素脆化を外せない。表面技術協会 ORIST	table cell	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	mekki.sfj.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-030	### 4.1 方式ごとの比較ポイント	fact	low	無電解めっき - 形成のしかた: 化学還元で析出させる	table cell	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	nickelinstitute.org | astm.org	3	1	industry_association | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-031	### 4.1 方式ごとの比較ポイント	fact	low	無電解めっき - 強み: 複雑形状でも比較的均一、電流分布に依らない	table cell	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	nickelinstitute.org | astm.org	3	1	industry_association | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-032	### 4.1 方式ごとの比較ポイント	fact	low	無電解めっき - 向いている例: 無電解 Ni-P、電子部品、機能性表面	table cell	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	nickelinstitute.org | astm.org	3	1	industry_association | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-033	### 4.1 方式ごとの比較ポイント	advice	high	無電解めっき - 主な注意点: 浴管理、析出速度、りん含有率、はんだ付け性や熱処理条件の確認が重要。Nickel Institute Nickel Plating Handbook ASTM B08 Scope	table cell	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	nickelinstitute.org | astm.org	3	1	industry_association | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-034	### 4.1 方式ごとの比較ポイント	fact	low	溶融めっき - 形成のしかた: 溶融金属浴に浸漬して被覆する	table cell	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	jisf.or.jp | astm.org	2	1	industry_association | standards_body	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-035	### 4.1 方式ごとの比較ポイント	fact	low	溶融めっき - 強み: 厚い防食層、鋼材用途に強い	table cell	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	jisf.or.jp | astm.org	2	1	industry_association | standards_body	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-036	### 4.1 方式ごとの比較ポイント	fact	low	溶融めっき - 向いている例: 建材、自動車用鋼板、鋼構造物	table cell	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	jisf.or.jp | astm.org	2	1	industry_association | standards_body	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-037	### 4.1 方式ごとの比較ポイント	fact	low	溶融めっき - 主な注意点: 鋼板・鋼材中心で、湿式めっきと同じ比較軸で語らない方が安全。日本鉄鋼連盟 ASTM B08 Scope	table cell	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://jisf.or.jp/business/tech/aen/index.html | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	jisf.or.jp | astm.org	2	1	industry_association | standards_body	0.85	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-038	### 4.1 方式ごとの比較ポイント	fact	low	乾式/真空系表面処理 - 形成のしかた: 蒸着、スパッタ等で薄膜形成	table cell	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	astm.org | semicon.jeita.or.jp	2	1	standards_body | industry_association	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-039	### 4.1 方式ごとの比較ポイント	fact	low	乾式/真空系表面処理 - 強み: 微細・高機能薄膜、半導体周辺で有効	table cell	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	astm.org | semicon.jeita.or.jp	2	1	standards_body | industry_association	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-040	### 4.1 方式ごとの比較ポイント	fact	low	乾式/真空系表面処理 - 向いている例: 半導体、真空プロセス用途	table cell	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	astm.org | semicon.jeita.or.jp	2	1	standards_body | industry_association	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-041	### 4.1 方式ごとの比較ポイント	fact	high	乾式/真空系表面処理 - 主な注意点: 広義の表面処理としては近いが、狭義の湿式めっきとは工程・設備・規制軸が違う。ASTM B08 Scope JEITA/ITRS 2007	table cell	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	astm.org | semicon.jeita.or.jp	2	1	standards_body | industry_association	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-042	### 4.1 方式ごとの比較ポイント	fact	low	方式名から入るより、「基材は何か」「防食か接点か実装か」「厚めの防食層が必要か、薄い機能層でよいか」を先に決めた方が比較しやすいです。ORIST Nickel Plating Handbook	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en	www2.orist.jp | nickelinstitute.org	2	1	government_context | industry_association	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-043	### 4.2 用途別・産業別に何が違うか	fact	high	自動車では、防食、耐久、量産安定性、サプライヤー管理が中心です。鋼板系では溶融亜鉛めっきや関連鋼板規格が強く、締結部品やばね材では水素脆化対策を外せません。JFS 日本鉄鋼連盟 ORIST JCU 表面処理技術資料 ASTM B849 ASTM F519	inline citation context	https://jisf.or.jp/business/standard/jfs | https://jisf.or.jp/business/tech/aen/index.html | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	https://jisf.or.jp/business/standard/jfs | https://jisf.or.jp/business/tech/aen/index.html | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	jisf.or.jp | www2.orist.jp | jcu-i.com | store.astm.org	6	3	industry_association | government_context | vendor_first_party | standard_or_code | standards_body	0.95	ok		2	1			Japan		high-strength steel components			standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-044	### 4.2 用途別・産業別に何が違うか	fact	high	電子部品やコネクタでは、接触抵抗、耐食、はんだ付け性、信頼性試験の条件が先に来ます。JEITA の信頼性評価観点は、用途別の試験や環境条件を意識させる材料として有用です。表面技術協会 JEITA 電子部品部会 JEITA 信頼性評価ガイド	inline citation context	https://mekki.sfj.or.jp/ | https://home.jeita.or.jp/ecb/about/part.html | https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	https://mekki.sfj.or.jp/ | https://home.jeita.or.jp/ecb/about/part.html | https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	mekki.sfj.or.jp | home.jeita.or.jp	3	1	professional_body | industry_association	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-045	### 4.2 用途別・産業別に何が違うか	fact	high	PCB/HDI では、OSP、ENIG、ENEPIG、IAg、ISn、HASL などの surface finish を、実装条件、微細配線、接点利用の有無と一緒に見ます。ENIG は便利ですが万能ではなく、finish だけで microvia 問題が解けるわけでもありません。IPC-4552 IPC-6012F IPC microvia warning	inline citation context	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	ipc.org | electronics.org	3	3	standards_body | standard_or_code	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	
claim-046	### 4.2 用途別・産業別に何が違うか	advice	medium	半導体周辺や先端パッケージングでは、公開資料の範囲では finer pitch と高密度化に合わせて finish と配線・接続の同時最適化が重要です。ここは一般的な機械部品めっきの延長ではなく、JEITA/ITRS 系の実装・パッケージ議論に寄せて見る方が自然です。JEITA/ITRS 2007 IPC-4552	inline citation context	https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	semicon.jeita.or.jp | ipc.org	2	1	industry_association | standards_body	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-047	### 4.2 用途別・産業別に何が違うか	advice	medium	建材や鋼板では、外観よりも長期防食、耐候、保守性、適用環境が強い判断軸になります。塗装亜鉛系めっき鋼板のように、後工程と一体で見た方がよい分野です。ORIST 日本鉄鋼連盟 塗装亜鉛系めっき鋼板の手引き	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jisf.or.jp/business/tech/aen/index.html | https://jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jisf.or.jp/business/tech/aen/index.html | https://jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf	www2.orist.jp | jisf.or.jp	3	1	government_context | industry_association	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-048	### 4.2 用途別・産業別に何が違うか	fact	low	装飾用途でも、公開資料の範囲では bright/decorative plating と実用的な耐食・外観維持が一緒に語られます。装飾でも前処理と耐食評価を軽く見ない方が安全です。ORIST 表面技術協会	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://mekki.sfj.or.jp/	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://mekki.sfj.or.jp/	www2.orist.jp | mekki.sfj.or.jp	2	2	government_context | professional_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-049	### 4.3 工程・設備・外注先を見るポイント	advice	high	まず前処理です。脱脂、酸洗、活性化のどこかが弱いと、後段で密着不良、ピット、ブリスター、膜厚不均一が出やすくなります。ORIST 表面技術協会	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://mekki.sfj.or.jp/	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://mekki.sfj.or.jp/	www2.orist.jp | mekki.sfj.or.jp	2	2	government_context | professional_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-050	### 4.3 工程・設備・外注先を見るポイント	advice	medium	次に浴管理です。無電解 Ni-P のような化学浴では、浴組成、析出速度、りん含有率、熱処理条件が性能に効きます。公開資料の範囲では、化学浴は「均一だから楽」ではなく「管理条件が別軸で重い」と見た方が安全です。Nickel Institute Nickel Plating Handbook ASTM B08 Scope	inline citation context	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081 | https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en | https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08	nickelinstitute.org | astm.org	3	1	industry_association | standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-051	### 4.3 工程・設備・外注先を見るポイント	advice	high	高強度鋼、ばね材、締結部品では、めっき後ベーキングの有無と試験条件を確認しないと、水素脆化の議論が抜けます。JCU 表面処理技術資料 ASTM B849 ASTM F519	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	jcu-i.com | store.astm.org	3	2	vendor_first_party | standard_or_code | standards_body	0.95	ok		2	1					high-strength steel components			standard	official, legal, standards, academic, or public-context support is present	
claim-052	### 4.3 工程・設備・外注先を見るポイント	advice	high	PCB/HDI では、finish の種類だけでなく、穴埋め、銅めっき、実装、qualification を分けずに確認した方が安全です。microvia warning を読むときも同じです。IPC-4552 IPC microvia warning	inline citation context	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	ipc.org	2	2	standards_body	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	
claim-053	### 4.3 工程・設備・外注先を見るポイント	regulatory	high	外注先評価では、めっき種、膜厚、後処理、検査、規格適合、排水処理、作業者ばく露管理まで含めて確認する必要があります。PRTR や排水対応は工程の周辺論点ではなく、量産可否に効く本体条件です。METI PRTR 手引き 環境省 一般排水基準 OSHA 29 CFR 1910.1026	inline citation context	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	meti.go.jp | env.go.jp | osha.gov	3	3	legal_text | official_regulator	0.95	ok		2	1			Japan	wastewater discharge				standard	official, legal, standards, academic, or public-context support is present	
claim-054	### 4.4 誤解しやすい点と例外	fact	low	「めっきは装飾中心」は誤解です。機能用途の説明を抜くと、自動車、電子、PCB、接点の議論が全部薄くなります。表面技術協会 ORIST	inline citation context	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://mekki.sfj.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	mekki.sfj.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-055	### 4.4 誤解しやすい点と例外	regulatory	high	「公共用水域向け排水基準」と「下水道への排除基準」は同じではありません。report では公共用水域/下水道を分けて書く必要があります。環境省 一般排水基準 国交省 除害施設	inline citation context	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html	env.go.jp | mlit.go.jp	2	2	official_regulator | government_context	0.95	ok		2	1			Japan	wastewater discharge	public water bodies			standard	official, legal, standards, academic, or public-context support is present	
claim-056	### 4.4 誤解しやすい点と例外	temporal	high	「六価クロムに暫定排水基準がある」と一括で言うのも危険です。今回確認できた現行一次情報では、2024-12-11 時点の暫定排水基準延長対象は亜鉛の電気めっき業です。環境省 2024-12-11 暫定基準延長	inline citation context	https://env.go.jp/press/press_03960.html	https://env.go.jp/press/press_03960.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1		2024-12-11	Japan	hexavalent chromium		2024-12-11	temporary transitional measure	standard	official, legal, standards, academic, or public-context support is present	
claim-057	### 4.4 誤解しやすい点と例外	fact	high	「microvia の警告」は電子一般ではなく、PCB/HDI の限定文脈です。電子部品一般の finish 議論へそのまま広げない方が安全です。IPC microvia warning IPC-6012F	inline citation context	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	ipc.org | electronics.org	2	2	standards_body | standard_or_code	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	scope-limited claim
claim-058	### 4.4 誤解しやすい点と例外	regulatory	high	「RoHS と REACH は同じ材料規制」でもありません。RoHS は含有制限、REACH Annex XVII の nickel は主に release 条件です。European Commission RoHS Directive ECHA Annex XVII conditions	inline citation context	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	environment.ec.europa.eu | echa.europa.eu	2	2	legal_text	0.95	ok		2	1			EU	hazardous substances in EEE				standard	official, legal, standards, academic, or public-context support is present	
claim-059	### 4.5 いま変わっている制度・市場・技術	temporal	high	日本の六価クロム関連では、2022-04-01 に環境基準が改正され、2024-02-05 公布・2024-04-01 施行で測定法も改められました。report では改正日と施行日を分けて書くべきです。環境省 2022-04-01 告示 環境省 2024-02-05 公布	inline citation context	https://env.go.jp/press/110052.html | https://env.go.jp/press/press_02720.html	https://env.go.jp/press/110052.html | https://env.go.jp/press/press_02720.html	env.go.jp	2	2	official_regulator	0.95	ok		2	1		2022-04-01 | 2024-02-05 | 2024-04-01	Japan	hexavalent chromium		2022-04-01		standard	official, legal, standards, academic, or public-context support is present	
claim-060	### 4.5 いま変わっている制度・市場・技術	temporal	high	2024-12-11 の暫定排水基準延長は、少なくとも今回確認した official source では亜鉛の電気めっき業が対象です。六価クロムの暫定基準として書くと誤りやすいです。環境省 2024-12-11 暫定基準延長	inline citation context	https://env.go.jp/press/press_03960.html	https://env.go.jp/press/press_03960.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1		2024-12-11	Japan	hexavalent chromium		2024-12-11	temporary transitional measure	standard	official, legal, standards, academic, or public-context support is present	
claim-061	### 4.5 いま変わっている制度・市場・技術	regulatory	high	米国では OSHA が Chromium(VI) ばく露、EPA が electroplating effluent guidelines と chrome finishing 文脈を別トラックで扱っています。PFAS も chrome plating の fume suppressant 文脈で見られており、単に「クロム工程だから PFAS」ではなく、用途と薬剤文脈を限定して読む必要があります。OSHA 29 CFR 1910.1026 EPA Electroplating Effluent Guidelines EPA Chromium Finishing Questionnaire	inline citation context	https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/eg/chromium-finishing-questionnaire	https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/eg/chromium-finishing-questionnaire	osha.gov | epa.gov	3	3	legal_text | official_regulator | government_context	0.95	ok		2	1			United States	worker exposure				standard	official, legal, standards, academic, or public-context support is present	scope-limited claim
claim-062	### 4.5 いま変わっている制度・市場・技術	regulatory	high	EU 側では、RoHS の hexavalent chromium と REACH Annex XVII の nickel release 条件を別々に確認する必要があります。ここは国・制度・製品カテゴリで話が分かれます。European Commission RoHS Directive ECHA Annex XVII conditions	inline citation context	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	environment.ec.europa.eu | echa.europa.eu	2	2	legal_text	0.95	ok		2	1			EU	hazardous substances in EEE				standard	official, legal, standards, academic, or public-context support is present	
claim-063	### 4.6 実務判断に効くコストと品質の勘所	advice	medium	最安の表面処理を選ぶより、再加工、歩留まり、field failure、EHS 対応コストまで見た方が実務では安くなることが多いです。ORIST METI PRTR 手引き	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf	www2.orist.jp | meti.go.jp	2	2	government_context | legal_text	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	
claim-064	### 4.6 実務判断に効くコストと品質の勘所	advice	medium	PCB では finish の単価差だけでなく、実装条件、ぬれ性、接点利用、qualification を一緒に見ないと比較を誤りやすいです。IPC-4552 IPC-6012F	inline citation context	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	ipc.org | electronics.org	2	2	standards_body | standard_or_code	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-065	### 4.6 実務判断に効くコストと品質の勘所	advice	medium	公開資料の範囲では、自社ラインと専業めっき会社では最適化対象が違います。自社ラインは製品統合、専業めっき会社は量産性や浴安定に寄りやすく、薬品/装置メーカーは標準プロセス側の最適化を示しやすいです。METI JCU 表面処理技術資料 JEITA 信頼性評価ガイド	inline citation context	https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf	meti.go.jp | jcu-i.com | home.jeita.or.jp	3	1	government_context | vendor_first_party | industry_association	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-066	### 4.7 見落とすと危険なドメイン固有リスク	advice	high	前処理不良: 後段の密着不良、ピット、ブリスター、膜厚不均一に直結します。ORIST JCU 表面処理技術資料	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	www2.orist.jp | jcu-i.com	2	1	government_context | vendor_first_party	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-067	### 4.7 見落とすと危険なドメイン固有リスク	advice	high	水素脆化: 高強度鋼、ばね材、締結部品ではベーキングと試験条件の確認が必須です。JCU 表面処理技術資料 ASTM B849 ASTM F519	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	jcu-i.com | store.astm.org	3	2	vendor_first_party | standard_or_code | standards_body	0.95	ok		2	1					high-strength steel components			standard	official, legal, standards, academic, or public-context support is present	
claim-068	### 4.7 見落とすと危険なドメイン固有リスク	advice	high	接触抵抗とはんだ付け性: コネクタや PCB finish は同じではなく、接点利用か実装中心かで見方が変わります。JEITA 信頼性評価ガイド IPC-4552	inline citation context	https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	home.jeita.or.jp | ipc.org	2	1	industry_association | standards_body	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-069	### 4.7 見落とすと危険なドメイン固有リスク	advice	high	microvia 潜在不良: PCB/HDI 文脈に限定して重く見るべきリスクで、電子一般へ広げすぎない方が安全です。IPC microvia warning IPC-6012F	inline citation context	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	ipc.org | electronics.org	2	2	standards_body | standard_or_code	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	scope-limited claim
claim-070	### 4.7 見落とすと危険なドメイン固有リスク	regulatory	high	排水・ばく露: 製品性能の良し悪しとは別に、量産可否を止めるリスクです。環境省 一般排水基準 OSHA 29 CFR 1910.1026 EPA Electroplating Effluent Guidelines	inline citation context	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://epa.gov/eg/electroplating-effluent-guidelines	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://epa.gov/eg/electroplating-effluent-guidelines	env.go.jp | osha.gov | epa.gov	3	3	official_regulator | legal_text	0.95	ok		2	1			Japan	wastewater discharge				standard	official, legal, standards, academic, or public-context support is present	
claim-071	### 4.7 見落とすと危険なドメイン固有リスク	regulatory	high	RoHS / REACH / nickel release: 含有量と放出条件を混同すると説明も設計判断も崩れます。European Commission RoHS Directive ECHA Annex XVII conditions	inline citation context	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	environment.ec.europa.eu | echa.europa.eu	2	2	legal_text	0.95	ok		2	1			EU	hazardous substances in EEE	skin-contact release condition			standard	official, legal, standards, academic, or public-context support is present	
claim-072	### 5.1 実務チェックリスト	advice	high	方式を選ぶ - 確認すること: 基材、要求性能、使用環境、厚み要求をまず固定する	table cell	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	astm.org | www2.orist.jp	2	2	standards_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-073	### 5.1 実務チェックリスト	advice	high	方式を選ぶ - なぜ重要か: 同じ「めっき」でも比較軸が違うため	table cell	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	astm.org | www2.orist.jp	2	2	standards_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-074	### 5.1 実務チェックリスト	advice	high	方式を選ぶ - 失敗した場合のリスク: 不適切な方式比較、過剰品質、性能不足	table cell	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	astm.org | www2.orist.jp	2	2	standards_body | government_context	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-075	### 5.1 実務チェックリスト	advice	high	外注先を選ぶ - 確認すること: 前処理、膜厚、後処理、検査、ベーキング条件を確認する	table cell	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	www2.orist.jp | jcu-i.com	2	1	government_context | vendor_first_party	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-076	### 5.1 実務チェックリスト	advice	high	外注先を選ぶ - なぜ重要か: めっき種だけでは品質が決まらないため	table cell	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	www2.orist.jp | jcu-i.com	2	1	government_context | vendor_first_party	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-077	### 5.1 実務チェックリスト	advice	high	外注先を選ぶ - 失敗した場合のリスク: 密着不良、水素脆化、再加工増加	table cell	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	www2.orist.jp | jcu-i.com	2	1	government_context | vendor_first_party	0.85	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-078	### 5.1 実務チェックリスト	advice	high	PCB finish を選ぶ - 確認すること: finish と microvia/実装条件を分けずに確認する	table cell	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	ipc.org | electronics.org	2	2	standards_body | standard_or_code	0.95	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	
claim-079	### 5.1 実務チェックリスト	advice	high	PCB finish を選ぶ - なぜ重要か: finish 単体比較では不十分だから	table cell	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	ipc.org | electronics.org	2	2	standards_body | standard_or_code	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-080	### 5.1 実務チェックリスト	advice	high	PCB finish を選ぶ - 失敗した場合のリスク: field failure、実装不良、過大一般化	table cell	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed	ipc.org | electronics.org	2	2	standards_body | standard_or_code	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	avoid over-generalization
claim-081	### 5.1 実務チェックリスト	advice	high	EHS を見る - 確認すること: 公共用水域か下水道か、六価クロムか nickel/release かを分ける	table cell	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | mlit.go.jp | echa.europa.eu	3	3	official_regulator | government_context | legal_text	0.95	ok		2	1			Japan	hexavalent chromium	public water bodies			standard	official, legal, standards, academic, or public-context support is present	
claim-082	### 5.1 実務チェックリスト	advice	high	EHS を見る - なぜ重要か: 規制ロジックが制度ごとに違うため	table cell	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | mlit.go.jp | echa.europa.eu	3	3	official_regulator | government_context | legal_text	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	
claim-083	### 5.1 実務チェックリスト	advice	high	EHS を見る - 失敗した場合のリスク: 誤説明、許認可/運用ミス	table cell	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | mlit.go.jp | echa.europa.eu	3	3	official_regulator | government_context | legal_text	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	
claim-084	### 5.1 実務チェックリスト	advice	high	高強度鋼に使う - 確認すること: 水素脆化対策とベーキング条件を確認する	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	jcu-i.com | store.astm.org	3	2	vendor_first_party | standard_or_code | standards_body	0.95	ok		2	1					high-strength steel components			standard	official, legal, standards, academic, or public-context support is present	
claim-085	### 5.1 実務チェックリスト	advice	high	高強度鋼に使う - なぜ重要か: 遅れ破壊リスクがあるため	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	jcu-i.com | store.astm.org	3	2	vendor_first_party | standard_or_code | standards_body	0.95	ok		2	1					high-strength steel components			standard	official, legal, standards, academic, or public-context support is present	
claim-086	### 5.1 実務チェックリスト	advice	high	高強度鋼に使う - 失敗した場合のリスク: 重大破損、事故、責任問題	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://store.astm.org/Standards/B849.htm | https://store.astm.org/f0519-17a.html	jcu-i.com | store.astm.org	3	2	vendor_first_party | standard_or_code | standards_body	0.95	ok		2	1					high-strength steel components			standard	official, legal, standards, academic, or public-context support is present	
claim-087	### 5.1 実務チェックリスト	advice	high	コストを比較する - 確認すること: 単価だけでなく歩留まり、再加工、field failure、EHS 対応費を含める	table cell	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	meti.go.jp | ipc.org	2	2	legal_text | standards_body	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	
claim-088	### 5.1 実務チェックリスト	advice	high	コストを比較する - なぜ重要か: 実際の総コストは後工程で決まりやすいため	table cell	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	meti.go.jp | ipc.org	2	2	legal_text | standards_body	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	
claim-089	### 5.1 実務チェックリスト	advice	high	コストを比較する - 失敗した場合のリスク: 見かけ安価だが総コスト高	table cell	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	meti.go.jp | ipc.org	2	2	legal_text | standards_body	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	
claim-090	### 5.2 追加で確認したい主張と調査の向き	advice	high	個別製品の膜厚値、合否判定、顧客固有規格は、ASTM/JIS/IPC や顧客図面に降りて確認した方が安全です。ASTM B08 Scope IPC-4552	inline citation context	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	astm.org | ipc.org	2	2	standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-091	### 5.2 追加で確認したい主張と調査の向き	advice	high	下水道接続の実務判断では、自治体・下水道管理者の排除基準や受入条件に加え、公共用水域向け基準との違いも別途確認すべきです。国交省 除害施設 環境省 一般排水基準	inline citation context	https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://env.go.jp/water/impure/haisui.html	https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://env.go.jp/water/impure/haisui.html	mlit.go.jp | env.go.jp	2	2	government_context | official_regulator	0.95	ok		2	1			Japan	wastewater discharge	public water bodies			standard	official, legal, standards, academic, or public-context support is present	local add-on rules may apply; confirm with sewerage authority
claim-092	### 5.2 追加で確認したい主張と調査の向き	advice	high	ENIG/ENEPIG、microvia、RDL のような細部は、製品カテゴリ別の IPC/JEITA/顧客規格へ進んだ方が安全です。IPC-4552 JEITA/ITRS 2007	inline citation context	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	https://ipc.org/TOC/IPC-4552wAm-1-2.pdf | https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf	ipc.org | semicon.jeita.or.jp	2	1	standards_body | industry_association	0.85	ok		2	1				microvia reliability				standard	official, legal, standards, academic, or public-context support is present	industry association evidence is best used for sector context, not plant-specific guarantees
claim-093	### 5.3 不確実性と追加調査	advice	high	今回は共通論点の整理を優先しており、個別の JIS / ASTM / IPC 要求値や顧客図面ベースの受入規格は、案件別に追加確認した方が安全です。ASTM B08 Scope IPC-4552	inline citation context	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08 | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	astm.org | ipc.org	2	2	standards_body	0.95	ok		2	1								standard	official, legal, standards, academic, or public-context support is present	
claim-094	### 5.3 不確実性と追加調査	advice	high	vendor や industry association の資料は代表例として使っているため、個別ラインや個別製品へ一般化する前に、該当規格と実工程を確認する必要があります。METI PRTR 手引き 表面技術協会	inline citation context	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://mekki.sfj.or.jp/	https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf | https://mekki.sfj.or.jp/	meti.go.jp | mekki.sfj.or.jp	2	2	legal_text | professional_body	0.95	ok		2	1			Japan					standard	official, legal, standards, academic, or public-context support is present	avoid over-generalization
claim-095	### 5.3 不確実性と追加調査	advice	high	日本の下水道側条件、顧客固有の膜厚・試験条件、特定 finish の詳細比較は、自治体、管理者、顧客図面の三つで追加確認が必要です。国交省 除害施設 IPC-4552	inline citation context	https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html | https://ipc.org/TOC/IPC-4552wAm-1-2.pdf	mlit.go.jp | ipc.org	2	2	government_context | standards_body	0.95	ok		2	1			Japan		sewer discharge			standard	official, legal, standards, academic, or public-context support is present	local add-on rules may apply
```

---

## FILE: `notes/topic-profile.md`

```text
# Topic Stop Profile

- Run ID: 20260419-224554-research
- Topic: めっき
- Preset: dr_ultra
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.
- Topic scope: standard (manual_override, breadth score 50)
- Budget scale: 0.45

## Stop posture

standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800

## Signals

- manual_override:focused_overview_report
- manual_override:no_prior_run_reuse
- manual_override:technology_overview

## Effective controls

- Query budget: 24
- Raw hit budget: 80
- Open budget: 30
- Deep-read budget: 14
- Novelty stop threshold: 0.04
- Max same-domain ratio: 0.18

## Use

- Stop widening once official, standards/professional, industry, vendor, and regulatory classes are all represented.
- Prefer closing high-risk claim gaps over adding more same-domain sources.
- Keep the run scoped: it is a focused overview, not a full DR-equivalent saturation pass.
```

---

## FILE: `notes/contradiction-log.md`

```text
# Contradiction Log

## Confirmed Contradictions

- 一般的な説明では「めっき」は外観処理の印象が強いが、今回の一次情報では防食、導電、接触、はんだ付け性、拡散バリアなど機能付与用途が主流として現れる。  
  Sources: `sfj.or.jp`, `Nickel Institute`, `JEITA`, `IPC`
- 「六価クロムに暫定排水基準がある」という理解は今回の一次情報では確認できず、2024-12-11 時点で暫定排水基準が延長されたのは亜鉛の電気めっき業のみ。  
  Sources: `env.go.jp/press/press_03960.html`, `env.go.jp/water/impure/haisui.html`
- IPC の microvia reliability warning は PCB/HDI の microvia-to-target plating reliability 文脈であり、電子用途全般のめっき一般に広げると過大一般化になる。  
  Sources: `ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high`, `ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed`

## Negative Evidence

- 公共用水域向けの一般排水基準ページでは六価クロム `0.2 mg/L` が確認できるが、下水道受入れを同じ数値で一律に説明する根拠は見当たらない。下水道側は別途排除基準・除害施設の整理が必要。  
  Sources: `env.go.jp/water/impure/haisui.html`, `mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html`
- vendor/industry 資料だけでは、個別製品に対する膜厚、ベーキング条件、合否判定を一般化する根拠としては不足する。標準や顧客規格の確認が必要。  
  Sources: `jcu-i.com`, `ipc.org`, `ASTM scope pages`

## Interpretation

- report では、規制の数値と日付は必ず official / legal source に寄せる。
- vendor / industry association 由来の説明は「公開資料の範囲では」「代表例として」で弱める。
- 方式比較、用途比較、規制比較を同じ表で一律化せず、適用範囲と判断場面を分ける。
```

---

## FILE: `notes/upstream-downstream-map.md`

```text
# Upstream and Downstream Map

## Upstream

- 基材: 鋼、銅合金、アルミ、樹脂上導体化対象など。基材で前処理、密着、脆化リスクが変わる。
- 薬品: 前処理薬品、めっき薬品、無電解浴、後処理薬品、fume suppressant。
- 設備: めっき槽、整流器、搬送、ろ過、分析、排水処理、排ガス処理。
- 標準/規格: IPC、ASTM、JEITA/JFS、顧客規格、受入基準。

## Downstream

- 自動車: 防食、耐久、締結部品、ばね材、外装・建材寄り鋼板。
- 電子部品/コネクタ: 接触抵抗、はんだ付け性、耐食、拡散バリア。
- PCB/HDI: surface finish、microvia、via fill、rigid board qualification。
- 半導体周辺/パッケージング: fine pitch、RDL、ワイヤボンドや接触系の表面仕様。
- 建材/装飾: 耐候、防食、外観、保守性。

## Adjacent Process Notes

- 前処理不良は後段の密着不良、ピット、ブリスター、膜厚不均一に直結する。
- 排水・排ガス・作業者ばく露は製品性能とは別系統の gate で、工程選定の初期から織り込む必要がある。
- 外注時は「めっき種」だけでなく、前処理、後処理、膜厚管理、ベーキング、検査方法、規格適合まで確認が必要。
```

---

## FILE: `notes/role-structure-matrix.md`

```text
# Role Structure Matrix

## Compared Entities

| Entity | Main role | What they usually optimize | Where they can mislead | Primary checks |
| --- | --- | --- | --- | --- |
| 専業めっき会社 | 受託加工 | 生産性、浴安定、歩留まり、顧客規格適合 | 自社得意工程を前提に語りやすい | 前処理、膜厚、後処理、検査、EHS |
| 自社ラインを持つ OEM/部品メーカー | 製品統合 | 製品性能、量産性、内製条件 | 製品固有条件が一般論に見えやすい | 基材、要求性能、量産窓、故障モード |
| 薬品メーカー | 浴・処方 | 浴寿命、析出性、品質安定 | 代表処方を一般解に見せやすい | 代表例か、適用基材、管理条件 |
| 装置メーカー | 設備 | 処理能力、自動化、分析・保全 | 設備で解ける問題と工程設計問題を混同しやすい | 槽設計、ろ過、整流、排気、保全 |
| 規制当局 | 規制/EHS | 排水、排ガス、ばく露、法令適合 | 製品性能の優劣は語らない | 日付、適用範囲、地域差、確認窓口 |
| 標準/業界団体 | 用語・品質基準 | 用語統一、試験、比較枠組み | 製品個別仕様までは持たない | 適用範囲、試験条件、顧客規格との差 |

## Matrix Notes

- 今回の report では official / legal / standards-backed claim を骨格にし、vendor/industry claim は代表例扱いにする。
- microvia、ENIG/ENEPIG、電気めっき薬品の具体論は vendor や IPC が強いが、適用範囲を狭く書く。
- 排水、六価クロム、RoHS/REACH、OSHA は official / legal source を優先する。

## Positioning Summary

- 読者がまず切り分けるべきなのは「製品性能の話」「工程能力の話」「規制/EHS の話」が同じではないこと。
- めっき種の名前だけでなく、誰の立場の情報かを見ると判断ミスが減る。
```

---

## FILE: `notes/domain-risk-map.md`

```text
# Domain Risk Map

## 1. Decision-Critical Failure Modes

| 判断場面 | 失敗モード | 何が起きるか | 初期兆候 | 根拠または確認先 |
| --- | --- | --- | --- | --- |
| 高強度鋼やばね材にめっきを使う | 水素脆化 | 遅れ破壊、締結部品破損 | 後工程での割れ、遅延破断 | ASTM B849 / B850 / F519, JCU |
| PCB/HDI で高密度配線を採る | microvia 潜在不良 | field failure、導通不安定 | microvia-to-target plating reliability の低下 | IPC-6012F, IPC microvia warning |
| 防食めっきを外装・建材に使う | 前処理/後処理不良 | 密着不良、早期腐食、外観不良 | ピット、ブリスター、膜厚ばらつき | ORIST, JISF |
| コネクタ/接点に表面仕上げを選ぶ | finish 選定ミス | 接触抵抗、はんだ付け性、耐食の不一致 | 挿抜後の接触不良、ぬれ不良 | IPC-4552, JEITA |

## 2. Actor-Specific Blind Spots

| 主体 | 見落としやすいリスク | なぜ起きやすいか | 追加確認 |
| --- | --- | --- | --- |
| 調達側 | めっき種だけで発注する | 前処理・後処理・規格条件が抜ける | 膜厚、後処理、検査、ベーキング条件 |
| 設計側 | microvia や接点 finish を一般論で決める | 用途別の要求が違う | IPC/顧客規格、使用環境、接触条件 |
| 生産側 | 排水/EHS を後回しにする | 製品性能と別系統の gate だから | env.go.jp, MLIT, OSHA, EPA |
| vendor 情報の読み手 | 代表例を一般解と誤認する | 成功事例の前提条件が省略されがち | 適用基材、工程窓、規格、ライン条件 |

## 3. Hidden Dependencies And Boundary Conditions

| リスク | 隠れた依存 | 説明が誤りやすい理由 | どこで確認するか |
| --- | --- | --- | --- |
| 六価クロム規制 | 公共用水域か下水道か | 同じ「排水規制」と思い込みやすい | env.go.jp, MLIT, 自治体/下水道管理者 |
| RoHS / REACH / nickel | 含有制限と放出条件 | 規制ロジックが異なる | EC, ECHA |
| 溶融亜鉛めっきと湿式めっきの比較 | 比較軸そのもの | 同じ表面処理でも工程が異なる | JISF, ASTM B08 |
| ENIG / ENEPIG / OSP | 使用環境と実装条件 | finish 名だけで万能に見えやすい | IPC, JEITA, 顧客規格 |

## 4. Domain-Specific Risk Buckets

### 4.1 Operational Failure

- 浴管理不良
- 前処理不良
- ベーキング条件の未確認

### 4.2 Quality Or Performance Failure

- 膜厚不均一
- 密着不良
- ピット / ブリスター
- 接触抵抗悪化
- はんだ付け性不良
- microvia 潜在不良

### 4.3 Safety, Compliance, Or Liability

- 六価クロム排水
- 大気排出
- 作業者ばく露
- RoHS / REACH / ニッケル放出条件
- PFAS を含む fume suppressant 管理

### 4.4 Supply, Vendor, Or Upstream/Downstream Exposure

- job plater と captive line の条件差
- 装置・薬品メーカー前提の標準プロセス依存
- 顧客規格未確認のままの外注

### 4.5 Financial, Commercial, Or Adoption Risk

- 歩留まり悪化
- 過剰品質によるコスト高
- EHS 対応の後追い投資

### 4.6 Reputation, Public Narrative, Or Policy Backlash

- クロム/PFAS を一括りにした誤解
- 「めっき=装飾」の固定観念

## 5. Common Reader Misunderstandings

| よくある誤解 | 実際の違い | なぜ危険か | 確認先 |
| --- | --- | --- | --- |
| めっきは装飾中心 | 実務では機能付与が中心 | 方式選定を誤る | SFJ, ORIST, IPC |
| 六価クロムの暫定基準がそのままある | 現行一次情報では亜鉛の電気めっき業のみ確認 | 規制説明を誤る | env.go.jp |
| microvia warning は電子全般に適用できる | PCB/HDI の限定文脈 | 過大一般化になる | IPC |
| RoHS と REACH は同じ | 含有制限と放出条件で別 | 適用判断を誤る | EC, ECHA |

## 6. Time-Sensitive Or Stale-Information Risks

| 変わりやすい論点 | なぜ変わるか | 最新確認先 | タイミング |
| --- | --- | --- | --- |
| 六価クロム関連の日付と測定法 | 告示・施行・分析法改定が分かれる | env.go.jp | report 直前 |
| 暫定排水基準 | 延長・失効がある | env.go.jp | report 直前 |
| EPA PFAS/chrome finishing 文脈 | 調査・規則作業が進行中 | epa.gov | report 直前 |
| IPC microvia warning の扱い | 技術文書・業界警告が更新されうる | ipc.org | report 直前 |

## 7. Latest-Check Items Before Delivery

- 日本の六価クロム環境基準、一般排水基準、測定法改正日。
- 暫定排水基準の対象業種。
- OSHA Chromium(VI) 数値。
- RoHS / REACH / nickel release の整理。

## 8. Report-Mandatory Risk Points

- Summary and section 2 must mention:
  高強度鋼の水素脆化、六価クロム規制の数値と日付、PCB microvia の限定性。
- Section 4 risk synthesis must mention:
  前処理、膜厚、密着、浴管理、排水/ばく露、RoHS/REACH。
- Checklist section must force the reader to confirm:
  基材、要求性能、適用規格、EHS 窓口、外注先の検査条件。

## 9. Missing Evidence And Follow-Up Queries

- Evidence gap:
  個別顧客規格値や各社の工程窓は今回の範囲外。
- What to search next:
  対象規格名、顧客図面、受入検査条件、自治体下水道基準。
- What must be downgraded or labeled uncertain if the gap remains:
  個別膜厚値、合否判定、量産条件の一般化。
```

---

## FILE: `notes/evidence-gap-followup.md`

```text
# Evidence Gap Follow-up

Run `scripts/build_gap_followup_queries.py <run_dir>` after `claim-ledger.tsv` shows weak or missing claims.

-
```

---

## FILE: `notes/latest-coverage-check.json`

```text
﻿{
  "run_id": "20260419-224554-research",
  "preset": "dr_ultra",
  "logic_milestone": "M4",
  "entity_scope": {
    "required": false,
    "mode": "off",
    "score": 0,
    "kind": "technology",
    "kind_score": 0,
    "bundle_id": "general-overview",
    "bundle_label": "一般トピック概説",
    "family_id": "independent_context",
    "family_id_matches_kind": true,
    "summary": "off / optional / kind technology / bundle 一般トピック概説; score 0; surface_floor=0, tail_queries=0"
  },
  "required_query_families": [
    {
      "family_id": "official_primary",
      "label": "一次・公式",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered",
      "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ## 1. 要約 (2); standards_body ipc.org @ ## 2. 主要な発見 (2); standards_body ipc.org @ ## 3. 主要な根拠と出典 (1); +102 more",
      "requested_coverage_evidence": "env.go.jp / osha.gov / environment.ec.europa.eu",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
          "domain": "epa.gov",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
          "domain": "epa.gov",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
          "domain": "epa.gov",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
          "domain": "epa.gov",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
          "domain": "epa.gov",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
          "domain": "meti.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        }
      ],
      "mapping_evidence_count": 105,
      "waiver_reason": "-",
      "matched_query_count": 4,
      "minimum_query_matches_required": 1,
      "sample_queries": [
        "めっき 防食 基礎 ORIST PDF",
        "JCU 表面処理技術 事業戦略 PDF",
        "METI めっき 用途分類 PDF"
      ],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "query_matches",
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "regulation_standards",
      "label": "規制・標準",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered",
      "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ## 1. 要約 (2); standards_body ipc.org @ ## 2. 主要な発見 (2); standards_body ipc.org @ ## 3. 主要な根拠と出典 (1); +86 more",
      "requested_coverage_evidence": "env.go.jp / ipc.org / echa.europa.eu",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
          "domain": "epa.gov",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
          "domain": "epa.gov",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
          "domain": "epa.gov",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        }
      ],
      "mapping_evidence_count": 89,
      "waiver_reason": "-",
      "matched_query_count": 1,
      "minimum_query_matches_required": 1,
      "sample_queries": [
        "EPA electroplating effluent guidelines"
      ],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "query_matches",
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "research_validation",
      "label": "研究・検証",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered_by_mapping",
      "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ## 1. 要約 (2); standards_body ipc.org @ ## 2. 主要な発見 (2); standards_body ipc.org @ ## 3. 主要な根拠と出典 (1); +62 more",
      "requested_coverage_evidence": "orist / JEITA / Nickel Institute",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
          "domain": "epa.gov",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
          "domain": "epa.gov",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
          "domain": "meti.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        }
      ],
      "mapping_evidence_count": 65,
      "waiver_reason": "-",
      "matched_query_count": 0,
      "minimum_query_matches_required": 1,
      "sample_queries": [],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "vendor_implementation",
      "label": "ベンダー実装",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered_by_mapping",
      "coverage_evidence": "auto-verified from citation-ledger: vendor_first_party jcu-i.com @ ## 2. 主要な発見 (2); vendor_first_party jcu-i.com @ ## 3. 主要な根拠と出典 (1); vendor_first_party jcu-i.com @ ### 4.2 用途別・産業別に何が違うか (1); +4 more",
      "requested_coverage_evidence": "jcu-i.com",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        }
      ],
      "mapping_evidence_count": 7,
      "waiver_reason": "-",
      "matched_query_count": 0,
      "minimum_query_matches_required": 1,
      "sample_queries": [],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "independent_context",
      "label": "独立コンテキスト",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered_by_mapping",
      "coverage_evidence": "auto-verified from citation-ledger: government_context www2.orist.jp @ ## 1. 要約 (2); government_context www2.orist.jp @ ## 3. 主要な根拠と出典 (2); government_context www2.orist.jp @ ### 4.1 方式ごとの比較ポイント (2); +45 more",
      "requested_coverage_evidence": "sfj.or.jp / jisf.or.jp / ampp.org",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 3,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 2,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://jisf.or.jp/business/standard/jfs",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://jisf.or.jp/business/standard/jfs",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://jisf.or.jp/business/standard/jfs",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
          "domain": "semicon.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
          "domain": "semicon.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
          "domain": "semicon.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
          "domain": "epa.gov",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
          "domain": "epa.gov",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
          "domain": "meti.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role"
          ]
        }
      ],
      "mapping_evidence_count": 48,
      "waiver_reason": "-",
      "matched_query_count": 0,
      "minimum_query_matches_required": 1,
      "sample_queries": [],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "japan_specific",
      "label": "日本語・国内",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered",
      "coverage_evidence": "auto-verified from citation-ledger: government_context www2.orist.jp @ ## 1. 要約 (2); government_context www2.orist.jp @ ## 3. 主要な根拠と出典 (2); government_context www2.orist.jp @ ### 4.1 方式ごとの比較ポイント (2); +62 more",
      "requested_coverage_evidence": "sfj.or.jp / meti.go.jp / jeita.or.jp",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 3,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 2,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 2,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://jisf.or.jp/business/tech/aen/index.html",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 2,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 1. 要約",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.7 見落とすと危険なドメイン固有リスク",
          "source_url": "https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.1 実務チェックリスト",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.3 不確実性と追加調査",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://home.jeita.or.jp/ecb/about/part.html",
          "domain": "home.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 2. 主要な発見",
          "source_url": "https://jisf.or.jp/business/standard/jfs",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "## 3. 主要な根拠と出典",
          "source_url": "https://jisf.or.jp/business/standard/jfs",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://jisf.or.jp/business/standard/jfs",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.1 方式ごとの比較ポイント",
          "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
          "domain": "semicon.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
          "domain": "semicon.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 5.2 追加で確認したい主張と調査の向き",
          "source_url": "https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf",
          "domain": "semicon.jeita.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.2 用途別・産業別に何が違うか",
          "source_url": "https://jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf",
          "domain": "jisf.or.jp",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
          "domain": "meti.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "domain"
          ]
        }
      ],
      "mapping_evidence_count": 65,
      "waiver_reason": "-",
      "matched_query_count": 1,
      "minimum_query_matches_required": 1,
      "sample_queries": [
        "溶融亜鉛めっき 日本鉄鋼連盟"
      ],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "query_matches",
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "contradiction_negative",
      "label": "反証・不在確認",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered_by_mapping",
      "coverage_evidence": "auto-verified from citation-ledger: legal_text echa.europa.eu @ ### 4.5 いま変わっている制度・市場・技術 (1); legal_text environment.ec.europa.eu @ ### 4.5 いま変わっている制度・市場・技術 (1); legal_text osha.gov @ ### 4.5 いま変わっている制度・市場・技術 (1); +5 more",
      "requested_coverage_evidence": "env.go.jp / ipc.org / mlit.go.jp",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/110052.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_02720.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://epa.gov/eg/electroplating-effluent-guidelines",
          "domain": "epa.gov",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.5 いま変わっている制度・市場・技術",
          "source_url": "https://epa.gov/eg/chromium-finishing-questionnaire",
          "domain": "epa.gov",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        }
      ],
      "mapping_evidence_count": 8,
      "waiver_reason": "-",
      "matched_query_count": 0,
      "minimum_query_matches_required": 1,
      "sample_queries": [],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "upstream_downstream",
      "label": "上流/下流",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered_by_mapping",
      "coverage_evidence": "auto-verified from citation-ledger: government_context www2.orist.jp @ ### 4.4 誤解しやすい点と例外 (1); official_regulator env.go.jp @ ### 4.4 誤解しやすい点と例外 (1); professional_body mekki.sfj.or.jp @ ### 4.4 誤解しやすい点と例外 (1); +6 more",
      "requested_coverage_evidence": "meti.go.jp / jcu-i.com / epa.gov",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459",
          "domain": "echa.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en",
          "domain": "environment.ec.europa.eu",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://env.go.jp/press/press_03960.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.4 誤解しやすい点と例外",
          "source_url": "https://mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html",
          "domain": "mlit.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        }
      ],
      "mapping_evidence_count": 9,
      "waiver_reason": "-",
      "matched_query_count": 0,
      "minimum_query_matches_required": 1,
      "sample_queries": [],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "role_structure",
      "label": "役割差・類型",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered_by_mapping",
      "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ### 4.3 工程・設備・外注先を見るポイント (1); government_context www2.orist.jp @ ### 4.3 工程・設備・外注先を見るポイント (1); standards_body astm.org @ ### 4.3 工程・設備・外注先を見るポイント (1); +10 more",
      "requested_coverage_evidence": "jeita.or.jp / jisf.or.jp / jcu-i.com",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://astm.org/membership-participation/technical-committees/committee-b08/scope-b08",
          "domain": "astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf",
          "domain": "jcu-i.com",
          "source_role": "vendor_first_party",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://env.go.jp/water/impure/haisui.html",
          "domain": "env.go.jp",
          "source_role": "official_regulator",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://mekki.sfj.or.jp/",
          "domain": "mekki.sfj.or.jp",
          "source_role": "professional_body",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026",
          "domain": "osha.gov",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/Standards/B849.htm",
          "domain": "store.astm.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://store.astm.org/f0519-17a.html",
          "domain": "store.astm.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.3 工程・設備・外注先を見るポイント",
          "source_url": "https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081",
          "domain": "nickelinstitute.org",
          "source_role": "industry_association",
          "citation_instances": 1,
          "matched_by": [
            "section_heading"
          ]
        }
      ],
      "mapping_evidence_count": 13,
      "waiver_reason": "-",
      "matched_query_count": 0,
      "minimum_query_matches_required": 1,
      "sample_queries": [],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "mapping_evidence"
      ],
      "covered": true
    },
    {
      "family_id": "chronology_change",
      "label": "時系列・変化点",
      "plan_status": "covered",
      "requested_coverage_status": "covered",
      "coverage_status": "covered_by_mapping",
      "coverage_evidence": "auto-verified from citation-ledger: standards_body ipc.org @ ### 4.6 実務判断に効くコストと品質の勘所 (1); government_context www2.orist.jp @ ### 4.6 実務判断に効くコストと品質の勘所 (1); standard_or_code electronics.org @ ### 4.6 実務判断に効くコストと品質の勘所 (1); +2 more",
      "requested_coverage_evidence": "env.go.jp",
      "mapping_evidence_items": [
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://ipc.org/TOC/IPC-4552wAm-1-2.pdf",
          "domain": "ipc.org",
          "source_role": "standards_body",
          "citation_instances": 1,
          "matched_by": [
            "source_role",
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf",
          "domain": "www2.orist.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role",
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed",
          "domain": "electronics.org",
          "source_role": "standard_or_code",
          "citation_instances": 1,
          "matched_by": [
            "source_role",
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf",
          "domain": "meti.go.jp",
          "source_role": "legal_text",
          "citation_instances": 1,
          "matched_by": [
            "source_role",
            "section_heading"
          ]
        },
        {
          "origin": "citation_ledger",
          "section": "### 4.6 実務判断に効くコストと品質の勘所",
          "source_url": "https://meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf",
          "domain": "meti.go.jp",
          "source_role": "government_context",
          "citation_instances": 1,
          "matched_by": [
            "source_role",
            "section_heading"
          ]
        }
      ],
      "mapping_evidence_count": 5,
      "waiver_reason": "-",
      "matched_query_count": 0,
      "minimum_query_matches_required": 1,
      "sample_queries": [],
      "has_explicit_coverage_evidence": true,
      "has_mapping_evidence": true,
      "is_waived": false,
      "coverage_basis": [
        "mapping_evidence"
      ],
      "covered": true
    }
  ],
  "required_report_sections": [
    {
      "section": "## 1. 要約",
      "matched_heading": "## 1. 要約",
      "present": true
    },
    {
      "section": "## 2. 主要な発見",
      "matched_heading": "## 2. 主要な発見",
      "present": true
    },
    {
      "section": "## 3. 主要な根拠と出典",
      "matched_heading": "## 3. 主要な根拠と出典",
      "present": true
    },
    {
      "section": "## 4. 論点別の分析",
      "matched_heading": "## 4. 論点別の分析",
      "present": true
    },
    {
      "section": "## 5. 判断のために確認すべきことと追加調査",
      "matched_heading": "## 5. 判断のために確認すべきことと追加調査",
      "present": true
    },
    {
      "section": "## 6. 主要ソース一覧",
      "matched_heading": "## 6. 主要ソース一覧",
      "present": true
    },
    {
      "section": "### 4.1 方式ごとの比較ポイント",
      "matched_heading": "### 4.1 方式ごとの比較ポイント",
      "present": true
    },
    {
      "section": "### 4.2 用途別・産業別に何が違うか",
      "matched_heading": "### 4.2 用途別・産業別に何が違うか",
      "present": true
    },
    {
      "section": "### 4.3 工程・設備・外注先を見るポイント",
      "matched_heading": "### 4.3 工程・設備・外注先を見るポイント",
      "present": true
    },
    {
      "section": "### 4.4 誤解しやすい点と例外",
      "matched_heading": "### 4.4 誤解しやすい点と例外",
      "present": true
    },
    {
      "section": "### 4.5 いま変わっている制度・市場・技術",
      "matched_heading": "### 4.5 いま変わっている制度・市場・技術",
      "present": true
    },
    {
      "section": "### 4.6 実務判断に効くコストと品質の勘所",
      "matched_heading": "### 4.6 実務判断に効くコストと品質の勘所",
      "present": true
    },
    {
      "section": "### 4.7 見落とすと危険なドメイン固有リスク",
      "matched_heading": "### 4.7 見落とすと危険なドメイン固有リスク",
      "present": true
    }
  ],
  "required_note_artifacts": [
    {
      "artifact": "notes/topic-profile.md",
      "required": true,
      "present": true
    },
    {
      "artifact": "notes/contradiction-log.md",
      "required": true,
      "present": true
    },
    {
      "artifact": "notes/upstream-downstream-map.md",
      "required": true,
      "present": true
    },
    {
      "artifact": "notes/role-structure-matrix.md",
      "required": true,
      "present": true
    },
    {
      "artifact": "notes/domain-risk-map.md",
      "required": true,
      "present": true
    }
  ],
  "gap_followup_artifact": null,
  "overall_complete": true,
  "coverage_status": "complete",
  "coverage_counts": {
    "query_families_covered": 10,
    "query_families_total": 10,
    "query_families_waived": 0,
    "report_sections_present": 13,
    "report_sections_total": 13,
    "note_artifacts_present": 5,
    "note_artifacts_total": 5
  },
  "missing_query_families": [],
  "missing_report_sections": [],
  "missing_note_artifacts": [],
  "missing_conditional_artifacts": []
}
```

---

## FILE: `notes/subagent-tech-foundations.md`

```text
# めっき 技術基礎メモ

## まず結論

めっきは「表面に薄い機能層をつくる」技術だが、実務上は防食だけでなく、導電、接触抵抗低減、はんだ付け性、拡散バリア、EMI/ESD シールド、耐摩耗、意匠、膜厚制御まで含む広い設計領域として扱うのが正確である。ASTM の金属・無機被膜委員会 B08 は、電気めっき、無電解めっき、置換めっき、真空系、化成処理、陽極酸化、溶融めっき、熱被覆を同じ技術群として整理しており、AMPP も防食系の被膜を「液状から乾燥して固膜になるもの」や「溶融・電気めっき・溶射で与える金属膜」として整理している。ここでの「湿式/乾式」は、便宜上、液相浴を使う工程群と、真空・熱・溶融金属などの非水系工程群に分けている。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center))

## 工程の整理

| 区分 | 技術的な見方 | 代表例 | 重要な含意 |
|---|---|---|---|
| 湿式めっき | 液相浴で金属イオンを析出・置換・自己触媒還元する | 電気めっき、無電解めっき、置換めっき | 複雑形状に膜を与えやすいが、前処理と浴管理が性能を左右する。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08)) |
| 非湿式めっき/表面処理 | 真空、熱、溶融金属、熱分解系を使う | 真空蒸着、スパッタ、イオンプレート、溶融亜鉛めっき、熱溶射 | 皮膜の密着機構や膜質が湿式と異なり、厚み・応力・熱影響の見方も変わる。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html), [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center)) |

## 電気めっき

電気めっきは、外部電源を使って金属を析出させる基本技術で、ASTM B08 はこれを金属・無機被膜の中核プロセスとして扱う。設計上は「見た目」よりも、用途ごとの機能要求を先に置くべきで、たとえば亜鉛めっきは防食、錫めっきは低接触抵抗とはんだ付け性、金めっきは低く安定した接触抵抗とボンダビリティが主要用途になる。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488))

亜鉛電気めっきの ASTM B633 は、鉄鋼を腐食から守ることを主目的にしつつ、膜厚クラス、補助仕上げ、付着性、耐食性、水素脆化対策を同時に規定する。つまり、電気めっきは単なる「膜を載せる」工程ではなく、前処理、後処理、膜厚、密着、脆化抑制を一体で設計する工程である。([ASTM B633](https://store.astm.org/Standards/B633.htm))

錫電気めっきは、低接触抵抗、防食、はんだ付け性、耐かじり性に使われる。ASTM B545 は、膜厚が薄くなるほどポロシティが増え、用途ごとに最小厚みの指定が必要になることも明記している。接触用途とはんだ用途では、単に「錫が乗っている」だけでは足りず、厚みと孔食管理が要点になる。([ASTM B545-22](https://store.astm.org/b0545-22.html))

## 無電解めっき

無電解 Ni-P は、外部電流を使わず、自己触媒的な化学還元で析出する。ASTM B733 は、酸性水溶液から高温で析出し、不規則形状でも液が回れば均一膜厚を得やすいこと、さらに硬さ・耐摩耗・耐食・磁性・導電性・拡散バリア・はんだ付け性などの多機能を持つことを示している。無電解めっきの本質は「電流がないこと」ではなく、「複雑形状に均一に機能膜を与えやすいこと」にある。([ASTM B733](https://store.astm.org/b0733-22.html))

Ni-P の低リン側は電子用途でとくに重要で、ASTM B733 は 1〜3%P の皮膜を、はんだ付け性、ボンディング性、導電性向上、強アルカリ耐性に使うとしている。Nickel Institute の技術資料も、無電解ニッケルの性質と用途を、工業用途の機能皮膜として整理している。([ASTM B733](https://store.astm.org/b0733-22.html), [Nickel Institute: Properties and Applications of Electroless Nickel](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/))

ASTM B733 は、無電解 Ni-P の膜厚評価、密着試験、孔食、微小硬さ、水素脆化まで評価対象に含めており、無電解めっきでも「浴が入れば終わり」ではなく、後工程と検査までが一体であることを示している。([ASTM B733](https://store.astm.org/b0733-22.html))

## 溶融めっき

溶融めっきは、溶融金属浴に浸漬して合金層を作るプロセスで、ASTM A123/A123M は鉄鋼製品への溶融亜鉛めっきの要求を規定している。ASTM A153/A153M は、溶融亜鉛が鉄表面と冶金反応して Zn/Fe 合金層を形成し、鋼に密着することを明示している。防食の観点では、AMPP も亜鉛を用いた被膜がガルバニック保護を与えることを説明している。([ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html), [ASTM A153/A153M-23](https://store.astm.org/a0153_a0153m-23.html), [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center))

溶融めっきは厚膜で耐久性が高い一方、寸法影響や歪み、前処理の影響を受けやすい。ASTM A385 は、良質な溶融亜鉛めっきを得るための注意点として、部材の化学成分や表面状態のばらつき、洗浄、寸法変化への注意を挙げている。([ASTM A385](https://store.astm.org/a0385-08.html))

## 主要機能

防食は最も広い用途だが、めっきの機能はそれだけではない。亜鉛は鉄鋼の防食、錫は低接触抵抗とはんだ付け性、金は低く安定した接触抵抗とボンディング性、無電解 Ni-P は拡散バリア・耐摩耗・導電補助・はんだ付け性、EMI/ESD 用の多層無電解 Ni/Cu はシールド機能を狙う。機能要件が変わると、皮膜材料・厚み・浴・後処理の最適解も変わる。([ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488), [ASTM B733](https://store.astm.org/b0733-22.html), [ASTM B904-25](https://store.astm.org/standards/b904))

## 重要論点

### 防食

防食はめっきの基礎機能だが、材料選定だけでは決まらない。錫めっきでも屋外では腐食が起こりうる一方、亜鉛めっきは鉄鋼の犠牲防食として広く使われる。溶融亜鉛めっきは、バリア保護だけでなくガルバニック保護も与える点が重要である。([ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html), [ASTM news: corrosion protection for steel bars](https://www.astm.org/news/press-releases/new-astm-standard-provides-corrosion-protection-steel-bars))

### 導電・接触

接触抵抗を下げる用途では、錫や金のように電気的な接点特性が重視される。錫は低接触抵抗、金は低く安定した接触抵抗が主要用途であり、無電解 Ni-P の低リン側は導電性向上にも使われる。接点用途では、酸化膜、ポロシティ、摩耗、フレッティングまで含めて考える必要がある。([ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488), [ASTM B733](https://store.astm.org/b0733-22.html), [ASTM B02 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b02/scope-b02))

### はんだ付け性

はんだ付け性は、錫めっきと低リン無電解 Ni-P で重要な設計要求になる。ASTM B545 は錫めっきをはんだ付け性のための表面として位置づけ、ASTM B733 は電子用途の低リン Ni-P にはんだ付け性を明記している。PCB の表面処理では、IPC-6012F が solderability testing と dewetting を主要な要求項目に追加しており、はんだのぬれだけでなく、濡れムラや界面欠陥まで評価対象になる。([ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733](https://store.astm.org/b0733-22.html), [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed))

### 膜厚

膜厚は、めっき仕様の中核である。ASTM B659 は、複数の金属・無機被膜で膜厚がサービス性能に直結し、測定法にはそれぞれ適用限界があると整理している。ASTM B633、B545、B733 もそれぞれ膜厚クラスや最小厚み、サービス条件番号を持ち、厚みは「見た目」ではなく性能パラメータとして扱われる。([ASTM B659](https://store.astm.org/b0659-90r21.html), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733](https://store.astm.org/b0733-22.html))

### 前処理

前処理は密着の前提条件で、表面清浄化、応力除去、機械処理、酸洗い、スミット除去、エッチングなどが含まれる。ASTM B242 は高炭素鋼の電気めっき前処理として、最小限の水素脆化と最大限の密着を目指す手順を示す。ASTM B849 は、電気めっきや無電解めっきなどで生じうる水素脆化を減らすための事前熱処理を規定している。([ASTM B242](https://store.astm.org/b242.html), [ASTM B849](https://store.astm.org/Standards/B849.htm))

### 密着

密着は、前処理・浴管理・後処理の総合結果である。ASTM B733 は無電解 Ni-P に対して、密着評価を bend / impact / thermal shock で確認するとし、B850 はめっき後熱処理が水素脆化低減に有効だが完全保証ではないと注意している。つまり、密着は「析出したか」ではなく「使用条件で剥がれないか」で見る必要がある。([ASTM B733](https://store.astm.org/b0733-22.html), [ASTM B850](https://store.astm.org/b0850-98r22.html))

### 水素脆化

水素脆化は高強度鋼で特に重要で、めっきそのものよりも、脱脂・酸洗い・めっき・後処理の連鎖で発生しやすい。ASTM B849 は前処理での低減策、ASTM B850 は後熱処理、ASTM F519 は製造中の表面処理・前処理・めっき条件が水素脆化を起こしていないかを機械試験で検証する枠組みを与える。([ASTM B849](https://store.astm.org/Standards/B849.htm), [ASTM B850](https://store.astm.org/b0850-98r22.html), [ASTM F519](https://store.astm.org/f0519-17a.html))

### microvia

microvia は PCB/HDI の要所で、IPC-2226 ベースでは「直径 150 μm 以下のブラインドホール」を指す。IPC-6012F は、PTH、buried/blind vias、microvias を含む構造に対して、microvia reliability、internal plated layers、solderability testing、dewetting まで要求を拡張している。IPC の技術資料でも、microvia-to-target plating failure は従来の顕微鏡観察だけでは見落としうると警告されており、microvia は「穴を埋める」ではなく「接続信頼性を作る」対象である。([IPC microvia definition PDF](https://www.ipc.org/system/files/technical_resource/E2%26S29_01.pdf), [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed), [IPC microvia reliability warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high))

### microvia の充填

microvia 充填では、電解銅めっきが実務上の中心になる。IPC の技術発表資料では、微小径の microvia を銅で充填する技術が量産で成立しており、via-in-pad、熱管理、積層 microvia の信頼性改善に使われている。別の IPC 資料では、through-hole でも bridge 形成から DC 補充填へつなぐ 2 段階の銅めっきで、薄い表面銅と良好な充填を両立できるとしている。([IPC microvia fill paper](https://www.ipc.org/system/files/technical_resource/E42%26S02_01%20-%20Moody%20Dreiza_Mustafa%20Oezkoek.pdf), [IPC through-hole fill paper](https://www.ipc.org/system/files/technical_resource/E38%26S09-01%20-%20Jim%20Watkowski.pdf))

## 参照した一次情報ソース

1. [ASTM Committee B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08)
2. [ASTM B633](https://store.astm.org/Standards/B633.htm)
3. [ASTM B545-22](https://store.astm.org/b0545-22.html)
4. [ASTM B733-22](https://store.astm.org/b0733-22.html)
5. [ASTM B659](https://store.astm.org/b0659-90r21.html)
6. [ASTM B849](https://store.astm.org/Standards/B849.htm)
7. [ASTM B850-98(2022)](https://store.astm.org/b0850-98r22.html)
8. [ASTM F519](https://store.astm.org/f0519-17a.html)
9. [ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html)
10. [ASTM A153/A153M-23](https://store.astm.org/a0153_a0153m-23.html)
11. [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center)
12. [Nickel Institute: Nickel Plating Handbook](https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/)
13. [Nickel Institute: Properties and Applications of Electroless Nickel](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/)
14. [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
15. [IPC microvia definition PDF](https://www.ipc.org/system/files/technical_resource/E2%26S29_01.pdf)
16. [IPC microvia reliability warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
17. [IPC microvia fill paper](https://www.ipc.org/system/files/technical_resource/E42%26S02_01%20-%20Moody%20Dreiza_Mustafa%20Oezkoek.pdf)
18. [IPC through-hole fill paper](https://www.ipc.org/system/files/technical_resource/E38%26S09-01%20-%20Jim%20Watkowski.pdf)

## 後で本体レポートに入れるべき high-signal claims

1. めっきは防食だけでなく、導電、接触抵抗低減、はんだ付け性、拡散バリア、EMI/ESD、耐摩耗まで含む機能表面技術として整理すべきである。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733-22](https://store.astm.org/b0733-22.html), [ASTM B488](https://store.astm.org/standards/b488), [ASTM B904-25](https://store.astm.org/standards/b904))
2. 湿式系は電気めっき、無電解めっき、置換めっきを中心に、液相浴の化学管理と前処理が性能を支配する。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM B733-22](https://store.astm.org/b0733-22.html), [ASTM B849](https://store.astm.org/Standards/B849.htm))
3. 非湿式系は真空、熱、溶融金属を使う被膜群として別枠で考えるべきで、溶融亜鉛めっきは冶金的に Zn/Fe 合金層を作る。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM A153/A153M-23](https://store.astm.org/a0153_a0153m-23.html))
4. 亜鉛電気めっきは防食向け、錫電気めっきは低接触抵抗とはんだ付け性向け、金電気めっきは低く安定した接触抵抗とボンディング向けというように、用途別に材料が選ばれる。([ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488))
5. 無電解 Ni-P は高温の酸性水溶液から自己触媒的に析出し、複雑形状でも均一膜厚を与えやすい。([ASTM B733-22](https://store.astm.org/b0733-22.html))
6. 低リン無電解 Ni-P は電子用途で、はんだ付け性、ボンディング性、導電性向上に使われる。([ASTM B733-22](https://store.astm.org/b0733-22.html))
7. 膜厚は性能パラメータであり、仕様ごとに service class や最小厚み、測定法が定義される。([ASTM B659](https://store.astm.org/b0659-90r21.html), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733-22](https://store.astm.org/b0733-22.html))
8. 前処理と後熱処理は水素脆化対策の本体であり、めっき後のベーキングだけでなく、めっき前の応力除去や洗浄条件も重要である。([ASTM B849](https://store.astm.org/Standards/B849.htm), [ASTM B850-98(2022)](https://store.astm.org/b0850-98r22.html), [ASTM F519](https://store.astm.org/f0519-17a.html))
9. 密着は bend、impact、thermal shock などの試験で確認すべきで、特に無電解 Ni-P や接点用途では表面の使われ方まで含めて評価する必要がある。([ASTM B733-22](https://store.astm.org/b0733-22.html), [ASTM B545-22](https://store.astm.org/b0545-22.html))
10. microvia は 150 μm 以下のブラインドホールとして設計され、IPC-6012F では microvia reliability と solderability/dewetting まで要求が拡張されている。([IPC microvia definition PDF](https://www.ipc.org/system/files/technical_resource/E2%26S29_01.pdf), [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed))
11. microvia 充填はすでに量産技術であり、電解銅めっきは via-in-pad と熱管理のための基盤技術になっている。([IPC microvia fill paper](https://www.ipc.org/system/files/technical_resource/E42%26S02_01%20-%20Moody%20Dreiza_Mustafa%20Oezkoek.pdf), [IPC through-hole fill paper](https://www.ipc.org/system/files/technical_resource/E38%26S09-01%20-%20Jim%20Watkowski.pdf))

```

---

## FILE: `notes/subagent-applications.md`

```text
# めっきの用途・産業・実務判断メモ

新規のWeb調査だけを使って、めっきの使いどころを「用途」「方式」「実務判断」で整理したメモです。一次情報・業界団体・公的資料・標準系を優先し、vendor 資料は使っていません。

## 1. まず押さえる前提

めっきは、単なる防錆ではなく、耐食・耐摩耗・導電・はんだ付け性・接触信頼性・意匠性を個別に設計する表面機能です。METI の用途分類では、湿式めっきは電気めっきと無電解めっき、溶融めっきは溶融金属への浸漬で皮膜を作る方法として整理されています。EPA も electroplating を、耐食、耐摩耗、抗摩擦、装飾などのための表面被覆として説明しています。  
出典: [METI](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf), [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines)

外注先や工程設計を考えるときは、電気めっきだけを見て終わらせず、前処理・洗浄・乾燥・排水処理・排ガス・後工程までを一連で見る必要があります。EPA は job plater と captive operation の両方を規制対象に含め、OSHA は装飾クロムめっきや六価クロム曝露の注意点を示しています。  
出典: [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines), [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 2. 用途別の見方

### 自動車

自動車では、めっきは「腐食しないこと」だけでは足りず、成形性、溶接性、部位ごとの耐食、量産安定性まで含めて選びます。日本鉄鋼連盟は、亜鉛めっき鋼板の用途を自動車・輸送機器、建築・土木、電気機器などに整理しており、自動車向けでは薄板・めっきに必要な機械的性質、寸法、形状、取引情報に加えて、めっき付着量や化成処理も規定する JFS の考え方を示しています。トヨタの資料では、亜鉛めっき鋼板のアーク溶接でブローホールが課題になり、MAG 条件の調整で全車種展開に結びつけた経緯が示されています。  
出典: [日本鉄鋼連盟](https://www.jisf.or.jp/business/tech/aen/index.html), [JFS](https://www.jisf.or.jp/business/standard/jfs/), [トヨタ](https://www.toyota.co.jp/jpn/company/history/75years/data/automotive_business/production/production_engineering/major_components/unit-field_stamping/engineering.html)

実務上は、ボディ外板と骨格部材で要求が違います。外板は外観・耐チッピング・耐白さび・塗装との相性、骨格や補強材は溶接適性と局所腐食が重要です。クロメートフリー化が進んでも、厳しい条件ではクロメート処理が残るという JISF の整理は、「環境優先で全部同じ」にできないことを示しています。  
出典: [日本鉄鋼連盟](https://www.jisf.or.jp/news/topics/070130.html), [日本鉄鋼連盟](https://www.jisf.or.jp/knowledge/variety/hyo.html)

### 電子部品

電子部品は、自動車以上に「接触の安定」「はんだ付け」「保存安定性」「複数回リフロー耐性」が効きます。JEITA は電子部品を、コネクタ、実装部品、センサーなどの相互接続部材として整理しており、車載・通信・医療など高信頼性市場向けで信頼性評価の重要性を強調しています。  
出典: [JEITA 電子部品部会](https://home.jeita.or.jp/ecb/about/part.html), [JEITA 信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)

PCB の表面仕上げは、HASL、OSP、ENIG、電解 Ni/Au、浸漬 Ag、浸漬 Sn などが代表です。IPC の比較資料では、OSP/ENIG/IAg が広く使われ、lead-free HASL は平坦性の再現が難しく、電解 Ni/Au は高コストとされています。ENIG 標準は、はんだ付けだけでなく、アルミワイヤボンド、press fit、接点用途まで含む多機能仕上げとして定義されています。  
出典: [IPC 比較資料](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf), [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)

PCB の品質判断は、見た目だけでは足りません。IPC-A-600 は、基材表面・内部状態、導体幅/間隔、annular ring、PTH の銅厚、ボイド、クラックまで受入基準に含めています。IPC-6012F は rigid board の qualification/performance の基準で、automotive addendum の基礎にもなっています。  
出典: [IPC-A-600](https://www.electronics.org/ipc-600-acceptability-printed-boards-endorsement-program), [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)

### 半導体周辺

半導体周辺では、めっきは「チップそのもの」よりも、パッケージ基板、リードフレーム、接続端子、バンプ、ワイヤボンド部で効いてきます。JEITA/ITRS のパッケージング資料では、フリップチップには OSP、無電解 Sn、ENIG が候補で、ワイヤボンドには電解 Ni/Au が候補として挙げられ、ENEPIG が両立案として有望とされています。つまり、万能な一種類ではなく、接合方式ごとに表面仕上げを使い分ける前提です。  
出典: [JEITA/ITRS 2007](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf)

さらに JEITA のアセンブリ＆パッケージング資料では、WLP と SiP が低コスト・高機能の解に位置づけられ、デバイスの複雑化はより高いコストのパッケージングで解く必要があると整理されています。半導体周辺では、めっき単価よりも、歩留まり・再加工性・検査設計の方が総コストを左右しやすいと読めます。  
出典: [JEITA/ITRS 2005](https://semicon.jeita.or.jp/STRJ/ITRS/2005/12_2005A%26P.pdf)

### 建材

建材では、耐食の長さとメンテナンス性が主役です。日本鉄鋼連盟の手引きでは、塗装亜鉛系めっき鋼板は亜鉛の犠牲防食と塗膜の保護で耐久性を高め、屋根・外壁・ウォールパネル・リフォームなどに使われると整理されています。塗装工程は現場塗装よりも、性能面・経済性・環境面で有利という位置づけです。  
出典: [塗装亜鉛系めっき鋼板の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)

また、屋外での耐久性は、材料そのものだけでなく保管・搬送・施工後養生の影響を強く受けます。高温多湿での保管、雨がかりの少ない部位、切り口処理、野積み時の浸水は、白さびやブリスターの引き金になります。建材は「めっき仕様」だけ見ても足りず、施工条件込みで設計するのが実務です。  
出典: [塗装亜鉛系めっき鋼板の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)

### 装飾

装飾用途では、めっきは見た目と耐変色性が前面に出ます。OSHA は、decorative/bright plating を、ニッケルなどの上に薄いクロムを析出させて、外観と耐変色性を得る用途と説明し、例としてホイール、家電、配管金具を挙げています。EPA も electroplating の用途に decorative purposes を含めています。  
出典: [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf), [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines)

装飾用途の判断では、厚い防食層よりも、光沢、色調、指紋汚れ、擦り傷、下地ニッケルとの相性が重要です。したがって、同じクロム系でも、自動車の機能部品とは評価軸がかなり違います。  
出典: [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 3. 方式の選び分け

めっき方式は、ざっくり次の軸で分けると判断しやすいです。  
出典: [METI](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf)

- 電気めっきは、導電性がある母材に電流を流して析出させるので、厚み管理と生産性を取りやすい一方、形状の電流集中に注意が要ります。
- 無電解めっきは、形状の回り込みが効きやすく、均一皮膜や非導電材料への適用で有利です。
- 溶融めっきは、大きな鋼材の耐食保護に強く、建材や鋼板での選択肢になります。
- ENIG/ENEPIG は、PCB・半導体周辺の接合互換性と保存安定性をまとめて取りにいく方式です。

選定のコツは、「何を守るか」を先に決めることです。耐食なら亜鉛系や塗装複合、導電接点なら Ni/Au 系、はんだ付け主導なら OSP/ENIG/浸漬 Sn/Ag、装飾なら bright chrome 系、という順で候補が自然に絞れます。  
出典: [IPC 比較資料](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf), [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf), [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 4. 工程・設備・外注先を見るポイント

外注先評価では、めっき槽そのものより、前処理、治具、洗浄、乾燥、分析、排水、排ガス、保全を一体で見るのが重要です。METI の PRTR 手引きは、めっき工程を代表的工程の一つとして扱い、工程ごとに原材料・添加剤・排出の考え方を分けています。EPA は、independent job platers と captive operations の両方を含めて規制しているので、外注型か内製型かよりも、工程管理の実力を見る方が本質です。  
出典: [METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf), [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines)

現場で確認したいのは、浴組成の管理記録、析出厚みの測定法、欠陥の見つけ方、ライン停止時の復旧手順、そしてクロスコンタミ防止です。IPC-4552 は ENIG に対して、ニッケル厚 3-6 µm、金厚 0.05 µm 以上、均一なめっき、接合性、清浄性、化学耐性、品質保証を要求しています。  
出典: [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)

設備観点では、排水処理と排ガス対策を「付帯設備」ではなく主設備の一部として扱うべきです。EPA はクロム工程や金属排出の規制を明示し、OSHA は六価クロム曝露を重要な安全論点として扱っています。つまり、めっきの量産能力は、浴の能力だけでなく公害・安全設備の処理能力で頭打ちになります。  
出典: [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines), [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 5. 品質・コスト・歩留まりの見方

品質は、外観よりも「使う条件で壊れないか」で見る方が失敗しにくいです。PCB なら平坦性、はんだ濡れ、PTH の銅厚、ボイド、クラック、保存後の再流し回数、接点抵抗を見ます。PCB の表面仕上げ比較では、各 finish に長所短所があり、複数回リフローや保存シミュレーションで差が出ると整理されています。  
出典: [IPC 比較資料](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf), [IPC-A-600](https://www.electronics.org/ipc-600-acceptability-printed-boards-endorsement-program)

半導体周辺では、めっきの歩留まりは単体の外観不良より、ワイヤボンド不良、フリップチップ接合不良、界面汚染、熱応力による剥離で失われやすいです。JEITA/ITRS は、組立と基板製造プロセスの最適化が量産の前提だと述べ、ENEPIG を含む複合表面仕上げの必要性を示しています。  
出典: [JEITA/ITRS 2007](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf)

建材と自動車では、初期コストだけでなく、再塗装・再処理・施工手戻りまで含めた総コストで見ます。塗装亜鉛系めっき鋼板の手引きは、保管・施工・切り口・雨がかり条件で劣化が進むと明記しており、材料単価が安くても現場損失が大きいと逆転しやすいことを示しています。  
出典: [塗装亜鉛系めっき鋼板の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)

## 6. 実務チェックリスト

- 何を一番守るかを一つに絞ったか。耐食、導通、はんだ、外観、摺動のうち、最優先を曖昧にしない。  
- 母材、形状、接合方式、使用環境を先に決めたか。自動車、PCB、半導体周辺、建材、装飾で要求は別物。  
- 方式を電気めっき、無電解、溶融、複合仕上げのどれにするか、理由付きで比較したか。  
- 厚み、均一性、密着、孔食、ボイド、接触抵抗、はんだ濡れのどれを合否にするか決めたか。  
- 前処理、洗浄、乾燥、排水処理、排ガス、測定の運用能力を外注先に確認したか。  
- job plater か captive かより、浴管理と欠陥解析の実力があるかを見たか。  
- 多重リフロー、保存、湿熱、塩水、振動、熱サイクルなど、実使用に近い条件で評価したか。  
- 量産歩留まりだけでなく、再加工性・手直し性・現場施工性まで見たか。  
- 規格や標準で縛れる部分と、個別仕様で詰める部分を分けたか。  
- コストは単価ではなく、工程数、検査、再処理、返品、保証まで含む総額で見たか。  

## 7. Reader decision layer

- この案件は、まず「防錆主導」か「導通主導」か「意匠主導」かを決める。  
- 自動車なら、溶接性と耐食の両立を優先し、必要ならクロメートフリーだけで押し切らない。  
- PCB なら、実装方式に合わせて OSP / ENIG / IAg / ISn / HASL を比較する。  
- 半導体周辺なら、ワイヤボンドとフリップチップで表面仕上げを分ける。  
- 建材なら、材料単体ではなく保管・施工・雨がかり条件を含めて選ぶ。  
- 装飾なら、見た目と耐変色を主評価にし、厚膜防食の発想を持ち込まない。  
- 外注先は、めっき厚より先に、前処理・洗浄・排水・分析・復旧手順を確認する。  
- 品質は外観合格だけでなく、実使用後の濡れ性、接触抵抗、剥離、腐食再現で判定する。  
- コストは加工単価ではなく、歩留まりと再処理コストまで入れて比較する。  
- 迷ったら、IPC / JEITA / JISF / METI / EPA のどの標準に乗せるかを先に決める。  

## 8. 不確実性と見直しポイント

今回の整理は、公開されている標準・団体資料・公的資料を中心にしたため、個別の材料系や浴組成、企業固有の量産ノウハウまでは踏み込んでいません。特に ENIG / ENEPIG、車載向け耐食、建材向け外装仕様は、実際には顧客規格と試験条件で大きく変わります。実案件では、最新版の IPC / JIS / 社内規格と、製品の使用環境データを合わせて再確認するのが安全です。  
出典: [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf), [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed), [JFS](https://www.jisf.or.jp/business/standard/jfs/)

## 参考ソース

- [METI 用途分類解説資料](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf)
- [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- [OSHA Electroplating Fact Sheet](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)
- [日本鉄鋼連盟 亜鉛鉄板](https://www.jisf.or.jp/business/tech/aen/index.html)
- [日本鉄鋼連盟 表面処理鋼板](https://www.jisf.or.jp/knowledge/variety/hyo.html)
- [日本鉄鋼連盟 塗装亜鉛系めっき鋼板ご使用の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)
- [日本鉄鋼連盟 JFS](https://www.jisf.or.jp/business/standard/jfs/)
- [トヨタ 75年史 ユニット系プレス・接合](https://www.toyota.co.jp/jpn/company/history/75years/data/automotive_business/production/production_engineering/major_components/unit-field_stamping/engineering.html)
- [IPC-4552 ENIG](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- [IPC Study of Various PCBA Surface Finishes](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf)
- [IPC-A-600 Acceptability of Printed Boards](https://www.electronics.org/ipc-600-acceptability-printed-boards-endorsement-program)
- [IPC-6012F Rigid Printed Boards](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
- [JEITA 電子部品の役割](https://home.jeita.or.jp/ecb/about/part.html)
- [JEITA 電子部品の信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)
- [JEITA/ITRS 2007 Assembly and Packaging](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf)
- [JEITA/ITRS 2005 Assembly & Packaging](https://semicon.jeita.or.jp/STRJ/ITRS/2005/12_2005A%26P.pdf)
```

---

## FILE: `notes/subagent-regulatory-ehs.md`

```text
# 規制・EHSメモ（めっき）

調査日: 2026-04-19  
対象: 六価クロムを中心に、日本・米国・EU の規制/EHS と日付依存論点を一次情報のみで整理

## まず押さえるべき結論

- 日本では、公共用水域・地下水の六価クロム環境基準が `2022-04-01` に `0.05 mg/L` から `0.02 mg/L` へ引き下げられた。これが後続の測定・検定方法見直しの直接の背景になっている。  
  URL: [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html)
- 日本の一般排水基準では、六価クロム化合物は `0.2 mg Cr(VI)/L`。環境基準より 1 桁緩いが、工場・事業場の排水口で適用される。  
  URL: [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
- `2024-02-05` に環境省が六価クロム化合物の測定方法を JIS K 0102-3 ベースへ見直し、分冊後の `JIS K0102-3 24.3.3` のフレーム原子吸光分析法を公定法から除外した。施行は `2024-04-01`。  
  URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
- 現行の暫定排水基準は、`2024-12-11` 時点で亜鉛の電気めっき業 `1 業種` のみで、`4 mg/L` を `2029-12-10` まで延長している。今回確認した公式資料では、六価クロムの暫定排水基準は見当たらなかった。  
  URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- 公共用水域への排出は水質汚濁防止法の排水規制で、排水基準は排水口で適用される。一方、公共下水道へ排除する場合は下水道法と条例に基づく除害施設・必要な措置が別途必要になる。  
  URL: [環境省 水濁法施行通達](https://www.env.go.jp/hourei/05/000137.html) / [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)
- 米国 OSHA の Chromium(VI) 標準は `5 µg/m³` の `8-hour TWA` を上限とし、規制区域、工学的・作業管理、PPE、医療監視、HazCom を要求する。  
  URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
- 米国 EPA は、`40 CFR Part 413` / `Part 433` の電気めっき・金属仕上げの排水規則を見直し中で、クロム仕上げ施設が PFAS の主要排出源になりうると整理している。  
  URL: [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines) / [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
- EU RoHS は電気電子機器の `hexavalent chromium` を含む `10 substances` を制限しており、ECHA の整理では `0.1 % w/w` の一様材料限度が示されている。  
  URL: [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) / [ECHA RoHS restricted substances](https://echa.europa.eu/en/restricted-subs-referred-art-4-rohs/-/legislationlist/substance/)
- REACH Annex XVII の nickel 規制では、ピアス等は `0.2 µg/cm²/week`、皮膚と長時間接触する製品は `0.5 µg/cm²/week` を超えてはならず、非ニッケル被膜も 2 年間の通常使用で `0.5` を超えないことが必要。  
  URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
- PFAS とクロム工程の関係は実務上かなり強い。EPA は、chrome plating のフューム抑制剤を対象に PFAS を調査しており、過去の PFOS 系代替や fume suppressant がクロムめっき工程に使われてきたことを公式に示している。  
  URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants) / [EPA proposed CERCLA PFOS/PFOA rule](https://www.epa.gov/system/files/documents/2022-08/FRL%207204-02-OLEM%20_%20Designating%20PFOA%20and%20PFOS%20as%20HSs%20_NPRM_20220823.pdf)

## 日本の論点

### 1) 六価クロムの環境基準改正と排水規制の連動

- `2022-04-01` 施行で、公共用水域・地下水の六価クロム環境基準は `0.05 mg/L` から `0.02 mg/L` に改正された。  
  URL: [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html)
- `2024-02-05` の改正では、六価クロム化合物の測定方法を分冊後の `JIS K0102-3` に合わせ、旧来のフレーム原子吸光分析法を公定法から外した。`2024-04-01` 施行なので、レポートでは「告示日」と「施行日」を分けて書くのが安全。  
  URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
- 一般排水基準は `0.2 mg Cr(VI)/L` で、これは工場・事業場の排水口での基準。環境基準 `0.02 mg/L` とは用途が違うので、同じ数字として扱わない。  
  URL: [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)

### 2) 暫定排水基準

- `2024-12-11` 時点の公式資料では、暫定排水基準が残っているのは亜鉛の電気めっき業のみで、`4 mg/L` を `2029-12-10` まで延長している。  
  URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- 六価クロムについては、今回の一次情報確認では「暫定排水基準あり」とは言えず、レポートでは「確認できた現行の暫定基準は亜鉛のみ」と書くのが安全。  
  URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)

### 3) 公共用水域と下水道の区別

- 水質汚濁防止法は、公共用水域に出る排出水を対象に排水規制をかけ、排水基準は排水口で適用される。  
  URL: [環境省 水濁法施行通達](https://www.env.go.jp/hourei/05/000137.html)
- 公共下水道へ排除する場合は、下水道法と条例に基づいて除害施設や必要な措置が必要になる。レポートでは「公共用水域向けの排水規制」と「公共下水道向けの除害規制」を分けて説明した方が誤解が少ない。  
  URL: [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)

## 米国の論点

### 4) OSHA Chromium(VI)

- OSHA の現行 Chromium(VI) 標準は `29 CFR 1910.1026` で、`5 µg/m³` の `8-hour TWA` を PEL としている。  
  URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
- OSHA は、`chromium (VI)` を癌、眼刺激、皮膚感作のハザードとして扱い、化学品の危険有害性情報、ラベル、SDS、教育訓練を要求している。  
  URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)

### 5) EPA の電気めっき/クロム規則

- EPA の電気めっき排水ガイドラインは、`1974` 制定の `40 CFR Part 413` を基礎にしつつ、現行の `40 CFR Part 433` と合わせて、間接排出・直接排出の区別を持っている。  
  URL: [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- EPA は、`chrome finishing facilities` が PFAS 排出の主な供給源になりうるとして、`chromium plating`、`chromium anodizing`、`chromic acid etching`、`chromate conversion coating` を個別に追跡している。  
  URL: [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
- EPA の 2022 年提案資料では、`chrome plating` を含む製造工程や、`wetting agent / fume suppressant` を使う plating process が PFAS の発生源として列挙されている。  
  URL: [EPA proposed CERCLA PFOS/PFOA rule](https://www.epa.gov/system/files/documents/2022-08/FRL%207204-02-OLEM%20_%20Designating%20PFOA%20and%20PFOS%20as%20HSs%20_NPRM_20220823.pdf)

### 6) PFAS とクロム工程

- EPA は chrome plating 施設 11 か所の fume suppressants と effluent を分析し、現在使用されている一部の抑制剤に PFAS が含まれているかを確認している。`PFOS-free` 製品でも、過去世代の抑制剤の残留が疑われるケースがある。  
  URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants)
- これを受けて、レポートでは「PFAS はクロムめっきそのものの規制物質ではないが、フューム抑制剤・湿潤剤として工程に入りやすく、排水と残留の論点が結びつく」と整理すると分かりやすい。  
  URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants)

## EU の論点

### 7) RoHS

- EU RoHS は、電気電子機器での `hexavalent chromium` の使用を含む `10 substances` を制限している。  
  URL: [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en)
- ECHA の RoHS 制限一覧では、hexavalent chromium の homogeneous material limit が `0.1 % w/w` とされている。  
  URL: [ECHA RoHS restricted substances](https://echa.europa.eu/en/restricted-subs-referred-art-4-rohs/-/legislationlist/substance/)

### 8) REACH Annex XVII の nickel release

- REACH Annex XVII の nickel 規制は、ピアス用 post assembly で `0.2 µg/cm²/week` 未満、皮膚と直接・長時間接触する製品で `0.5 µg/cm²/week` 以下を求める。  
  URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
- 製品の non-nickel coating についても、少なくとも `2 years` の通常使用で `0.5 µg/cm²/week` を超えないことが必要で、めっき品質や皮膚接触用途の設計条件に直結する。  
  URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)

## report に入れるべき regulatory / temporal claims

1. `2022-04-01` に、日本の公共用水域・地下水の六価クロム環境基準は `0.05 mg/L` から `0.02 mg/L` へ改正された。  
   URL: [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html)
2. `2024-02-05` に、六価クロム化合物の測定方法が `JIS K0102-3` ベースへ見直され、`JIS K0102-3 24.3.3` のフレーム原子吸光分析法は公定法から除外された。  
   URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
3. `2024-04-01` 施行のため、2024 年以降の六価クロムの分析・適合判断は、改正後の方法で整理する必要がある。  
   URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
4. 日本の一般排水基準では、六価クロム化合物は `0.2 mg Cr(VI)/L` である。  
   URL: [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
5. `2024-12-11` 時点で、暫定排水基準が残るのは亜鉛の電気めっき業のみで、`4 mg/L` が `2029-12-10` まで延長された。  
   URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
6. 公共用水域への排出は水質汚濁防止法の排水規制で、排水基準は排水口で適用される。  
   URL: [環境省 水濁法施行通達](https://www.env.go.jp/hourei/05/000137.html)
7. 公共下水道へ排除する場合は、下水道法と条例に基づく除害施設・必要な措置が別途必要である。  
   URL: [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)
8. OSHA の Chromium(VI) 標準は `5 µg/m³` の `8-hour TWA` を PEL とし、職場の規制区域・工学的対策・医療監視・危険有害性コミュニケーションを要求する。  
   URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
9. EPA は `40 CFR Part 413` と `Part 433` の電気めっき/金属仕上げ排水規則を見直しており、クロム仕上げ施設を PFAS 排出源として追跡している。  
   URL: [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines) / [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
10. EU RoHS は hexavalent chromium を制限対象に含み、ECHA では homogeneous material の上限が `0.1 % w/w` と整理されている。  
    URL: [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) / [ECHA RoHS restricted substances](https://echa.europa.eu/en/restricted-subs-referred-art-4-rohs/-/legislationlist/substance/)
11. REACH Annex XVII の nickel release 条件は、`0.2 µg/cm²/week` と `0.5 µg/cm²/week` の 2 段階で、皮膚接触製品のめっき仕様に直接影響する。  
    URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
12. PFAS は chrome plating 工程の fume suppressant と結びつきやすく、EPA も chrome plating 施設での PFAS 使用・排出を調査対象としている。  
    URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants) / [EPA proposed CERCLA PFOS/PFOA rule](https://www.epa.gov/system/files/documents/2022-08/FRL%207204-02-OLEM%20_%20Designating%20PFOA%20and%20PFOS%20as%20HSs%20_NPRM_20220823.pdf)

```
