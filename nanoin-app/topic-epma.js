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

    function buildEpmaScenario(stateVisual, visualModels) {
        const model = visualModels[stateVisual.material] || visualModels.silicate;
        const acceleratingVoltage = Number(stateVisual.acceleratingVoltage || 15);
        const beamCurrent = Number(stateVisual.beamCurrent || 40);
        const detectorMode = stateVisual.detectorMode || "wds";
        const carbonCoating = Number(stateVisual.carbonCoating || 12);
        const axis = buildEnergyAxis(0, 12, 0.05);
        const detectorWidthFactor = detectorMode === "wds" ? 0.34 : 1.08;
        const detectorGain = detectorMode === "wds" ? 0.86 : 1.0;
        const currentFactor = clamp(Math.sqrt(beamCurrent / 40), 0.45, 2.4);
        const lowEnergyPenalty = clamp(1 - carbonCoating * 0.018, 0.58, 1);
        const interactionDepth = clamp(0.22 + acceleratingVoltage * 0.11 * model.depthBias, 0.4, 4.8);
        const interactionDiameter = clamp(0.12 + acceleratingVoltage * 0.08 * model.spreadBias + beamCurrent * 0.002, 0.18, 4.2);
        const chargeScore = clamp(model.chargeBias + beamCurrent / 220 - carbonCoating / 20, 0, 1.4);
        const chargingRisk = chargeScore >= 0.95 ? "高" : chargeScore >= 0.55 ? "中" : "低";
        const peakSeparation = detectorMode === "wds" ? "高" : acceleratingVoltage >= 12 && beamCurrent >= 30 ? "中" : "低";
        const baseline = 0.03 + acceleratingVoltage * 0.006 + beamCurrent / 5000;

        function buildSpectrum(widthFactor, gain) {
            return axis.map((energy) => {
                const intensity = model.peaks.reduce((sum, peak) => {
                    const excitation = acceleratingVoltage >= peak.threshold
                        ? clamp(0.42 + (acceleratingVoltage - peak.threshold) / Math.max(peak.threshold, 1), 0.42, 1.35)
                        : 0.04;
                    const attenuation = peak.lowEnergy ? lowEnergyPenalty : 1;
                    return sum + gaussian(
                        energy,
                        peak.energy,
                        peak.width * widthFactor,
                        peak.height * excitation * attenuation * currentFactor * gain
                    );
                }, baseline);
                return {
                    x: Number(energy.toFixed(2)),
                    y: Number(intensity.toFixed(3))
                };
            });
        }

        const data = buildSpectrum(detectorWidthFactor, detectorGain);
        const altMode = detectorMode === "wds" ? "eds" : "wds";
        const compareData = buildSpectrum(altMode === "wds" ? 0.34 : 1.08, altMode === "wds" ? 0.86 : 1.0);

        return {
            model,
            acceleratingVoltage,
            beamCurrent,
            detectorMode,
            carbonCoating,
            interactionDepth: Number(interactionDepth.toFixed(2)),
            interactionDiameter: Number(interactionDiameter.toFixed(2)),
            chargingRisk,
            peakSeparation,
            peakMarkers: model.peaks.map((peak) => ({
                label: peak.label,
                energy: peak.energy
            })),
            insights: [
                {
                    title: "加速電圧で相互作用体積が変わる",
                    body: acceleratingVoltage >= 15
                        ? "高めの加速電圧では励起できる線種が増える一方、分析深さとビームの広がりも増えます。薄膜や粒子では下地影響を疑う視点が必要です。"
                        : "低めの加速電圧では局所性を保ちやすい一方、励起しにくい線種が出てきます。何を見たい条件かを先に決めることが重要です。"
                },
                {
                    title: "EDS と WDS は役割で使い分ける",
                    body: detectorMode === "wds"
                        ? "WDS はピーク分離と微量元素に強く、近接ピークや精密定量で価値が大きい条件です。"
                        : "EDS は全体スクリーニングに向きます。未知試料の入口として速く広く見るフェーズに向いています。"
                },
                {
                    title: "高電流は常に有利ではない",
                    body: chargingRisk === "高"
                        ? "今はチャージや熱損傷のリスクが高い条件です。炭素蒸着、デフォーカス、電流管理を合わせて考える必要があります。"
                        : "今はチャージや損傷のリスクをまだ抑えやすい条件です。必要なカウント数とのバランスを取りながら読めます。"
                }
            ],
            metrics: [
                { id: "interactionDepth", label: "分析深さの目安", value: `${interactionDepth.toFixed(1)} um` },
                { id: "interactionDiameter", label: "横方向の広がり", value: `${interactionDiameter.toFixed(1)} um` },
                { id: "peakSeparation", label: "ピーク分離しやすさ", value: peakSeparation, tone: peakSeparation },
                { id: "chargingRisk", label: "チャージリスク", value: chargingRisk, tone: chargingRisk }
            ],
            chart: {
                type: "scatter",
                datasets: [
                    {
                        label: detectorMode === "wds" ? "現在条件: WDS" : "現在条件: EDS",
                        data,
                        showLine: true,
                        borderColor: detectorMode === "wds" ? "#0f172a" : "#b45309",
                        backgroundColor: detectorMode === "wds" ? "#0f172a" : "#b45309",
                        borderWidth: 2.6,
                        pointRadius: 0,
                        tension: 0.14
                    },
                    {
                        label: altMode === "wds" ? "比較: WDS" : "比較: EDS",
                        data: compareData,
                        showLine: true,
                        borderColor: altMode === "wds" ? "#2563eb" : "#94a3b8",
                        backgroundColor: altMode === "wds" ? "#2563eb" : "#94a3b8",
                        borderWidth: 2,
                        borderDash: [8, 6],
                        pointRadius: 0,
                        tension: 0.14
                    }
                ],
                tooltipLabel(raw) {
                    return `エネルギー ${raw.x} keV, 相対強度 ${raw.y.toFixed(3)}`;
                }
            }
        };
    }

    const EPMA_HERO = {
        eyebrow: "ADAPTIVE LEARNING",
        titleLead: "EPMA を",
        titleAccent: "電子線から定量まで",
        titleTrail: "つなげて理解する",
        subtitle: "電子線マイクロアナライザの学習アプリ",
        description:
            "EPMA は、電子線を試料に当てて発生した特性 X 線を分光し、微小領域の元素と濃度を読む装置です。WDS / EDS の役割分担、試料作製、ZAF 補正、長時間マッピングまで、実務で迷いやすい判断を図解で整理します。"
    };

    const EPMA_INTRO_CARDS = [
        { id: "principle", title: "測定原理", body: "電子線で内殻を励起し、特性 X 線を分光して元素を読む。まずは電子線、相互作用体積、検出器の流れを押さえる。" },
        { id: "detectors", title: "EDS と WDS", body: "EDS は全体を速く見る入口、WDS はピーク分離と微量分析に強い。役割の違いを最初に整理する。" },
        { id: "prep", title: "試料作製", body: "平坦・清浄・導電の三条件が揃って初めて、定量とマッピングの品質が安定する。" }
    ];

    const EPMA_INTRO_SUMMARY_STATES = [
        { id: "beam", label: "電子線", summary: "加速電圧とビーム電流で、見える線種と相互作用体積が変わる。" },
        { id: "detector", label: "検出器", summary: "EDS は速く広く、WDS は細かく深く。比較で覚える。" },
        { id: "surface", label: "表面", summary: "研磨、洗浄、炭素蒸着の質が、定量の信頼性を左右する。" }
    ];

    const EPMA_SELF_CHECK = [
        {
            id: "detector",
            prompt: "EDS と WDS の使い分けを、どの程度説明できますか。",
            options: [
                { value: 0, label: "まだ説明できない" },
                { value: 1, label: "速い / 分離が高い、くらいは言える" },
                { value: 2, label: "用途ごとの役割分担で説明できる" }
            ]
        },
        {
            id: "prep",
            prompt: "なぜ鏡面研磨と炭素蒸着が必要かを説明できますか。",
            options: [
                { value: 0, label: "まだ曖昧" },
                { value: 1, label: "表面とチャージの話は分かる" },
                { value: 2, label: "定量精度との関係まで説明できる" }
            ]
        },
        {
            id: "matrix",
            prompt: "マトリックス補正が必要になる理由を説明できますか。",
            options: [
                { value: 0, label: "まだ難しい" },
                { value: 1, label: "強度だけでは濃度にならないのは分かる" },
                { value: 2, label: "ZAF / φ(ρz) の必要性を説明できる" }
            ]
        }
    ];

    const EPMA_FIGURE_CARDS = [
        {
            id: "column",
            title: "電子光学系",
            label: "図 1",
            illustration: `<svg viewBox='0 0 260 120' class='w-full'>
                <rect x='114' y='8' width='32' height='18' rx='6' fill='#0f172a'/>
                <rect x='120' y='26' width='20' height='32' rx='4' fill='#334155'/>
                <ellipse cx='130' cy='64' rx='18' ry='6' fill='none' stroke='#3b82f6' stroke-width='2.5'/>
                <ellipse cx='130' cy='76' rx='14' ry='5' fill='none' stroke='#3b82f6' stroke-width='2'/>
                <line x1='130' y1='58' x2='130' y2='92' stroke='#2563eb' stroke-width='2' stroke-dasharray='3 2'/>
                <ellipse cx='130' cy='98' rx='26' ry='10' fill='rgba(14,165,233,0.18)' stroke='rgba(14,165,233,0.5)' stroke-width='1.5'/>
                <text x='170' y='100' font-size='10' fill='#475569'>相互作用体積</text>
                <text x='148' y='16' font-size='10' fill='#0f172a'>電子銃</text>
            </svg>`,
            bullets: [
                { label: "電子銃", body: "高エネルギー電子線を生成し、レンズで細く絞る" },
                { label: "相互作用体積", body: "試料内で涙滴状に広がりながら特性 X 線が発生する" },
                { label: "局所性", body: "加速電圧が上がるほど分析深さと横広がりが増す" }
            ]
        },
        {
            id: "spectrometer",
            title: "分光系",
            label: "図 2",
            illustration: `<svg viewBox='0 0 260 120' class='w-full'>
                <rect x='16' y='44' width='54' height='28' rx='10' fill='#1d4ed8'/>
                <rect x='192' y='36' width='54' height='28' rx='10' fill='#0f766e'/>
                <rect x='108' y='16' width='44' height='36' rx='12' fill='#f59e0b'/>
                <text x='28' y='62' font-size='10' fill='#fff' font-weight='bold'>EDS</text>
                <text x='200' y='54' font-size='10' fill='#fff' font-weight='bold'>WDS</text>
                <text x='115' y='38' font-size='10' fill='#0f172a'>結晶</text>
                <line x1='70' y1='58' x2='108' y2='34' stroke='#94a3b8' stroke-width='2' stroke-dasharray='4 3'/>
                <line x1='152' y1='34' x2='192' y2='50' stroke='#94a3b8' stroke-width='2'/>
                <text x='72' y='100' font-size='10' fill='#475569'>全元素を同時取得</text>
                <text x='162' y='100' font-size='10' fill='#475569'>高分離・微量対応</text>
            </svg>`,
            bullets: [
                { label: "EDS", body: "全元素を同時に取得する広域スクリーニング向け" },
                { label: "WDS", body: "分光結晶で波長を選別し高い分解能で読む" },
                { label: "使い分け", body: "入口は EDS、精密定量・近接ピークは WDS" }
            ]
        },
        {
            id: "prepflow",
            title: "試料作製フロー",
            label: "図 3",
            illustration: `<svg viewBox='0 0 260 120' class='w-full'>
                <rect x='14' y='40' width='46' height='34' rx='10' fill='#e2e8f0'/>
                <rect x='78' y='40' width='46' height='34' rx='10' fill='#bfdbfe'/>
                <rect x='142' y='40' width='46' height='34' rx='10' fill='#d1fae5'/>
                <rect x='206' y='40' width='44' height='34' rx='10' fill='#fef3c7'/>
                <path d='M60 57h14' stroke='#94a3b8' stroke-width='3' marker-end='url(#a)' stroke-linecap='round'/>
                <path d='M124 57h14' stroke='#94a3b8' stroke-width='3' stroke-linecap='round'/>
                <path d='M188 57h14' stroke='#94a3b8' stroke-width='3' stroke-linecap='round'/>
                <text x='20' y='61' font-size='9' fill='#334155'>切断</text>
                <text x='22' y='70' font-size='9' fill='#334155'>包埋</text>
                <text x='84' y='61' font-size='9' fill='#1d4ed8'>研磨</text>
                <text x='84' y='70' font-size='9' fill='#1d4ed8'>洗浄</text>
                <text x='148' y='61' font-size='9' fill='#065f46'>炭素</text>
                <text x='148' y='70' font-size='9' fill='#065f46'>蒸着</text>
                <text x='210' y='61' font-size='9' fill='#92400e'>測定</text>
                <text x='210' y='70' font-size='9' fill='#92400e'>開始</text>
            </svg>`,
            bullets: [
                { label: "平坦性", body: "鏡面研磨で X 線経路長のばらつきを抑える" },
                { label: "清浄性", body: "研磨材・汚染物の残留は偽ピークにつながる" },
                { label: "導電性", body: "炭素蒸着でチャージを抑えながら X 線吸収を最小化" }
            ]
        }
    ];

    const EPMA_CONCEPTS = [
        {
            id: "excitation",
            title: "電子線と相互作用体積",
            short: "細いビームで入っても、試料内では広がりながら X 線を生む。",
            beginner: "電子線は表面に点で当たるように見えても、試料内では散乱しながら相互作用体積を作り、その中で特性 X 線が出ます。",
            advanced: "加速電圧を上げると励起できる線種は増えますが、同時に分析深さと横方向の広がりも増え、局所性とのトレードオフが強くなります。",
            relations: [
                { target: "detectors", label: "どの線をどの精度で読むかの判断につながる" },
                { target: "matrix", label: "発生した強度が濃度に直結しない理由になる" },
                { target: "charging", label: "高電流条件でのリスクとつながる" }
            ]
        },
        {
            id: "detectors",
            title: "EDS と WDS の使い分け",
            short: "EDS は速く広く、WDS は分離と微量分析に強い。",
            beginner: "EDS と WDS は優劣ではなく役割分担で覚えると整理しやすい。未知試料の入口と精密定量は同じ条件ではありません。",
            advanced: "EDS は同時取得に強く、WDS はブラッグ分光による高分解能と高い P/B 比に強みがあります。微量元素や近接ピークでは WDS の価値が大きいです。",
            relations: [
                { target: "excitation", label: "何の線が出るかが検出器選択に影響する" },
                { target: "matrix", label: "分離できたピークをどう定量へ戻すかとつながる" },
                { target: "prep", label: "高精度定量ほど前処理品質が効いてくる" }
            ]
        },
        {
            id: "prep",
            title: "試料作製が精度を支配する",
            short: "平坦・清浄・導電の三条件が揃ってこそ、定量とマッピングは安定する。",
            beginner: "EPMA は表面分析なので、凹凸や汚染があるだけで X 線の見え方が変わります。試料作製は前処理ではなく本体の一部です。",
            advanced: "鏡面研磨は経路長ばらつきを減らし、洗浄は偽ピークを減らし、炭素蒸着はチャージとビームの不安定化を抑えます。",
            relations: [
                { target: "charging", label: "炭素蒸着と清浄性はチャージ対策の中核" },
                { target: "matrix", label: "平坦性がないと補正の前提が崩れる" },
                { target: "detectors", label: "微量分析ほど試料品質の影響が強く出る" }
            ]
        },
        {
            id: "matrix",
            title: "マトリックス補正",
            short: "強度比だけでは濃度にならず、標準化と補正が必要になる。",
            beginner: "標準試料と未知試料で強度を比べても、そのままでは濃度になりません。発生、吸収、蛍光励起の差を補正する必要があります。",
            advanced: "ZAF や φ(ρz) は、発生効率、自己吸収、二次蛍光の差を補正して、強度比を濃度に戻すための枠組みです。",
            relations: [
                { target: "excitation", label: "相互作用体積の広がりが補正理由になる" },
                { target: "detectors", label: "分離できたピークをどう濃度へ戻すかにつながる" },
                { target: "prep", label: "平坦な表面でないと補正前提が崩れる" }
            ]
        },
        {
            id: "charging",
            title: "チャージと試料損傷",
            short: "高電流条件では、チャージと熱損傷のリスクが同時に増える。",
            beginner: "信号を増やしたいからといって電流を上げるほど安全とは限りません。絶縁体では位置ずれや強度低下が起こりやすくなります。",
            advanced: "炭素蒸着、ビーム電流、デフォーカス、低温ステージなどの組み合わせで、定量に必要なカウント数と損傷リスクのバランスを取ります。",
            relations: [
                { target: "prep", label: "前処理と炭素蒸着が対策の出発点になる" },
                { target: "excitation", label: "高電圧・高電流設計では損傷リスクも見る" },
                { target: "detectors", label: "WDS の大電流条件では特に意識が必要" }
            ]
        }
    ];

    const EPMA_CONCEPT_SUPPLEMENTS = {
        excitation: "電子線を上げるほど励起できる線種は増えますが、分析体積も広がります。薄膜や粒子では『見えている元素』と『見たい元素』がずれることがあります。",
        detectors: "実務では、まず EDS で全体を見て、その後に必要箇所だけ WDS で詰める流れが自然です。",
        prep: "EPMA の失敗は装置側だけではなく、試料作製で始まっていることが多いです。前処理を別工程にしない感覚が重要です。",
        matrix: "標準試料と未知試料で同じ濃度でも、見える強度は同じではありません。補正は後付けの小細工ではなく、定量の本体です。",
        charging: "チャージは『少しズレる』だけでは済まず、ランディングエネルギーや位置再現を崩します。微量定量では特に影響が大きくなります。"
    };

    const EPMA_CONCEPT_SCENES = {
        excitation: { type: "epma", eyebrow: "INTERACTION VOLUME", title: "電子線が広がりながら X 線を生む", summary: "細いビームで入っても、試料内部では相互作用体積が広がる。加速電圧を上げるほど深さも広がる。", checks: ["加速電圧", "分析深さ", "局所性"], visual: { variant: "column", labels: ["電子銃", "相互作用体積", "特性X線"], caption: "ビームは細く入っても、試料内では涙滴状に広がりながら X 線を発生させる。" }, beats: [{ step: "01", title: "細いビームで入る", body: "電子銃とレンズで絞った一次電子が試料表面へ入る。" }, { step: "02", title: "内部で広がる", body: "散乱しながら相互作用体積を形成し、局所性に限界が生まれる。" }, { step: "03", title: "線種と深さが変わる", body: "高電圧は深くまで励起できるが、分析体積も大きくなりやすい。" }] },
        detectors: { type: "epma", eyebrow: "DETECTORS", title: "EDS と WDS は役割で使い分ける", summary: "EDS は広く速く、WDS は細かく深く。近接ピークと微量元素では WDS の価値が大きい。", checks: ["同時計測", "ピーク分離", "微量元素"], visual: { variant: "detectors", labels: ["EDS", "分光結晶", "比例計数管"], caption: "EDS は一括取得、WDS は結晶で特定波長を選別して高分解能で読む。" }, beats: [{ step: "01", title: "EDS で全体を見る", body: "未知試料の構成元素を素早く把握する入口として強い。" }, { step: "02", title: "WDS で重なりをほどく", body: "近接ピークや微量元素は分光結晶で分けて読む。" }, { step: "03", title: "分析段階で分担する", body: "スクリーニングと精密定量を別フェーズで考えると整理しやすい。" }] },
        prep: { type: "epma", eyebrow: "PREPARATION", title: "鏡面研磨と炭素蒸着が定量の土台", summary: "平坦性、清浄性、導電性が揃ってはじめて、高精度な定量条件が成立する。", checks: ["鏡面研磨", "汚染除去", "炭素蒸着"], visual: { variant: "prep", labels: ["研磨", "乾燥", "炭素膜"], caption: "切断して終わりではなく、平坦・清浄・導電の三条件を揃える必要がある。" }, beats: [{ step: "01", title: "平坦に仕上げる", body: "凹凸やダレを抑え、X 線経路長のばらつきを減らす。" }, { step: "02", title: "残留物を残さない", body: "研磨材や汚染物が残ると偽ピークや誤定量につながる。" }, { step: "03", title: "炭素膜で導電性を確保", body: "チャージを抑えつつ、X 線吸収も増やしにくい。" }] },
        matrix: { type: "epma", eyebrow: "MATRIX CORRECTION", title: "強度比だけでは濃度にならない", summary: "発生効率、吸収、二次蛍光の差を補正して、標準試料との差を濃度に戻す。", checks: ["Z", "A", "F"], visual: { variant: "matrix", labels: ["発生", "吸収", "蛍光励起"], caption: "試料の組成が違うと、同じ濃度でも見える強度は変わる。" }, beats: [{ step: "01", title: "原子番号差で発生効率が変わる", body: "電子の止まり方や発生効率はマトリックスに依存する。" }, { step: "02", title: "出てくるまでに吸収される", body: "特に低エネルギー X 線は自己吸収の影響を受けやすい。" }, { step: "03", title: "補正して定量へ戻す", body: "ZAF や φ(ρz) はこの差を埋めるための計算枠組み。" }] },
        charging: { type: "epma", eyebrow: "CHARGING", title: "信号を増やすほど安全ではなくなる", summary: "絶縁体では電流を上げるほどチャージや熱損傷のリスクが上がり、条件設計が重要になる。", checks: ["絶縁体", "位置ずれ", "損傷"], visual: { variant: "charging", labels: ["帯電", "炭素膜", "電流"], caption: "導電性が不十分なまま高電流にすると、ビームは安定して当たり続けない。" }, beats: [{ step: "01", title: "電荷が蓄積する", body: "絶縁表面では入射電子が逃げにくく、負電荷が溜まる。" }, { step: "02", title: "軌道と実効電圧がずれる", body: "位置ズレやランディングエネルギー低下で強度が落ちる。" }, { step: "03", title: "前処理と条件で抑える", body: "炭素蒸着、電流管理、デフォーカスでリスクを下げる。" }] }
    };

    const EPMA_VISUAL_MODELS = {
        silicate: {
            label: "ケイ酸塩 / ガラス",
            note: "絶縁性が高く、チャージ対策と低エネルギー側の読み方が効いてくるモデルです。",
            depthBias: 1.05,
            spreadBias: 1.0,
            chargeBias: 0.82,
            peaks: [
                { label: "O Kα", energy: 0.52, width: 0.08, height: 0.44, threshold: 1.2, lowEnergy: true },
                { label: "Na Kα", energy: 1.04, width: 0.08, height: 0.28, threshold: 2.0, lowEnergy: true },
                { label: "Mg Kα", energy: 1.25, width: 0.08, height: 0.22, threshold: 2.1, lowEnergy: true },
                { label: "Al Kα", energy: 1.49, width: 0.08, height: 0.34, threshold: 2.3, lowEnergy: true },
                { label: "Si Kα", energy: 1.74, width: 0.08, height: 0.62, threshold: 2.5, lowEnergy: false },
                { label: "Ca Kα", energy: 3.69, width: 0.09, height: 0.24, threshold: 4.5, lowEnergy: false },
                { label: "Fe Kα", energy: 6.40, width: 0.11, height: 0.16, threshold: 7.2, lowEnergy: false }
            ]
        },
        metal: {
            label: "一般金属",
            note: "導電性は高く、近接ピーク分離や微量定量では WDS の価値が見えやすいモデルです。",
            depthBias: 0.78,
            spreadBias: 0.72,
            chargeBias: 0.12,
            peaks: [
                { label: "Cr Kα", energy: 5.41, width: 0.1, height: 0.34, threshold: 6.2, lowEnergy: false },
                { label: "Mn Kα", energy: 5.90, width: 0.1, height: 0.22, threshold: 6.6, lowEnergy: false },
                { label: "Fe Kα", energy: 6.40, width: 0.1, height: 0.62, threshold: 7.1, lowEnergy: false },
                { label: "Ni Kα", energy: 7.48, width: 0.1, height: 0.29, threshold: 8.3, lowEnergy: false }
            ]
        },
        oxide: {
            label: "酸化物セラミックス",
            note: "軽元素と近接ピークが共存しやすく、マトリックス補正の影響を考えやすいモデルです。",
            depthBias: 0.92,
            spreadBias: 0.88,
            chargeBias: 0.5,
            peaks: [
                { label: "O Kα", energy: 0.52, width: 0.08, height: 0.36, threshold: 1.2, lowEnergy: true },
                { label: "Al Kα", energy: 1.49, width: 0.08, height: 0.26, threshold: 2.3, lowEnergy: true },
                { label: "Ti Kα", energy: 4.51, width: 0.09, height: 0.48, threshold: 5.2, lowEnergy: false },
                { label: "Ba Lα", energy: 4.47, width: 0.11, height: 0.24, threshold: 5.1, lowEnergy: false },
                { label: "Zr Lα", energy: 2.04, width: 0.09, height: 0.18, threshold: 2.6, lowEnergy: false }
            ]
        },
        glass: {
            label: "ソーダ石灰ガラス",
            note: "Na や低エネルギー線の扱い、水分や熱の影響を考える練習に向くモデルです。",
            depthBias: 1.08,
            spreadBias: 1.02,
            chargeBias: 0.7,
            peaks: [
                { label: "O Kα", energy: 0.52, width: 0.08, height: 0.42, threshold: 1.2, lowEnergy: true },
                { label: "Na Kα", energy: 1.04, width: 0.08, height: 0.32, threshold: 2.0, lowEnergy: true },
                { label: "Mg Kα", energy: 1.25, width: 0.08, height: 0.2, threshold: 2.1, lowEnergy: true },
                { label: "Al Kα", energy: 1.49, width: 0.08, height: 0.18, threshold: 2.3, lowEnergy: true },
                { label: "Si Kα", energy: 1.74, width: 0.08, height: 0.58, threshold: 2.5, lowEnergy: false },
                { label: "Ca Kα", energy: 3.69, width: 0.09, height: 0.22, threshold: 4.5, lowEnergy: false }
            ]
        }
    };

    const EPMA_VISUAL_LEARNING = {
        title: "条件を変えて、EPMA で何が見えやすくなるかを読む",
        description: "加速電圧、ビーム電流、検出器モード、炭素蒸着厚を動かして、相互作用体積、ピーク分離、チャージリスクのバランスを見ます。",
        buildScenario: buildEpmaScenario,
        materialLabel: "試料モデル",
        controls: [
            { field: "acceleratingVoltage", label: "加速電圧", type: "slider", min: 5, max: 20, step: 1, formatValue(value) { return `${value} kV`; } },
            { field: "beamCurrent", label: "ビーム電流", type: "slider", min: 5, max: 100, step: 5, formatValue(value) { return `${value} nA`; } },
            { field: "detectorMode", label: "検出器モード", type: "select", options: [{ value: "eds", label: "EDS" }, { value: "wds", label: "WDS" }], formatValue(value) { return String(value).toUpperCase(); } },
            { field: "carbonCoating", label: "炭素蒸着厚", type: "slider", min: 5, max: 25, step: 1, formatValue(value) { return `${value} nm`; } }
        ],
        chartCaption: "スペクトルの高さだけでなく、ピークの分離、低エネルギー側の減衰、条件を変えたときの比較線との差を見ます。",
        xAxisRange: { min: 0, max: 12 },
        yAxisRange: { min: 0, max: 1.8 },
        axisLabels: { x: "エネルギー (keV)", y: "相対強度" }
    };

    const EPMA_DIAGNOSIS_QUESTIONS = {
        q1: {
            id: "q1",
            prompt: "未知試料の全体像を最初に素早くつかみたいとき、まず何を選ぶのが自然ですか。",
            whyEasy: "EDS と WDS を優劣で覚えると迷いやすく、役割分担で考えると整理しやすいポイントです。",
            options: [
                { id: "q1-a", label: "まず EDS で全体を見て、その後に必要箇所だけ WDS へ進む", explanation: "正解です。EDS は全元素を同時に見やすく、未知試料の入口として強いです。", correct: true, misconception: false, weakness: [], next: "q2" },
                { id: "q1-b", label: "最初から全部 WDS にすれば常に最良で、EDS は不要", explanation: "不正解です。WDS は高分解能ですが、全体スクリーニングは遅く、実務では補完関係で使います。", correct: false, misconception: true, weakness: ["detectors"], next: "q2" }
            ]
        },
        q2: {
            id: "q2",
            prompt: "鏡面研磨が崩れた試料で定量が不安定になる主な理由はどれですか。",
            whyEasy: "試料作製は見た目ではなく、X 線の経路長と補正前提に効くという理解が重要です。",
            options: [
                { id: "q2-a", label: "X 線の取り出し角と経路長がばらつき、補正前提が崩れるから", explanation: "正解です。平坦性がないと経路長のばらつきが増え、定量補正が不安定になります。", correct: true, misconception: false, weakness: [], next: "q3" },
                { id: "q2-b", label: "表面が荒いだけなら、定量結果にはほとんど影響しないから", explanation: "不正解です。EPMA は表面分析なので、表面状態の影響を強く受けます。", correct: false, misconception: true, weakness: ["prep"], next: "q3" }
            ]
        },
        q3: {
            id: "q3",
            prompt: "近接ピークの分離や微量定量で WDS が有利な主因はどれですか。",
            whyEasy: "高分解能・高い P/B 比という WDS の強みを、用途と結びつけて言えるかを見る問いです。",
            options: [
                { id: "q3-a", label: "分光結晶で特定波長を選別でき、ピーク分離と P/B 比を高めやすいから", explanation: "正解です。WDS の本質は高い分解能とバックグラウンドに対する強さにあります。", correct: true, misconception: false, weakness: [], next: "q4" },
                { id: "q3-b", label: "EDS より常に速く、全元素を同時に見られるから", explanation: "不正解です。WDS は同時取得よりも、選んで精密に測る場面に強いです。", correct: false, misconception: true, weakness: ["detectors"], next: "q4" }
            ]
        },
        q4: {
            id: "q4",
            prompt: "絶縁性の高い試料でビーム電流を上げすぎるとき、まず警戒すべきことは何ですか。",
            whyEasy: "高電流はカウントを増やしますが、チャージや損傷のリスクも同時に上がります。",
            options: [
                { id: "q4-a", label: "チャージや位置ずれによるランディング条件の変化", explanation: "正解です。チャージはビームの当たり方と実効電圧を崩し、定量結果も不安定にします。", correct: true, misconception: false, weakness: [], next: "q5" },
                { id: "q4-b", label: "電流を上げるほど、必ず定量は良くなるので特に注意点はない", explanation: "不正解です。高電流は信号だけでなく、チャージと熱損傷のリスクも増やします。", correct: false, misconception: true, weakness: ["charging"], next: "q5" }
            ]
        },
        q5: {
            id: "q5",
            prompt: "EPMA の定量で標準試料が重要になる主な理由はどれですか。",
            whyEasy: "定量はピークを見た瞬間に終わらず、標準との相対比較と補正を通って濃度へ戻る、という流れを押さえたい問いです。",
            options: [
                { id: "q5-a", label: "未知試料の強度を標準と比べ、k 比と補正を経て濃度へ戻すため", explanation: "正解です。EPMA の定量は標準化とマトリックス補正を通して成立します。", correct: true, misconception: false, weakness: [], next: null },
                { id: "q5-b", label: "標準試料は装置の飾りで、定量値は未知試料だけでほぼ決まるため", explanation: "不正解です。ピーク強度だけで濃度は決まりません。標準化と補正の流れが必要です。", correct: false, misconception: true, weakness: ["matrix"], next: null }
            ]
        }
    };

    const EPMA_DIAGNOSIS_UI = {
        noMistakesText: "大きな誤解は見えていません。次は visual で条件差と見え方の対応を自分の目で確認すると定着しやすいです。",
        noRevisitTagText: "戻るべき論点は少なめです",
        nextActions: [
            { section: "visual", label: "図解で条件差を見る" },
            { section: "concepts", label: "概念地図で整理する" },
            { section: "mastery", label: "理解確認へ進む" }
        ]
    };

    const EPMA_AI_SUGGESTED_PATHS = [
        "EDS と WDS の使い分けを、実務フローとして 3 ステップで説明して",
        "なぜ鏡面研磨と炭素蒸着が必要か、定量誤差の観点で説明して",
        "加速電圧を上げると何が良くなり、何が悪くなるかを整理して",
        "標準試料、k 比、ZAF の流れを、初心者向けに順番で説明して"
    ];

    const EPMA_LOCAL_AI_TOPICS = [
        {
            keywords: ["EDS", "WDS", "分離", "ピーク"],
            answer: [
                "EPMA では EDS を入口、WDS を精密定量の道具として分けて考えると整理しやすいです。",
                "EDS は全体スクリーニングに強く、WDS は近接ピーク分離と微量定量に強い、という役割分担で覚えるのが自然です。"
            ]
        },
        {
            keywords: ["研磨", "蒸着", "チャージ", "前処理"],
            answer: [
                "試料作製は EPMA の外側ではなく本体です。平坦・清浄・導電の三条件が崩れると定量とマッピングの品質が一気に落ちます。",
                "チャージ対策は炭素蒸着だけで完結せず、電流設定やデフォーカスとの組み合わせで考える必要があります。"
            ]
        },
        {
            keywords: ["加速電圧", "ビーム電流", "相互作用体積"],
            answer: [
                "加速電圧は励起できる線種と分析深さを、ビーム電流はカウント数と損傷リスクを主に左右します。",
                "EPMA の条件設計は『見えるようにする』と『壊さない』の両立を考える作業です。"
            ]
        },
        {
            keywords: ["標準", "k比", "ZAF", "定量"],
            answer: [
                "EPMA の定量は、未知試料のピーク高さをそのまま濃度に読むのではなく、まず標準試料と比べて k 比を作り、その後に ZAF などの補正で濃度へ戻します。",
                "つまり『ピークが見えた』と『濃度が決まった』の間には、標準化とマトリックス補正という工程があります。"
            ]
        }
    ];

    const EPMA_EXPLANATION_RUBRIC = [
        { title: "電子線がどこで広がり、どこで X 線が生まれるかを説明できる" },
        { title: "EDS と WDS の違いを、役割分担として説明できる" },
        { title: "試料作製が定量結果を左右する理由を説明できる" },
        { title: "ZAF やチャージを、定量設計と結びつけて話せる" }
    ];

    const EPMA_AI_UI = {
        textareaPlaceholder: "例: なぜ WDS は近接ピーク分離に強いのか、定量との関係で説明して"
    };

    const EPMA_MASTERY_QUIZ = [
        {
            id: "em1",
            prompt: "未知試料の全体像を素早く把握したいとき、最初の一手として最も自然なのはどれですか。",
            choices: [
                { id: "em1-a", label: "まず EDS で全体を見て、必要箇所だけ WDS に進む", correct: true, explanation: "全体を速く見たうえで、必要な箇所だけ高分解能で詰める流れが自然です。" },
                { id: "em1-b", label: "最初から全部 WDS に固定する", correct: false, explanation: "WDS は強力ですが、全体スクリーニングには向きません。" }
            ]
        },
        {
            id: "em2",
            prompt: "試料作製が EPMA に重要な理由として最も適切なのはどれですか。",
            choices: [
                { id: "em2-a", label: "X 線の経路長と補正前提を安定させ、チャージも抑えるため", correct: true, explanation: "平坦性、清浄性、導電性はどれも定量の土台です。" },
                { id: "em2-b", label: "見た目がきれいなら十分で、分析値とはほぼ無関係だから", correct: false, explanation: "表面状態は分析値そのものに直結します。" }
            ]
        },
        {
            id: "em3",
            prompt: "WDS が近接ピーク分離に強い主因はどれですか。",
            choices: [
                { id: "em3-a", label: "分光結晶で特定波長を選別し、高い分解能で読めるため", correct: true, explanation: "WDS の強みはここにあります。" },
                { id: "em3-b", label: "EDS より常に速く全元素を同時に読めるため", correct: false, explanation: "それは WDS の強みではありません。" }
            ]
        },
        {
            id: "em4",
            prompt: "標準試料と ZAF 補正の関係として最も適切なのはどれですか。",
            choices: [
                { id: "em4-a", label: "標準との相対強度から k 比を作り、ZAF で濃度へ戻す", correct: true, explanation: "定量は標準化と補正を通して初めて成立します。" },
                { id: "em4-b", label: "標準試料がなくても、ピーク高さだけで濃度はほぼ決まる", correct: false, explanation: "ピーク高さだけではマトリックス影響を外せません。" }
            ]
        }
    ];

    const EPMA_ROLE_TRACKS = [
        { id: "beginner", label: "初学者", summary: "電子線と EDS / WDS の違いを言葉で説明できる。" },
        { id: "operator", label: "操作担当", summary: "試料作製と安全な条件設定を意識して測定を進められる。" },
        { id: "analyst", label: "解析担当", summary: "定量補正と誤差要因を説明できる。" }
    ];

    const EPMA_COMPETENCIES = [
        { id: "epma-principle", title: "電子線と相互作用体積", summary: "電子線、相互作用体積、特性 X 線発生の因果を言葉で追える。", roleIds: ["beginner", "operator"], conceptIds: ["excitation", "charging"], nextStep: { section: "principle", label: "測定原理を見直す" }, sources: [{ type: "concept", id: "excitation" }, { type: "mastery", id: "em1" }] },
        { id: "epma-detectors", title: "EDS / WDS の使い分け", summary: "スクリーニングと精密定量の切り分けを説明できる。", roleIds: ["beginner", "analyst"], conceptIds: ["detectors"], nextStep: { section: "concepts", conceptId: "detectors", label: "検出器比較へ" }, sources: [{ type: "diagnosis", id: "q1" }, { type: "diagnosis", id: "q3" }, { type: "mastery", id: "em3" }] },
        { id: "epma-prep", title: "試料作製とチャージ対策", summary: "研磨、洗浄、炭素蒸着、ビーム条件のバランスを説明できる。", roleIds: ["operator", "analyst"], conceptIds: ["prep", "charging"], nextStep: { section: "visual", label: "図解で条件差を見る" }, sources: [{ type: "diagnosis", id: "q2" }, { type: "diagnosis", id: "q4" }, { type: "mastery", id: "em2" }] },
        { id: "epma-quant", title: "標準化と ZAF 補正", summary: "標準試料、k 比、補正の流れを定量の一連工程として説明できる。", roleIds: ["analyst"], conceptIds: ["matrix", "detectors"], nextStep: { section: "principle", label: "原理で定量の流れを見る" }, sources: [{ type: "diagnosis", id: "q5" }, { type: "mastery", id: "em4" }] }
    ];

    const EPMA_SIMULATION_MISSIONS = [
        { id: "epma-detector-compare", title: "EDS と WDS の見え方を比べる", summary: "同じ試料で検出器モードだけを切り替え、ピーク分離の差を観察する。", competencyId: "epma-detectors", conceptId: "detectors", values: { material: "oxide", detectorMode: "wds", acceleratingVoltage: 15, beamCurrent: 40, carbonCoating: 12 }, checks: ["Ti Kα と Ba Lα の近さを見る", "比較線との差でピーク分離を読む", "なぜ入口は EDS でもよいかを言葉にする"], completionText: "ピーク分離の価値を、スペクトル形状と用途の両方で説明できれば十分です。" },
        { id: "epma-voltage-balance", title: "加速電圧の上げすぎ / 下げすぎを読む", summary: "励起できる線種と分析深さのトレードオフを観察する。", competencyId: "epma-principle", conceptId: "excitation", values: { material: "silicate", detectorMode: "wds", acceleratingVoltage: 10, beamCurrent: 40, carbonCoating: 12 }, checks: ["低電圧で見えにくくなる線を確認する", "高電圧で相互作用体積が広がることを説明する", "局所性とのトレードオフを言葉にする"], completionText: "『励起できる』と『局所性を保てる』を分けて説明できれば、このミッションは十分です。" },
        { id: "epma-coat-balance", title: "炭素蒸着とチャージ対策を読む", summary: "絶縁性試料で蒸着厚と電流のバランスを見て、位置ずれのリスクを考える。", competencyId: "epma-prep", conceptId: "charging", values: { material: "glass", detectorMode: "eds", acceleratingVoltage: 12, beamCurrent: 60, carbonCoating: 8 }, checks: ["低エネルギー側の減衰を見る", "チャージリスクの変化を読む", "蒸着だけで全ては解決しないと説明する"], completionText: "試料状態とビーム条件を一緒に見て、チャージ対策を説明できれば前進です。" }
    ];

    const EPMA_PRINCIPLE = {
        eyebrow: "MEASUREMENT PRINCIPLE",
        title: "電子線を当てて、特性 X 線を分光して元素を読む",
        description: "EPMA は高エネルギー電子線を試料に当て、内殻励起によって生じた特性 X 線を EDS または WDS で分光して、元素と濃度を調べる装置です。電子線、相互作用体積、分光器、試料作製のつながりを一つの流れで理解すると、条件設計と結果解釈が安定します。",
        scene: { type: "epma", visual: { variant: "column", frameLabelLeft: "COLUMN", frameLabelRight: "XRAY", labels: ["電子銃", "相互作用体積", "検出器"], caption: "電子線は細く入っても、試料内で広がりながら特性 X 線を生み、その信号を分光して読む。" } },
        quickFacts: [
            { label: "一次電子", body: "数 kV から数十 kV の電子線で試料を励起する。" },
            { label: "特性 X 線", body: "内殻空孔へ外側電子が落ちるときのエネルギー差で出る。" },
            { label: "分光器", body: "EDS は一括取得、WDS は選択分光に強い。" },
            { label: "定量", body: "標準化と ZAF 補正で濃度へ戻す。" }
        ],
        steps: [
            { step: "01", title: "電子線を絞って入れる", body: "電子銃とレンズで細いビームを作り、試料表面へ入れる。" },
            { step: "02", title: "相互作用体積で X 線が生まれる", body: "試料内で散乱しながら特性 X 線が発生する。" },
            { step: "03", title: "分光して定量へ戻す", body: "EDS / WDS でピークを読み、標準化と補正で濃度に変える。" }
        ],
        callout: {
            title: "EPMA では装置と試料作製を分けて考えない",
            body: "高性能な検出器だけでは十分ではありません。表面状態、チャージ、相互作用体積まで含めて一つの測定系として考えることが重要です。"
        },
        details: [
            { title: "相互作用体積はビーム径そのものではない", body: "細いビームで入っても、試料内では広がります。加速電圧と試料密度の両方が深さを左右します。" },
            { title: "定量はピーク読解の次にある工程", body: "ピークが見えたことと、そのまま濃度になることは別です。標準化と補正の理解が必要です。" }
        ]
    };

    const EPMA_TOPIC = {
        id: "epma",
        name: "EPMA",
        pageTitle: "EPMA 電子線マイクロアナライザ 適応型学習アプリ",
        storageKeySuffix: "epma",
        hero: EPMA_HERO,
        principle: EPMA_PRINCIPLE,
        introCards: EPMA_INTRO_CARDS,
        introSummaryStates: EPMA_INTRO_SUMMARY_STATES,
        selfCheck: EPMA_SELF_CHECK,
        figureCards: EPMA_FIGURE_CARDS,
        concepts: EPMA_CONCEPTS,
        conceptSupplements: EPMA_CONCEPT_SUPPLEMENTS,
        conceptScenes: EPMA_CONCEPT_SCENES,
        visualModels: EPMA_VISUAL_MODELS,
        visualLearning: EPMA_VISUAL_LEARNING,
        diagnosisQuestions: EPMA_DIAGNOSIS_QUESTIONS,
        diagnosisUi: EPMA_DIAGNOSIS_UI,
        defaults: {
            currentSection: "intro",
            roleId: "beginner",
            conceptLevel: "basic",
            activeConceptId: "excitation",
            diagnosisStartQuestionId: "q1",
            visual: { material: "silicate", acceleratingVoltage: 15, beamCurrent: 40, detectorMode: "wds", carbonCoating: 12 },
            ai: { initialMessage: "ここでは EPMA の基礎、EDS / WDS の使い分け、試料作製とチャージ対策、ZAF の考え方まで一緒に整理できます。困っている場面を一つ挙げてください。" },
            settings: { apiProvider: "gemini", apiModel: "gemini-2.0-flash" }
        },
        ai: {
            systemInstruction: "あなたは EPMA 学習支援 AI です。電子線、相互作用体積、EDS / WDS、試料作製、チャージ、ZAF 補正、マッピング設計を日本語で分かりやすく説明してください。まず visual や concepts に戻る観点を示し、その後に現象と理由を結びつけて説明してください。",
            suggestedPaths: EPMA_AI_SUGGESTED_PATHS,
            localTopics: EPMA_LOCAL_AI_TOPICS,
            explanationRubric: EPMA_EXPLANATION_RUBRIC,
            ui: EPMA_AI_UI
        },
        roles: EPMA_ROLE_TRACKS,
        competencies: EPMA_COMPETENCIES,
        simulationMissions: EPMA_SIMULATION_MISSIONS,
        masteryQuiz: EPMA_MASTERY_QUIZ,
        media: {
            title: "参考リソース",
            description: "今回はまずアプリ内の原理・概念・図解を優先し、外部リンクは最小限にしています。",
            featuredVideo: null,
            resources: []
        }
    };

    window.NanoLearnTopicModules.epma = {
        topic: EPMA_TOPIC
    };
})();
