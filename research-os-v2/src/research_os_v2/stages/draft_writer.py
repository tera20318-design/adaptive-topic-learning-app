from __future__ import annotations

from collections import defaultdict

from research_os_v2.models import (
    CollectedEvidence,
    DomainAdapter,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    ResearchRequest,
)


SECTION_HINT_TO_KEY = {
    "direct_answer": "direct_answer",
    "scope": "scope",
    "core_explanation": "core",
    "decision_analysis": "analysis",
    "options": "options",
    "risks": "risks",
    "evidence_findings": "findings",
    "decision_layer": "decision_layer",
    "checklist": "checklist",
    "uncertainty": "uncertainty",
}


def write_initial_draft(
    request: ResearchRequest,
    adapter: DomainAdapter,
    evidence: CollectedEvidence,
    section_plan: list[ReportSectionPlan],
) -> ReportDraft:
    units: list[ReportUnit] = []
    index = 1

    by_section = defaultdict(list)
    for finding in evidence.findings:
        key = SECTION_HINT_TO_KEY.get(finding.section_hint, _default_section_for_claim_kind(finding.claim_kind))
        by_section[key].append(finding)

    source_role_lookup = {source.source_id: source.source_role for source in evidence.sources}

    for section in section_plan:
        if section.key == "scope":
            units.extend(_scope_units(request, section, index))
            index += len([unit for unit in units if unit.section_key == section.key])
            continue
        if section.key == "sources":
            units.extend(_source_units(evidence, section, index))
            index += len([unit for unit in units if unit.section_key == section.key])
            continue
        if section.key == "checklist":
            units.extend(_checklist_units(by_section["decision_layer"] or evidence.findings[:3], section, index, source_role_lookup))
            index += len([unit for unit in units if unit.section_key == section.key])
            continue
        if section.key == "uncertainty":
            units.extend(_uncertainty_units(adapter, by_section[section.key], section, index, source_role_lookup))
            index += len([unit for unit in units if unit.section_key == section.key])
            continue

        findings = by_section[section.key] or _fallback_findings(section.key, evidence)
        for finding in findings[:3]:
            units.append(
                ReportUnit(
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
                    jurisdiction=finding.jurisdiction,
                    contradiction_note=finding.contradiction_note,
                    caveat=finding.caveat,
                    required_fix=finding.required_fix,
                )
            )
            index += 1

    markdown = _render_markdown(request.topic, section_plan, units)
    return ReportDraft(
        title=request.topic,
        sections=section_plan,
        units=units,
        markdown=markdown,
    )


def _default_section_for_claim_kind(claim_kind: str) -> str:
    mapping = {
        "definition": "core",
        "mechanism": "core",
        "fact": "findings",
        "comparison": "options",
        "advice": "decision_layer",
        "recommendation": "decision_layer",
        "inference": "analysis",
        "absence": "uncertainty",
        "scope_boundary": "scope",
    }
    return mapping.get(claim_kind, "analysis")


def _fallback_findings(section_key: str, evidence: CollectedEvidence):
    if section_key == "direct_answer":
        return sorted(evidence.findings, key=lambda finding: (finding.risk_level != "high", finding.claim_kind != "fact"))
    if section_key == "risks":
        return [finding for finding in evidence.findings if finding.failure_modes or finding.risk_tags]
    if section_key == "options":
        return [finding for finding in evidence.findings if finding.claim_kind in {"comparison", "fact", "mechanism"}]
    if section_key == "analysis":
        return [finding for finding in evidence.findings if finding.claim_kind in {"advice", "inference", "comparison", "fact"}]
    if section_key == "decision_layer":
        return [finding for finding in evidence.findings if finding.decision_note or finding.claim_kind in {"advice", "recommendation"}]
    return evidence.findings


