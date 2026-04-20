# Evidence Gap Follow-up

- Run ID: 20260419-101901-research
- Topic: めっき
- Preset: dr_ultra
- Topic breadth: standard (manual_override, score 50)
- Topic budget scale: 0.45
- Topic stop posture: standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800
- Entity discovery: off (manual_override, score 0)
- Weak or missing claims: 67

Use the query families below to close gaps, then append new hits to `sources/search-results.tsv`,
rerun `normalize_sources.py`, rebuild `claim-ledger.tsv`, and check `check_evidence_gaps.py` again.

## Priority order

| Rank | Claim ID | Kind | Evidence gap | Primary gap | Severity |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | `claim-099` | advice | 2 | 1 | 9 |
| 2 | `claim-124` | advice | 2 | 1 | 9 |
| 3 | `claim-022` | fact | 2 | 1 | 8 |
| 4 | `claim-035` | fact | 2 | 1 | 8 |
| 5 | `claim-040` | fact | 2 | 1 | 8 |
| 6 | `claim-044` | fact | 2 | 1 | 8 |
| 7 | `claim-048` | fact | 2 | 1 | 8 |
| 8 | `claim-052` | fact | 2 | 1 | 8 |
| 9 | `claim-058` | fact | 2 | 1 | 8 |
| 10 | `claim-036` | advice | 0 | 1 | 5 |
| 11 | `claim-076` | advice | 0 | 1 | 5 |
| 12 | `claim-109` | advice | 0 | 1 | 5 |
| 13 | `claim-110` | advice | 0 | 1 | 5 |
| 14 | `claim-111` | advice | 0 | 1 | 5 |
| 15 | `claim-115` | advice | 0 | 1 | 5 |
| 16 | `claim-116` | advice | 0 | 1 | 5 |
| 17 | `claim-117` | advice | 0 | 1 | 5 |
| 18 | `claim-125` | advice | 0 | 1 | 5 |
| 19 | `claim-126` | advice | 0 | 1 | 5 |
| 20 | `claim-144` | advice | 0 | 1 | 5 |
| 21 | `claim-145` | advice | 0 | 1 | 5 |
| 22 | `claim-146` | advice | 0 | 1 | 5 |
| 23 | `claim-150` | advice | 0 | 1 | 5 |
| 24 | `claim-151` | advice | 0 | 1 | 5 |
| 25 | `claim-152` | advice | 0 | 1 | 5 |
| 26 | `claim-159` | advice | 0 | 1 | 5 |
| 27 | `claim-160` | advice | 0 | 1 | 5 |
| 28 | `claim-055` | temporal | 1 | 0 | 4 |
| 29 | `claim-091` | temporal | 1 | 0 | 4 |
| 30 | `claim-002` | fact | 0 | 1 | 4 |
| 31 | `claim-014` | fact | 0 | 1 | 4 |
| 32 | `claim-041` | fact | 0 | 1 | 4 |
| 33 | `claim-042` | fact | 0 | 1 | 4 |
| 34 | `claim-043` | fact | 0 | 1 | 4 |
| 35 | `claim-046` | fact | 0 | 1 | 4 |
| 36 | `claim-080` | fact | 0 | 1 | 4 |
| 37 | `claim-081` | fact | 0 | 1 | 4 |
| 38 | `claim-082` | fact | 0 | 1 | 4 |
| 39 | `claim-084` | fact | 0 | 1 | 4 |
| 40 | `claim-004` | temporal | 0 | 0 | 2 |
| 41 | `claim-010` | temporal | 0 | 0 | 2 |
| 42 | `claim-011` | regulatory | 0 | 0 | 2 |
| 43 | `claim-038` | regulatory | 0 | 0 | 2 |
| 44 | `claim-039` | regulatory | 0 | 0 | 2 |
| 45 | `claim-045` | regulatory | 0 | 0 | 2 |
| 46 | `claim-047` | regulatory | 0 | 0 | 2 |
| 47 | `claim-051` | regulatory | 0 | 0 | 2 |
| 48 | `claim-061` | temporal | 0 | 0 | 2 |
| 49 | `claim-063` | regulatory | 0 | 0 | 2 |
| 50 | `claim-078` | regulatory | 0 | 0 | 2 |
| 51 | `claim-079` | regulatory | 0 | 0 | 2 |
| 52 | `claim-083` | regulatory | 0 | 0 | 2 |
| 53 | `claim-085` | regulatory | 0 | 0 | 2 |
| 54 | `claim-088` | regulatory | 0 | 0 | 2 |
| 55 | `claim-096` | temporal | 0 | 0 | 2 |
| 56 | `claim-098` | regulatory | 0 | 0 | 2 |
| 57 | `claim-118` | regulatory | 0 | 0 | 2 |
| 58 | `claim-120` | regulatory | 0 | 0 | 2 |
| 59 | `claim-121` | regulatory | 0 | 0 | 2 |
| 60 | `claim-123` | regulatory | 0 | 0 | 2 |
| 61 | `claim-129` | regulatory | 0 | 0 | 2 |
| 62 | `claim-133` | regulatory | 0 | 0 | 2 |
| 63 | `claim-153` | regulatory | 0 | 0 | 2 |
| 64 | `claim-155` | regulatory | 0 | 0 | 2 |
| 65 | `claim-156` | regulatory | 0 | 0 | 2 |
| 66 | `claim-158` | regulatory | 0 | 0 | 2 |
| 67 | `claim-163` | regulatory | 0 | 0 | 2 |

