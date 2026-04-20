from __future__ import annotations

from research_os_v2.models import DomainAdapter, ReportSectionPlan


def build_report_plan(adapter: DomainAdapter) -> list[ReportSectionPlan]:
    return [
        ReportSectionPlan("direct_answer", "Direct answer", "Lead with the most decision-useful answer."),
        ReportSectionPlan("scope", "Scope and exclusions", "Prevent predictable misreadings early."),
        ReportSectionPlan("core", "Core explanation", "Explain the main mechanics or structure."),
        ReportSectionPlan("analysis", "Decision-relevant analysis", "Connect evidence to the reader's decision."),
        ReportSectionPlan("options", "Main options, categories, or mechanisms", "Show the main landscape clearly."),
        ReportSectionPlan("risks", "Risks and failure modes", "Give material risks real space."),
        ReportSectionPlan("findings", "Evidence-backed findings", "State what the evidence best supports."),
        ReportSectionPlan("decision_layer", "Reader decision layer", "Tell the reader what to check or decide next."),
        ReportSectionPlan("checklist", "Checklist or decision table", "Provide a practical verification aid."),
        ReportSectionPlan("uncertainty", "Uncertainty and next research", "State remaining gaps honestly."),
        ReportSectionPlan("sources", "Sources", "List the cited sources for quick auditability."),
    ]
