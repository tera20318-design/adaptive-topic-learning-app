from __future__ import annotations

from copy import deepcopy

from research_os_v2.catalogs import MODE_BASELINES
from research_os_v2.models import BudgetPlan, IntentClassification, ResearchRequest, RiskTierAssessment


def plan_scope_and_budget(
    request: ResearchRequest,
    intent: IntentClassification,
    risk: RiskTierAssessment,
) -> BudgetPlan:
    requested_mode = (request.requested_mode or "scoped").strip().lower()
    if requested_mode not in MODE_BASELINES:
        requested_mode = "scoped"

    recommended_mode = _recommended_mode(intent.label, risk.risk_tier)
    original_budget = deepcopy(MODE_BASELINES[recommended_mode])
    effective_budget = deepcopy(MODE_BASELINES[requested_mode])
    override_reason = "No override."

    if requested_mode != recommended_mode:
        override_reason = (
            f"Requested mode `{requested_mode}` overrides the `{recommended_mode}` baseline "
            f"recommended by intent and risk."
        )

    full_dr_equivalent = requested_mode == "full"
    implication = (
        "This run can be labeled complete only if its own gate passes; "
        "it is not full Deep Research equivalent."
    )
    if full_dr_equivalent:
        implication = "This run can be labeled complete if the full baseline gate passes."

    limitations = []
    if requested_mode != "full":
        limitations.append("The run is intentionally lighter than a full Deep Research equivalent.")
    if risk.risk_tier == "high" and requested_mode != "full":
        limitations.append("High-stakes areas in a scoped run require especially explicit limitations.")

    return BudgetPlan(
        requested_mode=request.requested_mode or requested_mode,
        effective_mode=requested_mode,
        preset_baseline_budget=original_budget,
        effective_budget=effective_budget,
        override_reason=override_reason,
        override_authority="user_request",
        full_dr_equivalent=full_dr_equivalent,
        report_status_implication=implication,
        limitations=limitations,
    )


def _recommended_mode(intent_label: str, risk_tier: str) -> str:
    if risk_tier == "high":
        return "full"
    if intent_label in {"comparison", "decision memo", "legal overview", "literature review"}:
        return "scoped"
    return "lightweight"
