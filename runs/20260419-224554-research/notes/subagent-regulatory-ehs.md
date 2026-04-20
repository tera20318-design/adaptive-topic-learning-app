# 規制・EHSメモ（めっき）

調査日: 2026-04-19  
対象: 六価クロムを中心に、日本・米国・EU の規制/EHS と日付依存論点を一次情報のみで整理

## まず押さえるべき結論

- 日本では、公共用水域・地下水の六価クロム環境基準が `2022-04-01` に `0.05 mg/L` から `0.02 mg/L` へ引き下げられた。これが後続の測定・検定方法見直しの直接の背景になっている。  
  URL: [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html)
- 日本の一般排水基準では、六価クロム化合物は `0.2 mg Cr(VI)/L`。環境基準より 1 桁緩いが、工場・事業場の排水口で適用される。  
  URL: [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
- `2024-02-05` に環境省が六価クロム化合物の測定方法を JIS K 0102-3 ベースへ見直し、分冊後の `JIS K0102-3 24.3.3` のフレーム原子吸光分析法を公定法から除外した。施行は `2024-04-01`。  
  URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
- 現行の暫定排水基準は、`2024-12-11` 時点で亜鉛の電気めっき業 `1 業種` のみで、`4 mg/L` を `2029-12-10` まで延長している。今回確認した公式資料では、六価クロムの暫定排水基準は見当たらなかった。  
  URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- 公共用水域への排出は水質汚濁防止法の排水規制で、排水基準は排水口で適用される。一方、公共下水道へ排除する場合は下水道法と条例に基づく除害施設・必要な措置が別途必要になる。  
  URL: [環境省 水濁法施行通達](https://www.env.go.jp/hourei/05/000137.html) / [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)
- 米国 OSHA の Chromium(VI) 標準は `5 µg/m³` の `8-hour TWA` を上限とし、規制区域、工学的・作業管理、PPE、医療監視、HazCom を要求する。  
  URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
- 米国 EPA は、`40 CFR Part 413` / `Part 433` の電気めっき・金属仕上げの排水規則を見直し中で、クロム仕上げ施設が PFAS の主要排出源になりうると整理している。  
  URL: [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines) / [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
- EU RoHS は電気電子機器の `hexavalent chromium` を含む `10 substances` を制限しており、ECHA の整理では `0.1 % w/w` の一様材料限度が示されている。  
  URL: [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) / [ECHA RoHS restricted substances](https://echa.europa.eu/en/restricted-subs-referred-art-4-rohs/-/legislationlist/substance/)
- REACH Annex XVII の nickel 規制では、ピアス等は `0.2 µg/cm²/week`、皮膚と長時間接触する製品は `0.5 µg/cm²/week` を超えてはならず、非ニッケル被膜も 2 年間の通常使用で `0.5` を超えないことが必要。  
  URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
- PFAS とクロム工程の関係は実務上かなり強い。EPA は、chrome plating のフューム抑制剤を対象に PFAS を調査しており、過去の PFOS 系代替や fume suppressant がクロムめっき工程に使われてきたことを公式に示している。  
  URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants) / [EPA proposed CERCLA PFOS/PFOA rule](https://www.epa.gov/system/files/documents/2022-08/FRL%207204-02-OLEM%20_%20Designating%20PFOA%20and%20PFOS%20as%20HSs%20_NPRM_20220823.pdf)

## 日本の論点

### 1) 六価クロムの環境基準改正と排水規制の連動

- `2022-04-01` 施行で、公共用水域・地下水の六価クロム環境基準は `0.05 mg/L` から `0.02 mg/L` に改正された。  
  URL: [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html)
- `2024-02-05` の改正では、六価クロム化合物の測定方法を分冊後の `JIS K0102-3` に合わせ、旧来のフレーム原子吸光分析法を公定法から外した。`2024-04-01` 施行なので、レポートでは「告示日」と「施行日」を分けて書くのが安全。  
  URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
- 一般排水基準は `0.2 mg Cr(VI)/L` で、これは工場・事業場の排水口での基準。環境基準 `0.02 mg/L` とは用途が違うので、同じ数字として扱わない。  
  URL: [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)

### 2) 暫定排水基準

- `2024-12-11` 時点の公式資料では、暫定排水基準が残っているのは亜鉛の電気めっき業のみで、`4 mg/L` を `2029-12-10` まで延長している。  
  URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
- 六価クロムについては、今回の一次情報確認では「暫定排水基準あり」とは言えず、レポートでは「確認できた現行の暫定基準は亜鉛のみ」と書くのが安全。  
  URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)

### 3) 公共用水域と下水道の区別

- 水質汚濁防止法は、公共用水域に出る排出水を対象に排水規制をかけ、排水基準は排水口で適用される。  
  URL: [環境省 水濁法施行通達](https://www.env.go.jp/hourei/05/000137.html)
- 公共下水道へ排除する場合は、下水道法と条例に基づいて除害施設や必要な措置が必要になる。レポートでは「公共用水域向けの排水規制」と「公共下水道向けの除害規制」を分けて説明した方が誤解が少ない。  
  URL: [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)

## 米国の論点

### 4) OSHA Chromium(VI)

- OSHA の現行 Chromium(VI) 標準は `29 CFR 1910.1026` で、`5 µg/m³` の `8-hour TWA` を PEL としている。  
  URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
- OSHA は、`chromium (VI)` を癌、眼刺激、皮膚感作のハザードとして扱い、化学品の危険有害性情報、ラベル、SDS、教育訓練を要求している。  
  URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)

### 5) EPA の電気めっき/クロム規則

- EPA の電気めっき排水ガイドラインは、`1974` 制定の `40 CFR Part 413` を基礎にしつつ、現行の `40 CFR Part 433` と合わせて、間接排出・直接排出の区別を持っている。  
  URL: [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines)
- EPA は、`chrome finishing facilities` が PFAS 排出の主な供給源になりうるとして、`chromium plating`、`chromium anodizing`、`chromic acid etching`、`chromate conversion coating` を個別に追跡している。  
  URL: [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
- EPA の 2022 年提案資料では、`chrome plating` を含む製造工程や、`wetting agent / fume suppressant` を使う plating process が PFAS の発生源として列挙されている。  
  URL: [EPA proposed CERCLA PFOS/PFOA rule](https://www.epa.gov/system/files/documents/2022-08/FRL%207204-02-OLEM%20_%20Designating%20PFOA%20and%20PFOS%20as%20HSs%20_NPRM_20220823.pdf)

### 6) PFAS とクロム工程

- EPA は chrome plating 施設 11 か所の fume suppressants と effluent を分析し、現在使用されている一部の抑制剤に PFAS が含まれているかを確認している。`PFOS-free` 製品でも、過去世代の抑制剤の残留が疑われるケースがある。  
  URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants)
- これを受けて、レポートでは「PFAS はクロムめっきそのものの規制物質ではないが、フューム抑制剤・湿潤剤として工程に入りやすく、排水と残留の論点が結びつく」と整理すると分かりやすい。  
  URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants)

## EU の論点

### 7) RoHS

- EU RoHS は、電気電子機器での `hexavalent chromium` の使用を含む `10 substances` を制限している。  
  URL: [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en)
- ECHA の RoHS 制限一覧では、hexavalent chromium の homogeneous material limit が `0.1 % w/w` とされている。  
  URL: [ECHA RoHS restricted substances](https://echa.europa.eu/en/restricted-subs-referred-art-4-rohs/-/legislationlist/substance/)

### 8) REACH Annex XVII の nickel release

- REACH Annex XVII の nickel 規制は、ピアス用 post assembly で `0.2 µg/cm²/week` 未満、皮膚と直接・長時間接触する製品で `0.5 µg/cm²/week` 以下を求める。  
  URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
- 製品の non-nickel coating についても、少なくとも `2 years` の通常使用で `0.5 µg/cm²/week` を超えないことが必要で、めっき品質や皮膚接触用途の設計条件に直結する。  
  URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)

## report に入れるべき regulatory / temporal claims

1. `2022-04-01` に、日本の公共用水域・地下水の六価クロム環境基準は `0.05 mg/L` から `0.02 mg/L` へ改正された。  
   URL: [環境省 2022-04-01 告示](https://www.env.go.jp/press/110052.html)
2. `2024-02-05` に、六価クロム化合物の測定方法が `JIS K0102-3` ベースへ見直され、`JIS K0102-3 24.3.3` のフレーム原子吸光分析法は公定法から除外された。  
   URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
3. `2024-04-01` 施行のため、2024 年以降の六価クロムの分析・適合判断は、改正後の方法で整理する必要がある。  
   URL: [環境省 2024-02-05 公布](https://www.env.go.jp/press/press_02720.html)
4. 日本の一般排水基準では、六価クロム化合物は `0.2 mg Cr(VI)/L` である。  
   URL: [環境省 一般排水基準](https://www.env.go.jp/water/impure/haisui.html)
5. `2024-12-11` 時点で、暫定排水基準が残るのは亜鉛の電気めっき業のみで、`4 mg/L` が `2029-12-10` まで延長された。  
   URL: [環境省 2024-12-11 暫定基準延長](https://www.env.go.jp/press/press_03960.html)
6. 公共用水域への排出は水質汚濁防止法の排水規制で、排水基準は排水口で適用される。  
   URL: [環境省 水濁法施行通達](https://www.env.go.jp/hourei/05/000137.html)
7. 公共下水道へ排除する場合は、下水道法と条例に基づく除害施設・必要な措置が別途必要である。  
   URL: [国交省 除害施設](https://www.mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html)
8. OSHA の Chromium(VI) 標準は `5 µg/m³` の `8-hour TWA` を PEL とし、職場の規制区域・工学的対策・医療監視・危険有害性コミュニケーションを要求する。  
   URL: [OSHA 29 CFR 1910.1026](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1026)
9. EPA は `40 CFR Part 413` と `Part 433` の電気めっき/金属仕上げ排水規則を見直しており、クロム仕上げ施設を PFAS 排出源として追跡している。  
   URL: [EPA Electroplating Effluent Guidelines](https://www.epa.gov/eg/electroplating-effluent-guidelines) / [EPA Chromium Finishing Questionnaire](https://www.epa.gov/eg/chromium-finishing-questionnaire)
10. EU RoHS は hexavalent chromium を制限対象に含み、ECHA では homogeneous material の上限が `0.1 % w/w` と整理されている。  
    URL: [European Commission RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en) / [ECHA RoHS restricted substances](https://echa.europa.eu/en/restricted-subs-referred-art-4-rohs/-/legislationlist/substance/)
11. REACH Annex XVII の nickel release 条件は、`0.2 µg/cm²/week` と `0.5 µg/cm²/week` の 2 段階で、皮膚接触製品のめっき仕様に直接影響する。  
    URL: [ECHA Annex XVII conditions](https://echa.europa.eu/documents/10162/3bbe9024-52a6-8e63-5581-e686331eb459)
12. PFAS は chrome plating 工程の fume suppressant と結びつきやすく、EPA も chrome plating 施設での PFAS 使用・排出を調査対象としている。  
    URL: [EPA PFAS in fume suppressants](https://www.epa.gov/research-states/epa-research-partner-support-story-sampling-and-analysis-pfas-fume-suppressants) / [EPA proposed CERCLA PFOS/PFOA rule](https://www.epa.gov/system/files/documents/2022-08/FRL%207204-02-OLEM%20_%20Designating%20PFOA%20and%20PFOS%20as%20HSs%20_NPRM_20220823.pdf)

