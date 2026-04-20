from __future__ import annotations

from pseudo_pro_v2.catalogs import REPORT_SECTIONS
from pseudo_pro_v2.models import DomainAdapter, ReportSectionPlan


def plan_report(adapter: DomainAdapter) -> list[ReportSectionPlan]:
    plans: list[ReportSectionPlan] = []
    for key, title, description in REPORT_SECTIONS:
        plans.append(
            ReportSectionPlan(
                key=key,
                title=title,
                description=description,
                target_claim_count=_target_claim_count(key, adapter),
                adapter_prompts=_adapter_prompts(key, adapter),
                required=_required(key, adapter),
            )
        )
    return plans


def _target_claim_count(section_key: str, adapter: DomainAdapter) -> int:
    if section_key == "direct_answer":
        return 1
    if section_key == "core":
        return 2
    if section_key == "analysis":
        return 2
    if section_key == "options":
        return 2 if "Options or comparison table" in adapter.required_tables else 1
    if section_key == "risks":
        return 2 if adapter.risk_tier == "high" else 1
    if section_key == "findings":
        return 3 if "Evidence-backed findings table" in adapter.required_tables else 1
    if section_key == "decision_layer":
        return max(1, min(2, len(adapter.required_decision_layer)))
    if section_key == "uncertainty":
        return 1 if adapter.risk_tier == "high" else 0
    if section_key in {"scope", "checklist", "sources"}:
        return 0
    return 1


def _adapter_prompts(section_key: str, adapter: DomainAdapter) -> list[str]:
    if section_key == "decision_layer":
        return list(adapter.required_decision_layer)
    if section_key == "checklist":
        return list(adapter.required_decision_layer)
    if section_key == "uncertainty":
        return list(adapter.known_limits)
    if section_key == "risks":
        return list(dict.fromkeys(adapter.likely_failure_modes + adapter.domain_specific_risks))
    if section_key == "core":
        return list(adapter.boundary_concepts)
    if section_key == "analysis":
        return list(adapter.must_not_overgeneralize)
    return []


def _required(section_key: str, adapter: DomainAdapter) -> bool:
    if section_key == "options":
        return "Options or comparison table" in adapter.required_tables or adapter.output_type in {"comparison", "decision memo"}
    if section_key == "findings":
        return "Evidence-backed findings table" in adapter.required_tables
    if section_key == "risks":
        return bool(adapter.likely_failure_modes or adapter.domain_specific_risks)
    return True
