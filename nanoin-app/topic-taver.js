(function () {
    window.NanoLearnTopicModules = window.NanoLearnTopicModules || {};

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
        yAxisRange: { min: 0, max: 120 },
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

    window.NanoLearnTopicModules.taver = {
        topic: TAVER_TOPIC
    };
})();
