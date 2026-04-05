/**
 * 学習問題アプリ - メインロジック
 *
 * データ: questions.json (同ディレクトリ)
 * ストレージ: localStorage (history, bookmarks, progress)
 */

'use strict';

// ===== 定数 =====
const STORAGE_KEY = 'quiz_app_v1';
let viewportHeightRaf = 0;
let layoutMetricsRaf = 0;

// ===== 状態管理 =====
let state = {
  data: null,           // questions.json の中身
  questions: [],        // 現在のセッションの問題リスト
  current: 0,           // 現在の問題インデックス
  answered: false,      // 現在の問題を回答済みか
  selectedIdx: null,    // 選択した選択肢インデックス
  session: {            // セッション結果
    correct: 0,
    wrong: 0,
    total: 0,
    answers: [],        // { qid, selected, correct, isCorrect }
  },
  mode: 'all',          // all | chapter | bookmarks | wrong
  chapterId: null,      // chapter モード時
  screen: 'home',       // home | mode | chapter_list | quiz | result | info
};

// ===== ストレージ =====
function loadStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : { history: {}, bookmarks: new Set() };
  } catch {
    return { history: {}, bookmarks: new Set() };
  }
}

function saveStorage(data) {
  try {
    // Set は JSON.stringify できないので配列に変換
    const toSave = {
      ...data,
      bookmarks: [...(data.bookmarks || [])]
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
  } catch (e) {
    console.error('save failed', e);
  }
}

let store = loadStorage();
// bookmarks を Set に復元
if (Array.isArray(store.bookmarks)) {
  store.bookmarks = new Set(store.bookmarks);
}

// ===== データ読み込み =====
async function loadData() {
  // questions.json を fetch で取得
  // ローカルファイルで開いた場合は fetch が失敗するので組み込みデモデータにフォールバック
  try {
    const res = await fetch('questions.json');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();
    return json;
  } catch (e) {
    console.warn('questions.json を読み込めませんでした。デモデータを使います:', e.message);
    return getBuiltinDemoData();
  }
}

function getBuiltinDemoData() {
  return {
    meta: {
      title: "学習問題集 (デモ)",
      version: "1.0",
      total_questions: 3
    },
    questions: [
      {
        id: "demo_001",
        chapter: "デモ問題",
        text: "これはデモ問題です。正しい選択肢を選んでください。\n\n実際の問題は questions.json を編集して追加できます。",
        choices: ["①　選択肢A (正解)", "②　選択肢B", "③　選択肢C", "④　選択肢D"],
        answer: 0,
        explanation: "選択肢Aが正解です。これはデモ用の解説です。",
        needs_review: false
      },
      {
        id: "demo_002",
        chapter: "デモ問題",
        text: "2問目のデモ問題です。どれが正しいでしょうか？",
        choices: ["①　誤りの選択肢", "②　これが正解", "③　誤りの選択肢", "④　誤りの選択肢"],
        answer: 1,
        explanation: "②が正解です。デモ用の解説テキストです。",
        needs_review: false
      },
      {
        id: "demo_003",
        chapter: "デモ問題",
        text: "3問目のデモ問題です。\n\nPWAとして使うには HTTP サーバーで配信してください。\nローカルファイルでも動作します。",
        choices: ["①　選択肢A", "②　選択肢B", "③　選択肢C (正解)", "④　選択肢D", "⑤　選択肢E"],
        answer: 2,
        explanation: "③が正解です。",
        needs_review: false
      }
    ]
  };
}

// ===== ユーティリティ =====
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function getChapters() {
  if (!state.data) return [];
  const map = new Map();
  for (const q of state.data.questions) {
    const ch = q.chapter || '未分類';
    if (!map.has(ch)) map.set(ch, { name: ch, total: 0, done: 0, correct: 0 });
    const entry = map.get(ch);
    entry.total++;
    const hist = store.history[q.id];
    if (hist) {
      entry.done++;
      if (hist.correct) entry.correct++;
    }
  }
  return [...map.entries()].map(([id, v]) => ({ id, ...v }));
}

function getQuestionsByMode(mode, chapterId) {
  if (!state.data) return [];
  let qs = state.data.questions;
  if (mode === 'chapter') {
    qs = qs.filter(q => (q.chapter || '未分類') === chapterId);
  } else if (mode === 'bookmarks') {
    qs = qs.filter(q => store.bookmarks.has(q.id));
  } else if (mode === 'wrong') {
    qs = qs.filter(q => {
      const h = store.history[q.id];
      return h && !h.correct;
    });
  } else if (mode === 'unanswered') {
    qs = qs.filter(q => !store.history[q.id]);
  }
  return qs;
}

function getStats() {
  if (!state.data) return { total: 0, done: 0, correct: 0, bookmarks: 0 };
  const qs = state.data.questions;
  let done = 0, correct = 0;
  for (const q of qs) {
    const h = store.history[q.id];
    if (h) { done++; if (h.correct) correct++; }
  }
  return {
    total: qs.length,
    done,
    correct,
    bookmarks: store.bookmarks.size
  };
}

// ===== 画面切り替え =====
function showScreen(name) {
  state.screen = name;
  document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
  const el = document.getElementById(`screen-${name}`);
  if (el) el.classList.add('active');

  // タブバーのアクティブ
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.screen === name);
  });
}

