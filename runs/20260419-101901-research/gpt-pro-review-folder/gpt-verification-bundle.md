# GPT Pro Review Bundle

- Bundle purpose: single-file upload for GPT Pro review
- Run ID: 20260419-101901-research
- As-of date: 2026-04-19
- Release gate: complete
- Claim coverage ratio: 1.0
- High-risk claim coverage ratio: 1.0
- Weak claims: 0
- Missing claims: 0
- Metadata consistency: consistent
- Coverage status: complete
- Primary source ratio: 0.76
- Constraint: verify only from this bundle and optional web checks for time-sensitive facts

## Included Files
- report\report-ja.md
- sources\search-results.tsv
- sources\triaged-sources.tsv
- sources\deep-read-queue.tsv
- sources\citation-ledger.tsv
- sources\claim-ledger.tsv
- metrics.json
- brief.md
- query-plan.md
- run-config.toml
- notes\topic-profile.md
- notes\contradiction-log.md
- notes\upstream-downstream-map.md
- notes\role-structure-matrix.md
- notes\domain-risk-map.md
- notes\evidence-gap-followup.md

---

## FILE: report\report-ja.md

````md
# めっきの基礎整理と実務判断ポイント

- Run ID: 20260419-101901-research
- 出力言語: Japanese
- 生成日時: 2026-04-19 10:19:01

## 1. まず押さえる結論

