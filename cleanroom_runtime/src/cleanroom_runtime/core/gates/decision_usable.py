from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re

from cleanroom_runtime.catalogs import AUTHORITATIVE_SOURCE_ROLES, INTERNAL_HEADING_FRAGMENTS, SEARCH_SCOPED_ABSENCE_TYPES
from cleanroom_runtime.models import (
    BudgetPlan,
    CitationLedgerRow,
    ClaimLedgerRow,
    DomainAdapter,
    IntentResult,
    MetricsSnapshot,
    ReportDraft,
    ReportUnit,
    RiskTierResult,
    RunRequest,
)
from cleanroom_runtime.utils import normalize_text

_EXCLUSION_MARKERS = (
    "exclude",
    "excluded",
    "does not cover",
    "does not establish",
    "not covered",
    "outside this run",
    "outside the checked scope",
    "bounded to",
    "limited to",
    "within the checked scope",
)
_TRADEOFF_MARKERS = (
    "tradeoff",
    "tradeoffs",
    "advantage",
    "advantages",
    "limitation",
    "limitations",
    "upside",
    "downside",
    "pros",
    "cons",
    "cost",
    "costs",
)
_GENERIC_UNCERTAINTY_MARKERS = (
    "more research is needed",
    "further research is needed",
    "this may change",
    "context matters",
    "history is complex",
    "culture is nuanced",
    "interpretations vary",
    "results may vary",
    "there may be limitations",
    "uncertainty remains",
    "additional verification may still be useful",
)
_SPECIFIC_UNCERTAINTY_MARKERS = (
    "checked",
    "scope",
    "source",
    "sources",
    "citation",
    "citations",
    "document",
    "packet",
    "record",
    "jurisdiction",
    "date",
    "timeframe",
    "support",
    "evidence",
    "claim",
    "outside the declared scope",
    "within the checked scope",
    "matched",
    "official",
)
_DOCUMENT_REVIEW_MARKERS = (
    "document review",
    "review the document",
    "review the packet",
    "review the record",
    "review the memo",
    "review the contract",
    "document packet",
    "review the text",
    "uploaded draft",
    "checked document",
)
_GROUNDING_MARKERS = (
    "the checked material",
    "the checked materials",
    "the reviewed document",
    "the reviewed packet",
    "the reviewed record",
    "the packet states",
    "the document states",
    "the record states",
    "the text states",
    "the cited source",
    "the cited sources",
    "the checked document",
    "the checked packet",
    "the checked document set",
    "direct grounding",
    "grounded in the checked document",
)
_GENERIC_ACTION_PHRASES = (
    "do more research",
    "continue research",
    "follow up later",
    "check later",
    "look into it",
    "review more",
    "investigate further",
    "as needed",
)
_ACTION_MARKERS = (
    "next action",
    "next research",
    "next step",
    "follow up",
    "follow-up",
    "verify",
    "check",
    "review",
    "compare",
    "confirm",
    "trace",
    "ground",
)
_RISK_DISCLOSURE_MARKERS = (
    "risk disclosure",
    "downside",
    "loss",
    "lose",
    "volatility",
    "not guaranteed",
    "suitability",
    "risk",
    "tradeoff",
    "tradeoffs",
)
_SPECIFIC_ACTION_OBJECT_MARKERS = (
    "claim",
    "claims",
    "citation",
    "citations",
    "source",
    "sources",
    "scope",
    "packet",
    "document",
    "record",
    "support",
    "tradeoff",
    "tradeoffs",
    "downside",
    "jurisdiction",
    "date",
    "decision",
)
_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "before",
        "by",
        "can",
        "for",
        "from",
        "how",
        "if",
        "in",
        "into",
        "is",
        "it",
        "now",
        "of",
        "on",
        "or",
        "still",
        "that",
        "the",
        "their",
        "them",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "to",
        "up",
        "use",
        "what",
        "when",
        "which",
        "while",
        "with",
        "reader",
        "support",
    }
)


@dataclass(slots=True)
class DecisionUsableFinding:
    code: str
    message: str
    required_fix: str
    severity: str
    blocks_release: bool = False
    claim_id: str = ""


