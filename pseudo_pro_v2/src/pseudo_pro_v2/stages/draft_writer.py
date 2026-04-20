from __future__ import annotations

from collections import defaultdict

from pseudo_pro_v2.models import BudgetPlan, CollectedEvidence, DomainAdapter, ReportDraft, ReportSectionPlan, ReportUnit, RunRequest, SourceFinding
from pseudo_pro_v2.utils import uniq


SECTION_HINT_TO_KEY = {
    "direct_answer": "direct_answer",
    "scope": "scope",
    "core": "core",
    "analysis": "analysis",
    "options": "options",
    "risks": "risks",
    "findings": "findings",
    "decision_layer": "decision_layer",
    "checklist": "checklist",
    "uncertainty": "uncertainty",
}


def write_draft(
    request: RunRequest,
    adapter: DomainAdapter,
    evidence: CollectedEvidence,
    section_plan: list[ReportSectionPlan],
    budget: BudgetPlan,
) -> ReportDraft:
    by_section = defaultdict(list)
    source_role_lookup = {source.source_id: source.source_role for source in evidence.sources}
    units: list[ReportUnit] = []
    used_finding_ids: set[str] = set()
    index = 1

    for finding in evidence.findings:
        key = SECTION_HINT_TO_KEY.get(finding.section_hint, _default_section(finding.claim_kind))
        by_section[key].append(finding)

    for section in section_plan:
        if section.key == "scope":
            for line in _scope_lines(request, budget):
                units.append(_non_claim_unit(index, section, line))
                index += 1
            continue

        if section.key == "sources":
            for source in evidence.sources:
                units.append(
                    ReportUnit(
                        unit_id=f"unit-{index:03d}",
                        section_key=section.key,
                        section_title=section.title,
                        text=f"{source.source_id}: {source.title} ({source.source_role}; {source.citation or source.title})",
                        claim_kind="scope_boundary",
                        risk_level="low",
                        source_ids=[source.source_id],
                        source_roles=[source.source_role],
                        confidence=1.0,
                        is_claim=False,
                    )
                )
                index += 1
            continue

        if section.key == "checklist":
            for line in _checklist_lines(section, by_section["decision_layer"], request, adapter):
                units.append(_non_claim_unit(index, section, line))
                index += 1
            continue

        if section.key == "uncertainty":
            for line in section.adapter_prompts[:3]:
                units.append(_non_claim_unit(index, section, line))
                index += 1

        for finding in _select_findings(section, by_section, evidence.findings, used_finding_ids):
            units.append(_from_finding(index, section, finding, source_role_lookup))
            used_finding_ids.add(finding.finding_id)
            index += 1

    for finding in evidence.findings:
        if finding.finding_id in used_finding_ids:
            continue
        section_key = SECTION_HINT_TO_KEY.get(finding.section_hint, _default_section(finding.claim_kind))
        section = next((item for item in section_plan if item.key == section_key), None)
        if section is None:
            continue
        shadow_unit = _from_finding(index, section, finding, source_role_lookup)
        units.append(
            ReportUnit(
                unit_id=shadow_unit.unit_id,
                section_key=shadow_unit.section_key,
                section_title=shadow_unit.section_title,
                text=shadow_unit.text,
                claim_kind=shadow_unit.claim_kind,
                risk_level=shadow_unit.risk_level,
                source_ids=shadow_unit.source_ids,
                source_roles=shadow_unit.source_roles,
                confidence=shadow_unit.confidence,
                support_status_hint=shadow_unit.support_status_hint,
                absence_type=shadow_unit.absence_type,
                contradiction_note=shadow_unit.contradiction_note,
                caveat=shadow_unit.caveat,
                required_fix=shadow_unit.required_fix,
                jurisdiction=shadow_unit.jurisdiction,
                origin_finding_id=shadow_unit.origin_finding_id,
                is_claim=True,
                include_in_report=False,
                exclusion_reason="Retained in the audit ledger but not selected for reader-facing prose.",
            )
        )
        index += 1

    return ReportDraft(title=request.topic, sections=section_plan, units=units)


def _from_finding(index: int, section: ReportSectionPlan, finding: SourceFinding, source_role_lookup: dict[str, str]) -> ReportUnit:
    return ReportUnit(
        unit_id=f"unit-{index:03d}",
        section_key=section.key,
        section_title=section.title,
        text=finding.statement,
        claim_kind=finding.claim_kind,
        risk_level=finding.risk_level,
        source_ids=finding.source_ids,
        source_roles=[source_role_lookup.get(source_id, "unknown") for source_id in finding.source_ids],
        confidence=finding.confidence,
        support_status_hint=finding.support_status_hint,
        absence_type=finding.absence_type,
        contradiction_note=finding.contradiction_note,
        caveat=finding.caveat,
        required_fix=finding.required_fix,
        jurisdiction=finding.jurisdiction,
        origin_finding_id=finding.finding_id,
    )


