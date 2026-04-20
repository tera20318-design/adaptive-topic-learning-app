# Child C Notes

## Scope

- Theme: めっき
- Focus: 薬品管理、排水・環境負荷、六価クロムなどの典型論点、膜厚・密着性・耐食性などの品質論点
- Output style: 親が `source_log.md` と `claim_table.md` に転記しやすい粒度

## Candidate Sources

- `C-S01`
  Title: めっき（化学物質管理の対策シート）
  Org: 厚生労働省 安全衛生情報センター
  URL: https://anzeninfo.mhlw.go.jp/user/anzen/kag/pdf/taisaku/Plating.pdf
  Why useful: SDS、換気、保護具、教育、使用量・保管量管理など、現場安全の基本を一枚で押さえられる。

- `C-S02`
  Title: 水質汚濁防止法施行規則等の一部を改正する省令の公布について
  Org: 環境省
  Date: 2024-01-25
  URL: https://www.env.go.jp/press/press_02672.html
  Why useful: 六価クロムの排水基準見直しと、電気めっき業への暫定基準を確認できる一次資料。

- `C-S03`
  Title: 六価クロムの下水排除基準について
  Org: 東京都下水道局
  Date: 2025-04-01
  URL: https://www.gesui.metro.tokyo.lg.jp/information/topics/2024/10/1001_6723
  Why useful: 下水道接続時の基準と、電気めっき業の暫定基準の実務確認に使える。

- `C-S04`
  Title: PRTRに関するQ&A（PRTR排出等算出マニュアル）
  Org: 経済産業省
  URL: https://www.meti.go.jp/policy/chemical_management/law/qa/manual_faq.html
  Why useful: めっき工程での陽極溶解分、浴への追加投入量など、薬品・金属の物質収支管理の考え方が分かる。

- `C-S05`
  Title: PRTR 排出量等算出マニュアル 第III部
  Org: 経済産業省
  Date: 2025
  URL: https://www.meti.go.jp/policy/chemical_management/law/prtr/pdf/r7_haishutsu_sanshutsu_manual/3.pdf
  Why useful: 排水処理後の水域排出量、汚泥の事業所外移動などを含めた算定例がある。

- `C-S06`
  Title: Electroplating Effluent Guidelines
  Org: U.S. EPA
  Date: 2026-03-17
  URL: https://www.epa.gov/eg/electroplating-effluent-guidelines
  Why useful: 排水論点に加えて、クロム工程で PFAS が六価クロムミスト対策に使われる場合があることを押さえられる。

- `C-S07`
  Title: Controlling Hexavalent Chromium Exposures during Electroplating
  Org: OSHA
  Date: 2013
  URL: https://www.osha.gov/sites/default/files/publications/OSHA_FS-3648_Electroplating.pdf
  Why useful: 六価クロムミスト、皮膚接触、換気、ミスト抑制、三価クロム代替など、典型的な安全論点がまとまっている。

- `C-S08`
  Title: 現場技術者のための めっき排水の処理技術 著者インタビュー
  Org: 東京都立産業技術研究センター
  Date: 2021-11-01
  URL: https://www.iri-tokyo.jp/tiri-news/jigyo-2021-11-01/
  Why useful: 排水処理設備の設定値継承不足、浴変更時の再検証など、実務で起きやすい落とし穴が具体的。

- `C-S09`
  Title: めっき液、めっきプロセスのモニタリング技術
  Org: 産業技術総合研究所
  URL: https://unit.aist.go.jp/stri/group_ics_detail2.html
  Why useful: めっき浴の不純物・添加剤状態と品質・環境負荷の関係を押さえられる。

- `C-S10`
  Title: めっき・塗装複合試験
  Org: 東京都立産業技術研究センター
  URL: https://www.iri-tokyo.jp/service/testing/brand/b-coating/
  Why useful: 耐食性、剥離、不具合断面観察など、品質評価を膜厚以外も含めて整理できる。

## Atomic Claims

- `C-C01`
  Claim: めっき工程の薬品管理では、SDS確認、ラベル表示、危険有害性を踏まえた手順書、換気、保護具、教育をセットで運用するのが基本である。
  Evidence: 厚労省対策シートが、SDS入手・閲覧、作業教育、換気設備、保護具、健康診断等を要点として列挙。
  Sources: `C-S01`
  Confidence: High
  Caveat: 実際の義務範囲は使用物質と作業内容で変わる。

- `C-C02`
  Claim: めっき薬品は「必要量だけ使う・保管する」「容器を確実に閉める」が安全と漏えい抑制の基本である。
  Evidence: 厚労省対策シートが、過剰使用・過剰保管の回避、容器のふた管理、古い薬品の廃棄を明示。
  Sources: `C-S01`
  Confidence: High
  Caveat: 個別薬品の反応禁忌や保管区分までは別途確認が必要。

