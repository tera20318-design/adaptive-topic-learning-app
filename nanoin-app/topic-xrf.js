(function () {
    window.NanoLearnTopicModules = window.NanoLearnTopicModules || {};

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
            peakMarkers: model.peaks
                .slice()
                .sort((a, b) => a.energy - b.energy)
                .map((peak) => ({
                    label: peak.label,
                    energy: peak.energy
                })),
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

    window.NanoLearnTopicModules.xrf = {
        topic: XRF_TOPIC
    };
})();
