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
