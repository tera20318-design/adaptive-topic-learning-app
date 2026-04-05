(function () {
    function renderScene(options, helpers) {
        const escapeHtml = helpers.escapeHtml;
        const asArray = helpers.asArray;
        const labels = asArray(options.labels).slice(0, 3);
        const variant = options.variant || "interferometer";
        let stage = "";

        if (variant === "absorbance") {
            stage = `
                <div class="scene-ir-stage scene-ir-stage-absorbance">
                    <div class="scene-ir-axis scene-ir-axis-y"></div>
                    <div class="scene-ir-axis scene-ir-axis-x"></div>
                    <div class="scene-ir-trace scene-ir-trace-a"></div>
                    <div class="scene-ir-trace scene-ir-trace-b"></div>
                    <div class="scene-ir-band scene-ir-band-a"></div>
                    <div class="scene-ir-band scene-ir-band-b"></div>
                </div>
            `;
        } else if (variant === "fingerprint") {
            stage = `
                <div class="scene-ir-stage scene-ir-stage-fingerprint">
                    <div class="scene-ir-region scene-ir-region-functional"></div>
                    <div class="scene-ir-region scene-ir-region-fingerprint"></div>
                    <div class="scene-ir-divider"></div>
                    <div class="scene-ir-mini-peak scene-ir-mini-peak-a"></div>
                    <div class="scene-ir-mini-peak scene-ir-mini-peak-b"></div>
                    <div class="scene-ir-mini-peak scene-ir-mini-peak-c"></div>
                    <div class="scene-ir-mini-peak scene-ir-mini-peak-d"></div>
                </div>
            `;
        } else if (variant === "sampling") {
            stage = `
                <div class="scene-ir-stage scene-ir-stage-sampling">
                    <div class="scene-ir-sample"></div>
                    <div class="scene-ir-mode scene-ir-mode-transmission"></div>
                    <div class="scene-ir-mode scene-ir-mode-atr"></div>
                    <div class="scene-ir-mode scene-ir-mode-reflection"></div>
                    <div class="scene-ir-ray scene-ir-ray-transmission"></div>
                    <div class="scene-ir-ray scene-ir-ray-atr-a"></div>
                    <div class="scene-ir-ray scene-ir-ray-atr-b"></div>
                    <div class="scene-ir-ray scene-ir-ray-reflection-a"></div>
                    <div class="scene-ir-ray scene-ir-ray-reflection-b"></div>
                </div>
            `;
        } else if (variant === "processing") {
            stage = `
                <div class="scene-ir-stage scene-ir-stage-processing">
                    <div class="scene-ir-axis scene-ir-axis-y"></div>
                    <div class="scene-ir-axis scene-ir-axis-x"></div>
                    <div class="scene-ir-trace scene-ir-trace-processing"></div>
                    <div class="scene-ir-water scene-ir-water-a"></div>
                    <div class="scene-ir-water scene-ir-water-b"></div>
                    <div class="scene-ir-baseline"></div>
                </div>
            `;
        } else {
            stage = `
                <div class="scene-ir-stage scene-ir-stage-interferometer">
                    <div class="scene-ir-source"></div>
                    <div class="scene-ir-splitter"></div>
                    <div class="scene-ir-detector"></div>
                    <div class="scene-ir-mirror scene-ir-mirror-fixed"></div>
                    <div class="scene-ir-mirror scene-ir-mirror-moving"></div>
                    <div class="scene-ir-beam scene-ir-beam-forward"></div>
                    <div class="scene-ir-beam scene-ir-beam-up"></div>
                    <div class="scene-ir-beam scene-ir-beam-down"></div>
                    <div class="scene-ir-beam scene-ir-beam-return-a"></div>
                    <div class="scene-ir-beam scene-ir-beam-return-b"></div>
                    <div class="scene-ir-wave"></div>
                </div>
            `;
        }

        return `
            <div class="concept-scene ${options.sceneClass || ""}">
                <div class="scene-frame scene-frame-ir">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "IR")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "SIGNAL")}</div>
                    ${stage}
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
                focus: ["主ピークの位置", "指紋領域の形"],
                note: "試料モデルを変えたら、まずどの帯域が主役になるかを見ます。"
            },
            measurementMode: {
                focus: ["相対強度", "ベースライン"],
                note: "ATR・透過・反射では見えている情報の深さが違うので、高さの比較だけで決めないことが重要です。"
            },
            pathLength: {
                focus: ["吸光度の増え方", "飽和しやすい帯域"],
                note: "厚みを増やすと全体が同じように伸びるとは限りません。強い帯域ほど先に見え方が変わります。"
            },
            resolution: {
                focus: ["ピーク幅", "指紋領域"],
                note: "分解能を粗くすると、近いピーク同士から先にまとまって見えます。"
            },
            moisture: {
                focus: ["3400 cm^-1", "1640 cm^-1"],
                note: "広い O-H と水分帯を混同しないために、測定系由来の干渉を先に疑います。"
            }
        };
        return guides[field] || { focus: [], note: "" };
    }

    function getGuideNarration(field, context) {
        const stateVisual = context.stateVisual || {};
        const scenario = context.scenario || {};
        const activeVisualModel = context.activeVisualModel || {};

        if (field === "material") {
            return {
                title: "試料モデルを変えたら、まず主ピークの位置を見る",
                body: activeVisualModel.note || "どの帯域が主役かを先に見て、そのあと指紋領域の形を比較します。"
            };
        }
        if (field === "measurementMode") {
            return stateVisual.measurementMode === "transmission"
                ? {
                    title: "透過は厚み依存を素直に見やすい",
                    body: "試料全体を通る前提なので、強い帯域は早く深くなります。高さ比較だけではなく飽和の気配も見ます。"
                }
                : stateVisual.measurementMode === "reflection"
                    ? {
                        title: "反射は表面状態とベースラインの影響を受けやすい",
                        body: "今はピークの高さだけでなく、全体の揺れや歪みも一緒に見るべき条件です。"
                    }
                    : {
                        title: "ATR は表面寄りの情報として読む",
                        body: "同じ試料でも透過と比べて相対強度が変わります。高さ差をそのまま濃度差と読まないのが大事です。"
                    };
        }
        if (field === "pathLength") {
            return Number(stateVisual.pathLength) >= 80
                ? {
                    title: "厚みを増やすと、強い帯域から見え方が変わる",
                    body: "今は吸光度が全体に上がりやすく、強い帯域は先に飽和気味になります。"
                }
                : {
                    title: "薄めの条件では位置と形を追いやすい",
                    body: "今は高さ差よりも、どの帯域が現れているかを見やすい条件です。"
                };
        }
        if (field === "resolution") {
            return Number(stateVisual.resolution) >= 10
                ? {
                    title: "粗い分解能で、指紋領域の差がつぶれやすい",
                    body: `今の見分けやすさは ${scenario.fingerprintContrast || "中"} です。細かなピーク差がまとまって見えます。`
                }
                : {
                    title: "細かな分解能で、近いピークの差を残しやすい",
                    body: `今の見分けやすさは ${scenario.fingerprintContrast || "中"} です。指紋領域の確認に向く条件です。`
                };
        }
        return Number(stateVisual.moisture) >= 20
            ? {
                title: "水分帯が読解を邪魔し始めている",
                body: `今の水分干渉は ${scenario.moistureRisk || "中"} です。3400 と 1640 cm^-1 を試料本来の O-H と即断しないようにします。`
            }
            : {
                title: "水分干渉は弱めで、試料本来の帯域を追いやすい",
                body: `今の水分干渉は ${scenario.moistureRisk || "低"} です。主ピーク位置と指紋領域の形を先に見ていけます。`
            };
    }

    window.NanoLearnIrUi = {
        renderScene,
        getControlGuide,
        getGuideNarration
    };
})();