## Claim-level follow-up

## claim-099

- Claim kind: advice
- Claim text: ### 5.1 選定前の実務チェックリスト
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 5.1 選定前の実務チェックリスト not found`
  - `めっき ### 5.1 選定前の実務チェックリスト 未確認`
  - `めっき ### 5.1 選定前の実務チェックリスト 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 5.1 選定前の実務チェックリスト supplier customer`
  - `めっき ### 5.1 選定前の実務チェックリスト 取引先`
  - `めっき ### 5.1 選定前の実務チェックリスト 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 5.1 選定前の実務チェックリスト positioning`
  - `めっき ### 5.1 選定前の実務チェックリスト role difference`
  - `めっき ### 5.1 選定前の実務チェックリスト 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-124

- Claim kind: advice
- Claim text: ### 5.2 判断を誤らないための運用ルール
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 5.2 判断を誤らないための運用ルール not found`
  - `めっき ### 5.2 判断を誤らないための運用ルール 未確認`
  - `めっき ### 5.2 判断を誤らないための運用ルール 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 5.2 判断を誤らないための運用ルール supplier customer`
  - `めっき ### 5.2 判断を誤らないための運用ルール 取引先`
  - `めっき ### 5.2 判断を誤らないための運用ルール 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 5.2 判断を誤らないための運用ルール positioning`
  - `めっき ### 5.2 判断を誤らないための運用ルール role difference`
  - `めっき ### 5.2 判断を誤らないための運用ルール 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-022

- Claim kind: fact
- Claim text: ### 4.1 方式比較の見取り図
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 4.1 方式比較の見取り図 not found`
  - `めっき ### 4.1 方式比較の見取り図 未確認`
  - `めっき ### 4.1 方式比較の見取り図 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 4.1 方式比較の見取り図 supplier customer`
  - `めっき ### 4.1 方式比較の見取り図 取引先`
  - `めっき ### 4.1 方式比較の見取り図 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 4.1 方式比較の見取り図 positioning`
  - `めっき ### 4.1 方式比較の見取り図 role difference`
  - `めっき ### 4.1 方式比較の見取り図 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-035

- Claim kind: fact
- Claim text: ### 4.2 何が選定を分けるか
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 4.2 何が選定を分けるか not found`
  - `めっき ### 4.2 何が選定を分けるか 未確認`
  - `めっき ### 4.2 何が選定を分けるか 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 4.2 何が選定を分けるか supplier customer`
  - `めっき ### 4.2 何が選定を分けるか 取引先`
  - `めっき ### 4.2 何が選定を分けるか 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 4.2 何が選定を分けるか positioning`
  - `めっき ### 4.2 何が選定を分けるか role difference`
  - `めっき ### 4.2 何が選定を分けるか 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-040

- Claim kind: fact
- Claim text: ### 4.3 用途別に見た方式の役割
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 4.3 用途別に見た方式の役割 not found`
  - `めっき ### 4.3 用途別に見た方式の役割 未確認`
  - `めっき ### 4.3 用途別に見た方式の役割 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 4.3 用途別に見た方式の役割 supplier customer`
  - `めっき ### 4.3 用途別に見た方式の役割 取引先`
  - `めっき ### 4.3 用途別に見た方式の役割 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 4.3 用途別に見た方式の役割 positioning`
  - `めっき ### 4.3 用途別に見た方式の役割 role difference`
  - `めっき ### 4.3 用途別に見た方式の役割 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-044

- Claim kind: fact
- Claim text: ### 4.4 工程全体と関係者のつながり
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 4.4 工程全体と関係者のつながり not found`
  - `めっき ### 4.4 工程全体と関係者のつながり 未確認`
  - `めっき ### 4.4 工程全体と関係者のつながり 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 4.4 工程全体と関係者のつながり supplier customer`
  - `めっき ### 4.4 工程全体と関係者のつながり 取引先`
  - `めっき ### 4.4 工程全体と関係者のつながり 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 4.4 工程全体と関係者のつながり positioning`
  - `めっき ### 4.4 工程全体と関係者のつながり role difference`
  - `めっき ### 4.4 工程全体と関係者のつながり 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-048

- Claim kind: fact
- Claim text: ### 4.5 例外条件と誤解しやすい境界
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 4.5 例外条件と誤解しやすい境界 not found`
  - `めっき ### 4.5 例外条件と誤解しやすい境界 未確認`
  - `めっき ### 4.5 例外条件と誤解しやすい境界 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 4.5 例外条件と誤解しやすい境界 supplier customer`
  - `めっき ### 4.5 例外条件と誤解しやすい境界 取引先`
  - `めっき ### 4.5 例外条件と誤解しやすい境界 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 4.5 例外条件と誤解しやすい境界 positioning`
  - `めっき ### 4.5 例外条件と誤解しやすい境界 role difference`
  - `めっき ### 4.5 例外条件と誤解しやすい境界 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-052

- Claim kind: fact
- Claim text: ### 4.6 直近の制度変更と日付
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 4.6 直近の制度変更と日付 not found`
  - `めっき ### 4.6 直近の制度変更と日付 未確認`
  - `めっき ### 4.6 直近の制度変更と日付 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 4.6 直近の制度変更と日付 supplier customer`
  - `めっき ### 4.6 直近の制度変更と日付 取引先`
  - `めっき ### 4.6 直近の制度変更と日付 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 4.6 直近の制度変更と日付 positioning`
  - `めっき ### 4.6 直近の制度変更と日付 role difference`
  - `めっき ### 4.6 直近の制度変更と日付 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-058

- Claim kind: fact
- Claim text: ### 4.7 見落としやすい実務リスク
- Gap note: needs >= 2 sources (has 0); needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ### 4.7 見落としやすい実務リスク not found`
  - `めっき ### 4.7 見落としやすい実務リスク 未確認`
  - `めっき ### 4.7 見落としやすい実務リスク 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ### 4.7 見落としやすい実務リスク supplier customer`
  - `めっき ### 4.7 見落としやすい実務リスク 取引先`
  - `めっき ### 4.7 見落としやすい実務リスク 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ### 4.7 見落としやすい実務リスク positioning`
  - `めっき ### 4.7 見落としやすい実務リスク role difference`
  - `めっき ### 4.7 見落としやすい実務リスク 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-036

- Claim kind: advice
- Claim text: 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用が候補に上がります。富士電機 全国鍍金工業組合連合会
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... not found`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 未確認`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... supplier customer`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 取引先`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... positioning`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... role difference`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-076

- Claim kind: advice
- Claim text: 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用が候補に上がります。富士電機 全国鍍金工業組合連合会
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... not found`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 未確認`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... supplier customer`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 取引先`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... positioning`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... role difference`
  - `めっき 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-109

