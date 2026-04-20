# めっきの用途・産業・実務判断メモ

新規のWeb調査だけを使って、めっきの使いどころを「用途」「方式」「実務判断」で整理したメモです。一次情報・業界団体・公的資料・標準系を優先し、vendor 資料は使っていません。

## 1. まず押さえる前提

めっきは、単なる防錆ではなく、耐食・耐摩耗・導電・はんだ付け性・接触信頼性・意匠性を個別に設計する表面機能です。METI の用途分類では、湿式めっきは電気めっきと無電解めっき、溶融めっきは溶融金属への浸漬で皮膜を作る方法として整理されています。EPA も electroplating を、耐食、耐摩耗、抗摩擦、装飾などのための表面被覆として説明しています。  
出典: [METI](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf), [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines)

外注先や工程設計を考えるときは、電気めっきだけを見て終わらせず、前処理・洗浄・乾燥・排水処理・排ガス・後工程までを一連で見る必要があります。EPA は job plater と captive operation の両方を規制対象に含め、OSHA は装飾クロムめっきや六価クロム曝露の注意点を示しています。  
出典: [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines), [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 2. 用途別の見方

### 自動車

自動車では、めっきは「腐食しないこと」だけでは足りず、成形性、溶接性、部位ごとの耐食、量産安定性まで含めて選びます。日本鉄鋼連盟は、亜鉛めっき鋼板の用途を自動車・輸送機器、建築・土木、電気機器などに整理しており、自動車向けでは薄板・めっきに必要な機械的性質、寸法、形状、取引情報に加えて、めっき付着量や化成処理も規定する JFS の考え方を示しています。トヨタの資料では、亜鉛めっき鋼板のアーク溶接でブローホールが課題になり、MAG 条件の調整で全車種展開に結びつけた経緯が示されています。  
出典: [日本鉄鋼連盟](https://www.jisf.or.jp/business/tech/aen/index.html), [JFS](https://www.jisf.or.jp/business/standard/jfs/), [トヨタ](https://www.toyota.co.jp/jpn/company/history/75years/data/automotive_business/production/production_engineering/major_components/unit-field_stamping/engineering.html)

実務上は、ボディ外板と骨格部材で要求が違います。外板は外観・耐チッピング・耐白さび・塗装との相性、骨格や補強材は溶接適性と局所腐食が重要です。クロメートフリー化が進んでも、厳しい条件ではクロメート処理が残るという JISF の整理は、「環境優先で全部同じ」にできないことを示しています。  
出典: [日本鉄鋼連盟](https://www.jisf.or.jp/news/topics/070130.html), [日本鉄鋼連盟](https://www.jisf.or.jp/knowledge/variety/hyo.html)

### 電子部品

電子部品は、自動車以上に「接触の安定」「はんだ付け」「保存安定性」「複数回リフロー耐性」が効きます。JEITA は電子部品を、コネクタ、実装部品、センサーなどの相互接続部材として整理しており、車載・通信・医療など高信頼性市場向けで信頼性評価の重要性を強調しています。  
出典: [JEITA 電子部品部会](https://home.jeita.or.jp/ecb/about/part.html), [JEITA 信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)

PCB の表面仕上げは、HASL、OSP、ENIG、電解 Ni/Au、浸漬 Ag、浸漬 Sn などが代表です。IPC の比較資料では、OSP/ENIG/IAg が広く使われ、lead-free HASL は平坦性の再現が難しく、電解 Ni/Au は高コストとされています。ENIG 標準は、はんだ付けだけでなく、アルミワイヤボンド、press fit、接点用途まで含む多機能仕上げとして定義されています。  
出典: [IPC 比較資料](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf), [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)

PCB の品質判断は、見た目だけでは足りません。IPC-A-600 は、基材表面・内部状態、導体幅/間隔、annular ring、PTH の銅厚、ボイド、クラックまで受入基準に含めています。IPC-6012F は rigid board の qualification/performance の基準で、automotive addendum の基礎にもなっています。  
出典: [IPC-A-600](https://www.electronics.org/ipc-600-acceptability-printed-boards-endorsement-program), [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)

### 半導体周辺

半導体周辺では、めっきは「チップそのもの」よりも、パッケージ基板、リードフレーム、接続端子、バンプ、ワイヤボンド部で効いてきます。JEITA/ITRS のパッケージング資料では、フリップチップには OSP、無電解 Sn、ENIG が候補で、ワイヤボンドには電解 Ni/Au が候補として挙げられ、ENEPIG が両立案として有望とされています。つまり、万能な一種類ではなく、接合方式ごとに表面仕上げを使い分ける前提です。  
出典: [JEITA/ITRS 2007](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf)

さらに JEITA のアセンブリ＆パッケージング資料では、WLP と SiP が低コスト・高機能の解に位置づけられ、デバイスの複雑化はより高いコストのパッケージングで解く必要があると整理されています。半導体周辺では、めっき単価よりも、歩留まり・再加工性・検査設計の方が総コストを左右しやすいと読めます。  
出典: [JEITA/ITRS 2005](https://semicon.jeita.or.jp/STRJ/ITRS/2005/12_2005A%26P.pdf)

### 建材

建材では、耐食の長さとメンテナンス性が主役です。日本鉄鋼連盟の手引きでは、塗装亜鉛系めっき鋼板は亜鉛の犠牲防食と塗膜の保護で耐久性を高め、屋根・外壁・ウォールパネル・リフォームなどに使われると整理されています。塗装工程は現場塗装よりも、性能面・経済性・環境面で有利という位置づけです。  
出典: [塗装亜鉛系めっき鋼板の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)

また、屋外での耐久性は、材料そのものだけでなく保管・搬送・施工後養生の影響を強く受けます。高温多湿での保管、雨がかりの少ない部位、切り口処理、野積み時の浸水は、白さびやブリスターの引き金になります。建材は「めっき仕様」だけ見ても足りず、施工条件込みで設計するのが実務です。  
出典: [塗装亜鉛系めっき鋼板の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)

### 装飾

装飾用途では、めっきは見た目と耐変色性が前面に出ます。OSHA は、decorative/bright plating を、ニッケルなどの上に薄いクロムを析出させて、外観と耐変色性を得る用途と説明し、例としてホイール、家電、配管金具を挙げています。EPA も electroplating の用途に decorative purposes を含めています。  
出典: [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf), [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines)

装飾用途の判断では、厚い防食層よりも、光沢、色調、指紋汚れ、擦り傷、下地ニッケルとの相性が重要です。したがって、同じクロム系でも、自動車の機能部品とは評価軸がかなり違います。  
出典: [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 3. 方式の選び分け

めっき方式は、ざっくり次の軸で分けると判断しやすいです。  
出典: [METI](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf)

- 電気めっきは、導電性がある母材に電流を流して析出させるので、厚み管理と生産性を取りやすい一方、形状の電流集中に注意が要ります。
- 無電解めっきは、形状の回り込みが効きやすく、均一皮膜や非導電材料への適用で有利です。
- 溶融めっきは、大きな鋼材の耐食保護に強く、建材や鋼板での選択肢になります。
- ENIG/ENEPIG は、PCB・半導体周辺の接合互換性と保存安定性をまとめて取りにいく方式です。

選定のコツは、「何を守るか」を先に決めることです。耐食なら亜鉛系や塗装複合、導電接点なら Ni/Au 系、はんだ付け主導なら OSP/ENIG/浸漬 Sn/Ag、装飾なら bright chrome 系、という順で候補が自然に絞れます。  
出典: [IPC 比較資料](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf), [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf), [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 4. 工程・設備・外注先を見るポイント

外注先評価では、めっき槽そのものより、前処理、治具、洗浄、乾燥、分析、排水、排ガス、保全を一体で見るのが重要です。METI の PRTR 手引きは、めっき工程を代表的工程の一つとして扱い、工程ごとに原材料・添加剤・排出の考え方を分けています。EPA は、independent job platers と captive operations の両方を含めて規制しているので、外注型か内製型かよりも、工程管理の実力を見る方が本質です。  
出典: [METI PRTR 手引き](https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r5_haishutsu_sanshutsu_manual/3-1.pdf), [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines)

現場で確認したいのは、浴組成の管理記録、析出厚みの測定法、欠陥の見つけ方、ライン停止時の復旧手順、そしてクロスコンタミ防止です。IPC-4552 は ENIG に対して、ニッケル厚 3-6 µm、金厚 0.05 µm 以上、均一なめっき、接合性、清浄性、化学耐性、品質保証を要求しています。  
出典: [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)

設備観点では、排水処理と排ガス対策を「付帯設備」ではなく主設備の一部として扱うべきです。EPA はクロム工程や金属排出の規制を明示し、OSHA は六価クロム曝露を重要な安全論点として扱っています。つまり、めっきの量産能力は、浴の能力だけでなく公害・安全設備の処理能力で頭打ちになります。  
出典: [EPA](https://www.epa.gov/eg/electroplating-effluent-guidelines), [OSHA](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)

## 5. 品質・コスト・歩留まりの見方

品質は、外観よりも「使う条件で壊れないか」で見る方が失敗しにくいです。PCB なら平坦性、はんだ濡れ、PTH の銅厚、ボイド、クラック、保存後の再流し回数、接点抵抗を見ます。PCB の表面仕上げ比較では、各 finish に長所短所があり、複数回リフローや保存シミュレーションで差が出ると整理されています。  
出典: [IPC 比較資料](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf), [IPC-A-600](https://www.electronics.org/ipc-600-acceptability-printed-boards-endorsement-program)

半導体周辺では、めっきの歩留まりは単体の外観不良より、ワイヤボンド不良、フリップチップ接合不良、界面汚染、熱応力による剥離で失われやすいです。JEITA/ITRS は、組立と基板製造プロセスの最適化が量産の前提だと述べ、ENEPIG を含む複合表面仕上げの必要性を示しています。  
出典: [JEITA/ITRS 2007](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf)

建材と自動車では、初期コストだけでなく、再塗装・再処理・施工手戻りまで含めた総コストで見ます。塗装亜鉛系めっき鋼板の手引きは、保管・施工・切り口・雨がかり条件で劣化が進むと明記しており、材料単価が安くても現場損失が大きいと逆転しやすいことを示しています。  
出典: [塗装亜鉛系めっき鋼板の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)

## 6. 実務チェックリスト

- 何を一番守るかを一つに絞ったか。耐食、導通、はんだ、外観、摺動のうち、最優先を曖昧にしない。  
- 母材、形状、接合方式、使用環境を先に決めたか。自動車、PCB、半導体周辺、建材、装飾で要求は別物。  
- 方式を電気めっき、無電解、溶融、複合仕上げのどれにするか、理由付きで比較したか。  
- 厚み、均一性、密着、孔食、ボイド、接触抵抗、はんだ濡れのどれを合否にするか決めたか。  
- 前処理、洗浄、乾燥、排水処理、排ガス、測定の運用能力を外注先に確認したか。  
- job plater か captive かより、浴管理と欠陥解析の実力があるかを見たか。  
- 多重リフロー、保存、湿熱、塩水、振動、熱サイクルなど、実使用に近い条件で評価したか。  
- 量産歩留まりだけでなく、再加工性・手直し性・現場施工性まで見たか。  
- 規格や標準で縛れる部分と、個別仕様で詰める部分を分けたか。  
- コストは単価ではなく、工程数、検査、再処理、返品、保証まで含む総額で見たか。  

## 7. Reader decision layer

- この案件は、まず「防錆主導」か「導通主導」か「意匠主導」かを決める。  
- 自動車なら、溶接性と耐食の両立を優先し、必要ならクロメートフリーだけで押し切らない。  
- PCB なら、実装方式に合わせて OSP / ENIG / IAg / ISn / HASL を比較する。  
- 半導体周辺なら、ワイヤボンドとフリップチップで表面仕上げを分ける。  
- 建材なら、材料単体ではなく保管・施工・雨がかり条件を含めて選ぶ。  
- 装飾なら、見た目と耐変色を主評価にし、厚膜防食の発想を持ち込まない。  
- 外注先は、めっき厚より先に、前処理・洗浄・排水・分析・復旧手順を確認する。  
- 品質は外観合格だけでなく、実使用後の濡れ性、接触抵抗、剥離、腐食再現で判定する。  
- コストは加工単価ではなく、歩留まりと再処理コストまで入れて比較する。  
- 迷ったら、IPC / JEITA / JISF / METI / EPA のどの標準に乗せるかを先に決める。  

## 8. 不確実性と見直しポイント

今回の整理は、公開されている標準・団体資料・公的資料を中心にしたため、個別の材料系や浴組成、企業固有の量産ノウハウまでは踏み込んでいません。特に ENIG / ENEPIG、車載向け耐食、建材向け外装仕様は、実際には顧客規格と試験条件で大きく変わります。実案件では、最新版の IPC / JIS / 社内規格と、製品の使用環境データを合わせて再確認するのが安全です。  
出典: [IPC-4552](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf), [IPC-6012F](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed), [JFS](https://www.jisf.or.jp/business/standard/jfs/)

## 参考ソース

- [METI 用途分類解説資料](https://www.meti.go.jp/policy/chemical_management/kasinhou/files/information/ra/use_category_002.pdf)
- [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- [OSHA Electroplating Fact Sheet](https://www.osha.gov/Publications/OSHA_FS-3648_Electroplating.pdf)
- [日本鉄鋼連盟 亜鉛鉄板](https://www.jisf.or.jp/business/tech/aen/index.html)
- [日本鉄鋼連盟 表面処理鋼板](https://www.jisf.or.jp/knowledge/variety/hyo.html)
- [日本鉄鋼連盟 塗装亜鉛系めっき鋼板ご使用の手引き](https://www.jisf.or.jp/info/book/docs/tosouaenkeimekkikouhangosiyounotebikikaitei.pdf)
- [日本鉄鋼連盟 JFS](https://www.jisf.or.jp/business/standard/jfs/)
- [トヨタ 75年史 ユニット系プレス・接合](https://www.toyota.co.jp/jpn/company/history/75years/data/automotive_business/production/production_engineering/major_components/unit-field_stamping/engineering.html)
- [IPC-4552 ENIG](https://www.ipc.org/TOC/IPC-4552wAm-1-2.pdf)
- [IPC Study of Various PCBA Surface Finishes](https://www.ipc.org/system/files/technical_resource/E15%26S13_02.pdf)
- [IPC-A-600 Acceptability of Printed Boards](https://www.electronics.org/ipc-600-acceptability-printed-boards-endorsement-program)
- [IPC-6012F Rigid Printed Boards](https://www.electronics.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
- [JEITA 電子部品の役割](https://home.jeita.or.jp/ecb/about/part.html)
- [JEITA 電子部品の信頼性評価ガイド](https://home.jeita.or.jp/page_file/20200526181633_4fCp1lxIJG.pdf)
- [JEITA/ITRS 2007 Assembly and Packaging](https://semicon.jeita.or.jp/STRJ/ITRS/2007/12%202007_ITRS_A%26P_Japanese_v2.0.pdf)
- [JEITA/ITRS 2005 Assembly & Packaging](https://semicon.jeita.or.jp/STRJ/ITRS/2005/12_2005A%26P.pdf)
