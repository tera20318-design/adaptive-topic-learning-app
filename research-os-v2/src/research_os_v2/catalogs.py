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

HIGH_STAKES_DOMAINS = {
    "legal",
    "medical",
    "financial",
    "safety",
    "regulatory",
    "procurement",
    "technical_failure",
}

HIGH_RISK_CLAIM_KINDS = {
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
    "government_context",
    "professional_body",
}

MODE_BASELINES = {
    "lightweight": {
        "candidate_target": 8,
        "deep_read_target": 4,
        "query_budget": 6,
        "open_budget": 6,
        "unique_cited_source_target": 4,
        "citation_instance_target": 10,
    },
    "scoped": {
        "candidate_target": 18,
        "deep_read_target": 8,
        "query_budget": 14,
        "open_budget": 12,
        "unique_cited_source_target": 8,
        "citation_instance_target": 20,
    },
    "full": {
        "candidate_target": 36,
        "deep_read_target": 18,
        "query_budget": 28,
        "open_budget": 24,
        "unique_cited_source_target": 14,
        "citation_instance_target": 36,
    },
}

INTENT_TYPES = {
    "report",
    "comparison",
    "decision memo",
    "technical explainer",
    "legal overview",
    "product guide",
    "literature review",
    "strategy memo",
}

ALLOWED_RELEASE_STATUSES = {"complete", "provisional", "needs_revision", "blocked"}