- Claim kind: advice
- Claim text: コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する not found`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 未確認`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する supplier customer`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 取引先`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する positioning`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する role difference`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-110

- Claim kind: advice
- Claim text: コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない not found`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 未確認`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない supplier customer`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 取引先`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない positioning`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない role difference`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-111

- Claim kind: advice
- Claim text: コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 not found`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 未確認`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 supplier customer`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 取引先`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 positioning`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 role difference`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-115

- Claim kind: advice
- Claim text: 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する not found`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 未確認`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する supplier customer`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 取引先`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する positioning`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する role difference`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-116

- Claim kind: advice
- Claim text: 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい not found`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 未確認`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい supplier customer`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 取引先`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい positioning`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい role difference`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-117

- Claim kind: advice
- Claim text: 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 not found`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 未確認`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 supplier customer`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 取引先`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 positioning`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 role difference`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-125

- Claim kind: advice
- Claim text: 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比較表を作ると、社内説明も見積り比較もぶれます。機材工 大阪府立産業技術総合研究所
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... not found`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 未確認`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... supplier customer`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 取引先`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... positioning`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... role difference`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-126

- Claim kind: advice
- Claim text: 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけが抜け落ちます。大阪府立産業技術総合研究所 全国鍍金工業組合連合会
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... not found`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 未確認`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... supplier customer`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 取引先`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... positioning`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... role difference`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-144

