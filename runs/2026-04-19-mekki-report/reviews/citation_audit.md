# Citation Audit

## Coverage Check

| Section | Key claim or sentence | Source IDs present | Audit result | Fix needed |
| --- | --- | --- | --- | --- |
| Executive Summary | めっきは表面機能を与える技術群であり、単なる装飾ではない | SRC-001, SRC-002, SRC-003 | Pass | None |
| Executive Summary | 方式、前後工程、品質評価、安全管理を組み合わせて成立する | SRC-003, SRC-004, SRC-014, SRC-016 | Pass | None |
| Question 1 | めっきの定義と広義・狭義の注記 | SRC-001, SRC-002, SRC-014 | Pass | 本稿が湿式めっき中心である旨を最終稿でも維持する |
| Question 2 | 電気めっきと無電解めっきの比較 | SRC-004, SRC-013, SRC-014, SRC-015 | Pass with caveat | 電気めっきの優位性は条件依存と明記する |
| Question 2 | 前処理が品質の土台になる | SRC-014, SRC-016 | Pass | None |
| Question 2 | 代表金属と用途の一覧 | SRC-003, SRC-012, SRC-013 | Pass | Ag の例は代表例であり網羅表現にしない |
| Question 3 | 薬品管理と安全衛生の基本 | SRC-008, SRC-017 | Pass | 日本国内の義務詳細は個別確認注記を維持する |
| Question 3 | 六価クロムの一般排水基準 0.2 mg/L と電気めっき業の暫定 0.5 mg/L | SRC-018, SRC-019 | Pass with caveat | 公共用水域排出と下水道接続の文脈差を明示する |
| Question 3 | 品質評価は膜厚だけでは足りない | SRC-020 | Partial but acceptable | 「実務では」の限定を維持し、一般法則化しない |
| Limitations | 規制記述は 2026-04-19 時点 | SRC-018, SRC-019 | Pass | None |

## Missing Citations

| Location | Why it needs a citation | Proposed source IDs | Status |
| --- | --- | --- | --- |
| Draft V1 / Key Findings 2 | 「制御性、コストで有利な場面が多い」は比較評価のため、古い単独レビュー依存と分かる形が望ましい | SRC-004 | Resolved in Draft V2 / Final Report with softer wording |
| Draft V1 / Evidence-Based Analysis Q2 caveat | 「装飾めっきと機能めっきは完全な二分法ではない」は分類論なので、本文では SRC-011, SRC-012 を残す | SRC-011, SRC-012 | Covered |
| Draft V1 / Recommendation Draft | 「規制や安全は後付けではなく初期条件」は推論を含む助言なので、事実主張と区別して書く | SRC-017, SRC-018, SRC-019 | Resolved in Draft V2 / Final Report as practical advice |

## Risk Notes

- Time-sensitive facts to re-check:
  - 六価クロム化合物の一般排水基準 0.2 mg/L の施行以後に追加改正がないか
  - 電気めっき業の暫定基準 0.5 mg/L の適用期間や延長有無
  - 下水排除基準の自治体運用差と更新時期
- Claims that still rely on weak sourcing:
  - 電気めっきの「制御性・浴安定性・コスト優位」は SRC-004 依存でやや古い
  - 品質評価の代表軸は SRC-020 が試験サービス紹介なので、最終稿では代表例として扱う
  - 銀めっきの装飾用途と機能用途の橋渡しは SRC-003 がイベント概要であるため、過度に膨らませない