- `C-C03`
  Claim: 日本の六価クロム排水規制は 2024-04-01 から強化され、一般排水基準は 0.2 mg/L になった。
  Evidence: 環境省改正通知が六価クロム化合物の排水基準を 0.2 mg/L に改めると明示。
  Sources: `C-S02`
  Confidence: High
  Caveat: 公共用水域への排出基準の話であり、下水道接続とは分けて扱う必要がある。

- `C-C04`
  Claim: 電気めっき業には六価クロムの暫定基準 0.5 mg/L が 3年間適用されているため、一般基準と業種暫定基準を混同しない方がよい。
  Evidence: 環境省と東京都下水道局の資料が、電気めっき業の暫定基準 0.5 mg/L と適用期間を記載。
  Sources: `C-S02`, `C-S03`
  Confidence: High
  Caveat: 適用先が「公共用水域排出」と「下水排除」で異なる。自治体差や期限延長の可能性にも注意。

- `C-C05`
  Claim: めっき工場では、浴変更や規制強化により既存の排水処理設備・設定値が合わなくなることがある。
  Evidence: 都産技研の記事が、浴変更や規制強化で従来設備では対応できなくなる事例と設定値伝承不足の問題を指摘。
  Sources: `C-S08`
  Confidence: Medium
  Caveat: 実務記事ベースであり、個別工場の適否は現地条件に依存。

- `C-C06`
  Claim: めっき工程の環境管理では、陽極溶解分、浴への追加投入、排水処理後の水域排出、汚泥の事業所外移動まで含めた物質収支把握が重要である。
  Evidence: METI Q&A と算定マニュアルが、陽極減耗分・浴投入量・排水処理・汚泥移動を算定対象として例示。
  Sources: `C-S04`, `C-S05`
  Confidence: High
  Caveat: PRTR算定は制度目的の手法であり、操業管理指標そのものではない。

- `C-C07`
  Claim: 六価クロムめっきの典型安全論点は、ミスト吸入と皮膚接触であり、開放容器、圧縮空気乾燥、清掃遅れ、換気不良がばく露を増やす。
  Evidence: OSHA電気めっき向けファクトシートがばく露経路と悪化要因、LEVや作業改善策を列挙。EPAもクロム化合物の大気排出を重要論点としている。
  Sources: `C-S06`, `C-S07`
  Confidence: High
  Caveat: 国内法の詳細値までは別資料確認が必要。三価クロム代替は用途により適否が分かれる。

- `C-C08`
  Claim: めっき工程では、六価クロムミスト対策が別の環境論点を生む場合があり、PFASのような補助薬剤使用も確認対象になる。
  Evidence: EPAが、クロム工程の一部施設で Cr(VI) 排出抑制のため PFAS が使われ、排水論点になっていると説明。
  Sources: `C-S06`
  Confidence: Medium
  Caveat: 米国の規制論点であり、日本の一般的な全工場実態とは限らない。

- `C-C09`
  Claim: 品質論点は膜厚だけでは足りず、密着性、剥離起点、耐食性、不具合断面の観察を組み合わせて評価する方が実務に近い。
  Evidence: 都産技研が、不具合解析で断面観察を、耐食性評価で塩水噴霧試験等を用いると紹介。
  Sources: `C-S10`
  Confidence: Medium
  Caveat: 製品によって要求特性は異なる。外観、摩耗、耐候など追加論点が入る場合もある。

- `C-C10`
  Claim: めっき浴の不純物や添加剤状態は品質に影響しやすく、液管理の高精度化は品質向上だけでなくコスト・環境負荷低減にもつながる。
  Evidence: 産総研が、めっき浴は不純物等の影響を受けやすく、液状態の高精度管理で品質向上と環境負荷低減を目指すと説明。
  Sources: `C-S09`
  Confidence: Medium
  Caveat: 主に先端めっきプロセス文脈の研究紹介。一般工場では導入レベルに差がある。

## Friction Points

- 六価クロムの `0.2 mg/L` は一般基準で、電気めっき業には暫定 `0.5 mg/L` がある。ここを混ぜると誤読が起きやすい。
- 排水基準と下水排除基準は同じ文脈ではない。工場が公共用水域へ直接出すのか、下水道へ流すのかで確認先が変わる。
- 三価クロム代替は安全・環境面で有力だが、全ての用途で無条件に置換できるとはまだ言い切らない方がよい。
- PFASは国際的には有力論点だが、日本の一般的なめっき総論へどこまで入れるかは親が判断した方がよい。
- 品質は膜厚だけで評価しない。密着性、腐食起点、前処理、後処理、複合皮膜の相性で結果が変わる。

## Transfer Shortlist

- `source_log.md` へ優先転記:
  `C-S01`, `C-S02`, `C-S03`, `C-S04`, `C-S05`, `C-S07`, `C-S08`, `C-S10`

- `claim_table.md` へ優先転記:
  `C-C01`, `C-C03`, `C-C04`, `C-C05`, `C-C06`, `C-C07`, `C-C09`

- 余力があれば追加:
  `C-S06`, `C-S09`, `C-C08`, `C-C10`
