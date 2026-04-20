# Query Plan

Topic: めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減）
Preset logic milestone: `M4`
Topic scope: `standard` (`inferred`, breadth score `57`)
Topic stop profile: standard / 標準 / score 57; floors q=31, candidates=292, deep=30; stop novelty=0.0400, same-domain=0.1800
Entity discovery: auto (`inferred`, score `40`)
Discovery kind: `policy` (`inferred`, score `40`)
Discovery bundle: `政策・制度ロスター`
Discovery family: `policy_surface_discovery`
Entity discovery profile: auto / required / kind policy / bundle 政策・制度ロスター; score 40; surface_floor=3, tail_queries=2

Discovery surfaces:
- 法令
- 指針
- 通達
- FAQ
- 公募
- notice pages

Discovery query hints:
- めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 法令
- めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 指針
- めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 通達
- めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） FAQ
- めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 公募
- めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） notice

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
| `official_primary` | required | 一次・公式 | Find original documents and first-party evidence. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） official`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） documentation`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） pdf` | pending |
| `regulation_standards` | required | 規制・標準 | Find laws, guidelines, standards, and regulator material. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） regulation`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） guideline`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） standard` | pending |
| `research_validation` | required | 研究・検証 | Find papers, benchmarks, and technical validation. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） paper`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） benchmark`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） evaluation` | pending |
| `vendor_implementation` | required | ベンダー実装 | Find first-party implementation details, products, and case studies. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） vendor`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） case study`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） deployment` | pending |
| `independent_context` | required | 独立コンテキスト | Find reputable external analysis and comparison context. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） analysis`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） review`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） outlook` | pending |
| `japan_specific` | required | 日本語・国内 | Find Japan-specific and local-language sources. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 日本`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 国内`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） ガイドライン` | pending |
| `contradiction_negative` | required | 反証・不在確認 | Look for contradictions, absences, and counterexamples. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） not found`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 未確認`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 不在` | pending |
| `upstream_downstream` | required | 上流/下流 | Trace suppliers, customers, adjacent process steps, and commercial flow. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） supplier customer`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 取引先`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 関係会社` | pending |
| `role_structure` | required | 役割差・類型 | Map the role differences, segmentation, and structure of the landscape. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） positioning`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） role difference`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 類型` | pending |
| `chronology_change` | required | 時系列・変化点 | Check chronology, change over time, and why the current year differs. | `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） timeline`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 2025 2026`; `めっきの環境・安全・規制動向（排水処理、有害物質、六価クロム/三価クロム、ニッケルアレルギー、RoHS/REACH、労働安全、環境負荷低減） 変化` | pending |
