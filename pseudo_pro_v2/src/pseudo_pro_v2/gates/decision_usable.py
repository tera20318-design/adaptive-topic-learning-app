from __future__ import annotations

from dataclasses import dataclass

from pseudo_pro_v2.catalogs import INTERNAL_HEADING_FRAGMENTS
from pseudo_pro_v2.models import ClaimLedgerRow, DomainAdapter, ReportDraft


@dataclass
class DecisionUsableRubricResult:
    direct_answer_present: bool
    scope_exclusions_present: bool
    uncertainty_present: bool
    reader_decision_layer_present: bool
    checklist_or_decision_table_present: bool
    next_action_or_next_research_present: bool
    no_internal_headings: bool
    no_unsupported_high_risk_in_mainline: bool
    comparison_tradeoff_ready: bool
    risk_disclosure_present: bool
    checklist_aligned_with_reader_task: bool
    specific_next_action_present: bool
    decision_layer_not_generic_filler: bool
    failures: list[str]

    @property
    def passed(self) -> bool:
        return not self.failures


def evaluate_decision_usable(draft: ReportDraft, claims: list[ClaimLedgerRow], adapter: DomainAdapter) -> DecisionUsableRubricResult:
    included_units = [unit for unit in draft.units if unit.include_in_report]
    included_claims = [claim for claim in claims if claim.included_in_report]
    by_section = {}
    for unit in included_units:
        by_section.setdefault(unit.section_key, []).append(unit)

    direct_answer_present = bool(by_section.get("direct_answer"))
    scope_exclusions_present = bool(by_section.get("scope"))
    uncertainty_present = bool(by_section.get("uncertainty"))
    reader_decision_layer_present = bool(by_section.get("decision_layer"))
    checklist_or_decision_table_present = bool(by_section.get("checklist"))
    next_action_or_next_research_present = _has_next_action_or_next_research(included_units, included_claims)
    no_internal_headings = not any(
        any(fragment in section.title.lower() for fragment in INTERNAL_HEADING_FRAGMENTS)
        for section in draft.sections
    )
    no_unsupported_high_risk_in_mainline = not any(
        claim.risk_level == "high" and claim.support_status != "supported"
        for claim in included_claims
    )
    comparison_tradeoff_ready = _comparison_tradeoff_ready(by_section, included_claims, adapter)
    risk_disclosure_present = _risk_disclosure_present(by_section, included_claims)
    checklist_aligned_with_reader_task = _checklist_aligned_with_reader_task(by_section, adapter)
    specific_next_action_present = _specific_next_action_present(by_section, adapter)
    decision_layer_not_generic_filler = _decision_layer_not_generic_filler(by_section, adapter)

    failures: list[str] = []
    if not direct_answer_present:
        failures.append("direct answer missing")
    if not scope_exclusions_present:
        failures.append("scope and exclusions missing")
    if not uncertainty_present:
        failures.append("uncertainty section missing")
    if not reader_decision_layer_present:
        failures.append("reader decision layer missing")
    if not checklist_or_decision_table_present:
        failures.append("checklist or decision table missing")
    if not next_action_or_next_research_present:
        failures.append("next action or next research missing")
    if not no_internal_headings:
        failures.append("internal headings present")
    if not no_unsupported_high_risk_in_mainline:
        failures.append("unsupported high-risk claim remains in mainline prose")
    if not comparison_tradeoff_ready:
        failures.append("comparison tradeoff structure is insufficient")
    if not risk_disclosure_present:
        failures.append("risk disclosure is insufficient for high-risk recommendations")
    if not checklist_aligned_with_reader_task:
        failures.append("checklist items do not align with the reader task")
    if not specific_next_action_present:
        failures.append("next action is not specific enough")
    if not decision_layer_not_generic_filler:
        failures.append("decision layer is generic filler")

    return DecisionUsableRubricResult(
        direct_answer_present=direct_answer_present,
        scope_exclusions_present=scope_exclusions_present,
        uncertainty_present=uncertainty_present,
        reader_decision_layer_present=reader_decision_layer_present,
        checklist_or_decision_table_present=checklist_or_decision_table_present,
        next_action_or_next_research_present=next_action_or_next_research_present,
        no_internal_headings=no_internal_headings,
        no_unsupported_high_risk_in_mainline=no_unsupported_high_risk_in_mainline,
        comparison_tradeoff_ready=comparison_tradeoff_ready,
        risk_disclosure_present=risk_disclosure_present,
        checklist_aligned_with_reader_task=checklist_aligned_with_reader_task,
        specific_next_action_present=specific_next_action_present,
        decision_layer_not_generic_filler=decision_layer_not_generic_filler,
        failures=failures,
    )