- めっきは、狭義には電気的または化学的反応で基材表面に金属皮膜を形成する湿式表面処理であり、金属だけでなく一部の非金属基材にも適用されます。一方で、実務や営業表現では蒸着やスパッタ等の乾式法まで「広義のめっき」と呼ぶ例もあるため、レポートでは狭義の湿式めっきを主対象とし、乾式法は隣接概念として扱うのが安全です。[表面技術協会](https://mekki.sfj.or.jp/) [富士電機](https://www.fujielectric.co.jp/products/plating/about/) [アルバックテクノ](https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html)
- 実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電子部品、プリント基板、半導体周辺、建材、装飾部材まで広く、用途ごとに選ばれる方式と評価指標が大きく変わります。[機材工](https://kizaikou.or.jp/basic.html) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)
- 選定で本当に効くのは、「何をめっきするか」だけではなく、「何の機能を出したいか」「形状的に均一膜厚が要るか」「どの規制がかかるか」「不良がどの段階で顕在化するか」の4点です。とくに 2024年4月1日施行の日本の六価クロム排水基準見直し、米国のクロムめっき排水・大気規制、EU の RoHS/REACH は、方式選定とライン運用の前提条件として切り離せません。[環境省](https://www.env.go.jp/water/impure/haisui.html) [大阪府](https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html) [US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines) [US EPA 大気](https://www.epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air) [欧州委員会 RoHS](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en#law) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)

## 2. 読み手が先に知るべき要点

- 電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で優位ですが、薬液管理とコスト負荷が重くなりやすいです。[富士電機](https://www.fujielectric.co.jp/products/plating/about/) [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/hyoumenshori.html) [表面技術協会](https://www.sfj.or.jp/kaikoku/20220829Kansai.html)
- 溶融亜鉛めっきは、精密電子用途のめっきと同じ土俵で比較すると誤ります。鋼構造物や屋外使用部材で、防食寿命と全浸漬性を重視する別系統の意思決定です。[日本溶融亜鉛鍍金協会](https://www.aen-mekki.or.jp/) [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)
- 自動車と電子部品は、今もめっきの中心需要先です。自動車では防食と摩擦係数、電子・半導体周辺では導電、接続、界面品質、熱履歴後の信頼性が重くなります。[機材工](https://kizaikou.or.jp/basic.html) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [経済産業省](https://www.meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf)
- 電子用途では、プリント基板、ビア形成、コネクタ、リードフレーム、半導体パッケージ基板まで、銅・ニッケル・金・銀・すず系の組合せが使い分けられます。品質問題は出荷時に顕在化しないこともあり、IPC は microvia-to-target plating failure の潜在化を警告しています。[JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 工程管理上は、前処理、浴組成、添加剤、不純物、洗浄、乾燥、検査の総合管理が重要で、薬品単価だけでは総コストを語れません。歩留まり、再処理率、停止頻度、分析自動化、廃液・排気処理が効いてきます。[大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [表面技術協会](https://www.sfj.or.jp/kaikoku/20220829Kansai.html) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf)
- 日本では、六価クロムの一般排水基準は 0.2 mg Cr(VI)/L で、2024年4月1日から電気めっき業の特定事業場には 0.5 mg/L の暫定基準が3年間適用されています。さらに 2024年2月5日には測定法も JIS K0102-3 ベースへ改められました。[環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html) [大阪府](https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html) [環境省 測定法改正](https://www.env.go.jp/press/press_02720.html)
- 労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3 という明確な基準があり、ばく露測定と是正が中心論点です。[厚生労働省](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html) [OSHA](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [NIEHS](https://www.niehs.nih.gov/health/topics/agents/hex-chromium)
- EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出条件で縛ります。RoHS 適合と REACH 適合は別問題であり、製品スコープと接触条件を付けて書く必要があります。[EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [欧州委員会 RoHS](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en#law) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) [ECHA nickel details](https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e266a)

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
- Query volume: 26 / 24
- Unique URLs: 26
- Deep reads: 18 / 14
- Citation instances: 175 / 36
- Primary-source ratio: 76.0% (target 70.0%)
- Report claim coverage: 89 / 89 (100.0%)
- High-risk claim coverage: 64 / 64 (100.0%)
- Source role mix: official/legal 41.1%, standards/academic 14.9%, vendor 21.1%, industry association 12.0%
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

## 3. 判断に使う主要根拠

| 主張 | 根拠の要旨 | 出典 |
| --- | --- | --- |
| [fact] めっきは基材表面に金属皮膜を形成して機能を付与する技術で、狭義では湿式反応、広義では乾式法まで含む用法がある。 | 表面技術協会と富士電機は湿式めっきの定義を示し、アルバックテクノは蒸着・スパッタ等を含む広義用法を明示している。 | [表面技術協会](https://mekki.sfj.or.jp/) [富士電機](https://www.fujielectric.co.jp/products/plating/about/) [アルバックテクノ](https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html) |
| [fact] 電気めっき、無電解めっき、溶融めっきは、原理も向く用途も異なるため分けて比較すべきである。 | 富士電機は電気・無電解・置換を区別し、全鍍連は無電解の均一析出性を説明し、日本溶融亜鉛鍍金協会は溶融亜鉛めっきを独立した技術分野として扱う。 | [富士電機](https://www.fujielectric.co.jp/products/plating/about/) [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/hyoumenshori.html) [日本溶融亜鉛鍍金協会](https://www.aen-mekki.or.jp/) |
| [fact] 自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。 | 機材工は代表用途を自動車部品、機械部品、電気電子部品、装飾部品と整理し、JCU は自動車部品、基板、電子部品、半導体周辺を具体例として挙げる。 | [機材工](https://kizaikou.or.jp/basic.html) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) |
| [fact] 電子用途では、基板・微細配線・コネクタ等でめっき品質が接続信頼性を左右し、潜在不良は熱負荷後に顕在化しうる。 | JCU は基板・ビアフィル・電子部品・半導体PKG基板向け銅めっき薬品を整理し、IPC は microvia-to-target plating failure が従来検査をすり抜けると警告している。 | [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high) |
| [fact] 工程不良の多くは前処理、浴管理、膜厚均一性、密着性、異物管理の失敗として現れる。 | ORIST はめっきの利用分野と前処理・機能を整理し、表面技術協会の湿式めっき基礎セミナーは無電解ニッケルの選定・管理方法の重要性を示している。 | [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [表面技術協会](https://www.sfj.or.jp/kaikoku/20220829Kansai.html) |
| [fact] 日本では六価クロムの一般排水基準が 0.2 mg Cr(VI)/L に整理され、2024年4月1日から電気めっき業には 0.5 mg/L の暫定基準が3年間適用されている。 | 環境省の一般排水基準ページが 0.2 mg Cr(VI)/L を示し、大阪府ページが 2024年4月1日施行の暫定基準 0.5 mg/L を説明している。 | [環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html) [大阪府](https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html) |
| [fact] 2024年2月5日、日本では六価クロムの測定法も見直され、JIS K0102-3 ベースへ改められた。 | 環境省の 2024-02-05 報道発表は、六価クロム化合物の検定法・測定法を JIS K0102-3 に改めたことを明示している。 | [環境省 測定法改正](https://www.env.go.jp/press/press_02720.html) [環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html) |
| [fact] 米国では、めっきは排水規制と大気規制の両面から管理され、クロム工程では PFAS と六価クロムが同時論点化している。 | EPA の電気めっき排水ガイドラインは chrome finishing facilities と PFAS 論点を示し、クロムめっき NESHAP は hard/decorative chromium electroplating を対象にしている。 | [US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines) [US EPA 大気](https://www.epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air) |
| [fact] 六価クロムは電気めっきで広く使われる一方、職業ばく露の健康影響が強く意識されている。 | NIEHS は electroplating を主要用途に挙げ、OSHA は PEL 5 µg/m3 と action level 2.5 µg/m3 を定めている。 | [NIEHS](https://www.niehs.nih.gov/health/topics/agents/hex-chromium) [OSHA](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) |
| [fact] EU では、EEE 向けには RoHS が六価クロムを制限し、皮膚接触品には REACH Annex XVII Entry 27 のニッケル放出条件が効く。 | 欧州委員会と EUR-Lex の RoHS 文書が hexavalent chromium を制限対象に挙げ、ECHA 文書が Entry 27 のニッケル条件を整理している。 | [欧州委員会 RoHS](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en#law) [EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) |

## 4. 方式選定で迷いやすい論点

### 4.1 方式比較の見取り図

| 方式 | 主な使いどころ | 強み | 主な弱み・注意 | 参考 |
| --- | --- | --- | --- | --- |
| 電気めっき | 自動車部品、コネクタ、外観部材、一般機能皮膜 | 金属種の選択肢が広く、量産しやすく、コスト/性能バランスが良い | 形状依存で膜厚が偏りやすい。前処理と電流分布設計が重要 | [富士電機](https://www.fujielectric.co.jp/products/plating/about/) [ASM](https://www.asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE/) |
| 無電解めっき | 複雑形状、非導体、均一膜厚重視、精密部品 | 電流分布に縛られず均一析出しやすい | 浴安定性、還元剤管理、コスト、浴寿命が論点 | [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/hyoumenshori.html) [表面技術協会](https://www.sfj.or.jp/kaikoku/20220829Kansai.html) |
| 溶融亜鉛めっき | 鋼構造物、建材、屋外部材 | 厚い防食皮膜、犠牲防食、全浸漬性 | 精密電子用途のような微細制御には向かない | [日本溶融亜鉛鍍金協会](https://www.aen-mekki.or.jp/) [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) |
| 乾式/真空系表面処理 | 意匠膜、薄膜機能、真空成膜 | 薄膜制御、湿式とは別の材料設計が可能 | 狭義のめっきと混同しやすく、工程比較の前提がずれる | [アルバックテクノ](https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html) [表面技術協会](https://mekki.sfj.or.jp/) |

### 4.2 何が選定を分けるか

- 方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用が候補に上がります。[富士電機](https://www.fujielectric.co.jp/products/plating/about/) [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/hyoumenshori.html)
- 用途差では、防食系と電子系を一括で語らない方がよいです。前者は耐食寿命や後処理、後者は接触信頼性、ボイド、界面、熱サイクル後の不良顕在化が中心になります。[機材工](https://kizaikou.or.jp/basic.html) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれているからです。[JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- 規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程での是正コストが大きくなります。[EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) [OSHA](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html)

### 4.3 用途別に見た方式の役割

- 需要側の類型:
  防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。[機材工](https://kizaikou.or.jp/basic.html) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf)
- 供給側の類型:
  日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要です。[JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [機材工](https://kizaikou.or.jp/basic.html)
- 技術類型:
  亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすくなります。[全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/shurui.html) [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)

### 4.4 工程全体と関係者のつながり

- 上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定しません。[US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines) [厚生労働省](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html)
- 中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。[JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [機材工](https://kizaikou.or.jp/basic.html)
- 下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、トレーサビリティ、規制適合の仕様へ跳ね返ります。[JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [経済産業省](https://www.meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf)

### 4.5 例外条件と誤解しやすい境界

- 「めっき = 電気めっき」と断定すると、無電解めっきや溶融めっき、さらには広義の乾式法との境界を取り違えます。逆に「真空蒸着も全部めっき」と書くと、工程比較が雑になります。[表面技術協会](https://mekki.sfj.or.jp/) [アルバックテクノ](https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html)
- 「外観が良い = 品質が高い」も危険です。電子用途では潜在不良がリフロー後や現地使用後に出ることがあり、逆に防食用途では外観差が直ちに寿命差を意味しない場合があります。[IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high) [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)
- 「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。[EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) [OSHA](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)

### 4.6 直近の制度変更と日付

- 2011年7月21日: 現行の RoHS 指令 2011/65/EU が発効し、EEE における有害物質制限の基盤となりました。2025年1月1日時点の統合版でも六価クロムは制限対象です。[欧州委員会 RoHS](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en#law) [EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101)
- 2022年5月31日以降: 日本では化学物質の自律的管理への制度改正が段階的に進み、めっき薬品を含む現場管理の負荷が高まっています。[厚生労働省](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html)
- 2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。[環境省 測定法改正](https://www.env.go.jp/press/press_02720.html)
- 2024年4月1日: 日本の六価クロム排水基準改正が施行され、一般排水基準 0.2 mg/L、電気めっき業の暫定基準 0.5 mg/L が実務上の焦点になりました。[環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html) [大阪府](https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html)
- 2021年以降継続中: EPA は chrome finishing facilities の PFAS 排出を理由に、電気めっき/金属仕上げカテゴリの見直しを進めています。2026年4月19日時点でも、クロム系工程は六価クロムだけでなく PFAS 論点と一体で読む必要があります。[US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines) [US EPA 大気](https://www.epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air)

### 4.7 見落としやすい実務リスク

- 定義と境界の取り違え:
  湿式めっき、乾式表面処理、溶融めっきを同じ比較表で一律に扱うと、設備要件、工程設計、品質保証の前提がずれます。まず「電析 / 無電解 / 溶融 / 乾式」のどこを比較しているのかを固定しないと、後段の原価比較や規制整理も誤ります。[アルバックテクノ](https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html) [表面技術協会](https://mekki.sfj.or.jp/)
- 品質と信頼性の見落とし:
  前処理不足は密着不良、剥離、ピット、ブリスターの起点になり、浴管理不良は膜厚不均一、析出ムラ、再処理増を招きます。電子部品では接触抵抗、はんだ付け性、熱履歴後の界面健全性まで見ないと、外観合格でも後工程で不良化します。[大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 材料・用途依存の落とし穴:
  高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HDI 基板や先端パッケージでは、microvia 周りのめっきは一般的な厚付け発想をそのまま適用できず、界面品質と後工程条件を別管理する必要があります。[大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 規制と EHS の取り違え:
  同じめっきでも、排水、排気、作業者ばく露、製品中含有、皮膚接触によるニッケル放出では根拠法令が異なります。RoHS / REACH、国内排水基準、クロム・ニッケルの労安管理を同じ論点として扱うと対応漏れが出ます。[環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html) [厚生労働省](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html) [OSHA](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
- 運用と原価の過小評価:
  薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積り時より総コストが悪化しやすいです。[表面技術協会](https://www.sfj.or.jp/kaikoku/20220829Kansai.html) [US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf)

## 5. 導入前に確認すべきこと

### 5.1 選定前の実務チェックリスト

| 判断場面 | 先に固定すること | 判断を誤りやすい理由 | 根拠・注意 |
| --- | --- | --- | --- |
| 防食目的で鋼部品を処理する | 使用環境、要求寿命、後処理、必要膜厚レンジ、構造物サイズを先に固定する | 亜鉛電気めっきと溶融亜鉛めっきでは比較軸とコスト構造が大きく違う | [日本溶融亜鉛鍍金協会](https://www.aen-mekki.or.jp/) [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/shurui.html) |
| 高強度鋼・ばね材を扱う | 水素脆化リスク、めっき後ベーキング要否、図面 / 材質仕様の管理責任を確認する | 強度保証を落とすと遅れ破壊が後工程や実使用で現れる | [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/hyoumenshori.html) |
| 電子部品・基板用途を選定する | 膜厚均一性、ボイド、界面、熱サイクル後信頼性に加え、HDI / microvia 条件を別項目で確認する | 初期検査合格でも microvia や界面起点の潜在不良が後で出る | [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high) |
| コネクタ・接点用途を選定する | 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する | 外観や名目膜厚だけでは通電安定性を判断できない | [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [富士電機](https://www.fujielectric.co.jp/products/plating/about/) |
| はんだ接合を前提にする | 表面仕上げとはんだ付け性、保管後 / リフロー後のぬれ性、後工程フラックス条件を確認する | 「導電性がある」と「はんだ付けしやすい」は同義ではない | [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [機材工](https://kizaikou.or.jp/basic.html) |
| 複雑形状や非導体に処理する | 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する | 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい | [富士電機](https://www.fujielectric.co.jp/products/plating/about/) [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/hyoumenshori.html) |
| クロム・ニッケル系を採用する | 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける | 法体系が違い、代替判断も一律ではない | [環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html) [OSHA](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) |
| ライン改善や外注切替を検討する | 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティを確認する | 総コストと監査負荷は浴管理と周辺インフラで大きく変わる | [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [厚生労働省](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html) [US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines) |

### 5.2 判断を誤らないための運用ルール

- 方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比較表を作ると、社内説明も見積り比較もぶれます。[機材工](https://kizaikou.or.jp/basic.html) [大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)
- 高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけが抜け落ちます。[大阪府立産業技術総合研究所](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf) [全国鍍金工業組合連合会](https://zentoren.or.jp/mekki/hyoumenshori.html)
- 電子部品、コネクタ、はんだ用途では、接触抵抗、はんだ付け性、熱履歴後信頼性を外観と切り離して管理する。HDI / microvia は一般的な厚付け発想をそのまま持ち込まず、界面品質と後工程条件を別管理にするのが安全です。[JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- 規制判断は「製品」「工場」「作業者」「顧客要求」の4レイヤーに分けて記載する。RoHS / REACH / 排水 / 労安 / ニッケル放出を一つの表現でまとめると、適用範囲を誤りやすくなります。[EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459) [OSHA](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026) [環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html)
- 調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総コストを読み違えます。[US EPA 排水](https://www.epa.gov/eg/electroplating-effluent-guidelines) [厚生労働省](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html) [JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf)

### 5.3 このレポートで残る不確実性

- 本レポートは実務向け概説の focused-budget pass であり、full dr_ultra-equivalent run ではありません。個別の JIS / ASTM / IPC 要求膜厚や合否判定、個社固有の工程窓までは踏み込んでいないため、製品設計や受入規格の議論では対象規格を別途特定する必要があります。
- EU の六価クロム規制運用は、認可継続と制限強化の移行途上で動きやすい領域です。2026年4月19日時点の整理としては、RoHS は有効、REACH ニッケル制限も有効ですが、Cr(VI) の将来運用は継続監視が必要です。[EUR-Lex RoHS](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101) [ECHA Annex XVII](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
- 日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。[環境省 排水基準](https://www.env.go.jp/water/impure/haisui.html) [大阪府](https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html)
- 半導体・先端パッケージ用途では、めっき条件そのものより界面品質や後工程適合性が支配的になるため、サプライヤー資料と顧客評価条件を合わせて読む必要があります。[JCU](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf) [IPC](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)

## 6. 参照した主要ソース

- [表面技術協会 めっき部会](https://mekki.sfj.or.jp/)
- [富士電機 めっきとは](https://www.fujielectric.co.jp/products/plating/about/)
- [アルバックテクノ めっきとは？](https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html)
- [全国鍍金工業組合連合会 めっきの表面処理](https://zentoren.or.jp/mekki/hyoumenshori.html)
- [全国鍍金工業組合連合会 めっきの種類](https://zentoren.or.jp/mekki/shurui.html)
- [機材工 一般社団法人日本表面処理機材工業会](https://kizaikou.or.jp/basic.html)
- [JCU 表面処理技術から未来を創造する](https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf)
- [大阪府立産業技術総合研究所 防錆・防食のためのめっきの基礎知識](https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf)
- [IPC microvia reliability warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
- [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
- [環境省 検定方法等の改正 2024-02-05](https://www.env.go.jp/press/press_02720.html)
- [大阪府 六価クロム排水基準改正 2024-04-01施行](https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html)
- [US EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- [US EPA Chromium Electroplating NESHAP](https://www.epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air)
- [OSHA Chromium (VI) standard](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
- [NIEHS Hexavalent Chromium](https://www.niehs.nih.gov/health/topics/agents/hex-chromium)
- [EUR-Lex RoHS consolidated text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101)
- [ECHA Annex XVII conditions of restriction](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
````

---

## FILE: sources\search-results.tsv

````tsv
query	title	url	snippet	published_at
めっき 定義 協会	めっき部会｜表面技術協会	https://mekki.sfj.or.jp/	表面技術協会めっき部会。めっきとは、成形された品物の表面に金・銀・銅などの金属の薄膜を施すことと説明し、多様な単一金属めっき・合金めっきや非金属基材も扱う。	
めっき 定義 メーカー	めっきとは ｜ 富士電機の表面処理（めっき） ｜ 富士電機	https://www.fujielectric.co.jp/products/plating/about/	めっきとは、金属または非金属の表面に金属の薄い皮膜を形成させる技術で、電気めっき・無電解めっき・置換めっきなどを区別している。	
めっき 広義 乾式めっき	めっきとは？｜FAQ｜表面処理｜サービス｜アルバックテクノ	https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html	広義には湿式めっきのほか、蒸着、スパッタ、溶射、はんだ被覆など乾式めっきも含むと説明する表面処理FAQ。	
溶融亜鉛めっき 協会	HOME | 一般社団法人 日本溶融亜鉛鍍金協会	https://www.aen-mekki.or.jp/	日本溶融亜鉛鍍金協会。溶融亜鉛めっき技術の開発・向上と普及・啓発、需要開拓のために活動する非営利団体。	2026-04-01
めっき 用途 業界団体	機材工 | 機材工 一般社団法人日本表面処理機材工業会	https://kizaikou.or.jp/basic.html	めっきは自動車部品、機械部品、電気・電子部品、装飾部品などに適用され、防錆性、耐摩耗性、電気伝導性、装飾性などの表面機能を付与すると説明。	
めっき 種類 団体	全国鍍金工業組合連合会（ぜんとれん）	https://zentoren.or.jp/mekki/hyoumenshori.html	無電解めっきは溶液中での還元反応を利用し、金属から非金属まで広くめっき可能で、膜厚精度が高く、主に機能を重視した工業用途に供されると説明。	
めっき 皮膜 種類	全国鍍金工業組合連合会（ぜんとれん）	https://zentoren.or.jp/mekki/shurui.html	白金めっき、亜鉛めっき、クロムめっきなど各皮膜の特性と用途を整理。工業用クロムめっきは比較的厚いめっきとして説明。	
electroplating definition asm	Electroplated Coatings - ASM International	https://www.asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE/	ASMの解説記事。electroplating を、基材と異なる表面特性や寸法を与えるための金属皮膜の電析と説明。	
湿式めっき 基礎 セミナー	2022年関西支部セミナー「湿式めっきの基礎」｜表面技術協会	https://www.sfj.or.jp/kaikoku/20220829Kansai.html	無電解ニッケルめっきの基礎と応用、自動車・機械・電気電子・半導体産業での重要性、めっき液の選定・管理方法を扱うセミナー案内。	2022-08-29
electroplating wastewater EPA	Electroplating Effluent Guidelines | US EPA	https://www.epa.gov/eg/electroplating-effluent-guidelines	EPAの電気めっき排水規制ページ。共通金属、貴金属、無電解めっき、PCBなどのサブカテゴリと対象金属、PFAS/六価クロム関連の論点を整理。	
chromium electroplating air EPA	Chromium Electroplating: National Emission Standards for Hazardous Air Pollutants | US EPA	https://www.epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	EPAの大気規制ページ。硬質・装飾クロムめっきおよびクロム酸陽極酸化槽からのクロム化合物排出を対象にしたNESHAP/MACTを説明。	
六価クロム 排水基準 環境省	一般排水基準 | 水・土壌・地盤・海洋環境の保全 | 環境省	https://www.env.go.jp/water/impure/haisui.html	環境省の一般排水基準。六価クロム化合物は 0.2 mg Cr(VI)/L と整理。	
六価クロム 暫定排水基準 大阪府	六価クロム化合物の排水基準と暫定排水基準が改正されました（令和6年4月1日施行）／大阪府（おおさかふ）ホームページ	https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	2024年4月1日施行。六価クロム化合物の排水基準を 0.2 mg/L に改め、電気めっき業の特定事業場には暫定基準 0.5 mg/L を3年間適用と説明。	2024-04-01
RoHS hexavalent chromium official	RoHS Directive - Environment - European Commission	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en#law	欧州委員会のRoHS解説。hexavalent chromium を含む10物質を制限し、電気電子機器への適合を求める。	
REACH nickel official	ANNEX XVII TO REACH – Conditions of restriction	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	ECHAのREACH Annex XVII資料。Entry 27 としてニッケルの制限条件を整理。	
hexavalent chromium exposure NIEHS	Hexavalent Chromium | National Institute of Environmental Health Sciences	https://www.niehs.nih.gov/health/topics/agents/hex-chromium	NIEHSの健康影響解説。六価クロムは electroplating などで広く使われ、吸入・摂取・皮膚接触でばく露しうると説明。	
めっき 電子部品 応用 公設研	防錆・防食のためのめっきの基礎知識	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	大阪府立産業技術総合研究所の資料。めっきの種類、利用分野、プリント基板や電子部品への応用、防食・耐摩耗などの機能を解説。	
めっき 用途 自動車 電子 JCU	表面処理技術から未来を創造する	https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	JCUのIR資料。装飾・防錆分野、Plating on Plastics、自動車部品、水栓金具、プリント基板/マザーボード向け銅めっき薬品などの用途を整理。	
PCB reliability IPC	IPC Issues Electronics Industry Warning on Printed Board Microvia Reliability for High Performance Products | IPC International, Inc.	https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	IPCのリリース。高性能製品での microvia-to-target plating failures と検査限界に関する注意喚起。	
ニッケル化合物 労働安全 厚労省	平成２０年１１月の特定障害予防規則等の改正（ニッケル化合物・砒素及びその化合物に係る規制の導入等）｜厚生労働省	https://www.mhlw.go.jp/bunya/roudoukijun/anzeneisei20/index.html	厚生労働省の安全衛生ページ。ニッケル化合物等に係る規制導入と健康障害防止対策強化の案内。	
めっき 用途 経産省	金属素材産業関係資料	https://www.meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	経済産業省の金属素材産業資料。めっきや表面処理を含む素材産業の位置づけと需要産業との関係を把握する補助資料。	
六価クロム 測定法 改正 環境省	環境大臣が定める排水基準に係る検定方法等の一部改正について | 報道発表資料 | 環境省	https://www.env.go.jp/press/press_02720.html	2024年2月5日公表。六価クロムに係る基準見直しを踏まえ、排水基準に係る検定方法等を改正。	2024-02-05
化学物質 自律的管理 厚労省	新たな化学物質規制に関する特設サイト｜厚生労働省	https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	厚労省の特設サイト。化学物質の自律的管理に向けた制度改正と対象物質拡大の整理。	
CrVI OSHA standard	1910.1026 - Chromium (VI). | Occupational Safety and Health Administration	https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	OSHAの六価クロム規則。一般産業向けの許容濃度、アクションレベル、ばく露管理などを整理。	
RoHS 統合版 EUR-Lex	Directive 2011/65/EU on the restriction of the use of certain hazardous substances in electrical and electronic equipment (consolidated text)	https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101	EUR-LexのRoHS統合版。六価クロムを含む制限物質と適用法構造を確認できる。	2025-01-01
REACH nickel details ECHA	ECHA restricted substances under REACH - Nickel details	https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e266a	ECHAのニッケル制限詳細ページ。長時間皮膚接触品に関する実務上の解釈を確認する補助資料。
````

---

## FILE: sources\triaged-sources.tsv

````tsv
rank_hint	score_hint	source_flags	dup_count	query_count	domain	title	canonical_url	queries	original_urls	sample_snippet	published_at
1	11	preferred-domain,institutional-domain,official-looking-path	1	1	env.go.jp	環境大臣が定める排水基準に係る検定方法等の一部改正について | 報道発表資料 | 環境省	https://env.go.jp/press/press_02720.html	六価クロム 測定法 改正 環境省	https://www.env.go.jp/press/press_02720.html	2024年2月5日公表。六価クロムに係る基準見直しを踏まえ、排水基準に係る検定方法等を改正。	2024-02-05
2	11	preferred-domain,institutional-domain,pdf	1	1	meti.go.jp	金属素材産業関係資料	https://meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	めっき 用途 経産省	https://www.meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	経済産業省の金属素材産業資料。めっきや表面処理を含む素材産業の位置づけと需要産業との関係を把握する補助資料。	
3	11	preferred-domain,institutional-domain,official-looking-path	1	1	osha.gov	1910.1026 - Chromium (VI). | Occupational Safety and Health Administration	https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	CrVI OSHA standard	https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	OSHAの六価クロム規則。一般産業向けの許容濃度、アクションレベル、ばく露管理などを整理。	
4	9	preferred-domain,institutional-domain	1	1	env.go.jp	一般排水基準 | 水・土壌・地盤・海洋環境の保全 | 環境省	https://env.go.jp/water/impure/haisui.html	六価クロム 排水基準 環境省	https://www.env.go.jp/water/impure/haisui.html	環境省の一般排水基準。六価クロム化合物は 0.2 mg Cr(VI)/L と整理。	
5	9	preferred-domain,institutional-domain	1	1	epa.gov	Electroplating Effluent Guidelines | US EPA	https://epa.gov/eg/electroplating-effluent-guidelines	electroplating wastewater EPA	https://www.epa.gov/eg/electroplating-effluent-guidelines	EPAの電気めっき排水規制ページ。共通金属、貴金属、無電解めっき、PCBなどのサブカテゴリと対象金属、PFAS/六価クロム関連の論点を整理。	
6	9	preferred-domain,institutional-domain	1	1	epa.gov	Chromium Electroplating: National Emission Standards for Hazardous Air Pollutants | US EPA	https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	chromium electroplating air EPA	https://www.epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	EPAの大気規制ページ。硬質・装飾クロムめっきおよびクロム酸陽極酸化槽からのクロム化合物排出を対象にしたNESHAP/MACTを説明。	
7	9	preferred-domain,institutional-domain	1	1	mhlw.go.jp	平成２０年１１月の特定障害予防規則等の改正（ニッケル化合物・砒素及びその化合物に係る規制の導入等）｜厚生労働省	https://mhlw.go.jp/bunya/roudoukijun/anzeneisei20/index.html	ニッケル化合物 労働安全 厚労省	https://www.mhlw.go.jp/bunya/roudoukijun/anzeneisei20/index.html	厚生労働省の安全衛生ページ。ニッケル化合物等に係る規制導入と健康障害防止対策強化の案内。	
8	9	preferred-domain,institutional-domain	1	1	mhlw.go.jp	新たな化学物質規制に関する特設サイト｜厚生労働省	https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	化学物質 自律的管理 厚労省	https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	厚労省の特設サイト。化学物質の自律的管理に向けた制度改正と対象物質拡大の整理。	
9	8	preferred-domain,pdf	1	1	jcu-i.com	表面処理技術から未来を創造する	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	めっき 用途 自動車 電子 JCU	https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	JCUのIR資料。装飾・防錆分野、Plating on Plastics、自動車部品、水栓金具、プリント基板/マザーボード向け銅めっき薬品などの用途を整理。	
10	8	preferred-domain,pdf	1	1	www2.orist.jp	防錆・防食のためのめっきの基礎知識	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	めっき 電子部品 応用 公設研	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	大阪府立産業技術総合研究所の資料。めっきの種類、利用分野、プリント基板や電子部品への応用、防食・耐摩耗などの機能を解説。	
11	6	preferred-domain	1	1	aen-mekki.or.jp	HOME | 一般社団法人 日本溶融亜鉛鍍金協会	https://aen-mekki.or.jp/	溶融亜鉛めっき 協会	https://www.aen-mekki.or.jp/	日本溶融亜鉛鍍金協会。溶融亜鉛めっき技術の開発・向上と普及・啓発、需要開拓のために活動する非営利団体。	2026-04-01
12	6	preferred-domain	1	1	asminternational.org	Electroplated Coatings - ASM International	https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	electroplating definition asm	https://www.asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE/	ASMの解説記事。electroplating を、基材と異なる表面特性や寸法を与えるための金属皮膜の電析と説明。	
13	6	preferred-domain	1	1	echa.europa.eu	ANNEX XVII TO REACH – Conditions of restriction	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	REACH nickel official	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	ECHAのREACH Annex XVII資料。Entry 27 としてニッケルの制限条件を整理。	
14	6	preferred-domain	1	1	echa.europa.eu	ECHA restricted substances under REACH - Nickel details	https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e266a	REACH nickel details ECHA	https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e266a	ECHAのニッケル制限詳細ページ。長時間皮膚接触品に関する実務上の解釈を確認する補助資料。	
15	6	preferred-domain	1	1	environment.ec.europa.eu	RoHS Directive - Environment - European Commission	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en	RoHS hexavalent chromium official	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en#law	欧州委員会のRoHS解説。hexavalent chromium を含む10物質を制限し、電気電子機器への適合を求める。	
16	6	preferred-domain	1	1	eur-lex.europa.eu	Directive 2011/65/EU on the restriction of the use of certain hazardous substances in electrical and electronic equipment (consolidated text)	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101	RoHS 統合版 EUR-Lex	https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101	EUR-LexのRoHS統合版。六価クロムを含む制限物質と適用法構造を確認できる。	2025-01-01
17	6	preferred-domain	1	1	fujielectric.co.jp	めっきとは ｜ 富士電機の表面処理（めっき） ｜ 富士電機	https://fujielectric.co.jp/products/plating/about	めっき 定義 メーカー	https://www.fujielectric.co.jp/products/plating/about/	めっきとは、金属または非金属の表面に金属の薄い皮膜を形成させる技術で、電気めっき・無電解めっき・置換めっきなどを区別している。	
18	6	preferred-domain	1	1	ipc.org	IPC Issues Electronics Industry Warning on Printed Board Microvia Reliability for High Performance Products | IPC International, Inc.	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	PCB reliability IPC	https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	IPCのリリース。高性能製品での microvia-to-target plating failures と検査限界に関する注意喚起。	
19	6	preferred-domain	1	1	kizaikou.or.jp	機材工 | 機材工 一般社団法人日本表面処理機材工業会	https://kizaikou.or.jp/basic.html	めっき 用途 業界団体	https://kizaikou.or.jp/basic.html	めっきは自動車部品、機械部品、電気・電子部品、装飾部品などに適用され、防錆性、耐摩耗性、電気伝導性、装飾性などの表面機能を付与すると説明。	
20	6	preferred-domain	1	1	mekki.sfj.or.jp	めっき部会｜表面技術協会	https://mekki.sfj.or.jp/	めっき 定義 協会	https://mekki.sfj.or.jp/	表面技術協会めっき部会。めっきとは、成形された品物の表面に金・銀・銅などの金属の薄膜を施すことと説明し、多様な単一金属めっき・合金めっきや非金属基材も扱う。	
21	6	preferred-domain	1	1	sfj.or.jp	2022年関西支部セミナー「湿式めっきの基礎」｜表面技術協会	https://sfj.or.jp/kaikoku/20220829Kansai.html	湿式めっき 基礎 セミナー	https://www.sfj.or.jp/kaikoku/20220829Kansai.html	無電解ニッケルめっきの基礎と応用、自動車・機械・電気電子・半導体産業での重要性、めっき液の選定・管理方法を扱うセミナー案内。	2022-08-29
22	6	preferred-domain	1	1	ulvac-techno.co.jp	めっきとは？｜FAQ｜表面処理｜サービス｜アルバックテクノ	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	めっき 広義 乾式めっき	https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html	広義には湿式めっきのほか、蒸着、スパッタ、溶射、はんだ被覆など乾式めっきも含むと説明する表面処理FAQ。	
23	6	preferred-domain	1	1	zentoren.or.jp	全国鍍金工業組合連合会（ぜんとれん）	https://zentoren.or.jp/mekki/hyoumenshori.html	めっき 種類 団体	https://zentoren.or.jp/mekki/hyoumenshori.html	無電解めっきは溶液中での還元反応を利用し、金属から非金属まで広くめっき可能で、膜厚精度が高く、主に機能を重視した工業用途に供されると説明。	
24	6	preferred-domain	1	1	zentoren.or.jp	全国鍍金工業組合連合会（ぜんとれん）	https://zentoren.or.jp/mekki/shurui.html	めっき 皮膜 種類	https://zentoren.or.jp/mekki/shurui.html	白金めっき、亜鉛めっき、クロムめっきなど各皮膜の特性と用途を整理。工業用クロムめっきは比較的厚いめっきとして説明。	
25	3	institutional-domain	1	1	niehs.nih.gov	Hexavalent Chromium | National Institute of Environmental Health Sciences	https://niehs.nih.gov/health/topics/agents/hex-chromium	hexavalent chromium exposure NIEHS	https://www.niehs.nih.gov/health/topics/agents/hex-chromium	NIEHSの健康影響解説。六価クロムは electroplating などで広く使われ、吸入・摂取・皮膚接触でばく露しうると説明。	
26	0	neutral	1	1	pref.osaka.lg.jp	六価クロム化合物の排水基準と暫定排水基準が改正されました（令和6年4月1日施行）／大阪府（おおさかふ）ホームページ	https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	六価クロム 暫定排水基準 大阪府	https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	2024年4月1日施行。六価クロム化合物の排水基準を 0.2 mg/L に改め、電気めっき業の特定事業場には暫定基準 0.5 mg/L を3年間適用と説明。	2024-04-01
````

---

## FILE: sources\deep-read-queue.tsv

````tsv
priority	status	reason	title	url	notes_file
high	read	定義と広義/狭義の境界を押さえるため	めっき部会｜表面技術協会	https://mekki.sfj.or.jp/	
high	read	方式分類の説明に使うため	めっきとは ｜ 富士電機の表面処理（めっき） ｜ 富士電機	https://www.fujielectric.co.jp/products/plating/about/	
high	read	乾式表面処理との境界を整理するため	めっきとは？｜FAQ｜表面処理｜サービス｜アルバックテクノ	https://www.ulvac-techno.co.jp/service/surface_treatment/faq/001.html	
high	selected	電気めっきの工学的定義と目的を補強するため	Electroplated Coatings - ASM International	https://www.asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE/	
medium	selected	溶融めっきの独立した位置づけを示すため	HOME | 一般社団法人 日本溶融亜鉛鍍金協会	https://www.aen-mekki.or.jp/	
high	read	日本の用途整理と産業的背景を押さえるため	機材工 | 機材工 一般社団法人日本表面処理機材工業会	https://kizaikou.or.jp/basic.html	
high	read	無電解めっきと皮膜種類の実務整理に使うため	全国鍍金工業組合連合会（ぜんとれん）	https://zentoren.or.jp/mekki/hyoumenshori.html	
high	read	皮膜別の特性・用途を補うため	全国鍍金工業組合連合会（ぜんとれん）	https://zentoren.or.jp/mekki/shurui.html	
high	read	電子・自動車・半導体周辺用途を具体化するため	表面処理技術から未来を創造する	https://www.jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	
medium	read	公設試の観点で機能と応用を補強するため	防錆・防食のためのめっきの基礎知識	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	
high	read	排水規制とPFAS/六価クロム論点を押さえるため	Electroplating Effluent Guidelines | US EPA	https://www.epa.gov/eg/electroplating-effluent-guidelines	
high	read	クロムめっきの大気規制とばく露リスクを押さえるため	Chromium Electroplating: National Emission Standards for Hazardous Air Pollutants | US EPA	https://www.epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	
high	read	日本の排水基準の現行値を確認するため	一般排水基準 | 水・土壌・地盤・海洋環境の保全 | 環境省	https://www.env.go.jp/water/impure/haisui.html	
high	read	六価クロム暫定基準の現行運用を確認するため	六価クロム化合物の排水基準と暫定排水基準が改正されました（令和6年4月1日施行）／大阪府（おおさかふ）ホームページ	https://www.pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	
medium	selected	RoHSで六価クロムがどう位置づくか確認するため	RoHS Directive - Environment - European Commission	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en#law	
medium	selected	REACH上のニッケル制限を確認するため	ANNEX XVII TO REACH – Conditions of restriction	https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	
medium	read	六価クロムの健康影響と職業ばく露を整理するため	Hexavalent Chromium | National Institute of Environmental Health Sciences	https://www.niehs.nih.gov/health/topics/agents/hex-chromium	
medium	read	電子基板のめっき品質リスクを具体化するため	IPC Issues Electronics Industry Warning on Printed Board Microvia Reliability for High Performance Products | IPC International, Inc.	https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high
````

---

## FILE: sources\citation-ledger.tsv

````tsv
source_url	domain	citation_instances	sections	is_primary	source_role	title	source_flags
https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	jcu-i.com	22	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	false	vendor_first_party	表面処理技術から未来を創造する	preferred-domain,pdf
https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	www2.orist.jp	13	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	government_context	防錆・防食のためのめっきの基礎知識	preferred-domain,pdf
https://env.go.jp/water/impure/haisui.html	env.go.jp	11	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	official_regulator	一般排水基準 | 水・土壌・地盤・海洋環境の保全 | 環境省	preferred-domain,institutional-domain
https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	echa.europa.eu	10	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	legal_text	ANNEX XVII TO REACH – Conditions of restriction	preferred-domain
https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101	eur-lex.europa.eu	10	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	legal_text	Directive 2011/65/EU on the restriction of the use of certain hazardous substances in electrical and electronic equipment (consolidated text)	preferred-domain
https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	ipc.org	10	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	standards_body	IPC Issues Electronics Industry Warning on Printed Board Microvia Reliability for High Performance Products | IPC International, Inc.	preferred-domain
https://kizaikou.or.jp/basic.html	kizaikou.or.jp	10	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	false	industry_association	機材工 | 機材工 一般社団法人日本表面処理機材工業会	preferred-domain
https://epa.gov/eg/electroplating-effluent-guidelines	epa.gov	9	1. まず押さえる結論 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	official_regulator	Electroplating Effluent Guidelines | US EPA	preferred-domain,institutional-domain
https://fujielectric.co.jp/products/plating/about	fujielectric.co.jp	9	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	false	vendor_first_party	めっきとは ｜ 富士電機の表面処理（めっき） ｜ 富士電機	preferred-domain
https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	osha.gov	8	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	legal_text	1910.1026 - Chromium (VI). | Occupational Safety and Health Administration	preferred-domain,institutional-domain,official-looking-path
https://zentoren.or.jp/mekki/hyoumenshori.html	zentoren.or.jp	8	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	false	industry_association	全国鍍金工業組合連合会（ぜんとれん）	preferred-domain
https://mekki.sfj.or.jp/	mekki.sfj.or.jp	6	1. まず押さえる結論 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 6. 参照した主要ソース	true	professional_body	めっき部会｜表面技術協会	preferred-domain
https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	mhlw.go.jp	6	2. 読み手が先に知るべき要点 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと	true	official_regulator	新たな化学物質規制に関する特設サイト｜厚生労働省	preferred-domain,institutional-domain
https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	pref.osaka.lg.jp	6	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	true	legal_text	六価クロム化合物の排水基準と暫定排水基準が改正されました（令和6年4月1日施行）／大阪府（おおさかふ）ホームページ	neutral
https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	ulvac-techno.co.jp	6	1. まず押さえる結論 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 6. 参照した主要ソース	false	vendor_first_party	めっきとは？｜FAQ｜表面処理｜サービス｜アルバックテクノ	preferred-domain
https://sfj.or.jp/kaikoku/20220829Kansai.html	sfj.or.jp	5	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点	true	professional_body	2022年関西支部セミナー「湿式めっきの基礎」｜表面技術協会	preferred-domain
https://aen-mekki.or.jp/	aen-mekki.or.jp	4	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと	true	professional_body	HOME | 一般社団法人 日本溶融亜鉛鍍金協会	preferred-domain
https://env.go.jp/press/press_02720.html	env.go.jp	4	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 6. 参照した主要ソース	true	official_regulator	環境大臣が定める排水基準に係る検定方法等の一部改正について | 報道発表資料 | 環境省	preferred-domain,institutional-domain,official-looking-path
https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en	environment.ec.europa.eu	4	1. まず押さえる結論 | 2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点	true	legal_text	RoHS Directive - Environment - European Commission	preferred-domain
https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	epa.gov	4	1. まず押さえる結論 | 3. 判断に使う主要根拠 | 4. 方式選定で迷いやすい論点 | 6. 参照した主要ソース	true	official_regulator	Chromium Electroplating: National Emission Standards for Hazardous Air Pollutants | US EPA	preferred-domain,institutional-domain
https://niehs.nih.gov/health/topics/agents/hex-chromium	niehs.nih.gov	3	2. 読み手が先に知るべき要点 | 3. 判断に使う主要根拠 | 6. 参照した主要ソース	true	government_context	Hexavalent Chromium | National Institute of Environmental Health Sciences	institutional-domain
https://zentoren.or.jp/mekki/shurui.html	zentoren.or.jp	3	4. 方式選定で迷いやすい論点 | 5. 導入前に確認すべきこと | 6. 参照した主要ソース	false	industry_association	全国鍍金工業組合連合会（ぜんとれん）	preferred-domain
https://meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	meti.go.jp	2	2. 読み手が先に知るべき要点 | 4. 方式選定で迷いやすい論点	true	government_context	金属素材産業関係資料	preferred-domain,institutional-domain,pdf
https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	asminternational.org	1	4. 方式選定で迷いやすい論点	true	professional_body	Electroplated Coatings - ASM International	preferred-domain
https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e266a	echa.europa.eu	1	2. 読み手が先に知るべき要点	true	government_context	ECHA restricted substances under REACH - Nickel details	preferred-domain
````

---

## FILE: sources\claim-ledger.tsv

````tsv
claim_id	section	claim_kind	risk_level	claim_text	evidence_summary	evidence_urls	source_urls	source_domains	evidence_count	primary_source_count	source_role	confidence	status	required_fix	required_evidence_count	required_primary_count	gap_note	exact_date	jurisdiction	regulated_subject	scope	effective_date	transition_period	caveat
claim-001	## 1. まず押さえる結論	scope	medium	めっきは、狭義には電気的または化学的反応で基材表面に金属皮膜を形成する湿式表面処理であり、金属だけでなく一部の非金属基材にも適用されます。一方で、実務や営業表現では蒸着やスパッタ等の乾式法まで「広義のめっき」と呼ぶ例もあるため、レポートでは狭義の湿式めっきを主対象とし、乾式法は隣接概念として扱うのが安全です。表面技術協会 富士電機 アルバックテクノ	inline citation context	https://mekki.sfj.or.jp/ | https://fujielectric.co.jp/products/plating/about | https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	https://mekki.sfj.or.jp/ | https://fujielectric.co.jp/products/plating/about | https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	mekki.sfj.or.jp | fujielectric.co.jp | ulvac-techno.co.jp	3	1	professional_body | vendor_first_party	0.80	out_of_scope		0	0								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-002	## 1. まず押さえる結論	fact	high	実務上の中心は、外観処理だけではなく、防食、耐摩耗、導電、接触信頼性、はんだ付け性、拡散バリアといった機能付与です。需要先は自動車部品、機械部品、電気・電子部品、プリント基板、半導体周辺、建材、装飾部材まで広く、用途ごとに選ばれる方式と評価指標が大きく変わります。機材工 JCU 大阪府立産業技術総合研究所	inline citation context	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	kizaikou.or.jp | jcu-i.com | www2.orist.jp	3	1	industry_association | vendor_first_party | government_context	0.95	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-003	## 1. まず押さえる結論	scope	high	選定で本当に効くのは、「何をめっきするか」だけではなく、「何の機能を出したいか」「形状的に均一膜厚が要るか」「どの規制がかかるか」「不良がどの段階で顕在化するか」の4点です。とくに 2024年4月1日施行の日本の六価クロム排水基準見直し、米国のクロムめっき排水・大気規制、EU の RoHS/REACH は、方式選定とライン運用の前提条件として切り離せません。環境省 大阪府 US EPA 排水 US EPA 大気 欧州委員会 RoHS ECHA Annex XVII	inline citation context	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html | https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air | https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html | https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air | https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | pref.osaka.lg.jp | epa.gov | environment.ec.europa.eu | echa.europa.eu	6	6	official_regulator | legal_text	0.80	out_of_scope		0	0		2024-04-01	EU	hexavalent chromium				
claim-004	## 2. 読み手が先に知るべき要点	advice	high	電気めっきは汎用性と量産性に優れますが、電流分布の影響で膜厚が形状依存になりやすく、深穴や凹部の均一性が課題です。無電解めっきは複雑形状や非導体への適用で優位ですが、薬液管理とコスト負荷が重くなりやすいです。富士電機 全国鍍金工業組合連合会 表面技術協会	inline citation context	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	fujielectric.co.jp | zentoren.or.jp | sfj.or.jp	3	1	vendor_first_party | industry_association | professional_body	0.95	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-005	## 2. 読み手が先に知るべき要点	advice	medium	溶融亜鉛めっきは、精密電子用途のめっきと同じ土俵で比較すると誤ります。鋼構造物や屋外使用部材で、防食寿命と全浸漬性を重視する別系統の意思決定です。日本溶融亜鉛鍍金協会 大阪府立産業技術総合研究所	inline citation context	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	aen-mekki.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1			Japan					
claim-006	## 2. 読み手が先に知るべき要点	advice	medium	自動車と電子部品は、今もめっきの中心需要先です。自動車では防食と摩擦係数、電子・半導体周辺では導電、接続、界面品質、熱履歴後の信頼性が重くなります。機材工 JCU 経済産業省	inline citation context	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	kizaikou.or.jp | jcu-i.com | meti.go.jp	3	1	industry_association | vendor_first_party | government_context	0.95	ok		2	1			Japan					industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-007	## 2. 読み手が先に知るべき要点	advice	high	電子用途では、プリント基板、ビア形成、コネクタ、リードフレーム、半導体パッケージ基板まで、銅・ニッケル・金・銀・すず系の組合せが使い分けられます。品質問題は出荷時に顕在化しないこともあり、IPC は microvia-to-target plating failure の潜在化を警告しています。JCU IPC	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	jcu-i.com | ipc.org	2	1	vendor_first_party | standards_body	0.85	ok		2	1				nickel	product use and exposure conditions			
claim-008	## 2. 読み手が先に知るべき要点	advice	medium	工程管理上は、前処理、浴組成、添加剤、不純物、洗浄、乾燥、検査の総合管理が重要で、薬品単価だけでは総コストを語れません。歩留まり、再処理率、停止頻度、分析自動化、廃液・排気処理が効いてきます。大阪府立産業技術総合研究所 表面技術協会 JCU	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://sfj.or.jp/kaikoku/20220829Kansai.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://sfj.or.jp/kaikoku/20220829Kansai.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	www2.orist.jp | sfj.or.jp | jcu-i.com	3	2	government_context | professional_body | vendor_first_party	0.95	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-009	## 2. 読み手が先に知るべき要点	temporal	high	日本では、六価クロムの一般排水基準は 0.2 mg Cr(VI)/L で、2024年4月1日から電気めっき業の特定事業場には 0.5 mg/L の暫定基準が3年間適用されています。さらに 2024年2月5日には測定法も JIS K0102-3 ベースへ改められました。環境省 排水基準 大阪府 環境省 測定法改正	inline citation context	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html | https://env.go.jp/press/press_02720.html	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html | https://env.go.jp/press/press_02720.html	env.go.jp | pref.osaka.lg.jp	3	3	official_regulator | legal_text	0.95	ok		2	1		2024-02-05 | 2024-04-01	Japan	hexavalent chromium		2024-02-05	3 years	
claim-010	## 2. 読み手が先に知るべき要点	regulatory	high	労働安全は個別規則だけでなく、自律的管理への移行が進んでいます。六価クロムは OSHA でも PEL 5 µg/m3、アクションレベル 2.5 µg/m3 という明確な基準があり、ばく露測定と是正が中心論点です。厚生労働省 OSHA NIEHS	inline citation context	https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://niehs.nih.gov/health/topics/agents/hex-chromium	https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://niehs.nih.gov/health/topics/agents/hex-chromium	mhlw.go.jp | osha.gov | niehs.nih.gov	3	3	official_regulator | legal_text | government_context	0.95	ok		2	1			Japan	hexavalent chromium				
claim-011	## 2. 読み手が先に知るべき要点	regulatory	high	EU では、RoHS が EEE 中の六価クロムを制限し、REACH Annex XVII Entry 27 はニッケルを「総量」ではなく皮膚接触時の放出条件で縛ります。RoHS 適合と REACH 適合は別問題であり、製品スコープと接触条件を付けて書く必要があります。EUR-Lex RoHS 欧州委員会 RoHS ECHA Annex XVII ECHA nickel details	inline citation context	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e266a	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e266a	eur-lex.europa.eu | environment.ec.europa.eu | echa.europa.eu	4	4	legal_text | government_context	0.95	ok		2	1			EU	hexavalent chromium	electrical and electronic equipment			
claim-012	## 3. 判断に使う主要根拠	fact	low	めっきは基材表面に金属皮膜を形成して機能を付与する技術で、狭義では湿式反応、広義では乾式法まで含む用法がある。	表面技術協会と富士電機は湿式めっきの定義を示し、アルバックテクノは蒸着・スパッタ等を含む広義用法を明示している。	https://mekki.sfj.or.jp/ | https://fujielectric.co.jp/products/plating/about | https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	https://mekki.sfj.or.jp/ | https://fujielectric.co.jp/products/plating/about | https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	mekki.sfj.or.jp | fujielectric.co.jp | ulvac-techno.co.jp	3	1	professional_body | vendor_first_party	0.95	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-013	## 3. 判断に使う主要根拠	fact	low	電気めっき、無電解めっき、溶融めっきは、原理も向く用途も異なるため分けて比較すべきである。	富士電機は電気・無電解・置換を区別し、全鍍連は無電解の均一析出性を説明し、日本溶融亜鉛鍍金協会は溶融亜鉛めっきを独立した技術分野として扱う。	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html | https://aen-mekki.or.jp/	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html | https://aen-mekki.or.jp/	fujielectric.co.jp | zentoren.or.jp | aen-mekki.or.jp	3	1	vendor_first_party | industry_association | professional_body	0.95	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-014	## 3. 判断に使う主要根拠	fact	low	自動車、機械、電気電子、建材は代表的な需要先であり、めっきは装飾だけでなく防食・導電・接続機能を担う。	機材工は代表用途を自動車部品、機械部品、電気電子部品、装飾部品と整理し、JCU は自動車部品、基板、電子部品、半導体周辺を具体例として挙げる。	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	kizaikou.or.jp | jcu-i.com	2	0	industry_association | vendor_first_party	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-015	## 3. 判断に使う主要根拠	fact	low	電子用途では、基板・微細配線・コネクタ等でめっき品質が接続信頼性を左右し、潜在不良は熱負荷後に顕在化しうる。	JCU は基板・ビアフィル・電子部品・半導体PKG基板向け銅めっき薬品を整理し、IPC は microvia-to-target plating failure が従来検査をすり抜けると警告している。	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	jcu-i.com | ipc.org	2	1	vendor_first_party | standards_body	0.85	ok		2	1								
claim-016	## 3. 判断に使う主要根拠	fact	high	工程不良の多くは前処理、浴管理、膜厚均一性、密着性、異物管理の失敗として現れる。	ORIST はめっきの利用分野と前処理・機能を整理し、表面技術協会の湿式めっき基礎セミナーは無電解ニッケルの選定・管理方法の重要性を示している。	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://sfj.or.jp/kaikoku/20220829Kansai.html	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://sfj.or.jp/kaikoku/20220829Kansai.html	www2.orist.jp | sfj.or.jp	2	2	government_context | professional_body	0.95	ok		2	1								
claim-017	## 3. 判断に使う主要根拠	fact	high	日本では六価クロムの一般排水基準が 0.2 mg Cr(VI)/L に整理され、2024年4月1日から電気めっき業には 0.5 mg/L の暫定基準が3年間適用されている。	環境省の一般排水基準ページが 0.2 mg Cr(VI)/L を示し、大阪府ページが 2024年4月1日施行の暫定基準 0.5 mg/L を説明している。	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	env.go.jp | pref.osaka.lg.jp	2	2	official_regulator | legal_text	0.95	ok		2	1		2024-04-01	Japan	hexavalent chromium			3 years	
claim-018	## 3. 判断に使う主要根拠	fact	high	2024年2月5日、日本では六価クロムの測定法も見直され、JIS K0102-3 ベースへ改められた。	環境省の 2024-02-05 報道発表は、六価クロム化合物の検定法・測定法を JIS K0102-3 に改めたことを明示している。	https://env.go.jp/press/press_02720.html | https://env.go.jp/water/impure/haisui.html	https://env.go.jp/press/press_02720.html | https://env.go.jp/water/impure/haisui.html	env.go.jp	2	2	official_regulator	0.95	ok		2	1		2024-02-05	Japan	hexavalent chromium				
claim-019	## 3. 判断に使う主要根拠	fact	high	米国では、めっきは排水規制と大気規制の両面から管理され、クロム工程では PFAS と六価クロムが同時論点化している。	EPA の電気めっき排水ガイドラインは chrome finishing facilities と PFAS 論点を示し、クロムめっき NESHAP は hard/decorative chromium electroplating を対象にしている。	https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	epa.gov	2	2	official_regulator	0.95	ok		2	1			United States	hexavalent chromium				
claim-020	## 3. 判断に使う主要根拠	fact	high	六価クロムは電気めっきで広く使われる一方、職業ばく露の健康影響が強く意識されている。	NIEHS は electroplating を主要用途に挙げ、OSHA は PEL 5 µg/m3 と action level 2.5 µg/m3 を定めている。	https://niehs.nih.gov/health/topics/agents/hex-chromium | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	https://niehs.nih.gov/health/topics/agents/hex-chromium | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	niehs.nih.gov | osha.gov	2	2	government_context | legal_text	0.95	ok		2	1			United States	hexavalent chromium				
claim-021	## 3. 判断に使う主要根拠	fact	high	EU では、EEE 向けには RoHS が六価クロムを制限し、皮膚接触品には REACH Annex XVII Entry 27 のニッケル放出条件が効く。	欧州委員会と EUR-Lex の RoHS 文書が hexavalent chromium を制限対象に挙げ、ECHA 文書が Entry 27 のニッケル条件を整理している。	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	environment.ec.europa.eu | eur-lex.europa.eu | echa.europa.eu	3	3	legal_text	0.95	ok		2	1			EU	hexavalent chromium	electrical and electronic equipment			
claim-022	### 4.1 方式比較の見取り図	fact	low	電気めっき - 主な使いどころ: 自動車部品、コネクタ、外観部材、一般機能皮膜	table cell	https://fujielectric.co.jp/products/plating/about | https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	https://fujielectric.co.jp/products/plating/about | https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	fujielectric.co.jp | asminternational.org	2	1	vendor_first_party | professional_body	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-023	### 4.1 方式比較の見取り図	fact	low	電気めっき - 強み: 金属種の選択肢が広く、量産しやすく、コスト/性能バランスが良い	table cell	https://fujielectric.co.jp/products/plating/about | https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	https://fujielectric.co.jp/products/plating/about | https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	fujielectric.co.jp | asminternational.org	2	1	vendor_first_party | professional_body	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-024	### 4.1 方式比較の見取り図	fact	high	電気めっき - 主な弱み・注意: 形状依存で膜厚が偏りやすい。前処理と電流分布設計が重要	table cell	https://fujielectric.co.jp/products/plating/about | https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	https://fujielectric.co.jp/products/plating/about | https://asminternational.org/results/-/journal_content/56/ASMHBA0003687/BOOK-ARTICLE	fujielectric.co.jp | asminternational.org	2	1	vendor_first_party | professional_body	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-025	### 4.1 方式比較の見取り図	fact	high	無電解めっき - 主な使いどころ: 複雑形状、非導体、均一膜厚重視、精密部品	table cell	https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	zentoren.or.jp | sfj.or.jp	2	1	industry_association | professional_body	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees
claim-026	### 4.1 方式比較の見取り図	fact	low	無電解めっき - 強み: 電流分布に縛られず均一析出しやすい	table cell	https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	zentoren.or.jp | sfj.or.jp	2	1	industry_association | professional_body	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees
claim-027	### 4.1 方式比較の見取り図	fact	low	無電解めっき - 主な弱み・注意: 浴安定性、還元剤管理、コスト、浴寿命が論点	table cell	https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	https://zentoren.or.jp/mekki/hyoumenshori.html | https://sfj.or.jp/kaikoku/20220829Kansai.html	zentoren.or.jp | sfj.or.jp	2	1	industry_association | professional_body	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees
claim-028	### 4.1 方式比較の見取り図	fact	low	溶融亜鉛めっき - 主な使いどころ: 鋼構造物、建材、屋外部材	table cell	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	aen-mekki.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								
claim-029	### 4.1 方式比較の見取り図	fact	low	溶融亜鉛めっき - 強み: 厚い防食皮膜、犠牲防食、全浸漬性	table cell	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	aen-mekki.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								
claim-030	### 4.1 方式比較の見取り図	fact	low	溶融亜鉛めっき - 主な弱み・注意: 精密電子用途のような微細制御には向かない	table cell	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://aen-mekki.or.jp/ | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	aen-mekki.or.jp | www2.orist.jp	2	2	professional_body | government_context	0.95	ok		2	1								
claim-031	### 4.1 方式比較の見取り図	fact	low	乾式/真空系表面処理 - 主な使いどころ: 意匠膜、薄膜機能、真空成膜	table cell	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	ulvac-techno.co.jp | mekki.sfj.or.jp	2	1	vendor_first_party | professional_body	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-032	### 4.1 方式比較の見取り図	fact	low	乾式/真空系表面処理 - 強み: 薄膜制御、湿式とは別の材料設計が可能	table cell	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	ulvac-techno.co.jp | mekki.sfj.or.jp	2	1	vendor_first_party | professional_body	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-033	### 4.1 方式比較の見取り図	scope	low	乾式/真空系表面処理 - 主な弱み・注意: 狭義のめっきと混同しやすく、工程比較の前提がずれる	table cell	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	ulvac-techno.co.jp | mekki.sfj.or.jp	2	1	vendor_first_party | professional_body	0.80	out_of_scope		0	0								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-034	### 4.2 何が選定を分けるか	advice	high	方式差でまず見るべきは、電流を使うかどうかではなく、形状依存性と基材適合性です。深穴や複雑形状で均一膜厚が必須なら、電気めっき単独より無電解やシード層併用が候補に上がります。富士電機 全国鍍金工業組合連合会	inline citation context	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	fujielectric.co.jp | zentoren.or.jp	2	0	vendor_first_party | industry_association	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-035	### 4.2 何が選定を分けるか	fact	low	用途差では、防食系と電子系を一括で語らない方がよいです。前者は耐食寿命や後処理、後者は接触信頼性、ボイド、界面、熱サイクル後の不良顕在化が中心になります。機材工 IPC	inline citation context	https://kizaikou.or.jp/basic.html | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://kizaikou.or.jp/basic.html | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	kizaikou.or.jp | ipc.org	2	1	industry_association | standards_body	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees
claim-036	### 4.2 何が選定を分けるか	regulatory	high	コスト差では、薬品単価よりライン停止、再処理、検査負荷、排水・排気処理の方が効く場面が多いです。これは、環境規制と品質保証が工程そのものに組み込まれているからです。JCU US EPA 排水	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://epa.gov/eg/electroplating-effluent-guidelines	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://epa.gov/eg/electroplating-effluent-guidelines	jcu-i.com | epa.gov	2	1	vendor_first_party | official_regulator	0.85	ok		2	1			United States	wastewater discharge				
claim-037	### 4.2 何が選定を分けるか	regulatory	high	規制差では、同じめっきでも「製品中の制限」「皮膚接触時の放出」「作業者ばく露」「排水」「大気排出」が別の法体系で管理されます。設計段階で混同すると、後工程での是正コストが大きくなります。EUR-Lex RoHS ECHA Annex XVII OSHA 環境省 排水基準	inline citation context	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://env.go.jp/water/impure/haisui.html	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://env.go.jp/water/impure/haisui.html	eur-lex.europa.eu | echa.europa.eu | osha.gov | env.go.jp	4	4	legal_text | official_regulator	0.95	ok		2	1			EU	hazardous substances in EEE	skin-contact release condition			
claim-038	### 4.3 用途別に見た方式の役割	fact	low	需要側の類型: 防食・耐候を重視する鋼部品/建材系、自動車の意匠・機能部品系、電子部品/基板/半導体周辺系で、採用する皮膜と検査指標が大きく違います。機材工 JCU	inline citation context	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://kizaikou.or.jp/basic.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	kizaikou.or.jp | jcu-i.com	2	0	industry_association | vendor_first_party	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-039	### 4.3 用途別に見た方式の役割	fact	low	供給側の類型: 日本では、めっき加工会社、薬品メーカー、装置メーカー、分析・検査、顧客品質保証が分業で動く構造が強く、材料選定より責任分担設計が実務上重要です。JCU 機材工	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	jcu-i.com | kizaikou.or.jp	2	0	vendor_first_party | industry_association	0.85	ok		2	1			Japan					industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-040	### 4.3 用途別に見た方式の役割	fact	high	技術類型: 亜鉛系防食、ニッケル系機能皮膜、銅系導電/配線形成、貴金属系接点/装飾、クロム系外観・硬質用途などに分けると、用途と不具合モードを整理しやすくなります。全国鍍金工業組合連合会 大阪府立産業技術総合研究所	inline citation context	https://zentoren.or.jp/mekki/shurui.html | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://zentoren.or.jp/mekki/shurui.html | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	zentoren.or.jp | www2.orist.jp	2	1	industry_association | government_context	0.85	ok		2	1				nickel	product use and exposure conditions			industry association evidence is best used for sector context, not plant-specific guarantees
claim-041	### 4.4 工程全体と関係者のつながり	regulatory	high	上流では、化学薬品、前処理、治具、整流器、排気、排水処理が一体で工程能力を決めます。めっきそのものだけを最適化しても、洗浄・乾燥・排水で詰まると量産は安定しません。US EPA 排水 厚生労働省	inline citation context	https://epa.gov/eg/electroplating-effluent-guidelines | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	https://epa.gov/eg/electroplating-effluent-guidelines | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	epa.gov | mhlw.go.jp	2	2	official_regulator	0.95	ok		2	1			Japan	wastewater discharge				
claim-042	### 4.4 工程全体と関係者のつながり	fact	low	中流では、専業めっき会社と自社ラインの両方が存在し、用途ごとに薬品メーカーや装置メーカーの標準プロセスが事実上の参照軸になります。JCU 機材工	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	jcu-i.com | kizaikou.or.jp	2	0	vendor_first_party | industry_association	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-043	### 4.4 工程全体と関係者のつながり	fact	high	下流では、自動車 OEM/Tier、電子部品メーカー、基板メーカー、半導体パッケージ基板メーカー、建材用途が主要な受け皿です。下流側の要求が、膜厚、公差、トレーサビリティ、規制適合の仕様へ跳ね返ります。JCU 経済産業省	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://meti.go.jp/policy/mono_info_service/mono/iron_and_steel/downloadfiles/kinzokusozai2.pdf	jcu-i.com | meti.go.jp	2	1	vendor_first_party | government_context	0.85	ok		2	1			Japan					vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-044	### 4.5 例外条件と誤解しやすい境界	fact	low	「めっき = 電気めっき」と断定すると、無電解めっきや溶融めっき、さらには広義の乾式法との境界を取り違えます。逆に「真空蒸着も全部めっき」と書くと、工程比較が雑になります。表面技術協会 アルバックテクノ	inline citation context	https://mekki.sfj.or.jp/ | https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	https://mekki.sfj.or.jp/ | https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html	mekki.sfj.or.jp | ulvac-techno.co.jp	2	1	professional_body | vendor_first_party	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-045	### 4.5 例外条件と誤解しやすい境界	advice	medium	「外観が良い = 品質が高い」も危険です。電子用途では潜在不良がリフロー後や現地使用後に出ることがあり、逆に防食用途では外観差が直ちに寿命差を意味しない場合があります。IPC 大阪府立産業技術総合研究所	inline citation context	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	ipc.org | www2.orist.jp	2	2	standards_body | government_context	0.95	ok		2	1								
claim-046	### 4.5 例外条件と誤解しやすい境界	regulatory	high	「六価クロムは禁止済み」「ニッケルめっきは違法」といった書き方も誤りです。実際には、国・用途・接触条件・法体系ごとに結論が違います。EUR-Lex RoHS ECHA Annex XVII OSHA	inline citation context	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026	eur-lex.europa.eu | echa.europa.eu | osha.gov	3	3	legal_text	0.95	ok		2	1			EU	hexavalent chromium	product use and exposure conditions			
claim-047	### 4.6 直近の制度変更と日付	scope	high	2011年7月21日: 現行の RoHS 指令 2011/65/EU が発効し、EEE における有害物質制限の基盤となりました。2025年1月1日時点の統合版でも六価クロムは制限対象です。欧州委員会 RoHS EUR-Lex RoHS	inline citation context	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101	https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101	environment.ec.europa.eu | eur-lex.europa.eu	2	2	legal_text	0.80	out_of_scope		0	0		2011-07-21 | 2025-01-01	EU	hexavalent chromium	electrical and electronic equipment			
claim-048	### 4.6 直近の制度変更と日付	scope	low	2022年5月31日以降: 日本では化学物質の自律的管理への制度改正が段階的に進み、めっき薬品を含む現場管理の負荷が高まっています。厚生労働省	inline citation context	https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html	mhlw.go.jp	1	1	official_regulator	0.80	out_of_scope		0	0		2022-05-31	Japan					
claim-049	### 4.6 直近の制度変更と日付	temporal	high	2024年2月5日: 環境省が六価クロムに関する測定法見直しを公表し、JIS K0102-3 ベースへ改正しました。環境省 測定法改正	inline citation context	https://env.go.jp/press/press_02720.html	https://env.go.jp/press/press_02720.html	env.go.jp	1	1	official_regulator	0.85	ok		2	1		2024-02-05	Japan	hexavalent chromium		2024-02-05		
claim-050	### 4.6 直近の制度変更と日付	temporal	high	2024年4月1日: 日本の六価クロム排水基準改正が施行され、一般排水基準 0.2 mg/L、電気めっき業の暫定基準 0.5 mg/L が実務上の焦点になりました。環境省 排水基準 大阪府	inline citation context	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	env.go.jp | pref.osaka.lg.jp	2	2	official_regulator | legal_text	0.95	ok		2	1		2024-04-01	Japan	hexavalent chromium		2024-04-01	temporary transitional measure	
claim-051	### 4.6 直近の制度変更と日付	temporal	high	2021年以降継続中: EPA は chrome finishing facilities の PFAS 排出を理由に、電気めっき/金属仕上げカテゴリの見直しを進めています。2026年4月19日時点でも、クロム系工程は六価クロムだけでなく PFAS 論点と一体で読む必要があります。US EPA 排水 US EPA 大気	inline citation context	https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	https://epa.gov/eg/electroplating-effluent-guidelines | https://epa.gov/stationary-sources-air-pollution/chromium-electroplating-national-emission-standards-hazardous-air	epa.gov	2	2	official_regulator	0.95	ok		2	1		2026-04-19	United States	hexavalent chromium		2026-04-19		
claim-052	### 4.7 見落としやすい実務リスク	scope	high	定義と境界の取り違え: 湿式めっき、乾式表面処理、溶融めっきを同じ比較表で一律に扱うと、設備要件、工程設計、品質保証の前提がずれます。まず「電析 / 無電解 / 溶融 / 乾式」のどこを比較しているのかを固定しないと、後段の原価比較や規制整理も誤ります。アルバックテクノ 表面技術協会	inline citation context	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	https://ulvac-techno.co.jp/service/surface_treatment/faq/001.html | https://mekki.sfj.or.jp/	ulvac-techno.co.jp | mekki.sfj.or.jp	2	1	vendor_first_party | professional_body	0.80	out_of_scope		0	0								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-053	### 4.7 見落としやすい実務リスク	fact	high	品質と信頼性の見落とし: 前処理不足は密着不良、剥離、ピット、ブリスターの起点になり、浴管理不良は膜厚不均一、析出ムラ、再処理増を招きます。電子部品では接触抵抗、はんだ付け性、熱履歴後の界面健全性まで見ないと、外観合格でも後工程で不良化します。大阪府立産業技術総合研究所 JCU IPC	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	www2.orist.jp | jcu-i.com | ipc.org	3	2	government_context | vendor_first_party | standards_body	0.95	ok		2	1								
claim-054	### 4.7 見落としやすい実務リスク	advice	high	材料・用途依存の落とし穴: 高強度鋼やばね材では、水素脆化リスクとめっき後ベーキング要否を仕様段階で確認しないと、機械特性低下や遅れ破壊を見逃します。HDI 基板や先端パッケージでは、microvia 周りのめっきは一般的な厚付け発想をそのまま適用できず、界面品質と後工程条件を別管理する必要があります。大阪府立産業技術総合研究所 JCU IPC	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	www2.orist.jp | jcu-i.com | ipc.org	3	2	government_context | vendor_first_party | standards_body	0.95	ok		2	1				microvia reliability	high-strength steel components			
claim-055	### 4.7 見落としやすい実務リスク	scope	high	規制と EHS の取り違え: 同じめっきでも、排水、排気、作業者ばく露、製品中含有、皮膚接触によるニッケル放出では根拠法令が異なります。RoHS / REACH、国内排水基準、クロム・ニッケルの労安管理を同じ論点として扱うと対応漏れが出ます。環境省 排水基準 厚生労働省 OSHA EUR-Lex RoHS ECHA Annex XVII	inline citation context	https://env.go.jp/water/impure/haisui.html | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | mhlw.go.jp | osha.gov | eur-lex.europa.eu | echa.europa.eu	5	5	official_regulator | legal_text	0.80	out_of_scope		0	0			EU	nickel	skin-contact release condition			
claim-056	### 4.7 見落としやすい実務リスク	regulatory	high	運用と原価の過小評価: 薬品単価だけでなく、浴分析頻度、補給管理、前処理再現性、排水処理、排気、トレーサビリティ、再処理、停止時間まで含めて見ないと、見積り時より総コストが悪化しやすいです。表面技術協会 US EPA 排水 JCU	inline citation context	https://sfj.or.jp/kaikoku/20220829Kansai.html | https://epa.gov/eg/electroplating-effluent-guidelines | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://sfj.or.jp/kaikoku/20220829Kansai.html | https://epa.gov/eg/electroplating-effluent-guidelines | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	sfj.or.jp | epa.gov | jcu-i.com	3	2	professional_body | official_regulator | vendor_first_party	0.95	ok		2	1			United States	wastewater discharge				
claim-057	### 5.1 選定前の実務チェックリスト	advice	high	防食目的で鋼部品を処理する - 先に固定すること: 使用環境、要求寿命、後処理、必要膜厚レンジ、構造物サイズを先に固定する	table cell	https://aen-mekki.or.jp/ | https://zentoren.or.jp/mekki/shurui.html	https://aen-mekki.or.jp/ | https://zentoren.or.jp/mekki/shurui.html	aen-mekki.or.jp | zentoren.or.jp	2	1	professional_body | industry_association	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees
claim-058	### 5.1 選定前の実務チェックリスト	advice	high	防食目的で鋼部品を処理する - 判断を誤りやすい理由: 亜鉛電気めっきと溶融亜鉛めっきでは比較軸とコスト構造が大きく違う	table cell	https://aen-mekki.or.jp/ | https://zentoren.or.jp/mekki/shurui.html	https://aen-mekki.or.jp/ | https://zentoren.or.jp/mekki/shurui.html	aen-mekki.or.jp | zentoren.or.jp	2	1	professional_body | industry_association	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees
claim-059	### 5.1 選定前の実務チェックリスト	advice	high	防食目的で鋼部品を処理する - 根拠・注意: 日本溶融亜鉛鍍金協会 全国鍍金工業組合連合会	table cell	https://aen-mekki.or.jp/ | https://zentoren.or.jp/mekki/shurui.html	https://aen-mekki.or.jp/ | https://zentoren.or.jp/mekki/shurui.html	aen-mekki.or.jp | zentoren.or.jp	2	1	professional_body | industry_association	0.85	ok		2	1			Japan					industry association evidence is best used for sector context, not plant-specific guarantees
claim-060	### 5.1 選定前の実務チェックリスト	scope	high	高強度鋼・ばね材を扱う - 先に固定すること: 水素脆化リスク、めっき後ベーキング要否、図面 / 材質仕様の管理責任を確認する	table cell	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	www2.orist.jp | zentoren.or.jp	2	1	government_context | industry_association	0.80	out_of_scope		0	0					high-strength steel components			industry association evidence is best used for sector context, not plant-specific guarantees
claim-061	### 5.1 選定前の実務チェックリスト	scope	high	高強度鋼・ばね材を扱う - 判断を誤りやすい理由: 強度保証を落とすと遅れ破壊が後工程や実使用で現れる	table cell	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	www2.orist.jp | zentoren.or.jp	2	1	government_context | industry_association	0.80	out_of_scope		0	0					high-strength steel components			industry association evidence is best used for sector context, not plant-specific guarantees
claim-062	### 5.1 選定前の実務チェックリスト	scope	high	高強度鋼・ばね材を扱う - 根拠・注意: 大阪府立産業技術総合研究所 全国鍍金工業組合連合会	table cell	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	www2.orist.jp | zentoren.or.jp	2	1	government_context | industry_association	0.80	out_of_scope		0	0					high-strength steel components			industry association evidence is best used for sector context, not plant-specific guarantees
claim-063	### 5.1 選定前の実務チェックリスト	advice	high	電子部品・基板用途を選定する - 先に固定すること: 膜厚均一性、ボイド、界面、熱サイクル後信頼性に加え、HDI / microvia 条件を別項目で確認する	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	jcu-i.com | ipc.org	2	1	vendor_first_party | standards_body	0.85	ok		2	1				microvia reliability				
claim-064	### 5.1 選定前の実務チェックリスト	advice	high	電子部品・基板用途を選定する - 判断を誤りやすい理由: 初期検査合格でも microvia や界面起点の潜在不良が後で出る	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	jcu-i.com | ipc.org	2	1	vendor_first_party | standards_body	0.85	ok		2	1				microvia reliability				
claim-065	### 5.1 選定前の実務チェックリスト	advice	high	電子部品・基板用途を選定する - 根拠・注意: JCU IPC	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	jcu-i.com | ipc.org	2	1	vendor_first_party | standards_body	0.85	ok		2	1								
claim-066	### 5.1 選定前の実務チェックリスト	advice	high	コネクタ・接点用途を選定する - 先に固定すること: 接触抵抗、摩耗後の導通、孔食 / ブリスター、下地金属との組み合わせを確認する	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://fujielectric.co.jp/products/plating/about	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://fujielectric.co.jp/products/plating/about	jcu-i.com | fujielectric.co.jp	2	0	vendor_first_party	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-067	### 5.1 選定前の実務チェックリスト	advice	high	コネクタ・接点用途を選定する - 判断を誤りやすい理由: 外観や名目膜厚だけでは通電安定性を判断できない	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://fujielectric.co.jp/products/plating/about	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://fujielectric.co.jp/products/plating/about	jcu-i.com | fujielectric.co.jp	2	0	vendor_first_party	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-068	### 5.1 選定前の実務チェックリスト	advice	high	コネクタ・接点用途を選定する - 根拠・注意: JCU 富士電機	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://fujielectric.co.jp/products/plating/about	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://fujielectric.co.jp/products/plating/about	jcu-i.com | fujielectric.co.jp	2	0	vendor_first_party	0.85	ok		2	1								vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-069	### 5.1 選定前の実務チェックリスト	scope	high	はんだ接合を前提にする - 先に固定すること: 表面仕上げとはんだ付け性、保管後 / リフロー後のぬれ性、後工程フラックス条件を確認する	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	jcu-i.com | kizaikou.or.jp	2	0	vendor_first_party | industry_association	0.80	out_of_scope		0	0								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-070	### 5.1 選定前の実務チェックリスト	scope	high	はんだ接合を前提にする - 判断を誤りやすい理由: 「導電性がある」と「はんだ付けしやすい」は同義ではない	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	jcu-i.com | kizaikou.or.jp	2	0	vendor_first_party | industry_association	0.80	out_of_scope		0	0								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-071	### 5.1 選定前の実務チェックリスト	scope	high	はんだ接合を前提にする - 根拠・注意: JCU 機材工	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://kizaikou.or.jp/basic.html	jcu-i.com | kizaikou.or.jp	2	0	vendor_first_party | industry_association	0.80	out_of_scope		0	0								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-072	### 5.1 選定前の実務チェックリスト	advice	high	複雑形状や非導体に処理する - 先に固定すること: 前処理、活性化、シード層、無電解併用の要否と厚み分布限界を確認する	table cell	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	fujielectric.co.jp | zentoren.or.jp	2	0	vendor_first_party | industry_association	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-073	### 5.1 選定前の実務チェックリスト	advice	high	複雑形状や非導体に処理する - 判断を誤りやすい理由: 前処理不足と形状依存で密着不良・膜厚不均一・ピット / ブリスターが増えやすい	table cell	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	fujielectric.co.jp | zentoren.or.jp	2	0	vendor_first_party | industry_association	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-074	### 5.1 選定前の実務チェックリスト	advice	high	複雑形状や非導体に処理する - 根拠・注意: 富士電機 全国鍍金工業組合連合会	table cell	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	https://fujielectric.co.jp/products/plating/about | https://zentoren.or.jp/mekki/hyoumenshori.html	fujielectric.co.jp | zentoren.or.jp	2	0	vendor_first_party | industry_association	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees; vendor evidence should be checked against the actual process, substrate, and acceptance test
claim-075	### 5.1 選定前の実務チェックリスト	advice	high	クロム・ニッケル系を採用する - 先に固定すること: 排水、大気、作業者ばく露、RoHS、REACH、ニッケル放出のどれが効くかをレイヤー別に切り分ける	table cell	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | osha.gov | eur-lex.europa.eu | echa.europa.eu	4	4	official_regulator | legal_text	0.95	ok		2	1			EU	nickel	skin-contact release condition			
claim-076	### 5.1 選定前の実務チェックリスト	advice	high	クロム・ニッケル系を採用する - 判断を誤りやすい理由: 法体系が違い、代替判断も一律ではない	table cell	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | osha.gov | eur-lex.europa.eu | echa.europa.eu	4	4	official_regulator | legal_text	0.95	ok		2	1			EU	nickel				
claim-077	### 5.1 選定前の実務チェックリスト	advice	high	クロム・ニッケル系を採用する - 根拠・注意: 環境省 排水基準 OSHA EUR-Lex RoHS ECHA Annex XVII	table cell	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://env.go.jp/water/impure/haisui.html | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	env.go.jp | osha.gov | eur-lex.europa.eu | echa.europa.eu	4	4	official_regulator | legal_text	0.95	ok		2	1			EU	nickel				
claim-078	### 5.1 選定前の実務チェックリスト	advice	high	ライン改善や外注切替を検討する - 先に固定すること: 薬品単価だけでなく、浴分析頻度、補給管理、再処理率、停止頻度、排水 / 排気能力、トレーサビリティを確認する	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://epa.gov/eg/electroplating-effluent-guidelines	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://epa.gov/eg/electroplating-effluent-guidelines	jcu-i.com | mhlw.go.jp | epa.gov	3	2	vendor_first_party | official_regulator	0.95	ok		2	1			Japan	wastewater discharge				
claim-079	### 5.1 選定前の実務チェックリスト	advice	high	ライン改善や外注切替を検討する - 判断を誤りやすい理由: 総コストと監査負荷は浴管理と周辺インフラで大きく変わる	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://epa.gov/eg/electroplating-effluent-guidelines	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://epa.gov/eg/electroplating-effluent-guidelines	jcu-i.com | mhlw.go.jp | epa.gov	3	2	vendor_first_party | official_regulator	0.95	ok		2	1			Japan					
claim-080	### 5.1 選定前の実務チェックリスト	advice	high	ライン改善や外注切替を検討する - 根拠・注意: JCU 厚生労働省 US EPA 排水	table cell	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://epa.gov/eg/electroplating-effluent-guidelines	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://epa.gov/eg/electroplating-effluent-guidelines	jcu-i.com | mhlw.go.jp | epa.gov	3	2	vendor_first_party | official_regulator	0.95	ok		2	1			Japan	wastewater discharge				
claim-081	### 5.2 判断を誤らないための運用ルール	advice	high	方式名から入らず、まず「失敗すると困る機能」「受入れ試験」「使用環境」を先に固定する。防食、接続、外観、耐摩耗、はんだ付け性のどれを守るのかが曖昧なまま比較表を作ると、社内説明も見積り比較もぶれます。機材工 大阪府立産業技術総合研究所	inline citation context	https://kizaikou.or.jp/basic.html | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	https://kizaikou.or.jp/basic.html | https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf	kizaikou.or.jp | www2.orist.jp	2	1	industry_association | government_context	0.85	ok		2	1								industry association evidence is best used for sector context, not plant-specific guarantees
claim-082	### 5.2 判断を誤らないための運用ルール	advice	high	高強度鋼・ばね材では、水素脆化とベーキング要否を工程条件の後追いではなく、図面・材質仕様・外注条件に先に入れる。ここを曖昧にすると、めっき後に強度保証だけが抜け落ちます。大阪府立産業技術総合研究所 全国鍍金工業組合連合会	inline citation context	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	https://www2.orist.jp/dl/izumi/archive/Gijutsu_shiryo/Corr.pdf | https://zentoren.or.jp/mekki/hyoumenshori.html	www2.orist.jp | zentoren.or.jp	2	1	government_context | industry_association	0.85	ok		2	1					high-strength steel components			industry association evidence is best used for sector context, not plant-specific guarantees
claim-083	### 5.2 判断を誤らないための運用ルール	advice	high	電子部品、コネクタ、はんだ用途では、接触抵抗、はんだ付け性、熱履歴後信頼性を外観と切り離して管理する。HDI / microvia は一般的な厚付け発想をそのまま持ち込まず、界面品質と後工程条件を別管理にするのが安全です。JCU IPC	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	jcu-i.com | ipc.org	2	1	vendor_first_party | standards_body	0.85	ok		2	1				microvia reliability				
claim-084	### 5.2 判断を誤らないための運用ルール	scope	high	規制判断は「製品」「工場」「作業者」「顧客要求」の4レイヤーに分けて記載する。RoHS / REACH / 排水 / 労安 / ニッケル放出を一つの表現でまとめると、適用範囲を誤りやすくなります。EUR-Lex RoHS ECHA Annex XVII OSHA 環境省 排水基準	inline citation context	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://env.go.jp/water/impure/haisui.html	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459 | https://osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026 | https://env.go.jp/water/impure/haisui.html	eur-lex.europa.eu | echa.europa.eu | osha.gov | env.go.jp	4	4	legal_text | official_regulator	0.80	out_of_scope		0	0			EU	nickel	skin-contact release condition			
claim-085	### 5.2 判断を誤らないための運用ルール	advice	high	調達や外注比較では、浴管理、排水 / 排気、分析、再処理、停止時間まで含めた運用能力を同じ表で比べる。薬品単価や設備価格だけで優劣を付けると、立上げ後の総コストを読み違えます。US EPA 排水 厚生労働省 JCU	inline citation context	https://epa.gov/eg/electroplating-effluent-guidelines | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	https://epa.gov/eg/electroplating-effluent-guidelines | https://mhlw.go.jp/stf/seisakunitsuite/bunya/0000099121_00005.html | https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf	epa.gov | mhlw.go.jp | jcu-i.com	3	2	official_regulator | vendor_first_party	0.95	ok		2	1			Japan	wastewater discharge				
claim-086	### 5.3 このレポートで残る不確実性	scope	high	本レポートは実務向け概説の focused-budget pass であり、full dr_ultra-equivalent run ではありません。個別の JIS / ASTM / IPC 要求膜厚や合否判定、個社固有の工程窓までは踏み込んでいないため、製品設計や受入規格の議論では対象規格を別途特定する必要があります。					0	0		0.80	out_of_scope		0	0								
claim-087	### 5.3 このレポートで残る不確実性	scope	high	EU の六価クロム規制運用は、認可継続と制限強化の移行途上で動きやすい領域です。2026年4月19日時点の整理としては、RoHS は有効、REACH ニッケル制限も有効ですが、Cr(VI) の将来運用は継続監視が必要です。EUR-Lex RoHS ECHA Annex XVII	inline citation context	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	https://eur-lex.europa.eu/legal-content/EN/TXT?uri=CELEX%3A02011L0065-20250101 | https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459	eur-lex.europa.eu | echa.europa.eu	2	2	legal_text	0.80	out_of_scope		0	0		2026-04-19	EU	hexavalent chromium				
claim-088	### 5.3 このレポートで残る不確実性	scope	high	日本の排水実務は、全国一律基準だけでなく、自治体上乗せ、下水道受入条件、顧客監査要求で厳しくなることがあります。工場立地単位の再確認が必要です。環境省 排水基準 大阪府	inline citation context	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	https://env.go.jp/water/impure/haisui.html | https://pref.osaka.lg.jp/o120080/jigyoshoshido/mizu/r6-4kaisei.html	env.go.jp | pref.osaka.lg.jp	2	2	official_regulator | legal_text	0.80	out_of_scope		0	0			Japan	wastewater discharge	sewer discharge			local add-on rules may apply
claim-089	### 5.3 このレポートで残る不確実性	scope	high	半導体・先端パッケージ用途では、めっき条件そのものより界面品質や後工程適合性が支配的になるため、サプライヤー資料と顧客評価条件を合わせて読む必要があります。JCU IPC	inline citation context	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	https://jcu-i.com/wp/wp-content/uploads/2022/10/irks1_20220511.pdf | https://ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high	jcu-i.com | ipc.org	2	1	vendor_first_party | standards_body	0.80	out_of_scope		0	0
````

---

## FILE: metrics.json

````json
{
  "run_id": "20260419-101901-research",
  "topic": "めっき",
  "mode": "gpt-like",
  "preset": "dr_ultra",
  "as_of_date": "2026-04-19",
  "updated_at": "2026-04-19 21:56:42",
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
    "bundle_label": "一般トピック概要",
    "family_id": "independent_context",
    "surface_label": "must-find concepts",
    "classification_source": "manual_override",
    "minimum_surface_floor": 0,
    "minimum_entity_floor": 0,
    "minimum_tail_query_floor": 0,
    "signals": [
      "manual_override:technology_overview"
    ],
    "summary": "off / optional / kind technology / bundle 一般トピック概要; score 0; surface_floor=0, tail_queries=0"
  },
  "logic": {
    "milestone": "M4",
    "requires_claim_ledger": true,
    "required_report_sections": [
      "## 1. 要約",
      "## 2. 主要な発見",
      "## 3. 根拠テーブル",
      "## 4. 詳細分析",
      "## 5. 実務で確認すべきことと追加調査",
      "## 6. 主要ソース一覧",
      "### 4.1 比較マトリクス",
      "### 4.2 主要な差分と含意",
      "### 4.3 役割差または類型",
      "### 4.4 上流/下流または主体ネットワーク",
      "### 4.5 反証・例外・境界条件",
      "### 4.6 時系列・変化点",
      "### 4.7 ドメインリスクマップ"
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
    "executed_queries": 26,
    "raw_hits": 26,
    "unique_urls": 26,
    "deep_read_selected": 18,
    "opened_sources": 14,
    "unique_cited_sources": 25,
    "citation_instances": 175,
    "primary_cited_sources": 19
  },
  "ratios": {
    "query_budget_utilization": 1.0833,
    "raw_hit_budget_utilization": 0.325,
    "open_budget_utilization": 0.4667,
    "deep_read_budget_utilization": 1.2857,
    "unique_cited_source_target_utilization": 1.7857,
    "citation_instance_target_utilization": 4.8611,
    "primary_source_ratio": 0.76,
    "official_regulator_ratio": 0.4114,
    "standards_or_academic_ratio": 0.1486,
    "vendor_dependency_ratio": 0.2114,
    "industry_association_dependency_ratio": 0.12
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
      "total_claims": 89,
      "fact_claims": 30,
      "inference_claims": 0,
      "open_question_claims": 0,
      "advice_claims": 30,
      "regulatory_claims": 7,
      "numeric_claims": 0,
      "temporal_claims": 4,
      "scope_claims": 18,
      "out_of_scope_claims": 18,
      "passing_claims": 71,
      "weak_claims": 0,
      "missing_claims": 0,
      "auditable_claims": 71
    },
    "ratios": {
      "passing_ratio": 1.0
    },
    "regulatory_numeric_temporal_gaps": []
  },
  "claim_coverage": {
    "extracted_report_claims_count": 89,
    "ledger_claims_count": 89,
    "high_risk_report_claims_count": 64,
    "high_risk_claims_in_ledger_count": 64,
    "claim_coverage_ratio": 1.0,
    "high_risk_claim_coverage_ratio": 1.0,
    "missing_claims_from_ledger": [],
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
    "search_duration_seconds": 505,
    "search_duration_human": "8m 25s",
    "total_elapsed_seconds": 9349,
    "total_elapsed_human": "2h 35m 49s",
    "phase_durations_seconds": {
      "planning": 380,
      "searching": 505,
      "writing": 8464
    }
  },
  "coverage": {
    "run_id": "20260419-101901-research",
    "preset": "dr_ultra",
    "logic_milestone": "M4",
    "entity_scope": {
      "required": false,
      "mode": "off",
      "score": 0,
      "kind": "technology",
      "kind_score": 0,
      "bundle_id": "general-overview",
      "bundle_label": "一般トピック概要",
      "family_id": "independent_context",
      "family_id_matches_kind": true,
      "summary": "off / optional / kind technology / bundle 一般トピック概要; score 0; surface_floor=0, tail_queries=0"
    },
    "required_query_families": [
      {
        "family_id": "official_primary",
        "label": "一次・公式",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "Direct official citations from `env.go.jp`, `osha.gov`, `eur-lex.europa.eu`, and `echa.europa.eu`.",
        "waiver_reason": "-",
        "matched_query_count": 2,
        "minimum_query_matches_required": 1,
        "sample_queries": [
          "RoHS hexavalent chromium official",
          "REACH nickel official"
        ],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "query_matches",
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "regulation_standards",
        "label": "規制・標準",
        "plan_status": "covered",
        "requested_coverage_status": "covered",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "Wastewater, OSHA, RoHS, and REACH claims are grounded in regulator or legal-text sources.",
        "waiver_reason": "-",
        "matched_query_count": 3,
        "minimum_query_matches_required": 1,
        "sample_queries": [
          "ニッケル化合物 労働安全 厚労省",
          "化学物質 自律的管理 厚労省",
          "CrVI OSHA standard"
        ],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "query_matches",
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "research_validation",
        "label": "研究・検証",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "`jcu-i.com`, `orist.jp`, and `ipc.org` cover reliability and technical caveats even though this focused pass did not preserve many explicit family-tagged search strings.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "vendor_implementation",
        "label": "ベンダー実装",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "Fuji Electric, ULVAC, and JCU were cited for implementation details, process framing, and application examples.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "independent_context",
        "label": "独立コンテキスト",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "SFJ, Zentoren, Kizaikou, and ORIST provide non-vendor context and comparison framing.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "japan_specific",
        "label": "日本語・国内",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "The report depends on Japan-facing sources such as `env.go.jp`, Osaka prefecture, SFJ, Zentoren, and related organizations.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "contradiction_negative",
        "label": "反証・不在確認",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "`notes/contradiction-log.md` and report section `4.5` explicitly capture over-generalization risks and boundary cases.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "upstream_downstream",
        "label": "上流/下流",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "`notes/upstream-downstream-map.md` and report section `4.4` cover pretreatment, plating, post-treatment, wastewater/air treatment, and customer quality handoff.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "role_structure",
        "label": "役割差・類型",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "`notes/role-structure-matrix.md` and report section `4.3` split method roles by application and failure mode.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      },
      {
        "family_id": "chronology_change",
        "label": "時系列・変化点",
        "plan_status": "covered_by_mapping",
        "requested_coverage_status": "covered_by_mapping",
        "coverage_status": "covered_by_mapping",
        "coverage_evidence": "Report section `4.6` and the cited `2024-02-05` / `2024-04-01` changes provide the chronology layer.",
        "waiver_reason": "-",
        "matched_query_count": 0,
        "minimum_query_matches_required": 1,
        "sample_queries": [],
        "has_explicit_coverage_evidence": true,
        "is_waived": false,
        "coverage_basis": [
          "coverage_evidence"
        ],
        "covered": true
      }
    ],
    "required_report_sections": [
      {
        "section": "## 1. 要約",
        "matched_heading": "## 1. まず押さえる結論",
        "present": true
      },
      {
        "section": "## 2. 主要な発見",
        "matched_heading": "## 2. 読み手が先に知るべき要点",
        "present": true
      },
      {
        "section": "## 3. 根拠テーブル",
        "matched_heading": "## 3. 判断に使う主要根拠",
        "present": true
      },
      {
        "section": "## 4. 詳細分析",
        "matched_heading": "## 4. 方式選定で迷いやすい論点",
        "present": true
      },
      {
        "section": "## 5. 実務で確認すべきことと追加調査",
        "matched_heading": "## 5. 導入前に確認すべきこと",
        "present": true
      },
      {
        "section": "## 6. 主要ソース一覧",
        "matched_heading": "## 6. 参照した主要ソース",
        "present": true
      },
      {
        "section": "### 4.1 比較マトリクス",
        "matched_heading": "### 4.1 方式比較の見取り図",
        "present": true
      },
      {
        "section": "### 4.2 主要な差分と含意",
        "matched_heading": "### 4.2 何が選定を分けるか",
        "present": true
      },
      {
        "section": "### 4.3 役割差または類型",
        "matched_heading": "### 4.3 用途別に見た方式の役割",
        "present": true
      },
      {
        "section": "### 4.4 上流/下流または主体ネットワーク",
        "matched_heading": "### 4.4 工程全体と関係者のつながり",
        "present": true
      },
      {
        "section": "### 4.5 反証・例外・境界条件",
        "matched_heading": "### 4.5 例外条件と誤解しやすい境界",
        "present": true
      },
      {
        "section": "### 4.6 時系列・変化点",
        "matched_heading": "### 4.6 直近の制度変更と日付",
        "present": true
      },
      {
        "section": "### 4.7 ドメインリスクマップ",
        "matched_heading": "### 4.7 見落としやすい実務リスク",
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
      "1. まず押さえる結論",
      "2. 読み手が先に知るべき要点",
      "0. Research Metadata",
      "3. 判断に使う主要根拠",
      "4. 方式選定で迷いやすい論点",
      "4.1 方式比較の見取り図",
      "4.2 何が選定を分けるか",
      "4.3 用途別に見た方式の役割",
      "4.4 工程全体と関係者のつながり",
      "4.5 例外条件と誤解しやすい境界",
      "4.6 直近の制度変更と日付",
      "4.7 見落としやすい実務リスク",
      "5. 導入前に確認すべきこと",
      "5.1 選定前の実務チェックリスト",
      "5.2 判断を誤らないための運用ルール",
      "5.3 このレポートで残る不確実性",
      "6. 参照した主要ソース"
    ]
  },
  "citation_integrity": {
    "report_citation_count": 25,
    "citation_ledger_count": 25,
    "missing_report_citations": []
  },
  "release_gate": {
    "strict": true,
    "finalization_requested": true,
    "status": "complete",
    "blocking_reasons": [],
    "revision_reasons": [],
    "unresolved_gaps": [],
    "next_required_actions": []
  }
}
````

---

## FILE: brief.md

````md
# Research Brief

- Run ID: 20260419-101901-research
- Topic: めっき
- Output language: Japanese
- Research mode: gpt-like
- Research preset: dr_ultra logic scaffold (focused-budget override; not a full dr_ultra-equivalent run)
- As-of date: 2026-04-19
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.
- Candidate collection target: focused-budget pass (raw-hit budget 80; practical floor 20 surviving candidates)
- Deep-read target: 14
- Topic breadth class: standard (manual override / focused overview)
- Topic breadth score: 50
- Topic budget scale: 0.45
- Topic stop profile: standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800
- Entity discovery mode: off
- Discovery kind: technology (`manual_override`, score 0)
- Discovery bundle: general overview
- Entity discovery profile: off / optional / kind technology / bundle general overview; score 0; surface_floor=0, tail_queries=0
- Generated at: 2026-04-19 10:19:01
- Run posture: document-first focused-budget overview; this run uses dr_ultra logic as a checklist scaffold only

## Core question

- めっきとは何かを、方式・用途・品質・環境安全の観点から、日本語で再利用しやすい概説レポートとして整理する。
- 読者が「どのめっき方式を、どんな目的で、どんな注意点と規制制約の下で採用するか」を短時間で把握できる状態を作る。

## User constraints

- 今回は再現性検証を兼ねるため、前回分や途中成果物は参照しない。
- fresh run の内部成果物だけを使って、ゼロから調査・執筆する。
- サブエージェントを使って並列調査する。
- この run は日本向け概説に絞った focused-budget pass であり、通常の dr_ultra 相当の探索量や tail sweep は実施していない。

## Must-cover angles

- めっきの定義と表面処理全体の中での位置づけ
- 主な方式: 電気めっき、無電解めっき、溶融めっき、真空めっき/乾式表面処理との境界
- 主な皮膜金属と代表機能: 防食、装飾、導電、はんだ付け性、耐摩耗、磁性など
- 主な用途: 自動車、電子部品、プリント基板、半導体周辺、建材、装飾
- 工程管理・品質指標: 密着性、膜厚、均一性、外観、耐食性、不具合
- 環境・安全・規制: 排水処理、六価クロム、ニッケル、RoHS/REACH、労働安全
- 日本の読者向けの産業・制度上の補足

## Reader decisions to support

- 概要説明資料として何を最低限押さえるべきか
- 湿式めっきと乾式表面処理をどう言い分けるべきか
- 防食・装飾・電子用途で方式選定時に何を比較すべきか
- レポート内で断定を避けるべき規制・健康影響の論点は何か

## Must-not-miss risks

- 「めっき」を電気めっきだけに狭く定義してしまうリスク
- 真空蒸着やスパッタを広義のめっきと呼ぶ文脈と、狭義では含めない文脈の混同
- 六価クロム規制やニッケル規制を、用途横断で一律に断定してしまうリスク
- 企業 marketing の主張を、一般論としてそのまま採用するリスク
- 日本の排水基準や暫定基準の時点依存性を落とすリスク

## Assumptions

- 対象読者は、材料・製造・品質・調達の初中級実務者を想定する。
- 学術レビューではなく、実務に使える概説レポートを目指す。
- 法令助言そのものではなく、規制論点の整理を行う。

## Preferred domains

- env.go.jp
- mhlw.go.jp
- epa.gov
- echa.europa.eu
- eur-lex.europa.eu
- sfj.or.jp
- mekki.sfj.or.jp
- zentoren.or.jp
- aen-mekki.or.jp
- kizaikou.or.jp
- asminternational.org

## Excluded angles

- 個別企業の売上ランキングや市場規模推計の深掘り
- 特定企業の途中資料、過去 run、既存レポートの再利用
- 量子・ナノ材料など周辺テーマへの逸脱

## Checklist ideas

- 用途に対して必要機能を先に定義したか
- 方式ごとの膜厚・均一性・密着性・量産性の違いを確認したか
- 皮膜金属と後処理の組み合わせを確認したか
- 六価クロム、ニッケル、排水、RoHS/REACH のどれが関係するか切り分けたか
- 製品接触条件と職業ばく露条件を混同していないか

## Tail sweep

- Entity discovery is off for this pass; do not reopen roster-building unless a later pass explicitly broadens scope.
- If a later pass re-enables discovery, switch to a technology/general-overview bundle rather than a company roster.

## Stop rule

Stop after the core decision layer is evidenced and newly surfaced sources add little novelty. This focused-budget pass should not chase full dr_ultra-equivalent tail coverage once the practical overview is stable.
````

---

## FILE: query-plan.md

````md
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
````

---

## FILE: run-config.toml

````toml
run_id = "20260419-101901-research"
topic = "めっき"
mode = "gpt-like"
preset = "dr_ultra"
output_language = "Japanese"
as_of_date = "2026-04-19"
generated_at = "2026-04-19 10:19:01"

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
bundle_label = "一般トピック概要"
family_id = "independent_context"
surface_label = "must-find concepts"
classification_source = "manual_override"
minimum_surface_floor = 0
minimum_entity_floor = 0
minimum_tail_query_floor = 0
signals = ["manual_override:technology_overview"]
summary = "off / optional / kind technology / bundle 一般トピック概要; score 0; surface_floor=0, tail_queries=0"

[coverage]
logic_milestone = "M4"
required_query_families = ["official_primary", "regulation_standards", "research_validation", "vendor_implementation", "independent_context", "japan_specific", "contradiction_negative", "upstream_downstream", "role_structure", "chronology_change"]
required_report_sections = ["## 1. 要約", "## 2. 主要な発見", "## 3. 根拠テーブル", "## 4. 詳細分析", "## 5. 実務で確認すべきことと追加調査", "## 6. 主要ソース一覧", "### 4.1 比較マトリクス", "### 4.2 主要な差分と含意", "### 4.3 役割差または類型", "### 4.4 上流/下流または主体ネットワーク", "### 4.5 反証・例外・境界条件", "### 4.6 時系列・変化点", "### 4.7 ドメインリスクマップ"]

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
````

---

## FILE: notes\topic-profile.md

````md
# Topic Stop Profile

- Run ID: 20260419-101901-research
- Topic: めっき
- Preset: dr_ultra logic scaffold
- Topic scope: standard (manual_override, breadth score 50)
- Budget scale: 0.45
- Preset baseline budget: candidates 1040, deep reads 84, queries 88, raw hits 1040, opens 280, deep-read budget 84, cited sources 52, citations 170
- Effective run budget: candidates 20, deep reads 10, queries 24, raw hits 80, opens 30, deep-read budget 14, cited sources 14, citations 36
- Override reason: Manual budget overrides reduced the preset baseline for: candidate_target, deep_read_target, query_budget, raw_hit_budget, open_budget, deep_read_budget, unique_cited_source_target, citation_instance_target.
- Override authority: user
- Full DR equivalent: no (scoped or lighter-than-full DR)
- Report status implication: A complete status only means the scoped override is satisfied; keep the report labeled as non-full-DR-equivalent.

## Stop posture

standard / focused overview override / floors q=12, candidates=20, deep=10; stop novelty=0.0400, same-domain=0.1800

## Signals

- The topic is broad in vocabulary but this run is intentionally narrowed to a practical overview report.
- The user explicitly requested a fresh run with no prior-run reuse.
- The required deliverable is a Japanese narrative report, not a market-sizing dossier.
- This run uses dr_ultra logic as a checklist scaffold, but it is not intended to be dr_ultra-equivalent in search breadth, tail sweep, or deep-read volume.

## Effective controls

- Query budget: 24
- Raw hit budget: 80
- Open budget: 30
- Deep-read budget: 14
- Novelty stop threshold: 0.04
- Max same-domain ratio: 0.18

## Use

- This focused-budget run should stop once the core decision layer is evidenced; it should not try to chase full dr_ultra tail coverage.
- If weak claims appear, switch to gap-closing before widening the search again.
- Treat missing long-tail entity coverage as acceptable in this pass unless it blocks the practical overview.

## Run-specific interpretation

- Treat "めっき" as a practical surface-engineering overview topic.
- Cover four method families: electroplating, electroless plating, hot-dip plating, and dry/vacuum surface treatment as a boundary concept.
- Prioritize Japan-facing regulatory and manufacturing context over global market statistics.
- Keep entity discovery off unless a later pass explicitly expands scope.
- Consider the run complete when method definitions, major applications, plating-specific failure modes, and environmental/safety constraints are all evidenced with current sources.
````

---

## FILE: notes\contradiction-log.md

````md
# Contradiction Log

## Confirmed Contradictions

- "めっき" is used narrowly for wet metal deposition in many technical contexts, but some industrial pages also use it broadly to include vacuum deposition, sputtering, thermal spraying, and solder coating.
- Decorative and functional chromium plating are often discussed together in basic introductions, but environmental and compliance burdens differ materially once hexavalent chromium, emissions, and substitution pressure are considered.
- Surface appearance defects do not always equal functional failure; for corrosion protection and some galvanized products, appearance acceptance can differ from durability acceptance.

## Negative Evidence

- No single cross-industry source provided one stable, globally shared definition that cleanly resolves the narrow-vs-broad meaning of "めっき."
- Product regulation and workplace regulation did not collapse into one rule set; the relevant constraint depends on whether the issue is product composition, skin contact, wastewater, or worker exposure.
- No single source covered all major application sectors with the same granularity; electronics required separate sources from general corrosion-protection uses.

## Interpretation

- In the report body, use "狭義のめっき" for wet deposition and explicitly label dry/vacuum methods as adjacent or broad-sense usage.
- Avoid blanket statements such as "chromium plating is prohibited" or "nickel plating is restricted" without specifying product class, geography, and exposure path.
- Separate cosmetic defects, functional defects, and regulatory non-compliance into different risk layers.
````

---

## FILE: notes\upstream-downstream-map.md

````md
# Upstream and Downstream Map

## Upstream

- Surface-treatment chemicals: metal salts, complexing agents, reducing agents, additives, cleaners, acids, alkalis.
- Equipment and line engineering: tanks, rectifiers, filtration, agitation, rinsing, dryers, exhaust, wastewater treatment.
- Pretreatment and substrate preparation: degreasing, etching, activation, undercoats, masking, jigs.
- Standards and test methods: corrosion tests, thickness tests, adhesion checks, electronics reliability tests.

## Downstream

- Job platers and captive plating lines.
- Automotive exterior and hardware parts.
- Printed circuit boards, connectors, lead frames, semiconductor package substrates, and wafer-adjacent components.
- Building hardware and steel structures requiring corrosion protection.
- Decorative goods, water fixtures, and consumer products with skin-contact considerations.

## Adjacent Process Notes

- Wastewater treatment and air-emission control are not side topics; they are process-enabling functions.
- Inspection and reliability testing sit downstream of plating but feed back into bath control and design rules.
- Chemical suppliers and equipment suppliers strongly shape what "standard" process windows look like for each end market.
````

---

## FILE: notes\role-structure-matrix.md

````md
# Role Structure Matrix

## Compared Entities

- Electroplating
- Electroless plating
- Hot-dip galvanizing / molten-metal plating
- Dry/vacuum surface treatment used under broad-sense "plating" language

## Matrix Notes

- Electroplating is strongest when cost, throughput, and selectable metal species matter, but it is shape-sensitive because current density affects thickness distribution.
- Electroless plating is strongest when uniformity on complex geometry or nonconductive substrates matters, but bath control and chemical cost are heavier.
- Hot-dip galvanizing is optimized for robust corrosion protection of steel structures rather than fine local functional tuning.
- Dry/vacuum methods matter when the reader encounters "vacuum plating" language; they are best treated as adjacent surface-engineering processes rather than default members of narrow-sense plating.

## Positioning Summary

- For corrosion-protection infrastructure, hot-dip zinc sits in a different decision space from precision electronic plating.
- For PCB and semiconductor-adjacent use, copper and electroless seed processes are tied to wiring formation and reliability rather than decoration.
- For decorative and plastics applications, plating chemistry is only one layer of the system; substrate preparation, adhesion, and product regulations can dominate the outcome.
````

---

## FILE: notes\domain-risk-map.md

````md
# Domain Risk Map

## Expert-Must-Cover Risks

- Misclassifying broad-sense surface treatment as narrow-sense wet plating and then carrying the wrong process, equipment, or compliance assumptions into a comparison.
- Missing hydrogen embrittlement risk on high-strength steels, springs, and stressed parts, or forgetting to confirm whether post-plate baking is required by drawing/specification.
- Treating pretreatment as a commodity step even though pretreatment failure often sits behind adhesion failure, pits, blisters, peel-off, and latent reliability escapes.
- Assuming nominal thickness alone is enough; thickness nonuniformity, pores, edge build-up, and bath-control drift can dominate corrosion life and electrical performance.
- Using electronics examples without separating contact resistance, solderability, and microvia reliability caveats.

## Common Reader Misunderstandings

- "More thickness is always better."
- "A shiny appearance means a good plated film."
- "If outgoing inspection passed, plating reliability is settled."
- "Nickel restrictions mean nickel plating is broadly banned."
- "RoHS, REACH, wastewater, air, and worker-exposure rules all regulate the same layer."

## Operational Failure, Compliance, Or Loss Scenarios

- Poor pretreatment or activation leads to adhesion failure, blistering, pits, peel-off, or hidden field failures.
- Weak bath control causes thickness nonuniformity, roughness drift, rework, scrap, and unstable contact resistance.
- Electronics or connector finishes can pass appearance checks and still fail after storage, reflow, thermal cycling, or wear because solderability/contact resistance were not validated.
- High-strength steel parts can carry delayed-failure risk if hydrogen embrittlement controls and baking windows are not explicitly managed.
- HDI / microvia use cases need a specific caveat: panel-level plating intuition does not safely generalize to microvia interfaces.
- Inadequate wastewater, exhaust, or worker-protection controls create compliance, cost, and business-continuity risk.

## Boundary Conditions And Adjacent Concepts

- Vacuum deposition, sputtering, and thermal spraying are adjacent and sometimes marketed as plating, but should be separated analytically unless the scope is explicitly broad.
- Hot-dip galvanizing is plating in the broad family sense, but its decision logic differs from precision functional wet plating.
- Nickel release for skin-contact products is not the same question as nickel content inside an internal industrial part.
- Connector / PCB logic does not automatically carry over to decorative or structural steel use cases.

## Stale-Information Risks

- Hexavalent chromium and PFAS-related regulatory activity is actively changing.
- Temporary wastewater standards, local sewer acceptance rules, and permit conditions create date- and site-sensitive statements.
- Product restrictions, nickel-release interpretations, and test methods can change with directive, annex, or standard revisions.
- Company process windows, chemistry recipes, and line capability claims go stale faster than high-level process definitions.

## Latest-Check Items

- Japan hexavalent chromium wastewater numbers and temporary treatment for electroplating facilities.
- Site-specific wastewater / sewer acceptance and air-exhaust obligations.
- Whether the target product falls under RoHS, REACH nickel release, or neither.
- Whether hydrogen embrittlement relief baking is specified for the part class.
- Contact-resistance, solderability, and microvia-reliability requirements for electronics use cases.
- EPA status of chrome-finishing / PFAS-related electroplating rulemaking.

## Report-Mandatory Risk Points

- Separate definition risk, quality risk, compliance risk, and operations risk.
- Name hydrogen embrittlement, pretreatment failure, thickness nonuniformity, adhesion failure, pits/blisters, bath control, contact resistance, solderability, and microvia caveats explicitly where relevant.
- Use dates whenever mentioning current regulatory thresholds or rulemaking posture.
- Make the reader state which layer is under discussion: product, plant, worker, or customer qualification.
````

---

## FILE: notes\evidence-gap-followup.md

````md
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
````

---
