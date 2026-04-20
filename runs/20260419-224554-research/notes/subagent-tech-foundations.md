# めっき 技術基礎メモ

## まず結論

めっきは「表面に薄い機能層をつくる」技術だが、実務上は防食だけでなく、導電、接触抵抗低減、はんだ付け性、拡散バリア、EMI/ESD シールド、耐摩耗、意匠、膜厚制御まで含む広い設計領域として扱うのが正確である。ASTM の金属・無機被膜委員会 B08 は、電気めっき、無電解めっき、置換めっき、真空系、化成処理、陽極酸化、溶融めっき、熱被覆を同じ技術群として整理しており、AMPP も防食系の被膜を「液状から乾燥して固膜になるもの」や「溶融・電気めっき・溶射で与える金属膜」として整理している。ここでの「湿式/乾式」は、便宜上、液相浴を使う工程群と、真空・熱・溶融金属などの非水系工程群に分けている。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center))

## 工程の整理

| 区分 | 技術的な見方 | 代表例 | 重要な含意 |
|---|---|---|---|
| 湿式めっき | 液相浴で金属イオンを析出・置換・自己触媒還元する | 電気めっき、無電解めっき、置換めっき | 複雑形状に膜を与えやすいが、前処理と浴管理が性能を左右する。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08)) |
| 非湿式めっき/表面処理 | 真空、熱、溶融金属、熱分解系を使う | 真空蒸着、スパッタ、イオンプレート、溶融亜鉛めっき、熱溶射 | 皮膜の密着機構や膜質が湿式と異なり、厚み・応力・熱影響の見方も変わる。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html), [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center)) |

## 電気めっき

電気めっきは、外部電源を使って金属を析出させる基本技術で、ASTM B08 はこれを金属・無機被膜の中核プロセスとして扱う。設計上は「見た目」よりも、用途ごとの機能要求を先に置くべきで、たとえば亜鉛めっきは防食、錫めっきは低接触抵抗とはんだ付け性、金めっきは低く安定した接触抵抗とボンダビリティが主要用途になる。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488))

