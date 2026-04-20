from __future__ import annotations

from research_os_v2.catalogs import INTENT_TYPES
from research_os_v2.models import IntentClassification, ResearchRequest


def classify_intent(request: ResearchRequest) -> IntentClassification:
    explicit = (request.output_type or "").strip().lower()
    if explicit in INTENT_TYPES:
        return IntentClassification(
            label=explicit,
            rationale="Used the explicit output type provided in the request.",
            decision_focus=_decision_focus_for(explicit),
        )

    haystack = " ".join(
        part
        for part in [
            request.topic,
            request.use_context,
            request.question,
            request.reader,
        ]
        if part
    ).lower()

    keyword_map = [
        ("comparison", ["compare", "comparison", "versus", "vs", "選定", "比較"]),
        ("decision memo", ["decision", "memo", "recommend", "procurement", "判断"]),
        ("technical explainer", ["how it works", "technical", "mechanism", "architecture", "仕組み"]),
        ("legal overview", ["legal", "regulation", "compliance", "regulatory", "法", "規制"]),
        ("product guide", ["buyer", "product", "tool", "guide", "製品"]),
        ("literature review", ["literature", "review", "papers", "research", "学術"]),
        ("strategy memo", ["strategy", "market", "adoption", "roadmap", "戦略"]),
    ]

    for label, keywords in keyword_map:
        if any(keyword in haystack for keyword in keywords):
            return IntentClassification(
                label=label,
                rationale=f"Detected {label} keywords in the request context.",
                decision_focus=_decision_focus_for(label),
            )

    return IntentClassification(
        label="report",
        rationale="Defaulted to a general report because no stronger signal was found.",
        decision_focus=_decision_focus_for("report"),
    )


def _decision_focus_for(intent_label: str) -> str:
    mapping = {
        "report": "Summarize what matters and help the reader decide what to check next.",
        "comparison": "Highlight tradeoffs, fit conditions, and non-obvious differences.",
        "decision memo": "Support a near-term decision with explicit conditions and risks.",
        "technical explainer": "Explain mechanisms, boundaries, and implementation-relevant implications.",
        "legal overview": "Separate binding text, interpretation, and practical caution.",
        "product guide": "Match reader needs to options and evaluation criteria.",
        "literature review": "Differentiate consensus, mixed evidence, and open questions.",
        "strategy memo": "Connect evidence to priorities, scenarios, and next moves.",
    }
    return mapping.get(intent_label, mapping["report"])