def _non_claim_unit(index: int, section: ReportSectionPlan, text: str) -> ReportUnit:
    return ReportUnit(
        unit_id=f"unit-{index:03d}",
        section_key=section.key,
        section_title=section.title,
        text=text,
        claim_kind="scope_boundary",
        risk_level="low",
        source_ids=[],
        source_roles=[],
        confidence=0.9,
        is_claim=False,
    )


def _scope_lines(request: RunRequest, budget: BudgetPlan) -> list[str]:
    lines = [
        f"This run addresses {request.topic} for {request.reader}.",
        f"It is intended to support: {request.use_context}.",
        f"The requested mode is `{budget.requested_mode}` and the effective mode is `{budget.effective_mode}`.",
    ]
    if not budget.full_dr_equivalent:
        lines.append("This is a scoped run and not a full Deep Research equivalent.")
    if request.jurisdiction:
        lines.append(f"Jurisdiction-sensitive statements are framed around {request.jurisdiction}.")
    return lines


def _checklist_lines(
    section: ReportSectionPlan,
    decision_findings: list[SourceFinding],
    request: RunRequest,
    adapter: DomainAdapter,
) -> list[str]:
    decision_notes = [finding.decision_note for finding in decision_findings if finding.decision_note]
    prompts = list(section.adapter_prompts)
    if request.use_context:
        prompts.insert(0, f"For {request.use_context}, verify scope, source-role support, and stated limitations.")
    if adapter.decision_context.reader_action:
        prompts.append(adapter.decision_context.reader_action)
    prompts = prompts or ["Verify scope, support, and uncertainty before action."]
    return [f"Check: {item}" for item in uniq(prompts + decision_notes)]


def _select_findings(
    section: ReportSectionPlan,
    by_section: dict[str, list[SourceFinding]],
    all_findings: list[SourceFinding],
    used_finding_ids: set[str],
) -> list[SourceFinding]:
    if section.target_claim_count <= 0:
        return []

    selected = _unused(by_section.get(section.key, []), used_finding_ids)
    if len(selected) >= section.target_claim_count:
        return _rank(selected)[: section.target_claim_count]

    fallback = _unused(_fallback_candidates(section.key, _fallback_pool(all_findings)), used_finding_ids)
    merged = _merge_unique_findings(selected + fallback)
    return _rank(merged)[: section.target_claim_count]


def _unused(findings: list[SourceFinding], used_finding_ids: set[str]) -> list[SourceFinding]:
    return [finding for finding in findings if finding.finding_id not in used_finding_ids]


def _rank(findings: list[SourceFinding]) -> list[SourceFinding]:
    return sorted(findings, key=lambda finding: (-finding.confidence, finding.finding_id))


def _merge_unique_findings(findings: list[SourceFinding]) -> list[SourceFinding]:
    seen: set[str] = set()
    ordered: list[SourceFinding] = []
    for finding in findings:
        if finding.finding_id in seen:
            continue
        seen.add(finding.finding_id)
        ordered.append(finding)
    return ordered


def _default_section(claim_kind: str) -> str:
    mapping = {
        "definition": "direct_answer",
        "mechanism": "core",
        "fact": "findings",
        "comparison": "options",
        "recommendation": "decision_layer",
        "advice": "decision_layer",
        "inference": "analysis",
        "absence": "uncertainty",
        "scope_boundary": "scope",
    }
    return mapping.get(claim_kind, "analysis")


def _fallback_candidates(section_key: str, findings: list[SourceFinding]) -> list[SourceFinding]:
    if section_key == "direct_answer":
        return [finding for finding in findings if finding.claim_kind in {"definition", "fact", "mechanism", "regulatory", "legal"}]
    if section_key == "core":
        return [finding for finding in findings if finding.claim_kind in {"mechanism", "definition"}]
    if section_key == "analysis":
        return [finding for finding in findings if finding.claim_kind in {"inference", "recommendation", "fact", "comparison"}]
    if section_key == "options":
        return [finding for finding in findings if finding.claim_kind in {"comparison", "mechanism", "fact"}]
    if section_key == "risks":
        return [finding for finding in findings if finding.failure_modes or finding.risk_level in {"medium", "high"}]
    if section_key == "findings":
        return [
            finding
            for finding in findings
            if finding.claim_kind in {"fact", "temporal", "numeric", "regulatory", "legal", "medical", "financial", "market"}
        ]
    if section_key == "decision_layer":
        return [finding for finding in findings if finding.decision_note or finding.claim_kind in {"advice", "recommendation"}]
    if section_key == "uncertainty":
        return [finding for finding in findings if finding.claim_kind == "absence" or finding.caveat or finding.required_fix]
    return list(findings)


def _fallback_pool(findings: list[SourceFinding]) -> list[SourceFinding]:
    return [finding for finding in findings if not finding.section_hint]