亜鉛電気めっきの ASTM B633 は、鉄鋼を腐食から守ることを主目的にしつつ、膜厚クラス、補助仕上げ、付着性、耐食性、水素脆化対策を同時に規定する。つまり、電気めっきは単なる「膜を載せる」工程ではなく、前処理、後処理、膜厚、密着、脆化抑制を一体で設計する工程である。([ASTM B633](https://store.astm.org/Standards/B633.htm))

錫電気めっきは、低接触抵抗、防食、はんだ付け性、耐かじり性に使われる。ASTM B545 は、膜厚が薄くなるほどポロシティが増え、用途ごとに最小厚みの指定が必要になることも明記している。接触用途とはんだ用途では、単に「錫が乗っている」だけでは足りず、厚みと孔食管理が要点になる。([ASTM B545-22](https://store.astm.org/b0545-22.html))

## 無電解めっき

無電解 Ni-P は、外部電流を使わず、自己触媒的な化学還元で析出する。ASTM B733 は、酸性水溶液から高温で析出し、不規則形状でも液が回れば均一膜厚を得やすいこと、さらに硬さ・耐摩耗・耐食・磁性・導電性・拡散バリア・はんだ付け性などの多機能を持つことを示している。無電解めっきの本質は「電流がないこと」ではなく、「複雑形状に均一に機能膜を与えやすいこと」にある。([ASTM B733](https://store.astm.org/b0733-22.html))

Ni-P の低リン側は電子用途でとくに重要で、ASTM B733 は 1〜3%P の皮膜を、はんだ付け性、ボンディング性、導電性向上、強アルカリ耐性に使うとしている。Nickel Institute の技術資料も、無電解ニッケルの性質と用途を、工業用途の機能皮膜として整理している。([ASTM B733](https://store.astm.org/b0733-22.html), [Nickel Institute: Properties and Applications of Electroless Nickel](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/))

ASTM B733 は、無電解 Ni-P の膜厚評価、密着試験、孔食、微小硬さ、水素脆化まで評価対象に含めており、無電解めっきでも「浴が入れば終わり」ではなく、後工程と検査までが一体であることを示している。([ASTM B733](https://store.astm.org/b0733-22.html))

## 溶融めっき

溶融めっきは、溶融金属浴に浸漬して合金層を作るプロセスで、ASTM A123/A123M は鉄鋼製品への溶融亜鉛めっきの要求を規定している。ASTM A153/A153M は、溶融亜鉛が鉄表面と冶金反応して Zn/Fe 合金層を形成し、鋼に密着することを明示している。防食の観点では、AMPP も亜鉛を用いた被膜がガルバニック保護を与えることを説明している。([ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html), [ASTM A153/A153M-23](https://store.astm.org/a0153_a0153m-23.html), [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center))

溶融めっきは厚膜で耐久性が高い一方、寸法影響や歪み、前処理の影響を受けやすい。ASTM A385 は、良質な溶融亜鉛めっきを得るための注意点として、部材の化学成分や表面状態のばらつき、洗浄、寸法変化への注意を挙げている。([ASTM A385](https://store.astm.org/a0385-08.html))

## 主要機能

防食は最も広い用途だが、めっきの機能はそれだけではない。亜鉛は鉄鋼の防食、錫は低接触抵抗とはんだ付け性、金は低く安定した接触抵抗とボンディング性、無電解 Ni-P は拡散バリア・耐摩耗・導電補助・はんだ付け性、EMI/ESD 用の多層無電解 Ni/Cu はシールド機能を狙う。機能要件が変わると、皮膜材料・厚み・浴・後処理の最適解も変わる。([ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488), [ASTM B733](https://store.astm.org/b0733-22.html), [ASTM B904-25](https://store.astm.org/standards/b904))

## 重要論点

### 防食

防食はめっきの基礎機能だが、材料選定だけでは決まらない。錫めっきでも屋外では腐食が起こりうる一方、亜鉛めっきは鉄鋼の犠牲防食として広く使われる。溶融亜鉛めっきは、バリア保護だけでなくガルバニック保護も与える点が重要である。([ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html), [ASTM news: corrosion protection for steel bars](https://www.astm.org/news/press-releases/new-astm-standard-provides-corrosion-protection-steel-bars))

### 導電・接触

接触抵抗を下げる用途では、錫や金のように電気的な接点特性が重視される。錫は低接触抵抗、金は低く安定した接触抵抗が主要用途であり、無電解 Ni-P の低リン側は導電性向上にも使われる。接点用途では、酸化膜、ポロシティ、摩耗、フレッティングまで含めて考える必要がある。([ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488), [ASTM B733](https://store.astm.org/b0733-22.html), [ASTM B02 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b02/scope-b02))

### はんだ付け性

はんだ付け性は、錫めっきと低リン無電解 Ni-P で重要な設計要求になる。ASTM B545 は錫めっきをはんだ付け性のための表面として位置づけ、ASTM B733 は電子用途の低リン Ni-P にはんだ付け性を明記している。PCB の表面処理では、IPC-6012F が solderability testing と dewetting を主要な要求項目に追加しており、はんだのぬれだけでなく、濡れムラや界面欠陥まで評価対象になる。([ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733](https://store.astm.org/b0733-22.html), [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed))

### 膜厚

膜厚は、めっき仕様の中核である。ASTM B659 は、複数の金属・無機被膜で膜厚がサービス性能に直結し、測定法にはそれぞれ適用限界があると整理している。ASTM B633、B545、B733 もそれぞれ膜厚クラスや最小厚み、サービス条件番号を持ち、厚みは「見た目」ではなく性能パラメータとして扱われる。([ASTM B659](https://store.astm.org/b0659-90r21.html), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733](https://store.astm.org/b0733-22.html))

### 前処理

前処理は密着の前提条件で、表面清浄化、応力除去、機械処理、酸洗い、スミット除去、エッチングなどが含まれる。ASTM B242 は高炭素鋼の電気めっき前処理として、最小限の水素脆化と最大限の密着を目指す手順を示す。ASTM B849 は、電気めっきや無電解めっきなどで生じうる水素脆化を減らすための事前熱処理を規定している。([ASTM B242](https://store.astm.org/b242.html), [ASTM B849](https://store.astm.org/Standards/B849.htm))

### 密着

密着は、前処理・浴管理・後処理の総合結果である。ASTM B733 は無電解 Ni-P に対して、密着評価を bend / impact / thermal shock で確認するとし、B850 はめっき後熱処理が水素脆化低減に有効だが完全保証ではないと注意している。つまり、密着は「析出したか」ではなく「使用条件で剥がれないか」で見る必要がある。([ASTM B733](https://store.astm.org/b0733-22.html), [ASTM B850](https://store.astm.org/b0850-98r22.html))

### 水素脆化

水素脆化は高強度鋼で特に重要で、めっきそのものよりも、脱脂・酸洗い・めっき・後処理の連鎖で発生しやすい。ASTM B849 は前処理での低減策、ASTM B850 は後熱処理、ASTM F519 は製造中の表面処理・前処理・めっき条件が水素脆化を起こしていないかを機械試験で検証する枠組みを与える。([ASTM B849](https://store.astm.org/Standards/B849.htm), [ASTM B850](https://store.astm.org/b0850-98r22.html), [ASTM F519](https://store.astm.org/f0519-17a.html))

### microvia

microvia は PCB/HDI の要所で、IPC-2226 ベースでは「直径 150 μm 以下のブラインドホール」を指す。IPC-6012F は、PTH、buried/blind vias、microvias を含む構造に対して、microvia reliability、internal plated layers、solderability testing、dewetting まで要求を拡張している。IPC の技術資料でも、microvia-to-target plating failure は従来の顕微鏡観察だけでは見落としうると警告されており、microvia は「穴を埋める」ではなく「接続信頼性を作る」対象である。([IPC microvia definition PDF](https://www.ipc.org/system/files/technical_resource/E2%26S29_01.pdf), [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed), [IPC microvia reliability warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high))

### microvia の充填

microvia 充填では、電解銅めっきが実務上の中心になる。IPC の技術発表資料では、微小径の microvia を銅で充填する技術が量産で成立しており、via-in-pad、熱管理、積層 microvia の信頼性改善に使われている。別の IPC 資料では、through-hole でも bridge 形成から DC 補充填へつなぐ 2 段階の銅めっきで、薄い表面銅と良好な充填を両立できるとしている。([IPC microvia fill paper](https://www.ipc.org/system/files/technical_resource/E42%26S02_01%20-%20Moody%20Dreiza_Mustafa%20Oezkoek.pdf), [IPC through-hole fill paper](https://www.ipc.org/system/files/technical_resource/E38%26S09-01%20-%20Jim%20Watkowski.pdf))

## 参照した一次情報ソース

1. [ASTM Committee B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08)
2. [ASTM B633](https://store.astm.org/Standards/B633.htm)
3. [ASTM B545-22](https://store.astm.org/b0545-22.html)
4. [ASTM B733-22](https://store.astm.org/b0733-22.html)
5. [ASTM B659](https://store.astm.org/b0659-90r21.html)
6. [ASTM B849](https://store.astm.org/Standards/B849.htm)
7. [ASTM B850-98(2022)](https://store.astm.org/b0850-98r22.html)
8. [ASTM F519](https://store.astm.org/f0519-17a.html)
9. [ASTM A123/A123M](https://store.astm.org/a0123_a0123m-00.html)
10. [ASTM A153/A153M-23](https://store.astm.org/a0153_a0153m-23.html)
11. [AMPP Protective Coatings Learning Center](https://www.ampp.org/technical-research/what-is-corrosion/protective-coatings-learning-center)
12. [Nickel Institute: Nickel Plating Handbook](https://nickelinstitute.org/en/resources/publications/nickel-plating-handbook-en/)
13. [Nickel Institute: Properties and Applications of Electroless Nickel](https://nickelinstitute.org/en/resources/technical-guides/properties-and-applications-of-electroless-nickel-10081/)
14. [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed)
15. [IPC microvia definition PDF](https://www.ipc.org/system/files/technical_resource/E2%26S29_01.pdf)
16. [IPC microvia reliability warning](https://www.ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high)
17. [IPC microvia fill paper](https://www.ipc.org/system/files/technical_resource/E42%26S02_01%20-%20Moody%20Dreiza_Mustafa%20Oezkoek.pdf)
18. [IPC through-hole fill paper](https://www.ipc.org/system/files/technical_resource/E38%26S09-01%20-%20Jim%20Watkowski.pdf)

## 後で本体レポートに入れるべき high-signal claims

1. めっきは防食だけでなく、導電、接触抵抗低減、はんだ付け性、拡散バリア、EMI/ESD、耐摩耗まで含む機能表面技術として整理すべきである。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733-22](https://store.astm.org/b0733-22.html), [ASTM B488](https://store.astm.org/standards/b488), [ASTM B904-25](https://store.astm.org/standards/b904))
2. 湿式系は電気めっき、無電解めっき、置換めっきを中心に、液相浴の化学管理と前処理が性能を支配する。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM B733-22](https://store.astm.org/b0733-22.html), [ASTM B849](https://store.astm.org/Standards/B849.htm))
3. 非湿式系は真空、熱、溶融金属を使う被膜群として別枠で考えるべきで、溶融亜鉛めっきは冶金的に Zn/Fe 合金層を作る。([ASTM B08 Scope](https://www.astm.org/membership-participation/technical-committees/committee-b08/scope-b08), [ASTM A153/A153M-23](https://store.astm.org/a0153_a0153m-23.html))
4. 亜鉛電気めっきは防食向け、錫電気めっきは低接触抵抗とはんだ付け性向け、金電気めっきは低く安定した接触抵抗とボンディング向けというように、用途別に材料が選ばれる。([ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B488](https://store.astm.org/standards/b488))
5. 無電解 Ni-P は高温の酸性水溶液から自己触媒的に析出し、複雑形状でも均一膜厚を与えやすい。([ASTM B733-22](https://store.astm.org/b0733-22.html))
6. 低リン無電解 Ni-P は電子用途で、はんだ付け性、ボンディング性、導電性向上に使われる。([ASTM B733-22](https://store.astm.org/b0733-22.html))
7. 膜厚は性能パラメータであり、仕様ごとに service class や最小厚み、測定法が定義される。([ASTM B659](https://store.astm.org/b0659-90r21.html), [ASTM B633](https://store.astm.org/Standards/B633.htm), [ASTM B545-22](https://store.astm.org/b0545-22.html), [ASTM B733-22](https://store.astm.org/b0733-22.html))
8. 前処理と後熱処理は水素脆化対策の本体であり、めっき後のベーキングだけでなく、めっき前の応力除去や洗浄条件も重要である。([ASTM B849](https://store.astm.org/Standards/B849.htm), [ASTM B850-98(2022)](https://store.astm.org/b0850-98r22.html), [ASTM F519](https://store.astm.org/f0519-17a.html))
9. 密着は bend、impact、thermal shock などの試験で確認すべきで、特に無電解 Ni-P や接点用途では表面の使われ方まで含めて評価する必要がある。([ASTM B733-22](https://store.astm.org/b0733-22.html), [ASTM B545-22](https://store.astm.org/b0545-22.html))
10. microvia は 150 μm 以下のブラインドホールとして設計され、IPC-6012F では microvia reliability と solderability/dewetting まで要求が拡張されている。([IPC microvia definition PDF](https://www.ipc.org/system/files/technical_resource/E2%26S29_01.pdf), [IPC-6012F release](https://www.ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed))
11. microvia 充填はすでに量産技術であり、電解銅めっきは via-in-pad と熱管理のための基盤技術になっている。([IPC microvia fill paper](https://www.ipc.org/system/files/technical_resource/E42%26S02_01%20-%20Moody%20Dreiza_Mustafa%20Oezkoek.pdf), [IPC through-hole fill paper](https://www.ipc.org/system/files/technical_resource/E38%26S09-01%20-%20Jim%20Watkowski.pdf))

