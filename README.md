# Adaptive Topic Learning App

`nanoin.html` は、単一テーマの説明ページではなく、`content.js` の topic 定義を差し替えて再利用できる学習アプリとして構成しています。現状は `ナノインデンター` と `蛍光X線分析装置` の 2 テーマを持っています。

## 現在の設計方針

- 中核は `nanoin-app/content.js` の topic schema
- UI 本体は `nanoin-app/app.js` が schema を読んで描画
- AI は `nanoin-app/ai.js` で adapter を分離
- 動画は必須ではなく、任意メディアとして topic 定義へぶら下げる
- 保存状態は topic ごとに `localStorage` を分離
- URL パラメータまたは UI ボタンで topic を切り替えられる

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

## GitHub Pages 公開

この repo には GitHub Pages 用の workflow を追加してあります。

- [pages.yml](/Users/7522857/Documents/Playground/.github/workflows/pages.yml)
- [index.html](/Users/7522857/Documents/Playground/index.html)

公開までの最短手順:

1. GitHub で空の repository を作る
2. このフォルダで remote を追加する
3. `master` を push する
4. GitHub の `Settings > Pages` で `Source: GitHub Actions` を選ぶ
5. Actions の `Deploy GitHub Pages` が通れば、`https://<user>.github.io/<repo>/` で見られる

PowerShell 例:

```powershell
cd C:\Users\7522857\Documents\Playground
git add .
git commit -m "Set up schema-driven learning app and GitHub Pages deploy"
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin master
```

公開URLの例:

- `https://<user>.github.io/<repo>/`
- `https://<user>.github.io/<repo>/?topic=nanoin`
- `https://<user>.github.io/<repo>/?topic=xrf`

`index.html` から `nanoin.html` へリダイレクトするので、トップURLでもそのまま開けます。

## 家PCで編集する方法

できます。基本は GitHub に push して、家PCで clone / pull するだけです。

家PCの初回:

```powershell
git clone https://github.com/<user>/<repo>.git
cd <repo>
```

家PCで更新を取り込む:

```powershell
git pull
```

家PCで編集して戻す:

```powershell
git add .
git commit -m "Update content"
git push
```

会社PCへ戻したら:

```powershell
git pull
```

同じファイルを両方のPCで同時に触ると競合は起きるので、編集前に毎回 `git pull` は入れた方が安全です。

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

- `id`, `name`, `pageTitle`
- `hero`
- `introSummaryStates`
- `introCards`, `selfCheck`, `concepts`
- `figureCards`, `conceptSupplements`
- `visualModels`
- `visualLearning`
- `diagnosisQuestions`
- `diagnosisUi`
- `ai.systemInstruction`, `ai.suggestedPaths`, `ai.localTopics`, `ai.explanationRubric`, `ai.ui`
- `masteryQuiz`
- `media.featuredVideo`, `media.resources`
- `defaults`

`defaults` には、初期表示セクション、初期概念、図解パラメータ、AI 初期文言、API モデルなどを持たせています。
`visualLearning.buildScenario` を持たせると、topic ごとに図解用の数値モデルとチャートデータを差し替えられます。

## 主要コンポーネント

- `nanoin-app/content.js`
  - topic 定義
  - topic ごとの初期値
  - セルフチェック後の導線文言
  - AI 指示文
  - 図カードと概念補助図
  - 図解UIのラベル、スライダー定義、インサイト生成
  - 任意メディア定義
- `nanoin-app/storage.js`
  - topic ごとの保存キー生成
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
- `index.html` から `nanoin.html` へ自動遷移する
- リロード後も進捗が保持される
- `保存データを初期化する` で topic の状態だけ消える
- AI キー未設定でもローカル応答が返る
- `media.featuredVideo` が `null` でも UI が崩れない
- KLA リンク一覧だけでも導入画面が成立する

## 次の拡張ポイント

- `media.featuredVideo` に YouTube またはローカル動画を差し込む
- 診断サマリー文や AI 接続説明など、残る topic 固有文言をさらに `content.js` 側へ寄せる
- topic 一覧を `content.js` 以外の JSON へ分離し、テーマ追加をデータ更新だけで回せる形にする
