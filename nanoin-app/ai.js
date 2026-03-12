(function () {
    const content = window.NanoLearnContent || {};
    const topicId = content.defaultTopicId || "nanoin";
    const topic = (content.topics && content.topics[topicId]) || content.topic || {};
    const topicName = topic.name || "学習テーマ";
    const LOCAL_AI_TOPICS = (topic.ai && topic.ai.localTopics) || content.LOCAL_AI_TOPICS || [];
    const AI_SUGGESTED_PATHS = (topic.ai && topic.ai.suggestedPaths) || content.AI_SUGGESTED_PATHS || [];
    const EXPLANATION_RUBRIC = (topic.ai && topic.ai.explanationRubric) || content.EXPLANATION_RUBRIC || [];
    const SYSTEM_INSTRUCTION = (topic.ai && topic.ai.systemInstruction) ||
        `あなたは${topicName}学習アプリの対話コーチです。日本語で簡潔に答え、最後に次の理解確認質問を 3 つ以内で提案してください。`;

    function uniqueItems(items) {
        return Array.from(new Set(items.filter(Boolean)));
    }

    function stripCodeFence(text) {
        return text.replace(/^```(?:json)?/i, "").replace(/```$/i, "").trim();
    }

    class LocalAIAdapter {
        respond(userText, state) {
            const matched = LOCAL_AI_TOPICS.find((topic) =>
                topic.keywords.some((keyword) => userText.includes(keyword))
            );

            const answerParts = matched
                ? matched.answer
                : [
                    "いまの質問は 1 つの正解を返すより、どの前提が曖昧かを分解すると理解が進みます。",
                    "まず『曲線のどの部分を見ているか』『硬さと弾性率のどちらを議論しているか』『基板や表面の影響を切り分けたか』の 3 点を確認してください。",
                    "必要なら、具体的な膜厚、材料系、気になっている深さ域を書いてもらえれば、その条件に寄せて整理します。"
                ];

            const revisit = (state.diagnosis.revisit || []).slice(0, 2);
            const followUps = uniqueItems(
                []
                    .concat(revisit.map((item) => `${item} を、初心者向けに図なしで説明してください。`))
                    .concat(AI_SUGGESTED_PATHS)
            ).slice(0, 3);

            return Promise.resolve({
                mode: "local",
                answer: answerParts.join("\n\n"),
                followUps
            });
        }

        evaluateExplanation(text) {
            const normalized = text.replace(/\s+/g, "");
            const matches = EXPLANATION_RUBRIC.map((rule) => {
                const score = rule.keywords.reduce((count, keyword) => (
                    normalized.includes(keyword) ? count + 1 : count
                ), 0);
                return {
                    id: rule.id,
                    title: rule.title,
                    matched: score >= 2 || (rule.id === "curve" && score >= 1)
                };
            });

            const strengths = matches.filter((item) => item.matched).map((item) => item.title);
            const missing = matches.filter((item) => !item.matched).map((item) => item.title);
            const risky = [];

            if (/硬さ/.test(text) && /強さ|靭性/.test(text) && /同じ|必ず|そのまま/.test(text)) {
                risky.push("硬さを強度や靭性と同一視している可能性があります。");
            }
            if (/浅い.*ほど.*良い|浅く.*すれば.*真値/.test(text)) {
                risky.push("浅すぎる条件の表面粗さ・先端丸みの影響が抜けています。");
            }
            if (!/基板|表面粗さ|先端|Oliver|接触深さ/.test(text)) {
                risky.push("誤差要因や解析前提への言及がなく、説明が理想条件寄りです。");
            }

            let level = "まだ骨格が弱い";
            if (strengths.length >= 4 && risky.length === 0) {
                level = "自分の言葉としてかなり整理できている";
            } else if (strengths.length >= 3) {
                level = "中核は押さえられている";
            }

            const nextAction = missing.length
                ? `次は「${missing[0]}」を 1 文追加して説明を組み直してください。`
                : "次は具体例を 1 つ入れて、薄膜測定の条件設計まで説明してみてください。";

            return Promise.resolve({
                mode: "local",
                level,
                strengths,
                missing,
                risky,
                nextAction
            });
        }
    }

    class GeminiAdapter {
        constructor(apiKey, model) {
            this.apiKey = apiKey;
            this.model = model || "gemini-2.0-flash";
        }

        async respond(userText, state) {
            const response = await fetch(
                `https://generativelanguage.googleapis.com/v1beta/models/${this.model}:generateContent?key=${this.apiKey}`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        systemInstruction: {
                            parts: [
                                {
                                    text: SYSTEM_INSTRUCTION
                                }
                            ]
                        },
                        contents: [
                            {
                                parts: [
                                    {
                                        text:
                                            `ユーザー質問:\n${userText}\n\n` +
                                            `学習状況メモ:\n` +
                                            `- 誤解診断の再学習点: ${(state.diagnosis.revisit || []).join("、") || "なし"}\n` +
                                            `- 現在の画面: ${state.currentSection}\n\n` +
                                            "出力形式:\n" +
                                            "1. 本文 3 段落以内\n" +
                                            "2. 最後に『次の確認候補:』で始め、箇条書き 3 件以内"
                                    }
                                ]
                            }
                        ]
                    })
                }
            );

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || "AI request failed");
            }

            const result = await response.json();
            const text = stripCodeFence(
                result.candidates &&
                result.candidates[0] &&
                result.candidates[0].content &&
                result.candidates[0].content.parts &&
                result.candidates[0].content.parts[0] &&
                result.candidates[0].content.parts[0].text
                    ? result.candidates[0].content.parts[0].text
                    : ""
            );

            const sections = text.split("次の確認候補:");
            const followUps = uniqueItems(
                (sections[1] || "")
                    .split("\n")
                    .map((line) => line.replace(/^[\-\d\.\s・]+/, "").trim())
            ).slice(0, 3);

            return {
                mode: "gemini",
                answer: (sections[0] || text).trim(),
                followUps: followUps.length ? followUps : AI_SUGGESTED_PATHS.slice(0, 3)
            };
        }
    }

    class AIService {
        constructor() {
            this.localAdapter = new LocalAIAdapter();
        }

        getApiKey(state) {
            return (state.settings && state.settings.geminiApiKey) || window.NANO_GUIDE_API_KEY || "";
        }

        async respond(userText, state) {
            const apiKey = this.getApiKey(state);
            if (!apiKey) {
                return this.localAdapter.respond(userText, state);
            }

            try {
                const remote = new GeminiAdapter(apiKey, state.settings.apiModel);
                return await remote.respond(userText, state);
            } catch (error) {
                console.warn("remote ai failed, using local adapter", error);
                const fallback = await this.localAdapter.respond(userText, state);
                fallback.answer =
                    "外部 AI には接続できなかったため、ローカル分岐モードで続行します。\n\n" +
                    fallback.answer;
                return fallback;
            }
        }

        evaluateExplanation(text) {
            return this.localAdapter.evaluateExplanation(text);
        }
    }

    window.NanoLearnAI = {
        AIService
    };
})();
