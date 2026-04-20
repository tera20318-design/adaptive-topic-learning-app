from __future__ import annotations

from pseudo_pro_v2.models import IntentResult, RunRequest


def classify_intent(request: RunRequest) -> IntentResult:
    text = " ".join([request.topic, request.use_context, request.desired_depth]).lower()
    if "document" in text and "review" in text:
        label = "user document review"
    elif "comparison" in text or "compare" in text:
        label = "comparison"
    elif "market" in text or "business" in text:
        label = "market/business analysis"
    elif "decision" in text or "memo" in text:
        label = "decision memo"
    elif "regulatory" in text or "legal" in text:
        label = "legal overview"
    elif "technical" in text or "system" in text or "process" in text:
        label = "technical explainer"
    else:
        label = "report"

    return IntentResult(
        intent_label=label,
        decision_focus="What the reader should decide or verify next.",
        reader_task=request.use_context,
        report_shape_hints=["reader-facing headings", "report-first", "decision-useful"],
    )
