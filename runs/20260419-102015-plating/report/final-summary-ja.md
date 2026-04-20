# めっき（plating）の技術的基礎 調査メモ

調査日: 2026-04-19

## 1. 重要ポイント

1. めっきは、基材表面に金属皮膜を形成して、防食、耐摩耗、導電、はんだ付け性、装飾性などの機能を付与する表面技術である。
2. 狭義では湿式の金属析出を指すことが多いが、日本語実務では真空蒸着やイオンプレーティングを「真空めっき」と呼ぶ場合もあり、用語の幅に注意が必要である。
3. 電気めっきは、外部電流で金属イオンを還元して析出させる方法で、汎用性、コスト、厚膜化、皮膜特性の調整しやすさに強みがある。
4. 電気めっきの弱点は、電流分布の影響で膜厚が偏りやすく、端部が厚く、凹部や深穴が薄くなりやすい点である。前処理不良や浴管理不良も品質に直結する。
5. 無電解めっきは、外部電流なしで自己触媒的に金属を析出させる方法で、複雑形状や穴内部でも比較的均一・低気孔な皮膜を得やすい。
6. 無電解めっきは、浴の安定性と化学管理が難しく、速度やコストの面で電気めっきより不利になりやすい。代表例は無電解 Ni-P、Ni-B、無電解 Cu である。
7. 溶融めっきは、洗浄した素材を溶融金属に浸して皮膜を作る方法で、代表は溶融亜鉛めっきである。鋼と亜鉛が金属学的に反応して、耐食性の高い被膜を形成する。
8. 溶融亜鉛めっきは、バリア防食に加えて犠牲防食も働くため、屋外鋼構造物で特に強い。全浸漬なので内面や複雑部にも回りやすい。
9. 乾式表面処理の PVD、CVD、スパッタ、イオンプレーティングは、機能的には「めっき」に近く扱われることがあるが、媒体と成膜機構は湿式めっきと別系統である。
10. 代表的な皮膜金属は、Zn、Ni、Cr、Cu、Sn、Au、Ag、Pd、Pt、Rh などで、合金や複合めっきとして Zn-Ni、Ni-Co、Ni-P、真鍮、はんだ系なども使われる。
11. 典型的な湿式工程は、脱脂、洗浄、酸洗または酸化膜除去、活性化、めっき、水洗、後処理、乾燥であり、実務上は前処理の良否が密着性と欠陥率を大きく左右する。
12. 品質指標は用途依存だが、一般化すると膜厚、均一性、密着性、外観、連続性、気孔、耐食性、硬さ、耐摩耗性、延性や脆化の有無が中心になる。
13. 溶融亜鉛めっきでは、とくに膜厚、外観・仕上げ、密着性、脆化、必要に応じた不動態化の有無が重要な検査項目になる。
14. 代表的不具合は、密着不良、はく離、ふくれ、ピット、ピンホール、ざらつき、こぶ、焼け、膜厚不足、応力割れ、水素脆化である。溶融めっきでは bare spot、flux inclusion、run、touch mark、wet storage stain も代表的である。
15. 外観異常が常に機能不良とは限らない。溶融亜鉛めっきでは、酸化線、粗面、striations などは、耐食性や intended use を損なわなければ許容される場合がある。

## 2. 主要ソース

- 表面技術協会 めっき部会: https://mekki.sfj.or.jp/
- 日本表面処理機材工業会 基本説明: https://www.kizaikou.or.jp/basic.html
- 米国 DOE/Lawrence Livermore の基礎資料: https://www.osti.gov/servlets/purl/6149794
- Open University の無電解めっき解説: https://www.open.edu/openlearn/science-maths-technology/engineering-technology/manupedia/electroless-plating
- American Galvanizers Association, Batch Hot-Dip Galvanizing: https://galvanizeit.org/corrosion/corrosion-protection/zinc-coatings/batch-hot-dip-galvanizing
- American Galvanizers Association, Inspection Guide PDF: https://galvanizeit.org/uploads/publications/Galvanized_Steel_Inspection_Guide.pdf
- J-STAGE, めっき前処理技術: https://www.jstage.jst.go.jp/article/sfj1970/33/8/33_8_286/_article/-char/ja/
- J-STAGE, 真空分野からみた表面処理分類: https://www.jstage.jst.go.jp/article/jvsj1958/30/12/30_12_1046/_article/-char/ja/
- J-STAGE, 物理的表面処理技術: https://www.jstage.jst.go.jp/article/sfj1950/30/5/30_5_216/_pdf

## 3. 用語上の注意

- 「めっき」は狭義では湿式の析出法だが、実務では「真空めっき」「ドライめっき」のような拡張用法がある。
- 「無電解めっき」と「置換めっき」は混同されやすいが、自己触媒型と置換反応型は区別して扱うのが安全である。
- 「電気めっき」と「電着」は近いが、文脈によっては電鋳や電解析出一般を含む広い語になる。
- 「亜鉛めっき」と「溶融亜鉛めっき」と「電気亜鉛めっき」は同じではない。
- 「ガルバナイズ」はしばしば広く使われるが、AGA は batch hot-dip galvanizing と他の亜鉛系被覆を区別している。

## 4. 日付依存の注意

- 定義や基本原理は比較的安定している。
- ただし、規格値、合否判定、膜厚要求、サンプリング、補修許容範囲は ASTM/JIS/ISO の改定で変わりうる。
- 六価クロム、カドミウム、シアン浴などに関する環境・労働安全規制は変化しやすい。
- 代替皮膜としての三価クロム、Zn-Al-Mg、Zn-Ni、複合無電解 Ni などの実用位置づけも年次で変動する。
