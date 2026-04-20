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
