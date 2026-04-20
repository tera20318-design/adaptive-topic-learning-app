# Evidence Gap Follow-up

- Run ID: 20260419-025714-research
- Topic: めっき
- Preset: dr_ultra
- Topic breadth: standard (inferred, score 50)
- Topic budget scale: 1.0
- Topic stop posture: standard / 標準 / score 50; floors q=31, candidates=292, deep=30; stop novelty=0.0400, same-domain=0.1800
- Entity discovery: auto (inferred, score 32)
- Weak or missing claims: 7

Use the query families below to close gaps, then append new hits to `sources/search-results.tsv`,
rerun `normalize_sources.py`, rebuild `claim-ledger.tsv`, and check `check_evidence_gaps.py` again.

## Priority order

| Rank | Claim ID | Kind | Evidence gap | Primary gap | Severity |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | `claim-002` | fact | 1 | 1 | 6 |
| 2 | `claim-003` | fact | 1 | 1 | 6 |
| 3 | `claim-004` | fact | 1 | 1 | 6 |
| 4 | `claim-001` | fact | 0 | 1 | 4 |
| 5 | `claim-005` | fact | 1 | 0 | 3 |
| 6 | `claim-006` | fact | 1 | 0 | 3 |
| 7 | `claim-007` | fact | 1 | 0 | 3 |

## Claim-level follow-up

## claim-002

- Claim kind: fact
- Claim text: 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。
- Gap note: needs >= 2 sources (has 1); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 not found`
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 未確認`
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 supplier customer`
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 取引先`
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 positioning`
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 role difference`
  - `めっき 電気めっき、無電解めっき、真空めっき、溶融めっきは強みが異なる。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-003

- Claim kind: fact
- Claim text: 品質評価の中核は膜厚、密着性、耐食性、硬さである。
- Gap note: needs >= 2 sources (has 1); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 not found`
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 未確認`
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 supplier customer`
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 取引先`
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 positioning`
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 role difference`
  - `めっき 品質評価の中核は膜厚、密着性、耐食性、硬さである。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-004

- Claim kind: fact
- Claim text: 溶融亜鉛めっきは明確な工程分解で理解できる。
- Gap note: needs >= 2 sources (has 1); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 not found`
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 未確認`
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 supplier customer`
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 取引先`
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 positioning`
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 role difference`
  - `めっき 溶融亜鉛めっきは明確な工程分解で理解できる。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-001

- Claim kind: fact
- Claim text: 日本の技術文脈では「めっき」は広義の表面処理として使われる。
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 not found`
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 未確認`
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 supplier customer`
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 取引先`
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 positioning`
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 role difference`
  - `めっき 日本の技術文脈では「めっき」は広義の表面処理として使われる。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-005

- Claim kind: fact
- Claim text: 六価クロムとシアンは日本の排水規制上の中心論点である。
- Gap note: needs >= 2 sources (has 1)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 not found`
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 未確認`
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 supplier customer`
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 取引先`
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 positioning`
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 role difference`
  - `めっき 六価クロムとシアンは日本の排水規制上の中心論点である。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-006

- Claim kind: fact
- Claim text: 六価クロムの環境基準は 2022年4月1日に強化された。
- Gap note: needs >= 2 sources (has 1)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 not found`
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 未確認`
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 supplier customer`
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 取引先`
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 positioning`
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 role difference`
  - `めっき 六価クロムの環境基準は 2022年4月1日に強化された。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-007

- Claim kind: fact
- Claim text: 東京都では電気めっき業向けの暫定排水基準が案内されている。
- Gap note: needs >= 2 sources (has 1)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 not found`
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 未確認`
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 supplier customer`
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 取引先`
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 positioning`
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 role difference`
  - `めっき 東京都では電気めっき業向けの暫定排水基準が案内されている。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.