def _scope_units(request: ResearchRequest, section: ReportSectionPlan, start_index: int) -> list[ReportUnit]:
    lines = [
        f"This run addresses {request.topic} for {request.reader}.",
        f"It is intended to support: {request.use_context}.",
        f"The requested mode is `{request.requested_mode}` and the analysis keeps that scope explicit.",
    ]
    if request.jurisdiction:
        lines.append(f"Jurisdiction-sensitive points are framed around {request.jurisdiction}.")
    return [
        ReportUnit(
            unit_id=f"unit-{start_index + offset:03d}",
            section_key=section.key,
            section_title=section.title,
            text=line,
            claim_kind="scope_boundary",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            support_status_hint="supported",
        )
        for offset, line in enumerate(lines)
    ]


def _source_units(
    evidence: CollectedEvidence,
    section: ReportSectionPlan,
    start_index: int,
) -> list[ReportUnit]:
    units: list[ReportUnit] = []
    for offset, source in enumerate(evidence.sources):
        citation = source.citation or source.url or source.title
        units.append(
            ReportUnit(
                unit_id=f"unit-{start_index + offset:03d}",
                section_key=section.key,
                section_title=section.title,
                text=f"{source.source_id}: {source.title} ({source.source_role}; {citation})",
                claim_kind="scope_boundary",
                risk_level="low",
                source_ids=[source.source_id],
                source_roles=[source.source_role],
                confidence=1.0,
                support_status_hint="supported",
            )
        )
    return units


def _checklist_units(findings, section: ReportSectionPlan, start_index: int, source_role_lookup: dict[str, str]) -> list[ReportUnit]:
    units: list[ReportUnit] = []
    for offset, finding in enumerate(findings[:4]):
        note = finding.decision_note or finding.statement
        units.append(
            ReportUnit(
                unit_id=f"unit-{start_index + offset:03d}",
                section_key=section.key,
                section_title=section.title,
                text=f"Check: {note}",
                claim_kind="advice",
                risk_level=finding.risk_level,
                source_ids=finding.source_ids,
                source_roles=[source_role_lookup.get(source_id, "unknown") for source_id in finding.source_ids],
                confidence=finding.confidence,
                support_status_hint=finding.support_status_hint,
                absence_type=finding.absence_type,
                jurisdiction=finding.jurisdiction,
                contradiction_note=finding.contradiction_note,
                caveat=finding.caveat,
            )
        )
    return units


def _uncertainty_units(
    adapter: DomainAdapter,
    section_findings,
    section: ReportSectionPlan,
    start_index: int,
    source_role_lookup: dict[str, str],
) -> list[ReportUnit]:
    units: list[ReportUnit] = []
    seed_findings = section_findings[:3]
    if not seed_findings:
        seed_findings = []
    for offset, finding in enumerate(seed_findings):
        units.append(
            ReportUnit(
                unit_id=f"unit-{start_index + offset:03d}",
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
                jurisdiction=finding.jurisdiction,
                contradiction_note=finding.contradiction_note,
                caveat=finding.caveat,
                required_fix=finding.required_fix,
            )
        )
    for extra_index, limit in enumerate(adapter.known_limits[:2], start=len(units)):
        units.append(
            ReportUnit(
                unit_id=f"unit-{start_index + extra_index:03d}",
                section_key=section.key,
                section_title=section.title,
                text=limit,
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.8,
                support_status_hint="supported",
            )
        )
    return units


def _render_markdown(title: str, sections: list[ReportSectionPlan], units: list[ReportUnit]) -> str:
    lines = [f"# {title}", ""]
    for section in sections:
        lines.append(f"## {section.title}")
        lines.append("")
        for unit in [item for item in units if item.section_key == section.key]:
            citation_text = ""
            if unit.source_ids:
                citation_text = " " + " ".join(f"[{source_id}]" for source_id in unit.source_ids)
            lines.append(f"- {unit.text}{citation_text}")
        if not any(item.section_key == section.key for item in units):
            lines.append("- No supported material was available for this section.")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
