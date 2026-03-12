(function () {
    const APP_META = {
        appName: "Adaptive Topic Learning App",
        pageTitle: "ナノインデンター適応型学習アプリ",
        storageNamespace: "nano_learn_app"
    };

    const APP_SECTIONS = [
        { id: "intro", label: "概要を見る", short: "概要" },
        { id: "concepts", label: "概念地図", short: "概念" },
        { id: "visual", label: "図解", short: "図解" },
        { id: "diagnosis", label: "誤解診断", short: "診断" },
        { id: "ai", label: "AI対話", short: "AI" },
        { id: "mastery", label: "理解確認", short: "確認" },
        { id: "record", label: "学習記録", short: "記録" }
    ];

    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    function gaussian(x, center, width, height) {
        return height * Math.exp(-Math.pow(x - center, 2) / (2 * Math.pow(width, 2)));
    }

    function buildEnergyAxis(min, max, step) {
        const points = [];
        for (let energy = min; energy <= max + 1e-9; energy += step) {
            points.push(Number(energy.toFixed(2)));
        }
        return points;
    }

    function buildNanoinScenario(stateVisual, visualModels) {
        const model = visualModels[stateVisual.material];
        const thickness = Number(stateVisual.filmThickness);
        const roughness = Number(stateVisual.roughness);
        const tipRadius = Number(stateVisual.tipRadius);

        const baseDepth = model.baseDepth + roughness * 4 + tipRadius * 1.2;
        const maxDepth = Math.min(Math.max(baseDepth, 70), thickness * 0.9 + baseDepth * 0.35);
        const substrateRiskRatio = maxDepth / Math.max(thickness * 0.1, 1);
        const substrateRisk = substrateRiskRatio >= 2.4 ? "高" : substrateRiskRatio >= 1.3 ? "中" : "低";
        const roughnessRisk = roughness >= 12 || tipRadius >= 75 ? "高" : roughness >= 7 || tipRadius >= 50 ? "中" : "低";
        const creepOffset = stateVisual.material === "polymer" ? 0.12 : 0.04;
        const recovery = Math.max(0.12, model.recovery - Math.min(substrateRiskRatio * 0.03, 0.08) + creepOffset);
        const finalDepth = Math.max(25, Math.round(maxDepth * (1 - recovery)));
        const contactDepth = Math.round(maxDepth - (maxDepth - finalDepth) * 0.72);
        const maxLoad = Number((model.load + roughness * 0.08 + tipRadius * 0.015).toFixed(1));
        const loading = [];
        const unloading = [];

        for (let step = 0; step <= 20; step += 1) {
            const h = (maxDepth / 20) * step;
            const y = maxLoad * Math.pow(h / maxDepth, model.exponent);
            loading.push({ x: Number(h.toFixed(1)), y: Number(y.toFixed(2)) });
        }

        for (let step = 0; step <= 15; step += 1) {
            const h = maxDepth - ((maxDepth - finalDepth) / 15) * step;
            const normalized = (h - finalDepth) / Math.max(maxDepth - finalDepth, 1);
            const y = maxLoad * Math.pow(Math.max(normalized, 0), 1.45);
            unloading.push({ x: Number(h.toFixed(1)), y: Number(y.toFixed(2)) });
        }

        return {
            model,
            thickness,
            roughness,
            tipRadius,
            maxDepth: Math.round(maxDepth),
            finalDepth,
            contactDepth,
            maxLoad,
            substrateRisk,
            roughnessRisk,
            metrics: [
                { id: "contactDepth", label: "接触深さ", value: `${contactDepth} nm` },
                { id: "finalDepth", label: "残留深さ", value: `${finalDepth} nm` },
                { id: "substrateRisk", label: "基板影響リスク", value: substrateRisk, tone: substrateRisk },
                { id: "roughnessRisk", label: "浅部ノイズリスク", value: roughnessRisk, tone: roughnessRisk }
            ],
            chart: {
                type: "scatter",
                datasets: [
                    {
                        label: "負荷",
                        data: loading,
                        showLine: true,
                        borderColor: "#dc2626",
                        backgroundColor: "#dc2626",
                        borderWidth: 2.4,
                        pointRadius: 0,
                        tension: 0.25
                    },
                    {
                        label: "除荷",
                        data: unloading,
                        showLine: true,
                        borderColor: "#2563eb",
                        backgroundColor: "#2563eb",
                        borderWidth: 2.4,
                        pointRadius: 0,
                        tension: 0.25
                    },
                    {
                        label: "注目点",
                        data: [
                            { x: Math.round(maxDepth), y: maxLoad, label: "hmax" },
                            { x: contactDepth, y: maxLoad * 0.72, label: "hc" },
                            { x: finalDepth, y: 0.15, label: "hf" }
                        ],
                        pointBackgroundColor: "#0f172a",
                        pointBorderColor: "#ffffff",
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        showLine: false
                    }
                ],
                tooltipLabel(raw) {
                    if (raw.label) {
                        return `${raw.label}: 深さ ${raw.x} nm, 荷重 ${raw.y.toFixed(2)} mN`;
                    }
                    return `深さ ${raw.x} nm, 荷重 ${raw.y.toFixed(2)} mN`;
                }
            }
        };
    }

    function buildXrfScenario(stateVisual, visualModels) {
        const model = visualModels[stateVisual.material];
        const atmosphere = stateVisual.atmosphere || "air";
        const coating = Number(stateVisual.coatingThickness || 10);
        const acquisition = Number(stateVisual.acquisitionTime || 20);
        const attenuationFactor = atmosphere === "helium" ? 1 : 0.56;
        const coatingPenalty = clamp(1 - coating * 0.012, 0.45, 1);
        const acquisitionFactor = clamp(0.6 + acquisition / 40, 0.75, 1.5);
        const matrixRiskScore = clamp(model.matrixComplexity + coating / 25, 1, 3);
        const matrixRisk = matrixRiskScore >= 2.5 ? "高" : matrixRiskScore >= 1.8 ? "中" : "低";
        const lightElementResponse = atmosphere === "helium" ? "改善" : "制約あり";
        const axis = buildEnergyAxis(0, 12.5, 0.1);

        const data = axis.map((energy) => {
            const baseline = 0.02 + (energy / 10) * 0.018;
            const intensity = model.peaks.reduce((sum, peak) => {
                const atmosphereGain = peak.light ? attenuationFactor : 1;
                const coatingGain = peak.surface ? coatingPenalty : 1;
                const acquisitionGain = 0.8 + acquisitionFactor * 0.2;
                return sum + gaussian(energy, peak.energy, peak.width, peak.height * atmosphereGain * coatingGain * acquisitionGain);
            }, baseline);
            return {
                x: Number(energy.toFixed(2)),
                y: Number(intensity.toFixed(3))
            };
        });

        const topPeak = model.peaks
            .map((peak) => ({
                label: peak.label,
                score: peak.height * (peak.light ? attenuationFactor : 1) * (peak.surface ? coatingPenalty : 1)
            }))
            .sort((a, b) => b.score - a.score)[0];

        return {
            model,
            atmosphere,
            coating,
            acquisition,
            matrixRisk,
            lightElementResponse,
            metrics: [
                { id: "majorPeak", label: "主ピーク候補", value: topPeak ? topPeak.label : "未定" },
                { id: "lightElements", label: "軽元素の見え方", value: lightElementResponse, tone: lightElementResponse === "改善" ? "低" : "中" },
                { id: "matrixRisk", label: "マトリクス影響", value: matrixRisk, tone: matrixRisk },
                { id: "coating", label: "表面被覆の影響", value: `${coating} um` }
            ],
            chart: {
                type: "scatter",
                datasets: [
                    {
                        label: `${model.label} スペクトル`,
                        data,
                        showLine: true,
                        borderColor: "#0f766e",
                        backgroundColor: "#0f766e",
                        borderWidth: 2.4,
                        pointRadius: 0,
                        tension: 0.18
                    }
                ],
                tooltipLabel(raw) {
                    return `エネルギー ${raw.x} keV, 相対強度 ${raw.y.toFixed(3)}`;
                }
            }
        };
    }

    const INTRO_SELF_CHECK = [
        {
            id: "familiarity",
            prompt: "ナノインデンターという言葉をどの程度説明できますか。",
            options: [
                { value: 0, label: "ほぼ説明できない" },
                { value: 1, label: "概要だけなら話せる" },
                { value: 2, label: "測定の流れまで説明できる" }
            ]
        },
        {
            id: "curveReading",
            prompt: "荷重-変位曲線のどこから何を読むか、自信はありますか。",
            options: [
                { value: 0, label: "まだ曖昧" },
                { value: 1, label: "最大深さくらいなら分かる" },
                { value: 2, label: "硬さと弾性率の読み分けまで分かる" }
            ]
        },
        {
            id: "errorFactors",
            prompt: "基板影響、表面粗さ、先端丸みの影響を区別できますか。",
            options: [
                { value: 0, label: "区別できない" },
                { value: 1, label: "聞いたことはある" },
                { value: 2, label: "測定条件に結び付けて説明できる" }
            ]
        }
    ];

    const CONCEPTS = [
        {
            id: "curve",
            title: "荷重-変位曲線",
            short: "押し込みの全履歴が詰まる中核データ",
            beginner: "押し込むときと戻すときの関係を 1 本の曲線で見ます。最大深さ、戻り方、残留深さが、材料の振る舞いを分けてくれます。",
            advanced: "負荷・保持・除荷の形から、弾塑性応答、クリープ、熱ドリフト補正の必要性まで読みます。数値だけでなく曲線形状そのものが診断材料です。",
            relations: [
                { target: "contact", label: "接触深さを見積もる出発点" },
                { target: "modulus", label: "除荷初期勾配が弾性率へつながる" },
                { target: "hardness", label: "最大荷重と接触面積の解釈を支える" }
            ]
        },
        {
            id: "contact",
            title: "接触深さ",
            short: "見た深さではなく、計算で推定する有効深さ",
            beginner: "圧子がどこまで入ったかと、実際に材料と接触している深さは同じではありません。ここを取り違えると硬さがずれます。",
            advanced: "Oliver-Pharr では除荷勾配と最大荷重から接触深さを推定します。先端丸みや pile-up / sink-in を無視すると面積関数が崩れます。",
            relations: [
                { target: "hardness", label: "接触面積を決める" },
                { target: "oliver", label: "前提条件の中心にある" },
                { target: "roughness", label: "浅い領域では特に不安定になる" }
            ]
        },
        {
            id: "hardness",
            title: "硬さ",
            short: "塑性変形のしにくさの指標",
            beginner: "硬さは、押し込んだときにどれだけ局所的に塑性変形しにくいかを見る量です。強度や靭性とそのまま同じではありません。",
            advanced: "H = Pmax / A で表せますが、A は接触面積の推定に依存します。薄膜では深さ依存性と基板影響を切り分けないと材料固有値と誤認しやすいです。",
            relations: [
                { target: "curve", label: "Pmax の位置関係が必要" },
                { target: "contact", label: "面積推定で値が変わる" },
                { target: "substrate", label: "薄膜では値の汚染源になる" }
            ]
        },
        {
            id: "modulus",
            title: "弾性率",
            short: "除荷でどれだけ押し返すかを見る",
            beginner: "除荷曲線の出だしが急なら、弾性的に押し返す力が強いと考えます。ここから弾性率を見積もります。",
            advanced: "実際には reduced modulus を求め、圧子側の弾性も補正します。除荷の初期区間が荒れている場合、表面状態や保持不足を疑う必要があります。",
            relations: [
                { target: "curve", label: "除荷勾配を読む" },
                { target: "oliver", label: "解析の前提と強く結び付く" },
                { target: "roughness", label: "浅い深さで誤差が増えやすい" }
            ]
        },
        {
            id: "substrate",
            title: "基板影響",
            short: "薄膜評価で最も起こりやすい読み違い",
            beginner: "薄い膜を深く押し込むと、膜ではなく下地の性質も混ざってしまいます。深さを入れすぎると膜の値ではなくなります。",
            advanced: "経験則として接触深さを膜厚の 10% 前後以下に抑える検討がよく行われますが、膜/基板の物性差や残留応力で最適深さは動きます。",
            relations: [
                { target: "hardness", label: "深さ依存の見かけ値を生む" },
                { target: "curve", label: "深い側で曲線形状が変わる" },
                { target: "roughness", label: "浅すぎても別の誤差が増える" }
            ]
        },
        {
            id: "roughness",
            title: "表面粗さ・先端丸み",
            short: "浅い領域を読むときの主要なノイズ源",
            beginner: "浅い押し込みでは、表面の凸凹や先端の丸みの影響が大きく、値が暴れやすくなります。",
            advanced: "最浅部の深さ依存性をそのまま材料固有の size effect と決めつけるのは危険です。粗さ、先端補正、熱ドリフト、接触検出を切り分けます。",
            relations: [
                { target: "contact", label: "接触深さ推定を不安定化する" },
                { target: "modulus", label: "除荷勾配の信頼性を落とす" },
                { target: "substrate", label: "浅すぎる条件とのトレードオフを作る" }
            ]
        },
        {
            id: "oliver",
            title: "Oliver-Pharr 前提",
            short: "解析を成立させる暗黙の約束",
            beginner: "見えた深さをそのまま使うのではなく、圧子形状と除荷の戻り方から面積や弾性率を推定する考え方です。",
            advanced: "等方的で自己相似な圧子形状、除荷初期の弾性支配、面積関数の校正などの前提が崩れると、見かけ上もっともらしい値でも解釈が危うくなります。",
            relations: [
                { target: "contact", label: "接触深さ計算の中核" },
                { target: "modulus", label: "reduced modulus 計算へ進む" },
                { target: "curve", label: "除荷の読み取り方を規定する" }
            ]
        }
    ];

    const VISUAL_MODELS = {
        ceramic: {
            label: "硬質膜 / セラミックス",
            note: "浅い深さでも荷重が乗りやすく、弾性回復も比較的大きいモデルです。",
            baseDepth: 140,
            recovery: 0.58,
            load: 9.5,
            exponent: 2.05
        },
        metal: {
            label: "一般金属",
            note: "塑性変形が進みやすく、残留深さがやや大きいモデルです。",
            baseDepth: 230,
            recovery: 0.36,
            load: 8.3,
            exponent: 1.9
        },
        polymer: {
            label: "ポリマー / 軟質膜",
            note: "深く入りやすく、保持中のクリープ影響も受けやすいモデルです。",
            baseDepth: 340,
            recovery: 0.28,
            load: 6.4,
            exponent: 1.65
        }
    };

    const DIAGNOSIS_QUESTIONS = {
        q1: {
            id: "q1",
            prompt: "硬さが高い材料なら、引張強さや壊れにくさも必ず高いと言ってよい。",
            whyEasy: "硬い、強い、壊れにくい、が日常語では近く見えるため、同じ物性だと感じやすい誤解です。",
            options: [
                {
                    id: "q1-a",
                    label: "はい。硬さが高いなら材料は全般に強いと見てよい。",
                    explanation: "硬さは局所的な塑性変形抵抗です。引張強さ、破壊靭性、疲労強度とは直接同一ではありません。",
                    correct: false,
                    misconception: true,
                    weakness: ["hardness"],
                    next: "q2-strength"
                },
                {
                    id: "q1-b",
                    label: "いいえ。硬さは一部の性質を反映するが、強度や靭性とは分けて考える。",
                    explanation: "この切り分けは重要です。特に薄膜評価では、硬さだけで性能全体を代表させない姿勢が必要です。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q2-substrate"
                }
            ]
        },
        "q2-strength": {
            id: "q2-strength",
            prompt: "硬さの結果から、最も直接には言えないものはどれですか。",
            whyEasy: "一つの数値から材料の良し悪しを全部言いたくなるため、指標の射程を広げすぎやすい場面です。",
            options: [
                {
                    id: "q2s-a",
                    label: "塑性変形のしにくさ",
                    explanation: "これは硬さが比較的直接反映する対象です。",
                    correct: false,
                    misconception: false,
                    weakness: [],
                    next: "q3-unload"
                },
                {
                    id: "q2s-b",
                    label: "破壊靭性や引張強さをそのまま代表すること",
                    explanation: "その通りです。ここを分けておくと、硬さデータの過大解釈を避けられます。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q3-unload"
                },
                {
                    id: "q2s-c",
                    label: "すべて同時に言える。硬さが高ければ強さも靭性も高い。",
                    explanation: "硬さから材料性能全体を代表させるのは危険です。靭性はむしろ逆方向に動くこともあります。",
                    correct: false,
                    misconception: true,
                    weakness: ["hardness"],
                    next: "q3-unload"
                }
            ]
        },
        "q2-substrate": {
            id: "q2-substrate",
            prompt: "膜厚 100 nm の薄膜で、接触深さが 35 nm まで入った場合、まず疑うべきものは何ですか。",
            whyEasy: "深く押し込めばデータが安定しそうに見える一方で、深さを増やすと別の材料を読んでしまう落とし穴があります。",
            options: [
                {
                    id: "q2b-a",
                    label: "膜の値として十分で、基板影響はほぼ無視できる",
                    explanation: "薄膜では深さが深いほど基板影響が混ざりやすくなります。深さ依存の確認が必要です。",
                    correct: false,
                    misconception: true,
                    weakness: ["substrate"],
                    next: "q3-surface"
                },
                {
                    id: "q2b-b",
                    label: "基板影響。膜だけではなく下地の応答が混ざる可能性が高い",
                    explanation: "その通りです。膜厚に対する接触深さを意識して条件を設計する姿勢が重要です。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q3-surface"
                }
            ]
        },
        "q3-unload": {
            id: "q3-unload",
            prompt: "除荷曲線の初期勾配から主に読みたいものはどれですか。",
            whyEasy: "最大荷重や最大深さの印象が強く、除荷の情報が見落とされやすいためです。",
            options: [
                {
                    id: "q3u-a",
                    label: "弾性率の見積もり",
                    explanation: "除荷初期勾配は弾性的な押し返しを反映するため、弾性率の推定に効きます。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q4-surface"
                },
                {
                    id: "q3u-b",
                    label: "硬さそのもの",
                    explanation: "硬さは最大荷重と接触面積の関係で見ます。除荷勾配は主に弾性率側です。",
                    correct: false,
                    misconception: true,
                    weakness: ["modulus", "curve"],
                    next: "q4-oliver"
                }
            ]
        },
        "q3-surface": {
            id: "q3-surface",
            prompt: "最浅部だけ値が大きく散るとき、材料固有の深さ依存と決める前に何を確認しますか。",
            whyEasy: "浅い方が膜だけを見ている感覚があるため、測定誤差の寄与を後回しにしがちです。",
            options: [
                {
                    id: "q3sf-a",
                    label: "表面粗さ、先端丸み、接触検出、熱ドリフト",
                    explanation: "ここを先に疑うのが安全です。浅い領域は材料より測定系の影響が目立ちます。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q4-oliver"
                },
                {
                    id: "q3sf-b",
                    label: "まず材料の size effect と考えてよい",
                    explanation: "浅い領域の散りは、測定系や表面状態の影響であることがよくあります。",
                    correct: false,
                    misconception: true,
                    weakness: ["roughness"],
                    next: "q4-oliver"
                }
            ]
        },
        "q4-surface": {
            id: "q4-surface",
            prompt: "薄膜評価で『浅くすればするほど良い』と単純化できない理由は何ですか。",
            whyEasy: "基板影響を避けたい意識が強いほど、浅い条件の別のリスクを見落としやすくなります。",
            options: [
                {
                    id: "q4s-a",
                    label: "浅すぎると表面粗さや先端丸みの影響が相対的に大きくなる",
                    explanation: "その通りです。薄膜測定は、深すぎると基板影響、浅すぎると表面・先端誤差、のトレードオフです。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: null
                },
                {
                    id: "q4s-b",
                    label: "理由は特にない。浅いほど常に膜の真値へ近づく",
                    explanation: "実際は浅すぎると別の誤差が急増します。最適条件はトレードオフで探します。",
                    correct: false,
                    misconception: true,
                    weakness: ["roughness", "substrate"],
                    next: null
                }
            ]
        },
        "q4-oliver": {
            id: "q4-oliver",
            prompt: "Oliver-Pharr の値が出たとき、最終的に意識すべき姿勢はどれですか。",
            whyEasy: "解析ソフトが数字を返すと、その前提や適用範囲を忘れやすくなるためです。",
            options: [
                {
                    id: "q4o-a",
                    label: "数字が出た時点で十分。前提条件は気にしなくてよい",
                    explanation: "面積関数、除荷の安定性、表面状態などの前提が崩れると、数字だけが整っていても解釈は危ういです。",
                    correct: false,
                    misconception: true,
                    weakness: ["oliver", "contact"],
                    next: null
                },
                {
                    id: "q4o-b",
                    label: "値だけでなく、曲線形状と前提条件が合っているかも確認する",
                    explanation: "この視点があると、もっともらしい誤値を避けやすくなります。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: null
                }
            ]
        }
    };

    const AI_SUGGESTED_PATHS = [
        "荷重-変位曲線のどこを見れば硬さと弾性率を読み分けられますか。",
        "薄膜測定で基板影響と表面粗さのトレードオフを整理したいです。",
        "Oliver-Pharr の前提が崩れるケースを初心者向けに説明してください。",
        "膜厚 100 nm の硬質膜を測るときのプレテスト手順を考えたいです。"
    ];

    const LOCAL_AI_TOPICS = [
        {
            keywords: ["基板", "膜厚", "薄膜"],
            answer: [
                "薄膜では、深く入るほど膜そのものではなく基板の応答が混ざります。",
                "まずは接触深さを膜厚の 10% 前後以下に抑えられる条件を仮置きし、深さ依存を確認してください。",
                "ただし浅すぎると表面粗さや先端丸みの影響が増えるので、深さ依存の安定域を探す姿勢が重要です。"
            ]
        },
        {
            keywords: ["硬さ", "強さ", "靭性"],
            answer: [
                "硬さは局所的な塑性変形抵抗です。",
                "引張強さ、破壊靭性、疲労特性とはそのまま同一ではないため、硬さだけで性能全体を代表させないでください。",
                "説明するときは『押し込みに対する抵抗』と『構造全体が壊れるか』を分けると整理しやすいです。"
            ]
        },
        {
            keywords: ["表面", "粗さ", "先端", "丸み"],
            answer: [
                "最浅部の値が散るときは、材料本質より先に測定系を疑うのが安全です。",
                "表面粗さ、接触検出、熱ドリフト、圧子先端の丸み補正を確認してください。",
                "浅いほど良い、ではなく、薄膜では『深すぎるリスク』と『浅すぎるリスク』の両方を見ます。"
            ]
        },
        {
            keywords: ["Oliver", "Pharr", "接触深さ", "面積関数"],
            answer: [
                "Oliver-Pharr は、押し込んだ深さそのものではなく、除荷の戻り方から接触深さを推定する考え方です。",
                "硬さは最大荷重と接触面積、弾性率は除荷初期勾配と接触面積の組み合わせで読みます。",
                "だからこそ、面積関数や除荷初期区間の信頼性が崩れると、値の解釈も崩れます。"
            ]
        }
    ];

    const EXPLANATION_RUBRIC = [
        {
            id: "curve",
            title: "荷重-変位曲線の役割",
            keywords: ["荷重", "変位", "曲線", "押し込み", "除荷"]
        },
        {
            id: "hardness",
            title: "硬さは接触面積を通して読むこと",
            keywords: ["硬さ", "接触面積", "最大荷重", "塑性"]
        },
        {
            id: "modulus",
            title: "弾性率は除荷勾配から読むこと",
            keywords: ["弾性率", "ヤング率", "除荷", "勾配", "傾き"]
        },
        {
            id: "limits",
            title: "誤差要因や前提に触れていること",
            keywords: ["基板", "表面粗さ", "先端", "Oliver", "前提", "接触深さ"]
        }
    ];

    const MASTERY_QUIZ = [
        {
            id: "m1",
            prompt: "荷重-変位曲線の除荷初期勾配から主に読みたいものはどれですか。",
            choices: [
                { id: "m1a", label: "弾性率", correct: true, explanation: "除荷初期勾配は弾性的な押し返しを反映し、弾性率推定の支点です。" },
                { id: "m1b", label: "試料表面の色", correct: false, explanation: "色はこの曲線から直接は読めません。" },
                { id: "m1c", label: "膜厚そのもの", correct: false, explanation: "膜厚は別測定や設計値が必要です。" }
            ]
        },
        {
            id: "m2",
            prompt: "薄膜を評価するとき、深く押し込みすぎると起きやすい問題は何ですか。",
            choices: [
                { id: "m2a", label: "基板影響が混ざる", correct: true, explanation: "深く入るほど、膜だけでなく基板の応答も混ざりやすくなります。" },
                { id: "m2b", label: "弾性率が必ず 0 になる", correct: false, explanation: "そのような現象ではありません。" },
                { id: "m2c", label: "表面粗さが消える", correct: false, explanation: "表面粗さの見え方は変わりますが、消えるわけではありません。" }
            ]
        },
        {
            id: "m3",
            prompt: "『浅くすればするほど常に良い』と言えない主な理由は何ですか。",
            choices: [
                { id: "m3a", label: "浅すぎると表面粗さや先端丸みの影響が増える", correct: true, explanation: "薄膜測定は、深すぎると基板影響、浅すぎると表面・先端誤差が増えるトレードオフです。" },
                { id: "m3b", label: "装置が必ず停止する", correct: false, explanation: "装置停止が本質的理由ではありません。" },
                { id: "m3c", label: "硬さが測れなくなるから", correct: false, explanation: "測れなくなるのではなく、誤差要因の比率が増えます。" }
            ]
        },
        {
            id: "m4",
            prompt: "硬さについて最も適切な説明はどれですか。",
            choices: [
                { id: "m4a", label: "硬さは局所的な塑性変形抵抗を表す", correct: true, explanation: "硬さは押し込みに対する局所的な塑性変形抵抗の指標です。" },
                { id: "m4b", label: "硬さが高ければ靭性も必ず高い", correct: false, explanation: "硬さと靭性は同一ではありません。" },
                { id: "m4c", label: "硬さは除荷勾配だけで決まる", correct: false, explanation: "硬さは最大荷重と接触面積の関係で見ます。" }
            ]
        }
    ];

    const FIGURE_CARDS = [
        {
            id: "curve-overview",
            label: "図 1",
            illustration: `
                <svg viewBox="0 0 260 120" class="w-full">
                    <path d="M18 92 C60 84, 88 52, 120 24" fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>
                    <path d="M120 24 C160 40, 182 74, 228 92" fill="none" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
                    <circle cx="120" cy="24" r="5" fill="#0f172a"/>
                    <line x1="18" y1="98" x2="240" y2="98" stroke="#94a3b8" stroke-width="2"/>
                    <line x1="18" y1="98" x2="18" y2="12" stroke="#94a3b8" stroke-width="2"/>
                    <text x="124" y="18" font-size="12" fill="#0f172a">hmax</text>
                    <text x="175" y="55" font-size="12" fill="#2563eb">除荷勾配</text>
                    <text x="58" y="78" font-size="12" fill="#dc2626">負荷側</text>
                </svg>
            `,
            bullets: [
                { label: "hmax", body: "どこまで入ったか" },
                { label: "除荷勾配", body: "弾性率を読む支点" },
                { label: "残留深さ", body: "塑性変形の残り方" }
            ]
        },
        {
            id: "thin-film-tradeoff",
            label: "図 2",
            illustration: `
                <svg viewBox="0 0 260 120" class="w-full">
                    <rect x="22" y="64" width="216" height="30" rx="8" fill="#cbd5e1"/>
                    <rect x="22" y="48" width="126" height="16" rx="6" fill="#93c5fd"/>
                    <path d="M122 20 L102 48 L142 48 Z" fill="#1d4ed8"/>
                    <path d="M186 20 L166 64 L206 64 Z" fill="#b91c1c"/>
                    <text x="80" y="112" font-size="12" fill="#1d4ed8">浅い: 膜寄り</text>
                    <text x="160" y="112" font-size="12" fill="#b91c1c">深い: 基板影響</text>
                </svg>
            `,
            bullets: [
                { label: "深すぎる", body: "基板影響が混ざる" },
                { label: "浅すぎる", body: "表面粗さと先端丸みが効く" },
                { label: "狙う場所", body: "両者の間の安定域" }
            ]
        },
        {
            id: "concept-map",
            label: "図 3",
            illustration: `
                <svg viewBox="0 0 260 120" class="w-full">
                    <circle cx="55" cy="60" r="24" fill="#dbeafe"/>
                    <circle cx="130" cy="30" r="24" fill="#ecfeff"/>
                    <circle cx="130" cy="90" r="24" fill="#ffedd5"/>
                    <circle cx="205" cy="60" r="24" fill="#ede9fe"/>
                    <line x1="79" y1="52" x2="106" y2="37" stroke="#94a3b8" stroke-width="2"/>
                    <line x1="79" y1="68" x2="106" y2="84" stroke="#94a3b8" stroke-width="2"/>
                    <line x1="154" y1="37" x2="181" y2="52" stroke="#94a3b8" stroke-width="2"/>
                    <line x1="154" y1="84" x2="181" y2="68" stroke="#94a3b8" stroke-width="2"/>
                    <text x="34" y="64" font-size="11" fill="#1d4ed8">曲線</text>
                    <text x="111" y="34" font-size="11" fill="#0f766e">弾性率</text>
                    <text x="107" y="94" font-size="11" fill="#b45309">硬さ</text>
                    <text x="183" y="64" font-size="11" fill="#6d28d9">前提</text>
                </svg>
            `,
            bullets: [
                { label: "曲線", body: "すべての出発点" },
                { label: "硬さ", body: "接触面積を通して読む" },
                { label: "前提", body: "Oliver-Pharr が解釈を支える" }
            ]
        }
    ];

    const CONCEPT_SUPPLEMENTS = {
        curve: `
            <div class="rounded-3xl bg-slate-50 p-4">
                <svg viewBox="0 0 260 120" class="w-full">
                    <path d="M20 96 C65 88, 94 55, 128 24" fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>
                    <path d="M128 24 C156 38, 182 68, 232 94" fill="none" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
                    <line x1="18" y1="100" x2="240" y2="100" stroke="#94a3b8" stroke-width="2"/>
                    <line x1="18" y1="100" x2="18" y2="14" stroke="#94a3b8" stroke-width="2"/>
                    <text x="132" y="16" font-size="12" fill="#0f172a">hmax</text>
                    <text x="174" y="54" font-size="12" fill="#2563eb">除荷勾配</text>
                    <text x="74" y="82" font-size="12" fill="#dc2626">負荷</text>
                </svg>
            </div>
        `,
        contact: `
            <div class="overflow-hidden rounded-3xl border border-slate-200">
                <table class="w-full text-sm">
                    <tbody>
                        <tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">見た深さ</th><td class="px-4 py-3 text-slate-600">hmax</td></tr>
                        <tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">解析で使う深さ</th><td class="px-4 py-3 text-slate-600">hc</td></tr>
                        <tr><th class="px-4 py-3 text-left font-bold text-slate-700">誤差源</th><td class="px-4 py-3 text-slate-600">先端丸み / pile-up / sink-in</td></tr>
                    </tbody>
                </table>
            </div>
        `,
        hardness: `
            <div class="overflow-hidden rounded-3xl border border-slate-200">
                <table class="w-full text-sm">
                    <tbody>
                        <tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">見る量</th><td class="px-4 py-3 text-slate-600">H = Pmax / A</td></tr>
                        <tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">意味</th><td class="px-4 py-3 text-slate-600">局所的な塑性変形抵抗</td></tr>
                        <tr><th class="px-4 py-3 text-left font-bold text-slate-700">混同しやすいもの</th><td class="px-4 py-3 text-slate-600">強度 / 靭性</td></tr>
                    </tbody>
                </table>
            </div>
        `,
        modulus: `
            <div class="rounded-3xl bg-slate-50 p-4">
                <svg viewBox="0 0 260 120" class="w-full">
                    <path d="M34 98 C70 74, 90 52, 128 20" fill="none" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
                    <line x1="128" y1="20" x2="192" y2="68" stroke="#0f172a" stroke-width="3" stroke-dasharray="6 6"/>
                    <text x="170" y="56" font-size="12" fill="#0f172a">S</text>
                    <text x="150" y="88" font-size="12" fill="#2563eb">除荷初期</text>
                </svg>
            </div>
        `,
        substrate: `
            <div class="rounded-3xl bg-slate-50 p-4">
                <svg viewBox="0 0 260 120" class="w-full">
                    <rect x="24" y="64" width="212" height="28" rx="8" fill="#cbd5e1"/>
                    <rect x="24" y="50" width="126" height="14" rx="5" fill="#93c5fd"/>
                    <path d="M110 24 L92 50 L128 50 Z" fill="#1d4ed8"/>
                    <path d="M186 18 L162 64 L210 64 Z" fill="#b91c1c"/>
                    <text x="58" y="108" font-size="12" fill="#1d4ed8">膜寄り</text>
                    <text x="165" y="108" font-size="12" fill="#b91c1c">基板影響</text>
                </svg>
            </div>
        `,
        roughness: `
            <div class="rounded-3xl bg-slate-50 p-4">
                <svg viewBox="0 0 260 120" class="w-full">
                    <path d="M18 78 L42 62 L65 82 L90 56 L114 80 L138 58 L162 84 L186 60 L210 80 L236 66" fill="none" stroke="#64748b" stroke-width="4" stroke-linecap="round"/>
                    <circle cx="126" cy="36" r="18" fill="#1d4ed8"/>
                    <text x="98" y="18" font-size="12" fill="#0f172a">表面粗さ</text>
                    <text x="116" y="66" font-size="12" fill="#1d4ed8">先端丸み</text>
                </svg>
            </div>
        `,
        oliver: `
            <div class="overflow-hidden rounded-3xl border border-slate-200">
                <table class="w-full text-sm">
                    <tbody>
                        <tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">前提</th><td class="px-4 py-3 text-slate-600">面積関数の校正</td></tr>
                        <tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">前提</th><td class="px-4 py-3 text-slate-600">除荷初期の弾性支配</td></tr>
                        <tr><th class="px-4 py-3 text-left font-bold text-slate-700">崩れると</th><td class="px-4 py-3 text-slate-600">数字は出ても解釈が危うい</td></tr>
                    </tbody>
                </table>
            </div>
        `
    };

    const REFERENCE_RESOURCES = [
        {
            id: "r1",
            title: "KLA IU Session 22",
            url: "https://www.kla.com/media-room/videos/indentation-university-session-3-basic-nanoindentation-theory",
            source: "KLA",
            note: "ナノインデンテーションの理論と stress-strain 解釈のつながりを押さえる基礎寄りの資料"
        },
        {
            id: "r2",
            title: "KLA IU Session 21",
            url: "https://www.kla.com/media-room/videos/indentation-university-session-21-scratch-testing-of-100nm-dlc-coated-cmps",
            source: "KLA",
            note: "100 nm 級の DLC コーティングを例に、薄膜条件と表面・界面の見方を追う回"
        },
        {
            id: "r3",
            title: "KLA IU Session 20",
            url: "https://www.kla.com/media-room/videos/indentation-university-session-20-statistics-in-nanomechanical-testing",
            source: "KLA",
            note: "ばらつきの見方と統計の扱いを押さえて、単発値の読み違いを避けたいとき向け"
        }
    ];

    const HERO = {
        eyebrow: "ADAPTIVE LEARNING",
        titleLead: "ナノインデンターを",
        titleAccent: "説明できる状態",
        titleTrail: "まで持っていく",
        subtitle: "未知領域理解のための学習アプリ",
        description:
            "説明を読むだけではなく、誤解を診断し、図解を動かし、AI と分岐質問で理解不足をあぶり出します。最後は選択式の理解確認で、どこが弱いかまで確認できます。"
    };

    const INTRO_OVERVIEW_CARDS = [
        {
            id: "what",
            eyebrow: "WHAT",
            title: "ナノインデンターとは何か",
            body:
                "圧子を押し込むときの荷重と深さを連続測定し、局所的な硬さや弾性率を推定する手法です。くぼみを目で測るのではなく、曲線全体を読むのが特徴です。"
        },
        {
            id: "learn",
            eyebrow: "LEARN",
            title: "何が分かるか",
            body:
                "硬さ、弾性率、深さ依存、基板影響の入り方、表面起因のばらつきの見分け方まで扱えます。数値だけでなく、曲線の形から条件の妥当性を判断します。"
        },
        {
            id: "misread",
            eyebrow: "MISREAD",
            title: "何を誤解しやすいか",
            body:
                "硬さと強さの混同、深さ依存を材料本質と決めつけること、基板影響や先端丸みの見落としが代表例です。"
        }
    ];

    const INTRO_SUMMARY_STATES = {
        empty: {
            label: "診断待ち",
            text: "最初の 3 問に答えると、どこから入るべきかを案内します。"
        },
        low: {
            label: "導入から着手",
            text: "まずは概念地図と図解で『何を測っているか』の骨格を作る段階です。"
        },
        medium: {
            label: "誤解の切り分けが効果的",
            text: "概要はつかめています。次は誤解診断で、硬さ・弾性率・深さ依存の混線をほどくと伸びやすいです。"
        },
        high: {
            label: "応用理解へ進める",
            text: "基礎用語は入っています。AI 対話や理解確認で、自分の言葉に変換できるかを詰める段階です。"
        }
    };

    const VISUAL_LEARNING = {
        title: "条件を動かして、どこを読むべきかを見る",
        description:
            "ここでは精密な実測再現ではなく、解釈の軸をつかむための概念モデルを使います。スライダーを動かし、どの条件でどの誤読が起きやすいかを確認してください。",
        buildScenario: buildNanoinScenario,
        materialLabel: "材料モデル",
        controls: [
            {
                field: "filmThickness",
                label: "膜厚",
                min: 60,
                max: 400,
                step: 10,
                formatValue(value) {
                    return `${value} nm`;
                }
            },
            {
                field: "roughness",
                label: "表面粗さ",
                min: 1,
                max: 20,
                step: 1,
                formatValue(value) {
                    return `Ra ${value} nm`;
                }
            },
            {
                field: "tipRadius",
                label: "先端丸み",
                min: 10,
                max: 120,
                step: 5,
                formatValue(value) {
                    return `R ${value} nm`;
                }
            }
        ],
        metrics: {
            contactDepth: "接触深さ",
            finalDepth: "残留深さ",
            substrateRisk: "基板影響リスク",
            roughnessRisk: "浅部ノイズリスク"
        },
        chartCaption:
            "赤: 負荷、青: 除荷、点: hmax / hc / hf。数値そのものより「どこが解釈の支点か」を見るための概念図です。",
        axisLabels: {
            x: "押し込み深さ h (nm)",
            y: "荷重 P (mN)"
        },
        buildInsights(scenario) {
            return [
                {
                    title: "見るべき箇所 1",
                    body: `最大深さ hmax は ${Math.round(scenario.maxDepth)} nm です。深さが増えるほど基板影響の混入余地が広がります。`
                },
                {
                    title: "見るべき箇所 2",
                    body: `接触深さ hc は約 ${scenario.contactDepth} nm と見積もられます。膜厚 ${scenario.thickness} nm に対して、まずはこの比率を見ます。`
                },
                {
                    title: "解釈メモ",
                    body:
                        scenario.roughnessRisk === "高"
                            ? "浅い領域の散りは、材料本質より表面粗さや先端丸みの寄与を疑う条件です。"
                            : "浅い領域のノイズは中程度以下です。それでも最浅点だけで結論を出さない方が安全です。"
                }
            ];
        }
    };

    const DIAGNOSIS_UI = {
        noMistakesText: "大きな誤解はまだ表面化していません。次は理解確認で、自分の言葉に変換できるかを見ます。",
        noRevisitTagText: "再学習候補はまだ絞られていません",
        nextActions: [
            { section: "visual", label: "図解で曲線と深さを見直す" },
            { section: "ai", label: "AI対話で弱点を言語化する" },
            { section: "mastery", label: "選択式テストで仕上げる" }
        ]
    };

    const AI_UI = {
        textareaPlaceholder: "例: 荷重-変位曲線の除荷勾配とヤング率の関係を、硬さとの違いも含めて説明してください。",
        mediaEmptyTitle: "動画は任意アセットです",
        mediaEmptyBody:
            "今は外部埋め込みに依存せず、図解と診断を主軸にしています。あとから YouTube かローカル動画を追加しても、この枠をそのまま使えます。"
    };

    const XRF_SELF_CHECK = [
        {
            id: "principle",
            prompt: "XRF が何を読んで元素を見分けるか、説明できますか。",
            options: [
                { value: 0, label: "まだ曖昧" },
                { value: 1, label: "元素固有のX線くらいなら言える" },
                { value: 2, label: "励起から検出まで流れで話せる" }
            ]
        },
        {
            id: "limits",
            prompt: "軽元素、膜厚、母材影響などの限界を区別できますか。",
            options: [
                { value: 0, label: "区別できない" },
                { value: 1, label: "なんとなく知っている" },
                { value: 2, label: "条件に結び付けて説明できる" }
            ]
        },
        {
            id: "safety",
            prompt: "X線装置としての安全上の注意を説明できますか。",
            options: [
                { value: 0, label: "自信がない" },
                { value: 1, label: "扉を開けない程度なら言える" },
                { value: 2, label: "インターロックまで含めて説明できる" }
            ]
        }
    ];

    const XRF_CONCEPTS = [
        {
            id: "excitation",
            title: "励起と蛍光X線",
            short: "一次X線で原子を励起し、固有X線を読む",
            beginner: "一次X線を当てると、元素ごとに違うエネルギーの蛍光X線が出ます。その違いを読んで元素を見分けます。",
            advanced: "内殻空孔を埋める電子遷移で K 線や L 線が生じます。ピーク位置は元素同定、ピーク強度は量の推定に使いますが、条件依存です。",
            relations: [
                { target: "spectrum", label: "蛍光X線はスペクトル上のピークになる" },
                { target: "matrix", label: "出てきた強度は母材条件で変わる" },
                { target: "safety", label: "X線源を扱うので安全管理が前提" }
            ]
        },
        {
            id: "spectrum",
            title: "スペクトル",
            short: "ピーク位置で元素、強度で量の目安を見る",
            beginner: "山の位置がどの元素か、山の大きさがどれくらい入っているかの手がかりになります。",
            advanced: "ピーク重なり、バックグラウンド、分解能の制約を考えずに定量すると誤解しやすいです。まずは同定とスクリーニングに向く、と整理します。",
            relations: [
                { target: "light", label: "低エネルギー側は見え方が変わりやすい" },
                { target: "matrix", label: "強度は単純比例ではない" },
                { target: "calibration", label: "定量には較正や標準が必要" }
            ]
        },
        {
            id: "light",
            title: "軽元素の制約",
            short: "空気や窓材で低エネルギーX線が減衰する",
            beginner: "軽い元素ほど低いエネルギーのX線になるため、空気中では見えにくくなります。",
            advanced: "He パージや真空、検出器窓材、表面状態で感度が変わります。見えないことと、存在しないことは分ける必要があります。",
            relations: [
                { target: "spectrum", label: "スペクトルの低エネルギー側に出る" },
                { target: "matrix", label: "表面被覆や母材でも隠れやすい" },
                { target: "calibration", label: "条件をそろえないと比較しにくい" }
            ]
        },
        {
            id: "matrix",
            title: "マトリクス影響",
            short: "母材や膜厚が強度解釈をゆがめる",
            beginner: "同じ元素量でも、周りの材料や表面被覆が違うとピークの大きさが変わることがあります。",
            advanced: "吸収・増強・膜厚・粗さの影響があるため、異なる材質を単純比較しにくい場面があります。定量は条件一致が前提です。",
            relations: [
                { target: "calibration", label: "標準や補正なしでは定量が危うい" },
                { target: "spectrum", label: "ピーク強度の読みを変えてしまう" },
                { target: "light", label: "低エネルギー側ほど影響を受けやすい" }
            ]
        },
        {
            id: "calibration",
            title: "較正と標準",
            short: "定量には標準試料と条件整合が必要",
            beginner: "元素があるかないかを見るだけなら簡単でも、どれだけ入っているかを正確に言うには基準が必要です。",
            advanced: "標準試料、測定時間、雰囲気、幾何条件をそろえないと比較が危うくなります。スクリーニングと定量の目的を分けて説明します。",
            relations: [
                { target: "matrix", label: "マトリクス差をそのまま放置できない" },
                { target: "spectrum", label: "強度解釈の土台になる" },
                { target: "safety", label: "再測定でも安全手順は省略できない" }
            ]
        },
        {
            id: "safety",
            title: "安全管理",
            short: "非破壊でもX線装置としての安全が最優先",
            beginner: "測定は簡単に見えても、X線を使う装置なのでインターロックや扉の管理を守る必要があります。",
            advanced: "扉開放測定、インターロック無効化、治具の不適切使用は論外です。社内説明では『早く測る』より『安全手順を守る』を先に置きます。",
            relations: [
                { target: "excitation", label: "一次X線源を使う以上、必須の前提" },
                { target: "calibration", label: "条件再現より安全が優先される" },
                { target: "spectrum", label: "測定品質以前に安全確保が必要" }
            ]
        }
    ];

    const XRF_FIGURE_CARDS = [
        {
            id: "xrf-flow",
            label: "図 1",
            illustration: `
                <svg viewBox="0 0 260 120" class="w-full">
                    <rect x="18" y="28" width="52" height="46" rx="10" fill="#0f172a"/>
                    <rect x="188" y="22" width="54" height="54" rx="16" fill="#0f766e"/>
                    <rect x="92" y="72" width="80" height="22" rx="8" fill="#14b8a6"/>
                    <path d="M70 52 L118 76" fill="none" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
                    <path d="M136 72 L188 50" fill="none" stroke="#34d399" stroke-width="4" stroke-linecap="round"/>
                    <text x="18" y="20" font-size="11" fill="#0f172a">X線管</text>
                    <text x="101" y="108" font-size="11" fill="#0f172a">試料</text>
                    <text x="188" y="16" font-size="11" fill="#0f172a">検出器</text>
                </svg>
            `,
            bullets: [
                { label: "照射", body: "一次X線を試料に当てる" },
                { label: "励起", body: "元素固有の蛍光X線が出る" },
                { label: "検出", body: "エネルギーと強度を読む" }
            ]
        },
        {
            id: "xrf-spectrum",
            label: "図 2",
            illustration: `
                <svg viewBox="0 0 260 120" class="w-full">
                    <line x1="20" y1="96" x2="240" y2="96" stroke="#94a3b8" stroke-width="2"/>
                    <line x1="20" y1="96" x2="20" y2="18" stroke="#94a3b8" stroke-width="2"/>
                    <path d="M20 92 C48 92, 54 88, 62 70 C70 40, 78 44, 90 92 C100 92, 112 90, 120 64 C128 30, 136 34, 148 92 C164 92, 170 88, 180 54 C188 28, 196 36, 210 92" fill="none" stroke="#0f766e" stroke-width="4" stroke-linecap="round"/>
                    <text x="56" y="62" font-size="11" fill="#0f766e">Cr</text>
                    <text x="116" y="56" font-size="11" fill="#0f766e">Fe</text>
                    <text x="176" y="46" font-size="11" fill="#0f766e">Ni</text>
                </svg>
            `,
            bullets: [
                { label: "位置", body: "どの元素かの手がかり" },
                { label: "高さ", body: "量の目安だが条件依存" },
                { label: "重なり", body: "単純読みは危険" }
            ]
        },
        {
            id: "xrf-limits",
            label: "図 3",
            illustration: `
                <svg viewBox="0 0 260 120" class="w-full">
                    <rect x="22" y="76" width="216" height="18" rx="8" fill="#cbd5e1"/>
                    <rect x="22" y="58" width="90" height="18" rx="8" fill="#7dd3fc"/>
                    <rect x="112" y="58" width="126" height="18" rx="8" fill="#34d399"/>
                    <text x="36" y="50" font-size="11" fill="#0369a1">軽元素側</text>
                    <text x="142" y="50" font-size="11" fill="#047857">重元素側</text>
                    <text x="36" y="108" font-size="11" fill="#0f172a">空気中で減衰しやすい</text>
                </svg>
            `,
            bullets: [
                { label: "軽元素", body: "空気中では見えにくい" },
                { label: "母材", body: "強度解釈をゆがめる" },
                { label: "安全", body: "非破壊でもX線装置" }
            ]
        }
    ];

    const XRF_CONCEPT_SUPPLEMENTS = {
        excitation: `
            <div class="rounded-3xl bg-slate-50 p-4">
                <svg viewBox="0 0 260 120" class="w-full">
                    <rect x="18" y="30" width="50" height="42" rx="10" fill="#0f172a"/>
                    <circle cx="130" cy="60" r="20" fill="#99f6e4"/>
                    <rect x="192" y="26" width="44" height="44" rx="12" fill="#0f766e"/>
                    <path d="M68 50 L112 56" fill="none" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
                    <path d="M148 56 L192 48" fill="none" stroke="#34d399" stroke-width="4" stroke-linecap="round"/>
                </svg>
            </div>
        `,
        spectrum: `
            <div class="overflow-hidden rounded-3xl border border-slate-200">
                <table class="w-full text-sm">
                    <tbody>
                        <tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">ピーク位置</th><td class="px-4 py-3 text-slate-600">元素同定</td></tr>
                        <tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">ピーク強度</th><td class="px-4 py-3 text-slate-600">量の目安</td></tr>
                        <tr><th class="px-4 py-3 text-left font-bold text-slate-700">注意点</th><td class="px-4 py-3 text-slate-600">重なり / 背景 / 分解能</td></tr>
                    </tbody>
                </table>
            </div>
        `,
        light: `
            <div class="rounded-3xl bg-slate-50 p-4">
                <svg viewBox="0 0 260 120" class="w-full">
                    <rect x="18" y="68" width="224" height="16" rx="8" fill="#cbd5e1"/>
                    <rect x="18" y="52" width="94" height="16" rx="8" fill="#7dd3fc"/>
                    <text x="28" y="42" font-size="12" fill="#0369a1">低エネルギー側</text>
                    <text x="130" y="42" font-size="12" fill="#0f172a">空気で減衰</text>
                </svg>
            </div>
        `,
        matrix: `
            <div class="overflow-hidden rounded-3xl border border-slate-200">
                <table class="w-full text-sm">
                    <tbody>
                        <tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">吸収</th><td class="px-4 py-3 text-slate-600">母材で弱まる</td></tr>
                        <tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">増強</th><td class="px-4 py-3 text-slate-600">周辺元素で強まる</td></tr>
                        <tr><th class="px-4 py-3 text-left font-bold text-slate-700">膜厚</th><td class="px-4 py-3 text-slate-600">下地寄与が混ざる</td></tr>
                    </tbody>
                </table>
            </div>
        `,
        calibration: `
            <div class="rounded-3xl bg-slate-50 p-4">
                <svg viewBox="0 0 260 120" class="w-full">
                    <rect x="28" y="34" width="52" height="56" rx="10" fill="#ccfbf1"/>
                    <rect x="104" y="22" width="52" height="68" rx="10" fill="#99f6e4"/>
                    <rect x="180" y="42" width="52" height="48" rx="10" fill="#5eead4"/>
                    <text x="32" y="104" font-size="11" fill="#0f172a">標準A</text>
                    <text x="108" y="104" font-size="11" fill="#0f172a">標準B</text>
                    <text x="184" y="104" font-size="11" fill="#0f172a">未知試料</text>
                </svg>
            </div>
        `,
        safety: `
            <div class="overflow-hidden rounded-3xl border border-slate-200">
                <table class="w-full text-sm">
                    <tbody>
                        <tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">禁止</th><td class="px-4 py-3 text-slate-600">扉開放測定</td></tr>
                        <tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">禁止</th><td class="px-4 py-3 text-slate-600">インターロック無効化</td></tr>
                        <tr><th class="px-4 py-3 text-left font-bold text-slate-700">優先</th><td class="px-4 py-3 text-slate-600">安全確認後に測定品質</td></tr>
                    </tbody>
                </table>
            </div>
        `
    };

    const XRF_VISUAL_MODELS = {
        sus304: {
            label: "SUS系合金",
            note: "Fe, Cr, Ni を主に見る標準例です。",
            matrixComplexity: 1.8,
            peaks: [
                { label: "Cr Kα", energy: 5.41, width: 0.15, height: 0.6 },
                { label: "Fe Kα", energy: 6.40, width: 0.14, height: 1.0 },
                { label: "Ni Kα", energy: 7.47, width: 0.16, height: 0.52 }
            ]
        },
        brass: {
            label: "真鍮",
            note: "Cu と Zn のピーク差が見やすい例です。",
            matrixComplexity: 1.4,
            peaks: [
                { label: "Cu Kα", energy: 8.04, width: 0.16, height: 0.95 },
                { label: "Zn Kα", energy: 8.64, width: 0.16, height: 0.72 }
            ]
        },
        mineral: {
            label: "鉱物・粉末",
            note: "Si, Ca, Fe などが混在し、母材影響の説明に向きます。",
            matrixComplexity: 2.6,
            peaks: [
                { label: "Si Kα", energy: 1.74, width: 0.12, height: 0.42, light: true, surface: true },
                { label: "Ca Kα", energy: 3.69, width: 0.14, height: 0.55 },
                { label: "Fe Kα", energy: 6.40, width: 0.15, height: 0.48 }
            ]
        },
        polymer: {
            label: "樹脂添加元素",
            note: "Br, Ti, Ca など添加元素の有無確認向けです。",
            matrixComplexity: 2.2,
            peaks: [
                { label: "Cl Kα", energy: 2.62, width: 0.12, height: 0.36, light: true, surface: true },
                { label: "Ca Kα", energy: 3.69, width: 0.14, height: 0.44 },
                { label: "Ti Kα", energy: 4.51, width: 0.13, height: 0.40 },
                { label: "Br Kα", energy: 11.92, width: 0.18, height: 0.70 }
            ]
        }
    };

    const XRF_INTRO_CARDS = [
        {
            id: "what",
            eyebrow: "WHAT",
            title: "XRF とは何か",
            body: "一次X線で元素を励起し、返ってくる蛍光X線のエネルギーを読んで元素を見分ける非破壊分析です。"
        },
        {
            id: "learn",
            eyebrow: "LEARN",
            title: "何が分かるか",
            body: "元素の有無確認、材質違いのスクリーニング、表面処理や異物混入の一次判定に向きます。"
        },
        {
            id: "misread",
            eyebrow: "MISREAD",
            title: "何を誤解しやすいか",
            body: "軽元素が見えないことを『存在しない』と決めつけること、強度をそのまま量とみなすこと、安全手順を軽視することが代表例です。"
        }
    ];

    const XRF_INTRO_SUMMARY_STATES = {
        empty: {
            label: "診断待ち",
            text: "最初の 3 問に答えると、原理から入るか、限界と安全から入るかを案内します。"
        },
        low: {
            label: "原理から着手",
            text: "まずは励起、蛍光X線、スペクトルのつながりを骨格として押さえる段階です。"
        },
        medium: {
            label: "限界整理が効果的",
            text: "概要は入っています。次は軽元素、マトリクス影響、安全管理の混線をほどくと理解が安定します。"
        },
        high: {
            label: "運用判断へ進める",
            text: "基礎は入っています。AI 対話と理解確認で、スクリーニングと定量をどう言い分けるかを詰める段階です。"
        }
    };

    const XRF_VISUAL_LEARNING = {
        title: "条件を変えて、スペクトルの読みどころを見る",
        description:
            "ここでは厳密な装置シミュレーションではなく、見え方がどう変わるかをつかむ概念モデルを使います。雰囲気、表面被覆、測定時間で何が変わるかを確認してください。",
        buildScenario: buildXrfScenario,
        materialLabel: "サンプルモデル",
        controls: [
            {
                field: "atmosphere",
                label: "測定雰囲気",
                type: "select",
                options: [
                    { value: "air", label: "空気中" },
                    { value: "helium", label: "Heパージ相当" }
                ],
                formatValue(value) {
                    return value === "helium" ? "Heパージ相当" : "空気中";
                }
            },
            {
                field: "coatingThickness",
                label: "表面被覆厚み",
                type: "range",
                min: 0,
                max: 40,
                step: 2,
                formatValue(value) {
                    return `${value} um`;
                }
            },
            {
                field: "acquisitionTime",
                label: "測定時間",
                type: "range",
                min: 5,
                max: 40,
                step: 5,
                formatValue(value) {
                    return `${value} s`;
                }
            }
        ],
        chartCaption:
            "緑の線は相対スペクトルの概念図です。ピーク位置で元素、見え方の変化で雰囲気や被覆の影響をつかみます。",
        axisLabels: {
            x: "エネルギー (keV)",
            y: "相対強度"
        }
    };

    const XRF_DIAGNOSIS_QUESTIONS = {
        q1: {
            id: "q1",
            prompt: "XRF のピークが大きいほど、その元素量をどんな試料でもそのまま比較してよい。",
            whyEasy: "グラフの山の高さがそのまま量に見えるため、母材や膜厚の影響を忘れやすいからです。",
            options: [
                {
                    id: "q1-a",
                    label: "はい。ピークが高い方が量も多いと単純に言える。",
                    explanation: "ピーク強度は量の手がかりですが、母材、膜厚、表面被覆、測定条件の影響を受けます。",
                    correct: false,
                    misconception: true,
                    weakness: ["matrix"],
                    next: "q2"
                },
                {
                    id: "q1-b",
                    label: "いいえ。まず条件差やマトリクス影響を確認する。",
                    explanation: "その通りです。XRF はまずスクリーニングと比較条件の整合を意識すると解釈が安定します。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q2"
                }
            ]
        },
        q2: {
            id: "q2",
            prompt: "空気中測定で軽元素のピークが見えにくいとき、最初に疑うべき説明はどれですか。",
            whyEasy: "見えないと存在しないと結論しやすい一方で、XRF は条件に強く依存するためです。",
            options: [
                {
                    id: "q2-a",
                    label: "試料にその元素は絶対に入っていない。",
                    explanation: "低エネルギーX線は空気や窓材で減衰しやすく、見えないことと存在しないことは同じではありません。",
                    correct: false,
                    misconception: true,
                    weakness: ["light"],
                    next: "q3"
                },
                {
                    id: "q2-b",
                    label: "雰囲気や装置条件のために見えにくくなっている可能性がある。",
                    explanation: "その通りです。He パージや真空条件、窓材、表面状態を確認します。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q3"
                }
            ]
        },
        q3: {
            id: "q3",
            prompt: "XRF の社内説明で、最優先で伝えるべき姿勢はどれですか。",
            whyEasy: "非破壊で手軽に見えるため、安全装置を軽視した説明になりやすいからです。",
            options: [
                {
                    id: "q3-a",
                    label: "安全手順より先に、早く結果が出ることを強調する。",
                    explanation: "X線装置としての安全が前提です。扉、インターロック、治具の扱いを先に徹底します。",
                    correct: false,
                    misconception: true,
                    weakness: ["safety"],
                    next: "q4"
                },
                {
                    id: "q3-b",
                    label: "安全確認が前提で、その上で何が分かるかを説明する。",
                    explanation: "その通りです。測定品質より前に安全管理が成立している必要があります。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: "q4"
                }
            ]
        },
        q4: {
            id: "q4",
            prompt: "XRF で最も適切な用途の整理はどれですか。",
            whyEasy: "万能分析のように見えやすく、用途の射程を広げすぎるためです。",
            options: [
                {
                    id: "q4-a",
                    label: "元素スクリーニングや材質違いの一次判定に向く。",
                    explanation: "その通りです。まずは元素の有無確認や比較用途に強い、と説明するのが安全です。",
                    correct: true,
                    misconception: false,
                    weakness: [],
                    next: null
                },
                {
                    id: "q4-b",
                    label: "どんな試料でも化学状態や価数までそのまま分かる。",
                    explanation: "一般的な卓上 XRF の説明としては過大です。化学状態や価数の議論は別手法が必要になることが多いです。",
                    correct: false,
                    misconception: true,
                    weakness: ["spectrum", "calibration"],
                    next: null
                }
            ]
        }
    };

    const XRF_AI_SUGGESTED_PATHS = [
        "XRF のピーク位置とピーク強度の違いを初心者向けに説明してください。",
        "軽元素が見えにくい理由を、空気中測定の制約も含めて整理してください。",
        "XRF を『定量』ではなく『スクリーニング』として説明する言い方を考えたいです。",
        "安全管理を先に伝えつつ、使うメリットも落とさない説明順を作りたいです。"
    ];

    const XRF_LOCAL_AI_TOPICS = [
        {
            keywords: ["軽元素", "空気", "ヘリウム", "真空"],
            answer: [
                "軽元素ほど低エネルギーのX線になり、空気や窓材で減衰しやすくなります。",
                "そのため、空気中で見えないことを『存在しない』と即断しないでください。",
                "説明するときは、He パージや真空で見え方が変わる可能性がある、と一言添えると安全です。"
            ]
        },
        {
            keywords: ["ピーク", "強度", "定量", "マトリクス"],
            answer: [
                "ピーク位置は元素同定、ピーク強度は量の手がかりです。",
                "ただし、母材、膜厚、表面被覆、測定条件で強度は変わるため、異なる試料間で単純比較しないでください。",
                "まずはスクリーニング、比較するなら条件整合、厳密定量なら標準や較正が必要、と整理すると伝わりやすいです。"
            ]
        },
        {
            keywords: ["安全", "扉", "インターロック"],
            answer: [
                "XRF は非破壊で手軽に見えても、X線装置としての安全管理が前提です。",
                "扉開放測定やインターロック無効化は論外で、説明順も『安全確認が先、その上で測定』が基本です。",
                "社内説明では『早い・便利』より前に『安全手順を守る』を置いてください。"
            ]
        }
    ];

    const XRF_EXPLANATION_RUBRIC = [
        {
            id: "excitation",
            title: "励起から蛍光X線発生まで触れていること",
            keywords: ["一次X線", "励起", "蛍光X線", "元素固有"]
        },
        {
            id: "spectrum",
            title: "ピーク位置と強度の役割を分けていること",
            keywords: ["ピーク", "位置", "強度", "元素", "量"]
        },
        {
            id: "limits",
            title: "軽元素やマトリクス影響などの限界に触れていること",
            keywords: ["軽元素", "空気", "マトリクス", "膜厚", "被覆"]
        },
        {
            id: "safety",
            title: "安全管理を前提として説明していること",
            keywords: ["安全", "扉", "インターロック", "X線"]
        }
    ];

    const XRF_MASTERY_QUIZ = [
        {
            id: "m1",
            prompt: "XRF のピーク位置から主に読みたいものはどれですか。",
            choices: [
                { id: "m1a", label: "どの元素か", correct: true, explanation: "ピーク位置は元素固有なので、まず元素同定に使います。" },
                { id: "m1b", label: "試料の色", correct: false, explanation: "色はスペクトル位置から直接は分かりません。" },
                { id: "m1c", label: "安全手順の有無", correct: false, explanation: "安全手順はスペクトルから読むものではありません。" }
            ]
        },
        {
            id: "m2",
            prompt: "空気中で軽元素が見えにくい主な理由は何ですか。",
            choices: [
                { id: "m2a", label: "低エネルギーX線が減衰しやすいから", correct: true, explanation: "空気や窓材で減衰しやすく、見え方が大きく変わります。" },
                { id: "m2b", label: "軽元素は蛍光X線を出さないから", correct: false, explanation: "出さないわけではなく、検出しにくくなります。" },
                { id: "m2c", label: "測定時間が長いほど必ず消えるから", correct: false, explanation: "本質は低エネルギー側の減衰です。" }
            ]
        },
        {
            id: "m3",
            prompt: "XRF のピーク強度をそのまま試料間比較しにくい理由として適切なのはどれですか。",
            choices: [
                { id: "m3a", label: "母材や表面被覆などのマトリクス影響があるから", correct: true, explanation: "強度は量だけでなく、周囲の条件にも左右されます。" },
                { id: "m3b", label: "検出器が常に同じ元素しか読まないから", correct: false, explanation: "そういう制約ではありません。" },
                { id: "m3c", label: "どの元素でもピーク位置が同じだから", correct: false, explanation: "ピーク位置は元素ごとに異なります。" }
            ]
        },
        {
            id: "m4",
            prompt: "XRF の社内説明で最初に置くべき姿勢はどれですか。",
            choices: [
                { id: "m4a", label: "安全管理を前提に、その上で用途を説明する", correct: true, explanation: "非破壊でもX線装置なので、安全が最優先です。" },
                { id: "m4b", label: "手軽さを先に強調し、安全は後で触れる", correct: false, explanation: "順序が逆です。" },
                { id: "m4c", label: "価数まで分かると先に説明する", correct: false, explanation: "一般説明としては過大です。" }
            ]
        }
    ];

    const XRF_DIAGNOSIS_UI = {
        noMistakesText: "大きな誤解はまだ表面化していません。次は理解確認で、用途の射程と限界を自分の言葉で整理してください。",
        noRevisitTagText: "再学習候補はまだ絞られていません",
        nextActions: [
            { section: "visual", label: "図解でスペクトルの見え方を見直す" },
            { section: "ai", label: "AI対話で用途と限界を言語化する" },
            { section: "mastery", label: "選択式テストで仕上げる" }
        ]
    };

    const XRF_AI_UI = {
        textareaPlaceholder: "例: XRF を『元素スクリーニングには強いが万能ではない』と伝える説明文を考えてください。",
        mediaEmptyTitle: "動画は必須ではありません",
        mediaEmptyBody:
            "まずは原理、限界、安全を図解と診断で押さえます。あとから装置デモ動画や社内操作動画を追加しても、この枠を流用できます。"
    };

    const XRF_HERO = {
        eyebrow: "ADAPTIVE LEARNING",
        titleLead: "蛍光X線分析装置を",
        titleAccent: "誤解なく説明できる状態",
        titleTrail: "まで持っていく",
        subtitle: "未知領域理解のための学習アプリ",
        description:
            "原理だけでなく、軽元素の制約、マトリクス影響、安全管理まで切り分けて理解するための学習アプリです。最後は選択式の理解確認で、どこが弱いかまで確認できます。"
    };

    const NANOINDENTER_TOPIC = {
        id: "nanoin",
        name: "ナノインデンター",
        pageTitle: "ナノインデンター適応型学習アプリ",
        storageKeySuffix: "nanoin",
        hero: HERO,
        introCards: INTRO_OVERVIEW_CARDS,
        introSummaryStates: INTRO_SUMMARY_STATES,
        selfCheck: INTRO_SELF_CHECK,
        figureCards: FIGURE_CARDS,
        concepts: CONCEPTS,
        conceptSupplements: CONCEPT_SUPPLEMENTS,
        visualModels: VISUAL_MODELS,
        visualLearning: VISUAL_LEARNING,
        diagnosisQuestions: DIAGNOSIS_QUESTIONS,
        diagnosisUi: DIAGNOSIS_UI,
        defaults: {
            currentSection: "intro",
            conceptLevel: "basic",
            activeConceptId: "curve",
            diagnosisStartQuestionId: "q1",
            visual: {
                material: "ceramic",
                filmThickness: 120,
                roughness: 6,
                tipRadius: 35
            },
            ai: {
                initialMessage:
                    "ここでは自由質問に答えるだけでなく、理解を深めるための次の一問も提案します。まずは気になるテーマを 1 つ選ぶか、自分の疑問を書いてください。"
            },
            settings: {
                apiProvider: "gemini",
                apiModel: "gemini-2.0-flash"
            }
        },
        ai: {
            systemInstruction:
                "あなたはナノインデンター学習アプリの対話コーチです。日本語で簡潔に答え、最後に次の理解確認質問を 3 つ以内で提案してください。過度に断定せず、硬さ・弾性率・基板影響・表面粗さ・Oliver-Pharr 前提の切り分けを重視してください。",
            suggestedPaths: AI_SUGGESTED_PATHS,
            localTopics: LOCAL_AI_TOPICS,
            explanationRubric: EXPLANATION_RUBRIC,
            ui: AI_UI
        },
        masteryQuiz: MASTERY_QUIZ,
        media: {
            title: "参考リソース",
            description:
                "動画は必須にせず、差し替え可能な任意アセットとして扱います。いまは KLA の参照リンクを置き、将来は YouTube やローカル動画を同じ枠に差し込める構成です。",
            featuredVideo: null,
            resources: REFERENCE_RESOURCES
        }
    };

    const XRF_TOPIC = {
        id: "xrf",
        name: "蛍光X線分析装置",
        pageTitle: "蛍光X線分析装置 適応型学習アプリ",
        storageKeySuffix: "xrf",
        hero: XRF_HERO,
        introCards: XRF_INTRO_CARDS,
        introSummaryStates: XRF_INTRO_SUMMARY_STATES,
        selfCheck: XRF_SELF_CHECK,
        figureCards: XRF_FIGURE_CARDS,
        concepts: XRF_CONCEPTS,
        conceptSupplements: XRF_CONCEPT_SUPPLEMENTS,
        visualModels: XRF_VISUAL_MODELS,
        visualLearning: XRF_VISUAL_LEARNING,
        diagnosisQuestions: XRF_DIAGNOSIS_QUESTIONS,
        diagnosisUi: XRF_DIAGNOSIS_UI,
        defaults: {
            currentSection: "intro",
            conceptLevel: "basic",
            activeConceptId: "excitation",
            diagnosisStartQuestionId: "q1",
            visual: {
                material: "sus304",
                atmosphere: "air",
                coatingThickness: 10,
                acquisitionTime: 20
            },
            ai: {
                initialMessage:
                    "ここでは XRF の原理、限界、安全の切り分けを一緒に進めます。説明に迷う点や、利用者へどう伝えるかを書いてください。"
            },
            settings: {
                apiProvider: "gemini",
                apiModel: "gemini-2.0-flash"
            }
        },
        ai: {
            systemInstruction:
                "あなたは蛍光X線分析装置の学習アプリの対話コーチです。日本語で簡潔に答え、最後に次の理解確認質問を 3 つ以内で提案してください。軽元素の制約、マトリクス影響、安全管理、スクリーニング用途と定量用途の切り分けを重視してください。",
            suggestedPaths: XRF_AI_SUGGESTED_PATHS,
            localTopics: XRF_LOCAL_AI_TOPICS,
            explanationRubric: XRF_EXPLANATION_RUBRIC,
            ui: XRF_AI_UI
        },
        masteryQuiz: XRF_MASTERY_QUIZ,
        media: {
            title: "参考リソース",
            description:
                "動画は必須にせず、差し替え可能な任意アセットとして扱います。まずは図解と診断で基礎を固め、必要なら装置デモや社内操作動画をあとから足す構成です。",
            featuredVideo: null,
            resources: []
        }
    };

    const TOPICS = {
        nanoin: NANOINDENTER_TOPIC,
        xrf: XRF_TOPIC
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

    const defaultTopicId = resolveDefaultTopicId(TOPICS, "nanoin");
    const defaultTopic = TOPICS[defaultTopicId] || NANOINDENTER_TOPIC;

    window.NanoLearnContent = {
        meta: APP_META,
        sections: APP_SECTIONS,
        defaultTopicId,
        topics: TOPICS,
        topic: defaultTopic,
        APP_SECTIONS,
        INTRO_SELF_CHECK,
        CONCEPTS,
        VISUAL_MODELS,
        DIAGNOSIS_QUESTIONS,
        AI_SUGGESTED_PATHS,
        LOCAL_AI_TOPICS,
        EXPLANATION_RUBRIC,
        MASTERY_QUIZ,
        FIGURE_CARDS,
        CONCEPT_SUPPLEMENTS,
        REFERENCE_RESOURCES
    };
})();