@dataclass(slots=True)
class DecisionUsableResult:
    decision_usable: bool
    checks: dict[str, bool]
    failed_checks: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    findings: list[DecisionUsableFinding] = field(default_factory=list)
    revision_reasons: list[str] = field(default_factory=list)
    blocking_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def assess_decision_usable(
    draft: ReportDraft,
    claims: list[ClaimLedgerRow],
    citations: list[CitationLedgerRow] | None = None,
    *,
    adapter: DomainAdapter | None = None,
    budget: BudgetPlan | None = None,
    metrics: MetricsSnapshot | None = None,
    risk: RiskTierResult | None = None,
    request: RunRequest | None = None,
    intent: IntentResult | None = None,
) -> DecisionUsableResult:
    del budget
    del metrics
    citations = citations or []
    included_units = [unit for unit in draft.units if unit.include_in_report]
    included_claims = [claim for claim in claims if claim.included_in_report]
    checklist_units = [unit for unit in included_units if unit.section_key == "checklist"]
    high_stakes_domains = set(risk.high_stakes_domains) if risk is not None else set()
    substantive_uncertainty = _has_non_generic_uncertainty(included_units, citations, adapter, request)

    checks = {
        "direct_answer_present": _section_has_content(included_units, "direct_answer"),
        "scope_and_exclusions_present": _has_scope_and_exclusions(included_units),
        "uncertainty_present": substantive_uncertainty,
        "non_generic_uncertainty_present": substantive_uncertainty,
        "reader_decision_layer_present": _section_has_content(included_units, "decision_layer"),
        "checklist_or_decision_table_present": _section_has_content(included_units, "checklist") or _has_tradeoff_table(included_units),
        "checklist_aligned_to_reader_task": _checklist_aligns_with_reader_task(checklist_units, adapter, request, intent),
        "next_action_or_next_research_present": _has_next_action_or_research(included_units),
        "specific_next_action_present": _has_specific_next_action(included_units, adapter, request),
        "no_internal_pipeline_headings": not _has_internal_heading_leak(draft, included_units),
        "no_unsupported_high_risk_claim_in_mainline": not _has_unsupported_high_risk_mainline(included_claims),
        "explicit_tradeoff_language_present": _tradeoff_language_sufficient(included_units, adapter, included_claims, intent),
        "visible_risk_disclosure_present": _risk_disclosure_sufficient(included_units, included_claims),
        "direct_document_grounding_present": _document_grounding_sufficient(included_units, citations, adapter, request, intent),
    }
    failed = [name for name, passed in checks.items() if not passed]
    findings = _findings_from_failed_checks(failed)

    if checklist_units and not _checklist_aligns_with_reader_task(checklist_units, adapter, request, intent):
        findings.append(
            DecisionUsableFinding(
                code="checklist_not_aligned_to_reader_task",
                message="Decision-usable rubric failed: checklist items do not align with the reader task.",
                required_fix="Align checklist items with the reader task so the reader can act on the same decision frame.",
                severity="medium",
            )
        )

    if _document_review_needed(adapter, request, intent, citations) and not _document_grounding_sufficient(included_units, citations, adapter, request, intent):
        findings.append(
            DecisionUsableFinding(
                code="document_review_without_grounding",
                message="Decision-usable rubric failed: document review output lacks direct grounding statements.",
                required_fix="State what the checked document, packet, or cited text says before moving into synthesis.",
                severity="medium",
            )
        )

    if _comparison_requires_tradeoff_table(adapter, included_claims, included_units) and not _has_tradeoff_table(included_units):
        findings.append(
            DecisionUsableFinding(
                code="missing_tradeoff_table",
                message="Comparison-style output is missing a reader-facing tradeoff table.",
                required_fix="Add a like-for-like tradeoff table that names the compared options, differences, and decision implications.",
                severity="medium",
            )
        )

    for claim in included_claims:
        authoritative_roles = _claim_authoritative_roles(claim, citations)
        if _needs_medical_authority(claim, high_stakes_domains) and not authoritative_roles:
            findings.append(
                DecisionUsableFinding(
                    code="medical_without_authoritative_support",
                    message="Reader-facing health guidance lacks authoritative support.",
                    required_fix="Add authoritative medical support or move the guidance out of mainline prose.",
                    severity="high",
                    blocks_release=True,
                    claim_id=claim.claim_id,
                )
            )
        if _needs_visible_risk_disclosure(claim, high_stakes_domains) and not _has_risk_disclosure(included_units):
            finance = _needs_finance_risk_disclosure(claim, high_stakes_domains)
            findings.append(
                DecisionUsableFinding(
                    code="financial_without_risk_disclosure" if finance else "guidance_without_risk_disclosure",
                    message=(
                        "Reader-facing finance recommendation lacks visible risk disclosure."
                        if finance
                        else "Reader-facing guidance lacks visible risk disclosure."
                    ),
                    required_fix=(
                        "Add reader-facing downside, suitability, and uncertainty disclosure next to the recommendation."
                        if finance
                        else "Add visible downside, uncertainty, or decision-risk disclosure next to the guidance."
                    ),
                    severity="high" if finance and claim.risk_level == "high" else "medium",
                    blocks_release=finance and claim.risk_level == "high",
                    claim_id=claim.claim_id,
                )
            )
        if claim.claim_kind == "absence" and claim.risk_level == "high" and _absence_basis(claim) in SEARCH_SCOPED_ABSENCE_TYPES:
            findings.append(
                DecisionUsableFinding(
                    code="scoped_search_absence_in_mainline",
                    message="A high-risk scoped-search absence claim remains in mainline prose.",
                    required_fix="Keep scoped-search absence in uncertainty or replace it with checked authoritative source support.",
                    severity="high",
                    blocks_release=True,
                    claim_id=claim.claim_id,
                )
            )

    findings = _dedupe_findings(findings)
    notes = [finding.message for finding in findings]
    revision_reasons = [finding.message for finding in findings if not finding.blocks_release]
    blocking_reasons = [finding.message for finding in findings if finding.blocks_release]
    return DecisionUsableResult(
        decision_usable=not findings,
        checks=checks,
        failed_checks=failed,
        notes=notes,
        findings=findings,
        revision_reasons=revision_reasons,
        blocking_reasons=blocking_reasons,
    )


