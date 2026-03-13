(function () {
    const content = window.NanoLearnContent || {};
    const meta = content.meta || {};
    const topicId = content.defaultTopicId || "nanoin";
    const topic = (content.topics && content.topics[topicId]) || content.topic || {};
    const defaults = topic.defaults || {};
    const aiSuggestedPaths = (topic.ai && topic.ai.suggestedPaths) || content.AI_SUGGESTED_PATHS || [];
    const storagePrefix = meta.storageNamespace || "nano_learn_app";
    const storageSuffix = topic.storageKeySuffix || topicId;
    const STORAGE_KEY = `${storagePrefix}_${storageSuffix}_state_v5`;
    const visualModels = topic.visualModels || content.VISUAL_MODELS || {};
    const visualModelKeys = Object.keys(visualModels);
    const defaultMaterial = defaults.visual && defaults.visual.material
        ? defaults.visual.material
        : (visualModelKeys[0] || "default");
    const conceptList = topic.concepts || content.CONCEPTS || [];
    const defaultConceptId = defaults.activeConceptId || (conceptList[0] && conceptList[0].id) || "";
    const diagnosisQuestions = topic.diagnosisQuestions || content.DIAGNOSIS_QUESTIONS || {};
    const diagnosisQuestionIds = Object.keys(diagnosisQuestions);
    const diagnosisStartQuestionId = defaults.diagnosisStartQuestionId || diagnosisQuestionIds[0] || "";
    const initialAiMessage = (defaults.ai && defaults.ai.initialMessage) ||
        "ここでは自由質問に答えるだけでなく、理解を深めるための次の一問も提案します。まずは気になるテーマを 1 つ選ぶか、自分の疑問を書いてください。";
    const apiModel = (defaults.settings && defaults.settings.apiModel) || "gemini-2.0-flash";

    const defaultState = {
        currentSection: defaults.currentSection || "intro",
        visitedSections: ["intro"],
        roleId: defaults.roleId || "beginner",
        introCheck: {},
        conceptLevel: defaults.conceptLevel || "basic",
        activeConceptId: defaultConceptId,
        visual: Object.assign({
            material: defaultMaterial,
            guideField: "material",
            currentMissionId: "",
            completedMissions: []
        }, clone(defaults.visual || {})),
        diagnosis: {
            currentQuestionId: diagnosisStartQuestionId,
            history: [],
            complete: false,
            misconceptions: [],
            revisit: [],
            correctCount: 0
        },
        ai: {
            input: "",
            actionPanel: "questions",
            messages: [
                {
                    role: "assistant",
                    mode: "local",
                    content: initialAiMessage,
                    followUps: aiSuggestedPaths.slice(0, 3)
                }
            ],
            pending: false,
            lastMode: "local"
        },
        mastery: {
            answers: {},
            result: null
        },
        settings: {
            geminiApiKey: "",
            apiModel
        },
        ui: {
            showIntroFigures: false,
            showResources: false
        }
    };

    function clone(value) {
        return JSON.parse(JSON.stringify(value));
    }

    function deepMerge(base, incoming) {
        if (Array.isArray(base)) {
            return Array.isArray(incoming) ? incoming : clone(base);
        }
        if (base && typeof base === "object") {
            const merged = {};
            const keys = new Set(Object.keys(base).concat(Object.keys(incoming || {})));
            keys.forEach((key) => {
                const baseValue = base[key];
                const incomingValue = incoming ? incoming[key] : undefined;
                if (incomingValue === undefined) {
                    merged[key] = clone(baseValue);
                } else if (baseValue && typeof baseValue === "object" && !Array.isArray(baseValue)) {
                    merged[key] = deepMerge(baseValue, incomingValue || {});
                } else {
                    merged[key] = incomingValue;
                }
            });
            return merged;
        }
        return incoming === undefined ? base : incoming;
    }

    function loadState() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) {
                return clone(defaultState);
            }
            const parsed = JSON.parse(raw);
            return deepMerge(defaultState, parsed);
        } catch (error) {
            console.warn("failed to load state", error);
            return clone(defaultState);
        }
    }

    function saveState(state) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    function resetState() {
        const fresh = clone(defaultState);
        saveState(fresh);
        return fresh;
    }

    window.NanoLearnStorage = {
        STORAGE_KEY,
        defaultState,
        loadState,
        saveState,
        resetState,
        clone
    };
})();
