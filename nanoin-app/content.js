(function () {
    const APP_META = {
        appName: "Adaptive Topic Learning App",
        pageTitle: "ナノインデンター適応型学習アプリ",
        storageNamespace: "nano_learn_app"
    };

    const APP_SECTIONS = [
        { id: "intro", label: "概要を見る", short: "概要" },
        { id: "principle", label: "測定原理", short: "原理" },
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

    function buildTaverScenario(stateVisual, visualModels) {
        const model = visualModels[stateVisual.material];
        const wearMode = stateVisual.wearMode || "abrasive";
        const wheelType = stateVisual.wheelType || "h18";
        const load = Number(stateVisual.load || 500);
        const cycles = [0, 100, 200, 400, 600, 800, 1000];
        const wheelDefs = {
            cs10: { label: "CS-10", intensity: 0.82 },
            h18: { label: "H-18", intensity: 1.15 },
            h22: { label: "H-22", intensity: 1.52 }
        };
        const wearModels = {
            abrasive: {
                label: "アブレシブ摩耗",
                onset: "序盤から増え続ける",
                watch: "傷幅と増加勾配",
                caution: "標準的なテーバー条件に最も近い",
                calculate(normalized, wheelIntensity, loadFactor, sample) {
                    const base = 36 * sample.abrasiveBias * wheelIntensity * (0.72 + 0.42 * loadFactor);
                    return base * normalized * (0.9 + 0.1 * normalized);
                }
            },
            adhesive: {
                label: "凝着摩耗",
                onset: "途中から急増しやすい",
                watch: "急な立ち上がり",
                caution: "高荷重では焼き付き側へ寄りやすい",
                calculate(normalized, wheelIntensity, loadFactor, sample) {
                    const base = 11 * sample.adhesiveBias * (0.88 + 0.14 * wheelIntensity);
                    const transition = Math.max(0.2, 0.58 - 0.13 * loadFactor);
                    const severeWear = Math.max(0, normalized - transition);
                    return base * normalized + 120 * Math.pow(severeWear, 2.1) * sample.adhesiveBias * (0.68 + 0.42 * loadFactor);
                }
            },
            fatigue: {
                label: "疲労摩耗",
                onset: "潜伏後に欠けが出る",
                watch: "潜伏期間の後の増加",
                caution: "寿命や剥離面積も見る必要がある",
                calculate(normalized, wheelIntensity, loadFactor, sample) {
                    const incubation = Math.max(0.18, 0.7 - 0.18 * loadFactor);
                    const crackGrowth = Math.max(0, normalized - incubation);
                    return 4 + 6 * normalized + 145 * Math.pow(crackGrowth, 2.45) * sample.fatigueBias * (0.82 + 0.12 * wheelIntensity);
                }
            }
        };

        const wheel = wheelDefs[wheelType] || wheelDefs.h18;
        const activeWear = wearModels[wearMode] || wearModels.abrasive;
        const loadFactor = load / 500;
        const selectedData = cycles.map((cycle) => {
            const normalized = cycle / 1000;
            return {
                x: cycle,
                y: Number(activeWear.calculate(normalized, wheel.intensity, loadFactor, model).toFixed(1))
            };
        });
        const baselineData = cycles.map((cycle) => {
            const normalized = cycle / 1000;
            return {
                x: cycle,
                y: Number(activeWear.calculate(normalized, wheelDefs.h18.intensity, 1, model).toFixed(1))
            };
        });

        const finalWear = selectedData[selectedData.length - 1].y;
        const baselineWear = baselineData[baselineData.length - 1].y;
        const delta = Number((finalWear - baselineWear).toFixed(1));
        const damageRisk = finalWear >= 85 ? "高" : finalWear >= 45 ? "中" : "低";
        const deltaLabel = delta > 0 ? `+${delta.toFixed(1)} mg` : `${delta.toFixed(1)} mg`;
        const insights = [
            {
                title: "どこで増え始めるか",
                body: `${activeWear.label}では「${activeWear.onset}」形です。まずは序盤一定か、途中で曲がるかを見ます。`
            },
            {
                title: "標準条件との差",
                body: `同じ試料・同じ摩耗メカニズムで H-18 / 500g を基準線に置いています。今の条件は ${deltaLabel} の差です。`
            },
            {
                title: "説明時の注意",
                body: activeWear.caution
            }
        ];

        return {
            model,
            wearMode,
            wheelType,
            load,
            wheelLabel: wheel.label,
            finalWear,
            damageRisk,
            insights,
            metrics: [
                { id: "finalWear", label: "1000回後の摩耗量", value: `${finalWear.toFixed(1)} mg` },
                { id: "onset", label: "立ち上がり", value: activeWear.onset },
                { id: "watch", label: "見る場所", value: activeWear.watch },
                { id: "risk", label: "損傷リスク", value: damageRisk }
            ],
            chart: {
                type: "scatter",
                datasets: [
                    {
                        label: "現在の条件",
                        data: selectedData,
                        showLine: true,
                        borderColor: wearMode === "abrasive" ? "#0f766e" : wearMode === "adhesive" ? "#dc2626" : "#7c3aed",
                        backgroundColor: wearMode === "abrasive" ? "#0f766e" : wearMode === "adhesive" ? "#dc2626" : "#7c3aed",
                        borderWidth: 2.6,
                        pointRadius: 0,
                        tension: 0.22
                    },
                    {
                        label: "標準条件の比較線",
                        data: baselineData,
                        showLine: true,
                        borderColor: "#94a3b8",
                        backgroundColor: "#94a3b8",
                        borderDash: [8, 6],
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.18
                    }
                ],
                tooltipLabel(raw, context) {
                    const label = context && context.dataset ? context.dataset.label : "摩耗量";
                    return `${label}: ${raw.x} 回, ${raw.y.toFixed(1)} mg`;
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

    const XRF_CONCEPT_SCENES = {
        excitation: {
            type: "xrf",
            eyebrow: "EXPLAINABLE ANIMATION",
            title: "一次X線が入り、固有X線が返る",
            summary: "XRF の最小単位は、照射して終わりではなく、励起と放出が 1 往復でつながる流れです。",
            checks: ["Primary", "Atom", "Fluor"],
            beats: [
                {
                    step: "01",
                    title: "一次X線が原子へ入る",
                    body: "X線源からの入射で原子内に空孔が生まれ、そこがスタート地点になります。"
                },
                {
                    step: "02",
                    title: "電子遷移で固有X線が出る",
                    body: "埋め戻しのときに元素固有のエネルギー差が現れ、蛍光X線として外へ出ます。"
                },
                {
                    step: "03",
                    title: "返ってきた信号を読む",
                    body: "この戻り光がスペクトル上のピークになり、元素同定の出発点になります。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-xrf concept-scene-excitation",
                sourceLabel: "X-RAY",
                detectorLabel: "FLUOR",
                labels: ["Primary X-ray", "Atom", "Fluorescence"],
                caption: "励起と放出を 1 往復として見ると、XRF の骨格が掴みやすい。"
            }
        },
        spectrum: {
            type: "xrf",
            eyebrow: "PEAK READING",
            title: "位置で元素、強度で量の目安を分ける",
            summary: "スペクトルは山の高さだけを見る図ではなく、位置と強度を別々に解釈するための画面です。",
            checks: ["Energy", "Peak", "Element"],
            beats: [
                {
                    step: "01",
                    title: "ピーク位置で元素を探す",
                    body: "どこに山が立つかは、まず元素同定の手掛かりになります。"
                },
                {
                    step: "02",
                    title: "高さは量の目安として使う",
                    body: "ただし高さは条件依存です。位置の話と量の話を同じ強さで扱わないことが重要です。"
                },
                {
                    step: "03",
                    title: "重なりと背景を残して考える",
                    body: "見た目に分かりやすい山でも、重なりやバックグラウンドを無視すると誤読しやすくなります。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-xrf concept-scene-spectrum",
                sourceLabel: "SCAN",
                detectorLabel: "PEAK",
                showPeaks: true,
                showScan: true,
                labels: ["Energy", "Peak", "Element"],
                caption: "位置と高さを同時に見せるが、意味づけは分けて扱う。"
            }
        },
        light: {
            type: "xrf",
            eyebrow: "LOW ENERGY LIMIT",
            title: "軽元素は空気と窓材で見え方が変わる",
            summary: "見えにくいことと、存在しないことは別です。低エネルギー側は条件差の影響を強く受けます。",
            checks: ["Low-E", "Air loss", "He purge"],
            beats: [
                {
                    step: "01",
                    title: "低エネルギー側の信号を意識する",
                    body: "軽元素は低いエネルギーに現れるため、最初から不利な側にいます。"
                },
                {
                    step: "02",
                    title: "空気経路で減衰する",
                    body: "空気中ではその信号が落ちやすく、He パージや真空で見え方が変わります。"
                },
                {
                    step: "03",
                    title: "見えない理由を条件側に求める",
                    body: "検出器窓材、表面被覆、雰囲気を見直してから、存在しないと判断します。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-xrf concept-scene-light",
                sourceLabel: "LIGHT",
                detectorLabel: "LOW-E",
                showPeaks: true,
                showScan: true,
                sampleClass: "scene-sample-light",
                labels: ["Low energy", "Air loss", "He purge"],
                caption: "低エネルギー側ほど、経路条件の違いが見え方を左右する。"
            }
        },
        matrix: {
            type: "xrf",
            eyebrow: "MATRIX EFFECT",
            title: "周囲成分がピーク強度を押したり吸ったりする",
            summary: "ピーク強度は元素量だけで決まらず、母材や被覆との相互作用で変わります。",
            checks: ["Absorb", "Enhance", "Interfere"],
            beats: [
                {
                    step: "01",
                    title: "母材が信号を吸収する",
                    body: "同じ元素量でも、周囲の材料次第で検出器へ届く前に弱まることがあります。"
                },
                {
                    step: "02",
                    title: "逆に強め合う場合もある",
                    body: "近くの成分や表面被覆が励起効率を変え、見かけの強度を押し上げることもあります。"
                },
                {
                    step: "03",
                    title: "強度差を量差と短絡しない",
                    body: "まず条件差を疑う姿勢が、スクリーニングと定量を切り分ける基礎になります。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-xrf concept-scene-matrix",
                sourceLabel: "MATRIX",
                detectorLabel: "SHIFT",
                showMatrixLayers: true,
                labels: ["Absorption", "Enhancement", "Interference"],
                caption: "ピーク強度は、周囲成分との相互作用込みで現れている。"
            }
        },
        calibration: {
            type: "xrf",
            eyebrow: "STANDARD LINE",
            title: "定量は標準と条件整合の上に立つ",
            summary: "『どれだけ入っているか』を言うには、標準試料と測定条件の整合が必要です。",
            checks: ["Standards", "Fit", "Prediction"],
            beats: [
                {
                    step: "01",
                    title: "既知濃度の標準を並べる",
                    body: "まずは濃度が分かっている試料群で、強度との対応関係を作ります。"
                },
                {
                    step: "02",
                    title: "条件をそろえて線を作る",
                    body: "測定時間、雰囲気、幾何条件が変わると、その線は別物になります。"
                },
                {
                    step: "03",
                    title: "未知試料へ外挿する",
                    body: "比較用途と定量用途を分けて説明すると、利用者に誤期待を持たせにくくなります。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-xrf concept-scene-calibration",
                sourceLabel: "STD",
                detectorLabel: "FIT",
                showPeaks: true,
                showScan: true,
                labels: ["Standards", "Fit line", "Prediction"],
                caption: "標準の並びがあって初めて、未知試料の量へ話を進められる。"
            }
        },
        safety: {
            type: "xrf",
            eyebrow: "SAFETY FIRST",
            title: "測定品質より先に安全機構が成立する",
            summary: "XRF は非破壊でも X線装置です。安全管理は説明の後ろではなく先頭に置きます。",
            checks: ["Interlock", "Shield", "Door"],
            beats: [
                {
                    step: "01",
                    title: "扉と遮蔽が閉じる",
                    body: "照射前に、装置側の物理的な遮蔽と扉閉状態が成立している必要があります。"
                },
                {
                    step: "02",
                    title: "インターロックで照射を制御する",
                    body: "安全機構が有効なときだけ照射できる、という前提を崩さないことが最優先です。"
                },
                {
                    step: "03",
                    title: "その上で測定品質を見る",
                    body: "再現性や時間短縮の議論は、安全手順を満たした後に初めて意味を持ちます。"
                }
            ],
            visual: {
                sceneClass: "concept-scene-xrf concept-scene-safety",
                sourceLabel: "LOCK",
                detectorLabel: "SAFE",
                showShield: true,
                showDoor: true,
                labels: ["Interlock", "Shield", "Door closed"],
                caption: "安全機構は測定性能とは独立した、先に満たすべき条件。"
            }
        }
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
        xAxisRange: {
            min: 0,
            max: 12.5
        },
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

    const XRF_ROLE_TRACKS = [
        {
            id: "beginner",
            label: "初心者",
            summary: "原理とスペクトルの読み方から固める導線です。",
            recommendedSections: ["intro", "concepts", "visual", "diagnosis", "mastery"],
            focusCompetencies: ["excitation-spectrum", "light-element-limits"]
        },
        {
            id: "operator",
            label: "現場オペレータ",
            summary: "安全確認とスクリーニング運用を優先します。",
            recommendedSections: ["intro", "visual", "diagnosis", "concepts", "record"],
            focusCompetencies: ["screening-judgement", "safety-operation"]
        },
        {
            id: "analyst",
            label: "解析担当",
            summary: "マトリクス影響と定量限界の整理を優先します。",
            recommendedSections: ["concepts", "visual", "diagnosis", "mastery", "record"],
            focusCompetencies: ["screening-judgement", "light-element-limits"]
        }
    ];

    const XRF_COMPETENCIES = [
        {
            id: "excitation-spectrum",
            title: "励起からスペクトルまで",
            summary: "ピーク位置で元素、強度で量の目安を分けて説明する力",
            conceptIds: ["excitation", "spectrum"],
            roleIds: ["beginner", "analyst"],
            sources: [
                { type: "intro", id: "principle" },
                { type: "mastery", id: "m1" }
            ],
            nextStep: {
                section: "concepts",
                conceptId: "spectrum",
                label: "スペクトルノードで位置と強度を整理"
            }
        },
        {
            id: "light-element-limits",
            title: "軽元素の見え方",
            summary: "空気中、He、表面被覆で見え方が変わることを判断する力",
            conceptIds: ["light", "matrix"],
            roleIds: ["beginner", "analyst"],
            sources: [
                { type: "intro", id: "limits" },
                { type: "diagnosis", id: "q2" },
                { type: "mastery", id: "m2" },
                { type: "mission", id: "xrf-light-air" }
            ],
            nextStep: {
                section: "visual",
                missionId: "xrf-light-air",
                conceptId: "light",
                label: "軽元素ミッションで雰囲気差を見る"
            }
        },
        {
            id: "screening-judgement",
            title: "スクリーニング判断",
            summary: "強度差をそのまま定量にしないで、条件差を先に見る力",
            conceptIds: ["matrix", "calibration", "spectrum"],
            roleIds: ["operator", "analyst"],
            sources: [
                { type: "intro", id: "limits" },
                { type: "diagnosis", id: "q1" },
                { type: "diagnosis", id: "q4" },
                { type: "mastery", id: "m3" },
                { type: "mission", id: "xrf-coating" }
            ],
            nextStep: {
                section: "visual",
                missionId: "xrf-coating",
                conceptId: "matrix",
                label: "表面被覆ミッションで条件差を確認"
            }
        },
        {
            id: "safety-operation",
            title: "安全優先の運用",
            summary: "X線装置としての安全を、運用説明の先頭に置く力",
            conceptIds: ["safety"],
            roleIds: ["operator"],
            sources: [
                { type: "intro", id: "safety" },
                { type: "diagnosis", id: "q3" },
                { type: "mastery", id: "m4" },
                { type: "mission", id: "xrf-screening" }
            ],
            nextStep: {
                section: "visual",
                missionId: "xrf-screening",
                conceptId: "safety",
                label: "標準スクリーニング条件を安全前提で確認"
            }
        }
    ];

    const XRF_SIMULATION_MISSIONS = [
        {
            id: "xrf-light-air",
            title: "軽元素を空気中で測る",
            summary: "軽元素ピークが見えにくい条件を、He パージ相当と比較します。",
            conceptId: "light",
            competencyId: "light-element-limits",
            values: {
                material: "polymer",
                atmosphere: "air",
                coatingThickness: 12,
                acquisitionTime: 20
            },
            checks: [
                "見えないことと存在しないことを分けて考える",
                "空気中と He パージ相当で見え方が変わる理由を言える",
                "軽元素側の注意点を説明できる"
            ],
            completionText: "雰囲気で低エネルギー側の見え方が変わると説明できれば完了です。"
        },
        {
            id: "xrf-coating",
            title: "表面被覆の影響を見る",
            summary: "被覆がある試料で、ピーク強度を単純比較しない感覚を作ります。",
            conceptId: "matrix",
            competencyId: "screening-judgement",
            values: {
                material: "mineral",
                atmosphere: "air",
                coatingThickness: 28,
                acquisitionTime: 20
            },
            checks: [
                "ピーク強度は量だけでなく条件に依存すると言える",
                "母材や被覆の影響を先に疑う",
                "定量よりスクリーニングが先だと説明できる"
            ],
            completionText: "表面被覆や母材差で強度解釈が揺れると説明できれば完了です。"
        },
        {
            id: "xrf-screening",
            title: "標準スクリーニング条件を確認",
            summary: "比較用途に向く条件と、安全優先の説明順を確認します。",
            conceptId: "safety",
            competencyId: "safety-operation",
            values: {
                material: "sus304",
                atmosphere: "helium",
                coatingThickness: 0,
                acquisitionTime: 10
            },
            checks: [
                "安全確認が先、その後に測定と言える",
                "比較用途では条件整合が必要だと説明できる",
                "短時間測定の用途をスクリーニングと結び付けられる"
            ],
            completionText: "安全を前提にスクリーニング用途を説明できれば完了です。"
        }
    ];

    const XRF_REFERENCE_RESOURCES = [
        {
            id: "xrf-r1",
            title: "XRF Academy",
            url: "https://www.thermofisher.com/us/en/home/industrial/spectroscopy-elemental-isotope-analysis/spectroscopy-elemental-isotope-analysis-learning-center/elemental-structural-analysis-information/xrf-academy.html/1000",
            source: "Thermo Fisher",
            note: "XRF の原理、用途、限界を学習用に整理した公式リソース"
        },
        {
            id: "xrf-r2",
            title: "OES / XRF Trainings",
            url: "https://www.thermofisher.com/us/en/home/industrial/spectroscopy-elemental-isotope-analysis/oes-xrd-xrf-analysis/x-ray-fluorescence/services/oes-xrf-trainings.html",
            source: "Thermo Fisher",
            note: "運用・トレーニング導線の例として参照しやすい公式ページ"
        }
    ];

    const TAVER_HERO = {
        eyebrow: "ADAPTIVE LEARNING",
        titleLead: "テーバー摩耗試験を",
        titleAccent: "条件つきで説明できる状態",
        titleTrail: "まで持っていく",
        subtitle: "装置説明と条件相談のための学習アプリ",
        description:
            "摩耗メカニズムの切り分け、テーバー特有の rub-wear action、摩耗輪と荷重の選び方、結果の読み方までを一続きで学ぶ topic です。"
    };

    const TAVER_INTRO_CARDS = [
        { id: "what", eyebrow: "WHAT", title: "テーバー摩耗試験とは何か", body: "回転テーブル上の試料に 2 つの摩耗輪を押し当て、転がりとすべりを伴う rub-wear action で耐摩耗性を比較する試験です。" },
        { id: "learn", eyebrow: "LEARN", title: "どこを理解するか", body: "アブレシブ・凝着・疲労の違い、オフセット配置が生む摩耗痕、摩耗輪と荷重で何が変わるか、結果の読み方を学びます。" },
        { id: "misread", eyebrow: "MISREAD", title: "何を誤解しやすいか", body: "テーバーがすべての摩耗をそのまま再現するわけではないこと、荷重を上げれば単純比例で悪化するとは限らないことが誤解されやすい点です。" }
    ];

    const TAVER_SELF_CHECK = [
        { id: "mechanism", prompt: "テーバー摩耗試験が、主にどの摩耗説明に向いているか言えますか。", options: [{ value: 0, label: "まだ曖昧" }, { value: 1, label: "アブレシブ寄りとは言える" }, { value: 2, label: "凝着や疲労と何が違うかまで話せる" }] },
        { id: "offset", prompt: "2つの摩耗輪が試料中心と同心ではなく、オフセット配置される理由を説明できますか。", options: [{ value: 0, label: "まだ説明できない" }, { value: 1, label: "すべりが入ることは知っている" }, { value: 2, label: "交差円弧状の摩耗痕まで説明できる" }] },
        { id: "result", prompt: "質量減少と wear index の違いを説明できますか。", options: [{ value: 0, label: "まだ混ざっている" }, { value: 1, label: "1000回換算だとは分かる" }, { value: 2, label: "寿命や剥離面積との違いも分けて話せる" }] }
    ];

    const TAVER_INTRO_SUMMARY_STATES = {
        empty: { label: "診断前", text: "最初の 3 問に答えると、摩耗メカニズム・装置配置・結果解釈のどこから先に詰めるべきかを出します。" },
        low: { label: "まずは摩耗メカニズムから", text: "アブレシブ・凝着・疲労の違いと、テーバーが主にどこに向くかを先に固めるのが近道です。" },
        medium: { label: "装置説明と条件説明をつなぐ段階", text: "装置の原理はつかめています。次は摩耗輪、荷重、結果指標がどうつながるかを図解で確認すると伸びやすいです。" },
        high: { label: "条件相談に進める", text: "基礎説明はかなり安定しています。次は試料に応じた摩耗輪と荷重の選定、結果の解釈を詰める段階です。" }
    };

    const TAVER_FIGURE_CARDS = [
        { id: "taver-basics", label: "図 1", illustration: `<svg viewBox="0 0 260 120" class="w-full"><rect x="26" y="62" width="208" height="30" rx="12" fill="#cbd5e1"/><rect x="52" y="30" width="26" height="48" rx="6" fill="#115e59"/><rect x="182" y="30" width="26" height="48" rx="6" fill="#115e59"/><path d="M130 18 C130 34, 130 44, 130 60" fill="none" stroke="#0f172a" stroke-width="4" stroke-linecap="round"/><text x="42" y="106" font-size="11" fill="#0f766e">2つの摩耗輪</text><text x="111" y="106" font-size="11" fill="#334155">回転テーブル</text></svg>`, bullets: [{ label: "装置の核", body: "2つの摩耗輪を一定荷重で押し当て、試料を回転させる" }, { label: "見どころ", body: "転がりだけでなく、すべりが入る" }, { label: "誤解しやすい点", body: "純転がり試験ではない" }] },
        { id: "taver-offset", label: "図 2", illustration: `<svg viewBox="0 0 260 120" class="w-full"><circle cx="130" cy="60" r="42" fill="none" stroke="#94a3b8" stroke-width="3"/><path d="M74 58 A56 56 0 0 1 126 22" fill="none" stroke="#0f766e" stroke-width="5" stroke-linecap="round"/><path d="M186 62 A56 56 0 0 0 134 98" fill="none" stroke="#b45309" stroke-width="5" stroke-linecap="round"/><circle cx="92" cy="36" r="10" fill="#115e59"/><circle cx="168" cy="84" r="10" fill="#115e59"/><text x="72" y="108" font-size="11" fill="#0f766e">交差円弧状</text><text x="150" y="108" font-size="11" fill="#b45309">rub-wear</text></svg>`, bullets: [{ label: "配置", body: "中心一致ではなくオフセット配置" }, { label: "結果", body: "円環帯の中に交差円弧状の摩耗痕が出る" }, { label: "説明時の軸", body: "全方向から擦るので方向依存が出にくい" }] },
        { id: "taver-result", label: "図 3", illustration: `<svg viewBox="0 0 260 120" class="w-full"><path d="M20 92 C66 88, 110 74, 164 54" fill="none" stroke="#0f766e" stroke-width="5" stroke-linecap="round"/><path d="M20 92 C70 90, 120 84, 166 78" fill="none" stroke="#94a3b8" stroke-width="4" stroke-dasharray="8 6" stroke-linecap="round"/><line x1="18" y1="96" x2="238" y2="96" stroke="#94a3b8" stroke-width="2"/><line x1="18" y1="96" x2="18" y2="20" stroke="#94a3b8" stroke-width="2"/><text x="170" y="48" font-size="11" fill="#0f766e">現在条件</text><text x="168" y="74" font-size="11" fill="#64748b">標準比較線</text></svg>`, bullets: [{ label: "比較のしかた", body: "今の条件と標準条件を同じ軸で見る" }, { label: "読む場所", body: "序盤の立ち上がりか、中盤以降の急増か" }, { label: "結果の扱い", body: "質量減少だけでなく wear index や寿命評価も分ける" }] }
    ];

    const TAVER_CONCEPTS = [
        { id: "abrasive", title: "アブレシブ摩耗", short: "硬い粒子や突起が表面を削るメカニズム", beginner: "硬い粒子や突起が、やすりのように表面を削っていく摩耗です。標準的なテーバー摩耗試験が最も説明しやすい摩耗です。", advanced: "2元アブレシブ摩耗に近い条件で、摩耗輪の攻撃性、荷重、試料硬さで増加勾配が変わります。3元条件のように粒子が逃げる場面とは挙動が異なります。", relations: [{ target: "rubwear", label: "なぜテーバーで再現しやすいか" }, { target: "wearindex", label: "結果をどう数値化するか" }, { target: "adhesive", label: "何が違うかを切り分ける" }] },
        { id: "adhesive", title: "凝着摩耗", short: "面同士が局所的に接合して移着・脱落する摩耗", beginner: "強い圧力ですべると、表面の小さな突起同士がくっついてちぎれ、片方の材料が移る摩耗です。", advanced: "高荷重では接合点が育って途中から急増し、焼き付き側へ移ることがあります。標準テーバーはこれを単独で再現する試験ではありません。", relations: [{ target: "abrasive", label: "標準テーバーとの相性を比べる" }, { target: "fatigue", label: "途中から悪化する点は似るが原因は違う" }, { target: "rubwear", label: "すべり成分が増えると影響しやすい" }] },
        { id: "fatigue", title: "疲労摩耗", short: "繰り返し応力で表面下き裂が育って剥離する摩耗", beginner: "最初から大きく削れるとは限らず、しばらくしてから表面が欠け始める摩耗です。", advanced: "潜伏期間の後にピッチングやフレーキングが現れます。質量減少だけではなく、寿命や剥離面積を見る必要があります。", relations: [{ target: "wearindex", label: "質量減少だけでは読み切れない" }, { target: "adhesive", label: "急増する見え方は似ても原因は異なる" }, { target: "rubwear", label: "テーバーでは単独再現しにくい" }] },
        { id: "rubwear", title: "rub-wear action", short: "転がりとすべりが同時に入るテーバー特有の接触", beginner: "摩耗輪はただ転がるのではなく、すべりながら試料を擦ります。そのため特徴的な摩耗痕ができます。", advanced: "試料中心と摩耗輪中心を一致させず、規格位置にオフセットすることで交差円弧状の摩耗痕が出ます。これが全方向性のある比較を支えます。", relations: [{ target: "abrasive", label: "標準条件がアブレシブ説明に向く理由" }, { target: "wearindex", label: "同じ回転数でも接触の質が効く" }, { target: "fatigue", label: "転がり疲労試験そのものではない" }] },
        { id: "wearindex", title: "wear index / 結果解釈", short: "質量減少を条件つきで比較用の数値にする読み方", beginner: "質量減少そのものと、1000回換算した wear index は似て見えても用途が少し違います。", advanced: "寿命、剥離面積、外観変化まで含めて読むべき場面があり、wear index だけで実使用寿命を言い切るのは危険です。", relations: [{ target: "abrasive", label: "最もそのまま比較しやすい" }, { target: "fatigue", label: "質量減少以外の評価も要る" }, { target: "rubwear", label: "同じ数値でも接触様式を忘れない" }] }
    ];

    const TAVER_CONCEPT_SUPPLEMENTS = {
        abrasive: `<div class="rounded-3xl bg-slate-50 p-4"><div class="text-sm font-bold text-slate-900">見るポイント</div><ul class="mt-3 space-y-2 text-sm leading-6 text-slate-600"><li>摩耗輪の攻撃性を上げると、序盤から勾配が増えやすい</li><li>標準テーバーはこの説明に最も向いている</li><li>やすりがけに近い比喩が有効</li></ul></div>`,
        adhesive: `<div class="overflow-hidden rounded-3xl border border-slate-200"><table class="w-full text-sm"><tbody><tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">序盤</th><td class="px-4 py-3 text-slate-600">軽微な移着</td></tr><tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">中盤</th><td class="px-4 py-3 text-slate-600">接合点が育つ</td></tr><tr><th class="px-4 py-3 text-left font-bold text-slate-700">高荷重</th><td class="px-4 py-3 text-slate-600">焼き付き側へ寄りやすい</td></tr></tbody></table></div>`,
        fatigue: `<div class="rounded-3xl bg-slate-50 p-4"><div class="text-sm font-bold text-slate-900">質量減少だけでは足りない理由</div><ul class="mt-3 space-y-2 text-sm leading-6 text-slate-600"><li>潜伏期間があると、初期は変化が小さい</li><li>表面欠けや剥離面積で見たほうが伝わる場面がある</li><li>寿命評価と同じ意味ではない</li></ul></div>`,
        rubwear: `<div class="rounded-3xl bg-slate-50 p-4"><svg viewBox="0 0 260 120" class="w-full"><circle cx="130" cy="60" r="44" fill="none" stroke="#94a3b8" stroke-width="3"/><path d="M76 58 A56 56 0 0 1 126 24" fill="none" stroke="#0f766e" stroke-width="5" stroke-linecap="round"/><path d="M184 62 A56 56 0 0 0 134 96" fill="none" stroke="#b45309" stroke-width="5" stroke-linecap="round"/><text x="74" y="108" font-size="11" fill="#0f766e">交差円弧</text><text x="160" y="108" font-size="11" fill="#b45309">offset</text></svg></div>`,
        wearindex: `<div class="overflow-hidden rounded-3xl border border-slate-200"><table class="w-full text-sm"><tbody><tr class="border-b border-slate-200 bg-slate-50"><th class="px-4 py-3 text-left font-bold text-slate-700">質量減少</th><td class="px-4 py-3 text-slate-600">実測した減少量</td></tr><tr class="border-b border-slate-200"><th class="px-4 py-3 text-left font-bold text-slate-700">wear index</th><td class="px-4 py-3 text-slate-600">1000回換算の比較指標</td></tr><tr><th class="px-4 py-3 text-left font-bold text-slate-700">補助評価</th><td class="px-4 py-3 text-slate-600">外観、剥離、寿命</td></tr></tbody></table></div>`
    };

    const TAVER_CONCEPT_SCENES = {
        abrasive: {
            type: "taver",
            eyebrow: "WEAR BASICS",
            title: "硬い粒子が削り続ける形を読む",
            summary: "標準的なテーバー摩耗試験に最も近い見え方です。序盤から一定勾配で増えるかを先に見ます。",
            checks: ["勾配", "摩耗輪", "荷重"],
            visual: {
                variant: "abrasive",
                labels: ["2元アブレシブ", "連続除去", "勾配"],
                caption: "やすりがけのように、硬い相手材が連続的に表面を削る見え方です。"
            },
            beats: [
                { step: "01", title: "最初から増え方を見る", body: "序盤から一定勾配で増えるなら、アブレシブ寄りの説明がしやすいです。" },
                { step: "02", title: "摩耗輪を変える", body: "H-18 と H-22 の差は、傷の攻撃性の差として説明できます。" },
                { step: "03", title: "荷重で勾配が変わる", body: "荷重を上げるほど勾配は増えやすいですが、比例と言い切らないのが重要です。" }
            ]
        },
        adhesive: {
            type: "taver",
            eyebrow: "ADHESIVE",
            title: "途中から急増するかを切り分ける",
            summary: "凝着摩耗では、ずっと同じ速度で削れるとは限りません。接合点が育つと途中から悪化します。",
            checks: ["移着", "急増", "焼き付き"],
            visual: {
                variant: "adhesive",
                labels: ["微小接合", "移着", "急増"],
                caption: "接合点が育つと、一定速度ではなく途中から悪化する見え方になります。"
            },
            beats: [
                { step: "01", title: "序盤は小さく見える", body: "最初は目立たなくても、中盤以降に増え方が変わる場合があります。" },
                { step: "02", title: "高荷重で接合点が育つ", body: "高荷重ほど接合点が成長しやすく、急な立ち上がりにつながります。" },
                { step: "03", title: "標準テーバーと切り分ける", body: "標準条件だけで凝着摩耗単独を再現したと言い切らないことが重要です。" }
            ]
        },
        fatigue: {
            type: "taver",
            eyebrow: "FATIGUE",
            title: "潜伏期間の後に欠けが出る",
            summary: "疲労摩耗は、最初から大量に減るとは限りません。潜伏後の剥離をどう読むかが要点です。",
            checks: ["潜伏", "き裂", "剥離"],
            visual: {
                variant: "fatigue",
                labels: ["潜伏期間", "き裂進展", "剥離"],
                caption: "最初は静かでも、繰返し応力の蓄積で後半から欠け始める見え方です。"
            },
            beats: [
                { step: "01", title: "初期は静かでもよい", body: "変化が小さい期間があっても不自然ではありません。" },
                { step: "02", title: "中盤以降の変曲を探す", body: "き裂成長が見え始めると、曲線の立ち上がり方が変わります。" },
                { step: "03", title: "質量減少以外も見る", body: "ピッチングやフレーキングは、外観評価も一緒に出したほうが伝わります。" }
            ]
        },
        rubwear: {
            type: "taver",
            eyebrow: "PRINCIPLE",
            title: "offset が rub-wear を生む",
            summary: "テーバーの本質は、中心一致の純転がりではなく、オフセット配置が作る転がり + すべりです。",
            checks: ["offset", "交差円弧", "全方向"],
            visual: {
                variant: "topview",
                labels: ["offset", "rub-wear", "交差円弧"],
                caption: "試料中心と摩耗輪中心をずらした配置で、Taber 特有の rub-wear action が生まれます。"
            },
            beats: [
                { step: "01", title: "同心ではない", body: "摩耗輪は試料中心にぴったり合っていません。" },
                { step: "02", title: "すべり成分が入る", body: "その配置で rub-wear action が生まれます。" },
                { step: "03", title: "摩耗痕の形で説明する", body: "交差円弧状の摩耗痕を見せると伝わりやすいです。" }
            ]
        },
        wearindex: {
            type: "taver",
            eyebrow: "RESULT",
            title: "数値の意味を混ぜない",
            summary: "質量減少、wear index、寿命、剥離面積は似た話に見えても役割が違います。",
            checks: ["比較指標", "寿命", "外観"],
            visual: {
                variant: "wearindex",
                labels: ["質量減少", "1000回換算", "寿命は別"],
                caption: "比較用の換算値と、実際の寿命・外観評価は別の軸として扱います。"
            },
            beats: [
                { step: "01", title: "質量減少は実測値", body: "まずは試験後にどれだけ減ったかを見る値です。" },
                { step: "02", title: "wear index は換算値", body: "1000回換算で条件比較しやすくした値です。" },
                { step: "03", title: "寿命とは分ける", body: "疲労や剥離では、外観や寿命を別に示す必要があります。" }
            ]
        }
    };

    const TAVER_VISUAL_MODELS = {
        coated: { label: "塗膜 / コーティング", note: "表面層の削れやすさと、摩耗輪の攻撃性の差が見えやすいモデルです。", abrasiveBias: 0.82, adhesiveBias: 0.7, fatigueBias: 0.9 },
        polymer: { label: "一般樹脂", note: "標準条件との差が出やすく、摩耗輪と荷重の影響を説明しやすいモデルです。", abrasiveBias: 1.05, adhesiveBias: 0.92, fatigueBias: 1.0 },
        metal: { label: "金属摺動部材", note: "凝着や疲労寄りの注意点も説明しやすいモデルです。", abrasiveBias: 0.76, adhesiveBias: 1.18, fatigueBias: 1.12 }
    };

    const TAVER_VISUAL_LEARNING = {
        title: "条件を動かして、摩耗の立ち上がり方を比べる",
        description: "taver.html の simulation を学習アプリ側へ寄せた topic です。摩耗メカニズム、摩耗輪、荷重を変えたときに、どこが変わるかを同じ軸で見比べます。",
        buildScenario: buildTaverScenario,
        materialLabel: "試料モデル",
        controls: [
            { field: "wearMode", label: "支配的な摩耗メカニズム", type: "select", options: [{ value: "abrasive", label: "アブレシブ摩耗" }, { value: "adhesive", label: "凝着摩耗" }, { value: "fatigue", label: "疲労摩耗" }], formatValue(value) { return value === "adhesive" ? "凝着摩耗" : value === "fatigue" ? "疲労摩耗" : "アブレシブ摩耗"; } },
            { field: "wheelType", label: "摩耗輪", type: "select", options: [{ value: "cs10", label: "CS-10" }, { value: "h18", label: "H-18" }, { value: "h22", label: "H-22" }], formatValue(value) { return value === "cs10" ? "CS-10" : value === "h22" ? "H-22" : "H-18"; } },
            { field: "load", label: "荷重", type: "select", options: [{ value: 250, label: "250 g" }, { value: 500, label: "500 g" }, { value: 1000, label: "1000 g" }], formatValue(value) { return `${value} g`; } }
        ],
        chartCaption: "実測の完全再現ではなく、条件変更で損傷の立ち上がり方がどう変わるかを見るための概念シミュレーションです。",
        xAxisRange: { min: 0, max: 1000 },
        axisLabels: { x: "回転数 (cycles)", y: "摩耗量 index (mg)" }
    };

    const TAVER_DIAGNOSIS_QUESTIONS = { q1: { id: "q1", prompt: "標準的なテーバー摩耗試験は、主にどの摩耗説明に向いていますか。", whyEasy: "摩耗には複数の種類があるため、試験機ひとつで全部を同じように再現できると思いやすいからです。", options: [{ id: "q1-a", label: "アブレシブ摩耗の説明に最も向いている", explanation: "その通りです。標準的なテーバー試験は 2 元アブレシブ摩耗 + すべり寄りの説明に最も向いています。", correct: true, misconception: false, weakness: [], next: "q2" }, { id: "q1-b", label: "凝着摩耗や疲労摩耗も、標準条件ならそのまま単独で再現できる", explanation: "そこが誤解です。凝着や疲労を説明するときは、何が近くて何が違うかを必ず補足する必要があります。", correct: false, misconception: true, weakness: ["mechanism"], next: "q2" }] }, q2: { id: "q2", prompt: "テーバーで摩耗痕が交差円弧状になる説明として、最も適切なのはどれですか。", whyEasy: "2つの摩耗輪があると見た目だけで X 字と覚えがちで、配置理由まで意識しにくいためです。", options: [{ id: "q2-a", label: "摩耗輪が試料中心と同心で純転がりしているから", explanation: "違います。純転がりではなく、規格のオフセット配置によって転がり + すべりが入り、交差円弧状の摩耗痕になります。", correct: false, misconception: true, weakness: ["offset"], next: "q3" }, { id: "q2-b", label: "摩耗輪がオフセット配置され、rub-wear action が生まれるから", explanation: "その通りです。テーバーの説明ではこの offset と rub-wear action が核になります。", correct: true, misconception: false, weakness: [], next: "q3" }] }, q3: { id: "q3", prompt: "荷重を 2 倍にすると、摩耗量も必ずきれいに 2 倍になると言ってよいですか。", whyEasy: "荷重を上げるほど悪化するのは事実なので、比例まで言いたくなりやすいからです。", options: [{ id: "q3-a", label: "よい。常にほぼ比例で増える", explanation: "そこは言い過ぎです。アブレシブでは比例に近く見える場面がありますが、凝着や疲労では立ち上がり方が変わることがあります。", correct: false, misconception: true, weakness: ["load"], next: "q4" }, { id: "q3-b", label: "増えやすいが、摩耗メカニズムによって立ち上がり方は変わる", explanation: "その通りです。荷重は重要ですが、単純比例と言い切らず、どのメカニズム寄りかと一緒に説明します。", correct: true, misconception: false, weakness: [], next: "q4" }] }, q4: { id: "q4", prompt: "wear index について最も適切な説明はどれですか。", whyEasy: "質量減少と似た話に見えるため、実使用寿命まで同じ意味で扱ってしまいやすいためです。", options: [{ id: "q4-a", label: "1000回換算の比較指標で、寿命や外観評価とは分けて使う", explanation: "その通りです。wear index は比較用の換算指標であり、寿命や剥離面積と同じ意味ではありません。", correct: true, misconception: false, weakness: [], next: "q5" }, { id: "q4-b", label: "wear index が分かれば実使用寿命までそのまま言える", explanation: "そこが誤解です。疲労や剥離では、寿命や外観評価を別に示す必要があります。", correct: false, misconception: true, weakness: ["result"], next: "q5" }] }, q5: { id: "q5", prompt: "結果の再現性を守るために、摩耗輪について最優先で確認すべきことは何ですか。", whyEasy: "試料や荷重に目が向きやすく、摩耗輪の状態管理が後回しになりやすいからです。", options: [{ id: "q5-a", label: "リフェイシングや目詰まり確認が適切に行われているか", explanation: "その通りです。摩耗輪の状態は結果に強く効くため、目詰まりや目立てを必ず管理します。", correct: true, misconception: false, weakness: [], next: null }, { id: "q5-b", label: "摩耗輪は同じ型番なら、状態を見なくても結果はほぼ同じ", explanation: "違います。摩耗輪の状態管理を外すと、同じ型番でも結果がぶれやすくなります。", correct: false, misconception: true, weakness: ["maintenance"], next: null }] } };

    const TAVER_DIAGNOSIS_UI = { noMistakesText: "大きな誤解はまだ出ていません。次は図解で、摩耗メカニズムごとの立ち上がり方を比べると理解が安定します。", noRevisitTagText: "まだ戻るべき設問はありません", nextActions: [{ section: "visual", label: "図解で立ち上がり方を比較する" }, { section: "concepts", label: "摩耗メカニズムの違いを整理する" }, { section: "mastery", label: "理解確認で仕上げる" }] };
    const TAVER_AI_SUGGESTED_PATHS = ["H-18 と H-22 をどう説明し分けるか整理したいです。", "標準テーバーが凝着摩耗や疲労摩耗の単独再現ではない理由を説明したいです。", "wear index と実使用寿命を混同しない説明の仕方を考えたいです。", "塗膜試料でプレテストするときの荷重選定の考え方を整理したいです。"];
    const TAVER_LOCAL_AI_TOPICS = [{ keywords: ["摩耗輪", "H-18", "H-22", "CS-10"], answer: ["摩耗輪の違いは、まず攻撃性の差として説明すると伝わりやすいです。", "CS-10 は比較的マイルド、H-18 は標準、H-22 はより攻撃的という順で、序盤の勾配がどう変わるかを図と一緒に見せると理解されやすくなります。", "ただし、荷重や試料側の脆さでも見え方は変わるので、型番だけで絶対評価にしないのが重要です。"] }, { keywords: ["凝着", "焼き付き", "疲労"], answer: ["標準的なテーバー摩耗試験は、アブレシブ摩耗の説明に最も向いています。", "凝着摩耗は接合点が育って途中から急増する、疲労摩耗は潜伏期間の後に欠けが出る、という違いを先に出すと整理しやすいです。", "テーバーで似た見え方が出ても、単独再現と言い切らず、近い点と違う点を分けて説明してください。"] }, { keywords: ["wear index", "寿命", "質量減少"], answer: ["wear index は 1000 回換算の比較指標で、質量減少を条件比較しやすくした値です。", "実使用寿命や剥離面積とは役割が違うので、疲労や剥離の話をするときは別の評価軸も一緒に出すのが安全です。", "結果説明では、まず実測値、次に換算比較値、その次に外観や寿命評価という順に並べると混線しにくくなります。"] }];
    const TAVER_EXPLANATION_RUBRIC = [{ id: "mechanism", title: "摩耗メカニズムを分けて説明すること", keywords: ["アブレシブ", "凝着", "疲労", "違い"] }, { id: "offset", title: "offset と rub-wear action に触れること", keywords: ["offset", "オフセット", "rub-wear", "交差円弧"] }, { id: "condition", title: "摩耗輪と荷重が何を変えるかを言うこと", keywords: ["摩耗輪", "荷重", "H-18", "H-22", "勾配"] }, { id: "result", title: "wear index と結果解釈を混ぜないこと", keywords: ["wear index", "質量減少", "寿命", "剥離"] }];
    const TAVER_AI_UI = { textareaPlaceholder: "例: H-18 と H-22 を利用者にどう説明し分ければよいですか。塗膜試料で 500g を避けるべき場面はありますか。", mediaEmptyTitle: "参考リンクは topic 側に用意しています", mediaEmptyBody: "図解と診断で前提を固めたあとに、摩耗輪や荷重の相談へ進むと会話が噛み合いやすくなります。" };
    const TAVER_MASTERY_QUIZ = [{ id: "tm1", prompt: "標準的なテーバー摩耗試験が最も説明しやすい摩耗はどれですか。", choices: [{ id: "tm1a", label: "アブレシブ摩耗", correct: true, explanation: "その通りです。標準条件は 2 元アブレシブ摩耗寄りの説明に最も向いています。" }, { id: "tm1b", label: "凝着摩耗だけ", correct: false, explanation: "凝着は近い場面がありますが、標準条件だけで単独再現とは言えません。" }, { id: "tm1c", label: "疲労摩耗だけ", correct: false, explanation: "疲労摩耗は潜伏や剥離の評価も必要で、標準テーバーだけで言い切れません。" }] }, { id: "tm2", prompt: "テーバーで交差円弧状の摩耗痕が出る説明として適切なのはどれですか。", choices: [{ id: "tm2a", label: "摩耗輪がオフセット配置され、転がり + すべりが入るから", correct: true, explanation: "その通りです。これが rub-wear action の核です。" }, { id: "tm2b", label: "摩耗輪が試料中心と同心で純転がりしているから", correct: false, explanation: "純転がりではなく、オフセット配置が重要です。" }, { id: "tm2c", label: "荷重が大きいほど自動的に X 字になるから", correct: false, explanation: "形の理由は荷重より配置にあります。" }] }, { id: "tm3", prompt: "wear index の説明として最も適切なのはどれですか。", choices: [{ id: "tm3a", label: "1000回換算の比較指標で、寿命とは分けて使う", correct: true, explanation: "その通りです。比較指標と寿命評価は役割が違います。" }, { id: "tm3b", label: "wear index が高ければ、必ず実使用寿命も長い", correct: false, explanation: "寿命は外観や剥離も含めて別に評価する必要があります。" }, { id: "tm3c", label: "質量減少とまったく同じ意味の言い換えである", correct: false, explanation: "似ていますが、換算比較値としての役割があります。" }] }, { id: "tm4", prompt: "同じ摩耗輪型番でも結果がぶれやすくなる主因として、最も先に疑うべきものは何ですか。", choices: [{ id: "tm4a", label: "摩耗輪の目詰まりやリフェイシング不足", correct: true, explanation: "その通りです。摩耗輪の状態管理は最優先の確認項目です。" }, { id: "tm4b", label: "試料の色", correct: false, explanation: "色よりも摩耗輪状態の影響が大きいです。" }, { id: "tm4c", label: "1000回未満の回転数では差が出ないこと", correct: false, explanation: "差は回転数だけではなく摩耗輪状態でも強く出ます。" }] }];
    const TAVER_ROLE_TRACKS = [{ id: "beginner", label: "初心者", summary: "摩耗メカニズムと装置原理を先に固める導線です。", focusCompetencies: ["taver-mechanism", "taver-principle"] }, { id: "operator", label: "装置担当", summary: "摩耗輪、荷重、結果指標の説明を優先する導線です。", focusCompetencies: ["taver-setup", "taver-result"] }, { id: "analyst", label: "解析担当", summary: "条件比較と結果解釈の限界を説明する導線です。", focusCompetencies: ["taver-result", "taver-mechanism"] }];
    const TAVER_COMPETENCIES = [{ id: "taver-mechanism", title: "摩耗メカニズムの切り分け", summary: "アブレシブ・凝着・疲労を混ぜずに説明する力", roleIds: ["beginner", "analyst"], conceptIds: ["abrasive", "adhesive", "fatigue"], nextStep: { section: "concepts", conceptId: "abrasive", label: "摩耗メカニズムを整理する" }, sources: [{ type: "intro", id: "mechanism" }, { type: "diagnosis", id: "q1" }, { type: "diagnosis", id: "q3" }, { type: "mastery", id: "tm1" }] }, { id: "taver-principle", title: "装置原理の説明", summary: "offset と rub-wear action を軸に説明する力", roleIds: ["beginner", "operator"], conceptIds: ["rubwear"], nextStep: { section: "concepts", conceptId: "rubwear", label: "rub-wear の説明を固める" }, sources: [{ type: "intro", id: "offset" }, { type: "diagnosis", id: "q2" }, { type: "mastery", id: "tm2" }] }, { id: "taver-setup", title: "条件選定の説明", summary: "摩耗輪・荷重・試料モデルの違いを説明する力", roleIds: ["operator", "analyst"], conceptIds: ["abrasive", "rubwear"], nextStep: { missionId: "taver-wheel-compare", label: "摩耗輪比較ミッションへ" }, sources: [{ type: "mission", id: "taver-wheel-compare" }, { type: "diagnosis", id: "q3" }, { type: "mastery", id: "tm4" }] }, { id: "taver-result", title: "結果解釈の整理", summary: "wear index、質量減少、寿命評価を混ぜずに説明する力", roleIds: ["operator", "analyst"], conceptIds: ["wearindex", "fatigue"], nextStep: { missionId: "taver-result-compare", label: "結果比較ミッションへ" }, sources: [{ type: "intro", id: "result" }, { type: "diagnosis", id: "q4" }, { type: "mastery", id: "tm3" }, { type: "mission", id: "taver-result-compare" }] }];
    const TAVER_SIMULATION_MISSIONS = [{ id: "taver-wheel-compare", title: "摩耗輪の差を説明する", summary: "同じ試料・同じ荷重で、CS-10 / H-18 / H-22 の立ち上がり差を比べます。", competencyId: "taver-setup", conceptId: "abrasive", values: { material: "polymer", wearMode: "abrasive", wheelType: "h22", load: 500 }, checks: ["標準線との差をまず見る", "序盤の勾配差を摩耗輪の攻撃性として説明する", "試料側の脆さも効くので絶対化しない"], completionText: "摩耗輪型番を、単なる名前ではなく増加勾配の違いとして説明できれば完了です。" }, { id: "taver-load-compare", title: "荷重を上げたときの変化を比べる", summary: "500 g を基準に、250 g / 1000 g で立ち上がり方がどう変わるかを確認します。", competencyId: "taver-setup", conceptId: "adhesive", values: { material: "metal", wearMode: "adhesive", wheelType: "h18", load: 1000 }, checks: ["比例と言い切らず、途中からの急増を見る", "焼き付き寄りの注意を一言添える", "標準条件との差を同じ軸で話す"], completionText: "荷重を上げたときの説明が、単純比例ではなくメカニズム依存として話せれば完了です。" }, { id: "taver-result-compare", title: "結果指標を混ぜずに説明する", summary: "疲労寄りの条件で、質量減少だけでは足りない理由を確認します。", competencyId: "taver-result", conceptId: "wearindex", values: { material: "metal", wearMode: "fatigue", wheelType: "h18", load: 1000 }, checks: ["潜伏後の立ち上がりを見る", "wear index と寿命を分ける", "外観や剥離面積も補助評価に入れる"], completionText: "質量減少、wear index、寿命評価を別の言葉で整理できれば完了です。" }];
    const TAVER_REFERENCE_RESOURCES = [{ id: "tr1", title: "Thermo Fisher OES / XRF Trainings", url: "https://www.thermofisher.com/us/en/home/industrial/spectroscopy-elemental-isotope-analysis/oes-xrd-xrf-analysis/x-ray-fluorescence/services/oes-xrf-trainings.html", source: "Thermo Fisher", note: "利用者教育の流れを考えるときの参考リンク" }, { id: "tr2", title: "Taber abrasion test overview", url: "https://en.wikipedia.org/wiki/Taber_abrasion_test", source: "Wikipedia", note: "原理や用語の確認用。正式説明では社内基準や規格と併用する" }];
    const TAVER_PRINCIPLE = {
        eyebrow: "MEASUREMENT PRINCIPLE",
        title: "offset 配置で rub-wear action をつくる",
        description:
            "テーバー摩耗試験の核は、2つの摩耗輪を試料中心と同心に置かず、規格の offset 配置で接触させることです。この配置で転がりとすべりが同時に入り、交差円弧状の摩耗痕と全方向の擦れを再現します。",
        scene: {
            type: "taver",
            visual: {
                variant: "topview",
                frameLabelLeft: "TOP VIEW",
                frameLabelRight: "RUB-WEAR",
                labels: ["offset", "交差円弧", "全方向比較"],
                caption: "摩耗輪中心をずらして配置することで、純転がりではない rub-wear action が成立します。"
            }
        },
        quickFacts: [
            { label: "配置", body: "2つの摩耗輪を平行に置き、試料中心から offset させる" },
            { label: "接触", body: "転がりだけでなく、すべり成分が入る" },
            { label: "痕跡", body: "円環帯の中に交差円弧状の摩耗痕が出る" },
            { label: "効用", body: "方向依存に寄りすぎない総合比較がしやすい" }
        ],
        steps: [
            { step: "01", title: "試料台が回転する", body: "ターンテーブル上の試料が回転し、2つの摩耗輪が一定荷重で接触します。" },
            { step: "02", title: "offset がすべりを生む", body: "摩耗輪中心を一致させないため、純転がりではなく rub-wear action が生まれます。" },
            { step: "03", title: "交差円弧として痕が残る", body: "片側は外周方向へ、もう片側は中心方向へ擦るため、交差円弧状の摩耗痕になります。" }
        ],
        callout: {
            title: "なぜこの配置が重要か",
            body: "中心一致の純転がりモデルで説明すると、テーバー特有の rub-wear action が抜け落ちます。説明図も実機寄りの offset 配置で見せるほうが正確です。"
        },
        details: [
            { title: "利用者へ最初に伝えること", body: "標準テーバーは主に 2 元アブレシブ摩耗 + すべり寄りの比較に向く、と先に置くと誤解が減ります。" },
            { title: "見た目は X 字でも、説明は交差円弧", body: "見た目の印象より、円環帯の中で交差する円弧として説明したほうが技術的に正確です。" }
        ]
    };
    const TAVER_TOPIC = {
        id: "taver",
        name: "テーバー摩耗",
        pageTitle: "テーバー摩耗試験 適応型学習アプリ",
        storageKeySuffix: "taver",
        hero: TAVER_HERO,
        principle: TAVER_PRINCIPLE,
        introCards: TAVER_INTRO_CARDS,
        introSummaryStates: TAVER_INTRO_SUMMARY_STATES,
        selfCheck: TAVER_SELF_CHECK,
        figureCards: TAVER_FIGURE_CARDS,
        concepts: TAVER_CONCEPTS,
        conceptSupplements: TAVER_CONCEPT_SUPPLEMENTS,
        conceptScenes: TAVER_CONCEPT_SCENES,
        visualModels: TAVER_VISUAL_MODELS,
        visualLearning: TAVER_VISUAL_LEARNING,
        diagnosisQuestions: TAVER_DIAGNOSIS_QUESTIONS,
        diagnosisUi: TAVER_DIAGNOSIS_UI,
        defaults: {
            currentSection: "intro",
            roleId: "beginner",
            conceptLevel: "basic",
            activeConceptId: "abrasive",
            diagnosisStartQuestionId: "q1",
            visual: { material: "polymer", wearMode: "abrasive", wheelType: "h18", load: 500 },
            ai: {
                initialMessage:
                    "ここではテーバー摩耗試験の説明を支援します。摩耗メカニズム、摩耗輪、荷重、wear index のどれを整理したいかを 1 つ選んでください。"
            },
            settings: { apiProvider: "gemini", apiModel: "gemini-2.0-flash" }
        },
        ai: {
            systemInstruction:
                "あなたはテーバー摩耗試験の学習アプリの AI コーチです。標準的なテーバー試験が主にアブレシブ摩耗の説明に向くこと、offset による rub-wear action、摩耗輪と荷重で立ち上がり方が変わること、wear index と寿命評価を混同しないことを重視して日本語で答えてください。",
            suggestedPaths: TAVER_AI_SUGGESTED_PATHS,
            localTopics: TAVER_LOCAL_AI_TOPICS,
            explanationRubric: TAVER_EXPLANATION_RUBRIC,
            ui: TAVER_AI_UI
        },
        roles: TAVER_ROLE_TRACKS,
        competencies: TAVER_COMPETENCIES,
        simulationMissions: TAVER_SIMULATION_MISSIONS,
        masteryQuiz: TAVER_MASTERY_QUIZ,
        media: {
            title: "参考リンク",
            description: "必要な人だけ外部資料へ進める構成です。まずはこのアプリ内の図解と診断を優先します。",
            featuredVideo: null,
            resources: TAVER_REFERENCE_RESOURCES
        }
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

    const XRF_PRINCIPLE = {
        eyebrow: "MEASUREMENT PRINCIPLE",
        title: "一次 X 線で励起し、戻ってきた蛍光 X 線を読む",
        description:
            "XRF は試料へ一次 X 線を当て、内殻電子の空孔を埋めるときに出る蛍光 X 線を検出して元素を推定します。原理の中心は、照射、励起、検出、そしてマトリクス影響の切り分けです。",
        scene: {
            type: "xrf",
            visual: {
                frameLabelLeft: "SOURCE",
                frameLabelRight: "DETECTOR",
                sourceLabel: "X-RAY",
                detectorLabel: "SDD",
                showMatrixLayers: true,
                showPeaks: true,
                showScan: true,
                labels: ["励起", "蛍光", "スペクトル"],
                caption: "一次 X 線で励起し、戻ってきた蛍光 X 線を検出してスペクトルから元素候補を読む構造です。"
            }
        },
        quickFacts: [
            { label: "入力", body: "一次 X 線を照射する" },
            { label: "応答", body: "元素ごとの蛍光 X 線が出る" },
            { label: "出力", body: "スペクトル上のピーク位置と強度で読む" },
            { label: "注意", body: "軽元素・表面層・マトリクス影響で見え方が変わる" }
        ],
        steps: [
            { step: "01", title: "一次 X 線を当てる", body: "X 線源からの照射で内殻電子がはじき出され、励起状態が生まれます。" },
            { step: "02", title: "蛍光 X 線が戻る", body: "空孔を埋める遷移で、元素固有エネルギーの蛍光 X 線が出ます。" },
            { step: "03", title: "スペクトルで読む", body: "ピーク位置だけでなく、雰囲気、被覆、取得時間で見え方がどう変わるかを切り分けます。" }
        ],
        callout: {
            title: "見えない = 存在しない、ではない",
            body: "空気中では軽元素側が落ちやすく、表面被覆やマトリクスでもピークは変形します。見え方の条件依存を先に押さえることが重要です。"
        },
        details: [
            { title: "スクリーニングと定量は別", body: "元素の有無をざっくり見る用途と、厳密な定量は同じ説明では足りません。" },
            { title: "安全は原理と別枠で必要", body: "放射線管理やインターロックは、測定原理と同じくらい説明が必要です。" }
        ]
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

    const XRF_TOPIC = {
        id: "xrf",
        name: "蛍光X線分析装置",
        pageTitle: "蛍光X線分析装置 適応型学習アプリ",
        storageKeySuffix: "xrf",
        hero: XRF_HERO,
        principle: XRF_PRINCIPLE,
        introCards: XRF_INTRO_CARDS,
        introSummaryStates: XRF_INTRO_SUMMARY_STATES,
        selfCheck: XRF_SELF_CHECK,
        figureCards: XRF_FIGURE_CARDS,
        concepts: XRF_CONCEPTS,
        conceptSupplements: XRF_CONCEPT_SUPPLEMENTS,
        conceptScenes: XRF_CONCEPT_SCENES,
        visualModels: XRF_VISUAL_MODELS,
        visualLearning: XRF_VISUAL_LEARNING,
        diagnosisQuestions: XRF_DIAGNOSIS_QUESTIONS,
        diagnosisUi: XRF_DIAGNOSIS_UI,
        defaults: {
            currentSection: "intro",
            roleId: "beginner",
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
        roles: XRF_ROLE_TRACKS,
        competencies: XRF_COMPETENCIES,
        simulationMissions: XRF_SIMULATION_MISSIONS,
        masteryQuiz: XRF_MASTERY_QUIZ,
        media: {
            title: "参考リソース",
            description:
                "動画は必須にせず、差し替え可能な任意アセットとして扱います。まずは図解と診断で基礎を固め、必要なら装置デモや社内操作動画をあとから足す構成です。",
            featuredVideo: null,
            resources: XRF_REFERENCE_RESOURCES
        }
    };

    const TOPICS = {
        nanoin: NANOINDENTER_TOPIC,
        xrf: XRF_TOPIC,
        taver: TAVER_TOPIC
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