- Claim kind: advice
- Claim text: コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する not found`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 未確認`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する supplier customer`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 取引先`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する positioning`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する role difference`
  - `めっき コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-145

- Claim kind: advice
- Claim text: コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない not found`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 未確認`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない supplier customer`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 取引先`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない positioning`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない role difference`
  - `めっき コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-146

- Claim kind: advice
- Claim text: コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 not found`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 未確認`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 supplier customer`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 取引先`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 positioning`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 role difference`
  - `めっき コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-150

- Claim kind: advice
- Claim text: 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する not found`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 未確認`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する supplier customer`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 取引先`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する positioning`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する role difference`
  - `めっき 複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-151

- Claim kind: advice
- Claim text: 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい not found`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 未確認`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい supplier customer`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 取引先`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい positioning`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい role difference`
  - `めっき 複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-152

- Claim kind: advice
- Claim text: 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 not found`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 未確認`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 supplier customer`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 取引先`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 positioning`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 role difference`
  - `めっき 複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-159

- Claim kind: advice
- Claim text: 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比較表を作ると、社内説明も見積り比較もぶれます。機材工 大阪府立産業技術総合研究所
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... not found`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 未確認`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... supplier customer`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 取引先`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... positioning`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... role difference`
  - `めっき 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-160

- Claim kind: advice
- Claim text: 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけが抜け落ちます。大阪府立産業技術総合研究所 全国鍍金工業組合連合会
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... not found`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 未確認`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... supplier customer`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 取引先`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... positioning`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... role difference`
  - `めっき 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけ... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-055

- Claim kind: temporal
- Claim text: 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正
- Gap note: needs >= 2 sources (has 1)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 not found`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 未確認`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 supplier customer`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 取引先`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 positioning`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 role difference`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-091

- Claim kind: temporal
- Claim text: 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正
- Gap note: needs >= 2 sources (has 1)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 not found`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 未確認`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 supplier customer`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 取引先`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 positioning`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 role difference`
  - `めっき 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-002

- Claim kind: fact
- Claim text: 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電子部品、プリント基板、半導体周辺、建材、装飾部材まで広く、用途ごとに選ばれる方式と評価指標が大きく変わります。機材工 JCU 大阪府立産業技術総合研究所
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... not found`
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... 未確認`
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... supplier customer`
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... 取引先`
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... positioning`
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... role difference`
  - `めっき 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-014

- Claim kind: fact
- Claim text: 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 not found`
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 未確認`
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 supplier customer`
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 取引先`
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 positioning`
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 role difference`
  - `めっき 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-041

- Claim kind: fact
- Claim text: 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材工 JCU
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... not found`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 未確認`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... supplier customer`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 取引先`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... positioning`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... role difference`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-042

- Claim kind: fact
- Claim text: 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要です。JCU 機材工
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... not found`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 未確認`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... supplier customer`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 取引先`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... positioning`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... role difference`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-043

- Claim kind: fact
- Claim text: 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすくなります。全国鍍金工業組合連合会 大阪府立産業技術総合研究所
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... not found`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 未確認`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... supplier customer`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 取引先`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... positioning`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... role difference`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-046

- Claim kind: fact
- Claim text: 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 not found`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 未確認`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 supplier customer`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 取引先`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 positioning`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 role difference`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-080

- Claim kind: fact
- Claim text: 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材工 JCU
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... not found`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 未確認`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... supplier customer`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 取引先`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... positioning`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... role difference`
  - `めっき 需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-081

