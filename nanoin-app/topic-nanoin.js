(function () {
    window.NanoLearnTopicModules = window.NanoLearnTopicModules || {};

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
        const contactNormalized = (contactDepth - finalDepth) / Math.max(maxDepth - finalDepth, 1);
        const contactLoad = Number((maxLoad * Math.pow(Math.max(contactNormalized, 0), 1.45)).toFixed(2));
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
                            { x: contactDepth, y: contactLoad, label: "hc" }
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

    const AI_UI = {
        textareaPlaceholder: "例: なぜ膜厚が薄いと硬さが高く見えやすいのか、基板影響の観点で説明して",
        mediaEmptyTitle: "参考動画はまだ設定していません",
        mediaEmptyBody: "まずは図解と誤解診断で前提を固め、その後に必要なら装置動画や社内資料へ進む構成です。"
    };

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
        xAxisRange: {
            min: 0,
            max: 420
        },
        yAxisRange: {
            min: 0,
            max: 14
        },
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

    const NANO_PRINCIPLE = {
        eyebrow: "MEASUREMENT PRINCIPLE",
        title: "押し込みと除荷を、同じ曲線で読む",
        description:
            "ナノインデンターは圧子を押し込むときの荷重と深さを連続取得し、除荷初期の戻り方から接触剛性を読みます。くぼみの見た目ではなく、荷重-深さ応答そのものが測定原理の中心です。",
        scene: {
            type: "nano",
            visual: {
                frameLabelLeft: "LOAD",
                frameLabelRight: "DEPTH",
                showContactHalo: true,
                showStressFan: true,
                showDepthMarker: true,
                showCurve: true,
                showFilm: true,
                showSubstrate: true,
                indentClass: "scene-indent-medium",
                labels: ["押込み", "接触", "除荷初期"],
                caption: "押し込みながら荷重と深さを取得し、除荷初期の勾配から接触剛性を読む構造です。"
            }
        },
        quickFacts: [
            { label: "入力", body: "荷重を増やしながら圧子を押し込む" },
            { label: "観測", body: "深さが連続で記録される" },
            { label: "支点", body: "除荷初期の勾配 S を見る" },
            { label: "注意", body: "面積関数と表面状態の前提が崩れると解釈が危うい" }
        ],
        steps: [
            { step: "01", title: "押し込みで応答をつくる", body: "負荷中の曲線は、材料だけでなく先端形状や表面状態の影響も受けます。" },
            { step: "02", title: "最大荷重で接触状態が決まる", body: "hmax そのものより、どこまで有効接触しているかを次段で切り分けます。" },
            { step: "03", title: "除荷初期で剛性を読む", body: "最初の戻り勾配から接触剛性を見て、弾性率推定へつなげます。" }
        ],
        callout: {
            title: "数字より先に確認すること",
            body: "薄膜なら基板影響、浅部なら表面粗さと先端丸み、解析なら Oliver-Pharr の前提が保たれているかを先に確認します。"
        },
        details: [
            { title: "hmax と hc は同じではない", body: "見えている最大深さ hmax と、面積計算に使う接触深さ hc は役割が違います。" },
            { title: "除荷勾配は万能ではない", body: "除荷初期がきれいに弾性支配と見なせるかを必ず疑います。" }
        ]
    };

    const NANO_CONCEPT_SCENES = {
        curve: {
            type: "nano",
            eyebrow: "EXPLAINABLE ANIMATION",
            title: "押す・止める・戻すを 1 本で追う",
            summary: "荷重-変位曲線は結果表ではなく、圧子と試料のやり取り全体を残した履歴です。",
            checks: ["hmax", "hc", "hf"],
            beats: [
                {
                    step: "01",
                    title: "負荷で深さが伸びる",
                    body: "圧子が入り、曲線が右上へ伸びる。最大深さ hmax はまず最初に押さえる基準点です。"
                },
                {
                    step: "02",
                    title: "保持で時間依存を疑う",
                    body: "その場で止めたときの揺れは、クリープやドリフト補正の必要性を示す手掛かりになります。"
                },
                {
                    step: "03",
                    title: "除荷の戻り方を読む",
                    body: "戻り始めの勾配は弾性率側、最後に残る深さ hf は塑性変形側の情報として分けて見ます。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-nano concept-scene-curve",
                indentClass: "scene-indent-deep",
                showCurve: true,
                showFilm: true,
                labels: ["Load", "Depth", "Unload slope"],
                caption: "最大値だけでなく、戻り始めの傾きと残留深さまで一連で読む。"
            }
        },
        contact: {
            type: "nano",
            eyebrow: "CONTACT AREA",
            title: "見た深さと接触深さを分ける",
            summary: "硬さは見かけの侵入深さではなく、有効な接触面積で決まります。",
            checks: ["Contact", "Area", "Radius"],
            beats: [
                {
                    step: "01",
                    title: "圧子先端が最初に触れる",
                    body: "接触の瞬間は 1 点でも、その後に有効半径が広がるので、単純な見た目の深さとは一致しません。"
                },
                {
                    step: "02",
                    title: "有効面積が計算で決まる",
                    body: "接触深さ hc と面積関数がつながり、硬さ計算に使う A がここで決まります。"
                },
                {
                    step: "03",
                    title: "浅部ほど不安定になる",
                    body: "先端丸みや pile-up / sink-in を無視すると、面積推定がずれて結果全体が崩れます。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-nano concept-scene-contact",
                indentClass: "scene-indent-shallow",
                showContactHalo: true,
                labels: ["Contact point", "Area", "Radius"],
                caption: "見た深さではなく、有効接触面積がどこで決まるかに注目する。"
            }
        },
        hardness: {
            type: "nano",
            eyebrow: "PLASTIC RESPONSE",
            title: "最大荷重を面積で割って意味づける",
            summary: "硬さは『どれだけ入りにくいか』の指標であり、強度や靭性の代表値ではありません。",
            checks: ["Pmax", "Area", "Hardness"],
            beats: [
                {
                    step: "01",
                    title: "Pmax を支点に置く",
                    body: "最大荷重 Pmax は式の分子ですが、それだけでは硬さになりません。"
                },
                {
                    step: "02",
                    title: "接触面積とセットで読む",
                    body: "同じ荷重でも面積が広ければ硬さは下がるため、接触深さの推定がそのまま効きます。"
                },
                {
                    step: "03",
                    title: "性能全体へ拡張しすぎない",
                    body: "硬さは局所塑性の指標です。引張強さや靭性と自動で同一視しないことが重要です。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-nano concept-scene-hardness",
                indentClass: "scene-indent-deep",
                showStressFan: true,
                labels: ["Pmax", "Area", "Hardness"],
                caption: "荷重と接触面積を 1 組として見ると、硬さの守備範囲が分かる。"
            }
        },
        modulus: {
            type: "nano",
            eyebrow: "ELASTIC RETURN",
            title: "戻り始めの勾配で弾性を読む",
            summary: "弾性率は最大荷重ではなく、除荷初期の押し返し方から見積もります。",
            checks: ["Elastic", "Slope", "Er"],
            beats: [
                {
                    step: "01",
                    title: "除荷初期だけを切り出す",
                    body: "戻り始めの最初の傾きが、弾性的な押し返しの強さを最もよく反映します。"
                },
                {
                    step: "02",
                    title: "ばねの戻りと重ねて考える",
                    body: "反発が強いほど勾配は急になります。硬さとは別軸だと視覚的に分けておきます。"
                },
                {
                    step: "03",
                    title: "荒れた曲線は前提を疑う",
                    body: "粗さ、保持不足、接触検出の揺れがあると、弾性率推定の信頼性が一気に落ちます。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-nano concept-scene-modulus",
                indentClass: "scene-indent-medium",
                showSpring: true,
                showCurve: true,
                labels: ["Elastic recovery", "Slope", "Reduced modulus"],
                caption: "除荷の立ち上がりを、反発の強さとして読む。"
            }
        },
        substrate: {
            type: "nano",
            eyebrow: "THIN FILM WINDOW",
            title: "膜だけを見ている深さかを確かめる",
            summary: "深く押しすぎると、膜ではなく基材まで一緒に読んでしまいます。",
            checks: ["Film", "Substrate", "Depth ratio"],
            beats: [
                {
                    step: "01",
                    title: "膜と基材を層で意識する",
                    body: "同じ押し込みでも、浅い領域では膜、深い領域では基材の寄与が混ざります。"
                },
                {
                    step: "02",
                    title: "接触深さと膜厚の比を見る",
                    body: "10% ルールは出発点です。実際には物性差や残留応力で安全域が前後します。"
                },
                {
                    step: "03",
                    title: "深いほど安定とは限らない",
                    body: "ノイズを減らすために深くしすぎると、膜固有値ではなく見かけ値を読むことになります。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-nano concept-scene-substrate",
                indentClass: "scene-indent-deep",
                showFilm: true,
                showSubstrate: true,
                showDepthMarker: true,
                labels: ["Film", "Substrate", "10% rule"],
                caption: "膜を抜けて基材の応答が混ざり始める境界を探る。"
            }
        },
        roughness: {
            type: "nano",
            eyebrow: "SHALLOW NOISE",
            title: "浅いほど表面と先端の影響が出る",
            summary: "最浅部は材料本質より、表面粗さや先端丸みが前に出やすい領域です。",
            checks: ["Peak", "Valley", "Scatter"],
            beats: [
                {
                    step: "01",
                    title: "最初の当たり位置が揺れる",
                    body: "凸部に当たるか谷に当たるかで、最初の深さと面積推定が変わります。"
                },
                {
                    step: "02",
                    title: "先端丸みが浅部を支配する",
                    body: "理想形状からのずれは、浅い条件ほど相対的に大きな誤差として現れます。"
                },
                {
                    step: "03",
                    title: "size effect と即断しない",
                    body: "最浅部だけ高い、散る、再現しないときは、まず測定系の寄与を切り分けます。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-nano concept-scene-roughness",
                indentClass: "scene-indent-shallow",
                roughSurface: true,
                showContactHalo: true,
                labels: ["Peak", "Valley", "Scatter"],
                caption: "凹凸と先端形状が接触位置を揺らし、散りの原因になる。"
            }
        },
        oliver: {
            type: "nano",
            eyebrow: "ANALYSIS ASSUMPTION",
            title: "除荷曲線から逆算していく",
            summary: "Oliver-Pharr は見えた深さをそのまま使わず、除荷曲線から接触深さを戻し計算する考え方です。",
            checks: ["Unload fit", "hc", "Area function"],
            beats: [
                {
                    step: "01",
                    title: "除荷曲線を近似する",
                    body: "まず戻り始めの形を捉え、弾性支配の区間として扱えるかを見ます。"
                },
                {
                    step: "02",
                    title: "接触深さ hc を戻す",
                    body: "最大深さから補正量を引いて hc を求め、そこから面積関数へつなぎます。"
                },
                {
                    step: "03",
                    title: "前提が崩れる条件を意識する",
                    body: "圧子校正、自己相似形状、弾性支配が怪しいと、もっともらしい数値でも解釈が危うくなります。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-nano concept-scene-oliver",
                indentClass: "scene-indent-medium",
                showCurve: true,
                showSpring: true,
                showDepthMarker: true,
                labels: ["Unload fit", "hc", "Area function"],
                caption: "除荷曲線から接触深さを逆算し、面積関数へ渡す。"
            }
        }
    };

    const NANO_ROLE_TRACKS = [
        {
            id: "beginner",
            label: "初心者",
            summary: "用語と読み方を先に固める導線です。",
            recommendedSections: ["intro", "concepts", "visual", "diagnosis", "mastery"],
            focusCompetencies: ["curve-reading", "hardness-interpretation"]
        },
        {
            id: "operator",
            label: "現場オペレータ",
            summary: "測定条件の組み方とミス回避を優先します。",
            recommendedSections: ["intro", "visual", "diagnosis", "concepts", "record"],
            focusCompetencies: ["thin-film-window", "analysis-assumptions"]
        },
        {
            id: "analyst",
            label: "解析担当",
            summary: "曲線解釈と前提条件の検証を優先します。",
            recommendedSections: ["concepts", "visual", "diagnosis", "mastery", "record"],
            focusCompetencies: ["curve-reading", "analysis-assumptions"]
        }
    ];

    const NANO_COMPETENCIES = [
        {
            id: "curve-reading",
            title: "荷重-変位曲線の読解",
            summary: "除荷勾配と曲線形状から、何を読めるかを切り分ける力",
            conceptIds: ["curve", "modulus"],
            roleIds: ["beginner", "analyst"],
            sources: [
                { type: "intro", id: "curveReading" },
                { type: "diagnosis", id: "q3-unload" },
                { type: "mastery", id: "m1" },
                { type: "mission", id: "nanoin-modulus" }
            ],
            nextStep: {
                section: "visual",
                missionId: "nanoin-modulus",
                conceptId: "modulus",
                label: "除荷勾配ミッションで読みどころを確認"
            }
        },
        {
            id: "thin-film-window",
            title: "薄膜条件の見極め",
            summary: "基板影響と浅部ノイズの間で、安定域を探す力",
            conceptIds: ["substrate", "roughness"],
            roleIds: ["operator", "analyst"],
            sources: [
                { type: "intro", id: "errorFactors" },
                { type: "diagnosis", id: "q2-substrate" },
                { type: "diagnosis", id: "q4-surface" },
                { type: "mastery", id: "m2" },
                { type: "mastery", id: "m3" },
                { type: "mission", id: "nanoin-window" }
            ],
            nextStep: {
                section: "visual",
                missionId: "nanoin-window",
                conceptId: "substrate",
                label: "薄膜ウィンドウの境界を見直す"
            }
        },
        {
            id: "hardness-interpretation",
            title: "硬さの意味づけ",
            summary: "硬さを強度や靭性と混同せずに説明する力",
            conceptIds: ["hardness"],
            roleIds: ["beginner", "operator"],
            sources: [
                { type: "intro", id: "familiarity" },
                { type: "diagnosis", id: "q1" },
                { type: "diagnosis", id: "q2-strength" },
                { type: "mastery", id: "m4" }
            ],
            nextStep: {
                section: "concepts",
                conceptId: "hardness",
                label: "硬さノードで説明の射程を整理"
            }
        },
        {
            id: "analysis-assumptions",
            title: "解析前提の確認",
            summary: "接触深さや Oliver-Pharr の前提を点検する力",
            conceptIds: ["contact", "oliver"],
            roleIds: ["operator", "analyst"],
            sources: [
                { type: "intro", id: "errorFactors" },
                { type: "diagnosis", id: "q4-oliver" },
                { type: "mission", id: "nanoin-surface" }
            ],
            nextStep: {
                section: "visual",
                missionId: "nanoin-surface",
                conceptId: "contact",
                label: "浅部ノイズのミッションで前提を点検"
            }
        }
    ];

    const NANO_SIMULATION_MISSIONS = [
        {
            id: "nanoin-window",
            title: "薄膜ウィンドウを探す",
            summary: "100 nm 膜で、基板影響が混ざり始める前の見方を確認します。",
            conceptId: "substrate",
            competencyId: "thin-film-window",
            values: {
                material: "ceramic",
                filmThickness: 100,
                roughness: 6,
                tipRadius: 30
            },
            checks: [
                "接触深さ hc と膜厚の比を見る",
                "基板影響リスクが高いかどうかを言える",
                "深くしすぎたときの誤読を説明できる"
            ],
            completionText: "膜厚に対する接触深さの比で、膜だけを見ているかを判断できれば完了です。"
        },
        {
            id: "nanoin-surface",
            title: "浅部ノイズを疑う",
            summary: "浅い条件で、粗さと先端丸みが先に効く場面を確認します。",
            conceptId: "roughness",
            competencyId: "analysis-assumptions",
            values: {
                material: "ceramic",
                filmThickness: 80,
                roughness: 16,
                tipRadius: 85
            },
            checks: [
                "散りを size effect と即断しない",
                "粗さ・先端丸み・接触検出を先に疑う",
                "浅すぎる条件のリスクを説明できる"
            ],
            completionText: "最浅部のばらつきを材料本質と切り分けて説明できれば完了です。"
        },
        {
            id: "nanoin-modulus",
            title: "除荷勾配を読む",
            summary: "除荷初期勾配から弾性率を読む支点を確認します。",
            conceptId: "modulus",
            competencyId: "curve-reading",
            values: {
                material: "metal",
                filmThickness: 180,
                roughness: 4,
                tipRadius: 25
            },
            checks: [
                "除荷初期勾配がどこかを指させる",
                "硬さではなく弾性率側の情報だと言える",
                "曲線形状と解析前提をセットで見る"
            ],
            completionText: "除荷初期勾配が弾性率推定の支点だと説明できれば完了です。"
        }
    ];

    const AI_SUGGESTED_PATHS = [
        "荷重-変位曲線のどこを見れば硬さと弾性率を読み分けられますか。",
        "薄膜測定で基板影響と表面粗さのトレードオフを整理したいです。",
        "Oliver-Pharr の前提が崩れるケースを初心者向けに説明してください。",
        "膜厚 100 nm の硬質膜を測るときのプレテスト手順を考えたいです。"
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

    const NANOINDENTER_TOPIC = {
        id: "nanoin",
        name: "ナノインデンター",
        pageTitle: "ナノインデンター適応型学習アプリ",
        storageKeySuffix: "nanoin",
        hero: HERO,
        principle: NANO_PRINCIPLE,
        introCards: INTRO_OVERVIEW_CARDS,
        introSummaryStates: INTRO_SUMMARY_STATES,
        selfCheck: INTRO_SELF_CHECK,
        figureCards: FIGURE_CARDS,
        concepts: CONCEPTS,
        conceptSupplements: CONCEPT_SUPPLEMENTS,
        conceptScenes: NANO_CONCEPT_SCENES,
        visualModels: VISUAL_MODELS,
        visualLearning: VISUAL_LEARNING,
        diagnosisQuestions: DIAGNOSIS_QUESTIONS,
        diagnosisUi: DIAGNOSIS_UI,
        defaults: {
            currentSection: "intro",
            roleId: "beginner",
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
        roles: NANO_ROLE_TRACKS,
        competencies: NANO_COMPETENCIES,
        simulationMissions: NANO_SIMULATION_MISSIONS,
        masteryQuiz: MASTERY_QUIZ,
        media: {
            title: "参考リソース",
            description:
                "動画は必須にせず、差し替え可能な任意アセットとして扱います。いまは KLA の参照リンクを置き、将来は YouTube やローカル動画を同じ枠に差し込める構成です。",
            featuredVideo: null,
            resources: REFERENCE_RESOURCES
        }
    };

    window.NanoLearnTopicModules.nanoin = {
        topic: NANOINDENTER_TOPIC
    };
})();
