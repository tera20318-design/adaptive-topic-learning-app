# Query Plan

Topic: めっき
Preset logic milestone: `OUTPUT`
Topic scope: `standard` (`inferred`, breadth score `50`)
Topic stop profile: standard / 標準 / score 50; floors q=40, candidates=359, deep=37; stop novelty=0.0350, same-domain=0.1600
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
- めっき 企業一覧
- めっき 会社一覧
- めっき 会員企業
- めっき 出展社一覧
- めっき 事業所一覧
- めっき directory

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
- `### 4.1 定義・範囲・前提`
- `### 4.2 歴史・変遷・現在地`
- `### 4.3 主要方式・方法・類型`
- `### 4.4 構成要素・材料・入力条件`
- `### 4.5 評価軸・性能・品質`
- `### 4.6 規格・制度・標準`
- `### 4.7 工程・設備・供給構造`
- `### 4.8 環境・安全・制約`
- `### 4.9 用途・適用領域・導入先`
- `### 4.10 コスト・経済性・導入条件`
- `### 4.11 ドメインリスクマップ`

Required logic artifacts:
- `notes/topic-profile.md`
- `notes/contradiction-log.md`
- `notes/upstream-downstream-map.md`
- `notes/role-structure-matrix.md`
- `notes/domain-risk-map.md`

Status guidance: use `pending`, `in_progress`, `covered`, `skipped`, or `blocked`.

| Family ID | Required | Query family | Goal | Example queries | Status |
| --- | --- | --- | --- | --- | --- |
| `official_primary` | required | 一次・公式 | Find original documents and first-party evidence. | `めっき official`; `めっき documentation`; `めっき pdf` | pending |
| `regulation_standards` | required | 規制・標準 | Find laws, guidelines, standards, and regulator material. | `めっき regulation`; `めっき guideline`; `めっき standard` | pending |
| `research_validation` | required | 研究・検証 | Find papers, benchmarks, and technical validation. | `めっき paper`; `めっき benchmark`; `めっき evaluation` | pending |
| `vendor_implementation` | required | ベンダー実装 | Find first-party implementation details, products, and case studies. | `めっき vendor`; `めっき case study`; `めっき deployment` | pending |
| `independent_context` | required | 独立コンテキスト | Find reputable external analysis and comparison context. | `めっき analysis`; `めっき review`; `めっき outlook` | pending |
| `japan_specific` | required | 日本語・国内 | Find Japan-specific and local-language sources. | `めっき 日本`; `めっき 国内`; `めっき ガイドライン` | pending |
| `contradiction_negative` | required | 反証・不在確認 | Look for contradictions, absences, and counterexamples. | `めっき not found`; `めっき 未確認`; `めっき 不在` | pending |
| `upstream_downstream` | required | 上流/下流 | Trace suppliers, customers, adjacent process steps, and commercial flow. | `めっき supplier customer`; `めっき 取引先`; `めっき 関係会社` | pending |
| `role_structure` | required | 役割差・類型 | Map the role differences, segmentation, and structure of the landscape. | `めっき positioning`; `めっき role difference`; `めっき 類型` | pending |
| `chronology_change` | required | 時系列・変化点 | Check chronology, change over time, and why the current year differs. | `めっき timeline`; `めっき 2025 2026`; `めっき 変化` | pending |