def _section_has_content(units: list[ReportUnit], section_key: str) -> bool:
    return any(unit.section_key == section_key and unit.text.strip() for unit in units)


def _has_scope_and_exclusions(units: list[ReportUnit]) -> bool:
    scope_units = [unit for unit in units if unit.section_key == "scope"]
    if not scope_units:
        return False
    return any(any(marker in normalize_text(unit.text) for marker in _EXCLUSION_MARKERS) for unit in scope_units)


def _has_non_generic_uncertainty(
    units: list[ReportUnit],
    citations: list[CitationLedgerRow],
    adapter: DomainAdapter | None,
    request: RunRequest | None,
) -> bool:
    uncertainty_units = [unit for unit in units if unit.section_key == "uncertainty" and unit.text.strip()]
    if not uncertainty_units:
        return False
    specific_tokens = set(
        _meaningful_tokens(
            " ".join(
                [
                    *(citation.source_title for citation in citations),
                    adapter.use_context if adapter is not None else "",
                    request.question if request is not None else "",
                ]
            )
        )
    )
    return any(_is_non_generic_uncertainty_text(unit.text, specific_tokens) for unit in uncertainty_units)


def _is_non_generic_uncertainty_text(text: str, specific_tokens: set[str]) -> bool:
    lowered = normalize_text(text)
    if any(token in lowered for token in specific_tokens):
        return True
    if any(marker in lowered for marker in _SPECIFIC_UNCERTAINTY_MARKERS):
        return True
    if any(marker in lowered for marker in _GENERIC_UNCERTAINTY_MARKERS):
        return False
    tokens = _meaningful_tokens(lowered)
    return len(tokens) >= 6 and any(token in {"scope", "source", "support", "evidence", "claim", "document", "packet"} for token in tokens)


def _has_next_action_or_research(units: list[ReportUnit]) -> bool:
    action_sections = {"decision_layer", "checklist", "uncertainty"}
    for unit in units:
        if unit.section_key not in action_sections:
            continue
        if _contains_next_step_marker(unit.text) and _is_specific_action_line(unit.text):
            return True
    return False


def _is_specific_action_line(text: str) -> bool:
    lowered = normalize_text(text)
    if not any(marker in lowered for marker in _ACTION_MARKERS):
        return False
    if any(phrase in lowered for phrase in _GENERIC_ACTION_PHRASES):
        return False
    tokens = _meaningful_tokens(lowered)
    if len(tokens) < 4:
        return False
    if any(marker in lowered for marker in _SPECIFIC_ACTION_OBJECT_MARKERS):
        return True
    return any(token in {"whether", "which", "against", "within", "before"} for token in lowered.split())


