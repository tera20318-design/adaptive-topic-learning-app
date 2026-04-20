from __future__ import annotations

from research_os_v2.catalogs import AUTHORITATIVE_SOURCE_ROLES
from research_os_v2.models import IntentClassification, RiskTierAssessment, SourceStrategy


def build_source_strategy(intent: IntentClassification, risk: RiskTierAssessment) -> SourceStrategy:
    required_source_roles = {
        "definition": ["standards_body", "academic_review", "government_context"],
        "fact": ["government_context", "professional_body", "academic_review", "standards_body"],
        "mechanism": ["academic_review", "academic_paper", "standards_body", "vendor_first_party"],
        "temporal": ["official_regulator", "legal_text", "government_context"],
        "numeric": ["official_regulator", "academic_paper", "government_context"],
        "regulatory": ["official_regulator", "legal_text", "court_or_authoritative_interpretation"],
        "legal": ["legal_text", "court_or_authoritative_interpretation", "official_regulator"],
        "medical": ["academic_review", "academic_paper", "professional_body", "official_regulator"],
        "financial": ["official_regulator", "government_context", "academic_review"],
        "market": ["government_context", "industry_association", "academic_review", "secondary_media"],
        "recommendation": ["official_regulator", "academic_review", "professional_body", "government_context"],
        "inference": ["government_context", "academic_review", "standards_body"],
        "advice": ["official_regulator", "professional_body", "standards_body", "government_context"],
        "absence": ["official_regulator", "legal_text", "court_or_authoritative_interpretation"],
        "comparison": ["standards_body", "academic_review", "government_context", "vendor_first_party"],
        "scope_boundary": ["official_regulator", "government_context", "legal_text"],
    }

    source_priority = [
        "official_regulator",
        "legal_text",
        "court_or_authoritative_interpretation",
        "standards_body",
        "standard_or_code",
        "academic_review",
        "academic_paper",
        "professional_body",
        "government_context",
        "industry_association",
        "vendor_first_party",
        "secondary_media",
        "trade_media",
        "user_provided_source",
        "unknown",
    ]

    if risk.risk_tier == "low" and intent.label in {"technical explainer", "product guide"}:
        source_priority = [
            "standards_body",
            "academic_review",
            "academic_paper",
            "professional_body",
            "government_context",
            "vendor_first_party",
            "industry_association",
            "secondary_media",
            "unknown",
        ]

    compatibility_notes = {
        claim_kind: _build_note(claim_kind, roles)
        for claim_kind, roles in required_source_roles.items()
    }
    compatibility_notes["authoritative_roles"] = ", ".join(sorted(AUTHORITATIVE_SOURCE_ROLES))

    return SourceStrategy(
        source_priority=source_priority,
        required_source_roles=required_source_roles,
        compatibility_notes=compatibility_notes,
    )


def _build_note(claim_kind: str, roles: list[str]) -> str:
    role_text = ", ".join(roles)
    return f"{claim_kind} claims should prefer: {role_text}."
