(function () {
    function renderScene(options, helpers) {
        const escapeHtml = helpers.escapeHtml;
        const asArray = helpers.asArray;
        const labels = asArray(options.labels).slice(0, 3);
        const variant = options.variant || "column";
        let stage = "";

        if (variant === "detectors") {
            stage = `
                <div class="scene-epma-stage scene-epma-stage-detectors">
                    <div class="scene-epma-sample-block"></div>
                    <div class="scene-epma-beam-column"></div>
                    <div class="scene-epma-beam-line"></div>
                    <div class="scene-epma-ray scene-epma-ray-a"></div>
                    <div class="scene-epma-ray scene-epma-ray-b"></div>
                    <div class="scene-epma-eds-box">EDS</div>
                    <div class="scene-epma-wds-crystal"></div>
                    <div class="scene-epma-wds-counter">WDS</div>
                    <div class="scene-epma-detector-rail"></div>
                </div>
            `;
        } else if (variant === "prep") {
            stage = `
                <div class="scene-epma-stage scene-epma-stage-prep">
                    <div class="scene-epma-sample-tile"></div>
                    <div class="scene-epma-polish-head"></div>
                    <div class="scene-epma-polish-trail"></div>
                    <div class="scene-epma-rinse-drop scene-epma-rinse-drop-a"></div>
                    <div class="scene-epma-rinse-drop scene-epma-rinse-drop-b"></div>
                    <div class="scene-epma-carbon-film"></div>
                    <div class="scene-epma-prep-chip scene-epma-prep-chip-a"></div>
                    <div class="scene-epma-prep-chip scene-epma-prep-chip-b"></div>
                </div>
            `;
        } else if (variant === "matrix") {
            stage = `
                <div class="scene-epma-stage scene-epma-stage-matrix">
                    <div class="scene-epma-matrix-sample"></div>
                    <div class="scene-epma-beam-column"></div>
                    <div class="scene-epma-beam-line"></div>
                    <div class="scene-epma-volume-shell scene-epma-volume-shell-a"></div>
                    <div class="scene-epma-volume-shell scene-epma-volume-shell-b"></div>
                    <div class="scene-epma-matrix-arrow scene-epma-matrix-arrow-z">Z</div>
                    <div class="scene-epma-matrix-arrow scene-epma-matrix-arrow-a">A</div>
                    <div class="scene-epma-matrix-arrow scene-epma-matrix-arrow-f">F</div>
                </div>
            `;
        } else if (variant === "charging") {
            stage = `
                <div class="scene-epma-stage scene-epma-stage-charging">
                    <div class="scene-epma-sample-block scene-epma-sample-block-insulator"></div>
                    <div class="scene-epma-carbon-film scene-epma-carbon-film-thin"></div>
                    <div class="scene-epma-beam-column"></div>
                    <div class="scene-epma-beam-line scene-epma-beam-line-jitter"></div>
                    <div class="scene-epma-charge-ring scene-epma-charge-ring-a"></div>
                    <div class="scene-epma-charge-ring scene-epma-charge-ring-b"></div>
                    <div class="scene-epma-charge-dot scene-epma-charge-dot-a"></div>
                    <div class="scene-epma-charge-dot scene-epma-charge-dot-b"></div>
                    <div class="scene-epma-charge-dot scene-epma-charge-dot-c"></div>
                </div>
            `;
        } else {
            stage = `
                <div class="scene-epma-stage scene-epma-stage-column">
                    <div class="scene-epma-column"></div>
                    <div class="scene-epma-gun"></div>
                    <div class="scene-epma-lens scene-epma-lens-a"></div>
                    <div class="scene-epma-lens scene-epma-lens-b"></div>
                    <div class="scene-epma-beam-line"></div>
                    <div class="scene-epma-sample-block"></div>
                    <div class="scene-epma-volume"></div>
                    <div class="scene-epma-ray scene-epma-ray-a"></div>
                    <div class="scene-epma-ray scene-epma-ray-b"></div>
                    <div class="scene-epma-detector-box">${escapeHtml(options.detectorLabel || "EDS / WDS")}</div>
                </div>
            `;
        }

        return `
            <div class="concept-scene ${options.sceneClass || ""}">
                <div class="scene-frame scene-frame-epma">
                    <div class="scene-frame-grid"></div>
                    <div class="scene-frame-glow"></div>
                    <div class="scene-frame-label scene-frame-label-left">${escapeHtml(options.frameLabelLeft || "COLUMN")}</div>
                    <div class="scene-frame-label scene-frame-label-right">${escapeHtml(options.frameLabelRight || "XRAY")}</div>
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
                focus: ["ピーク構成", "チャージリスク"],
                note: "試料モデルを変えると、見えるピークとチャージしやすさが同時に変わります。"
            },
            acceleratingVoltage: {
                focus: ["相互作用体積", "励起できる線種"],
                note: "電圧を上げるほど深くまで励起できますが、局所性は落ちやすくなります。"
            },
            beamCurrent: {
                focus: ["相対強度", "損傷 / チャージ"],
                note: "電流は信号量を増やす一方で、絶縁試料では損傷と帯電のリスクも上げます。"
            },
            detectorMode: {
                focus: ["ピーク分離", "比較線との差"],
                note: "EDS と WDS の違いは、高さよりも重なり方と分解能の差で読みます。"
            },
            carbonCoating: {
                focus: ["低エネルギー側", "チャージリスク"],
                note: "炭素膜を厚くすると帯電は抑えやすくなりますが、軽元素側の見え方には影響が出ます。"
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
                title: "試料ごとに、見えるピークと壊れやすさが変わる",
                body: activeVisualModel.note || "導電性、軽元素の多さ、近接ピークの有無で、最適条件は変わります。"
            };
        }
        if (field === "acceleratingVoltage") {
            return Number(stateVisual.acceleratingVoltage) >= 15
                ? {
                    title: "高い加速電圧で深くまで励起できる",
                    body: `今は ${Number(scenario.interactionDepth || 0).toFixed(1)} um 程度まで相互作用体積が広がる想定です。励起できる線は増えますが、局所性は落ちやすくなります。`
                }
                : {
                    title: "低めの加速電圧で局所性を保ちやすい",
                    body: `今は ${Number(scenario.interactionDepth || 0).toFixed(1)} um 程度で比較的浅く、表面近傍の情報を重視する条件です。見えにくくなる線種も同時に意識します。`
                };
        }
        if (field === "beamCurrent") {
            return Number(stateVisual.beamCurrent) >= 60
                ? {
                    title: "信号は増えるが、帯電と損傷の余裕は減る",
                    body: `電流を上げて相対強度は稼げますが、現在のチャージリスクは ${scenario.chargingRisk || "中"} 寄りです。絶縁試料では攻めすぎに注意します。`
                }
                : {
                    title: "穏やかな電流で試料を守りやすい",
                    body: "低めの電流では信号は控えめですが、チャージや熱損傷を抑えながら条件検討しやすくなります。"
                };
        }
        if (field === "detectorMode") {
            return stateVisual.detectorMode === "wds"
                ? {
                    title: "WDS は分離して読むためのモード",
                    body: `現在はピーク分離が ${scenario.peakSeparation || "中"} で、比較線よりも細く分かれた形を狙う設定です。微量元素や近接ピーク向きです。`
                }
                : {
                    title: "EDS は全体像を速く掴むためのモード",
                    body: "同時に広く見られる一方で、近接ピークは重なりやすくなります。未知試料の入口として使うのが自然です。"
                };
        }
        return Number(stateVisual.carbonCoating) >= 15
            ? {
                title: "厚めの炭素膜で帯電を抑えにいく",
                body: "帯電は抑えやすくなりますが、低エネルギー側では減衰も増えます。軽元素ピークの見え方を一緒に確認します。"
            }
            : {
                title: "薄めの炭素膜で軽元素側を見やすくする",
                body: "低エネルギー側の減衰は抑えやすい一方で、導電性確保が不足するとチャージリスクが上がります。"
            };
    }

    window.NanoLearnEpmaUi = {
        renderScene,
        getControlGuide,
        getGuideNarration
    };
})();