def _contains_next_step_marker(text: str) -> bool:
    lowered = normalize_text(text)
    return any(marker in lowered for marker in ("next action", "next research", "next step", "follow up", "follow-up"))


def _checklist_aligns_with_reader_task(
    checklist_units: list[ReportUnit],
    adapter: DomainAdapter | None,
    request: RunRequest | None,
    intent: IntentResult | None,
) -> bool:
    if not checklist_units:
        return True
    reader_task = normalize_text(
        " ".join(
            [
                adapter.decision_context.reader_action if adapter is not None else "",
                adapter.decision_context.primary_decision if adapter is not None else "",
                intent.reader_task if intent is not None else "",
                request.question if request is not None else "",
                request.use_context if request is not None else "",
            ]
        )
    )
    task_tokens = set(_meaningful_tokens(reader_task))
    if not task_tokens:
        return True
    return any(_line_aligns_with_tokens(unit.text, task_tokens) for unit in checklist_units)


def _line_aligns_with_tokens(text: str, task_tokens: set[str]) -> bool:
    line_tokens = set(_meaningful_tokens(text))
    if line_tokens & task_tokens:
        return True
    text_lower = normalize_text(text)
    return any(
        token.startswith(stem) or stem.startswith(token)
        for token in line_tokens
        for stem in task_tokens
        if len(token) >= 4 and len(stem) >= 4
    ) or ("tradeoff" in text_lower and any(token.startswith("tradeoff") for token in task_tokens))


def _has_internal_heading_leak(draft: ReportDraft, units: list[ReportUnit]) -> bool:
    titles = [section.title for section in draft.sections]
    text_pool = [*titles, *(unit.section_title for unit in units)]
    for value in text_pool:
        lowered = value.casefold()
        if any(fragment in lowered for fragment in INTERNAL_HEADING_FRAGMENTS):
            return True
    return False


def _has_unsupported_high_risk_mainline(claims: list[ClaimLedgerRow]) -> bool:
    return any(claim.risk_level == "high" and claim.support_status not in {"supported", "scoped_absence"} for claim in claims)


def _has_specific_next_action(units: list[ReportUnit], adapter: DomainAdapter | None, request: RunRequest | None) -> bool:
    task_tokens = set(
        _meaningful_tokens(
            " ".join(
                [
                    getattr(adapter.decision_context, "reader_action", "") if adapter is not None else "",
                    request.question if request is not None else "",
                ]
            )
        )
    )
    for unit in units:
        if unit.section_key not in {"decision_layer", "checklist", "uncertainty"}:
            continue
        normalized = normalize_text(unit.text)
        if not _contains_next_step_marker(normalized):
            continue
        if not _is_specific_action_line(unit.text):
            continue
        if not task_tokens or any(token in normalized for token in task_tokens):
            return True
    return False


def _comparison_requires_tradeoff_table(
    adapter: DomainAdapter | None,
    claims: list[ClaimLedgerRow],
    units: list[ReportUnit],
) -> bool:
    if adapter is not None and "Options or comparison table" in adapter.required_tables:
        return True
    if any(claim.claim_kind == "comparison" for claim in claims):
        return True
    return any(unit.section_key == "options" for unit in units)


def _tradeoff_language_sufficient(
    units: list[ReportUnit],
    adapter: DomainAdapter | None,
    claims: list[ClaimLedgerRow],
    intent: IntentResult | None,
) -> bool:
    if not _comparison_requires_tradeoff_table(adapter, claims, units) and not (
        intent is not None and intent.intent_label == "comparison_report"
    ):
        return True
    return _has_tradeoff_table(units) or any(
        unit.section_key in {"options", "analysis", "decision_layer"} and any(marker in normalize_text(unit.text) for marker in _TRADEOFF_MARKERS)
        for unit in units
    )


def _has_tradeoff_table(units: list[ReportUnit]) -> bool:
    option_units = [unit for unit in units if unit.section_key == "options"]
    if len(option_units) < 2:
        return False
    table_like = [normalize_text(unit.text) for unit in option_units if unit.text.count("|") >= 2]
    if len(table_like) < 2:
        return False
    joined = " ".join(table_like)
    return any(marker in joined for marker in _TRADEOFF_MARKERS)


