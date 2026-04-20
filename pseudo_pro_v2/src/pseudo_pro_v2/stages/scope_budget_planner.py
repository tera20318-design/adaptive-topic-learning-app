from __future__ import annotations

from copy import deepcopy

from pseudo_pro_v2.catalogs import MODE_BASELINES
from pseudo_pro_v2.models import BudgetPlan, IntentResult, RiskTierResult, RunRequest


def plan_scope_and_budget(request: RunRequest, intent: IntentResult, risk: RiskTierResult) -> BudgetPlan:
    requested_mode = request.mode if request.mode in MODE_BASELINES else "scoped"
    recommended_mode = "full" if risk.risk_tier == "high" else "scoped"
    preset_baseline_budget = deepcopy(MODE_BASELINES[recommended_mode])
    effective_budget = deepcopy(MODE_BASELINES[requested_mode])

    override_reason = "No override."
    if requested_mode != recommended_mode:
        override_reason = (
            f"Requested mode `{requested_mode}` overrides the `{recommended_mode}` baseline recommended by intent and risk."
        )

    full_dr_equivalent = requested_mode == "full"
    implications = (
        "This run targets full-equivalent conditions if the release gate passes."
        if full_dr_equivalent
        else "This is a scoped run and not a full Deep Research equivalent."
    )
    limitations = []
    if not full_dr_equivalent:
        limitations.append("This run is scoped and not a full Deep Research equivalent.")
    if risk.risk_tier == "high" and not full_dr_equivalent:
        limitations.append("High-risk areas in a scoped run require explicit limitations and stronger gate scrutiny.")

    return BudgetPlan(
        requested_mode=requested_mode,
        effective_mode=requested_mode,
        preset_baseline_budget=preset_baseline_budget,
        effective_budget=effective_budget,
        override_reason=override_reason,
        override_authority="user_request",
        full_dr_equivalent=full_dr_equivalent,
        report_status_implication=implications,
        limitations=limitations,
        target_profile=request.target_profile,
        waivers=request.waivers,
    )
