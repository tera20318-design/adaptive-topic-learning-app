(function () {
    const content = window.NanoLearnContent || {};
    const meta = content.meta || {};
    const TOPICS = content.topics || {};
    const TOPIC_LIST = Object.values(TOPICS);
    const topicId = content.defaultTopicId || "nanoin";
    const topic = (content.topics && content.topics[topicId]) || content.topic || {};
    const topicName = topic.name || "学習テーマ";
    const APP_SECTIONS = content.sections || content.APP_SECTIONS || [];
    const HERO = topic.hero || {};
    const INTRO_OVERVIEW_CARDS = topic.introCards || [];
    const INTRO_SUMMARY_STATES = topic.introSummaryStates || {};
    const INTRO_SELF_CHECK = topic.selfCheck || content.INTRO_SELF_CHECK || [];
    const FIGURE_CARDS = topic.figureCards || content.FIGURE_CARDS || [];
    const CONCEPTS = topic.concepts || content.CONCEPTS || [];
    const CONCEPT_SUPPLEMENTS = topic.conceptSupplements || content.CONCEPT_SUPPLEMENTS || {};
    const VISUAL_MODELS = topic.visualModels || content.VISUAL_MODELS || {};
    const VISUAL_LEARNING = topic.visualLearning || {};
    const DIAGNOSIS_QUESTIONS = topic.diagnosisQuestions || content.DIAGNOSIS_QUESTIONS || {};
    const DIAGNOSIS_UI = topic.diagnosisUi || {};
    const AI_SUGGESTED_PATHS = (topic.ai && topic.ai.suggestedPaths) || content.AI_SUGGESTED_PATHS || [];
    const EXPLANATION_RUBRIC = (topic.ai && topic.ai.explanationRubric) || content.EXPLANATION_RUBRIC || [];
    const AI_UI = (topic.ai && topic.ai.ui) || {};
    const MASTERY_QUIZ = topic.masteryQuiz || content.MASTERY_QUIZ || [];
    const MEDIA = topic.media || { featuredVideo: null, resources: [] };
    const { loadState, saveState, resetState } = window.NanoLearnStorage;
    const { AIService } = window.NanoLearnAI;

    const root = document.getElementById("app");
    const aiService = new AIService();
    let state = loadState();
    let chart = null;

    const conceptMap = Object.fromEntries(CONCEPTS.map((concept) => [concept.id, concept]));
    const sectionIndex = Object.fromEntries(APP_SECTIONS.map((section, index) => [section.id, index]));

    document.title = topic.pageTitle || meta.pageTitle || `${topicName}学習アプリ`;

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function formatTextBlock(text) {
        return escapeHtml(text)
            .split(/\n{2,}/)
            .map((paragraph) => `<p class="leading-7">${paragraph.replace(/\n/g, "<br>")}</p>`)
            .join("");
    }

    function metricToneClass(tone) {
        if (tone === "高") {
            return "text-amber-700";
        }
        if (tone === "中") {
            return "text-sky-700";
        }
        return "text-emerald-700";
    }

    function persist() {
        saveState(state);
    }

    function visitSection(sectionId) {
        state.currentSection = sectionId;
        if (!state.visitedSections.includes(sectionId)) {
            state.visitedSections.push(sectionId);
        }
        persist();
    }

    function progressPercent() {
        const completedByInteraction =
            (Object.keys(state.introCheck).length === INTRO_SELF_CHECK.length ? 1 : 0) +
            (state.diagnosis.complete ? 1 : 0) +
            (state.mastery.result ? 1 : 0);
        const total = APP_SECTIONS.length + 3;
        const done = state.visitedSections.length + completedByInteraction;
        return Math.min(100, Math.round((done / total) * 100));
    }

    function introSummary() {
        const answers = Object.values(state.introCheck);
        if (!answers.length) {
            return INTRO_SUMMARY_STATES.empty || {
                label: "診断待ち",
                text: "最初の 3 問に答えると、どこから入るべきかを案内します。"
            };
        }

        const total = answers.reduce((sum, value) => sum + Number(value), 0);
        if (total <= 1) {
            return INTRO_SUMMARY_STATES.low || {
                label: "導入から着手",
                text: "まずは概念地図と図解で『何を測っているか』の骨格を作る段階です。"
            };
        }
        if (total <= 4) {
            return INTRO_SUMMARY_STATES.medium || {
                label: "誤解の切り分けが効果的",
                text: "概要はつかめています。次は誤解診断で、硬さ・弾性率・深さ依存の混線をほどくと伸びやすいです。"
            };
        }
        return INTRO_SUMMARY_STATES.high || {
            label: "応用理解へ進める",
            text: "基礎用語は入っています。AI 対話や理解確認で、自分の言葉に変換できるかを詰める段階です。"
        };
    }

    function getActiveConcept() {
        return conceptMap[state.activeConceptId] || CONCEPTS[0];
    }

    function isRelatedConcept(targetId) {
        const active = getActiveConcept();
        return active.relations.some((item) => item.target === targetId);
    }

    function getVisualScenario() {
        if (typeof VISUAL_LEARNING.buildScenario === "function") {
            return VISUAL_LEARNING.buildScenario(state.visual, VISUAL_MODELS);
        }
        return {
            metrics: [],
            insights: [],
            chart: {
                type: "scatter",
                datasets: []
            }
        };
    }

    function diagnosisWeakPoints() {
        const counts = {};
        state.diagnosis.history.forEach((entry) => {
            (entry.weakness || []).forEach((tag) => {
                counts[tag] = (counts[tag] || 0) + 1;
            });
        });
        return Object.entries(counts)
            .sort((a, b) => b[1] - a[1])
            .map(([tag]) => conceptMap[tag] ? conceptMap[tag].title : tag);
    }

    function diagnosisSummaryText() {
        const mistakes = state.diagnosis.history.filter((entry) => entry.misconception);
        if (!mistakes.length) {
            return DIAGNOSIS_UI.noMistakesText || "大きな誤解はまだ表面化していません。次は理解確認で、自分の言葉に変換できるかを見ます。";
        }
        return `誤解が出やすかったのは「${mistakes.map((item) => item.label).slice(0, 2).join(" / ")}」周辺です。値の読み方よりも、何と何を混同しやすいかに注意してください。`;
    }

    function diagnosisAccuracy() {
        if (!state.diagnosis.history.length) {
            return 0;
        }
        return Math.round((state.diagnosis.correctCount / state.diagnosis.history.length) * 100);
    }

    function masteryAccuracy() {
        const answered = Object.keys(state.mastery.answers || {}).length;
        if (!answered) {
            return 0;
        }
        const correct = MASTERY_QUIZ.filter((question) => {
            const selected = state.mastery.answers[question.id];
            const choice = question.choices.find((item) => item.id === selected);
            return choice && choice.correct;
        }).length;
        return Math.round((correct / answered) * 100);
    }

    function computeMasteryResult() {
        const answered = Object.keys(state.mastery.answers || {}).length;
        const correct = MASTERY_QUIZ.filter((question) => {
            const selected = state.mastery.answers[question.id];
            const choice = question.choices.find((item) => item.id === selected);
            return choice && choice.correct;
        }).length;
        const missing = MASTERY_QUIZ
            .filter((question) => !state.mastery.answers[question.id])
            .map((question) => question.prompt);
        const weakQuestions = MASTERY_QUIZ
            .filter((question) => {
                const selected = state.mastery.answers[question.id];
                const choice = question.choices.find((item) => item.id === selected);
                return selected && choice && !choice.correct;
            })
            .map((question) => question.prompt);

        let level = "未着手";
        if (answered === MASTERY_QUIZ.length && correct === MASTERY_QUIZ.length) {
            level = "全問正解";
        } else if (correct >= 3) {
            level = "中核は押さえられている";
        } else if (answered > 0) {
            level = "再確認が必要";
        }

        return {
            answered,
            correct,
            accuracy: answered ? Math.round((correct / answered) * 100) : 0,
            missing,
            weakQuestions,
            level
        };
    }

    function renderFigureCards() {
        return `
            <div class="grid gap-4 lg:grid-cols-3">
                ${FIGURE_CARDS.map((card) => `
                    <div class="panel-card p-5">
                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">${escapeHtml(card.label || "")}</div>
                        <div class="mt-3 rounded-3xl bg-slate-50 p-4">
                            ${card.illustration || ""}
                        </div>
                        <div class="mt-3 rounded-2xl bg-slate-50 p-4 text-sm leading-7 text-slate-600">
                            ${(card.bullets || []).map((item) => `
                                <div><span class="font-bold text-slate-900">${escapeHtml(item.label)}:</span> ${escapeHtml(item.body)}</div>
                            `).join("")}
                        </div>
                    </div>
                `).join("")}
            </div>
        `;
    }

    function orderedDiagnosisQuestions() {
        return Object.values(DIAGNOSIS_QUESTIONS);
    }

    function diagnosisEntry(questionId) {
        return state.diagnosis.history.find((entry) => entry.questionId === questionId) || null;
    }

    function renderFeaturedMedia() {
        const featured = MEDIA.featuredVideo;
        if (!featured) {
            return `
                <div class="rounded-[28px] border border-dashed border-slate-300 bg-slate-50 p-5">
                    <div class="text-sm font-bold text-slate-900">${escapeHtml(AI_UI.mediaEmptyTitle || "動画は任意アセットです")}</div>
                    <p class="mt-2 text-sm leading-7 text-slate-600">
                        ${escapeHtml(AI_UI.mediaEmptyBody || "今は外部埋め込みに依存せず、図解と診断を主軸にしています。あとから YouTube かローカル動画を追加しても、この枠をそのまま使えます。")}
                    </p>
                </div>
            `;
        }

        if (featured.type === "youtube") {
            return `
                <div class="overflow-hidden rounded-[28px] border border-slate-200 bg-slate-50">
                    <div class="aspect-video bg-slate-100">
                        <iframe
                            class="h-full w-full"
                            src="${featured.src}"
                            title="${escapeHtml(featured.title)}"
                            loading="lazy"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                    </div>
                </div>
            `;
        }

        if (featured.type === "file") {
            return `
                <div class="overflow-hidden rounded-[28px] border border-slate-200 bg-slate-50 p-3">
                    <video class="aspect-video w-full rounded-[22px] bg-slate-100" controls preload="metadata" ${featured.poster ? `poster="${featured.poster}"` : ""}>
                        <source src="${featured.src}">
                    </video>
                </div>
            `;
        }

        return "";
    }

    function renderMediaSection() {
        return `
            <div class="panel-card p-6 sm:p-8">
                <div class="flex items-center justify-between gap-4">
                    <div>
                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">OPTIONAL MEDIA</div>
                        <h3 class="mt-2 text-2xl font-black">${escapeHtml(MEDIA.title || "参考リソース")}</h3>
                    </div>
                    <div class="tag tag-neutral">差し替え可能な補助教材</div>
                </div>
                <p class="mt-3 text-sm leading-7 text-slate-600">
                    ${escapeHtml(MEDIA.description || "図解と診断を主軸にしつつ、必要なら外部教材や任意動画を足せる構成です。")}
                </p>
                <div class="mt-5">
                    ${renderFeaturedMedia()}
                </div>
                <div class="mt-5 grid gap-5 lg:grid-cols-3">
                    ${(MEDIA.resources || []).map((resource) => `
                        <div class="rounded-[30px] border border-slate-200 bg-white p-4">
                            <div class="rounded-3xl bg-slate-50 p-5">
                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">${escapeHtml(resource.source)}</div>
                                <div class="mt-2 text-lg font-black text-slate-900">${escapeHtml(resource.title)}</div>
                                <p class="mt-3 text-sm leading-7 text-slate-600">${escapeHtml(resource.note)}</p>
                            </div>
                            <a class="mt-4 inline-flex text-sm font-bold text-blue-700" href="${resource.url}" target="_blank" rel="noreferrer">元ページを開く</a>
                        </div>
                    `).join("")}
                </div>
            </div>
        `;
    }

    function renderConceptSupplement(concept) {
        return CONCEPT_SUPPLEMENTS[concept.id] || "";
    }

    function renderHeader() {
        const intro = introSummary();
        return `
            <header class="mx-auto max-w-6xl px-4 pb-6 pt-5 sm:px-6 sm:pt-8">
                ${TOPIC_LIST.length > 1 ? `
                    <div class="mb-4 flex flex-wrap gap-2">
                        ${TOPIC_LIST.map((item) => `
                            <button class="rounded-full px-4 py-2 text-sm font-bold ${item.id === topicId ? "bg-slate-900 text-white" : "border border-slate-300 bg-white text-slate-700"}" data-action="switch-topic" data-topic="${item.id}">
                                ${escapeHtml(item.name)}
                            </button>
                        `).join("")}
                    </div>
                ` : ""}
                <div class="hero-grid">
                    <section class="panel-card glass-card panel-card-soft overflow-hidden p-6 sm:p-8">
                        <div class="mb-5 inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-bold tracking-[0.18em] text-blue-700">${escapeHtml(HERO.eyebrow || "ADAPTIVE LEARNING")}</div>
                        <h1 class="max-w-3xl text-2xl font-black leading-snug text-slate-900 sm:text-4xl">
                            ${escapeHtml(HERO.titleLead || `${topicName}を`)}
                            <span class="text-blue-700">${escapeHtml(HERO.titleAccent || "説明できる状態")}</span>
                            ${escapeHtml(HERO.titleTrail || "まで持っていく")}
                        </h1>
                        <p class="mt-2 text-lg font-bold text-slate-800">${escapeHtml(HERO.subtitle || "未知領域理解のための学習アプリ")}</p>
                        <p class="mt-4 max-w-3xl text-sm leading-7 text-slate-600">
                            ${escapeHtml(HERO.description || "")}
                        </p>
                        <div class="mt-6 flex flex-wrap gap-3">
                            <button class="rounded-full bg-blue-700 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-blue-800" data-action="goto-section" data-section="intro">学習を始める</button>
                            <button class="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-bold text-slate-700 transition hover:border-blue-300 hover:text-blue-700" data-action="goto-section" data-section="diagnosis">誤解診断から入る</button>
                            <button class="rounded-full border border-rose-300 bg-rose-50 px-5 py-3 text-sm font-bold text-rose-700 transition hover:bg-rose-100" data-action="reset-progress">初期状態に戻す</button>
                        </div>
                    </section>
                    <aside class="panel-card glass-card p-6">
                        <div class="flex items-start justify-between gap-4">
                            <div>
                                <div class="text-xs font-bold uppercase tracking-[0.2em] text-slate-500">学習進捗</div>
                                <div class="mt-2 text-3xl font-black text-slate-900">${progressPercent()}%</div>
                            </div>
                            <div class="rounded-2xl bg-emerald-50 px-3 py-2 text-xs font-bold text-emerald-700">${escapeHtml(intro.label)}</div>
                        </div>
                        <div class="progress-track mt-5">
                            <div class="progress-fill" style="width:${progressPercent()}%"></div>
                        </div>
                        <p class="mt-4 text-sm leading-7 text-slate-600">${escapeHtml(intro.text)}</p>
                        <dl class="mt-5 space-y-3 text-sm">
                            <div class="metric-card p-4">
                                <dt class="font-bold text-slate-700">現在地</dt>
                                <dd class="mt-1 text-slate-600">${escapeHtml(APP_SECTIONS[sectionIndex[state.currentSection]].label)}</dd>
                            </div>
                            <div class="metric-card p-4">
                                <dt class="font-bold text-slate-700">再学習候補</dt>
                                <dd class="mt-1 text-slate-600">${escapeHtml((state.diagnosis.revisit || []).slice(0, 2).join(" / ") || "まだ診断前です")}</dd>
                            </div>
                        </dl>
                    </aside>
                </div>
            </header>
        `;
    }

    function renderSectionNav() {
        return `
            <nav class="mx-auto max-w-6xl px-4 sm:px-6">
                <div class="panel-card glass-card overflow-x-auto px-3 py-3">
                    <div class="flex min-w-max gap-2">
                        ${APP_SECTIONS.map((section) => `
                            <button
                                class="section-chip ${section.id === state.currentSection ? "section-chip-active" : ""} rounded-full px-4 py-2 text-sm font-bold"
                                data-action="goto-section"
                                data-section="${section.id}">
                                ${escapeHtml(section.label)}
                            </button>
                        `).join("")}
                    </div>
                </div>
            </nav>
        `;
    }

    function renderIntroSection() {
        const summary = introSummary();
        return `
            <section class="space-y-6">
                <div class="grid gap-4 lg:grid-cols-3">
                    ${INTRO_OVERVIEW_CARDS.map((card) => `
                        <article class="panel-card p-6">
                            <div class="text-xs font-bold tracking-[0.18em] text-${card.id === "what" ? "blue" : card.id === "learn" ? "emerald" : "amber"}-700">${escapeHtml(card.eyebrow)}</div>
                            <h2 class="mt-2 text-2xl font-black">${escapeHtml(card.title)}</h2>
                            <p class="mt-3 text-sm leading-7 text-slate-600">${escapeHtml(card.body)}</p>
                        </article>
                    `).join("")}
                </div>

                <div class="panel-card p-6 sm:p-8">
                    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">SELF CHECK</div>
                            <h3 class="mt-2 text-2xl font-black">学習開始前の理解度セルフチェック</h3>
                        </div>
                        <div class="rounded-2xl bg-blue-50 px-4 py-3 text-sm font-bold text-blue-700">${escapeHtml(summary.label)}</div>
                    </div>
                    <div class="mt-6 space-y-6">
                        ${INTRO_SELF_CHECK.map((question) => `
                            <div class="rounded-3xl border border-slate-200 p-5">
                                <p class="text-sm font-bold leading-7 text-slate-800">${escapeHtml(question.prompt)}</p>
                                <div class="mt-4 grid gap-3 sm:grid-cols-3">
                                    ${question.options.map((option) => `
                                        <label class="diagnosis-choice ${Number(state.introCheck[question.id]) === option.value ? "border-blue-400 bg-blue-50" : ""}">
                                            <input class="sr-only" type="radio" name="intro-${question.id}" value="${option.value}" data-action="set-intro-answer" data-question="${question.id}">
                                            <span class="text-sm font-bold text-slate-800">${escapeHtml(option.label)}</span>
                                        </label>
                                    `).join("")}
                                </div>
                            </div>
                        `).join("")}
                    </div>
                    <div class="mt-6 rounded-3xl bg-slate-50 p-5">
                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">現在のおすすめ導線</div>
                        <p class="mt-3 text-sm leading-7 text-slate-700">${escapeHtml(summary.text)}</p>
                        <div class="mt-4 flex flex-wrap gap-3">
                            <button class="rounded-full bg-slate-900 px-4 py-3 text-sm font-bold text-white" data-action="goto-section" data-section="concepts">概念地図へ進む</button>
                            <button class="rounded-full border border-slate-300 bg-white px-4 py-3 text-sm font-bold text-slate-700" data-action="goto-section" data-section="diagnosis">誤解診断へ進む</button>
                        </div>
                    </div>
                </div>

                ${renderFigureCards()}

                ${renderMediaSection()}
            </section>
        `;
    }

    function renderConceptSection() {
        const active = getActiveConcept();
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-blue-700">CONCEPT MAP</div>
                            <h2 class="mt-2 text-2xl font-black">中核概念を関係ごとにつかむ</h2>
                            <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                                ノードをタップすると、初学者向け説明と一歩踏み込んだ説明を切り替えられます。
                                何が何に効いているかを、単語単体ではなく関係で見てください。
                            </p>
                        </div>
                        <div class="inline-flex rounded-full bg-slate-100 p-1">
                            <button class="rounded-full px-4 py-2 text-sm font-bold ${state.conceptLevel === "basic" ? "bg-white text-blue-700 shadow-sm" : "text-slate-600"}" data-action="set-concept-level" data-level="basic">初学者向け</button>
                            <button class="rounded-full px-4 py-2 text-sm font-bold ${state.conceptLevel === "advanced" ? "bg-white text-blue-700 shadow-sm" : "text-slate-600"}" data-action="set-concept-level" data-level="advanced">少し踏み込む</button>
                        </div>
                    </div>
                    <div class="mt-6 grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
                        <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                            ${CONCEPTS.map((concept) => `
                                <button class="concept-node p-5 text-left ${concept.id === active.id ? "concept-node-active" : ""} ${isRelatedConcept(concept.id) ? "concept-node-related" : ""}" data-action="set-active-concept" data-concept="${concept.id}">
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">NODE</div>
                                    <div class="mt-2 text-lg font-black text-slate-900">${escapeHtml(concept.title)}</div>
                                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(concept.short)}</p>
                                </button>
                            `).join("")}
                        </div>
                        <aside class="panel-card-soft rounded-[28px] border border-blue-100 p-6">
                            <div class="text-xs font-bold tracking-[0.18em] text-blue-700">ACTIVE NODE</div>
                            <h3 class="mt-2 text-2xl font-black text-slate-900">${escapeHtml(active.title)}</h3>
                            <p class="mt-4 text-sm leading-7 text-slate-700">${escapeHtml(state.conceptLevel === "basic" ? active.beginner : active.advanced)}</p>
                            <div class="mt-5">
                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">図と表で確認</div>
                                <div class="mt-3">
                                    ${renderConceptSupplement(active)}
                                </div>
                            </div>
                            <div class="mt-6">
                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">関係の流れ</div>
                                <div class="mt-3 flex flex-wrap gap-2">
                                    ${active.relations.map((relation) => `
                                        <span class="relation-pill">${escapeHtml(active.title)} → ${escapeHtml(conceptMap[relation.target].title)}</span>
                                    `).join("")}
                                </div>
                                <div class="mt-4 space-y-3">
                                    ${active.relations.map((relation) => `
                                        <div class="rounded-2xl bg-white/80 p-4">
                                            <div class="text-sm font-bold text-slate-800">${escapeHtml(conceptMap[relation.target].title)}</div>
                                            <p class="mt-1 text-sm leading-6 text-slate-600">${escapeHtml(relation.label)}</p>
                                        </div>
                                    `).join("")}
                                </div>
                            </div>
                        </aside>
                    </div>
                </div>
            </section>
        `;
    }

    function renderVisualSection() {
        const scenario = getVisualScenario();
        const controls = VISUAL_LEARNING.controls || [];
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="text-xs font-bold tracking-[0.18em] text-emerald-700">VISUAL LEARNING</div>
                    <h2 class="mt-2 text-2xl font-black">${escapeHtml(VISUAL_LEARNING.title || "条件を動かして、どこを読むべきかを見る")}</h2>
                    <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                        ${escapeHtml(VISUAL_LEARNING.description || "ここでは精密な実測再現ではなく、解釈の軸をつかむための概念モデルを使います。スライダーを動かし、どの条件でどの誤読が起きやすいかを確認してください。")}
                    </p>
                    <div class="mt-6 grid gap-6 xl:grid-cols-[0.88fr_1.12fr]">
                        <div class="space-y-5">
                            <div class="rounded-3xl border border-slate-200 p-5">
                                <div class="text-sm font-bold text-slate-800">${escapeHtml(VISUAL_LEARNING.materialLabel || "材料モデル")}</div>
                                <div class="mt-3 grid gap-3">
                                    ${Object.entries(VISUAL_MODELS).map(([key, model]) => `
                                        <button class="diagnosis-choice ${state.visual.material === key ? "border-blue-400 bg-blue-50" : ""}" data-action="set-material" data-material="${key}">
                                            <div class="text-sm font-bold text-slate-900">${escapeHtml(model.label)}</div>
                                            <div class="mt-1 text-sm leading-6 text-slate-600">${escapeHtml(model.note)}</div>
                                        </button>
                                    `).join("")}
                                </div>
                            </div>

                            <div class="rounded-3xl border border-slate-200 p-5">
                                <div class="space-y-5">
                                    ${controls.map((control) => `
                                        <div>
                                            <div class="flex items-center justify-between text-sm font-bold text-slate-800">
                                                <span>${escapeHtml(control.label)}</span>
                                                <span>${escapeHtml(typeof control.formatValue === "function" ? control.formatValue(state.visual[control.field], scenario) : String(state.visual[control.field]))}</span>
                                            </div>
                                            ${control.type === "select"
                                                ? `
                                                    <select class="mt-3 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm" data-action="set-visual-field" data-field="${control.field}">
                                                        ${(control.options || []).map((option) => `
                                                            <option value="${option.value}" ${String(state.visual[control.field]) === String(option.value) ? "selected" : ""}>${escapeHtml(option.label)}</option>
                                                        `).join("")}
                                                    </select>
                                                `
                                                : `<input class="slider mt-3" type="range" min="${control.min}" max="${control.max}" step="${control.step}" value="${state.visual[control.field]}" data-action="set-visual-slider" data-field="${control.field}">`
                                            }
                                        </div>
                                    `).join("")}
                                </div>
                            </div>

                            <div class="grid gap-3 sm:grid-cols-2">
                                ${(scenario.metrics || []).map((metric) => `
                                    <div class="metric-card p-4">
                                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">${escapeHtml(metric.label)}</div>
                                        <div class="mt-2 text-2xl font-black ${metric.tone ? metricToneClass(metric.tone) : "text-slate-900"}">${escapeHtml(String(metric.value))}</div>
                                    </div>
                                `).join("")}
                            </div>
                        </div>

                        <div class="space-y-5">
                            <div class="rounded-[28px] border border-slate-200 bg-white p-5">
                                <div class="chart-wrap">
                                    <canvas id="visualChart"></canvas>
                                </div>
                                <p class="mt-4 text-xs leading-6 text-slate-500">
                                    ${escapeHtml(VISUAL_LEARNING.chartCaption || "赤: 負荷、青: 除荷、点: hmax / hc / hf。数値そのものより「どこが解釈の支点か」を見るための概念図です。")}
                                </p>
                            </div>
                            <div class="grid gap-4 sm:grid-cols-3">
                                ${scenario.insights.map((insight) => `
                                    <div class="rounded-3xl bg-slate-50 p-5">
                                        <div class="text-sm font-bold text-slate-900">${escapeHtml(insight.title)}</div>
                                        <p class="mt-2 text-sm leading-7 text-slate-600">${escapeHtml(insight.body)}</p>
                                    </div>
                                `).join("")}
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        `;
    }

    function renderDiagnosisSection() {
        const questions = orderedDiagnosisQuestions();
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-amber-700">MISCONCEPTION DIAGNOSIS</div>
                            <h2 class="mt-2 text-2xl font-black">よくある誤解を先に見つける</h2>
                            <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                                分岐順ではなく、代表的な誤解を最初からすべて並べています。各設問は選ぶとすぐに正誤と解説が出ます。
                            </p>
                        </div>
                        <button class="rounded-full border border-slate-300 bg-white px-4 py-3 text-sm font-bold text-slate-700" data-action="reset-diagnosis">診断をやり直す</button>
                    </div>

                    <div class="mt-6 grid gap-4 md:grid-cols-3">
                        <div class="metric-card p-4">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">回答数</div>
                            <div class="mt-2 text-2xl font-black text-slate-900">${state.diagnosis.history.length}</div>
                        </div>
                        <div class="metric-card p-4">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">正答数</div>
                            <div class="mt-2 text-2xl font-black text-slate-900">${state.diagnosis.correctCount}</div>
                        </div>
                        <div class="metric-card p-4">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">正答率</div>
                            <div class="mt-2 text-2xl font-black text-slate-900">${diagnosisAccuracy()}%</div>
                        </div>
                    </div>

                    <div class="mt-6 space-y-5">
                        ${questions.map((question) => {
                            const entry = diagnosisEntry(question.id);
                            return `
                                <div class="rounded-[30px] border border-slate-200 bg-white p-6">
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">設問</div>
                                    <h3 class="mt-2 text-xl font-black leading-tight text-slate-900">${escapeHtml(question.prompt)}</h3>
                                    <p class="mt-3 text-sm leading-7 text-slate-600">
                                        引っかかりやすい理由:
                                        ${escapeHtml(question.whyEasy)}
                                    </p>
                                    <div class="mt-5 space-y-3">
                                        ${question.options.map((option) => `
                                            <button class="diagnosis-choice ${entry && entry.optionId === option.id ? (entry.correct ? "border-emerald-400 bg-emerald-50" : "border-amber-400 bg-amber-50") : ""}" data-action="answer-diagnosis" data-question="${question.id}" data-option="${option.id}">
                                                <span class="text-sm font-bold text-slate-900">${escapeHtml(option.label)}</span>
                                            </button>
                                        `).join("")}
                                    </div>
                                    ${entry ? `
                                        <div class="mt-5 rounded-3xl ${entry.correct ? "bg-emerald-50 text-emerald-900" : "bg-amber-50 text-amber-900"} p-5">
                                            <div class="text-sm font-black">${entry.correct ? "正解です" : "不正解です"}</div>
                                            <div class="mt-1 text-xs font-bold tracking-[0.16em]">${entry.correct ? "誤解を回避できています" : "この誤解は起こりやすいです"}</div>
                                            <p class="mt-2 text-sm leading-7">${escapeHtml(entry.explanation)}</p>
                                        </div>
                                    ` : ""}
                                </div>
                            `;
                        }).join("")}
                    </div>

                    ${state.diagnosis.complete ? `
                        <div class="mt-6 grid gap-4 lg:grid-cols-[1fr_0.9fr]">
                            <div class="rounded-3xl border border-slate-200 p-6">
                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">診断結果</div>
                                <h3 class="mt-2 text-2xl font-black text-slate-900">弱点の傾向</h3>
                                <p class="mt-3 text-sm leading-7 text-slate-600">${escapeHtml(diagnosisSummaryText())}</p>
                                <div class="mt-5 flex flex-wrap gap-2">
                                    ${(state.diagnosis.revisit || []).length
                                        ? state.diagnosis.revisit.map((item) => `<span class="tag tag-weak">${escapeHtml(item)}</span>`).join("")
                                        : `<span class="tag tag-good">${escapeHtml(DIAGNOSIS_UI.noRevisitTagText || "再学習候補はまだ絞られていません")}</span>`
                                    }
                                </div>
                            </div>
                            <div class="rounded-3xl bg-blue-50 p-6">
                                <div class="text-sm font-bold text-blue-900">次のおすすめ</div>
                                <div class="mt-4 space-y-3">
                                    ${(DIAGNOSIS_UI.nextActions || [
                                        { section: "visual", label: "図解で曲線と深さを見直す" },
                                        { section: "ai", label: "AI対話で弱点を言語化する" },
                                        { section: "mastery", label: "選択式テストで仕上げる" }
                                    ]).map((item) => `
                                        <button class="w-full rounded-2xl bg-white px-4 py-4 text-left text-sm font-bold text-slate-800" data-action="goto-section" data-section="${item.section}">${escapeHtml(item.label)}</button>
                                    `).join("")}
                                </div>
                            </div>
                        </div>
                    ` : ""}
                </div>
            </section>
        `;
    }

    function renderAiSection() {
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="grid gap-6 lg:grid-cols-[1.08fr_0.92fr]">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-blue-700">AI COACH</div>
                            <h2 class="mt-2 text-2xl font-black">自由質問 + 分岐質問で深掘りする</h2>
                            <p class="mt-3 text-sm leading-7 text-slate-600">
                                API キーが未設定でも、ローカルの分岐質問テンプレートで最低限動作します。
                                外部 AI を使う場合も、UI 側から見えるのは adapter / service 層だけです。
                            </p>
                            <div class="mt-5 rounded-3xl bg-slate-50 p-5">
                                <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                                    <div>
                                        <div class="text-sm font-bold text-slate-900">接続状態</div>
                                        <div class="mt-1 text-sm text-slate-600">${state.settings.geminiApiKey ? "Gemini adapter を使用可能" : "ローカル分岐モードで動作中"}</div>
                                    </div>
                                    <div class="tag ${state.settings.geminiApiKey ? "tag-good" : "tag-neutral"}">${escapeHtml(state.ai.lastMode === "gemini" ? "直近応答: Gemini" : "直近応答: Local")}</div>
                                </div>
                                <div class="mt-4 grid gap-3 sm:grid-cols-[1fr_auto]">
                                    <input id="apiKeyInput" type="password" class="w-full rounded-2xl border border-slate-300 px-4 py-3 text-sm" placeholder="Gemini API キー（任意）" value="${escapeHtml(state.settings.geminiApiKey)}">
                                    <button class="rounded-2xl bg-slate-900 px-4 py-3 text-sm font-bold text-white" data-action="clear-api-key">クリア</button>
                                </div>
                                <p class="mt-2 text-xs leading-6 text-slate-500">
                                    キーはこのブラウザの localStorage にのみ保存します。未設定でも学習機能は止まりません。
                                </p>
                            </div>

                            <div class="mt-6 rounded-3xl border border-slate-200 p-5">
                                <div class="text-sm font-bold text-slate-900">AI からの深掘り候補</div>
                                <div class="mt-4 flex flex-wrap gap-3">
                                    ${AI_SUGGESTED_PATHS.map((prompt) => `
                                        <button class="rounded-full border border-slate-300 bg-white px-4 py-3 text-sm font-bold text-slate-700" data-action="send-ai-suggestion" data-prompt="${escapeHtml(prompt)}">${escapeHtml(prompt)}</button>
                                    `).join("")}
                                </div>
                            </div>
                        </div>

                        <div class="space-y-4">
                            <div class="rounded-[30px] border border-slate-200 bg-slate-50 p-4 sm:p-5">
                                <div class="max-h-[420px] space-y-3 overflow-y-auto pr-1">
                                    ${state.ai.messages.map((message) => `
                                        <div class="chat-bubble ${message.role === "user" ? "chat-user ml-auto" : "chat-assistant"}">
                                            <div class="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-slate-500">${message.role === "user" ? "YOU" : message.mode === "gemini" ? "AI" : "LOCAL COACH"}</div>
                                            <div class="space-y-3 text-sm leading-7 text-slate-700">${formatTextBlock(message.content)}</div>
                                            ${message.followUps && message.followUps.length ? `
                                                <div class="mt-4 flex flex-wrap gap-2">
                                                    ${message.followUps.map((follow) => `
                                                        <button class="rounded-full border border-slate-300 bg-white px-3 py-2 text-xs font-bold text-slate-700" data-action="send-ai-suggestion" data-prompt="${escapeHtml(follow)}">${escapeHtml(follow)}</button>
                                                    `).join("")}
                                                </div>
                                            ` : ""}
                                        </div>
                                    `).join("")}
                                    ${state.ai.pending ? `
                                        <div class="chat-bubble chat-assistant">
                                            <div class="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-slate-500">THINKING</div>
                                            <div class="flex items-center gap-2">
                                                <span class="loader-dot"></span>
                                                <span class="loader-dot"></span>
                                                <span class="loader-dot"></span>
                                            </div>
                                        </div>
                                    ` : ""}
                                </div>
                            </div>

                            <div class="rounded-[28px] border border-slate-200 bg-white p-4">
                                <label class="text-sm font-bold text-slate-900" for="aiPrompt">質問を書く</label>
                                <textarea id="aiPrompt" class="mt-3 min-h-[140px] w-full rounded-3xl border border-slate-300 px-4 py-4 text-sm leading-7" placeholder="${escapeHtml(AI_UI.textareaPlaceholder || "例: 荷重-変位曲線の除荷勾配とヤング率の関係を、硬さとの違いも含めて説明してください。")}">${escapeHtml(state.ai.input)}</textarea>
                                <div class="mt-4 flex items-center justify-between gap-4">
                                    <p class="text-xs leading-6 text-slate-500">自由質問でも、上の候補ボタンからでも送れます。</p>
                                    <button class="rounded-full bg-blue-700 px-5 py-3 text-sm font-bold text-white ${state.ai.pending ? "opacity-50" : ""}" data-action="submit-ai">送信する</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        `;
    }

    function renderMasterySection() {
        const result = state.mastery.result || computeMasteryResult();
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="grid gap-6 lg:grid-cols-[0.92fr_1.08fr]">
                        <div class="space-y-5">
                            <div>
                                <div class="text-xs font-bold tracking-[0.18em] text-emerald-700">MASTERY CHECK</div>
                                <h2 class="mt-2 text-2xl font-black">最後は選択式テストで仕上げる</h2>
                                <p class="mt-3 text-sm leading-7 text-slate-600">
                                    入力欄は使わず、短い選択式で中核概念を確認します。選ぶとすぐ正誤と解説が出ます。
                                </p>
                            </div>
                            <div class="rounded-3xl bg-slate-50 p-5">
                                <div class="text-sm font-bold text-slate-900">合格ラインの目安</div>
                                <div class="mt-4 space-y-3">
                                    ${EXPLANATION_RUBRIC.map((item) => `
                                        <div class="rounded-2xl bg-white p-4 text-sm leading-7 text-slate-700">
                                            <span class="font-bold text-slate-900">${escapeHtml(item.title)}</span>
                                        </div>
                                    `).join("")}
                                </div>
                            </div>
                        </div>
                        <div class="space-y-4">
                            <div class="grid gap-4 md:grid-cols-3">
                                <div class="metric-card p-4">
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">回答数</div>
                                    <div class="mt-2 text-2xl font-black text-slate-900">${result.answered}</div>
                                </div>
                                <div class="metric-card p-4">
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">正答数</div>
                                    <div class="mt-2 text-2xl font-black text-slate-900">${result.correct}</div>
                                </div>
                                <div class="metric-card p-4">
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">正答率</div>
                                    <div class="mt-2 text-2xl font-black text-slate-900">${result.accuracy}%</div>
                                </div>
                            </div>
                            <div class="space-y-4">
                                ${MASTERY_QUIZ.map((question) => {
                                    const selected = state.mastery.answers[question.id];
                                    const selectedChoice = question.choices.find((item) => item.id === selected);
                                    return `
                                        <div class="rounded-[30px] border border-slate-200 bg-white p-5">
                                            <div class="text-sm font-black leading-7 text-slate-900">${escapeHtml(question.prompt)}</div>
                                            <div class="mt-4 space-y-3">
                                                ${question.choices.map((choice) => `
                                                    <button class="diagnosis-choice ${selected === choice.id ? (choice.correct ? "border-emerald-400 bg-emerald-50" : "border-amber-400 bg-amber-50") : ""}" data-action="answer-mastery" data-question="${question.id}" data-choice="${choice.id}">
                                                        <span class="text-sm font-bold text-slate-900">${escapeHtml(choice.label)}</span>
                                                    </button>
                                                `).join("")}
                                            </div>
                                            ${selectedChoice ? `
                                                <div class="mt-4 rounded-3xl ${selectedChoice.correct ? "bg-emerald-50 text-emerald-900" : "bg-amber-50 text-amber-900"} p-4">
                                                    <div class="text-sm font-black">${selectedChoice.correct ? "正解" : "不正解"}</div>
                                                    <p class="mt-2 text-sm leading-7">${escapeHtml(selectedChoice.explanation)}</p>
                                                </div>
                                            ` : ""}
                                        </div>
                                    `;
                                }).join("")}
                            </div>
                            ${result.answered ? `
                                <div class="rounded-[30px] border border-slate-200 bg-slate-50 p-5">
                                    <div class="flex items-center justify-between gap-4">
                                        <div class="text-sm font-bold text-slate-900">結果サマリー</div>
                                        <div class="tag ${result.accuracy >= 75 ? "tag-good" : "tag-weak"}">${escapeHtml(result.level)}</div>
                                    </div>
                                    <div class="mt-4 grid gap-4 md:grid-cols-2">
                                        <div class="rounded-2xl bg-white p-4">
                                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">まだ弱い問い</div>
                                            <ul class="mt-3 space-y-2 text-sm leading-7 text-slate-700">
                                                ${(result.weakQuestions.length
                                                    ? result.weakQuestions
                                                    : ["現時点で大きな取りこぼしはありません"]
                                                ).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
                                            </ul>
                                        </div>
                                        <div class="rounded-2xl bg-white p-4">
                                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">未回答</div>
                                            <ul class="mt-3 space-y-2 text-sm leading-7 text-slate-700">
                                                ${(result.missing.length
                                                    ? result.missing
                                                    : ["全問回答済みです"]
                                                ).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
                                            </ul>
                                        </div>
                                    </div>
                                    <div class="mt-4 rounded-2xl bg-blue-50 p-4 text-sm leading-7 text-blue-900">
                                        ${result.accuracy >= 75
                                            ? "選択式では中核を押さえています。次は AI 対話で、自分の言葉でも説明できるか確認してください。"
                                            : "正答率が低い問いは、図解と誤解診断の該当部分へ戻ってから再挑戦すると定着しやすいです。"}
                                    </div>
                                </div>
                            ` : ""}
                        </div>
                    </div>
                </div>
            </section>
        `;
    }

    function renderRecordSection() {
        const revisit = diagnosisWeakPoints();
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">LEARNING RECORD</div>
                            <h2 class="mt-2 text-2xl font-black">学習状態の保存と振り返り</h2>
                            <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                                どこまで進んだか、どこでつまずいたか、何を再学習すべきかをローカルに保持します。
                            </p>
                        </div>
                        <button class="rounded-full border border-red-300 bg-white px-4 py-3 text-sm font-bold text-red-700" data-action="reset-progress">保存データを初期化する</button>
                    </div>

                    <div class="mt-6 grid gap-4 lg:grid-cols-3">
                        <div class="metric-card p-5">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">訪問済み画面</div>
                            <div class="mt-3 flex flex-wrap gap-2">
                                ${state.visitedSections.map((id) => `<span class="tag tag-neutral">${escapeHtml(APP_SECTIONS[sectionIndex[id]].label)}</span>`).join("")}
                            </div>
                        </div>
                        <div class="metric-card p-5">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">誤解が出やすかった点</div>
                            <div class="mt-3 flex flex-wrap gap-2">
                                ${revisit.length ? revisit.map((item) => `<span class="tag tag-weak">${escapeHtml(item)}</span>`).join("") : '<span class="tag tag-good">まだ未診断または大きな偏りなし</span>'}
                            </div>
                        </div>
                        <div class="metric-card p-5">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">理解確認</div>
                            <div class="mt-3 text-sm leading-7 text-slate-700">
                                ${state.mastery.result ? `${escapeHtml(state.mastery.result.level)} (${state.mastery.result.accuracy}%)` : "まだ未評価です。最後に選択式テストで確認してください。"}
                            </div>
                        </div>
                    </div>

                    <div class="mt-6 rounded-[30px] bg-slate-50 p-6">
                        <div class="text-sm font-bold text-slate-900">次にやるとよいこと</div>
                        <div class="mt-4 grid gap-3 md:grid-cols-3">
                            <button class="rounded-2xl bg-white px-4 py-4 text-left text-sm font-bold text-slate-800" data-action="goto-section" data-section="concepts">概念地図を再確認する</button>
                            <button class="rounded-2xl bg-white px-4 py-4 text-left text-sm font-bold text-slate-800" data-action="goto-section" data-section="visual">図解を動かして条件差を見る</button>
                            <button class="rounded-2xl bg-white px-4 py-4 text-left text-sm font-bold text-slate-800" data-action="goto-section" data-section="mastery">選択式テストをやり直す</button>
                        </div>
                    </div>
                </div>
            </section>
        `;
    }

    function renderSection() {
        switch (state.currentSection) {
            case "intro":
                return renderIntroSection();
            case "concepts":
                return renderConceptSection();
            case "visual":
                return renderVisualSection();
            case "diagnosis":
                return renderDiagnosisSection();
            case "ai":
                return renderAiSection();
            case "mastery":
                return renderMasterySection();
            case "record":
                return renderRecordSection();
            default:
                return renderIntroSection();
        }
    }

    function renderFooterNav() {
        const currentIdx = sectionIndex[state.currentSection];
        const prev = APP_SECTIONS[currentIdx - 1];
        const next = APP_SECTIONS[currentIdx + 1];
        return `
            <div class="sticky-footer-nav mt-8 border-t border-slate-200/70 bg-white/90">
                <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
                    <button class="rounded-full border border-slate-300 px-4 py-3 text-sm font-bold text-slate-700 ${prev ? "" : "opacity-40"}" ${prev ? `data-action="goto-section" data-section="${prev.id}"` : "disabled"}>前へ</button>
                    <div class="text-xs font-bold uppercase tracking-[0.22em] text-slate-500">${currentIdx + 1} / ${APP_SECTIONS.length}</div>
                    <button class="rounded-full bg-slate-900 px-4 py-3 text-sm font-bold text-white ${next ? "" : "opacity-40"}" ${next ? `data-action="goto-section" data-section="${next.id}"` : "disabled"}>次へ</button>
                </div>
            </div>
        `;
    }

    function renderApp() {
        root.innerHTML = `
            <div class="learning-shell pb-24">
                ${renderHeader()}
                ${renderSectionNav()}
                <main class="mx-auto max-w-6xl px-4 py-6 sm:px-6">
                    ${renderSection()}
                </main>
                ${renderFooterNav()}
            </div>
        `;
        renderChartIfNeeded();
        syncInputs();
    }

    function syncInputs() {
        INTRO_SELF_CHECK.forEach((question) => {
            const selected = state.introCheck[question.id];
            if (selected === undefined) {
                return;
            }
            const input = root.querySelector(`input[name="intro-${question.id}"][value="${selected}"]`);
            if (input) {
                input.checked = true;
            }
        });
    }

    function destroyChart() {
        if (chart) {
            chart.destroy();
            chart = null;
        }
    }

    function renderChartIfNeeded() {
        const canvas = document.getElementById("visualChart");
        if (!canvas || !window.Chart) {
            destroyChart();
            return;
        }

        const scenario = getVisualScenario();
        const chartConfig = scenario.chart || { type: "scatter", datasets: [] };
        destroyChart();

        chart = new window.Chart(canvas.getContext("2d"), {
            type: chartConfig.type || "scatter",
            data: {
                datasets: chartConfig.datasets || []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top"
                    },
                    tooltip: {
                        callbacks: {
                            label(context) {
                                const raw = context.raw;
                                if (typeof chartConfig.tooltipLabel === "function") {
                                    return chartConfig.tooltipLabel(raw, context);
                                }
                                if (raw.label) {
                                    return `${raw.label}: ${raw.x}, ${raw.y}`;
                                }
                                return `${raw.x}, ${raw.y}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: "linear",
                        title: {
                            display: true,
                            text: (VISUAL_LEARNING.axisLabels && VISUAL_LEARNING.axisLabels.x) || "X"
                        },
                        grid: {
                            color: "#e5e7eb"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: (VISUAL_LEARNING.axisLabels && VISUAL_LEARNING.axisLabels.y) || "Y"
                        },
                        grid: {
                            color: "#e5e7eb"
                        }
                    }
                }
            }
        });
    }

    function setDiagnosisComplete() {
        state.diagnosis.complete = state.diagnosis.history.length === orderedDiagnosisQuestions().length;
        state.diagnosis.misconceptions = state.diagnosis.history
            .filter((entry) => entry.misconception)
            .map((entry) => entry.label);
        state.diagnosis.revisit = diagnosisWeakPoints().slice(0, 3);
    }

    function answerDiagnosis(questionId, optionId) {
        const question = DIAGNOSIS_QUESTIONS[questionId];
        const option = question.options.find((item) => item.id === optionId);
        if (!option) {
            return;
        }

        state.diagnosis.history = state.diagnosis.history.filter((entry) => entry.questionId !== questionId);
        state.diagnosis.history.push({
            questionId,
            question: question.prompt,
            optionId,
            label: option.label,
            explanation: option.explanation,
            misconception: option.misconception,
            weakness: option.weakness || [],
            correct: Boolean(option.correct)
        });
        state.diagnosis.correctCount = state.diagnosis.history.filter((entry) => entry.correct).length;
        setDiagnosisComplete();
        persist();
        renderApp();
    }

    async function submitAiPrompt(promptText) {
        const prompt = promptText.trim();
        if (!prompt || state.ai.pending) {
            return;
        }

        state.ai.pending = true;
        state.ai.messages.push({
            role: "user",
            mode: "user",
            content: prompt
        });
        state.ai.input = "";
        persist();
        renderApp();

        try {
            const result = await aiService.respond(prompt, state);
            state.ai.messages.push({
                role: "assistant",
                mode: result.mode,
                content: result.answer,
                followUps: result.followUps
            });
            state.ai.lastMode = result.mode;
        } catch (error) {
            state.ai.messages.push({
                role: "assistant",
                mode: "local",
                content: "応答の取得に失敗しました。ローカル分岐モードで続けるか、質問をもう少し具体化してください。"
            });
            state.ai.lastMode = "local";
        } finally {
            state.ai.pending = false;
            persist();
            renderApp();
        }
    }

    function answerMastery(questionId, choiceId) {
        state.mastery.answers[questionId] = choiceId;
        state.mastery.result = computeMasteryResult();
        persist();
        renderApp();
    }

    root.addEventListener("click", (event) => {
        const button = event.target.closest("[data-action]");
        if (!button) {
            return;
        }

        const action = button.dataset.action;

        if (action === "goto-section") {
            visitSection(button.dataset.section);
            renderApp();
            return;
        }

        if (action === "switch-topic") {
            const params = new URLSearchParams(window.location.search);
            params.set("topic", button.dataset.topic);
            const nextSearch = params.toString();
            window.location.search = nextSearch ? `?${nextSearch}` : "";
            return;
        }

        if (action === "set-concept-level") {
            state.conceptLevel = button.dataset.level;
            persist();
            renderApp();
            return;
        }

        if (action === "set-active-concept") {
            state.activeConceptId = button.dataset.concept;
            persist();
            renderApp();
            return;
        }

        if (action === "set-material") {
            state.visual.material = button.dataset.material;
            persist();
            renderApp();
            return;
        }

        if (action === "answer-diagnosis") {
            answerDiagnosis(button.dataset.question, button.dataset.option);
            return;
        }

        if (action === "reset-diagnosis") {
            state.diagnosis = {
                currentQuestionId: "q1",
                history: [],
                complete: false,
                misconceptions: [],
                revisit: [],
                correctCount: 0
            };
            persist();
            renderApp();
            return;
        }

        if (action === "submit-ai") {
            submitAiPrompt(state.ai.input || "");
            return;
        }

        if (action === "send-ai-suggestion") {
            submitAiPrompt(button.dataset.prompt || "");
            return;
        }

        if (action === "answer-mastery") {
            answerMastery(button.dataset.question, button.dataset.choice);
            return;
        }

        if (action === "clear-api-key") {
            state.settings.geminiApiKey = "";
            persist();
            renderApp();
            return;
        }

        if (action === "reset-progress") {
            if (window.confirm("学習状態を初期化します。保存済みの進捗、AI 履歴、診断結果も消えます。続けますか。")) {
                state = resetState();
                renderApp();
                window.scrollTo({ top: 0, behavior: "smooth" });
            }
        }
    });

    root.addEventListener("change", (event) => {
        const target = event.target;
        if (target.dataset.action === "set-intro-answer") {
            state.introCheck[target.dataset.question] = Number(target.value);
            persist();
            renderApp();
            return;
        }

        if (target.dataset.action === "set-visual-slider") {
            state.visual[target.dataset.field] = Number(target.value);
            persist();
            renderApp();
            return;
        }

        if (target.dataset.action === "set-visual-field") {
            state.visual[target.dataset.field] = target.value;
            persist();
            renderApp();
        }
    });

    root.addEventListener("input", (event) => {
        const target = event.target;
        if (target.id === "aiPrompt") {
            state.ai.input = target.value;
            persist();
            return;
        }
        if (target.id === "apiKeyInput") {
            state.settings.geminiApiKey = target.value.trim();
            persist();
        }
    });

    visitSection(state.currentSection || "intro");
    renderApp();
})();
