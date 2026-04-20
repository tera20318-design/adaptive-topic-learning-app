from __future__ import annotations

from cleanroom_runtime.catalogs import REPORT_SECTIONS
from cleanroom_runtime.models import BudgetPlan, DomainAdapter, IntentResult, ReportSectionPlan, SourceStrategy


def plan_report(
    intent: IntentResult,
    adapter: DomainAdapter,
    budget: BudgetPlan,
    strategy: SourceStrategy,
) -> list[ReportSectionPlan]:
    del budget
    del strategy
    sections: list[ReportSectionPlan] = []
    for key, title, purpose, guardrails in REPORT_SECTIONS:
        if key == "options" and "Options or comparison table" not in adapter.required_tables:
            continue
        if key == "direct_answer" and intent.intent_label == "technical_explainer":
            purpose = "Lead with the clearest bounded explanation available."
        sections.append(ReportSectionPlan(key=key, title=title, purpose=purpose, guardrails=list(guardrails)))
    return sections
