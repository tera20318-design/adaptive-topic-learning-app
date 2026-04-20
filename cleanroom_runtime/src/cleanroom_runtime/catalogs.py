from __future__ import annotations

from types import MappingProxyType


def _frozen_budget(**entries: int) -> MappingProxyType[str, int]:
    return MappingProxyType(entries)


def _ordered(*roles: str) -> list[str]:
    return sorted(roles)


SOURCE_ROLES: tuple[str, ...] = (
    "official_regulator",
    "legal_text",
    "court_or_authoritative_interpretation",
    "standards_body",
    "standard_or_code",
    "academic_review",
    "academic_paper",
    "professional_body",
    "industry_association",
    "vendor_first_party",
    "government_context",
    "trade_media",
    "secondary_media",
    "user_provided_source",
    "unknown",
)

CLAIM_KINDS: tuple[str, ...] = (
    "definition",
    "fact",
    "mechanism",
    "temporal",
    "numeric",
    "regulatory",
    "legal",
    "medical",
    "financial",
    "market",
    "recommendation",
    "inference",
    "advice",
    "absence",
    "comparison",
    "scope_boundary",
)

SUPPORT_STATUSES: tuple[str, ...] = (
    "supported",
    "scoped_absence",
    "weak",
    "missing",
    "out_of_scope",
    "contradicted",
)

ABSENCE_TYPES: tuple[str, ...] = (
    "not_found_in_checked_scope",
    "not_found_in_scoped_search",
    "not_found_in_official_source_checked",
    "explicitly_not_applicable",
    "explicitly_repealed",
    "replaced_by_later_rule",
    "different_subject_matter",
    "contradicted_by_source",
)

INTENT_LABELS: tuple[str, ...] = (
    "report",
    "comparison",
    "comparison memo",
    "decision memo",
    "technical explainer",
    "legal overview",
    "product guide",
    "literature review",
    "strategy memo",
    "comparison_report",
    "decision_memo",
    "document_review",
    "technical_explainer",
    "generic_report",
)

RISK_LEVELS: tuple[str, ...] = ("low", "medium", "high")
RELEASE_STATUSES: tuple[str, ...] = ("complete", "provisional", "needs_revision", "blocked")
AUDIT_SEVERITIES: tuple[str, ...] = ("low", "medium", "moderate", "high", "critical")
EVIDENCE_LINK_RELATIONS: tuple[str, ...] = ("supports", "qualifies", "contradicts", "scopes")

HIGH_RISK_CLAIM_KINDS = frozenset({"regulatory", "legal", "medical", "financial", "absence"})
CRITICAL_HIGH_RISK_CLAIM_KINDS = frozenset(HIGH_RISK_CLAIM_KINDS)
UNSUPPORTED_SUPPORT_STATUSES = frozenset({"weak", "missing", "out_of_scope", "contradicted"})

AUTHORITATIVE_SOURCE_ROLES = frozenset(
    {
        "official_regulator",
        "legal_text",
        "court_or_authoritative_interpretation",
        "standards_body",
        "standard_or_code",
        "academic_review",
        "academic_paper",
        "professional_body",
        "government_context",
    }
)

DISCOVERY_ONLY_SOURCE_ROLES = frozenset({"trade_media", "secondary_media", "unknown"})
DISCOVERY_SOURCE_ROLES = DISCOVERY_ONLY_SOURCE_ROLES
WEAK_OVERVIEW_SOURCE_ROLES = frozenset(
    {"industry_association", "vendor_first_party", "trade_media", "secondary_media", "unknown"}
)

SEARCH_SCOPED_ABSENCE_TYPES = frozenset(
    {"not_found_in_checked_scope", "not_found_in_scoped_search", "not_found_in_official_source_checked"}
)
EXPLICIT_ABSENCE_TYPES = frozenset(
    {
        "explicitly_not_applicable",
        "explicitly_repealed",
        "replaced_by_later_rule",
        "different_subject_matter",
        "contradicted_by_source",
    }
)

MODE_BASELINES = MappingProxyType(
    {
        "lightweight": _frozen_budget(
            min_sources=2,
            min_distinct_roles=1,
            min_high_risk_sources=1,
            candidate_target=8,
            deep_read_target=4,
            query_budget=6,
            open_budget=6,
            unique_cited_source_target=4,
            citation_instance_target=10,
        ),
        "scoped": _frozen_budget(
            min_sources=3,
            min_distinct_roles=2,
            min_high_risk_sources=1,
            candidate_target=18,
            deep_read_target=8,
            query_budget=14,
            open_budget=12,
            unique_cited_source_target=8,
            citation_instance_target=20,
        ),
        "full": _frozen_budget(
            min_sources=5,
            min_distinct_roles=3,
            min_high_risk_sources=2,
            candidate_target=36,
            deep_read_target=18,
            query_budget=28,
            open_budget=24,
            unique_cited_source_target=14,
            citation_instance_target=36,
        ),
    }
)

REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND = MappingProxyType(
    {
        "definition": _ordered("academic_review", "government_context", "standards_body"),
        "fact": _ordered("academic_review", "government_context", "professional_body", "standards_body"),
        "mechanism": _ordered("academic_paper", "academic_review", "professional_body", "standards_body"),
        "temporal": _ordered("government_context", "legal_text", "official_regulator"),
        "numeric": _ordered("academic_paper", "government_context", "official_regulator", "standard_or_code"),
        "regulatory": _ordered(
            "court_or_authoritative_interpretation",
            "legal_text",
            "official_regulator",
        ),
        "legal": _ordered("court_or_authoritative_interpretation", "legal_text", "official_regulator"),
        "medical": _ordered("academic_paper", "academic_review", "official_regulator", "professional_body"),
        "financial": _ordered("academic_review", "government_context", "official_regulator"),
        "market": _ordered("academic_review", "government_context", "industry_association", "secondary_media"),
        "recommendation": _ordered("academic_review", "government_context", "official_regulator", "professional_body"),
        "inference": _ordered("academic_review", "government_context", "standards_body"),
        "advice": _ordered("government_context", "official_regulator", "professional_body", "standards_body"),
        "absence": _ordered(
            "court_or_authoritative_interpretation",
            "legal_text",
            "official_regulator",
        ),
        "comparison": _ordered("academic_review", "government_context", "professional_body", "standards_body"),
        "scope_boundary": _ordered("government_context", "legal_text", "official_regulator", "user_provided_source"),
    }
)

DEFAULT_SOURCE_ROLE_REQUIREMENTS = REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND

REPORT_SECTION_CATALOG: tuple[tuple[str, str, str], ...] = (
    ("direct_answer", "Direct answer", "Lead with the bounded answer the reader needs."),
    ("scope", "Scope and exclusions", "State what the run covers and what it does not."),
    ("core", "How it works", "Explain the mechanism without claiming more than the evidence supports."),
    ("analysis", "Decision-relevant analysis", "Connect evidence to the reader's decision."),
    ("options", "Options compared", "Compare the main options or categories clearly."),
    ("findings", "What the evidence supports", "State the findings the sources actually support."),
    ("decision_layer", "Checks before you act", "List the checks or decisions that still matter."),
    ("checklist", "Verification checklist", "Provide a short decision table or checklist for the reader."),
    ("uncertainty", "Limitations and uncertainty", "Keep limitations visible and explicit."),
    ("sources", "Sources", "List cited materials for auditability."),
)

REPORT_SECTIONS: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    (
        "direct_answer",
        "Direct answer",
        "Lead with the bounded answer the reader needs.",
        ("Do not overstate completeness.", "Name decisive limitations when they affect the answer."),
    ),
    (
        "scope",
        "Scope and exclusions",
        "State what the run covers and what it does not.",
        ("Keep scope visible.", "Do not imply exhaustive research unless the budget supports it."),
    ),
    (
        "core",
        "How it works",
        "Explain the mechanism without claiming more than the evidence supports.",
        ("Separate mechanism from inference.",),
    ),
    (
        "analysis",
        "Decision-relevant analysis",
        "Connect evidence to the reader's decision.",
        ("Highlight decision-critical tradeoffs.",),
    ),
    (
        "options",
        "Options compared",
        "Compare the main options or categories clearly.",
        ("Use like-for-like comparisons when possible.",),
    ),
    (
        "findings",
        "What the evidence supports",
        "State the findings the sources actually support.",
        ("Prefer evidence-backed statements over synthesis flourishes.",),
    ),
    (
        "decision_layer",
        "Checks before you act",
        "List the checks or decisions that still matter.",
        ("Keep action items explicit.",),
    ),
    (
        "checklist",
        "Verification checklist",
        "Provide a short decision table or checklist for the reader.",
        ("Make next actions visible.",),
    ),
    (
        "uncertainty",
        "Limitations and uncertainty",
        "Keep limitations visible and explicit.",
        ("Do not bury unsupported or scoped material.",),
    ),
    (
        "sources",
        "Sources",
        "List cited materials for auditability.",
        ("Keep source IDs traceable.",),
    ),
)

INTERNAL_HEADING_FRAGMENTS = frozenset(
    {
        "claim audit",
        "evidence matrix",
        "internal pipeline",
        "source-role map",
        "adapter diagnostics",
        "release gate",
    }
)
