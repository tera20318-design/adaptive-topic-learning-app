from __future__ import annotations

SOURCE_ROLES = [
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
]

CLAIM_KINDS = [
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
]

ABSENCE_TYPES = [
    "not_found_in_scoped_search",
    "not_found_in_official_source_checked",
    "explicitly_not_applicable",
    "explicitly_repealed",
    "replaced_by_later_rule",
    "different_subject_matter",
    "contradicted_by_source",
]

HIGH_RISK_CLAIM_KINDS = {
    "regulatory",
    "legal",
    "medical",
    "financial",
    "absence",
}

CRITICAL_HIGH_RISK_CLAIM_KINDS = {
    "regulatory",
    "legal",
    "medical",
    "financial",
    "absence",
}

AUTHORITATIVE_SOURCE_ROLES = {
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

DISCOVERY_ONLY_SOURCE_ROLES = {
    "trade_media",
    "secondary_media",
    "unknown",
}

WEAK_OVERVIEW_SOURCE_ROLES = {
    "industry_association",
    "vendor_first_party",
    "trade_media",
    "secondary_media",
    "unknown",
}

MODE_BASELINES = {
    "scoped": {
        "min_sources": 3,
        "min_citations": 5,
        "min_report_claim_capture_ratio": 0.9,
    },
    "full": {
        "min_sources": 5,
        "min_citations": 8,
        "min_report_claim_capture_ratio": 0.95,
    },
}

REQUIRED_SOURCE_ROLES_BY_CLAIM_KIND = {
    "definition": ["standards_body", "academic_review", "government_context"],
    "fact": ["government_context", "professional_body", "academic_review", "standards_body"],
    "mechanism": ["academic_review", "academic_paper", "professional_body", "standards_body"],
    "temporal": ["official_regulator", "legal_text", "government_context"],
    "numeric": ["official_regulator", "government_context", "standard_or_code", "academic_paper"],
    "regulatory": ["official_regulator", "legal_text", "court_or_authoritative_interpretation"],
    "legal": ["legal_text", "court_or_authoritative_interpretation", "official_regulator"],
    "medical": ["academic_review", "academic_paper", "professional_body", "official_regulator"],
    "financial": ["official_regulator", "government_context", "academic_review"],
    "market": ["government_context", "industry_association", "academic_review", "secondary_media"],
    "recommendation": ["official_regulator", "academic_review", "professional_body", "government_context"],
    "inference": ["government_context", "academic_review", "standards_body"],
    "advice": ["official_regulator", "professional_body", "standards_body", "government_context"],
    "absence": ["official_regulator", "legal_text", "court_or_authoritative_interpretation"],
    "comparison": ["standards_body", "academic_review", "government_context", "professional_body"],
    "scope_boundary": ["official_regulator", "government_context", "legal_text", "user_provided_source"],
}

REPORT_SECTIONS = [
    ("direct_answer", "Direct answer", "Lead with the answer the reader needs."),
    ("scope", "Scope and exclusions", "State what the run does and does not cover."),
    ("core", "Core explanation", "Explain the central structure or mechanism."),
    ("analysis", "Decision-relevant analysis", "Connect evidence to the reader's decision."),
    ("options", "Main options/categories/mechanisms", "Show the major landscape clearly."),
    ("risks", "Risks and failure modes", "Give real space to failure and downside."),
    ("findings", "Evidence-backed findings", "State what the available evidence supports."),
    ("decision_layer", "Reader decision layer", "Tell the reader what to decide or verify next."),
    ("checklist", "Checklist or decision table", "Provide a practical verification aid."),
    ("uncertainty", "Uncertainty and next research", "State limitations honestly."),
    ("sources", "Sources", "List the cited sources for auditability."),
]

INTERNAL_HEADING_FRAGMENTS = {
    "role structure",
    "upstream downstream",
    "contradiction notes",
    "domain risk map",
    "claim audit",
    "evidence matrix",
    "internal pipeline",
}