// ===== ホーム画面 =====
function renderHome() {
  const stats = getStats();
  const pct = stats.total ? Math.round(stats.done / stats.total * 100) : 0;

  document.getElementById('stat-total').textContent = stats.total;
  document.getElementById('stat-done').textContent = stats.done;
  document.getElementById('stat-correct').textContent = stats.correct;
  document.getElementById('home-progress-fill').style.width = pct + '%';
  document.getElementById('home-progress-label').textContent =
    `${stats.done}/${stats.total} 問 解答済み (正解率 ${stats.total ? Math.round(stats.correct/stats.total*100) : 0}%)`;
}

// ===== モード選択 =====
function renderMode() {
  // 苦手・ブックマークの件数を更新
  const wrong = getQuestionsByMode('wrong').length;
  const bm = getQuestionsByMode('bookmarks').length;
  const unans = getQuestionsByMode('unanswered').length;

  document.getElementById('mode-wrong-count').textContent = wrong + ' 問';
  document.getElementById('mode-bm-count').textContent = bm + ' 問';
  document.getElementById('mode-unans-count').textContent = unans + ' 問';
}

// ===== 章一覧 =====
function renderChapterList() {
  const container = document.getElementById('chapter-list');
  container.innerHTML = '';
  const chapters = getChapters();

  if (!chapters.length) {
    container.innerHTML = `<div class="empty-state">
      <p>問題データが読み込まれていません</p>
    </div>`;
    return;
  }

  for (const ch of chapters) {
    const pct = ch.total ? Math.round(ch.done / ch.total * 100) : 0;
    const div = document.createElement('div');
    div.className = 'chapter-item';
    div.innerHTML = `
      <div class="chapter-header" data-chapter="${ch.id}">
        <div>
          <div class="chapter-name">${escHtml(ch.name)}</div>
          <div class="chapter-meta">
            <span>${ch.done}/${ch.total} 問</span>
            <span>${pct}% 解答</span>
          </div>
        </div>
        <span class="badge badge-blue">${ch.total}</span>
      </div>
      <div class="progress-wrap" style="padding:0 12px 12px">
        <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
      </div>
    `;
    div.querySelector('.chapter-header').addEventListener('click', () => {
      startQuiz('chapter', ch.id);
    });
    container.appendChild(div);
  }
}

// ===== クイズ開始 =====
function startQuiz(mode, chapterId, shuffle_ = false) {
  let qs = getQuestionsByMode(mode, chapterId);
  if (!qs.length) {
    alert('この条件に一致する問題がありません');
    return;
  }
  if (shuffle_) qs = shuffle(qs);

  state.mode = mode;
  state.chapterId = chapterId;
  state.questions = qs;
  state.current = 0;
  state.session = { correct: 0, wrong: 0, total: qs.length, answers: [] };

  showScreen('quiz');
  renderQuestion();
  scheduleLayoutMetrics();
}

