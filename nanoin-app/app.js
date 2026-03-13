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
    const PRINCIPLE = topic.principle || {};
    const INTRO_OVERVIEW_CARDS = topic.introCards || [];
    const INTRO_SUMMARY_STATES = topic.introSummaryStates || {};
    const INTRO_SELF_CHECK = topic.selfCheck || content.INTRO_SELF_CHECK || [];
    const FIGURE_CARDS = topic.figureCards || content.FIGURE_CARDS || [];
    const CONCEPTS = topic.concepts || content.CONCEPTS || [];
    const CONCEPT_SUPPLEMENTS = topic.conceptSupplements || content.CONCEPT_SUPPLEMENTS || {};
    const CONCEPT_SCENES = topic.conceptScenes || {};
    const VISUAL_MODELS = topic.visualModels || content.VISUAL_MODELS || {};
    const VISUAL_LEARNING = topic.visualLearning || {};
    const DIAGNOSIS_QUESTIONS = topic.diagnosisQuestions || content.DIAGNOSIS_QUESTIONS || {};
    const DIAGNOSIS_UI = topic.diagnosisUi || {};
    const AI_SUGGESTED_PATHS = (topic.ai && topic.ai.suggestedPaths) || content.AI_SUGGESTED_PATHS || [];
    const EXPLANATION_RUBRIC = (topic.ai && topic.ai.explanationRubric) || content.EXPLANATION_RUBRIC || [];
    const AI_UI = (topic.ai && topic.ai.ui) || {};
    const MASTERY_QUIZ = topic.masteryQuiz || content.MASTERY_QUIZ || [];
    const MEDIA = topic.media || { featuredVideo: null, resources: [] };
    const ROLE_TRACKS = topic.roles || [];
    const COMPETENCIES = topic.competencies || [];
    const SIMULATION_MISSIONS = topic.simulationMissions || [];
    const { loadState, saveState, resetState } = window.NanoLearnStorage;
    const { AIService } = window.NanoLearnAI;

    const root = document.getElementById("app");
    const aiService = new AIService();
    let state = loadState();
    let chart = null;
    let currentChartConfig = null;

    const conceptMap = Object.fromEntries(CONCEPTS.map((concept) => [concept.id, concept]));
    const introQuestionMap = Object.fromEntries(INTRO_SELF_CHECK.map((question) => [question.id, question]));
    const masteryQuestionMap = Object.fromEntries(MASTERY_QUIZ.map((question) => [question.id, question]));
    const roleMap = Object.fromEntries(ROLE_TRACKS.map((role) => [role.id, role]));
    const competencyMap = Object.fromEntries(COMPETENCIES.map((competency) => [competency.id, competency]));
    const missionMap = Object.fromEntries(SIMULATION_MISSIONS.map((mission) => [mission.id, mission]));
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

    function asArray(value) {
        return Array.isArray(value) ? value : [];
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

    function getActiveRole() {
        return roleMap[state.roleId] || ROLE_TRACKS[0] || null;
    }

    function introAnsweredCount() {
        return Object.keys(state.introCheck).length;
    }

    function selfCheckComplete() {
        return Boolean(INTRO_SELF_CHECK.length) && introAnsweredCount() === INTRO_SELF_CHECK.length;
    }

    function nextIntroQuestion() {
        return INTRO_SELF_CHECK.find((question) => state.introCheck[question.id] === undefined) || INTRO_SELF_CHECK[INTRO_SELF_CHECK.length - 1] || null;
    }

    function hasMeaningfulProgress() {
        return selfCheckComplete() ||
            state.visitedSections.length > 1 ||
            state.diagnosis.history.length > 0 ||
            Object.keys(state.mastery.answers || {}).length > 0 ||
            (state.visual.completedMissions || []).length > 0;
    }

    function getDiagnosisHistoryEntry(questionId) {
        return state.diagnosis.history.find((entry) => entry.questionId === questionId) || null;
    }

    function introQuestionMax(questionId) {
        const question = introQuestionMap[questionId];
        if (!question || !question.options || !question.options.length) {
            return 1;
        }
        return Math.max(...question.options.map((option) => Number(option.value) || 0), 1);
    }

    function sourceWeight(source) {
        if (source.weight !== undefined) {
            return source.weight;
        }
        return source.type === "intro" ? 0.7 : 1;
    }

    function sourceProgress(source) {
        if (source.type === "intro") {
            const value = state.introCheck[source.id];
            if (value === undefined) {
                return 0;
            }
            return Math.max(0, Math.min(1, Number(value) / introQuestionMax(source.id)));
        }
        if (source.type === "diagnosis") {
            const entry = getDiagnosisHistoryEntry(source.id);
            if (!entry) {
                return 0;
            }
            return entry.correct ? 1 : 0;
        }
        if (source.type === "mastery") {
            const question = masteryQuestionMap[source.id];
            const selected = state.mastery.answers[source.id];
            if (!question || !selected) {
                return 0;
            }
            const choice = question.choices.find((item) => item.id === selected);
            return choice && choice.correct ? 1 : 0;
        }
        if (source.type === "mission") {
            return (state.visual.completedMissions || []).includes(source.id) ? 1 : 0;
        }
        return 0;
    }

    function evaluateCompetency(competency) {
        const sources = competency.sources || [];
        if (!sources.length) {
            return {
                id: competency.id,
                definition: competency,
                progress: 0,
                percent: 0,
                status: "not-started"
            };
        }

        let weightedTotal = 0;
        let weightSum = 0;
        sources.forEach((source) => {
            const weight = sourceWeight(source);
            weightedTotal += sourceProgress(source) * weight;
            weightSum += weight;
        });

        const progress = weightSum ? weightedTotal / weightSum : 0;
        let status = "not-started";
        if (progress >= 0.85) {
            status = "mastered";
        } else if (progress > 0) {
            status = "in-progress";
        }

        return {
            id: competency.id,
            definition: competency,
            progress,
            percent: Math.round(progress * 100),
            status
        };
    }

    function competencyStates() {
        return COMPETENCIES.map(evaluateCompetency);
    }

    function sortedCompetencyStates() {
        const activeRole = getActiveRole();
        return competencyStates().sort((left, right) => {
            const leftFocus = activeRole && (left.definition.roleIds || []).includes(activeRole.id) ? 1 : 0;
            const rightFocus = activeRole && (right.definition.roleIds || []).includes(activeRole.id) ? 1 : 0;
            if (leftFocus !== rightFocus) {
                return rightFocus - leftFocus;
            }
            return left.progress - right.progress;
        });
    }

    function progressPercent() {
        const items = competencyStates();
        if (!items.length) {
            return 0;
        }
        const total = items.reduce((sum, item) => sum + item.progress, 0);
        return Math.round((total / items.length) * 100);
    }

    function competencyStatusLabel(status) {
        if (status === "mastered") {
            return "仕上がり";
        }
        if (status === "in-progress") {
            return "進行中";
        }
        return "未着手";
    }

    function competencyStatusClass(status) {
        if (status === "mastered") {
            return "tag-good";
        }
        if (status === "in-progress") {
            return "tag-neutral";
        }
        return "tag-weak";
    }

    function topCompetencies(limit) {
        return sortedCompetencyStates().slice(0, limit);
    }

    function buildQuestionQueue() {
        const queue = [];
        const seen = new Set();

        function pushItem(item) {
            if (!item || seen.has(item.id)) {
                return;
            }
            seen.add(item.id);
            queue.push(item);
        }

        sortedCompetencyStates().forEach((competencyState) => {
            (competencyState.definition.sources || []).forEach((source) => {
                if (queue.length >= 5) {
                    return;
                }
                if (source.type === "diagnosis") {
                    const question = DIAGNOSIS_QUESTIONS[source.id];
                    const entry = getDiagnosisHistoryEntry(source.id);
                    if (!question || (entry && entry.correct)) {
                        return;
                    }
                    pushItem({
                        id: `diagnosis-${source.id}`,
                        title: question.prompt,
                        detail: competencyState.definition.title,
                        section: "diagnosis",
                        buttonLabel: "誤解診断へ"
                    });
                }
                if (source.type === "mastery") {
                    const question = masteryQuestionMap[source.id];
                    const selected = state.mastery.answers[source.id];
                    const selectedChoice = question && question.choices.find((item) => item.id === selected);
                    if (!question || (selectedChoice && selectedChoice.correct)) {
                        return;
                    }
                    pushItem({
                        id: `mastery-${source.id}`,
                        title: question.prompt,
                        detail: competencyState.definition.title,
                        section: "mastery",
                        buttonLabel: "理解確認へ"
                    });
                }
            });
        });

        sortedCompetencyStates().forEach((competencyState) => {
            if (queue.length >= 5) {
                return;
            }
            const conceptId = (competencyState.definition.conceptIds || [])[0];
            const concept = conceptMap[conceptId];
            if (!concept) {
                return;
            }
            pushItem({
                id: `concept-${competencyState.id}`,
                title: `${competencyState.definition.title}を 1 文で説明する`,
                detail: concept.title,
                section: "concepts",
                conceptId,
                buttonLabel: "概念地図へ"
            });
        });

        return queue.slice(0, 5);
    }

    function getPrimaryMediaLink() {
        const featured = MEDIA.featuredVideo;
        if (featured && (featured.url || featured.link || featured.src)) {
            return {
                url: featured.url || featured.link || featured.src,
                title: featured.title || MEDIA.title || "参考動画"
            };
        }
        const resource = (MEDIA.resources || [])[0];
        if (!resource) {
            return null;
        }
        return {
            url: resource.url,
            title: resource.title
        };
    }

    function getRecommendedVisualMission() {
        const competencyState = sortedCompetencyStates().find(
            (item) => item.definition.nextStep && item.definition.nextStep.missionId
        );
        if (competencyState) {
            return missionMap[competencyState.definition.nextStep.missionId] || null;
        }
        return SIMULATION_MISSIONS[0] || null;
    }

    function renderSmartAction(action, label, className) {
        if (!action) {
            return "";
        }
        const text = escapeHtml(label || action.label || "開く");
        if (action.missionId) {
            return `<button class="${className}" data-action="apply-sim-mission" data-mission="${action.missionId}">${text}</button>`;
        }
        if (action.section === "concepts" && action.conceptId) {
            return `<button class="${className}" data-action="open-concept" data-concept="${action.conceptId}">${text}</button>`;
        }
        if (action.url) {
            return `<button class="${className}" data-action="open-url" data-url="${action.url}">${text}</button>`;
        }
        if (action.section) {
            return `<button class="${className}" data-action="goto-section" data-section="${action.section}">${text}</button>`;
        }
        return "";
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
        return asArray(active && active.relations).some((item) => item.target === targetId);
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
                    <div class="panel-card figure-card p-5">
                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">${escapeHtml(card.label || "")}</div>
                        <div class="figure-stage mt-3 rounded-3xl p-4">
                            ${card.illustration || ""}
                        </div>
                        <div class="mt-3 rounded-2xl bg-slate-50 p-4 text-sm leading-7 text-slate-600">
                            ${(card.bullets || []).map((item) => `
                                <div class="figure-bullet"><span class="font-bold text-slate-900">${escapeHtml(item.label)}:</span> ${escapeHtml(item.body)}</div>
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

    function getConceptScene(active) {
        if (!active) {
            return null;
        }
        return CONCEPT_SCENES[active.id] || null;
    }

    function renderNanoIndentScene(options) {
        const sceneClass = options.sceneClass || "";
        const labels = asArray(options.labels).slice(0, 3);
        return `
            <div class="concept-scene ${sceneClass}">
                <div class="scene-frame scene-frame-nano">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "FORCE")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "READOUT")}</div>
                    <div class="scene-indent-wrap">
                        <div class="scene-probe"></div>
                        <div class="scene-force-line"></div>
                        ${options.showContactHalo ? '<div class="scene-contact-halo"></div>' : ""}
                        ${options.showStressFan ? '<div class="scene-stress-fan"></div>' : ""}
                        ${options.showDepthMarker ? '<div class="scene-depth-marker"></div>' : ""}
                        <div class="scene-surface ${options.roughSurface ? "scene-surface-rough" : ""}"></div>
                        ${options.showFilm ? '<div class="scene-film-layer"></div>' : ""}
                        ${options.showSubstrate ? '<div class="scene-substrate-layer"></div>' : ""}
                        <div class="scene-indent-mark ${options.indentClass || ""}"></div>
                        ${options.showCurve ? '<div class="scene-mini-curve"></div>' : ""}
                        ${options.showSpring ? '<div class="scene-spring-arc"></div>' : ""}
                    </div>
                </div>
                <div class="scene-legend">
                    ${labels.map((label) => `<span class="scene-legend-chip">${escapeHtml(label)}</span>`).join("")}
                </div>
                <p class="scene-caption">${escapeHtml(options.caption || "")}</p>
            </div>
        `;
    }

    function renderXrfScene(options) {
        const labels = asArray(options.labels).slice(0, 3);
        return `
            <div class="concept-scene ${options.sceneClass || ""}">
                <div class="scene-frame scene-frame-xrf">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "SOURCE")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "DETECTOR")}</div>
                    <div class="scene-xrf-wrap">
                        <div class="scene-source-box">${escapeHtml(options.sourceLabel || "SOURCE")}</div>
                        <div class="scene-beam scene-beam-forward"></div>
                        ${options.showShield ? '<div class="scene-shield"></div>' : ""}
                        <div class="scene-sample-block ${options.sampleClass || ""}">
                            <div class="scene-sample-core"></div>
                        </div>
                        ${options.showMatrixLayers ? '<div class="scene-matrix-layers"><span></span><span></span><span></span></div>' : ""}
                        <div class="scene-beam scene-beam-return"></div>
                        <div class="scene-detector-box">${escapeHtml(options.detectorLabel || "DETECT")}</div>
                        ${options.showPeaks ? '<div class="scene-spectrum-peaks"></div>' : ""}
                        ${options.showScan ? '<div class="scene-scan-line"></div>' : ""}
                        ${options.showDoor ? '<div class="scene-door-panel"></div>' : ""}
                    </div>
                </div>
                <div class="scene-legend">
                    ${labels.map((label) => `<span class="scene-legend-chip">${escapeHtml(label)}</span>`).join("")}
                </div>
                <p class="scene-caption">${escapeHtml(options.caption || "")}</p>
            </div>
        `;
    }

    function renderTaverScene(options) {
        const labels = asArray(options.labels).slice(0, 3);
        const variant = options.variant || "topview";

        let stage = "";
        if (variant === "abrasive") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-abrasive">
                    <div class="scene-taver-surface"></div>
                    <div class="scene-taver-surface scene-taver-subsurface"></div>
                    <div class="scene-taver-abrasive-tool"></div>
                    <div class="scene-taver-scratch-band"></div>
                    <div class="scene-taver-scratch-band scene-taver-scratch-band-2"></div>
                </div>
            `;
        } else if (variant === "adhesive") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-adhesive">
                    <div class="scene-taver-adhesive-top">
                        <div class="scene-taver-adhesive-bond"></div>
                    </div>
                    <div class="scene-taver-adhesive-base"></div>
                    <div class="scene-taver-adhesive-transfer"></div>
                </div>
            `;
        } else if (variant === "fatigue") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-fatigue">
                    <div class="scene-taver-fatigue-hit scene-taver-fatigue-hit-a"></div>
                    <div class="scene-taver-fatigue-hit scene-taver-fatigue-hit-b"></div>
                    <div class="scene-taver-fatigue-hit scene-taver-fatigue-hit-c"></div>
                    <div class="scene-taver-fatigue-base"></div>
                    <div class="scene-taver-fatigue-crack"></div>
                </div>
            `;
        } else if (variant === "wearindex") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-index">
                    <div class="scene-taver-index-axis scene-taver-index-axis-y"></div>
                    <div class="scene-taver-index-axis scene-taver-index-axis-x"></div>
                    <div class="scene-taver-index-bar scene-taver-index-bar-a"></div>
                    <div class="scene-taver-index-bar scene-taver-index-bar-b"></div>
                    <div class="scene-taver-index-bar scene-taver-index-bar-c"></div>
                    <div class="scene-taver-index-guide"></div>
                </div>
            `;
        } else {
            stage = `
                <div class="scene-taver-topview">
                    <div class="scene-taver-table"></div>
                    <div class="scene-taver-track scene-taver-track-a"></div>
                    <div class="scene-taver-track scene-taver-track-b"></div>
                    <div class="scene-taver-axis"></div>
                    <div class="scene-taver-wheel scene-taver-wheel-left"></div>
                    <div class="scene-taver-wheel scene-taver-wheel-right"></div>
                    <div class="scene-taver-offset scene-taver-offset-left"></div>
                    <div class="scene-taver-offset scene-taver-offset-right"></div>
                </div>
            `;
        }

        return `
            <div class="concept-scene ${options.sceneClass || ""}">
                <div class="scene-frame scene-frame-taver">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "TABER")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "MOTION")}</div>
                    ${stage}
                </div>
                <div class="scene-legend">
                    ${labels.map((label) => `<span class="scene-legend-chip">${escapeHtml(label)}</span>`).join("")}
                </div>
                <p class="scene-caption">${escapeHtml(options.caption || "")}</p>
            </div>
        `;
    }

    function renderPrincipleScene(scene) {
        if (!scene) {
            return "";
        }
        const visual = Object.assign({}, scene.visual || {});
        if (scene.type === "nano") {
            return renderNanoIndentScene(visual);
        }
        if (scene.type === "xrf") {
            return renderXrfScene(visual);
        }
        if (scene.type === "taver") {
            return renderTaverScene(visual);
        }
        return "";
    }

    function renderConceptMotionScene(active) {
        const scene = getConceptScene(active);
        if (!scene) {
            return `
                <div class="concept-scene concept-scene-generic">
                    <div class="scene-generic-orb"></div>
                    <div class="scene-generic-line"></div>
                    <div class="scene-generic-card">${escapeHtml(active.title)}</div>
                    <p class="scene-caption">${escapeHtml(active.short || "")}</p>
                </div>
            `;
        }
        const visual = Object.assign({}, scene.visual || {});
        if (scene.type === "nano") {
            return renderNanoIndentScene(visual);
        }
        if (scene.type === "xrf") {
            return renderXrfScene(visual);
        }
        if (scene.type === "taver") {
            return renderTaverScene(visual);
        }
        return `
            <div class="concept-scene concept-scene-generic">
                <div class="scene-generic-orb"></div>
                <div class="scene-generic-line"></div>
                <div class="scene-generic-card">${escapeHtml(active.title)}</div>
                <p class="scene-caption">${escapeHtml(active.short || "")}</p>
            </div>
        `;
    }

    function renderConceptHero(active) {
        return renderConceptMotionScene(active);
    }

    function renderConceptExplainer(active) {
        const scene = getConceptScene(active);
        const checks = asArray(scene && scene.checks).slice(0, 3);
        const beats = asArray(scene && scene.beats).slice(0, 3);
        return `
            <div class="concept-explainer-card">
                <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                    <div>
                        <div class="text-xs font-black tracking-[0.2em] text-blue-700">${escapeHtml(scene && scene.eyebrow ? scene.eyebrow : "EXPLAINABLE ANIMATION")}</div>
                        <div class="mt-2 text-2xl font-black text-slate-950">${escapeHtml(scene && scene.title ? scene.title : active.title)}</div>
                        <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">${escapeHtml(scene && scene.summary ? scene.summary : active.short || "")}</p>
                    </div>
                    ${checks.length ? `
                        <div class="concept-checks">
                            ${checks.map((item) => `<span class="concept-check-chip">${escapeHtml(item)}</span>`).join("")}
                        </div>
                    ` : ""}
                </div>
                <div class="mt-5">
                    ${renderConceptMotionScene(active)}
                </div>
                ${beats.length ? `
                    <div class="mt-5 grid gap-3 md:grid-cols-3">
                        ${beats.map((beat) => `
                            <article class="concept-beat-card">
                                <div class="concept-beat-step">${escapeHtml(beat.step || "")}</div>
                                <div class="mt-3 text-sm font-black text-slate-900">${escapeHtml(beat.title || "")}</div>
                                <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(beat.body || "")}</p>
                            </article>
                        `).join("")}
                    </div>
                ` : ""}
            </div>
        `;
    }

    function renderConceptConstellation(active) {
        const relations = asArray(active && active.relations).slice(0, 3);
        if (!relations.length) {
            return "";
        }
        const orbitPositions = [
            "concept-orbit-node-a",
            "concept-orbit-node-b",
            "concept-orbit-node-c"
        ];
        return `
            <div class="concept-orbit-card">
                <div class="flex items-center justify-between gap-4">
                    <div>
                        <div class="text-xs font-black tracking-[0.18em] text-slate-500">RELATION MAP</div>
                        <div class="mt-2 text-xl font-black text-slate-950">${escapeHtml(active.title)} を起点に見る</div>
                    </div>
                    <div class="tag tag-neutral">${relations.length} links</div>
                </div>
                <div class="concept-orbit-stage">
                    <div class="concept-orbit-ring"></div>
                    <div class="concept-orbit-center">
                        <div class="text-[11px] font-black tracking-[0.2em] text-blue-700">CORE NODE</div>
                        <div class="mt-2 text-lg font-black text-slate-950">${escapeHtml(active.title)}</div>
                        <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(active.short || "")}</p>
                    </div>
                    ${relations.map((relation, index) => {
                        const target = conceptMap[relation.target];
                        const targetTitle = target ? target.title : relation.target;
                        return `
                            <span class="concept-orbit-line concept-orbit-line-${index + 1}"></span>
                            <button class="concept-orbit-node ${orbitPositions[index] || ""}" data-action="open-concept" data-concept="${escapeHtml(relation.target)}">
                                <div class="concept-orbit-step">0${index + 1}</div>
                                <div class="mt-2 text-sm font-black text-slate-900">${escapeHtml(targetTitle)}</div>
                                <p class="mt-2 text-xs leading-5 text-slate-600">${escapeHtml(relation.label)}</p>
                            </button>
                        `;
                    }).join("")}
                </div>
                <div class="mt-5 grid gap-3">
                    ${relations.map((relation, index) => {
                        const target = conceptMap[relation.target];
                        const targetTitle = target ? target.title : relation.target;
                        const targetShort = target ? target.short : "";
                        return `
                            <article class="concept-relation-card">
                                <div class="flex items-start justify-between gap-3">
                                    <div>
                                        <div class="text-xs font-black tracking-[0.18em] text-slate-500">FLOW 0${index + 1}</div>
                                        <div class="mt-2 text-sm font-black text-slate-900">${escapeHtml(active.title)} → ${escapeHtml(targetTitle)}</div>
                                    </div>
                                    <button class="relation-pill" data-action="open-concept" data-concept="${escapeHtml(relation.target)}">${escapeHtml(targetTitle)}</button>
                                </div>
                                <p class="mt-3 text-sm leading-6 text-slate-600">${escapeHtml(relation.label)}</p>
                                ${targetShort ? `<p class="mt-2 text-xs leading-5 text-slate-500">${escapeHtml(targetShort)}</p>` : ""}
                            </article>
                        `;
                    }).join("")}
                </div>
            </div>
        `;
    }

    function renderConceptConstellationClean(active) {
        const relations = asArray(active && active.relations).slice(0, 3);
        if (!relations.length) {
            return "";
        }
        return `
            <div class="concept-orbit-card">
                <div class="flex items-center justify-between gap-4">
                    <div>
                        <div class="text-xs font-black tracking-[0.18em] text-slate-500">RELATION MAP</div>
                        <div class="mt-2 text-xl font-black text-slate-950">${escapeHtml(active.title)} ${"\u304b\u3089\u3069\u3053\u3078\u3064\u306a\u304c\u308b\u304b"}</div>
                    </div>
                    <div class="tag tag-neutral">${relations.length}${"\u3064\u306a\u304c\u308a"}</div>
                </div>
                <div class="concept-flow-summary mt-4 rounded-[22px] border border-slate-200 bg-white p-4">
                    <div class="text-[11px] font-black tracking-[0.2em] text-blue-700">${"\u30b3\u30a2\u30ce\u30fc\u30c9"}</div>
                    <div class="mt-2 text-lg font-black text-slate-950">${escapeHtml(active.title)}</div>
                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(active.short || "")}</p>
                </div>
                <div class="concept-flow-grid mt-5 grid gap-3">
                    ${relations.map((relation, index) => {
                        const target = conceptMap[relation.target];
                        const targetTitle = target ? target.title : relation.target;
                        const targetShort = target ? target.short : "";
                        return `
                            <article class="concept-relation-card">
                                <div class="flex items-start justify-between gap-3">
                                    <div>
                                        <div class="text-xs font-black tracking-[0.18em] text-slate-500">FLOW 0${index + 1}</div>
                                        <div class="mt-2 text-sm font-black text-slate-900">${escapeHtml(active.title)} ${"\u2192"} ${escapeHtml(targetTitle)}</div>
                                    </div>
                                    <button class="relation-pill" data-action="open-concept" data-concept="${escapeHtml(relation.target)}">${escapeHtml(targetTitle)}</button>
                                </div>
                                <p class="mt-3 text-sm leading-6 text-slate-600">${escapeHtml(relation.label)}</p>
                                ${targetShort ? `<p class="mt-2 text-xs leading-5 text-slate-500">${escapeHtml(targetShort)}</p>` : ""}
                            </article>
                        `;
                    }).join("")}
                </div>
            </div>
        `;
    }

    function renderConceptCompareTabs(active) {
        const relatedItems = [
            active,
            ...asArray(active && active.relations)
                .map((relation) => conceptMap[relation.target])
                .filter(Boolean)
        ].filter((item, index, items) => item && items.findIndex((candidate) => candidate.id === item.id) === index);

        if (relatedItems.length <= 1) {
            return "";
        }

        return `
            <div class="concept-compare-card rounded-[24px] border border-slate-200 bg-white p-4">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <div class="text-[11px] font-black tracking-[0.18em] text-slate-500">QUICK COMPARE</div>
                        <div class="mt-2 text-base font-black text-slate-900">近い概念だけを横で見比べる</div>
                    </div>
                    <div class="tag tag-neutral">${relatedItems.length} tabs</div>
                </div>
                <div class="concept-compare-tabs mt-4 flex flex-wrap gap-2">
                    ${relatedItems.map((concept) => `
                        <button
                            class="concept-compare-tab ${concept.id === active.id ? "concept-compare-tab-active" : ""}"
                            data-action="set-active-concept"
                            data-concept="${concept.id}">
                            ${escapeHtml(concept.title)}
                        </button>
                    `).join("")}
                </div>
                <p class="mt-4 text-sm leading-6 text-slate-600">
                    ${escapeHtml(active.short || "")}
                </p>
            </div>
        `;
    }

    function renderRoleTrackSelector() {
        const activeRole = getActiveRole();
        if (!ROLE_TRACKS.length || !activeRole) {
            return "";
        }
        return `
            <div class="mt-6 space-y-3">
                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">ROLE PATH</div>
                <div class="grid gap-3 lg:grid-cols-3">
                    ${ROLE_TRACKS.map((role) => `
                        <button class="role-card text-left ${role.id === activeRole.id ? "role-card-active" : ""}" data-action="switch-role" data-role="${role.id}">
                            <div class="flex items-center justify-between gap-3">
                                <div class="text-base font-black text-slate-900">${escapeHtml(role.label)}</div>
                                <div class="tag ${role.id === activeRole.id ? "tag-good" : "tag-neutral"}">${role.id === activeRole.id ? "選択中" : "切替"}</div>
                            </div>
                            <p class="mt-3 text-sm leading-6 text-slate-600">${escapeHtml(role.summary)}</p>
                            <div class="mt-4 flex flex-wrap gap-2">
                                ${(role.focusCompetencies || []).map((competencyId) => {
                                    const competency = competencyMap[competencyId];
                                    return competency ? `<span class="tag tag-neutral">${escapeHtml(competency.title)}</span>` : "";
                                }).join("")}
                            </div>
                        </button>
                    `).join("")}
                </div>
            </div>
        `;
    }

    function renderCompetencySnapshot(limit) {
        const items = topCompetencies(limit);
        if (!items.length) {
            return "";
        }
        return items.map((item) => `
            <div class="skill-card">
                <div class="flex items-start justify-between gap-3">
                    <div>
                        <div class="text-sm font-bold text-slate-900">${escapeHtml(item.definition.title)}</div>
                        <p class="mt-1 text-xs leading-6 text-slate-600">${escapeHtml(item.definition.summary)}</p>
                    </div>
                    <div class="tag ${competencyStatusClass(item.status)}">${escapeHtml(competencyStatusLabel(item.status))}</div>
                </div>
                <div class="mt-4 flex items-center justify-between text-xs font-bold uppercase tracking-[0.16em] text-slate-500">
                    <span>Skill</span>
                    <span>${item.percent}%</span>
                </div>
                <div class="skill-meter mt-2">
                    <div class="skill-meter-fill" style="width:${item.percent}%"></div>
                </div>
            </div>
        `).join("");
    }

    function renderSimulationMissionPanel() {
        if (!SIMULATION_MISSIONS.length) {
            return "";
        }
        const activeMission = missionMap[state.visual.currentMissionId] || null;
        return `
            <div class="grid gap-4 xl:grid-cols-[1.08fr_0.92fr]">
                <div class="rounded-[28px] border border-slate-200 bg-slate-50 p-5">
                    <div class="flex items-center justify-between gap-4">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">SIMULATION MISSIONS</div>
                            <div class="mt-2 text-xl font-black text-slate-900">操作課題で条件差をつかむ</div>
                        </div>
                        <div class="tag tag-neutral">${(state.visual.completedMissions || []).length}/${SIMULATION_MISSIONS.length}</div>
                    </div>
                    <div class="mt-5 grid gap-3">
                        ${SIMULATION_MISSIONS.map((mission) => {
                            const competency = competencyMap[mission.competencyId];
                            const completed = (state.visual.completedMissions || []).includes(mission.id);
                            const isActive = state.visual.currentMissionId === mission.id;
                            return `
                                <button class="mission-card text-left ${isActive ? "mission-card-active" : ""}" data-action="apply-sim-mission" data-mission="${mission.id}">
                                    <div class="flex items-start justify-between gap-3">
                                        <div>
                                            <div class="text-sm font-black text-slate-900">${escapeHtml(mission.title)}</div>
                                            <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(mission.summary)}</p>
                                        </div>
                                        <div class="tag ${completed ? "tag-good" : "tag-neutral"}">${completed ? "完了" : "開始"}</div>
                                    </div>
                                    <div class="mt-4 flex flex-wrap gap-2">
                                        ${competency ? `<span class="tag tag-neutral">${escapeHtml(competency.title)}</span>` : ""}
                                        ${mission.conceptId && conceptMap[mission.conceptId] ? `<span class="tag tag-neutral">${escapeHtml(conceptMap[mission.conceptId].title)}</span>` : ""}
                                    </div>
                                </button>
                            `;
                        }).join("")}
                    </div>
                </div>
                <div class="rounded-[28px] border border-slate-200 bg-white p-5">
                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">CURRENT MISSION</div>
                    ${activeMission ? `
                        <div class="mt-2 text-xl font-black text-slate-900">${escapeHtml(activeMission.title)}</div>
                        <p class="mt-3 text-sm leading-7 text-slate-600">${escapeHtml(activeMission.summary)}</p>
                        <ul class="mt-5 space-y-3 text-sm leading-7 text-slate-700">
                            ${(activeMission.checks || []).map((item) => `<li class="mission-check">${escapeHtml(item)}</li>`).join("")}
                        </ul>
                        <div class="mt-5 rounded-2xl bg-blue-50 p-4 text-sm leading-7 text-blue-900">${escapeHtml(activeMission.completionText || "")}</div>
                        <div class="mt-5">
                            <button class="rounded-full bg-slate-900 px-5 py-3 text-sm font-bold text-white" data-action="complete-sim-mission" data-mission="${activeMission.id}">
                                ${(state.visual.completedMissions || []).includes(activeMission.id) ? "完了として保持済み" : "この挙動を理解した"}
                            </button>
                        </div>
                    ` : `
                        <div class="mt-3 rounded-2xl bg-slate-50 p-4 text-sm leading-7 text-slate-600">
                            上の課題を 1 つ選ぶと、推奨条件を反映したうえで見るべきポイントを表示します。
                        </div>
                    `}
                </div>
            </div>
        `;
    }

    function renderSimulationMissionFlowPanel() {
        if (!SIMULATION_MISSIONS.length) {
            return "";
        }
        const activeMission = missionMap[state.visual.currentMissionId] || null;
        return `
            <div class="rounded-[28px] border border-slate-200 bg-slate-50 p-5">
                <div class="flex items-start justify-between gap-4">
                    <div>
                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">SIMULATION MISSIONS</div>
                        <div class="mt-2 text-xl font-black text-slate-900">謫堺ｽ懆ｪｲ鬘後〒譚｡莉ｶ蟾ｮ繧偵▽縺九・</div>
                        <p class="mt-3 text-sm leading-6 text-slate-600">
                            ${activeMission
                                ? "選んだ mission の見どころと完了条件を、そのカード内で続けて確認できます。"
                                : "まず 1 つ選ぶと、そのカードの中に current mission の要点が展開されます。"}
                        </p>
                    </div>
                    <div class="tag tag-neutral">${(state.visual.completedMissions || []).length}/${SIMULATION_MISSIONS.length}</div>
                </div>
                <div class="mission-stack mt-5 grid gap-3">
                    ${SIMULATION_MISSIONS.map((mission) => {
                        const competency = competencyMap[mission.competencyId];
                        const completed = (state.visual.completedMissions || []).includes(mission.id);
                        const isActive = state.visual.currentMissionId === mission.id;
                        return `
                            <article class="mission-card mission-card-shell ${isActive ? "mission-card-active" : ""}">
                                <button class="mission-card-trigger text-left" data-action="apply-sim-mission" data-mission="${mission.id}">
                                    <div class="flex items-start justify-between gap-3">
                                        <div>
                                            <div class="text-sm font-black text-slate-900">${escapeHtml(mission.title)}</div>
                                            <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(mission.summary)}</p>
                                        </div>
                                        <div class="flex flex-wrap items-center justify-end gap-2">
                                            ${isActive ? '<span class="tag tag-good">CURRENT</span>' : ""}
                                            <span class="tag ${completed ? "tag-good" : "tag-neutral"}">${completed ? "螳御ｺ・" : "髢句ｧ・"}</span>
                                        </div>
                                    </div>
                                    <div class="mt-4 flex flex-wrap gap-2">
                                        ${competency ? `<span class="tag tag-neutral">${escapeHtml(competency.title)}</span>` : ""}
                                        ${mission.conceptId && conceptMap[mission.conceptId] ? `<span class="tag tag-neutral">${escapeHtml(conceptMap[mission.conceptId].title)}</span>` : ""}
                                    </div>
                                </button>
                                ${isActive ? `
                                    <div class="mission-card-detail mt-4 border-t border-slate-200 pt-4">
                                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">CURRENT MISSION</div>
                                        <ul class="mt-4 space-y-3 text-sm leading-7 text-slate-700">
                                            ${(mission.checks || []).map((item) => `<li class="mission-check">${escapeHtml(item)}</li>`).join("")}
                                        </ul>
                                        <div class="mt-4 rounded-2xl bg-blue-50 p-4 text-sm leading-7 text-blue-900">${escapeHtml(mission.completionText || "")}</div>
                                        <div class="mt-4 flex flex-wrap items-center gap-3">
                                            <button class="rounded-full bg-slate-900 px-5 py-3 text-sm font-bold text-white" data-action="complete-sim-mission" data-mission="${mission.id}">
                                                ${completed ? "螳御ｺ・→縺励※菫晄戟貂医∩" : "縺薙・謖吝虚繧堤炊隗｣縺励◆"}
                                            </button>
                                        </div>
                                    </div>
                                ` : ""}
                            </article>
                        `;
                    }).join("")}
                </div>
            </div>
        `;
    }

    function renderSimulationMissionFlowPanelClean() {
        if (!SIMULATION_MISSIONS.length) {
            return "";
        }
        const activeMission = missionMap[state.visual.currentMissionId] || null;
        return `
            <div class="rounded-[28px] border border-slate-200 bg-slate-50 p-5">
                <div class="flex items-start justify-between gap-4">
                    <div>
                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">SIMULATION MISSIONS</div>
                        <div class="mt-2 text-xl font-black text-slate-900">${"\u30df\u30c3\u30b7\u30e7\u30f3\u3092\u9078\u3093\u3067\u632f\u308b\u821e\u3044\u3092\u6bd4\u8f03\u3059\u308b"}</div>
                        <p class="mt-3 text-sm leading-6 text-slate-600">
                            ${activeMission
                                ? "\u9078\u3093\u3060\u30df\u30c3\u30b7\u30e7\u30f3\u306e\u898b\u308b\u30dd\u30a4\u30f3\u30c8\u3068\u5b8c\u4e86\u6761\u4ef6\u3092\u3001\u305d\u306e\u30ab\u30fc\u30c9\u5185\u3067\u7d9a\u3051\u3066\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002"
                                : "\u307e\u305a1\u3064\u9078\u3076\u3068\u3001\u305d\u306e\u30ab\u30fc\u30c9\u306e\u4e2d\u306b\u73fe\u5728\u306e\u30df\u30c3\u30b7\u30e7\u30f3\u8981\u70b9\u304c\u5c55\u958b\u3055\u308c\u307e\u3059\u3002"}
                        </p>
                    </div>
                    <div class="tag tag-neutral">${(state.visual.completedMissions || []).length}/${SIMULATION_MISSIONS.length}</div>
                </div>
                <div class="mission-stack mt-5 grid gap-3">
                    ${SIMULATION_MISSIONS.map((mission) => {
                        const competency = competencyMap[mission.competencyId];
                        const completed = (state.visual.completedMissions || []).includes(mission.id);
                        const isActive = state.visual.currentMissionId === mission.id;
                        return `
                            <article class="mission-card mission-card-shell ${isActive ? "mission-card-active" : ""}">
                                <button class="mission-card-trigger text-left" data-action="apply-sim-mission" data-mission="${mission.id}">
                                    <div class="flex items-start justify-between gap-3">
                                        <div>
                                            <div class="text-sm font-black text-slate-900">${escapeHtml(mission.title)}</div>
                                            <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(mission.summary)}</p>
                                        </div>
                                        <div class="flex flex-wrap items-center justify-end gap-2">
                                            ${isActive ? `<span class="tag tag-good">${"\u9078\u629e\u4e2d"}</span>` : ""}
                                            <span class="tag ${completed ? "tag-good" : "tag-neutral"}">${completed ? "\u5b8c\u4e86" : "\u672a\u7740\u624b"}</span>
                                        </div>
                                    </div>
                                    <div class="mt-4 flex flex-wrap gap-2">
                                        ${competency ? `<span class="tag tag-neutral">${escapeHtml(competency.title)}</span>` : ""}
                                        ${mission.conceptId && conceptMap[mission.conceptId] ? `<span class="tag tag-neutral">${escapeHtml(conceptMap[mission.conceptId].title)}</span>` : ""}
                                    </div>
                                </button>
                                ${isActive ? `
                                    <div class="mission-card-detail mt-4 border-t border-slate-200 pt-4">
                                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">${"\u73fe\u5728\u306e\u30df\u30c3\u30b7\u30e7\u30f3"}</div>
                                        <ul class="mt-4 space-y-3 text-sm leading-7 text-slate-700">
                                            ${(mission.checks || []).map((item) => `<li class="mission-check">${escapeHtml(item)}</li>`).join("")}
                                        </ul>
                                        <div class="mt-4 rounded-2xl bg-blue-50 p-4 text-sm leading-7 text-blue-900">${escapeHtml(mission.completionText || "")}</div>
                                        <div class="mt-4 flex flex-wrap items-center gap-3">
                                            <button class="rounded-full bg-slate-900 px-5 py-3 text-sm font-bold text-white" data-action="complete-sim-mission" data-mission="${mission.id}">
                                                ${completed ? "\u5b8c\u4e86\u3068\u3057\u3066\u4fdd\u6301" : "\u7406\u89e3\u3067\u304d\u305f"}
                                            </button>
                                        </div>
                                    </div>
                                ` : ""}
                            </article>
                        `;
                    }).join("")}
                </div>
            </div>
        `;
    }

    function getVisualChartDatasets(chartConfig) {
        const datasets = asArray(chartConfig && chartConfig.datasets);
        if (topicId === "nanoin") {
            return datasets.filter((dataset) => dataset.showLine !== false);
        }
        return datasets;
    }

    function getVisualChartCaption() {
        if (topicId === "nanoin") {
            return "\u8d64\u306f\u8ca0\u8377\u3001\u9752\u306f\u9664\u8377\u3002\u70b9\u3067\u306f\u306a\u304f\u3001\u66f2\u7dda\u306e\u5f62\u3068\u623b\u308a\u65b9\u306e\u9055\u3044\u3092\u898b\u308b\u305f\u3081\u306e\u6982\u5ff5\u56f3\u3067\u3059\u3002";
        }
        return VISUAL_LEARNING.chartCaption || "";
    }

    function refreshVisualCaption() {
        const caption = root.querySelector("[data-visual-caption]");
        if (caption) {
            caption.textContent = getVisualChartCaption();
        }
    }

    function getVisualControlGuide(field) {
        if (topicId === "taver") {
            const guides = {
                material: {
                    focus: ["勾配", "立ち上がり"],
                    note: "試料モデルを変えたら、同じ摩耗メカニズムでも標準比較線との差がどう変わるかを見ます。"
                },
                wearMode: {
                    focus: ["立ち上がり", "増え方の形"],
                    note: "アブレシブは序盤から、凝着は途中から、疲労は潜伏後に変わりやすい形を見ます。"
                },
                wheelType: {
                    focus: ["序盤の勾配", "標準比較線との差"],
                    note: "摩耗輪を変えたら、まず序盤の増え方と標準条件との差を見ます。"
                },
                load: {
                    focus: ["急増の位置", "損傷リスク"],
                    note: "荷重を上げたら単純比例と決めず、どこから悪化が目立つかを見ます。"
                }
            };
            return guides[field] || { focus: [], note: "" };
        }
        const guides = {
            nanoin: {
                material: {
                    focus: ["曲線の形", "残留深さ"],
                    note: "材料モデルを変えたら、まず曲線形状と残留深さの違いを見る。"
                },
                filmThickness: {
                    focus: ["接触深さ", "基板影響リスク"],
                    note: "膜厚を変えたら、膜厚に対する深さ比と基板影響リスクを見る。"
                },
                roughness: {
                    focus: ["浅部ノイズリスク", "接触深さ"],
                    note: "粗さを上げたら、浅部の散りと接触深さの安定性を見る。"
                },
                tipRadius: {
                    focus: ["接触深さ", "浅部ノイズリスク"],
                    note: "先端丸みは最浅部に効くので、浅部の読みがどう崩れるかを見る。"
                }
            },
            xrf: {
                material: {
                    focus: ["主ピーク候補", "スペクトル形状"],
                    note: "サンプルモデルを変えたら、どこにピークが立つかを見る。"
                },
                atmosphere: {
                    focus: ["軽元素の見え方", "低エネルギー側"],
                    note: "雰囲気を変えたら、低エネルギー側と軽元素の見え方を見る。"
                },
                coatingThickness: {
                    focus: ["表面被覆の影響", "主ピーク候補"],
                    note: "被覆厚みを変えたら、ピーク強度の落ち方を見る。"
                },
                acquisitionTime: {
                    focus: ["主ピーク候補", "スペクトル形状"],
                    note: "測定時間を変えたら、山の見えやすさを比較する。"
                }
            }
        };
        const topicGuides = guides[topicId] || {};
        return topicGuides[field] || { focus: [], note: "" };
    }

    function getVisualGuideItems() {
        return [
            {
                field: "material",
                label: VISUAL_LEARNING.materialLabel || "材料モデル"
            },
            ...asArray(VISUAL_LEARNING.controls).map((control) => ({
                field: control.field,
                label: control.label
            }))
        ];
    }

    function getVisualGuideField() {
        const items = getVisualGuideItems();
        const current = state.visual.guideField;
        return items.some((item) => item.field === current) ? current : (items[0] && items[0].field) || "material";
    }

    function getVisualGuideNarration(field, scenario, activeVisualModel) {
        if (topicId === "taver") {
            if (field === "material") {
                return {
                    title: "試料モデルで標準条件との差が変わる",
                    body: activeVisualModel.note || "まずは現在条件と標準比較線の差が、どこで広がるかを見ます。"
                };
            }
            if (field === "wearMode") {
                if (state.visual.wearMode === "adhesive") {
                    return {
                        title: "途中から急増する見え方を確認する",
                        body: "凝着寄りでは、序盤より中盤以降の立ち上がり変化が重要です。常に一定勾配とは限らない点を見ます。"
                    };
                }
                if (state.visual.wearMode === "fatigue") {
                    return {
                        title: "潜伏後に増え方が変わるかを見る",
                        body: "疲労寄りでは、初期の静かな区間と後半の変曲を切り分けます。質量減少だけで寿命まで言い切らない前提で見ます。"
                    };
                }
                return {
                    title: "序盤から増える標準的な見え方を比べる",
                    body: "アブレシブ寄りでは、最初から勾配差が出やすいので、摩耗輪と荷重で立ち上がりがどう変わるかを見ます。"
                };
            }
            if (field === "wheelType") {
                if (state.visual.wheelType === "h22") {
                    return {
                        title: "攻撃性が強く、序盤から差が開きやすい",
                        body: "H-22 はより強い条件として見せやすく、標準比較線との差が早い段階で広がるかを確認します。"
                    };
                }
                if (state.visual.wheelType === "cs10") {
                    return {
                        title: "比較的マイルドで、差は緩やかに出る",
                        body: "CS-10 は穏やかな条件として扱いやすいので、立ち上がりの勾配差が小さくなる見え方を確認します。"
                    };
                }
                return {
                    title: "標準輪としての見え方を基準にする",
                    body: "H-18 を基準に置いて、他の摩耗輪がどの方向にずれるかを比較すると説明しやすくなります。"
                };
            }
            return Number(state.visual.load) >= 1000
                ? {
                    title: "高荷重で急増位置が前倒しになりやすい",
                    body: "荷重を上げると増えやすくなりますが、単純比例と決めず、どこから悪化が目立つかを曲線の形で見ます。"
                }
                : Number(state.visual.load) <= 250
                    ? {
                        title: "低荷重では差が穏やかに出る",
                        body: "250 g では標準比較線との差が小さく見えやすい条件です。差がないのではなく、立ち上がりが遅い点を見ます。"
                    }
                    : {
                        title: "500 g を基準に条件差を読む",
                        body: "まずは標準比較線との差を基準として、荷重変更で勾配と急増位置がどうずれるかを確認します。"
                    };
        }

        if (topicId === "nanoin") {
            if (field === "material") {
                return {
                    title: "材料モデルで曲線の戻り方が変わる",
                    body: activeVisualModel.note || "材料モデルを変えたら、曲線の形と残留深さの変化を先に見ます。"
                };
            }
            if (field === "filmThickness") {
                const ratio = scenario.thickness ? scenario.maxDepth / scenario.thickness : 0;
                return ratio >= 0.3
                    ? {
                        title: "膜に対して深く入り始めている",
                        body: `最大深さが膜厚の ${(ratio * 100).toFixed(0)}% 付近です。膜だけでなく、基板影響リスクも一緒に確認する段階です。`
                    }
                    : {
                        title: "まだ膜寄りの読みを保ちやすい",
                        body: `最大深さは膜厚の ${(ratio * 100).toFixed(0)}% 付近です。まずは接触深さが膜厚に対してどこまで近づくかを見ます。`
                    };
            }
            if (field === "roughness") {
                return Number(state.visual.roughness) >= 12
                    ? {
                        title: "浅部ノイズを材料差と誤読しやすい",
                        body: "粗さが大きいので、最浅部の散りを材料固有の depth dependence と決める前に、表面状態の寄与を疑います。"
                    }
                    : {
                        title: "浅部ノイズは比較的抑えやすい",
                        body: "粗さは中程度なので、浅部の読みはまだ安定域にあります。次は先端丸みと合わせて見ます。"
                    };
            }
            if (field === "tipRadius") {
                return Number(state.visual.tipRadius) >= 70
                    ? {
                        title: "先端丸みが最浅部をなだらかにする",
                        body: "鋭い差が出にくくなるので、浅部の接触深さをそのまま材料差として読むと外しやすくなります。"
                    }
                    : {
                        title: "先端はまだ鋭めで浅部を拾いやすい",
                        body: "最浅部の反応が出やすい条件です。粗さ由来の散りと区別しながら見ます。"
                    };
            }
        }

        if (field === "material") {
            return {
                title: "材料モデルでピーク構成が変わる",
                body: activeVisualModel.note || "まずは主ピークの位置と、どのエネルギー帯が強いかを見ます。"
            };
        }
        if (field === "atmosphere") {
            return state.visual.atmosphere === "helium"
                ? {
                    title: "低エネルギー側を見やすくする条件",
                    body: "He パージでは軽元素側が持ち上がりやすくなります。まずは低エネルギー側の見え方を確認します。"
                }
                : {
                    title: "空気中では軽元素側が落ちやすい",
                    body: "空気中では低エネルギー側が弱くなりやすいので、見えないことを即ゼロと解釈しないことが重要です。"
                };
        }
        if (field === "coatingThickness") {
            return Number(state.visual.coatingThickness) >= 20
                ? {
                    title: "表面層が主ピークの見え方を変えやすい",
                    body: "表面層が厚いので、主ピークや軽元素の見え方に表面の寄与が混ざりやすい条件です。"
                }
                : {
                    title: "表面層の影響はまだ限定的",
                    body: "表面層が薄いので、まずは母材側のピーク構成を読みやすい条件です。"
                };
        }
        return Number(state.visual.acquisitionTime) <= 10
            ? {
                title: "短時間でピーク判定が不安定になりやすい",
                body: "取得時間が短いので、ピーク高さの差を材料差と決める前に統計ゆらぎを疑います。"
            }
            : {
                title: "取得時間に少し余裕がある",
                body: "ピーク高さの比較がしやすい条件です。次はマトリクス影響と表面層の寄与を切り分けます。"
            };
    }

    function renderVisualGuideDeck(scenario, activeVisualModel) {
        const guideField = getVisualGuideField();
        const guide = getVisualControlGuide(guideField);
        const narration = getVisualGuideNarration(guideField, scenario, activeVisualModel);

        return `
            <div class="visual-guide-card rounded-[24px] border border-slate-200 bg-white p-4">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <div class="text-[11px] font-black tracking-[0.18em] text-slate-500">READING GUIDE</div>
                        <div class="mt-2 text-base font-black text-slate-900">どの違いを見比べるかを固定する</div>
                    </div>
                    <div class="tag tag-neutral">${escapeHtml(getVisualGuideItems().find((item) => item.field === guideField)?.label || "")}</div>
                </div>
                <div class="visual-guide-tabs mt-4 flex flex-wrap gap-2">
                    ${getVisualGuideItems().map((item) => `
                        <button
                            class="visual-guide-tab ${item.field === guideField ? "visual-guide-tab-active" : ""}"
                            data-action="set-visual-guide"
                            data-field="${item.field}">
                            ${escapeHtml(item.label)}
                        </button>
                    `).join("")}
                </div>
                <div class="mt-4">
                    <div class="text-sm font-black text-slate-900" data-visual-guide-title>${escapeHtml(narration.title)}</div>
                    <p class="mt-2 text-sm leading-6 text-slate-600" data-visual-guide-body>${escapeHtml(narration.body)}</p>
                    <div class="mt-4 text-[11px] font-black tracking-[0.16em] text-slate-500">WATCH HERE</div>
                    <div class="mt-2 flex flex-wrap gap-2" data-visual-guide-focus>
                        ${renderVisualFocusChips(guide.focus)}
                    </div>
                    ${guide.note ? `<p class="mt-2 text-xs leading-5 text-slate-500" data-visual-guide-note>${escapeHtml(guide.note)}</p>` : `<p class="mt-2 text-xs leading-5 text-slate-500" data-visual-guide-note></p>`}
                </div>
            </div>
        `;
    }

    function refreshVisualGuide() {
        const scenario = getVisualScenario();
        const activeVisualModel = VISUAL_MODELS[state.visual.material] || {};
        const guideField = getVisualGuideField();
        const guide = getVisualControlGuide(guideField);
        const narration = getVisualGuideNarration(guideField, scenario, activeVisualModel);
        const title = root.querySelector("[data-visual-guide-title]");
        const body = root.querySelector("[data-visual-guide-body]");
        const focus = root.querySelector("[data-visual-guide-focus]");
        const note = root.querySelector("[data-visual-guide-note]");
        const tag = root.querySelector(".visual-guide-card .tag");
        if (!title || !body || !focus || !note || !tag) {
            return;
        }
        title.textContent = narration.title;
        body.textContent = narration.body;
        focus.innerHTML = renderVisualFocusChips(guide.focus);
        note.textContent = guide.note || "";
        tag.textContent = (getVisualGuideItems().find((item) => item.field === guideField)?.label) || "";
        root.querySelectorAll("[data-action=\"set-visual-guide\"]").forEach((button) => {
            button.classList.toggle("visual-guide-tab-active", button.dataset.field === guideField);
        });
    }

    function renderVisualFocusChips(items) {
        return asArray(items).map((item) => `<span class="visual-focus-chip">${escapeHtml(item)}</span>`).join("");
    }

    function renderHeader() {
        const intro = introSummary();
        const activeRole = getActiveRole();
        const currentSection = APP_SECTIONS[sectionIndex[state.currentSection]] || APP_SECTIONS[0] || { label: "導入" };
        const started = hasMeaningfulProgress();
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
                        ${started ? `
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
                                    <dt class="font-bold text-slate-700">現在の役割</dt>
                                    <dd class="mt-1 text-slate-600">${escapeHtml(activeRole ? activeRole.label : "標準")}</dd>
                                </div>
                                <div class="metric-card p-4">
                                    <dt class="font-bold text-slate-700">現在地</dt>
                                    <dd class="mt-1 text-slate-600">${escapeHtml(currentSection.label)}</dd>
                                </div>
                            </dl>
                        ` : `
                            <div class="text-xs font-bold uppercase tracking-[0.2em] text-slate-500">最初はシンプルに開始</div>
                            <h2 class="mt-2 text-2xl font-black text-slate-900">まずは 3 問だけ答える</h2>
                            <p class="mt-4 text-sm leading-7 text-slate-600">
                                最初のセルフチェックが終わるまでは、進捗や詳細スキルは出しません。今はどこから始めるかだけ決めれば十分です。
                            </p>
                            <div class="mt-5 rounded-2xl bg-slate-50 p-4 text-sm leading-7 text-slate-700">
                                セルフチェック完了後に、おすすめ導線と役割別の進み方を出します。
                            </div>
                        `}
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
        const answeredCount = introAnsweredCount();
        const currentQuestion = nextIntroQuestion();
        const activeRole = getActiveRole();
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">START HERE</div>
                    <h2 class="mt-2 text-2xl font-black">${escapeHtml(INTRO_OVERVIEW_CARDS[0] ? INTRO_OVERVIEW_CARDS[0].title : `${topicName}を学ぶ`)}</h2>
                    <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                        ${escapeHtml(HERO.description || (INTRO_OVERVIEW_CARDS[0] && INTRO_OVERVIEW_CARDS[0].body) || "")}
                    </p>
                    <div class="mt-5 flex flex-wrap gap-2">
                        ${INTRO_OVERVIEW_CARDS.slice(0, 3).map((card) => `<span class="tag tag-neutral">${escapeHtml(card.title)}</span>`).join("")}
                    </div>
                </div>

                <div class="panel-card p-6 sm:p-8">
                    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">SELF CHECK</div>
                            <h3 class="mt-2 text-2xl font-black">最初に 3 問だけ答える</h3>
                        </div>
                        <div class="rounded-2xl bg-blue-50 px-4 py-3 text-sm font-bold text-blue-700">${answeredCount} / ${INTRO_SELF_CHECK.length}</div>
                    </div>
                    <div class="mt-6 space-y-6">
                        ${currentQuestion && !selfCheckComplete() ? `
                            <div class="rounded-3xl border border-slate-200 p-5">
                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">QUESTION ${Math.min(answeredCount + 1, INTRO_SELF_CHECK.length)}</div>
                                <p class="mt-3 text-base font-bold leading-8 text-slate-800">${escapeHtml(currentQuestion.prompt)}</p>
                                <div class="mt-5 grid gap-3 sm:grid-cols-3">
                                    ${currentQuestion.options.map((option) => `
                                        <label class="diagnosis-choice ${Number(state.introCheck[currentQuestion.id]) === option.value ? "border-blue-400 bg-blue-50" : ""}">
                                            <input class="sr-only" type="radio" name="intro-${currentQuestion.id}" value="${option.value}" data-action="set-intro-answer" data-question="${currentQuestion.id}">
                                            <span class="text-sm font-bold text-slate-800">${escapeHtml(option.label)}</span>
                                        </label>
                                    `).join("")}
                                </div>
                                <p class="mt-4 text-xs leading-6 text-slate-500">
                                    回答すると自動で保存されます。残り ${Math.max(INTRO_SELF_CHECK.length - answeredCount - 1, 0)} 問です。
                                </p>
                            </div>
                        ` : ""}
                    </div>
                    ${selfCheckComplete() ? `
                        <div class="mt-6 rounded-3xl bg-slate-50 p-5">
                            <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                                <div>
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">現在のおすすめ導線</div>
                                    <p class="mt-3 text-sm leading-7 text-slate-700">${escapeHtml(summary.text)}</p>
                                </div>
                                <div class="tag tag-good">${escapeHtml(summary.label)}</div>
                            </div>
                            <div class="mt-4 flex flex-wrap gap-3">
                                ${renderSmartAction(topCompetencies(1)[0] && topCompetencies(1)[0].definition.nextStep, topCompetencies(1)[0] && topCompetencies(1)[0].definition.nextStep && topCompetencies(1)[0].definition.nextStep.label, "rounded-full bg-slate-900 px-4 py-3 text-sm font-bold text-white")}
                                <button class="rounded-full border border-slate-300 bg-white px-4 py-3 text-sm font-bold text-slate-700" data-action="goto-section" data-section="diagnosis">誤解診断へ進む</button>
                                <button class="rounded-full border border-slate-300 bg-white px-4 py-3 text-sm font-bold text-slate-700" data-action="reset-intro-check">セルフチェックをやり直す</button>
                            </div>
                        </div>
                    ` : ""}
                </div>

                ${selfCheckComplete() && activeRole ? `
                    <div class="panel-card p-6 sm:p-8">
                        <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                            <div>
                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">ROLE BLUEPRINT</div>
                                <h2 class="mt-2 text-2xl font-black">${escapeHtml(activeRole.label)}向けの進み方</h2>
                                <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">${escapeHtml(activeRole.summary)}</p>
                            </div>
                            <div class="tag tag-good">${escapeHtml(activeRole.label)}</div>
                        </div>
                        ${renderRoleTrackSelector()}
                        <div class="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-5">
                            <div class="text-sm font-bold text-slate-900">続ける人向けの詳細</div>
                            <div class="mt-4 grid gap-4 md:grid-cols-2">
                                ${topCompetencies(2).map((item) => `
                                    <div class="skill-card">
                                        <div class="text-sm font-black text-slate-900">${escapeHtml(item.definition.title)}</div>
                                        <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(item.definition.summary)}</p>
                                        <div class="mt-4">${renderSmartAction(item.definition.nextStep, item.definition.nextStep && item.definition.nextStep.label, "rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700")}</div>
                                    </div>
                                `).join("")}
                            </div>
                        </div>
                    </div>
                ` : ""}

                ${selfCheckComplete() ? `
                    <div class="panel-card p-6 sm:p-8">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">VISUAL EXPLAINERS</div>
                            <h3 class="mt-2 text-2xl font-black">図解でつかむ</h3>
                            <p class="mt-3 text-sm leading-7 text-slate-600">セルフチェック後は、そのまま主要な図解を見られるようにしています。</p>
                        </div>
                        <div class="mt-6">
                            ${renderFigureCards()}
                        </div>
                    </div>
                ` : ""}
            </section>
        `;
    }

    function renderPrincipleSection() {
        const quickFacts = asArray(PRINCIPLE.quickFacts).slice(0, 4);
        const steps = asArray(PRINCIPLE.steps).slice(0, 4);
        const details = asArray(PRINCIPLE.details).slice(0, 3);

        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-blue-700">${escapeHtml(PRINCIPLE.eyebrow || "MEASUREMENT PRINCIPLE")}</div>
                            <h2 class="mt-2 text-2xl font-black">${escapeHtml(PRINCIPLE.title || "測定原理をつかむ")}</h2>
                            <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                                ${escapeHtml(PRINCIPLE.description || "この section では、装置が何を入れて、何を返してきて、どこを解釈の支点にするかを整理します。")}
                            </p>
                        </div>
                        <div class="tag tag-neutral">${escapeHtml(topicName)}</div>
                    </div>

                    <div class="principle-grid mt-6">
                        <div class="principle-scene-card">
                            ${renderPrincipleScene(PRINCIPLE.scene)}
                        </div>
                        <div class="principle-side-stack">
                            ${quickFacts.length ? `
                                <div class="principle-side-card">
                                    <div class="text-[11px] font-black tracking-[0.18em] text-slate-500">WHAT TO WATCH</div>
                                    <div class="mt-4 grid gap-3">
                                        ${quickFacts.map((item) => `
                                            <article class="principle-fact-card">
                                                <div class="text-sm font-black text-slate-900">${escapeHtml(item.label || "")}</div>
                                                <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(item.body || "")}</p>
                                            </article>
                                        `).join("")}
                                    </div>
                                </div>
                            ` : ""}
                            ${PRINCIPLE.callout ? `
                                <div class="principle-callout">
                                    <div class="text-[11px] font-black tracking-[0.18em] text-blue-700">WHY IT MATTERS</div>
                                    <div class="mt-2 text-lg font-black text-slate-950">${escapeHtml(PRINCIPLE.callout.title || "")}</div>
                                    <p class="mt-3 text-sm leading-7 text-slate-700">${escapeHtml(PRINCIPLE.callout.body || "")}</p>
                                </div>
                            ` : ""}
                        </div>
                    </div>

                    ${steps.length ? `
                        <div class="principle-step-grid mt-6">
                            ${steps.map((step) => `
                                <article class="principle-step-card">
                                    <div class="principle-step-badge">${escapeHtml(step.step || "")}</div>
                                    <div class="mt-3 text-base font-black text-slate-900">${escapeHtml(step.title || "")}</div>
                                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(step.body || "")}</p>
                                </article>
                            `).join("")}
                        </div>
                    ` : ""}

                    ${details.length ? `
                        <div class="principle-detail-grid mt-6">
                            ${details.map((item) => `
                                <article class="principle-detail-card">
                                    <div class="text-sm font-black text-slate-900">${escapeHtml(item.title || "")}</div>
                                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(item.body || "")}</p>
                                </article>
                            `).join("")}
                        </div>
                    ` : ""}

                    <div class="mt-6 flex flex-wrap gap-3">
                        <button class="rounded-full bg-slate-900 px-4 py-3 text-sm font-bold text-white" data-action="goto-section" data-section="concepts">概念比較へ進む</button>
                        <button class="rounded-full border border-slate-300 bg-white px-4 py-3 text-sm font-bold text-slate-700" data-action="goto-section" data-section="visual">条件比較を見る</button>
                    </div>
                </div>
            </section>
        `;
    }

    function renderConceptSection() {
        const active = getActiveConcept();
        const relations = asArray(active && active.relations);
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                        <div>
                            <div class="text-xs font-bold tracking-[0.18em] text-blue-700">CONCEPT MAP</div>
                            <h2 class="mt-2 text-2xl font-black">中核概念を動きと関係でつかむ</h2>
                            <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                                ノードをタップすると、初学者向け説明と一歩踏み込んだ説明を切り替えられます。
                                単語単体ではなく、何が動きの起点で、どこへ効くかを順番で見てください。
                            </p>
                        </div>
                        <div class="inline-flex rounded-full bg-slate-100 p-1">
                            <button class="rounded-full px-4 py-2 text-sm font-bold ${state.conceptLevel === "basic" ? "bg-white text-blue-700 shadow-sm" : "text-slate-600"}" data-action="set-concept-level" data-level="basic">初学者向け</button>
                            <button class="rounded-full px-4 py-2 text-sm font-bold ${state.conceptLevel === "advanced" ? "bg-white text-blue-700 shadow-sm" : "text-slate-600"}" data-action="set-concept-level" data-level="advanced">少し踏み込む</button>
                        </div>
                    </div>
                    <div class="concept-layout-stack mt-6 space-y-4">
                        <div class="concept-node-rail rounded-[28px] border border-slate-200 bg-slate-50 p-4">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">NODE RAIL</div>
                            <div class="mt-3 concept-node-grid flex gap-3">
                            ${CONCEPTS.map((concept) => `
                                <button class="concept-node p-5 text-left ${concept.id === active.id ? "concept-node-active" : ""} ${isRelatedConcept(concept.id) ? "concept-node-related" : ""}" data-action="set-active-concept" data-concept="${concept.id}">
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">NODE</div>
                                    <div class="mt-2 text-lg font-black text-slate-900">${escapeHtml(concept.title)}</div>
                                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(concept.short)}</p>
                                </button>
                            `).join("")}
                            </div>
                        </div>
                        <aside class="panel-card-soft concept-focus-panel rounded-[28px] border border-blue-100 p-6">
                            <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                                <div>
                                    <div class="text-xs font-bold tracking-[0.18em] text-blue-700">ACTIVE NODE</div>
                                    <h3 class="mt-2 text-2xl font-black text-slate-900">${escapeHtml(active.title)}</h3>
                                    <p class="mt-4 text-sm leading-7 text-slate-700">${escapeHtml(state.conceptLevel === "basic" ? active.beginner : active.advanced)}</p>
                                </div>
                                <div class="flex flex-wrap gap-2">
                                    <span class="tag tag-neutral">${relations.length} relations</span>
                                </div>
                            </div>
                            <div class="mt-6">
                                ${renderConceptExplainer(active)}
                            </div>
                            <div class="mt-4">
                                ${renderConceptCompareTabs(active)}
                            </div>
                            <div class="concept-detail-grid mt-6 grid gap-4">
                                <div class="concept-reference-card">
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">REFERENCE SNAPSHOT</div>
                                    <div class="mt-3">
                                        ${renderConceptSupplement(active)}
                                    </div>
                                </div>
                                <div>
                                    ${renderConceptConstellationClean(active)}
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
        const controls = asArray(VISUAL_LEARNING.controls);
        const insights = asArray(scenario && scenario.insights);
        const activeVisualModel = VISUAL_MODELS[state.visual.material] || {};
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="text-xs font-bold tracking-[0.18em] text-emerald-700">VISUAL LEARNING</div>
                    <h2 class="mt-2 text-2xl font-black">${escapeHtml(VISUAL_LEARNING.title || "条件を動かして、どこを読むべきかを見る")}</h2>
                    <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                        ${escapeHtml(VISUAL_LEARNING.description || "ここでは精密な実測再現ではなく、解釈の軸をつかむための概念モデルを使います。スライダーを動かし、どの条件でどの誤読が起きやすいかを確認してください。")}
                    </p>
                    <div class="visual-workbench mt-6">
                        <div class="visual-cockpit-card rounded-[28px] border border-slate-200 bg-white p-5">
                            <div class="flex items-start justify-between gap-4">
                                <div>
                                    <div class="text-xs font-bold tracking-[0.18em] text-slate-500">VISUAL COCKPIT</div>
                                    <div class="mt-2 text-xl font-black text-slate-900">グラフの横で選択肢を変える</div>
                                </div>
                                <div class="tag tag-good">${escapeHtml(activeVisualModel.label || "")}</div>
                            </div>
                            <div class="visual-cockpit-grid mt-5 grid gap-5">
                                <div class="visual-figure-column space-y-4">
                                    <div class="visual-metrics-grid grid gap-3 sm:grid-cols-2">
                                        ${(scenario.metrics || []).map((metric, index) => `
                                            <div class="metric-card p-4">
                                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500" data-visual-metric-label="${index}">${escapeHtml(metric.label)}</div>
                                                <div class="mt-2 text-2xl font-black ${metric.tone ? metricToneClass(metric.tone) : "text-slate-900"}" data-visual-metric-value="${index}">${escapeHtml(String(metric.value))}</div>
                                            </div>
                                        `).join("")}
                                    </div>
                                    <div class="visual-chart-panel rounded-[24px] bg-slate-50 p-4">
                                        <div class="chart-wrap">
                                            <canvas id="visualChart"></canvas>
                                        </div>
                                    </div>
                                    <div class="visual-inline-controls grid gap-3">
                                        ${controls.map((control) => `
                                            <div class="visual-control-item">
                                                <div class="flex items-center justify-between gap-3 text-sm font-bold text-slate-800">
                                                    <span>${escapeHtml(control.label)}</span>
                                                    <span class="visual-control-value" data-visual-control-value="${control.field}">${escapeHtml(typeof control.formatValue === "function" ? control.formatValue(state.visual[control.field], scenario) : String(state.visual[control.field]))}</span>
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
                                                <div class="mt-3">
                                                    <div class="text-[11px] font-black tracking-[0.16em] text-slate-500">WATCH HERE</div>
                                                    <div class="mt-2 flex flex-wrap gap-2">
                                                        ${renderVisualFocusChips(getVisualControlGuide(control.field).focus)}
                                                    </div>
                                                    ${getVisualControlGuide(control.field).note
                                                        ? `<p class="mt-2 text-xs leading-5 text-slate-500">${escapeHtml(getVisualControlGuide(control.field).note)}</p>`
                                                        : ""}
                                                </div>
                                            </div>
                                        `).join("")}
                                    </div>
                                    <p class="text-xs leading-6 text-slate-500" data-visual-caption>
                                        ${escapeHtml(VISUAL_LEARNING.chartCaption || "赤: 負荷、青: 除荷、点: hmax / hc / hf。数値そのものより「どこが解釈の支点か」を見るための概念図です。")}
                                    </p>
                                </div>
                                <aside class="visual-side-rail space-y-4">
                                    <div class="visual-controls-card rounded-[24px] bg-slate-50 p-4">
                                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">CONTROL DECK</div>
                                        <div class="mt-2 text-lg font-black text-slate-900">どの選択肢がどこを変えるか</div>
                                        <div class="mt-4">
                                            <div class="text-sm font-bold text-slate-800">${escapeHtml(VISUAL_LEARNING.materialLabel || "材料モデル")}</div>
                                            <div class="visual-material-grid mt-3 grid gap-2">
                                                ${Object.entries(VISUAL_MODELS).map(([key, model]) => `
                                                    <button class="diagnosis-choice visual-material-choice ${state.visual.material === key ? "border-blue-400 bg-blue-50" : ""}" data-action="set-material" data-material="${key}">
                                                        <div class="text-sm font-bold text-slate-900">${escapeHtml(model.label)}</div>
                                                    </button>
                                                `).join("")}
                                            </div>
                                            <div class="visual-active-note mt-3 rounded-2xl bg-white p-4">
                                                <div class="text-sm font-bold text-slate-900">${escapeHtml(activeVisualModel.label || "")}</div>
                                                <p class="mt-1 text-sm leading-6 text-slate-600">${escapeHtml(activeVisualModel.note || "")}</p>
                                                <div class="mt-3">
                                                    <div class="text-[11px] font-black tracking-[0.16em] text-slate-500">WATCH HERE</div>
                                                    <div class="mt-2 flex flex-wrap gap-2">
                                                        ${renderVisualFocusChips(getVisualControlGuide("material").focus)}
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="mt-3">
                                                ${renderVisualGuideDeck(scenario, activeVisualModel)}
                                            </div>
                                        </div>
                                    </div>
                                </aside>
                            </div>
                        </div>
                        <div class="mt-5 grid gap-4 sm:grid-cols-3">
                            ${insights.map((insight, index) => `
                                <div class="rounded-3xl bg-slate-50 p-5">
                                    <div class="text-sm font-bold text-slate-900" data-visual-insight-title="${index}">${escapeHtml(insight.title)}</div>
                                    <p class="mt-2 text-sm leading-7 text-slate-600" data-visual-insight-body="${index}">${escapeHtml(insight.body)}</p>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                    <div class="mt-6">
                        ${renderSimulationMissionFlowPanelClean()}
                    </div>
                </div>
            </section>
        `;
    }

    function renderDiagnosisSection() {
        const questions = asArray(orderedDiagnosisQuestions());
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
        const queue = buildQuestionQueue();
        const mediaTarget = getPrimaryMediaLink();
        const visualMission = getRecommendedVisualMission();
        const aiMessages = asArray(state.ai && state.ai.messages);
        return `
            <section class="space-y-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="grid gap-6 lg:grid-cols-[1.08fr_0.92fr]">
                        <div class="space-y-5">
                            <div>
                                <div class="text-xs font-bold tracking-[0.18em] text-blue-700">LEARNING COACH</div>
                                <h2 class="mt-2 text-2xl font-black">会話より先に、次の行動を出す</h2>
                                <p class="mt-3 text-sm leading-7 text-slate-600">
                                    まずは今の役割と弱点に合わせて、次の 5 問、見直す図、参照資料を即実行できる形で出します。自由質問はその下で補助的に使います。
                                </p>
                            </div>

                            <div class="grid gap-3 md:grid-cols-3">
                                <button class="coach-action ${state.ai.actionPanel === "questions" ? "coach-action-active" : ""} text-left" data-action="set-ai-action-panel" data-panel="questions">
                                    <div class="text-sm font-black text-slate-900">次の5問</div>
                                    <p class="mt-2 text-sm leading-6 text-slate-600">未回答と弱点から、今やるべき設問を並べます。</p>
                                </button>
                                <button class="coach-action text-left" data-action="launch-visual-review">
                                    <div class="text-sm font-black text-slate-900">この図を見直す</div>
                                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(visualMission ? visualMission.title : "図解セクションへ移動")}</p>
                                </button>
                                <button class="coach-action text-left" data-action="open-primary-media">
                                    <div class="text-sm font-black text-slate-900">この動画を見る</div>
                                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(mediaTarget ? mediaTarget.title : "利用可能な参考資料を開きます")}</p>
                                </button>
                            </div>

                            <div class="rounded-[30px] border border-slate-200 bg-slate-50 p-5">
                                <div class="flex items-center justify-between gap-4">
                                    <div>
                                        <div class="text-xs font-bold tracking-[0.18em] text-slate-500">ACTION QUEUE</div>
                                        <div class="mt-2 text-xl font-black text-slate-900">今やる 5 項目</div>
                                    </div>
                                    <div class="tag tag-neutral">${queue.length} items</div>
                                </div>
                                <div class="mt-5 space-y-3">
                                    ${queue.map((item, index) => `
                                        <div class="rounded-2xl border border-slate-200 bg-white p-4">
                                            <div class="flex items-start justify-between gap-3">
                                                <div>
                                                    <div class="text-xs font-bold tracking-[0.16em] text-slate-500">STEP ${index + 1}</div>
                                                    <div class="mt-2 text-sm font-black leading-7 text-slate-900">${escapeHtml(item.title)}</div>
                                                    <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(item.detail)}</p>
                                                </div>
                                                ${item.section === "concepts" && item.conceptId
                                                    ? `<button class="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700" data-action="open-concept" data-concept="${item.conceptId}">${escapeHtml(item.buttonLabel)}</button>`
                                                    : `<button class="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700" data-action="goto-section" data-section="${item.section}">${escapeHtml(item.buttonLabel)}</button>`
                                                }
                                            </div>
                                        </div>
                                    `).join("")}
                                </div>
                            </div>

                            <div class="rounded-3xl border border-slate-200 p-5">
                                <div class="text-sm font-bold text-slate-900">自由質問に切り替えるときの候補</div>
                                <div class="mt-4 flex flex-wrap gap-3">
                                    ${AI_SUGGESTED_PATHS.map((prompt) => `
                                        <button class="rounded-full border border-slate-300 bg-white px-4 py-3 text-sm font-bold text-slate-700" data-action="send-ai-suggestion" data-prompt="${escapeHtml(prompt)}">${escapeHtml(prompt)}</button>
                                    `).join("")}
                                </div>
                            </div>
                        </div>

                        <div class="space-y-4">
                            <div class="rounded-3xl bg-slate-50 p-5">
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

                            <div class="rounded-[30px] border border-slate-200 bg-slate-50 p-4 sm:p-5">
                                <div class="max-h-[420px] space-y-3 overflow-y-auto pr-1">
                                    ${aiMessages.map((message) => `
                                        <div class="chat-bubble ${message.role === "user" ? "chat-user ml-auto" : "chat-assistant"}">
                                            <div class="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-slate-500">${message.role === "user" ? "YOU" : message.mode === "gemini" ? "AI" : "LOCAL COACH"}</div>
                                            <div class="space-y-3 text-sm leading-7 text-slate-700">${formatTextBlock(message.content)}</div>
                                            ${asArray(message.followUps).length ? `
                                                <div class="mt-4 flex flex-wrap gap-2">
                                                    ${asArray(message.followUps).map((follow) => `
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
                                <label class="text-sm font-bold text-slate-900" for="aiPrompt">自由質問を書く</label>
                                <textarea id="aiPrompt" class="mt-3 min-h-[140px] w-full rounded-3xl border border-slate-300 px-4 py-4 text-sm leading-7" placeholder="${escapeHtml(AI_UI.textareaPlaceholder || "例: 荷重-変位曲線の除荷勾配とヤング率の関係を、硬さとの違いも含めて説明してください。")}">${escapeHtml(state.ai.input)}</textarea>
                                <div class="mt-4 flex items-center justify-between gap-4">
                                    <p class="text-xs leading-6 text-slate-500">即実行アクションで足りないときだけ、自由質問に切り替えてください。</p>
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
        const activeRole = getActiveRole();
        const competencyItems = sortedCompetencyStates();
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
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">現在の役割</div>
                            <div class="mt-3 text-sm leading-7 text-slate-700">
                                ${escapeHtml(activeRole ? `${activeRole.label}: ${activeRole.summary}` : "標準導線")}
                            </div>
                        </div>
                        <div class="metric-card p-5">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">誤解が出やすかった点</div>
                            <div class="mt-3 flex flex-wrap gap-2">
                                ${revisit.length ? revisit.map((item) => `<span class="tag tag-weak">${escapeHtml(item)}</span>`).join("") : '<span class="tag tag-good">まだ未診断または大きな偏りなし</span>'}
                            </div>
                        </div>
                        <div class="metric-card p-5">
                            <div class="text-xs font-bold tracking-[0.18em] text-slate-500">操作課題</div>
                            <div class="mt-3 text-sm leading-7 text-slate-700">
                                ${(state.visual.completedMissions || []).length
                                    ? `${(state.visual.completedMissions || []).length} / ${SIMULATION_MISSIONS.length} 課題を完了`
                                    : "まだ未完了です。図解セクションでミッションを 1 つ選んでください。"}
                            </div>
                        </div>
                    </div>

                    <div class="mt-6 rounded-[30px] border border-slate-200 bg-slate-50 p-6">
                        <div class="flex items-center justify-between gap-4">
                            <div>
                                <div class="text-xs font-bold tracking-[0.18em] text-slate-500">SKILL PROGRESS</div>
                                <div class="mt-2 text-2xl font-black text-slate-900">competency ごとの進捗</div>
                            </div>
                            <div class="tag tag-neutral">${progressPercent()}%</div>
                        </div>
                        <div class="mt-5 grid gap-4 lg:grid-cols-2">
                            ${competencyItems.map((item) => `
                                <div class="skill-card">
                                    <div class="flex items-start justify-between gap-4">
                                        <div>
                                            <div class="text-sm font-black text-slate-900">${escapeHtml(item.definition.title)}</div>
                                            <p class="mt-2 text-sm leading-6 text-slate-600">${escapeHtml(item.definition.summary)}</p>
                                        </div>
                                        <div class="tag ${competencyStatusClass(item.status)}">${escapeHtml(competencyStatusLabel(item.status))}</div>
                                    </div>
                                    <div class="mt-4 flex items-center justify-between text-xs font-bold uppercase tracking-[0.16em] text-slate-500">
                                        <span>progress</span>
                                        <span>${item.percent}%</span>
                                    </div>
                                    <div class="skill-meter mt-2">
                                        <div class="skill-meter-fill" style="width:${item.percent}%"></div>
                                    </div>
                                    <div class="mt-4 flex flex-wrap gap-2">
                                        ${(item.definition.conceptIds || []).map((conceptId) => conceptMap[conceptId] ? `<span class="tag tag-neutral">${escapeHtml(conceptMap[conceptId].title)}</span>` : "").join("")}
                                    </div>
                                    <div class="mt-4">
                                        ${renderSmartAction(item.definition.nextStep, item.definition.nextStep && item.definition.nextStep.label, "rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700")}
                                    </div>
                                </div>
                            `).join("")}
                        </div>
                    </div>

                    <div class="mt-6 rounded-[30px] bg-slate-50 p-6">
                        <div class="text-sm font-bold text-slate-900">次にやるとよいこと</div>
                        <div class="mt-4 grid gap-3 md:grid-cols-3">
                            ${topCompetencies(3).map((item) => renderSmartAction(item.definition.nextStep, item.definition.nextStep && item.definition.nextStep.label, "rounded-2xl bg-white px-4 py-4 text-left text-sm font-bold text-slate-800")).join("")}
                        </div>
                    </div>

                    <div class="mt-6 rounded-[30px] border border-slate-200 bg-white p-6">
                        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                            <div>
                                <div class="text-sm font-bold text-slate-900">参考資料</div>
                                <p class="mt-2 text-sm leading-6 text-slate-600">必要な人だけ外部教材を開く構成にしています。</p>
                            </div>
                            <button class="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-bold text-slate-700" data-action="toggle-ui-panel" data-panel="showResources">
                                ${state.ui && state.ui.showResources ? "参考資料を閉じる" : "参考資料を開く"}
                            </button>
                        </div>
                        ${state.ui && state.ui.showResources ? `
                            <div class="mt-5">
                                ${renderMediaSection()}
                            </div>
                        ` : ""}
                    </div>
                </div>
            </section>
        `;
    }

    function renderSection() {
        switch (state.currentSection) {
            case "intro":
                return renderIntroSection();
            case "principle":
                return renderPrincipleSection();
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

    function renderFatalError(error) {
        const message = error && error.message ? error.message : "unknown error";
        root.innerHTML = `
            <div class="mx-auto max-w-3xl px-4 py-10 sm:px-6">
                <div class="panel-card p-6 sm:p-8">
                    <div class="text-xs font-bold tracking-[0.18em] text-rose-700">RENDER ERROR</div>
                    <h1 class="mt-2 text-2xl font-black text-slate-900">表示に失敗しました</h1>
                    <p class="mt-4 text-sm leading-7 text-slate-600">
                        保存済みの状態やブラウザキャッシュが、現在のUI構造と合わずに壊れている可能性があります。
                    </p>
                    <div class="mt-5 rounded-2xl bg-slate-50 p-4 text-sm leading-7 text-slate-700">
                        ${escapeHtml(message)}
                    </div>
                    <div class="mt-6 flex flex-wrap gap-3">
                        <button class="rounded-full bg-slate-900 px-5 py-3 text-sm font-bold text-white" data-action="force-reset-state">保存状態を初期化して再読み込み</button>
                        <button class="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-bold text-slate-700" data-action="reload-page">そのまま再読み込み</button>
                    </div>
                </div>
            </div>
        `;
    }

    function renderApp() {
        try {
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
            refreshVisualCaption();
            refreshVisualGuide();
        } catch (error) {
            console.error("renderApp failed", error);
            renderFatalError(error);
        }
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
        currentChartConfig = null;
    }

    function chartTooltipLabel(context) {
        const raw = context.raw;
        if (currentChartConfig && typeof currentChartConfig.tooltipLabel === "function") {
            return currentChartConfig.tooltipLabel(raw, context);
        }
        if (raw && raw.label) {
            return `${raw.label}: ${raw.x}, ${raw.y}`;
        }
        return `${raw.x}, ${raw.y}`;
    }

    function applyChartConfig(chartConfig) {
        currentChartConfig = chartConfig;
        if (!chart) {
            return;
        }
        const xAxisRange = VISUAL_LEARNING.xAxisRange || {};
        chart.data.datasets = getVisualChartDatasets(chartConfig);
        chart.options.plugins.tooltip.callbacks.label = chartTooltipLabel;
        chart.options.scales.x.title.text = (VISUAL_LEARNING.axisLabels && VISUAL_LEARNING.axisLabels.x) || "X";
        chart.options.scales.x.min = xAxisRange.min;
        chart.options.scales.x.max = xAxisRange.max;
        chart.options.scales.y.title.text = (VISUAL_LEARNING.axisLabels && VISUAL_LEARNING.axisLabels.y) || "Y";
        chart.update("none");
    }

    function refreshVisualLiveState() {
        if (state.currentSection !== "visual") {
            return;
        }

        const scenario = getVisualScenario();
        const metrics = asArray(scenario && scenario.metrics);
        const metricNodes = metrics.map((_, index) => ({
            label: root.querySelector(`[data-visual-metric-label="${index}"]`),
            value: root.querySelector(`[data-visual-metric-value="${index}"]`)
        }));
        if (metricNodes.some((entry) => !entry.label || !entry.value)) {
            renderApp();
            return;
        }

        metrics.forEach((metric, index) => {
            metricNodes[index].label.textContent = metric.label;
            metricNodes[index].value.textContent = String(metric.value);
            metricNodes[index].value.className = `mt-2 text-2xl font-black ${metric.tone ? metricToneClass(metric.tone) : "text-slate-900"}`;
        });

        asArray(VISUAL_LEARNING.controls).forEach((control) => {
            const valueNode = root.querySelector(`[data-visual-control-value="${control.field}"]`);
            if (!valueNode) {
                return;
            }
            valueNode.textContent = typeof control.formatValue === "function"
                ? control.formatValue(state.visual[control.field], scenario)
                : String(state.visual[control.field]);
        });

        const insights = asArray(scenario && scenario.insights);
        const insightNodes = insights.map((_, index) => ({
            title: root.querySelector(`[data-visual-insight-title="${index}"]`),
            body: root.querySelector(`[data-visual-insight-body="${index}"]`)
        }));
        if (insightNodes.some((entry) => !entry.title || !entry.body)) {
            renderApp();
            return;
        }

        insights.forEach((insight, index) => {
            insightNodes[index].title.textContent = insight.title;
            insightNodes[index].body.textContent = insight.body;
        });

        renderChartIfNeeded();
        refreshVisualCaption();
        refreshVisualGuide();
    }

    function renderChartIfNeeded() {
        const canvas = document.getElementById("visualChart");
        if (!canvas || !window.Chart) {
            destroyChart();
            return;
        }

        const scenario = getVisualScenario();
        const chartConfig = scenario.chart || { type: "scatter", datasets: [] };
        if (chart && chart.canvas !== canvas) {
            destroyChart();
        }

        if (chart && chart.config.type === (chartConfig.type || "scatter")) {
            applyChartConfig(chartConfig);
            return;
        }

        destroyChart();
        currentChartConfig = chartConfig;

        chart = new window.Chart(canvas.getContext("2d"), {
            type: chartConfig.type || "scatter",
            data: {
                datasets: getVisualChartDatasets(chartConfig)
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
                            label: chartTooltipLabel
                        }
                    }
                },
                scales: {
                    x: {
                        type: "linear",
                        min: VISUAL_LEARNING.xAxisRange && VISUAL_LEARNING.xAxisRange.min,
                        max: VISUAL_LEARNING.xAxisRange && VISUAL_LEARNING.xAxisRange.max,
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

    function switchRole(roleId) {
        if (!roleMap[roleId]) {
            return;
        }
        state.roleId = roleId;
        persist();
        renderApp();
    }

    function openConcept(conceptId) {
        if (!conceptMap[conceptId]) {
            return;
        }
        state.activeConceptId = conceptId;
        visitSection("concepts");
        renderApp();
    }

    function applySimulationMission(missionId) {
        const mission = missionMap[missionId];
        if (!mission) {
            return;
        }
        state.visual = Object.assign({}, state.visual, mission.values || {}, {
            currentMissionId: mission.id,
            completedMissions: state.visual.completedMissions || []
        });
        state.visual.guideField = Object.keys(mission.values || {}).find((key) => key !== "material") || "material";
        if (mission.conceptId && conceptMap[mission.conceptId]) {
            state.activeConceptId = mission.conceptId;
        }
        visitSection("visual");
        renderApp();
    }

    function completeSimulationMission(missionId) {
        if (!(state.visual.completedMissions || []).includes(missionId)) {
            state.visual.completedMissions = (state.visual.completedMissions || []).concat(missionId);
        }
        state.visual.currentMissionId = missionId;
        persist();
        renderApp();
    }

    function toggleUiPanel(panelName) {
        state.ui = state.ui || {};
        state.ui[panelName] = !state.ui[panelName];
        persist();
        renderApp();
    }

    function openPrimaryMedia() {
        const media = getPrimaryMediaLink();
        if (media && media.url) {
            window.open(media.url, "_blank", "noopener,noreferrer");
            return;
        }
        visitSection("intro");
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

        if (action === "switch-role") {
            switchRole(button.dataset.role);
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
            state.visual.guideField = "material";
            persist();
            renderApp();
            return;
        }

        if (action === "set-visual-guide") {
            state.visual.guideField = button.dataset.field || "material";
            persist();
            renderApp();
            return;
        }

        if (action === "open-concept") {
            openConcept(button.dataset.concept);
            return;
        }

        if (action === "apply-sim-mission") {
            applySimulationMission(button.dataset.mission);
            return;
        }

        if (action === "complete-sim-mission") {
            completeSimulationMission(button.dataset.mission);
            return;
        }

        if (action === "toggle-ui-panel") {
            toggleUiPanel(button.dataset.panel);
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

        if (action === "set-ai-action-panel") {
            state.ai.actionPanel = button.dataset.panel || "questions";
            persist();
            renderApp();
            return;
        }

        if (action === "reset-intro-check") {
            state.introCheck = {};
            persist();
            renderApp();
            return;
        }

        if (action === "launch-visual-review") {
            const mission = getRecommendedVisualMission();
            if (mission) {
                applySimulationMission(mission.id);
                return;
            }
            visitSection("visual");
            renderApp();
            return;
        }

        if (action === "open-primary-media") {
            openPrimaryMedia();
            return;
        }

        if (action === "open-url") {
            if (button.dataset.url) {
                window.open(button.dataset.url, "_blank", "noopener,noreferrer");
            }
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
            return;
        }

        if (action === "force-reset-state") {
            state = resetState();
            window.location.reload();
            return;
        }

        if (action === "reload-page") {
            window.location.reload();
            return;
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
            state.visual.guideField = target.dataset.field;
            persist();
            return;
        }

        if (target.dataset.action === "set-visual-field") {
            state.visual[target.dataset.field] = target.value;
            state.visual.guideField = target.dataset.field;
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
        if (target.dataset.action === "set-visual-slider") {
            state.visual[target.dataset.field] = Number(target.value);
            state.visual.guideField = target.dataset.field;
            refreshVisualLiveState();
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
