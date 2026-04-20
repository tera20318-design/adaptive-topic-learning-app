# Query Plan

Topic: めっき
Preset logic milestone: `M4` (`dr_ultra` logic scaffold only; this is not a full dr_ultra-equivalent run)
Topic scope: `standard` (`manual_override`, breadth score `50`)
Topic stop profile: standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800
Entity discovery: off (`manual_override`, score `0`)
Discovery kind: `technology` (`manual_override`, score `0`)
Discovery bundle: `general overview`
Discovery family: `independent_context`
Entity discovery profile: off / optional / kind technology / bundle general overview; score 0; surface_floor=0, tail_queries=0
Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
Override authority: user
Full DR equivalent: no (scoped or lighter-than-full DR)
Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.

Discovery surfaces:
- method definitions and boundary conditions
- electroplating / electroless / hot-dip / dry-process distinctions
- quality and failure-mode terminology
- regulatory layers: wastewater, air, worker exposure, RoHS, REACH, nickel release
- electronics-specific reliability caveats
- Japan-specific regulatory changes and implementation context

Discovery query hints:
- めっき 定義 表面処理 違い
- めっき 電気めっき 無電解めっき 違い
- めっき 規制 排水 六価クロム
- めっき OSHA chromium VI
- めっき RoHS REACH nickel release
- めっき microvia reliability

Required query families:
- `official_primary`: 一次情報・公式情報
- `regulation_standards`: 法令・基準・規格
- `research_validation`: 技術的な検証・信頼性
- `vendor_implementation`: 実装・工程・用途の具体例
- `independent_context`: 業界文脈と比較
- `japan_specific`: 日本語・日本制度
- `contradiction_negative`: 反証・境界条件
- `upstream_downstream`: 前後工程と主体関係
- `role_structure`: 用途別・役割別の整理
- `chronology_change`: 日付・制度変更

Required report sections:
- `## 1. 結論`
- `## 2. 読み手が最初に押さえるべきこと`
- `## 3. 主要な根拠と出典`
- `## 4. 論点別の分析`
- `## 5. 判断のために確認すべきことと追加調査`
- `## 6. 主な情報源`
- `### 4.1 方式比較の見取り図`
- `### 4.2 何が選定を分けるか`
- `### 4.3 用途別に見た方式の役割`
- `### 4.4 工程全体と関係者のつながり`
- `### 4.5 例外条件と誤解しやすい境界`
- `### 4.6 直近の制度変更と日付`
- `### 4.7 見落としやすい実務リスク`

Required logic artifacts:
- `notes/topic-profile.md`
- `notes/contradiction-log.md`
- `notes/upstream-downstream-map.md`
- `notes/role-structure-matrix.md`
- `notes/domain-risk-map.md`

Status guidance: use `pending`, `in_progress`, `covered`, `covered_by_mapping`, `waived`, or `not_covered`.

| Family ID | Required | Query family | Goal | Example queries | Status | Coverage | Coverage evidence | Waiver reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `official_primary` | required | 一次情報・公式情報 | Find original documents and first-party evidence. | `めっき official`; `めっき documentation`; `めっき pdf` | covered | covered | Direct official citations from `env.go.jp`, `osha.gov`, `eur-lex.europa.eu`, and `echa.europa.eu`. | - |
| `regulation_standards` | required | 法令・基準・規格 | Find laws, guidelines, standards, and regulator material. | `めっき regulation`; `めっき guideline`; `めっき standard` | covered | covered | Wastewater, OSHA, RoHS, and REACH claims are grounded in regulator or legal-text sources. | - |
| `research_validation` | required | 技術的な検証・信頼性 | Find papers, benchmarks, and technical validation. | `めっき paper`; `めっき benchmark`; `めっき evaluation` | covered_by_mapping | covered_by_mapping | `jcu-i.com`, `orist.jp`, and `ipc.org` cover reliability and technical caveats even though this focused pass did not preserve many explicit family-tagged search strings. | - |
| `vendor_implementation` | required | 実装・工程・用途の具体例 | Find first-party implementation details, products, and case studies. | `めっき vendor`; `めっき case study`; `めっき deployment` | covered_by_mapping | covered_by_mapping | Fuji Electric, ULVAC, and JCU were cited for implementation details, process framing, and application examples. | - |
| `independent_context` | required | 業界文脈と比較 | Find reputable external analysis and comparison context. | `めっき analysis`; `めっき review`; `めっき outlook` | covered_by_mapping | covered_by_mapping | SFJ, Zentoren, Kizaikou, and ORIST provide non-vendor context and comparison framing. | - |
| `japan_specific` | required | 日本語・日本制度 | Find Japan-specific and local-language sources. | `めっき 日本`; `めっき ガイドライン`; `めっき 六価クロム` | covered_by_mapping | covered_by_mapping | The report depends on Japan-facing sources such as `env.go.jp`, Osaka prefecture, SFJ, Zentoren, and related organizations. | - |
| `contradiction_negative` | required | 反証・境界条件 | Look for contradictions, absences, and counterexamples. | `めっき not found`; `めっき 未確認`; `めっき 例外` | covered_by_mapping | covered_by_mapping | `notes/contradiction-log.md` and report section `4.5` explicitly capture over-generalization risks and boundary cases. | - |
| `upstream_downstream` | required | 前後工程と主体関係 | Trace suppliers, customers, adjacent process steps, and commercial flow. | `めっき supplier customer`; `めっき 前後工程`; `めっき 関係者` | covered_by_mapping | covered_by_mapping | `notes/upstream-downstream-map.md` and report section `4.4` cover pretreatment, plating, post-treatment, wastewater/air treatment, and customer quality handoff. | - |
| `role_structure` | required | 用途別・役割別の整理 | Map role differences, segmentation, and structure. | `めっき positioning`; `めっき role difference`; `めっき 用途別` | covered_by_mapping | covered_by_mapping | `notes/role-structure-matrix.md` and report section `4.3` split method roles by application and failure mode. | - |
| `chronology_change` | required | 日付・制度変更 | Check chronology, change over time, and why the current year differs. | `めっき timeline`; `めっき 2024 2026`; `めっき 施行日` | covered_by_mapping | covered_by_mapping | Report section `4.6` and the cited `2024-02-05` / `2024-04-01` changes provide the chronology layer. | - |
