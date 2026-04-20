# Query Plan

Topic: めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合
Preset logic milestone: `M4`
Topic scope: `standard` (`inferred`, breadth score `50`)
Topic stop profile: standard / 標準 / score 50; floors q=31, candidates=292, deep=30; stop novelty=0.0400, same-domain=0.1800
Entity discovery: auto (`inferred`, score `40`)
Discovery kind: `technology` (`inferred`, score `40`)
Discovery bundle: `技術・研究ロスター`
Discovery family: `technology_surface_discovery`
Entity discovery profile: auto / required / kind technology / bundle 技術・研究ロスター; score 40; surface_floor=3, tail_queries=2

Discovery surfaces:
- papers
- benchmarks
- patents
- standards
- proceedings
- technical docs

Discovery query hints:
- めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 paper
- めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 benchmark
- めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 patent
- めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 standard
- めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 proceedings
- めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 技術資料

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
| `official_primary` | required | 一次・公式 | Find original documents and first-party evidence. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 official`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 documentation`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 pdf` | pending |
| `regulation_standards` | required | 規制・標準 | Find laws, guidelines, standards, and regulator material. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 regulation`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 guideline`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 standard` | pending |
| `research_validation` | required | 研究・検証 | Find papers, benchmarks, and technical validation. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 paper`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 benchmark`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 evaluation` | pending |
| `vendor_implementation` | required | ベンダー実装 | Find first-party implementation details, products, and case studies. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 vendor`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 case study`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 deployment` | pending |
| `independent_context` | required | 独立コンテキスト | Find reputable external analysis and comparison context. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 analysis`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 review`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 outlook` | pending |
| `japan_specific` | required | 日本語・国内 | Find Japan-specific and local-language sources. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 日本`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 国内`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 ガイドライン` | pending |
| `contradiction_negative` | required | 反証・不在確認 | Look for contradictions, absences, and counterexamples. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 not found`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 未確認`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 不在` | pending |
| `upstream_downstream` | required | 上流/下流 | Trace suppliers, customers, adjacent process steps, and commercial flow. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 supplier customer`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 取引先`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 関係会社` | pending |
| `role_structure` | required | 役割差・類型 | Map the role differences, segmentation, and structure of the landscape. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 positioning`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 role difference`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 類型` | pending |
| `chronology_change` | required | 時系列・変化点 | Check chronology, change over time, and why the current year differs. | `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 timeline`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 2025 2026`; `めっき（plating）の技術的基礎：定義、方式、代表皮膜金属、工程、品質指標、長所短所、不具合 変化` | pending |
