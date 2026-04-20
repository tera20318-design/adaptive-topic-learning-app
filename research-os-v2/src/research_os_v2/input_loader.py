from __future__ import annotations

from typing import Any

from research_os_v2.catalogs import CLAIM_KINDS, SOURCE_ROLES
from research_os_v2.models import Finding, ResearchRequest, SourcePacket


SOURCE_ROLE_ALIASES = {
    "authoritative": "official_regulator",
    "primary": "user_provided_source",
    "secondary": "secondary_media",
    "official": "official_regulator",
    "internal": "user_provided_source",
}

CLAIM_KIND_ALIASES = {
    "architecture": "mechanism",
    "workflow": "mechanism",
    "operational constraint": "advice",
    "constraint": "scope_boundary",
    "obligation": "regulatory",
    "interpretation": "legal",
    "trend": "market",
    "recommendation": "advice",
    "request flow": "mechanism",
    "timeline": "temporal",
    "metric": "numeric",
    "history": "fact",
    "process": "mechanism",
    "document finding": "fact",
    "risk": "fact",
}

OUTPUT_TYPE_ALIASES = {
    "technical overview": "technical explainer",
    "technical brief": "technical explainer",
    "regulatory memo": "legal overview",
    "legal review": "legal overview",
    "product comparison": "comparison",
    "market analysis": "strategy memo",
    "document review": "report",
}


def load_request(payload: dict[str, Any], *, as_of_date: str = "") -> ResearchRequest:
    source_packets = [load_source_packet(item, payload.get("output_type", "")) for item in payload.get("source_packets", [])]
    return ResearchRequest(
        topic=payload["topic"],
        reader=payload["reader"],
        use_context=payload["use_context"],
        requested_mode=normalize_mode(payload.get("requested_mode", "scoped")),
        output_type=normalize_output_type(payload.get("output_type", "")),
        question=payload.get("question", payload.get("use_context", "")),
        jurisdiction=payload.get("jurisdiction", ""),
        temporal_context=payload.get("temporal_context", ""),
        as_of_date=as_of_date or payload.get("as_of_date", ""),
        provided_document_name=payload.get("provided_document_name", ""),
        source_packets=source_packets,
    )


def load_source_packet(payload: dict[str, Any], output_type: str) -> SourcePacket:
    role = normalize_source_role(payload.get("source_role", "unknown"), payload.get("quality_flags", []), output_type)
    return SourcePacket(
        source_id=payload["source_id"],
        title=payload["title"],
        source_role=role,
        citation=payload.get("citation", payload.get("title", "")),
        url=payload.get("url", ""),
        publisher=payload.get("publisher", ""),
        published_on=payload.get("published_on", ""),
        jurisdiction=payload.get("jurisdiction", ""),
        quality_flags=payload.get("quality_flags", []),
        summary=payload.get("summary", ""),
        findings=[load_finding(item, payload["source_id"], output_type) for item in payload.get("findings", [])],
    )


def load_finding(payload: dict[str, Any], source_id: str, output_type: str) -> Finding:
    claim_kind = normalize_claim_kind(payload.get("claim_kind", "fact"), output_type)
    return Finding(
        finding_id=payload["finding_id"],
        statement=payload["statement"],
        claim_kind=claim_kind,
        risk_level=normalize_risk_level(payload.get("risk_level", "medium")),
        section_hint=normalize_section_hint(payload.get("section_hint", "")),
        decision_note=payload.get("decision_note", ""),
        support_status_hint=normalize_support_hint(payload.get("support_status_hint", "supported")),
        confidence=float(payload.get("confidence", 0.8)),
        source_ids=payload.get("source_ids", [source_id]),
        risk_tags=payload.get("risk_tags", []),
        failure_modes=payload.get("failure_modes", []),
        misunderstandings=payload.get("misunderstandings", []),
        boundary_concepts=payload.get("boundary_concepts", []),
        caveat=payload.get("caveat", ""),
        absence_type=payload.get("absence_type", ""),
        contradiction_note=payload.get("contradiction_note", ""),
        required_fix=payload.get("required_fix", ""),
        jurisdiction=payload.get("jurisdiction", ""),
        temporal_note=payload.get("temporal_note", ""),
        scope_note=payload.get("scope_note", ""),
    )


def normalize_output_type(value: str) -> str:
    normalized = value.strip().lower()
    return OUTPUT_TYPE_ALIASES.get(normalized, normalized)


def normalize_mode(value: str) -> str:
    lowered = value.strip().lower()
    if lowered in {"full", "scoped", "lightweight"}:
        return lowered
    if "full" in lowered or "deep" in lowered:
        return "full"
    if "light" in lowered or "brief" in lowered:
        return "lightweight"
    return "scoped"


def normalize_source_role(value: str, quality_flags: list[str], output_type: str) -> str:
    lowered = value.strip().lower()
    if lowered in SOURCE_ROLES:
        return lowered
    if lowered in SOURCE_ROLE_ALIASES:
        mapped = SOURCE_ROLE_ALIASES[lowered]
        if lowered == "authoritative" and "binding-text" in quality_flags:
            return "legal_text"
        if lowered == "authoritative" and "guideline" in " ".join(quality_flags).lower():
            return "professional_body"
        return mapped
    if "official" in quality_flags:
        return "official_regulator"
    if "binding-text" in quality_flags:
        return "legal_text"
    if "internal" in quality_flags:
        return "user_provided_source"
    if "analysis" in quality_flags:
        return "secondary_media"
    return "unknown"


def normalize_claim_kind(value: str, output_type: str) -> str:
    lowered = value.strip().lower()
    if lowered in CLAIM_KINDS:
        return lowered
    if lowered in CLAIM_KIND_ALIASES:
        return CLAIM_KIND_ALIASES[lowered]
    if "legal" in output_type.lower() and lowered in {"trigger", "duty", "rule"}:
        return "legal"
    if "medical" in output_type.lower() and lowered in {"benefit", "harm", "signal"}:
        return "medical"
    if "financial" in output_type.lower() and lowered in {"fee", "cost", "return"}:
        return "financial"
    return "fact"


def normalize_risk_level(value: str) -> str:
    lowered = value.strip().lower()
    if lowered == "moderate":
        return "medium"
    if lowered not in {"low", "medium", "high"}:
        return "medium"
    return lowered


def normalize_section_hint(value: str) -> str:
    lowered = value.strip().lower()
    if any(token in lowered for token in ["scope", "boundary"]):
        return "scope"
    if any(token in lowered for token in ["risk", "failure", "hazard"]):
        return "risks"
    if any(token in lowered for token in ["option", "compare", "category"]):
        return "options"
    if any(token in lowered for token in ["decision", "adoption", "recommend", "prerequisite"]):
        return "decision_layer"
    if any(token in lowered for token in ["uncertain", "gap", "not found"]):
        return "uncertainty"
    if any(token in lowered for token in ["explain", "flow", "architecture", "process", "mechanism", "trigger"]):
        return "core_explanation"
    return lowered or "evidence_findings"


def normalize_support_hint(value: str) -> str:
    lowered = value.strip().lower()
    mapping = {
        "partial": "weak",
        "open": "weak",
        "supported": "supported",
        "weak": "weak",
        "missing": "missing",
    }
    return mapping.get(lowered, "supported")