// ===== 問題表示 =====
function renderQuestion() {
  const q = state.questions[state.current];
  if (!q) { showResult(); return; }

  state.answered = false;
  state.selectedIdx = null;

  const total = state.questions.length;
  const cur = state.current + 1;
  const pct = Math.round((state.current) / total * 100);

  document.getElementById('quiz-progress-fill').style.width = pct + '%';
  document.getElementById('quiz-progress-label').textContent = `${cur} / ${total} 問`;
  document.getElementById('quiz-chapter').textContent = q.chapter || '';
  document.getElementById('quiz-qnum').textContent = `問題 ${cur}`;

  // 苦手マーク
  const starBtn = document.getElementById('star-btn');
  starBtn.textContent = store.bookmarks.has(q.id) ? '⭐' : '☆';
  starBtn.onclick = () => toggleBookmark(q.id);

  // 問題文
  document.getElementById('question-text').textContent = q.text || '';

  // needs_review バッジ
  const badge = document.getElementById('review-badge');
  if (q.needs_review) {
    badge.style.display = 'inline';
  } else {
    badge.style.display = 'none';
  }

  // 選択肢
  const choicesEl = document.getElementById('choices-list');
  choicesEl.innerHTML = '';
  const choices = q.choices || [];
  for (let i = 0; i < choices.length; i++) {
    const btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.innerHTML = `<span class="choice-num">${numLabel(i)}</span><span>${escHtml(choices[i])}</span>`;
    btn.addEventListener('click', () => selectChoice(i));
    choicesEl.appendChild(btn);
  }

  // 判定パネル非表示
  document.getElementById('result-panel').style.display = 'none';

  // フッターボタン
  document.getElementById('btn-submit').style.display = 'inline-flex';
  document.getElementById('btn-submit').disabled = true;
  document.getElementById('btn-next').style.display = 'none';

  // モバイルでは前問のスクロール位置が残ると選択肢が見切れやすいので、
  // 新しい問題を出すたびに必ず先頭へ戻す。
  const quizContent = document.getElementById('quiz-content');
  if (quizContent) {
    quizContent.scrollTop = 0;
  }

  scheduleLayoutMetrics();
}

function numLabel(i) {
  const labels = ['①', '②', '③', '④', '⑤', '⑥'];
  return labels[i] || (i + 1) + '.';
}

function escHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// ===== 選択肢選択 =====
function selectChoice(idx) {
  if (state.answered) return;
  state.selectedIdx = idx;

  document.querySelectorAll('.choice-btn').forEach((btn, i) => {
    btn.classList.toggle('selected', i === idx);
  });

  document.getElementById('btn-submit').disabled = false;
}

// ===== 回答提出 =====
function submitAnswer() {
  if (state.selectedIdx === null) return;
  if (state.answered) return;
  state.answered = true;

  const q = state.questions[state.current];
  const selected = state.selectedIdx;
  const correct = q.answer; // 0始まりのインデックス (null なら未設定)
  const isCorrect = correct !== null && correct !== undefined
    ? selected === correct
    : null; // null = 答え未設定

  // 選択肢の色付け
  document.querySelectorAll('.choice-btn').forEach((btn, i) => {
    btn.disabled = true;
    btn.classList.remove('selected');
    if (correct !== null && i === correct) btn.classList.add('correct');
    if (i === selected && !isCorrect) btn.classList.add('wrong');
    if (i === selected && isCorrect) btn.classList.add('correct');
  });

  // 判定パネル表示
  const panel = document.getElementById('result-panel');
  panel.style.display = 'block';

  let labelText = '回答しました';
  let panelClass = 'result-panel';

  if (isCorrect === true) {
    labelText = '✓ 正解！';
    panelClass = 'result-panel correct';
    state.session.correct++;
  } else if (isCorrect === false) {
    labelText = '✗ 不正解';
    panelClass = 'result-panel wrong';
    state.session.wrong++;
    // 正解を表示
    if (correct !== null && q.choices) {
      document.getElementById('correct-answer-text').textContent =
        `正解: ${numLabel(correct)} ${q.choices[correct] || ''}`;
      document.getElementById('correct-answer-text').style.display = 'block';
    }
  } else {
    // 答え未設定
    labelText = '回答済み (正解未設定)';
    document.getElementById('correct-answer-text').textContent =
      '※ この問題の正解はまだ設定されていません (questions.json を編集してください)';
    document.getElementById('correct-answer-text').style.display = 'block';
  }

  panel.className = panelClass;
  document.getElementById('result-label').textContent = labelText;
  document.getElementById('explanation-text').textContent = q.explanation || '';

  if (isCorrect === null) {
    document.getElementById('correct-answer-text').style.display = 'block';
  }

  // 履歴保存
  if (isCorrect !== null) {
    store.history[q.id] = {
      correct: isCorrect,
      ts: Date.now(),
      selected
    };
    saveStorage(store);
  }

  // セッション記録
  state.session.answers.push({ qid: q.id, selected, correct, isCorrect });

  // ボタン切り替え
  document.getElementById('btn-submit').style.display = 'none';
  document.getElementById('btn-next').style.display = 'inline-flex';

  const isLast = state.current >= state.questions.length - 1;
  document.getElementById('btn-next').textContent = isLast ? '結果を見る' : '次の問題 →';
}

