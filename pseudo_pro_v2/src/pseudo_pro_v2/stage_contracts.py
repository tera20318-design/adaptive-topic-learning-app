from __future__ import annotations


STAGE_FAILURE_CODES = {
    "missing_required_input",
    "invalid_schema",
    "empty_output",
    "downstream_contract_violation",
    "clean_room_integrity_violation",
    "unsupported_high_risk_claim",
    "required_table_missing",
    "metadata_inconsistent",
    "target_miss_without_waiver",
    "citation_trace_mismatch",
    "document_grounding_missing",
}

STAGE_SNAPSHOT_REQUIRED_FIELDS = {
    "stage_name",
    "inputs_summary",
    "outputs_summary",
    "failure_codes",
    "invariants_checked",
}

STAGE_CONTRACTS = {
    "intent_classifier": {
        "required_inputs": ["RunRequest.topic", "RunRequest.use_context", "RunRequest.desired_depth"],
        "required_outputs": ["IntentResult.intent_label", "IntentResult.decision_focus", "IntentResult.reader_task"],
        "failure_codes": ["missing_required_input", "empty_output"],
        "invariants": ["intent_label is non-empty", "report_shape_hints is non-empty"],
    },
    "risk_tier_classifier": {
        "required_inputs": ["RunRequest", "IntentResult.intent_label"],
        "required_outputs": ["RiskTierResult.risk_tier", "RiskTierResult.high_stakes_domains"],
        "failure_codes": ["missing_required_input", "downstream_contract_violation"],
        "invariants": ["risk_tier is one of low|medium|high", "rationale is non-empty"],
    },
    "scope_budget_planner": {
        "required_inputs": ["RunRequest.mode", "RunRequest.target_profile", "RiskTierResult.risk_tier"],
        "required_outputs": ["BudgetPlan.requested_mode", "BudgetPlan.effective_mode", "BudgetPlan.target_profile"],
        "failure_codes": ["missing_required_input", "invalid_schema"],
        "invariants": ["full_dr_equivalent is boolean", "target_profile exists"],
    },
    "domain_adapter_generator": {
        "required_inputs": [
            "RunRequest.topic",
            "RunRequest.reader",
            "RunRequest.use_context",
            "IntentResult.intent_label",
            "RiskTierResult.risk_tier",
            "BudgetPlan.limitations",
        ],
        "required_outputs": [
            "DomainAdapter.output_type",
            "DomainAdapter.risk_tier",
            "DomainAdapter.required_tables",
            "DomainAdapter.required_decision_layer",
            "DomainAdapter.source_roles_required_by_claim_kind",
        ],
        "failure_codes": ["invalid_schema", "empty_output", "clean_room_integrity_violation"],
        "invariants": ["all schema-required fields present", "domain_specific_risks is non-empty"],
    },
    "source_strategy_builder": {
        "required_inputs": ["DomainAdapter.source_priority", "DomainAdapter.source_roles_required_by_claim_kind"],
        "required_outputs": ["SourceStrategy.required_source_roles_by_claim_kind", "SourceStrategy.compatibility_notes"],
        "failure_codes": ["missing_required_input", "downstream_contract_violation"],
        "invariants": ["every claim-kind mapping has at least one source role"],
    },
    "evidence_collector": {
        "required_inputs": ["RunRequest.source_packets"],
        "required_outputs": ["CollectedEvidence.sources", "CollectedEvidence.findings", "CollectedEvidence.source_counts_by_role"],
        "failure_codes": ["missing_required_input", "invalid_schema", "empty_output"],
        "invariants": ["every source has source_id/source_role/title", "every finding has finding_id/statement/claim_kind/risk_level"],
    },
    "report_planner": {
        "required_inputs": ["DomainAdapter.required_tables", "DomainAdapter.required_decision_layer", "DomainAdapter.risk_tier"],
        "required_outputs": ["ReportSectionPlan.key", "ReportSectionPlan.title", "ReportSectionPlan.target_claim_count"],
        "failure_codes": ["missing_required_input", "downstream_contract_violation"],
        "invariants": ["required reader-facing sections are present", "internal headings do not appear in plan titles"],
    },
    "draft_writer": {
        "required_inputs": ["RunRequest", "DomainAdapter", "CollectedEvidence", "ReportSectionPlan[]", "BudgetPlan"],
        "required_outputs": ["ReportDraft.title", "ReportDraft.sections", "ReportDraft.units"],
        "failure_codes": ["missing_required_input", "empty_output", "downstream_contract_violation"],
        "invariants": ["section titles remain reader-facing", "every claim unit preserves origin_finding_id"],
    },
    "claim_extractor": {
        "required_inputs": ["ReportDraft.units", "SourceStrategy.required_source_roles_by_claim_kind"],
        "required_outputs": ["ClaimLedgerRow.claim_id", "ClaimLedgerRow.claim_kind", "ClaimLedgerRow.risk_level", "ClaimLedgerRow.support_status"],
        "failure_codes": ["empty_output", "downstream_contract_violation"],
        "invariants": ["every claim unit becomes exactly one claim row", "included_in_report is preserved"],
    },
    "evidence_mapper": {
        "required_inputs": ["ClaimLedgerRow[]", "CollectedEvidence", "SourceStrategy.required_source_roles_by_claim_kind"],
        "required_outputs": ["ClaimLedgerRow.required_role_matched", "ClaimLedgerRow.role_fit_status", "ClaimLedgerRow.support_status", "CitationLedgerRow[]"],
        "failure_codes": ["missing_required_input", "metadata_inconsistent", "unsupported_high_risk_claim", "citation_trace_mismatch"],
        "invariants": ["high-risk support requires claim-kind-appropriate role match", "every cited source exists in collected evidence"],
    },
    "contradiction_absence_guard": {
        "required_inputs": ["ClaimLedgerRow[]", "ReportDraft", "RunRequest"],
        "required_outputs": ["ClaimLedgerRow.included_in_report", "ClaimLedgerRow.exclusion_reason", "ContradictionEntry[]", "EvidenceGapEntry[]"],
        "failure_codes": ["unsupported_high_risk_claim", "downstream_contract_violation"],
        "invariants": ["high-risk scoped absence is not left in mainline prose", "excluded claims remain visible in the ledger"],
    },
    "tone_controller": {
        "required_inputs": ["ReportDraft", "ClaimLedgerRow[]"],
        "required_outputs": ["ReportUnit.text"],
        "failure_codes": ["downstream_contract_violation"],
        "invariants": ["excluded claims stay excluded", "every tone mode is explicit and known"],
    },
    "release_gate": {
        "required_inputs": [
            "ReportDraft",
            "ClaimLedgerRow[]",
            "CitationLedgerRow[]",
            "BudgetPlan",
            "DomainAdapter",
            "metrics",
            "validation_errors",
        ],
        "required_outputs": ["ReleaseGateDecision.status", "ReleaseGateDecision.reasons", "ReleaseGateDecision.blocking_reasons"],
        "failure_codes": [
            "unsupported_high_risk_claim",
            "metadata_inconsistent",
            "target_miss_without_waiver",
            "required_table_missing",
            "clean_room_integrity_violation",
            "citation_trace_mismatch",
            "document_grounding_missing",
        ],
        "invariants": ["blocking claim failures override aggregate metrics", "rubric failures cannot become complete"],
    },
    "bundle_renderer": {
        "required_inputs": ["PipelineBundle"],
        "required_outputs": [
            "final_report.md",
            "domain-adapter.md",
            "metrics.json",
            "claim-ledger.tsv",
            "citation-ledger.tsv",
            "release-gate-summary.md",
        ],
        "failure_codes": ["downstream_contract_violation", "metadata_inconsistent"],
        "invariants": ["included and excluded claims render consistently into ledgers", "report headings remain reader-facing"],
    },
}


