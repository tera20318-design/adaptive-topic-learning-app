(function () {
    window.NanoLearnTopicModules = window.NanoLearnTopicModules || {};

    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    function gaussian(x, center, width, height) {
        return height * Math.exp(-Math.pow(x - center, 2) / (2 * Math.pow(width, 2)));
    }

    function buildAxis(min, max, step) {
        const points = [];
        for (let value = min; value <= max + 1e-9; value += step) {
            points.push(Number(value.toFixed(0)));
        }
        return points;
    }

    function buildIrScenario(stateVisual, visualModels) {
        const model = visualModels[stateVisual.material] || visualModels.polymer;
        const measurementMode = stateVisual.measurementMode || "atr";
        const pathLength = Number(stateVisual.pathLength || 35);
        const resolution = Number(stateVisual.resolution || 4);
        const moisture = Number(stateVisual.moisture || 8);
        const axis = buildAxis(400, 4000, 4);
        const modeGain = measurementMode === "transmission" ? 1.08 : measurementMode === "reflection" ? 0.78 : 0.92;
        const pathFactor = measurementMode === "transmission"
            ? clamp(pathLength / 45, 0.45, 2.6)
            : measurementMode === "atr"
                ? clamp(0.7 + pathLength / 140, 0.72, 1.55)
                : clamp(0.55 + pathLength / 220, 0.55, 1.2);
        const resolutionFactor = 1 + (resolution - 2) / 12 * 1.45;
        const moistureFactor = clamp(moisture / 35, 0, 1.25);
        const baselineLift = 0.018 + moistureFactor * 0.05;
        const broadeningPenalty = clamp(1 - (resolution - 2) / 20, 0.45, 1);

        const data = axis.map((wavenumber) => {
            const fingerprintBias = wavenumber < 1500 ? 1.08 : 1;
            const modeBias = measurementMode === "atr"
                ? (wavenumber < 1500 ? 1.1 : 0.9)
                : measurementMode === "reflection"
                    ? (wavenumber < 1800 ? 0.82 : 0.9)
                    : 1;
            const signal = model.peaks.reduce((sum, peak) => (
                sum + gaussian(
                    wavenumber,
                    peak.position,
                    peak.width * resolutionFactor,
                    peak.height * modeGain * pathFactor * fingerprintBias * modeBias
                )
            ), 0);
            const waterSignal =
                gaussian(wavenumber, 3400, 150 * (1 + moistureFactor * 0.2), 0.18 * moistureFactor) +
                gaussian(wavenumber, 1640, 70 * (1 + moistureFactor * 0.15), 0.1 * moistureFactor);
            const ripple = measurementMode === "reflection"
                ? 0.018 * Math.sin(wavenumber / 115)
                : 0.008 * Math.sin(wavenumber / 150);
            return {
                x: Number(wavenumber.toFixed(0)),
                y: Number(clamp(baselineLift + signal + waterSignal + ripple, 0, 1.58).toFixed(3))
            };
        });

        const dominantPeak = model.peaks.slice().sort((a, b) => b.height - a.height)[0];
        const fingerprintContrast = broadeningPenalty >= 0.82 ? "高" : broadeningPenalty >= 0.62 ? "中" : "低";
        const moistureRisk = moisture >= 26 ? "高" : moisture >= 12 ? "中" : "低";

        return {
            model,
            measurementMode,
            pathLength,
            resolution,
            moisture,
            fingerprintContrast,
            moistureRisk,
            peakMarkerUnit: "cm^-1",
            peakMarkers: model.peaks.slice(0, 5).map((peak) => ({ label: peak.label, position: peak.position })),
            metrics: [
                { id: "dominantBand", label: "主な吸収帯", value: dominantPeak ? dominantPeak.label : "未設定" },
                { id: "fingerprintContrast", label: "指紋領域の見分けやすさ", value: fingerprintContrast, tone: fingerprintContrast },
                { id: "moistureRisk", label: "水分干渉", value: moistureRisk, tone: moistureRisk },
                { id: "mode", label: "測定モード", value: measurementMode === "atr" ? "ATR" : measurementMode === "transmission" ? "透過" : "反射" }
            ],
            insights: [
                { title: "横軸は固定して読む", body: "IR は波数位置が手がかりなので、設定を変えても横軸固定で比較します。" },
                { title: "分解能は指紋領域に先に効く", body: resolution >= 10 ? "今は指紋領域の差がつぶれやすい条件です。" : "今は指紋領域の差をまだ追いやすい条件です。" },
                { title: "水分帯を先に疑う", body: moisture >= 20 ? "3400 と 1640 cm^-1 付近は水分干渉を疑う状態です。" : "水分干渉は弱めで、試料本来のピークを読みやすい状態です。" }
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
                        borderWidth: 2.5,
                        pointRadius: 0,
                        tension: 0.12
                    }
                ],
                tooltipLabel(raw) {
                    return `波数 ${raw.x} cm^-1, 吸光度 ${raw.y.toFixed(3)}`;
                }
            }
        };
    }

    const conceptScenes = {
        ftir: { type: "ir", eyebrow: "FOURIER TRANSFORM", title: "干渉信号を波数スペクトルへ戻す", summary: "FT-IR は干渉計でまとめて取り、変換して読む。", checks: ["干渉計", "変換", "波数"], visual: { variant: "interferometer", labels: ["光源", "移動鏡", "検出器"], caption: "FT-IR は干渉信号から波数スペクトルへ戻して読む。" }, beats: [{ step: "01", title: "光を分ける", body: "ビームスプリッタで 2 本の光路へ分ける。" }, { step: "02", title: "干渉信号を取る", body: "光路差を変えながら干渉信号を得る。" }, { step: "03", title: "変換して読む", body: "フーリエ変換で波数ごとの吸収に戻す。" }] },
        absorbance: { type: "ir", eyebrow: "AXIS READING", title: "横軸を固定して位置で読む", summary: "高さより先に波数位置を見るのが IR の入口。", checks: ["波数", "吸光度", "比較"], visual: { variant: "absorbance", labels: ["波数軸", "吸光度", "比較"], caption: "横軸固定で、どこにピークがあるかを基準に読む。" }, beats: [{ step: "01", title: "位置を先に見る", body: "どの帯域に吸収があるかで候補を絞る。" }, { step: "02", title: "高さだけで決めない", body: "高さは厚みやモードでも変わる。" }, { step: "03", title: "軸固定で比べる", body: "横軸が動くと比較の意味が崩れる。" }] },
        regions: { type: "ir", eyebrow: "READING FLOW", title: "特性吸収帯で絞り、指紋領域で見分ける", summary: "高波数側は候補を絞る場、低波数側は決めに行く場。", checks: ["4000–1500", "1500–400", "官能基"], visual: { variant: "fingerprint", labels: ["特性吸収帯", "指紋領域", "帰属"], caption: "高波数側で絞り、低波数側で見分ける。" }, beats: [{ step: "01", title: "目立つ帯域で絞る", body: "O-H や C=O のような強い帯域から始める。" }, { step: "02", title: "組み合わせで見る", body: "単独ピークではなく帯域の組み合わせで考える。" }, { step: "03", title: "指紋領域で確かめる", body: "最後は低波数側の細かな違いを見る。" }] },
        sampling: { type: "ir", eyebrow: "SAMPLING MODE", title: "ATR・透過・反射で見え方が変わる", summary: "モード差は、どこをどの深さで見ているかの違い。", checks: ["ATR", "透過", "反射"], visual: { variant: "sampling", labels: ["ATR", "透過", "反射"], caption: "同じ試料でもモード差で相対強度が変わる。" }, beats: [{ step: "01", title: "当たり方が違う", body: "透過は通し、ATR は接触面、反射は表面寄りを読む。" }, { step: "02", title: "相対強度が変わる", body: "同じ官能基でも高さ比較は単純ではない。" }, { step: "03", title: "目的で選ぶ", body: "試料形状と欲しい情報でモードを決める。" }] },
        processing: { type: "ir", eyebrow: "PROCESSING", title: "分解能と干渉を切り分ける", summary: "ピークの広がり、水分帯、ベースラインを混同しない。", checks: ["分解能", "水分", "補正"], visual: { variant: "processing", labels: ["分解能", "水分帯", "補正"], caption: "試料本来の吸収と測定条件由来の変化を分けて読む。" }, beats: [{ step: "01", title: "分解能で幅が変わる", body: "粗い条件では細かな差がつぶれる。" }, { step: "02", title: "水分帯を疑う", body: "3400 と 1640 cm^-1 は測定系由来の可能性がある。" }, { step: "03", title: "補正前提を意識する", body: "差スペクトルや検索は前処理が揃ってこそ安定する。" }] }
    };

    const visualModels = {
        polymer: { label: "ポリエチレン系", note: "C-H 系の基本ピークを読みやすい基礎練習向けモデルです。", peaks: [{ label: "C-H stretch", position: 2916, width: 36, height: 0.34 }, { label: "C-H stretch", position: 2848, width: 34, height: 0.28 }, { label: "CH2 bend", position: 1465, width: 26, height: 0.24 }, { label: "CH2 rock", position: 720, width: 18, height: 0.2 }] },
        alcohol: { label: "アルコール系", note: "広い O-H と C-O が特徴で、水分干渉との見分け練習に向きます。", peaks: [{ label: "O-H", position: 3340, width: 170, height: 0.36 }, { label: "C-H stretch", position: 2970, width: 40, height: 0.16 }, { label: "CH bend", position: 1450, width: 28, height: 0.14 }, { label: "C-O", position: 1050, width: 34, height: 0.32 }] },
        ketone: { label: "ケトン系", note: "強い C=O で素早く候補を絞る練習に向くモデルです。", peaks: [{ label: "C=O", position: 1715, width: 28, height: 0.44 }, { label: "C-H stretch", position: 2960, width: 34, height: 0.16 }, { label: "CH3 bend", position: 1360, width: 26, height: 0.18 }, { label: "C-C / C-O", position: 1220, width: 24, height: 0.12 }] },
        aromatic: { label: "芳香族系", note: "芳香環のピークがあり、指紋領域の使い方を練習しやすいモデルです。", peaks: [{ label: "Ar C-H", position: 3025, width: 26, height: 0.16 }, { label: "C=C", position: 1600, width: 24, height: 0.26 }, { label: "Ring mode", position: 1493, width: 22, height: 0.18 }, { label: "oop bend", position: 758, width: 18, height: 0.2 }, { label: "oop bend", position: 698, width: 16, height: 0.16 }] }
    };

    const topic = {
        id: "ir",
        name: "IR赤外分光",
        pageTitle: "IR赤外分光 適応型学習アプリ",
        storageKeySuffix: "ir",
        hero: {
            eyebrow: "ADAPTIVE LEARNING",
            titleLead: "IR 赤外分光を",
            titleAccent: "波数とピークの因果",
            titleTrail: "で読めるようにする",
            subtitle: "FT-IR を中心に、原理・読解・条件設計をつなぐ学習アプリ",
            description: "IR は横軸の波数位置、縦軸の透過率 / 吸光度、そして測定モードや前処理によって見え方が変わります。ATR、透過、反射の違いと、特性吸収帯・指紋領域・ベースライン処理を一つの流れで理解します。"
        },
        principle: {
            eyebrow: "MEASUREMENT PRINCIPLE",
            title: "FT-IR は干渉信号を取り、波数スペクトルへ戻して読む",
            description: "赤外分光では、試料がどの波数で吸収するかを見ることで結合や官能基の手がかりを得ます。FT-IR は干渉計でまとめて信号を取り、フーリエ変換で波数スペクトルへ戻す仕組みです。そのうえで、ATR・透過・反射や分解能、水分干渉が見え方を左右します。",
            scene: { type: "ir", visual: { variant: "interferometer", frameLabelLeft: "SOURCE", frameLabelRight: "READOUT", labels: ["干渉計", "変換", "スペクトル"], caption: "FT-IR は干渉信号から波数スペクトルへ戻して読む。" } },
            quickFacts: [{ label: "代表範囲", body: "中赤外では 4000–400 cm^-1 をまず使う。" }, { label: "表示", body: "縦軸は透過率か吸光度、横軸は波数。" }, { label: "読解", body: "特性吸収帯で絞り、指紋領域で見分ける。" }, { label: "条件差", body: "モード、分解能、背景で見え方が変わる。" }],
            steps: [{ step: "01", title: "干渉信号を取る", body: "光路差を変えながら時間領域の信号をまとめて取得する。" }, { step: "02", title: "波数スペクトルへ戻す", body: "フーリエ変換で波数ごとの吸収に変換する。" }, { step: "03", title: "帯域と条件で読む", body: "官能基、指紋領域、測定条件の差を合わせて解釈する。" }],
            callout: { title: "IR はピーク位置と測定条件の両方を読む装置", body: "高さだけを見て即断すると誤読しやすいです。位置、幅、組み合わせ、そして測定モードや水分干渉を一緒に見ることが大事です。" },
            details: [{ title: "横軸を固定する理由", body: "IR はどこに吸収が出るかが本質です。設定差を比較するときも、横軸は動かさずに見ます。" }, { title: "前処理の価値", body: "分解能、背景、水分干渉、ベースラインの影響を切り分けてこそ、官能基推定や検索が安定します。" }]
        },
        introCards: [{ id: "axis", title: "軸の読み方", body: "横軸は波数、縦軸は透過率または吸光度です。まずは 4000–400 cm^-1 の全体地図を持つことから始めます。" }, { id: "mode", title: "測定モード", body: "ATR、透過、反射では同じ試料でも見え方が変わります。モードを選ぶ理由を原理からつなげて理解します。" }, { id: "bands", title: "帯域の考え方", body: "特性吸収帯で候補を絞り、指紋領域で見分けるという読み方を演習で身につけます。" }],
        introSummaryStates: [{ id: "axis", label: "軸", summary: "波数位置を基準にして、どの帯域が何を意味するかを先に掴みます。" }, { id: "transform", label: "FT", summary: "干渉計からインターフェログラムを取り、変換してスペクトルへ戻す流れを押さえます。" }, { id: "readout", label: "読解", summary: "特性吸収帯で絞り、指紋領域と測定条件で確かめる流れに慣れます。" }],
        selfCheck: [{ id: "range", prompt: "中赤外でまず押さえる代表的な波数範囲を説明できますか。", options: [{ value: 0, label: "まだ曖昧" }, { value: 1, label: "4000–400 cm^-1 を見ている" }, { value: 2, label: "波数範囲と読解の意味まで説明できる" }] }, { id: "mode", prompt: "ATR / 透過 / 反射の違いを、見えるピークの差として話せますか。", options: [{ value: 0, label: "まだ難しい" }, { value: 1, label: "名前と用途は分かる" }, { value: 2, label: "条件差として説明できる" }] }, { id: "interpretation", prompt: "特性吸収帯と指紋領域を分けて読む流れを持っていますか。", options: [{ value: 0, label: "まだ自信がない" }, { value: 1, label: "ざっくりなら分かる" }, { value: 2, label: "ピーク位置から絞り込める" }] }],
        figureCards: [{ id: "ir-flow", label: "図 1", illustration: "<svg viewBox='0 0 260 120' class='w-full'><rect x='16' y='34' width='48' height='40' rx='10' fill='#0f172a'/><rect x='102' y='30' width='56' height='48' rx='16' fill='#0f766e'/><rect x='196' y='36' width='44' height='36' rx='10' fill='#1d4ed8'/><path d='M64 54 L102 54' stroke='#38bdf8' stroke-width='4' stroke-linecap='round'/><path d='M158 54 L196 54' stroke='#34d399' stroke-width='4' stroke-linecap='round'/><text x='12' y='24' font-size='11' fill='#0f172a'>光源</text><text x='92' y='22' font-size='11' fill='#0f172a'>干渉計</text><text x='184' y='24' font-size='11' fill='#0f172a'>検出器</text></svg>", bullets: [{ label: "取得", body: "干渉計で時間領域の信号を取る" }, { label: "変換", body: "フーリエ変換して波数軸へ戻す" }, { label: "読解", body: "ピーク位置と形から官能基を絞る" }] }, { id: "ir-regions", label: "図 2", illustration: "<svg viewBox='0 0 260 120' class='w-full'><rect x='18' y='34' width='112' height='46' rx='14' fill='#dbeafe'/><rect x='132' y='34' width='110' height='46' rx='14' fill='#dcfce7'/><text x='34' y='61' font-size='13' fill='#1d4ed8'>特性吸収帯</text><text x='157' y='61' font-size='13' fill='#166534'>指紋領域</text><text x='24' y='96' font-size='11' fill='#475569'>4000–1500 cm^-1</text><text x='150' y='96' font-size='11' fill='#475569'>1500–400 cm^-1</text></svg>", bullets: [{ label: "絞る", body: "まず高波数側の帯域で候補を絞る" }, { label: "確かめる", body: "低波数側の細かな形で見分ける" }, { label: "比較", body: "横軸固定で差を見る" }] }],
        concepts: [{ id: "ftir", title: "FT-IR と干渉計", short: "時間領域の干渉信号をフーリエ変換して、波数スペクトルへ戻す。", beginner: "FT-IR は最初から波数ごとの強さを直接並べて測るのではなく、干渉計でまとめて信号を取り、最後に変換してスペクトルに戻します。", advanced: "干渉計で得たインターフェログラムを変換することで、多波長を同時に扱いながら実用的な分解能と感度を両立します。", relations: [{ target: "absorbance", label: "変換後に吸光度や透過率として読む" }, { target: "sampling", label: "モード選択で見える情報が変わる" }, { target: "processing", label: "分解能や前処理の影響につながる" }] }, { id: "absorbance", title: "吸光度と波数軸", short: "横軸は波数、縦軸は透過率か吸光度。比較するときは軸を固定して読む。", beginner: "IR ではどこにピークがあるかが大事です。横軸がずれると比較の意味が崩れるので、位置を基準に読みます。", advanced: "吸光度は定量や差スペクトルに向き、透過率は直感的に読みやすい表示です。", relations: [{ target: "regions", label: "特性吸収帯と指紋領域の読み分けにつながる" }, { target: "processing", label: "ベースライン補正や差スペクトルの前提になる" }, { target: "sampling", label: "モード差で縦方向の見え方が変わる" }] }, { id: "regions", title: "特性吸収帯と指紋領域", short: "高波数側で候補を絞り、低波数側で見分ける。", beginner: "まずは O-H、C=O、C-H のような目立つ帯域で候補を絞ります。そのあとで 1500 cm^-1 以下の細かな形を見て区別します。", advanced: "官能基同定では、位置だけでなく幅・強度・組み合わせが重要です。", relations: [{ target: "absorbance", label: "波数軸の読み方を土台にして成立する" }, { target: "sampling", label: "測定モード差で相対強度が変わる" }, { target: "processing", label: "分解能が足りないと細かな差がつぶれる" }] }, { id: "sampling", title: "ATR・透過・反射", short: "同じ試料でも、どのモードで測るかでピークの見え方が変わる。", beginner: "ATR は表面寄り、透過は厚み依存を見やすく、反射は表面状態の影響を受けやすい。", advanced: "モード差は相対強度、ピーク形状、ベースラインに現れます。", relations: [{ target: "ftir", label: "取得系は同じでもサンプリングで情報が変わる" }, { target: "regions", label: "指紋領域のコントラストにも影響する" }, { target: "processing", label: "背景差し引きや補正の設計とつながる" }] }, { id: "processing", title: "ベースライン・分解能・水分干渉", short: "ピークを見る前に、何が測定条件由来の変化かを切り分ける。", beginner: "分解能が粗いとピークは広がり、水分が多いと 3400 と 1640 cm^-1 付近に余分な吸収が現れます。", advanced: "差スペクトルや検索は便利ですが、前処理の影響を理解しないと誤同定につながります。", relations: [{ target: "absorbance", label: "表示と前処理を切り分けて考える" }, { target: "sampling", label: "モード差と前処理差を混同しない" }, { target: "regions", label: "指紋領域の読みやすさを左右する" }] }],
        conceptScenes,
        visualModels,
        visualLearning: { title: "条件を変えて、IR スペクトルの見え方の差を読む", description: "測定モード、実効厚み、分解能、水分干渉を動かしながら、特性吸収帯と指紋領域の見え方がどう変わるかを比較します。", buildScenario: buildIrScenario, materialLabel: "試料モデル", controls: [{ field: "measurementMode", label: "測定モード", type: "select", options: [{ value: "atr", label: "ATR" }, { value: "transmission", label: "透過" }, { value: "reflection", label: "反射" }], formatValue(value) { return value === "atr" ? "ATR" : value === "transmission" ? "透過" : "反射"; } }, { field: "pathLength", label: "実効厚み", type: "slider", min: 10, max: 120, step: 5, formatValue(value) { return `${value} um`; } }, { field: "resolution", label: "分解能", type: "slider", min: 2, max: 16, step: 2, formatValue(value) { return `${value} cm^-1`; } }, { field: "moisture", label: "水分干渉", type: "slider", min: 0, max: 35, step: 1, formatValue(value) { return `${value}%`; } }], chartCaption: "波数軸は固定です。設定を変えたら、まずピーク位置は維持されたまま、幅・高さ・ベースラインがどう変わるかを見ます。", xAxisRange: { min: 400, max: 4000 }, yAxisRange: { min: 0, max: 1.6 }, axisLabels: { x: "波数 (cm^-1)", y: "吸光度" }, reverseXAxis: true },
        diagnosisQuestions: { q1: { id: "q1", prompt: "IR スペクトルを読み始めるとき、まず何を軸に見るのが自然ですか。", whyEasy: "高さだけでなく、波数位置を基準に読むことが IR の入口です。", options: [{ id: "q1-a", label: "横軸の波数位置を見て、どの帯域に吸収があるかを先に確認する", explanation: "正解です。まず位置で候補を絞り、そのあとに形や強さを見ます。", correct: true, misconception: false, weakness: [], next: "q2" }, { id: "q1-b", label: "一番深いピークだけを見て、官能基を即断する", explanation: "不十分です。高さは厚みやモードでも変わるので、位置と帯域の組み合わせで考える必要があります。", correct: false, misconception: true, weakness: ["absorbance"], next: "q2" }] }, q2: { id: "q2", prompt: "ATR と透過の違いとして、最も自然な説明はどれですか。", whyEasy: "モード差は単なる操作ではなく、どこをどのように見ているかの違いです。", options: [{ id: "q2-a", label: "同じ試料でも、表面寄りか厚み全体かで相対強度の見え方が変わる", explanation: "正解です。ATR と透過は情報の取り方が違うため、相対強度も変わります。", correct: true, misconception: false, weakness: [], next: "q3" }, { id: "q2-b", label: "モードを変えても、ピークの見え方は基本的に変わらない", explanation: "不正解です。モード差はピークの高さやベースラインの見え方に影響します。", correct: false, misconception: true, weakness: ["sampling"], next: "q3" }] }, q3: { id: "q3", prompt: "1500 cm^-1 以下の領域を特に重視する理由は何ですか。", whyEasy: "IR の定番の読み方は、特性吸収帯で絞って指紋領域で見分ける流れです。", options: [{ id: "q3-a", label: "化合物ごとの差が細かく出やすく、最終確認に向くから", explanation: "正解です。指紋領域は候補同士の見分けに価値があります。", correct: true, misconception: false, weakness: [], next: "q4" }, { id: "q3-b", label: "高波数側より常に定量性が高いから", explanation: "そうではありません。指紋領域は読みやすさが分解能や前処理に左右されます。", correct: false, misconception: true, weakness: ["regions"], next: "q4" }] }, q4: { id: "q4", prompt: "3400 cm^-1 付近の広い吸収と 1640 cm^-1 付近の吸収が強く出たとき、まず疑うべきなのは何ですか。", whyEasy: "水分干渉は IR で頻出の読み違いポイントです。", options: [{ id: "q4-a", label: "測定系の水分やバックグラウンドの影響", explanation: "正解です。試料本来の O-H と見分けるためにも、測定条件由来の寄与を先に疑います。", correct: true, misconception: false, weakness: [], next: null }, { id: "q4-b", label: "どんな試料でも必ずカルボン酸が入っている", explanation: "不正解です。広い O-H は水分や前処理由来でも現れるため、即断は危険です。", correct: false, misconception: true, weakness: ["processing"], next: null }] } },
        diagnosisUi: { noMistakesText: "大きな誤解は見えていません。次は visual で分解能と水分干渉の差を自分の目で確かめると定着しやすいです。", noRevisitTagText: "戻るべき論点は少なめです", nextActions: [{ section: "visual", label: "図解で条件差を見る" }, { section: "concepts", label: "概念地図で整理する" }, { section: "mastery", label: "理解確認へ進む" }] },
        roles: [{ id: "beginner", label: "初学者", summary: "軸、帯域、測定モードの違いを言葉で説明できる。" }, { id: "reader", label: "読解者", summary: "特性吸収帯と指紋領域を使って候補を絞れる。" }, { id: "operator", label: "条件設計者", summary: "モード、分解能、干渉の影響を見込んで条件を選べる。" }],
        competencies: [{ id: "ir-axis", title: "軸と帯域の読み方", summary: "波数軸、吸光度、特性吸収帯と指紋領域の役割をつなげて説明できる。", roleIds: ["beginner", "reader"], conceptIds: ["absorbance", "regions"], nextStep: { section: "concepts", conceptId: "regions", label: "概念地図で読む" }, sources: [{ type: "diagnosis", id: "q1" }] }, { id: "ir-mode", title: "測定モードの使い分け", summary: "ATR / 透過 / 反射の違いを、見える情報の差として説明できる。", roleIds: ["beginner", "operator"], conceptIds: ["sampling"], nextStep: { section: "visual", label: "図解でモード差を見る" }, sources: [{ type: "diagnosis", id: "q2" }] }, { id: "ir-processing", title: "分解能と干渉の切り分け", summary: "分解能低下、水分干渉、ベースライン変動を、試料本来の変化と分けて読める。", roleIds: ["reader", "operator"], conceptIds: ["processing"], nextStep: { section: "visual", label: "図解で分解能差を見る" }, sources: [{ type: "diagnosis", id: "q4" }] }],
        simulationMissions: [{ id: "ir-mode-compare", title: "ATR と透過の見え方を比べる", summary: "同じ試料で測定モードだけを変え、相対強度の違いを読む。", competencyId: "ir-mode", conceptId: "sampling", values: { material: "alcohol", measurementMode: "atr", pathLength: 35, resolution: 4, moisture: 8 }, checks: ["O-H と C-O の見え方の差", "表面寄りの情報の読みやすさ", "高さだけで即断しない"], completionText: "測定モード差を、試料そのものの違いと混同せずに読めれば十分です。" }, { id: "ir-fingerprint", title: "分解能を変えて指紋領域の差を読む", summary: "分解能を粗くしたとき、どの帯域から差がつぶれるかを確認する。", competencyId: "ir-processing", conceptId: "processing", values: { material: "aromatic", measurementMode: "transmission", pathLength: 50, resolution: 12, moisture: 6 }, checks: ["1500 cm^-1 以下の差", "ピーク幅の広がり", "横軸固定で比較する"], completionText: "分解能が落ちると細かな違いが先につぶれる、という感覚を持てれば前進です。" }, { id: "ir-moisture", title: "水分干渉を見分ける", summary: "3400 と 1640 cm^-1 付近に出る干渉を、試料本来の O-H と切り分ける。", competencyId: "ir-processing", conceptId: "processing", values: { material: "ketone", measurementMode: "atr", pathLength: 25, resolution: 4, moisture: 28 }, checks: ["3400 と 1640 cm^-1 の挙動", "水分干渉と本来ピークの切り分け", "前処理を疑う視点"], completionText: "広い O-H を見たら即断せず、水分や背景由来の可能性を先に疑う姿勢が大事です。" }],
        masteryQuiz: [{ id: "ir1", prompt: "IR スペクトルで最初に波数位置を見る理由として最も適切なのはどれですか。", choices: [{ id: "ir1-a", label: "ピーク位置が官能基推定の主要な手がかりになるから", correct: true, explanation: "正解です。高さだけではなく、どの帯域に吸収があるかが入口になります。" }, { id: "ir1-b", label: "高さだけで化合物を一意に決められるから", correct: false, explanation: "高さは厚みやモードでも変わるので、それだけでは不十分です。" }] }, { id: "ir2", prompt: "指紋領域の説明として正しいのはどれですか。", choices: [{ id: "ir2-a", label: "候補同士の最終的な見分けに向く低波数側の領域", correct: true, explanation: "正解です。特性吸収帯で絞った候補を、指紋領域で見分けます。" }, { id: "ir2-b", label: "どんな条件でも高波数側より読みやすい領域", correct: false, explanation: "そうではありません。分解能や前処理の影響を受けやすいです。" }] }, { id: "ir3", prompt: "分解能を粗くしたときに起こりやすい変化はどれですか。", choices: [{ id: "ir3-a", label: "近いピーク同士がまとまり、指紋領域の差が見えにくくなる", correct: true, explanation: "正解です。細かな差は先に失われます。" }, { id: "ir3-b", label: "横軸の波数位置が大きく移動して別の帯域になる", correct: false, explanation: "通常は位置が大きく動くのではなく、幅や見え方が変わります。" }] }],
        defaults: { currentSection: "intro", roleId: "beginner", conceptLevel: "basic", activeConceptId: "ftir", diagnosisStartQuestionId: "q1", visual: { material: "polymer", measurementMode: "atr", pathLength: 35, resolution: 4, moisture: 8 }, ai: { initialMessage: "ここでは IR 赤外分光の基礎から読解まで扱います。軸の読み方、ATR と透過の違い、指紋領域の使い方などを一緒に整理できます。" }, settings: { apiProvider: "gemini", apiModel: "gemini-2.0-flash" } },
        ai: { systemInstruction: "あなたは IR 赤外分光の学習支援 AI です。FT-IR、波数軸、吸光度、ATR / 透過 / 反射、特性吸収帯、指紋領域、分解能、水分干渉、ベースライン処理を日本語で分かりやすく説明してください。まず図解や概念地図に戻る観点を示し、次に現象と理由を結びつけて説明してください。", suggestedPaths: ["ATR と透過の違いを、表面情報と厚み依存の観点で3ステップで説明して", "特性吸収帯と指紋領域の読み分けを、初心者向けに整理して", "3400 cm^-1 付近の広いピークを見たときの考え方を教えて"], localTopics: [{ keywords: ["ATR", "透過", "反射", "モード"], answer: ["IR では、同じ試料でも測定モードによって見えている情報の深さと相対強度が変わります。", "ATR は表面寄り、透過は厚み全体、反射は表面状態の影響を受けやすい、とまず整理すると読みやすくなります。"] }, { keywords: ["指紋領域", "特性吸収帯", "官能基", "ピーク"], answer: ["まず特性吸収帯で候補を絞り、そのあと指紋領域で見分けるのが IR の基本です。", "ピークは単独ではなく、位置・幅・組み合わせで読むと誤読が減ります。"] }, { keywords: ["水分", "ベースライン", "分解能", "ノイズ"], answer: ["3400 と 1640 cm^-1 付近は水分干渉を疑う代表帯域です。", "分解能が粗いと指紋領域の差がつぶれやすいので、試料本来の変化か測定条件由来かを切り分けて考えるのが大事です。"] }], explanationRubric: [{ title: "FT-IR で干渉信号から波数スペクトルへ戻す流れを説明できる" }, { title: "横軸を固定して、ピーク位置から読む理由を説明できる" }, { title: "ATR / 透過 / 反射の違いを、見える情報の差として説明できる" }, { title: "分解能・水分干渉・ベースラインの影響を切り分けて話せる" }], ui: { textareaPlaceholder: "例: ATR と透過の違いを、表面情報と厚み依存で説明して" } },
        media: { title: "参考リソース", description: "今回はまずアプリ内の原理・概念・図解を優先し、外部リンクは最小限にしています。", featuredVideo: null, resources: [] }
    };

    window.NanoLearnTopicModules.ir = {
        topic
    };
})();
