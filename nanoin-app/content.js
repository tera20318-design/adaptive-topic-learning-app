(function () {
    const APP_META = {
        appName: "Adaptive Topic Learning App",
        pageTitle: "\u30ca\u30ce\u30a4\u30f3\u30c7\u30f3\u30bf\u30fc \u9069\u5fdc\u578b\u5b66\u7fd2\u30a2\u30d7\u30ea",
        storageNamespace: "nano_learn_app"
    };

    const APP_SECTIONS = [
        { id: "intro", label: "\u7406\u89e3\u3092\u307f\u308b", short: "\u5c0e\u5165" },
        { id: "principle", label: "\u6e2c\u5b9a\u539f\u7406", short: "\u539f\u7406" },
        { id: "concepts", label: "\u6982\u5ff5\u5730\u56f3", short: "\u6982\u5ff5" },
        { id: "visual", label: "\u56f3\u89e3", short: "\u56f3\u89e3" },
        { id: "diagnosis", label: "\u7406\u89e3\u8a3a\u65ad", short: "\u8a3a\u65ad" },
        { id: "ai", label: "AI\u5bfe\u8a71", short: "AI" },
        { id: "mastery", label: "\u7406\u89e3\u78ba\u8a8d", short: "\u78ba\u8a8d" },
        { id: "record", label: "\u5b66\u7fd2\u8a18\u9332", short: "\u8a18\u9332" }
    ];

    const TOPIC_MANIFEST = {
        nanoin: {
            id: "nanoin",
            name: "\u30ca\u30ce\u30a4\u30f3\u30c7\u30f3\u30bf\u30fc",
            pageTitle: "\u30ca\u30ce\u30a4\u30f3\u30c7\u30f3\u30bf\u30fc \u9069\u5fdc\u578b\u5b66\u7fd2\u30a2\u30d7\u30ea"
        },
        xrf: {
            id: "xrf",
            name: "\u86cd\u5149X\u7dda\u5206\u6790",
            pageTitle: "\u86cd\u5149X\u7dda\u5206\u6790 \u9069\u5fdc\u578b\u5b66\u7fd2\u30a2\u30d7\u30ea"
        },
        taver: {
            id: "taver",
            name: "\u30c6\u30fc\u30d0\u30fc\u6469\u8017",
            pageTitle: "\u30c6\u30fc\u30d0\u30fc\u6469\u8017 \u9069\u5fdc\u578b\u5b66\u7fd2\u30a2\u30d7\u30ea"
        },
        epma: {
            id: "epma",
            name: "EPMA",
            pageTitle: "EPMA \u9069\u5fdc\u578b\u5b66\u7fd2\u30a2\u30d7\u30ea"
        },
        ir: {
            id: "ir",
            name: "IR\u8d64\u5916\u5206\u5149",
            pageTitle: "IR\u8d64\u5916\u5206\u5149 \u9069\u5fdc\u578b\u5b66\u7fd2\u30a2\u30d7\u30ea"
        }
    };

    function resolveDefaultTopicId(topics, fallbackId) {
        try {
            const requestedId = new URLSearchParams(window.location.search).get("topic");
            if (requestedId && topics[requestedId]) {
                return requestedId;
            }
        } catch (error) {
            console.warn("failed to read topic from url", error);
        }
        return fallbackId;
    }

    const topicModules = window.NanoLearnTopicModules || {};
    const defaultTopicId = resolveDefaultTopicId(TOPIC_MANIFEST, "nanoin");
    const activeModule = topicModules[defaultTopicId] || topicModules.nanoin || null;
    const activeTopic = activeModule && activeModule.topic ? activeModule.topic : TOPIC_MANIFEST.nanoin;
    const topics = Object.fromEntries(
        Object.entries(TOPIC_MANIFEST).map(([id, manifestTopic]) => [
            id,
            id === defaultTopicId && activeModule && activeModule.topic ? activeModule.topic : manifestTopic
        ])
    );

    window.NanoLearnContent = {
        meta: APP_META,
        sections: APP_SECTIONS,
        defaultTopicId,
        topics,
        topic: activeTopic,
        APP_SECTIONS,
        INTRO_SELF_CHECK: activeTopic.selfCheck || [],
        CONCEPTS: activeTopic.concepts || [],
        VISUAL_MODELS: activeTopic.visualModels || {},
        DIAGNOSIS_QUESTIONS: activeTopic.diagnosisQuestions || {},
        AI_SUGGESTED_PATHS: (activeTopic.ai && activeTopic.ai.suggestedPaths) || [],
        LOCAL_AI_TOPICS: (activeTopic.ai && activeTopic.ai.localTopics) || [],
        EXPLANATION_RUBRIC: (activeTopic.ai && activeTopic.ai.explanationRubric) || [],
        MASTERY_QUIZ: activeTopic.masteryQuiz || [],
        FIGURE_CARDS: activeTopic.figureCards || [],
        CONCEPT_SUPPLEMENTS: activeTopic.conceptSupplements || {},
        REFERENCE_RESOURCES: (activeTopic.media && activeTopic.media.resources) || []
    };
})();
