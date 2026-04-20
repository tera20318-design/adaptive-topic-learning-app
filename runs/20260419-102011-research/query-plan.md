# Query Plan

Topic: めっきの産業用途と市場・実務観点
Preset logic milestone: `M4`
Topic scope: `standard` (`inferred`, breadth score `58`)
Topic stop profile: standard / 標準 / score 58; floors q=31, candidates=292, deep=30; stop novelty=0.0400, same-domain=0.1800
Entity discovery: auto (`inferred`, score `32`)
Discovery kind: `company` (`inferred`, score `32`)
Discovery bundle: `企業・事業所ロスター`
Discovery family: `entity_discovery`
Entity discovery profile: auto / optional / kind company / bundle 企業・事業所ロスター; score 32; surface_floor=0, tail_queries=0

Discovery surfaces:
- 企業一覧
- 会社一覧
- 会員企業
- 出展社一覧
- 事業所一覧
- directory pages

Discovery query hints:
- めっきの産業用途と市場・実務観点 企業一覧
- めっきの産業用途と市場・実務観点 会社一覧
- めっきの産業用途と市場・実務観点 会員企業
- めっきの産業用途と市場・実務観点 出展社一覧
- めっきの産業用途と市場・実務観点 事業所一覧
- めっきの産業用途と市場・実務観点 directory

Required query families:
- `official_primary`: 一次・公式
- `regulation_standards`: 規制・標準
- `research_validation`: 研究・検証
- `vendor_implementation`: ベンダー実装
- `independent_context`: 独立コンテキスト
- `japan_specific`: 日本語・国内
- `contradiction_negative`: 反証・不在確認
- `upstream_downstream`: 上流/下流
- `role_structure`: 役割差・類型
- `chronology_change`: 時系列・変化点

Required report sections:
- `## 1. 要約`
- `## 2. 主要な発見`
- `## 3. 根拠テーブル`
- `## 4. 詳細分析`
- `## 5. 実務で確認すべきことと追加調査`
- `## 6. 主要ソース一覧`
- `### 4.1 比較マトリクス`
- `### 4.2 主要な差分と含意`
- `### 4.3 役割差または類型`
- `### 4.4 上流/下流または主体ネットワーク`
- `### 4.5 反証・例外・境界条件`
- `### 4.6 時系列・変化点`
- `### 4.7 ドメインリスクマップ`

Required logic artifacts:
- `notes/topic-profile.md`
- `notes/contradiction-log.md`
- `notes/upstream-downstream-map.md`
- `notes/role-structure-matrix.md`
- `notes/domain-risk-map.md`

Status guidance: use `pending`, `in_progress`, `covered`, `skipped`, or `blocked`.

| Family ID | Required | Query family | Goal | Example queries | Status |
| --- | --- | --- | --- | --- | --- |
| `official_primary` | required | 一次・公式 | Find original documents and first-party evidence. | `めっきの産業用途と市場・実務観点 official`; `めっきの産業用途と市場・実務観点 documentation`; `めっきの産業用途と市場・実務観点 pdf` | pending |
| `regulation_standards` | required | 規制・標準 | Find laws, guidelines, standards, and regulator material. | `めっきの産業用途と市場・実務観点 regulation`; `めっきの産業用途と市場・実務観点 guideline`; `めっきの産業用途と市場・実務観点 standard` | pending |
| `research_validation` | required | 研究・検証 | Find papers, benchmarks, and technical validation. | `めっきの産業用途と市場・実務観点 paper`; `めっきの産業用途と市場・実務観点 benchmark`; `めっきの産業用途と市場・実務観点 evaluation` | pending |
| `vendor_implementation` | required | ベンダー実装 | Find first-party implementation details, products, and case studies. | `めっきの産業用途と市場・実務観点 vendor`; `めっきの産業用途と市場・実務観点 case study`; `めっきの産業用途と市場・実務観点 deployment` | pending |
| `independent_context` | required | 独立コンテキスト | Find reputable external analysis and comparison context. | `めっきの産業用途と市場・実務観点 analysis`; `めっきの産業用途と市場・実務観点 review`; `めっきの産業用途と市場・実務観点 outlook` | pending |
| `japan_specific` | required | 日本語・国内 | Find Japan-specific and local-language sources. | `めっきの産業用途と市場・実務観点 日本`; `めっきの産業用途と市場・実務観点 国内`; `めっきの産業用途と市場・実務観点 ガイドライン` | pending |
| `contradiction_negative` | required | 反証・不在確認 | Look for contradictions, absences, and counterexamples. | `めっきの産業用途と市場・実務観点 not found`; `めっきの産業用途と市場・実務観点 未確認`; `めっきの産業用途と市場・実務観点 不在` | pending |
| `upstream_downstream` | required | 上流/下流 | Trace suppliers, customers, adjacent process steps, and commercial flow. | `めっきの産業用途と市場・実務観点 supplier customer`; `めっきの産業用途と市場・実務観点 取引先`; `めっきの産業用途と市場・実務観点 関係会社` | pending |
| `role_structure` | required | 役割差・類型 | Map the role differences, segmentation, and structure of the landscape. | `めっきの産業用途と市場・実務観点 positioning`; `めっきの産業用途と市場・実務観点 role difference`; `めっきの産業用途と市場・実務観点 類型` | pending |
| `chronology_change` | required | 時系列・変化点 | Check chronology, change over time, and why the current year differs. | `めっきの産業用途と市場・実務観点 timeline`; `めっきの産業用途と市場・実務観点 2025 2026`; `めっきの産業用途と市場・実務観点 変化` | pending |