- Claim kind: fact
- Claim text: 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要です。JCU 機材工
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... not found`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 未確認`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... supplier customer`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 取引先`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... positioning`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... role difference`
  - `めっき 供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-082

- Claim kind: fact
- Claim text: 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすくなります。全国鍍金工業組合連合会 大阪府立産業技術総合研究所
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... not found`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 未確認`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... supplier customer`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 取引先`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... positioning`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... role difference`
  - `めっき 技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすく... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-084

- Claim kind: fact
- Claim text: 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工
- Gap note: needs >= 1 primary sources (has 0)

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 not found`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 未確認`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 supplier customer`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 取引先`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 positioning`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 role difference`
  - `めっき 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-004

- Claim kind: temporal
- Claim text: 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で優位ですが、薬液管理とコスト負荷が重くなりやすいです。富士電機 全国鍍金工業組合連合会 表面技術協会
- Gap note: needs official regulator or legal text support; needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... not found`
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... 未確認`
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... supplier customer`
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... 取引先`
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... positioning`
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... role difference`
  - `めっき 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-010

- Claim kind: temporal
- Claim text: 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3 という明確な基準があり、ばく露測定と是正が中心論点です。厚生労働省 OSHA NIEHS
- Gap note: needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... not found`
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... 未確認`
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... supplier customer`
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... 取引先`
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... positioning`
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... role difference`
  - `めっき 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-011

- Claim kind: regulatory
- Claim text: EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出条件で縛ります。RoHS 適合と REACH 適合は別問題であり、製品スコープと接触条件を付けて書く必要があります。EUR-Lex RoHS 欧州委員会 RoHS ECHA Annex XVII ECHA nickel details
- Gap note: needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... not found`
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... 未確認`
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... supplier customer`
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... 取引先`
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... positioning`
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... role difference`
  - `めっき EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-038

- Claim kind: regulatory
- Claim text: コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれているからです。JCU US EPA 排水
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... not found`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 未確認`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... supplier customer`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 取引先`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... positioning`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... role difference`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-039

- Claim kind: regulatory
- Claim text: 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程での是正コストが大きくなります。EUR-Lex RoHS ECHA Annex XVII OSHA 環境省 排水基準
- Gap note: needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... not found`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 未確認`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... supplier customer`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 取引先`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... positioning`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... role difference`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-045

- Claim kind: regulatory
- Claim text: 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定しません。US EPA 排水 厚生労働省
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... not found`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 未確認`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... supplier customer`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 取引先`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... positioning`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... role difference`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-047

- Claim kind: regulatory
- Claim text: 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、トレーサビリティ、規制適合の仕様へ跳ね返ります。JCU 経済産業省
- Gap note: needs official regulator or legal text support; needs exact date or effective date; needs regulated subject; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... not found`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 未確認`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... supplier customer`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 取引先`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... positioning`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... role difference`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-051

- Claim kind: regulatory
- Claim text: 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoHS ECHA Annex XVII OSHA
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... not found`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 未確認`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... supplier customer`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 取引先`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... positioning`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... role difference`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-061

- Claim kind: temporal
- Claim text: 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HDI 基板や先端パッケージでは、microvia 周りのめっきは一般的な厚付け発想をそのまま適用できず、界面品質と後工程条件を別管理する必要があります。大阪府立産業技術総合研究所 JCU IPC
- Gap note: needs official regulator or legal text support; needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... not found`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 未確認`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... supplier customer`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 取引先`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... positioning`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... role difference`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-063

- Claim kind: regulatory
- Claim text: 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積り時より総コストが悪化しやすいです。表面技術協会 US EPA 排水 JCU
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... not found`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 未確認`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... supplier customer`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 取引先`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... positioning`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... role difference`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-078

- Claim kind: regulatory
- Claim text: コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれているからです。JCU US EPA 排水
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... not found`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 未確認`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... supplier customer`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 取引先`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... positioning`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... role difference`
  - `めっき コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれている... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-079

- Claim kind: regulatory
- Claim text: 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程での是正コストが大きくなります。EUR-Lex RoHS ECHA Annex XVII OSHA 環境省 排水基準
- Gap note: needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... not found`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 未確認`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... supplier customer`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 取引先`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... positioning`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... role difference`
  - `めっき 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-083