def _document_review_needed(
    adapter: DomainAdapter | None,
    request: RunRequest | None,
    intent: IntentResult | None,
    citations: list[CitationLedgerRow],
) -> bool:
    if intent is not None and intent.intent_label == "document_review":
        return True
    if any(citation.source_role == "user_provided_source" for citation in citations):
        return True
    if adapter is not None and _needs_document_review_grounding(adapter):
        return True
    if request is None:
        return False
    haystack = normalize_text(" ".join([request.topic, request.use_context, request.question, request.desired_depth]))
    return any(marker in haystack for marker in ("document", "memo", "draft", "review"))


def _document_grounding_sufficient(
    units: list[ReportUnit],
    citations: list[CitationLedgerRow],
    adapter: DomainAdapter | None,
    request: RunRequest | None,
    intent: IntentResult | None,
) -> bool:
    if not _document_review_needed(adapter, request, intent, citations):
        return True
    title_tokens = set(
        _meaningful_tokens(
            " ".join(
                citation.source_title
                for citation in citations
                if citation.source_role == "user_provided_source"
            )
        )
    )
    if not title_tokens:
        title_tokens = set(_meaningful_tokens(" ".join(citation.source_title for citation in citations)))
    return _has_direct_grounding(units, title_tokens)


def _has_direct_grounding(units: list[ReportUnit], title_tokens: set[str]) -> bool:
    grounding_units = [unit for unit in units if unit.section_key in {"direct_answer", "scope", "findings"}]
    for unit in grounding_units:
        normalized = normalize_text(unit.text)
        if any(marker in normalized for marker in _GROUNDING_MARKERS):
            return True
        if title_tokens and any(token in normalized for token in title_tokens):
            return True
    return False


def _claim_authoritative_roles(claim: ClaimLedgerRow, citations: list[CitationLedgerRow]) -> set[str]:
    roles = set(claim.matched_source_roles) & AUTHORITATIVE_SOURCE_ROLES
    for citation in citations:
        if citation.claim_id == claim.claim_id and citation.included_in_report and citation.source_role in AUTHORITATIVE_SOURCE_ROLES:
            roles.add(citation.source_role)
    return roles


def _risk_disclosure_sufficient(units: list[ReportUnit], claims: list[ClaimLedgerRow]) -> bool:
    if not any(claim.claim_kind in {"advice", "recommendation", "financial"} for claim in claims):
        return True
    return _has_risk_disclosure(units)


def _has_risk_disclosure(units: list[ReportUnit]) -> bool:
    for unit in units:
        lowered = normalize_text(unit.text)
        if any(marker in lowered for marker in ("risk disclosure", "downside", "loss", "lose", "volatility", "not guaranteed", "suitability")):
            return True
        if "risk" in lowered and "high-risk" not in lowered and any(marker in lowered for marker in ("tradeoff", "tradeoffs", "constraint", "constraints", "tolerance")):
            return True
    return False


def _absence_basis(claim: ClaimLedgerRow) -> str:
    if claim.absence_scope is None:
        return ""
    return getattr(claim.absence_scope, "basis", "")


def _needs_medical_authority(claim: ClaimLedgerRow, high_stakes_domains: set[str]) -> bool:
    if claim.claim_kind == "medical":
        return True
    return "medical" in high_stakes_domains and claim.claim_kind in {"advice", "recommendation"}


def _needs_visible_risk_disclosure(claim: ClaimLedgerRow, high_stakes_domains: set[str]) -> bool:
    if claim.claim_kind in {"advice", "recommendation"}:
        return True
    return _needs_finance_risk_disclosure(claim, high_stakes_domains)


def _needs_finance_risk_disclosure(claim: ClaimLedgerRow, high_stakes_domains: set[str]) -> bool:
    if claim.claim_kind == "financial":
        return True
    return "financial" in high_stakes_domains and claim.claim_kind in {"advice", "recommendation"}


def _needs_document_review_grounding(adapter: DomainAdapter) -> bool:
    haystack = normalize_text(" ".join([adapter.topic, adapter.use_context, adapter.decision_context.primary_decision, adapter.decision_context.reader_action]))
    return any(marker in haystack for marker in _DOCUMENT_REVIEW_MARKERS)


