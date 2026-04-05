(function () {
    function renderTaverScene(options, helpers) {
        const escapeHtml = helpers.escapeHtml;
        const asArray = helpers.asArray;
        const labels = asArray(options.labels).slice(0, 3);
        const variant = options.variant || "topview";

        let stage = "";
        if (variant === "abrasive") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-abrasive">
                    <div class="scene-taver-bed"></div>
                    <div class="scene-taver-bed-edge"></div>
                    <div class="scene-taver-abrasive-tool">
                        <span class="scene-taver-abrasive-grit scene-taver-abrasive-grit-a"></span>
                        <span class="scene-taver-abrasive-grit scene-taver-abrasive-grit-b"></span>
                        <span class="scene-taver-abrasive-grit scene-taver-abrasive-grit-c"></span>
                    </div>
                    <div class="scene-taver-scratch-band"></div>
                    <div class="scene-taver-scratch-band scene-taver-scratch-band-2"></div>
                    <div class="scene-taver-chip scene-taver-chip-a"></div>
                    <div class="scene-taver-chip scene-taver-chip-b"></div>
                </div>
            `;
        } else if (variant === "adhesive") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-adhesive">
                    <div class="scene-taver-bed"></div>
                    <div class="scene-taver-bed-edge"></div>
                    <div class="scene-taver-adhesive-top">
                        <div class="scene-taver-adhesive-bond"></div>
                    </div>
                    <div class="scene-taver-adhesive-shadow"></div>
                    <div class="scene-taver-adhesive-transfer"></div>
                </div>
            `;
        } else if (variant === "fatigue") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-fatigue">
                    <div class="scene-taver-fatigue-hit scene-taver-fatigue-hit-a"></div>
                    <div class="scene-taver-fatigue-hit scene-taver-fatigue-hit-b"></div>
                    <div class="scene-taver-fatigue-hit scene-taver-fatigue-hit-c"></div>
                    <div class="scene-taver-fatigue-echo scene-taver-fatigue-echo-a"></div>
                    <div class="scene-taver-fatigue-echo scene-taver-fatigue-echo-b"></div>
                    <div class="scene-taver-bed"></div>
                    <div class="scene-taver-bed-edge scene-taver-fatigue-edge"></div>
                    <div class="scene-taver-fatigue-crack"></div>
                </div>
            `;
        } else if (variant === "wearindex") {
            stage = `
                <div class="scene-taver-wear scene-taver-wear-index">
                    <div class="scene-taver-index-axis scene-taver-index-axis-y"></div>
                    <div class="scene-taver-index-axis scene-taver-index-axis-x"></div>
                    <div class="scene-taver-index-bar scene-taver-index-bar-a"></div>
                    <div class="scene-taver-index-bar scene-taver-index-bar-b"></div>
                    <div class="scene-taver-index-bar scene-taver-index-bar-c"></div>
                    <div class="scene-taver-index-guide"></div>
                </div>
            `;
        } else {
            stage = `
                <div class="scene-taver-topview">
                    <div class="scene-taver-platter">
                        <div class="scene-taver-table"></div>
                        <div class="scene-taver-dash"></div>
                        <div class="scene-taver-ring"></div>
                        <div class="scene-taver-track scene-taver-track-a"></div>
                        <div class="scene-taver-track scene-taver-track-b"></div>
                        <div class="scene-taver-hub"></div>
                    </div>
                    <div class="scene-taver-carriage">
                        <div class="scene-taver-wheel scene-taver-wheel-left"></div>
                        <div class="scene-taver-wheel scene-taver-wheel-right"></div>
                        <div class="scene-taver-axis"></div>
                    </div>
                </div>
            `;
        }

        return `
            <div class="concept-scene ${options.sceneClass || ""}">
                <div class="scene-frame scene-frame-taver">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "TABER")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "MOTION")}</div>
                    ${stage}
                </div>
                <div class="scene-legend">
                    ${labels.map((label) => `<span class="scene-legend-chip">${escapeHtml(label)}</span>`).join("")}
                </div>
                <p class="scene-caption">${escapeHtml(options.caption || "")}</p>
            </div>
        `;
    }
    
    function enhanceTaverVisualScenario(baseScenario) {
        const scenario = Object.assign({}, baseScenario);
        if (scenario.chart) {
            scenario.chart.tooltipLabel = (raw) => {
                return `cycle ${raw.x}: ${raw.y.toFixed(1)} mg`;
            };
        }
        return scenario;
    }

    function getControlGuide(field) {
        const guides = {
            material: {
                focus: ["摩耗量", "曲線の傾き"],
                note: "試料側の違いで、同じ条件でも摩耗の増え方が変わります。",
            },
            wearMode: {
                focus: ["立ち上がり", "終点"],
                note: "摩耗メカニズムを変えると、初期と後半の増え方が変わります。",
            },
            wheelType: {
                focus: ["勾配", "最終摩耗量"],
                note: "摩耗輪の種類で削れ方の強さと安定性を見分けます。",
            },
            load: {
                focus: ["摩耗量", "測定時間"],
                note: "荷重を上げると摩耗は増えやすい一方で、比較条件も揃える必要があります。",
            }
        };
        return guides[field] || { focus: [], note: "" };
    }

    function getGuideNarration(field, options) {
        const { stateVisual, scenario, activeVisualModel } = options;

        if (field === "material") {
            return {
                title: "試料差の読み方",
                body: activeVisualModel.note || "試料によって同じ条件でも摩耗の増え方が変わります。",
            };
        }
        if (field === "wearMode") {
            if (stateVisual.wearMode === "adhesive") {
                return {
                    title: "凝着摩耗の見え方",
                    body: "移着や引きずりが効くと、途中から摩耗量の増え方が変わりやすくなります。",
                };
            }
            if (stateVisual.wearMode === "fatigue") {
                return {
                    title: "疲労摩耗の見え方",
                    body: "繰り返し荷重で表面が崩れると、後半の摩耗増加が強く出やすくなります。",
                };
            }
            return {
                title: "アブレシブ摩耗の見え方",
                body: "削る成分が支配的なときは、摩耗曲線が比較的素直に立ち上がります。",
            };
        }
        if (field === "wheelType") {
            if (stateVisual.wheelType === "h22") {
                return {
                    title: "H-22 の強さ",
                    body: "H-22 は強めの条件になりやすく、短い時間でも差が開きやすい設定です。",
                };
            }
            if (stateVisual.wheelType === "cs10") {
                return {
                    title: "CS-10 の穏やかさ",
                    body: "CS-10 は比較的穏やかな摩耗輪として、条件差の見分けに向きます。",
                };
            }
            return {
                title: "H-18 を基準に見る",
                body: "H-18 を基準に、他の摩耗輪で勾配と終点がどう変わるかを比較します。",
            };
        }
        if (field === "load") {
            return Number(stateVisual.load) >= 1000
                ? {
                    title: "重い荷重で差が開く",
                    body: "高荷重では摩耗量が増えやすく、条件差も短時間で見えやすくなります。",
                }
                : Number(stateVisual.load) <= 250
                    ? {
                        title: "軽い荷重で初期を見る",
                        body: "250 g では変化が緩やかになり、初期挙動を比較しやすくなります。",
                    }
                    : {
                        title: "500 g を基準に比較する",
                        body: "中間荷重では、強すぎず弱すぎない条件として差を見やすくできます。",
                    };
        }
        return {
            title: "条件を比較する",
            body: "条件を変えてグラフを観察します。"
        };
    }

    function renderTaverIntroJourneyCard() {
        return `
            <div class="intro-journey-card rounded-[28px] p-6 sm:p-8">
                <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <div class="text-xs font-bold tracking-[0.18em] text-blue-700">FIRST ROUTE</div>
                        <h3 class="mt-2 text-2xl font-black text-slate-900">最初に見る順番を決めておく</h3>
                        <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                            テーバーは、いきなり摩耗量だけを見るよりも、装置の動きと摩耗メカニズムを先に押さえると結果が読みやすくなります。
                        </p>
                    </div>
                    <div class="tag tag-good">taver 導線</div>
                </div>
                <div class="intro-journey-grid mt-6 grid gap-3">
                    <div class="intro-journey-step">
                        <div class="intro-journey-badge">01</div>
                        <div class="mt-3 text-base font-black text-slate-900">測定原理</div>
                        <p class="mt-2 text-sm leading-6 text-slate-600">offset 配置と rub-wear action を先に見て、装置が何をしているかを押さえます。</p>
                    </div>
                    <div class="intro-journey-step">
                        <div class="intro-journey-badge">02</div>
                        <div class="mt-3 text-base font-black text-slate-900">概念地図</div>
                        <p class="mt-2 text-sm leading-6 text-slate-600">abrasive / adhesive / fatigue の違いを並べて、何が効くかを整理します。</p>
                    </div>
                    <div class="intro-journey-step">
                        <div class="intro-journey-badge">03</div>
                        <div class="mt-3 text-base font-black text-slate-900">図解</div>
                        <p class="mt-2 text-sm leading-6 text-slate-600">摩耗輪と荷重を変えて、摩耗量がどう増えるかを条件付きで比較します。</p>
                    </div>
                </div>
                <div class="mt-6 flex flex-wrap gap-3">
                    <button class="rounded-full bg-slate-900 px-5 py-3 text-sm font-bold text-white" data-action="goto-section" data-section="principle">測定原理から見る</button>
                    <button class="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-bold text-slate-700" data-action="goto-section" data-section="concepts">概念地図へ進む</button>
                </div>
            </div>
        `;
    }

    window.NanoLearnTaverUi = {
        renderScene: renderTaverScene,
        enhanceVisualScenario: enhanceTaverVisualScenario,
        getControlGuide,
        getGuideNarration,
        renderIntroJourneyCard: renderTaverIntroJourneyCard
    };
})();