// ===== 次へ =====
function nextQuestion() {
  if (state.current < state.questions.length - 1) {
    state.current++;
    renderQuestion();
    // スクロールをトップに戻す
    document.getElementById('quiz-content').scrollTop = 0;
    scheduleLayoutMetrics();
  } else {
    showResult();
  }
}

// ===== 結果画面 =====
function showResult() {
  const { correct, total, answers } = state.session;
  const pct = total ? Math.round(correct / total * 100) : 0;

  document.getElementById('score-number').textContent = correct;
  document.getElementById('score-denom').textContent = `/ ${total} 問`;
  document.getElementById('result-pct').textContent = `正解率 ${pct}%`;
  document.getElementById('result-msg').textContent = resultMessage(pct);

  showScreen('result');
}

function resultMessage(pct) {
  if (pct >= 90) return '素晴らしい！完璧に近いです 🎉';
  if (pct >= 70) return 'よくできました！もう少しで完璧 💪';
  if (pct >= 50) return 'あと少し！復習してもう一度 📚';
  return '復習が必要です。解説を確認しましょう 📖';
}

// ===== ブックマーク =====
function toggleBookmark(qid) {
  if (store.bookmarks.has(qid)) {
    store.bookmarks.delete(qid);
  } else {
    store.bookmarks.add(qid);
  }
  saveStorage(store);

  // アイコン更新
  const starBtn = document.getElementById('star-btn');
  if (starBtn) {
    starBtn.textContent = store.bookmarks.has(qid) ? '⭐' : '☆';
  }
}

// ===== 情報画面 =====
function renderInfo() {
  if (!state.data) return;
  const m = state.data.meta || {};
  const stats = getStats();

  document.getElementById('info-title').textContent = m.title || '不明';
  document.getElementById('info-version').textContent = m.version || '-';
  document.getElementById('info-total').textContent = stats.total;
  document.getElementById('info-done').textContent = stats.done;
  document.getElementById('info-correct').textContent = stats.correct;
  document.getElementById('info-rate').textContent =
    stats.done ? Math.round(stats.correct / stats.done * 100) + '%' : '-';
  document.getElementById('info-bm').textContent = stats.bookmarks;

  const needsReview = state.data.questions.filter(q => q.needs_review).length;
  document.getElementById('info-review').textContent = needsReview;
}

// ===== 履歴クリア =====
function clearHistory() {
  if (!confirm('学習履歴をすべて削除しますか？')) return;
  store.history = {};
  saveStorage(store);
  renderHome();
  renderInfo();
  alert('削除しました');
}

function syncViewportHeight() {
  const viewport = window.visualViewport;
  const height = Math.round((viewport && viewport.height) ? viewport.height : window.innerHeight);
  document.documentElement.style.setProperty('--app-height', `${height}px`);
}

function syncQuizFooterGap() {
  const footer = document.querySelector('.quiz-footer');
  const footerHeight = footer ? Math.ceil(footer.getBoundingClientRect().height) : 0;
  const gap = Math.max(160, footerHeight + 24);
  document.documentElement.style.setProperty('--quiz-footer-gap', `${gap}px`);
}