def _has_next_action_or_next_research(included_units, included_claims) -> bool:
    if any(claim.claim_kind in {"advice", "recommendation"} for claim in included_claims if claim.report_section == "Reader decision layer"):
        return True
    action_tokens = ("verify", "confirm", "check", "review", "research", "investigate", "next")
    return any(
        unit.section_key in {"decision_layer", "uncertainty", "checklist"}
        and any(token in unit.text.lower() for token in action_tokens)
        for unit in included_units
    )


def _comparison_tradeoff_ready(by_section, included_claims, adapter: DomainAdapter) -> bool:
    if "Options or comparison table" not in adapter.required_tables:
        return True
    option_claims = [claim for claim in included_claims if claim.report_section == "Main options/categories/mechanisms"]
    comparison_count = len([claim for claim in option_claims if claim.claim_kind == "comparison"])
    option_units = by_section.get("options", [])
    tradeoff_markers = ("but", "while", "however", "tradeoff", "trade-off", "at the cost of", "versus")
    has_tradeoff_language = any(marker in unit.text.lower() for unit in option_units for marker in tradeoff_markers)
    return len(option_claims) >= 2 and comparison_count >= 1 and has_tradeoff_language


def _risk_disclosure_present(by_section, included_claims) -> bool:
    high_risk_recommendations = [
        claim
        for claim in included_claims
        if claim.risk_level == "high" and claim.claim_kind in {"advice", "recommendation", "financial"}
    ]
    if not high_risk_recommendations:
        return True
    risk_units = by_section.get("risks", [])
    uncertainty_units = by_section.get("uncertainty", [])
    disclosure_tokens = ("risk", "uncertain", "limit", "verify", "wait", "disclosure", "constraint")
    return (
        bool(risk_units)
        and bool(uncertainty_units)
        and any(any(token in unit.text.lower() for token in disclosure_tokens) for unit in risk_units)
        and any(any(token in unit.text.lower() for token in disclosure_tokens) for unit in uncertainty_units)
    )


def _checklist_aligned_with_reader_task(by_section, adapter: DomainAdapter) -> bool:
    checklist_units = by_section.get("checklist", [])
    if not checklist_units:
        return False
    task_tokens = _content_tokens(
        " ".join(
            [adapter.use_context, adapter.decision_context.reader_action] + list(adapter.required_decision_layer)
        )
    )
    if not task_tokens:
        return True
    return any(_content_tokens(unit.text) & task_tokens for unit in checklist_units)


def _specific_next_action_present(by_section, adapter: DomainAdapter) -> bool:
    action_units = by_section.get("decision_layer", []) + by_section.get("uncertainty", []) + by_section.get("checklist", [])
    action_verbs = ("verify", "confirm", "check", "review", "compare", "escalate", "inspect", "wait", "ground", "trace")
    reference_tokens = _content_tokens(" ".join([adapter.use_context, adapter.decision_context.reader_action]))
    for unit in action_units:
        text = unit.text.lower()
        if not any(verb in text for verb in action_verbs):
            continue
        if not reference_tokens:
            return True
        if _content_tokens(unit.text) & reference_tokens:
            return True
    return False


def _decision_layer_not_generic_filler(by_section, adapter: DomainAdapter) -> bool:
    decision_units = by_section.get("decision_layer", [])
    if not decision_units:
        return False
    banned_phrases = (
        "summary only",
        "use judgment",
        "more research may help",
        "consider context",
        "reader-facing summary",
    )
    reference_tokens = _content_tokens(" ".join(adapter.required_decision_layer + [adapter.use_context, adapter.decision_context.reader_action]))
    for unit in decision_units:
        text = unit.text.lower()
        if any(phrase in text for phrase in banned_phrases):
            return False
        if reference_tokens and not (_content_tokens(unit.text) & reference_tokens):
            return False
    return True


def _content_tokens(text: str) -> set[str]:
    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "what",
        "still",
        "needs",
        "before",
        "after",
        "from",
        "into",
        "your",
        "their",
        "reader",
        "report",
        "action",
        "next",
        "should",
        "already",
        "safe",
        "say",
    }
    raw = "".join(char.lower() if char.isalnum() else " " for char in text)
    return {token for token in raw.split() if len(token) > 2 and token not in stopwords}
