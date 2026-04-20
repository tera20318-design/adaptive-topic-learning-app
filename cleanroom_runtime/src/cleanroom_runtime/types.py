from __future__ import annotations

from enum import StrEnum
from typing import Literal, TypeAlias


ResearchMode: TypeAlias = Literal["lightweight", "scoped", "full"]
EvidenceMode: TypeAlias = Literal["synthetic", "live"]
RiskLevel: TypeAlias = Literal["low", "medium", "high"]
IntentLabel: TypeAlias = Literal[
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
    "technical_explainer",
    "generic_report",
]
SourceRole: TypeAlias = Literal[
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
ClaimKind: TypeAlias = Literal[
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
SupportStatus: TypeAlias = Literal[
    "supported",
    "scoped_absence",
    "weak",
    "missing",
    "out_of_scope",
    "contradicted",
]
ReleaseStatus: TypeAlias = Literal["complete", "provisional", "needs_revision", "blocked"]
AuditSeverity: TypeAlias = Literal["low", "medium", "moderate", "high", "critical"]

STAGE_SNAPSHOT_SCHEMA_VERSION = "stage_contract.v2"


class StageFailureCode(StrEnum):
    REQUIRED_FIELD_MISSING = "REQUIRED_FIELD_MISSING"
    DOWNSTREAM_FIELD_MISSING = "DOWNSTREAM_FIELD_MISSING"
    SCHEMA_VALIDATION_FAILED = "SCHEMA_VALIDATION_FAILED"
    INTENT_SHAPE_HINTS_REQUIRED = "INTENT_SHAPE_HINTS_REQUIRED"
    RISK_HIGH_TIER_REQUIRES_DOMAIN = "RISK_HIGH_TIER_REQUIRES_DOMAIN"
    BUDGET_RESEARCH_NOTE_MISMATCH = "BUDGET_RESEARCH_NOTE_MISMATCH"
    ADAPTER_REQUEST_MIRROR_MISMATCH = "ADAPTER_REQUEST_MIRROR_MISMATCH"
    ADAPTER_LIMITATIONS_NOT_PROPAGATED = "ADAPTER_LIMITATIONS_NOT_PROPAGATED"
    STRATEGY_PRIORITY_MUST_ALIGN_ADAPTER = "STRATEGY_PRIORITY_MUST_ALIGN_ADAPTER"
    STRATEGY_ROLE_MAP_MUST_ALIGN_ADAPTER = "STRATEGY_ROLE_MAP_MUST_ALIGN_ADAPTER"
    EVIDENCE_FINDING_SOURCE_LINEAGE = "EVIDENCE_FINDING_SOURCE_LINEAGE"
    REPORT_PLAN_UNCERTAINTY_REQUIRED = "REPORT_PLAN_UNCERTAINTY_REQUIRED"
    REPORT_PLAN_DECISION_LAYER_REQUIRED = "REPORT_PLAN_DECISION_LAYER_REQUIRED"
    REPORT_PLAN_OPTIONS_SECTION_REQUIRED = "REPORT_PLAN_OPTIONS_SECTION_REQUIRED"
    DRAFT_SECTIONS_MUST_ALIGN_PLAN = "DRAFT_SECTIONS_MUST_ALIGN_PLAN"
    DRAFT_LIMITATIONS_VISIBLE = "DRAFT_LIMITATIONS_VISIBLE"
    CLAIM_LEDGER_COVERAGE_MISMATCH = "CLAIM_LEDGER_COVERAGE_MISMATCH"
    CLAIM_NORMALIZATION_MISMATCH = "CLAIM_NORMALIZATION_MISMATCH"
    EVIDENCE_MAP_CITATION_COVERAGE_MISMATCH = "EVIDENCE_MAP_CITATION_COVERAGE_MISMATCH"
    GUARD_HIGH_RISK_UNSUPPORTED_EXCLUDED = "GUARD_HIGH_RISK_UNSUPPORTED_EXCLUDED"
    GUARD_CLAIM_DRAFT_SYNC_BROKEN = "GUARD_CLAIM_DRAFT_SYNC_BROKEN"
    TONE_WEAK_CLAIM_PREFIX_REQUIRED = "TONE_WEAK_CLAIM_PREFIX_REQUIRED"
    TONE_SCOPED_ABSENCE_REWRITE_REQUIRED = "TONE_SCOPED_ABSENCE_REWRITE_REQUIRED"
    METRICS_TARGET_MISSES_ALIGN_RESULTS = "METRICS_TARGET_MISSES_ALIGN_RESULTS"
    RELEASE_SYNTHETIC_NOT_COMPLETE = "RELEASE_SYNTHETIC_NOT_COMPLETE"
    RELEASE_BLOCKED_REASON_REQUIRED = "RELEASE_BLOCKED_REASON_REQUIRED"
    SEMANTIC_FIXTURE_NOUN_LEAK = "SEMANTIC_FIXTURE_NOUN_LEAK"
    SEMANTIC_RISK_PHRASE_LEAK = "SEMANTIC_RISK_PHRASE_LEAK"
    SEMANTIC_REGULATION_WORDING_LEAK = "SEMANTIC_REGULATION_WORDING_LEAK"
    SEMANTIC_OVERCLAIM_PHRASING_LEAK = "SEMANTIC_OVERCLAIM_PHRASING_LEAK"
