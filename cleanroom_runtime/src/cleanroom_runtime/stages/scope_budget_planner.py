from __future__ import annotations

from cleanroom_runtime.catalogs import MODE_BASELINES
from cleanroom_runtime.models import BudgetPlan, IntentResult, RiskTierResult, RunRequest, TargetProfile


def plan_scope_and_budget(request: RunRequest, intent: IntentResult, risk: RiskTierResult) -> BudgetPlan:
    del intent
    requested_mode = request.mode if request.mode in MODE_BASELINES else "scoped"
    preset = MODE_BASELINES[requested_mode]
    effective = dict(preset)
    limitations: list[str] = []

    if risk.risk_tier == "high" and requested_mode == "scoped":
        effective["min_sources"] += 1
        effective["min_high_risk_sources"] += 1
        limitations.append("High-risk topics in scoped mode are treated as bounded rather than exhaustive.")

    if request.evidence_mode == "synthetic":
        limitations.append("Synthetic evidence can validate contracts but cannot prove live research completeness.")

    full_dr_equivalent = requested_mode == "full" and request.evidence_mode == "live"
    if not full_dr_equivalent:
        limitations.append("This run must not be described as a full Deep Research equivalent.")
    if not limitations:
        limitations.append("Even a full-equivalent live run remains bounded by the declared scope, targets, dates, and jurisdiction.")

    target_profile = TargetProfile(
        min_sources=max(request.target_profile.min_sources, effective["min_sources"]),
        min_distinct_roles=max(request.target_profile.min_distinct_roles, effective["min_distinct_roles"]),
        min_high_risk_sources=max(request.target_profile.min_high_risk_sources, effective["min_high_risk_sources"]),
    )

    research_note = (
        "synthetic_validation_only"
        if request.evidence_mode == "synthetic"
        else "live_full_candidate" if full_dr_equivalent else "live_scoped_only"
    )
    implication = (
        "This run may be complete if claim-level evidence and audit conditions are satisfied."
        if full_dr_equivalent
        else "This run can be useful within scope but is not full-equivalent research."
    )

    return BudgetPlan(
        requested_mode=requested_mode,
        effective_mode=requested_mode,
        preset_baseline_budget=dict(preset),
        effective_budget=effective,
        override_reason="No override." if requested_mode == request.mode else "Unknown mode downgraded to scoped baseline.",
        override_authority="runtime_default",
        full_dr_equivalent=full_dr_equivalent,
        report_status_implication=implication,
        limitations=limitations,
        evidence_mode=request.evidence_mode,
        research_completeness_note=research_note,
        target_profile=target_profile,
        waivers=list(request.waivers),
    )