- Claim kind: regulatory
- Claim text: 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定しません。US EPA 排水 厚生労働省
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... not found`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 未確認`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... supplier customer`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 取引先`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... positioning`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... role difference`
  - `めっき 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-085

- Claim kind: regulatory
- Claim text: 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、トレーサビリティ、規制適合の仕様へ跳ね返ります。JCU 経済産業省
- Gap note: needs official regulator or legal text support; needs exact date or effective date; needs regulated subject; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... not found`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 未確認`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... supplier customer`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 取引先`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... positioning`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... role difference`
  - `めっき 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-088

- Claim kind: regulatory
- Claim text: 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoHS ECHA Annex XVII OSHA
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... not found`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 未確認`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... supplier customer`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 取引先`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... positioning`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... role difference`
  - `めっき 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoH... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-096

- Claim kind: temporal
- Claim text: 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HDI 基板や先端パッケージでは、microvia 周りのめっきは一般的な厚付け発想をそのまま適用できず、界面品質と後工程条件を別管理する必要があります。大阪府立産業技術総合研究所 JCU IPC
- Gap note: needs official regulator or legal text support; needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... not found`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 未確認`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... supplier customer`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 取引先`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... positioning`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... role difference`
  - `めっき 材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HD... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-098

- Claim kind: regulatory
- Claim text: 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積り時より総コストが悪化しやすいです。表面技術協会 US EPA 排水 JCU
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... not found`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 未確認`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... supplier customer`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 取引先`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... positioning`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... role difference`
  - `めっき 運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-118

- Claim kind: regulatory
- Claim text: クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける
- Gap note: needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける not found`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 未確認`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける supplier customer`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 取引先`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける positioning`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける role difference`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-120

- Claim kind: regulatory
- Claim text: クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII not found`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 未確認`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII supplier customer`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 取引先`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII positioning`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII role difference`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-121

- Claim kind: regulatory
- Claim text: ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティを確認する
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... not found`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 未確認`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... supplier customer`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 取引先`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... positioning`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... role difference`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-123

- Claim kind: regulatory
- Claim text: ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 not found`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 未確認`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 supplier customer`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 取引先`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 positioning`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 role difference`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-129

- Claim kind: regulatory
- Claim text: 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総コストを読み違えます。US EPA 排水 厚生労働省 JCU
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... not found`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 未確認`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... supplier customer`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 取引先`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... positioning`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... role difference`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-133

- Claim kind: regulatory
- Claim text: 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排水基準 大阪府
- Gap note: needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... not found`
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... 未確認`
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... supplier customer`
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... 取引先`
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... positioning`
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... role difference`
  - `めっき 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-153

- Claim kind: regulatory
- Claim text: クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける
- Gap note: needs exact date or effective date

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける not found`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 未確認`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける supplier customer`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 取引先`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける positioning`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける role difference`
  - `めっき クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-155

- Claim kind: regulatory
- Claim text: クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII not found`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 未確認`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII supplier customer`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 取引先`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII positioning`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII role difference`
  - `めっき クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-156

- Claim kind: regulatory
- Claim text: ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティを確認する
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... not found`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 未確認`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... supplier customer`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 取引先`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... positioning`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... role difference`
  - `めっき ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティ... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-158

- Claim kind: regulatory
- Claim text: ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 not found`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 未確認`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 supplier customer`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 取引先`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 positioning`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 role difference`
  - `めっき ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.

## claim-163

- Claim kind: regulatory
- Claim text: 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総コストを読み違えます。US EPA 排水 厚生労働省 JCU
- Gap note: needs exact date or effective date; needs scope statement

### Recommended query families

- `contradiction_negative` (反証・不在確認): Look for contradictions, absences, and counterexamples.
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... not found`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 未確認`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 不在`
- `upstream_downstream` (上流/下流): Trace suppliers, customers, adjacent process steps, and commercial flow.
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... supplier customer`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 取引先`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 関係会社`
- `role_structure` (役割差・類型): Map the role differences, segmentation, and structure of the landscape.
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... positioning`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... role difference`
  - `めっき 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総... 類型`

### Suggested next step

- Search the queries above and append strong candidates.
- Prioritize primary or official sources when possible.
- Rebuild the claim ledger and re-run the evidence-gap check.
