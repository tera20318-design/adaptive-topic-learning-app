# Contradiction Log

## Confirmed Contradictions

- 一般的な説明では「めっき」は外観処理の印象が強いが、今回の一次情報では防食、導電、接触、はんだ付け性、拡散バリアなど機能付与用途が主流として現れる。  
  Sources: `sfj.or.jp`, `Nickel Institute`, `JEITA`, `IPC`
- 「六価クロムに暫定排水基準がある」という理解は今回の一次情報では確認できず、2024-12-11 時点で暫定排水基準が延長されたのは亜鉛の電気めっき業のみ。  
  Sources: `env.go.jp/press/press_03960.html`, `env.go.jp/water/impure/haisui.html`
- IPC の microvia reliability warning は PCB/HDI の microvia-to-target plating reliability 文脈であり、電子用途全般のめっき一般に広げると過大一般化になる。  
  Sources: `ipc.org/news-release/ipc-issues-electronics-industry-warning-printed-board-microvia-reliability-high`, `ipc.org/news-release/ipc-releases-ipc-6012f-qualification-and-performance-specification-rigid-printed`

## Negative Evidence

- 公共用水域向けの一般排水基準ページでは六価クロム `0.2 mg/L` が確認できるが、下水道受入れを同じ数値で一律に説明する根拠は見当たらない。下水道側は別途排除基準・除害施設の整理が必要。  
  Sources: `env.go.jp/water/impure/haisui.html`, `mlit.go.jp/mizukokudo/sewerage/mizukokudo_sewerage_tk_000637.html`
- vendor/industry 資料だけでは、個別製品に対する膜厚、ベーキング条件、合否判定を一般化する根拠としては不足する。標準や顧客規格の確認が必要。  
  Sources: `jcu-i.com`, `ipc.org`, `ASTM scope pages`

## Interpretation

- report では、規制の数値と日付は必ず official / legal source に寄せる。
- vendor / industry association 由来の説明は「公開資料の範囲では」「代表例として」で弱める。
- 方式比較、用途比較、規制比較を同じ表で一律化せず、適用範囲と判断場面を分ける。
