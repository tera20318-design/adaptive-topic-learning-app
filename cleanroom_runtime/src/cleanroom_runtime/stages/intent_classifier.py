from __future__ import annotations

from cleanroom_runtime.models import IntentResult, RunRequest
from cleanroom_runtime.utils import normalize_text


def classify_intent(request: RunRequest) -> IntentResult:
    haystack = normalize_text(" ".join([request.topic, request.use_context, request.desired_depth, request.output_type]))
    if any(token in haystack for token in ("document review", "review a draft", "review the draft", "document", "memo", "policy draft", "uploaded")):
        return IntentResult(
            intent_label="document_review",
            decision_focus="ground conclusions in the checked document without overextending what it proves",
            reader_task="confirm what the checked document states, what it does not establish, and what needs outside verification",
            report_shape_hints=["direct_answer", "decision_layer", "checklist", "uncertainty"],
        )
    if any(token in haystack for token in ("compare", "comparison", "versus", "vs")):
        return IntentResult(
            intent_label="comparison_report",
            decision_focus="compare meaningful differences without overstating evidence",
            reader_task="understand tradeoffs before choosing",
            report_shape_hints=["options", "decision_layer", "checklist"],
        )
    if any(token in haystack for token in ("decide", "decision", "recommend", "procure", "approve")):
        return IntentResult(
            intent_label="decision_memo",
            decision_focus="support a bounded decision with visible uncertainty",
            reader_task="decide what can be acted on now and what still needs checking",
            report_shape_hints=["analysis", "decision_layer", "checklist"],
        )
    if any(token in haystack for token in ("explain", "overview", "mechanism", "how it works")):
        return IntentResult(
            intent_label="technical_explainer",
            decision_focus="clarify the structure, mechanism, and limits",
            reader_task="understand the topic well enough to ask the next right question",
            report_shape_hints=["direct_answer", "findings", "uncertainty"],
        )
    return IntentResult(
        intent_label="generic_report",
        decision_focus="answer the stated question without inflating confidence",
        reader_task="use the checked evidence with visible limits",
        report_shape_hints=["direct_answer", "findings", "decision_layer"],
    )
