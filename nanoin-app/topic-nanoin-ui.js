(function () {
    function renderNanoIndentScene(options, helpers) {
        const escapeHtml = helpers.escapeHtml;
        const asArray = helpers.asArray;
        const sceneClass = options.sceneClass || "";
        const labels = asArray(options.labels).slice(0, 3);
        
        return `
            <div class="concept-scene ${sceneClass}">
                <div class="scene-frame scene-frame-nano">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "FORCE")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "READOUT")}</div>
                    <div class="scene-indent-wrap">
                        <div class="scene-probe"></div>
                        <div class="scene-force-line"></div>
                        ${options.showContactHalo ? '<div class="scene-contact-halo"></div>' : ""}
                        ${options.showStressFan ? '<div class="scene-stress-fan"></div>' : ""}
                        ${options.showDepthMarker ? '<div class="scene-depth-marker"></div>' : ""}
                        <div class="scene-surface ${options.roughSurface ? "scene-surface-rough" : ""}"></div>
                        ${options.showFilm ? '<div class="scene-film-layer"></div>' : ""}
                        ${options.showSubstrate ? '<div class="scene-substrate-layer"></div>' : ""}
                        <div class="scene-indent-mark ${options.indentClass || ""}"></div>
                        ${options.showCurve ? '<div class="scene-mini-curve"></div>' : ""}
                        ${options.showSpring ? '<div class="scene-spring-arc"></div>' : ""}
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
                focus: ["曲線の形", "残留深さ"],
                note: "材料モデルで負荷曲線と除荷後の戻り方が変わります。",
            },
            filmThickness: {
                focus: ["接触深さ", "基板影響"],
                note: "膜厚に対して押し込みが深すぎると、下地の影響を受けやすくなります。",
            },
            roughness: {
                focus: ["浅部ノイズ", "読み取りの揺れ"],
                note: "表面粗さが大きいほど、浅い領域の読みが不安定になります。",
            },
            tipRadius: {
                focus: ["初期勾配", "接触面積"],
                note: "先端が丸いほど、初期接触の見え方と接触面積が変わります。",
            }
        };
        return guides[field] || { focus: [], note: "" };
    }

    function getGuideNarration(field, options) {
        const { stateVisual, scenario, activeVisualModel } = options;

        if (field === "material") {
            return {
                title: "材料差を読む",
                body: activeVisualModel.note || "材料ごとに曲線の形と残留深さの出方が変わります。",
            };
        }
        if (field === "filmThickness") {
            const ratio = scenario.thickness ? scenario.maxDepth / scenario.thickness : 0;
            return ratio >= 0.3
                ? {
                    title: "基板影響に注意する",
                    body: `押し込み深さが膜厚の ${(ratio * 100).toFixed(0)}% に近く、下地の影響を受けやすい条件です。`,
                }
                : {
                    title: "膜単体に近い読み",
                    body: `押し込み深さが膜厚の ${(ratio * 100).toFixed(0)}% 程度で、膜の挙動を読みやすい条件です。`,
                };
        }
        if (field === "roughness") {
            return Number(stateVisual.roughness) >= 12
                ? {
                    title: "浅部ノイズを読む",
                    body: "表面粗さが大きいと、浅い領域の立ち上がりが揺れやすくなります。",
                }
                : {
                    title: "浅部が比較的安定する",
                    body: "粗さが小さいため、初期接触の違いを読み取りやすい条件です。",
                };
        }
        if (field === "tipRadius") {
            return Number(stateVisual.tipRadius) >= 70
                ? {
                    title: "丸い先端で接触が広がる",
                    body: "先端が丸いほど、初期接触面積が広くなり、浅部の勾配が変わります。",
                }
                : {
                    title: "鋭い先端で食い込みやすい",
                    body: "先端が鋭いほど、浅い領域でも深さが入りやすくなります。",
                };
        }
        return {
            title: "条件を比較する",
            body: "条件を変えてグラフを観察します。"
        };
    }

    window.NanoLearnNanoinUi = {
        renderScene: renderNanoIndentScene,
        getControlGuide,
        getGuideNarration
    };
})();