def _meaningful_tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", normalize_text(text))
        if len(token) >= 4 and token not in _STOPWORDS
    ]


def _findings_from_failed_checks(failed_checks: list[str]) -> list[DecisionUsableFinding]:
    mapping = {
        "direct_answer_present": (
            "Decision-usable rubric failed: the draft does not start with a bounded direct answer.",
            "Add a direct answer that states the supported answer before the supporting detail.",
            "medium",
            False,
        ),
        "scope_and_exclusions_present": (
            "Decision-usable rubric failed: the draft does not make scope and exclusions explicit.",
            "State what was checked, what was excluded, and how the scope bounds the answer.",
            "medium",
            False,
        ),
        "uncertainty_present": (
            "Decision-usable rubric failed: the draft does not keep uncertainty visible.",
            "Add a dedicated uncertainty section that keeps limitations and unresolved questions visible.",
            "medium",
            False,
        ),
        "non_generic_uncertainty_present": (
            "Decision-usable rubric failed: uncertainty is too generic to guide the reader.",
            "Tie uncertainty to the checked scope, packet, date window, document, or unresolved question.",
            "medium",
            False,
        ),
        "reader_decision_layer_present": (
            "Decision-usable rubric failed: the draft is missing a reader decision layer.",
            "Add a section that tells the reader what still matters before acting.",
            "medium",
            False,
        ),
        "checklist_or_decision_table_present": (
            "Decision-usable rubric failed: the draft lacks a checklist or decision table.",
            "Add a checklist or decision table the reader can use directly.",
            "medium",
            False,
        ),
        "checklist_aligned_to_reader_task": (
            "Decision-usable rubric failed: checklist items are not aligned with the reader task.",
            "Rewrite the checklist so it directly tests the reader task or decision frame.",
            "medium",
            False,
        ),
        "next_action_or_next_research_present": (
            "Decision-usable rubric failed: the draft does not tell the reader what to do or research next.",
            "Add an explicit next action or next research step.",
            "medium",
            False,
        ),
        "specific_next_action_present": (
            "Decision-usable rubric failed: the next action is too generic to guide the reader.",
            "State a concrete next action tied to the reader task, missing support, or checked document.",
            "medium",
            False,
        ),
        "no_internal_pipeline_headings": (
            "Decision-usable rubric failed: the draft uses internal pipeline headings instead of reader-facing headings.",
            "Rename headings so they stay reader-facing and decision-usable.",
            "medium",
            False,
        ),
        "no_unsupported_high_risk_claim_in_mainline": (
            "Decision-usable rubric failed: unsupported high-risk claims remain in mainline prose.",
            "Remove or repair unsupported high-risk claims before release.",
            "high",
            True,
        ),
        "explicit_tradeoff_language_present": (
            "Decision-usable rubric failed: comparison output does not name the tradeoffs explicitly.",
            "Use explicit tradeoff language such as advantage, limitation, cost, downside, or tradeoff.",
            "medium",
            False,
        ),
        "visible_risk_disclosure_present": (
            "Decision-usable rubric failed: recommendation-oriented output lacks visible risk disclosure.",
            "Add visible downside, suitability, or uncertainty disclosure next to the recommendation.",
            "medium",
            False,
        ),
        "direct_document_grounding_present": (
            "Decision-usable rubric failed: document review output is not directly grounded in the checked document.",
            "State which checked document or document set grounds the answer before moving into synthesis.",
            "medium",
            False,
        ),
    }
    findings: list[DecisionUsableFinding] = []
    for code in failed_checks:
        message, required_fix, severity, blocks_release = mapping[code]
        findings.append(
            DecisionUsableFinding(
                code=code,
                message=message,
                required_fix=required_fix,
                severity=severity,
                blocks_release=blocks_release,
            )
        )
    return findings


def _dedupe_findings(findings: list[DecisionUsableFinding]) -> list[DecisionUsableFinding]:
    ordered: list[DecisionUsableFinding] = []
    seen: set[tuple[str, str]] = set()
    for finding in findings:
        key = (finding.code, finding.claim_id)
        if key in seen:
            continue
        seen.add(key)
        ordered.append(finding)
    return ordered
