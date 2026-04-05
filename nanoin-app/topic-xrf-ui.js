(function () {
    function renderXrfScene(options, helpers) {
        const escapeHtml = helpers.escapeHtml;
        const asArray = helpers.asArray;
        const labels = asArray(options.labels).slice(0, 3);
        
        return `
            <div class="concept-scene ${options.sceneClass || ""}">
                <div class="scene-frame scene-frame-xrf">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "SOURCE")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "DETECTOR")}</div>
                    <div class="scene-xrf-wrap">
                        <div class="scene-source-box">${escapeHtml(options.sourceLabel || "SOURCE")}</div>
                        <div class="scene-beam scene-beam-forward"></div>
                        ${options.showShield ? '<div class="scene-shield"></div>' : ""}
                        <div class="scene-sample-block ${options.sampleClass || ""}">
                            <div class="scene-sample-core"></div>
                        </div>
                        ${options.showMatrixLayers ? '<div class="scene-matrix-layers"><span></span><span></span><span></span></div>' : ""}
                        <div class="scene-beam scene-beam-return"></div>
                        <div class="scene-detector-box">${escapeHtml(options.detectorLabel || "DETECT")}</div>
                        ${options.showPeaks ? '<div class="scene-spectrum-peaks"></div>' : ""}
                        ${options.showScan ? '<div class="scene-scan-line"></div>' : ""}
                        ${options.showDoor ? '<div class="scene-door-panel"></div>' : ""}
                    </div>
                </div>
                <div class="scene-legend">
                    ${labels.map((label) => `<span class="scene-legend-chip">${escapeHtml(label)}</span>`).join("")}
                </div>
                <p class="scene-caption">${escapeHtml(options.caption || "")}</p>
            </div>
        `;
    }

    function getControlGuide(field) {
        const guides = {
            material: {
                focus: ["ピーク位置", "バックグラウンド"],
                note: "母材によって、注目ピークと背景の見えやすさが変わります。",
            },
            atmosphere: {
                focus: ["軽元素", "低エネルギー側"],
                note: "雰囲気を変えると、低エネルギー側の減衰が変わります。",
            },
            coatingThickness: {
                focus: ["膜ピーク", "下地ピーク"],
                note: "被覆厚みを変えると、膜由来と下地由来の比率が変わります。",
            },
            acquisitionTime: {
                focus: ["S/N", "微小ピーク"],
                note: "測定時間を伸ばすと、微弱なピークの見分けがしやすくなります。",
            }
        };
        return guides[field] || { focus: [], note: "" };
    }

    function getGuideNarration(field, options) {
        const { stateVisual, scenario, activeVisualModel } = options;

        if (field === "material") {
            return {
                title: "試料モデルを基準に読む",
                body: activeVisualModel.note || "試料モデルごとにピークと背景の見え方が変わります。",
            };
        }
        if (field === "atmosphere") {
            return stateVisual.atmosphere === "helium"
                ? {
                    title: "He 雰囲気で軽元素を見る",
                    body: "He 雰囲気では低エネルギー側の減衰が抑えられ、軽元素が見えやすくなります。",
                }
                : {
                    title: "真空で主要ピークを安定化",
                    body: "真空では散乱が少なく、主要ピークの比較を安定して行いやすくなります。",
                };
        }
        if (field === "coatingThickness") {
            return Number(stateVisual.coatingThickness) >= 20
                ? {
                    title: "膜ピークが優勢になる",
                    body: "被覆が厚いほど、膜由来のピークが強まり下地ピークは見えにくくなります。",
                }
                : {
                    title: "下地ピークも残る",
                    body: "被覆が薄いと、膜と下地の両方を読み分ける必要があります。",
                };
        }
        if (field === "acquisitionTime") {
            return Number(stateVisual.acquisitionTime) <= 10
                ? {
                    title: "短時間ではノイズが残る",
                    body: "測定時間が短いと、微小ピークの判断が難しくなります。",
                }
                : {
                    title: "時間をかけるとピークが見やすい",
                    body: "測定時間を伸ばすと、微弱なピークとバックグラウンドの差を読みやすくなります。",
                };
        }

        return {
            title: "条件を比較する",
            body: "条件を変えてグラフを観察します。"
        };
    }

    window.NanoLearnXrfUi = {
        renderScene: renderXrfScene,
        getControlGuide,
        getGuideNarration
    };
})();