def validate_stage_contract_registry() -> list[str]:
    errors: list[str] = []
    for stage_name, contract in STAGE_CONTRACTS.items():
        if not contract.get("required_inputs"):
            errors.append(f"{stage_name}: missing required_inputs")
        if not contract.get("required_outputs"):
            errors.append(f"{stage_name}: missing required_outputs")
        if not contract.get("invariants"):
            errors.append(f"{stage_name}: missing invariants")
        for failure_code in contract.get("failure_codes", []):
            if failure_code not in STAGE_FAILURE_CODES:
                errors.append(f"{stage_name}: unknown failure code `{failure_code}`")
    return errors


def validate_stage_snapshot(snapshot: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(STAGE_SNAPSHOT_REQUIRED_FIELDS - set(snapshot))
    if missing:
        errors.append(f"stage snapshot missing required fields: {', '.join(missing)}")
    if "failure_codes" in snapshot and not isinstance(snapshot["failure_codes"], list):
        errors.append("stage snapshot `failure_codes` should be a list")
    if "invariants_checked" in snapshot and not isinstance(snapshot["invariants_checked"], list):
        errors.append("stage snapshot `invariants_checked` should be a list")
    if isinstance(snapshot.get("failure_codes"), list):
        unknown = [item for item in snapshot["failure_codes"] if item not in STAGE_FAILURE_CODES]
        if unknown:
            errors.append(f"stage snapshot has unknown failure codes: {unknown}")
    return errors
