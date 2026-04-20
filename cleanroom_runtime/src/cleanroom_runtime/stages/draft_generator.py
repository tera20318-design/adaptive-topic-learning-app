from __future__ import annotations

from collections import defaultdict

from cleanroom_runtime.models import BudgetPlan, CollectedEvidence, DomainAdapter, ReportDraft, ReportSectionPlan, ReportUnit, RunRequest
from cleanroom_runtime.utils import normalize_text


SECTION_HINT_TO_KEY = {
    "direct_answer": "direct_answer",
    "scope": "scope",
    "findings": "findings",
    "analysis": "analysis",
    "options": "options",
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
    units: list[ReportUnit] = []
    grouped = defaultdict(list)
    role_lookup = {source.source_id: source.source_role for source in evidence.sources}
    used_statement_keys: set[str] = set()
    unit_index = 1

    for finding in evidence.findings:
        section_key = SECTION_HINT_TO_KEY.get(finding.section_hint, _default_section(finding.claim_kind))
        statement_key = normalize_text(finding.statement)
        if statement_key in used_statement_keys:
            continue
        used_statement_keys.add(statement_key)
        grouped[section_key].append(finding)

    for section in section_plan:
        if section.key == "scope":
            for line in _scope_lines(request, adapter, evidence, budget):
                units.append(
                    ReportUnit(
                        unit_id=f"unit-{unit_index:03d}",
                        section_key=section.key,
                        section_title=section.title,
                        text=line,
                        claim_kind="scope_boundary",
                        risk_level="medium",
                        source_ids=[],
                        source_roles=[],
                        confidence=0.9,
                        is_claim=False,
                    )
                )
                unit_index += 1
            continue

        if section.key == "decision_layer":
            for line in adapter.required_decision_layer:
                units.append(
                    ReportUnit(
                        unit_id=f"unit-{unit_index:03d}",
                        section_key=section.key,
                        section_title=section.title,
                        text=line,
                        claim_kind="advice",
                        risk_level=adapter.risk_tier,
                        source_ids=[],
                        source_roles=[],
                        confidence=0.7,
                        is_claim=False,
                    )
                )
                unit_index += 1
            for line in _decision_action_lines(request, adapter):
                units.append(
                    ReportUnit(
                        unit_id=f"unit-{unit_index:03d}",
                        section_key=section.key,
                        section_title=section.title,
                        text=line,
                        claim_kind="advice",
                        risk_level=adapter.risk_tier,
                        source_ids=[],
                        source_roles=[],
                        confidence=0.7,
                        is_claim=False,
                    )
                )
                unit_index += 1
            continue

        if section.key == "checklist":
            for line in _checklist_lines(request, adapter, evidence):
                units.append(
                    ReportUnit(
                        unit_id=f"unit-{unit_index:03d}",
                        section_key=section.key,
                        section_title=section.title,
                        text=line,
                        claim_kind="advice",
                        risk_level=adapter.risk_tier,
                        source_ids=[],
                        source_roles=[],
                        confidence=0.7,
                        is_claim=False,
                    )
                )
                unit_index += 1
            continue

        if section.key == "uncertainty":
            for line in _uncertainty_lines(request, adapter, evidence, budget):
                units.append(
                    ReportUnit(
                        unit_id=f"unit-{unit_index:03d}",
                        section_key=section.key,
                        section_title=section.title,
                        text=line,
                        claim_kind="scope_boundary",
                        risk_level="medium",
                        source_ids=[],
                        source_roles=[],
                        confidence=0.9,
                        is_claim=False,
                    )
                )
                unit_index += 1
            for finding in grouped.get(section.key, [])[:3]:
                units.append(_unit_from_finding(unit_index, section, finding, role_lookup))
                unit_index += 1
            continue

        if section.key == "sources":
            for source in evidence.sources:
                units.append(
                    ReportUnit(
                        unit_id=f"unit-{unit_index:03d}",
                        section_key=section.key,
                        section_title=section.title,
                        text=f"{source.source_id}: {source.title} ({source.source_role})",
                        claim_kind="scope_boundary",
                        risk_level="low",
                        source_ids=[source.source_id],
                        source_roles=[source.source_role],
                        confidence=1.0,
                        is_claim=False,
                    )
                )
                unit_index += 1
            continue

        for finding in grouped.get(section.key, [])[:3]:
            units.append(_unit_from_finding(unit_index, section, finding, role_lookup))
            unit_index += 1

    return ReportDraft(title=adapter.topic, sections=section_plan, units=units)


def _unit_from_finding(index: int, section: ReportSectionPlan, finding, role_lookup: dict[str, str]) -> ReportUnit:
    return ReportUnit(
        unit_id=f"unit-{index:03d}",
        section_key=section.key,
        section_title=section.title,
        text=_render_finding_text(finding),
        claim_kind=finding.claim_kind,
        risk_level=finding.risk_level,
        source_ids=list(finding.source_ids),
        source_roles=[role_lookup.get(source_id, "unknown") for source_id in finding.source_ids],
        confidence=finding.confidence,
        finding_id=finding.finding_id,
        support_status_hint=finding.support_status_hint,
        caveat=finding.caveat,
        required_fix=finding.required_fix,
        contradiction_note=finding.contradiction_note,
        jurisdiction=finding.jurisdiction,
        absence_scope=finding.absence_scope,
        source_span_label=finding.source_span_label,
        source_span_start=finding.source_span_start,
        source_span_end=finding.source_span_end,
        source_span_labels=list(finding.source_span_labels),
        source_span_starts=list(finding.source_span_starts),
        source_span_ends=list(finding.source_span_ends),
        grounding_marker=finding.grounding_marker,
        grounding_scope_note=finding.grounding_scope_note or finding.scope_note,
        subject_key=finding.subject_key,
    )


def _render_finding_text(finding) -> str:
    if finding.claim_kind == "absence" and finding.absence_scope:
        scope_label = getattr(finding.absence_scope, "scope_label", "").strip()
        subject = getattr(finding.absence_scope, "subject", "").strip()
        if scope_label and subject:
            return f"Within the checked scope ({scope_label}), no evidence was found for {subject}."
        if subject:
            return f"The checked materials did not establish {subject} within the declared scope."
        return "The checked materials do not establish this absence claim safely enough for reader-facing prose."
    if finding.grounding_kind in {"direct_quote", "paraphrase"} and finding.source_excerpt:
        return f"The checked document states: {finding.source_excerpt}"
    return finding.statement


def _scope_lines(request: RunRequest, adapter: DomainAdapter, evidence: CollectedEvidence, budget: BudgetPlan) -> list[str]:
    lines = [
        f"This run is framed for: {adapter.use_context}.",
        f"The effective mode is `{budget.effective_mode}` and the evidence mode is `{budget.evidence_mode}`.",
        budget.report_status_implication,
        "Excluded from this run are unchecked jurisdictions, unchecked dates, and claims that still need stronger support.",
    ]
    if _is_document_review(request, evidence):
        titles = ", ".join(source.title for source in evidence.sources[:2])
        if titles:
            lines.append(f"Direct grounding is limited to the checked document set: {titles}.")
    lines.extend(adapter.known_limits[:2])
    return lines


def _decision_action_lines(request: RunRequest, adapter: DomainAdapter) -> list[str]:
    lines: list[str] = []
    task_tokens = _task_tokens(adapter.decision_context.reader_action, adapter.use_context, request.question)
    if adapter.decision_context.reader_action:
        lines.append(f"Next action: {adapter.decision_context.reader_action}.")
    if task_tokens:
        lines.append(f"Next research: verify the remaining support gap for {' '.join(task_tokens[:4])} before acting.")
    else:
        lines.append("Next research: verify the support gap that could still change the reader's decision.")
    return lines


def _checklist_lines(request: RunRequest, adapter: DomainAdapter, evidence: CollectedEvidence) -> list[str]:
    task_tokens = _task_tokens(adapter.decision_context.reader_action, adapter.use_context, request.question)
    lines = []
    if task_tokens:
        lines.append(f"Check whether the current packet is sufficient to support {' '.join(task_tokens[:4])}.")
    lines.extend(
        [
            "Verify claim-kind source-role fit before acting on any high-risk statement.",
            "Check whether any absence statement is scoped rather than global.",
            "Treat synthetic validation as contract proof only, not research completeness.",
        ]
    )
    if "Options or comparison table" in adapter.required_tables:
        lines.append("Confirm that compared options use explicit tradeoff language and like-for-like source roles.")
    if _is_document_review(request, evidence):
        lines.append("Confirm that every recommendation is grounded in the checked document text before inferring anything beyond it.")
    return lines


def _uncertainty_lines(request: RunRequest, adapter: DomainAdapter, evidence: CollectedEvidence, budget: BudgetPlan) -> list[str]:
    lines = [
        "Uncertainty remains wherever the checked materials do not establish exhaustive coverage outside the declared scope, date window, or jurisdiction.",
        "Do not treat this report as permission to ignore later evidence, changed conditions, or unverified edge cases that would change the stated answer.",
    ]
    if request.question:
        lines.append(f"Uncertainty remains specific to this question: {request.question}")
    if _is_document_review(request, evidence):
        lines.append("Any conclusion that goes beyond the checked document text still needs external verification.")
    lines.extend(list(dict.fromkeys([*budget.limitations, *adapter.known_limits])))
    return list(dict.fromkeys(lines))


def _is_document_review(request: RunRequest, evidence: CollectedEvidence) -> bool:
    if any(source.source_role == "user_provided_source" for source in evidence.sources):
        return True
    haystack = normalize_text(" ".join([request.topic, request.use_context, request.question, request.desired_depth]))
    return any(token in haystack for token in ("document", "memo", "draft", "review"))


def _task_tokens(*values: str) -> list[str]:
    stopwords = {
        "the",
        "and",
        "with",
        "that",
        "from",
        "this",
        "what",
        "does",
        "still",
        "need",
        "needs",
        "reader",
        "before",
        "acting",
        "report",
        "checked",
        "current",
        "should",
        "would",
    }
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        for token in normalize_text(value).split():
            if len(token) < 4 or token in stopwords or token.isdigit():
                continue
            if token not in seen:
                ordered.append(token)
                seen.add(token)
    return ordered


def _default_section(claim_kind: str) -> str:
    mapping = {
        "definition": "direct_answer",
        "fact": "findings",
        "mechanism": "analysis",
        "temporal": "findings",
        "numeric": "findings",
        "comparison": "options",
        "recommendation": "decision_layer",
        "advice": "decision_layer",
        "inference": "analysis",
        "absence": "uncertainty",
        "scope_boundary": "scope",
    }
    return mapping.get(claim_kind, "analysis")
