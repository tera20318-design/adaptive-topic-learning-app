# Adaptive Topic Learning App

`nanoin.html` は、単一テーマの説明ページではなく、`content.js` の topic 定義を差し替えて再利用できる学習アプリとして構成しています。現状は `ナノインデンター` と `蛍光X線分析装置` の 2 テーマを持っています。

## 現在の設計方針

- 中核は `nanoin-app/content.js` の topic schema
- UI 本体は `nanoin-app/app.js` が schema を読んで描画
- AI は `nanoin-app/ai.js` で adapter を分離
- 動画は必須ではなく、任意メディアとして topic 定義へぶら下げる
- 保存状態は topic ごとに `localStorage` を分離
- URL パラメータで topic を切り替えられる

## 起動方法

### 最小手順

1. `nanoin.html` をブラウザで開く

### 推奨手順

PowerShell 例:

```powershell
cd C:\Users\7522857\Documents\Playground
python -m http.server 8000
```

その後、`http://localhost:8000/nanoin.html` を開きます。

別 topic を直接開く例:

- `http://localhost:8000/nanoin.html?topic=nanoin`
- `http://localhost:8000/nanoin.html?topic=xrf`

## 画面構成

1. 学習導入
2. 概念地図
3. 図解
4. 誤解診断
5. AI対話
6. 理解確認
7. 学習記録

## ファイル構成

```text
nanoin.html
manifest.webmanifest
nanoin-app/
  app.js
  ai.js
  content.js
  storage.js
  styles.css
```

## topic schema の役割

`nanoin-app/content.js` では、少なくとも次を topic 単位で持てます。

- `id`, `name`
- `hero`
- `introCards`, `selfCheck`, `concepts`
- `visualModels`
- `diagnosisQuestions`
- `ai.suggestedPaths`, `ai.localTopics`, `ai.explanationRubric`
- `masteryQuiz`
- `media.featuredVideo`, `media.resources`

## 主要コンポーネント

- `nanoin-app/content.js`
  - topic 定義
  - 導入カード
  - 診断、クイズ、AI fallback の内容
  - 任意メディア定義
- `nanoin-app/storage.js`
  - 保存 / 復元 / 初期化
- `nanoin-app/ai.js`
  - `LocalAIAdapter`
  - `GeminiAdapter`
  - `AIService`
- `nanoin-app/app.js`
  - schema 読み込み
  - topic 切り替え UI
  - 描画
  - イベント処理
  - Chart.js 更新
- `nanoin-app/styles.css`
  - UI テーマ

## AI 差し替えポイント

差し替え対象は主に `nanoin-app/ai.js` です。

- API なしでも `LocalAIAdapter` で最低限動作
- 外部呼び出しは現状 `GeminiAdapter`
- topic ごとの指示文は `content.js` 側で定義

OpenAI など別の LLM を使う場合は、adapter を追加し、`AIService.respond()` の選択ロジックを広げれば UI 側はそのまま流用できます。

## 動作確認ポイント

- `nanoin.html` を開いて 7 画面を移動できる
- リロード後も進捗が保持される
- `保存データを初期化する` で状態が消える
- AI キー未設定でもローカル応答が返る
- `media.featuredVideo` が `null` でも UI が崩れない
- KLA リンク一覧だけでも導入画面が成立する

## 次の拡張ポイント

- `media.featuredVideo` に YouTube またはローカル動画を差し込む
- 概念補助図や図解ラベルも topic データへ寄せる
- topic 一覧を `content.js` 以外の JSON へ分離し、テーマ追加をデータ更新だけで回せる形にする