function scheduleLayoutMetrics() {
  if (layoutMetricsRaf) {
    cancelAnimationFrame(layoutMetricsRaf);
  }
  layoutMetricsRaf = requestAnimationFrame(() => {
    syncViewportHeight();
    syncQuizFooterGap();
    layoutMetricsRaf = 0;
  });
}

function bindViewportHeight() {
  const schedule = () => {
    if (viewportHeightRaf) {
      cancelAnimationFrame(viewportHeightRaf);
    }
    viewportHeightRaf = requestAnimationFrame(() => {
      scheduleLayoutMetrics();
      viewportHeightRaf = 0;
    });
  };

  scheduleLayoutMetrics();
  window.addEventListener('resize', schedule, { passive: true });
  window.addEventListener('orientationchange', schedule, { passive: true });
  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', schedule, { passive: true });
    window.visualViewport.addEventListener('scroll', schedule, { passive: true });
  }
}

// ===== イベントバインド =====
function bindEvents() {
  // タブバー
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const s = btn.dataset.screen;
      if (s === 'home') { renderHome(); showScreen('home'); }
      else if (s === 'mode') { renderMode(); showScreen('mode'); }
      else if (s === 'chapters') { renderChapterList(); showScreen('chapter_list'); }
      else if (s === 'info') { renderInfo(); showScreen('info'); }
    });
  });

  // ホーム: すべての問題を開始
  document.getElementById('btn-start-all').addEventListener('click', () => {
    startQuiz('all', null);
  });

  // ホーム: シャッフル
  document.getElementById('btn-start-shuffle').addEventListener('click', () => {
    startQuiz('all', null, true);
  });

  // モード選択カード
  document.getElementById('mode-all').addEventListener('click', () => startQuiz('all', null));
  document.getElementById('mode-shuffle').addEventListener('click', () => startQuiz('all', null, true));
  document.getElementById('mode-wrong').addEventListener('click', () => startQuiz('wrong'));
  document.getElementById('mode-bookmarks').addEventListener('click', () => startQuiz('bookmarks'));
  document.getElementById('mode-unanswered').addEventListener('click', () => startQuiz('unanswered'));
  document.getElementById('mode-chapters').addEventListener('click', () => {
    renderChapterList();
    showScreen('chapter_list');
  });

  // 回答提出
  document.getElementById('btn-submit').addEventListener('click', submitAnswer);

  // 次の問題
  document.getElementById('btn-next').addEventListener('click', nextQuestion);

  // クイズ中の戻るボタン
  document.getElementById('quiz-back').addEventListener('click', () => {
    if (confirm('中断して戻りますか？（現在の進捗は保存されません）')) {
      renderHome();
      showScreen('home');
    }
  });

  // 結果画面: もう一度
  document.getElementById('btn-retry').addEventListener('click', () => {
    startQuiz(state.mode, state.chapterId);
  });

  // 結果画面: シャッフルでもう一度
  document.getElementById('btn-retry-shuffle').addEventListener('click', () => {
    startQuiz(state.mode, state.chapterId, true);
  });

  // 結果画面: ホームへ
  document.getElementById('btn-home').addEventListener('click', () => {
    renderHome();
    showScreen('home');
  });

  // 履歴クリア
  document.getElementById('btn-clear-history').addEventListener('click', clearHistory);
}

// ===== 起動 =====
async function init() {
  // ローディング表示
  document.getElementById('loading').style.display = 'flex';
  bindViewportHeight();

  try {
    state.data = await loadData();
  } catch (e) {
    console.error('初期化エラー:', e);
    state.data = getBuiltinDemoData();
  }

  document.getElementById('loading').style.display = 'none';

  bindEvents();
  renderHome();
  showScreen('home');
  scheduleLayoutMetrics();

  // タイトル設定
  const title = state.data?.meta?.title || '学習問題集';
  document.title = title;
  document.getElementById('app-title').textContent = title;
}

document.addEventListener('DOMContentLoaded', init);
