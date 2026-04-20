from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .models import (
    AuditArtifacts,
    BudgetPlan,
    ClaimLedgerRow,
    CitationLedgerRow,
    CollectedEvidence,
    DomainAdapter,
    IntentResult,
    MetricsSnapshot,
    ReleaseGateDecision,
    ReportDraft,
    ReportSectionPlan,
    RunRequest,
    SourceStrategy,
    StageContractFailure,
    StageSnapshot,
)
from .semantic_isolation import detect_semantic_leakage, semantic_anchor_values
from .types import STAGE_SNAPSHOT_SCHEMA_VERSION, StageFailureCode
from .utils import normalize_text
from .validators import (
    validate_audit_artifacts,
    validate_budget_plan,
    validate_claim_records,
    validate_citation_record,
    validate_domain_adapter,
    validate_evidence_collection,
    validate_intent_classification,
    validate_metrics,
    validate_release_decision,
    validate_report_draft,
    validate_report_plan,
    validate_risk_classification,
    validate_source_strategy,
)

MISSING = object()
SCHEMA_VALIDATION_FAILED = StageFailureCode.SCHEMA_VALIDATION_FAILED
REQUIRED_FIELD_MISSING = StageFailureCode.REQUIRED_FIELD_MISSING
DOWNSTREAM_FIELD_MISSING = StageFailureCode.DOWNSTREAM_FIELD_MISSING


@dataclass(frozen=True, slots=True)
class StageInvariantSpec:
    code: StageFailureCode
    description: str
    evaluator: Callable[[str, Any, dict[str, Any]], list[StageContractFailure]]
    emitted_codes: tuple[StageFailureCode, ...] = ()


@dataclass(frozen=True, slots=True)
class StageContractSpec:
    artifact_type: str
    required_fields: tuple[str, ...] = ()
    downstream_must_have_fields: dict[str, tuple[str, ...]] = field(default_factory=dict)
    snapshot_fields: tuple[str, ...] = ()
    schema_validator: Callable[[Any, dict[str, Any]], list[str]] | None = None
    invariants: tuple[StageInvariantSpec, ...] = ()
    strictness: str = "strict"


def validate_stage_output(stage: str, output: Any, **context: Any) -> list[StageContractFailure]:
    spec = STAGE_CONTRACTS[stage]
    failures: list[StageContractFailure] = []

    for field_name in spec.required_fields:
        value = _resolve_path(output, field_name)
        if _is_missing(value):
            failures.append(
                StageContractFailure(
                    stage=stage,
                    code=REQUIRED_FIELD_MISSING,
                    message=f"{stage} must populate `{field_name}` before handoff.",
                    field=field_name,
                )
            )

    for downstream_stage, field_names in spec.downstream_must_have_fields.items():
        for field_name in field_names:
            value = _resolve_path(output, field_name)
            if _is_missing(value):
                failures.append(
                    StageContractFailure(
                        stage=stage,
                        code=DOWNSTREAM_FIELD_MISSING,
                        message=f"{stage} must populate `{field_name}` for downstream stage `{downstream_stage}`.",
                        field=field_name,
                        downstream_stage=downstream_stage,
                    )
                )

    has_required_field_failure = any(failure.code == REQUIRED_FIELD_MISSING for failure in failures)
    if spec.schema_validator is not None and not has_required_field_failure:
        try:
            for error in spec.schema_validator(output, context):
                failures.append(StageContractFailure(stage=stage, code=SCHEMA_VALIDATION_FAILED, message=error))
        except (KeyError, TypeError, AttributeError) as exc:
            failures.append(
                StageContractFailure(
                    stage=stage,
                    code=SCHEMA_VALIDATION_FAILED,
                    message=f"{stage} schema validator could not evaluate the payload: {exc}",
                )
            )

    if not has_required_field_failure:
        for invariant in spec.invariants:
            failures.extend(invariant.evaluator(stage, output, context))

    return failures


def audit_stage_output(stage: str, output: Any, **context: Any) -> tuple[list[StageContractFailure], StageSnapshot]:
    failures = validate_stage_output(stage, output, **context)
    spec = STAGE_CONTRACTS[stage]
    snapshot = StageSnapshot(
        stage=stage,
        artifact_type=spec.artifact_type,
        required_fields=list(spec.required_fields),
        downstream_must_have_fields={key: list(value) for key, value in spec.downstream_must_have_fields.items()},
        invariant_codes=[invariant.code for invariant in spec.invariants],
        contract_ok=not failures,
        failure_codes=[failure.code for failure in failures],
        summary={field_name: _snapshot_value(_resolve_path(output, field_name)) for field_name in spec.snapshot_fields},
    )
    return failures, snapshot


def contract_error_messages(failures: list[StageContractFailure]) -> list[str]:
    return [f"[{failure.stage}:{failure.code}] {failure.message}" for failure in failures]


def stage_failure_codes() -> tuple[StageFailureCode, ...]:
    return tuple(StageFailureCode)


def stage_snapshot_schema() -> dict[str, Any]:
    return {
        "snapshot_schema_version": STAGE_SNAPSHOT_SCHEMA_VERSION,
        "required_fields": {
            "stage": "str",
            "artifact_type": "str",
            "required_fields": "list[str]",
            "downstream_must_have_fields": "dict[str, list[str]]",
            "invariant_codes": "list[StageFailureCode]",
            "contract_ok": "bool",
            "failure_codes": "list[StageFailureCode]",
            "summary": "dict[str, Any]",
            "snapshot_schema_version": "str",
        },
        "summary_tracks_declared_snapshot_fields": True,
        "failure_code_enum": [code.value for code in StageFailureCode],
    }


def validate_stage_snapshot(snapshot: StageSnapshot | dict[str, Any]) -> list[str]:
    if isinstance(snapshot, dict):
        snapshot = StageSnapshot(**snapshot)
    schema = stage_snapshot_schema()
    errors: list[str] = []
    required_schema_fields = schema["required_fields"]

    for field_name in required_schema_fields:
        if not hasattr(snapshot, field_name):
            errors.append(f"stage snapshot missing schema field `{field_name}`")

    if snapshot.snapshot_schema_version != schema["snapshot_schema_version"]:
        errors.append(
            f"stage snapshot schema version must be `{schema['snapshot_schema_version']}`, found `{snapshot.snapshot_schema_version}`"
        )
    if not isinstance(snapshot.contract_ok, bool):
        errors.append("stage snapshot `contract_ok` must be boolean")
    if not isinstance(snapshot.required_fields, list):
        errors.append("stage snapshot `required_fields` must be a list")
    if not isinstance(snapshot.downstream_must_have_fields, dict):
        errors.append("stage snapshot `downstream_must_have_fields` must be a dict")
    if not isinstance(snapshot.summary, dict):
        errors.append("stage snapshot `summary` must be a dict")
    unknown_failure_codes = [code for code in snapshot.failure_codes if not isinstance(code, StageFailureCode)]
    if unknown_failure_codes:
        errors.append("stage snapshot contains unknown failure codes: " + ", ".join(str(code) for code in unknown_failure_codes))

    spec = STAGE_CONTRACTS.get(snapshot.stage)
    if spec is None:
        errors.append(f"stage snapshot references unknown stage `{snapshot.stage}`")
        return errors

    if snapshot.required_fields != list(spec.required_fields):
        errors.append(f"stage snapshot `{snapshot.stage}` required_fields do not match the contract registry")
    if snapshot.downstream_must_have_fields != {key: list(value) for key, value in spec.downstream_must_have_fields.items()}:
        errors.append(f"stage snapshot `{snapshot.stage}` downstream fields do not match the contract registry")
    if snapshot.invariant_codes != [invariant.code for invariant in spec.invariants]:
        errors.append(f"stage snapshot `{snapshot.stage}` invariant codes do not match the contract registry")
    if set(snapshot.summary.keys()) != set(spec.snapshot_fields):
        errors.append(f"stage snapshot `{snapshot.stage}` summary does not cover every declared snapshot field")
    return errors


def validate_stage_contract_registry() -> list[str]:
    errors: list[str] = []
    for stage_name, spec in STAGE_CONTRACTS.items():
        if spec.strictness != "strict":
            errors.append(f"{stage_name} contract strictness must remain `strict`")
        if not spec.required_fields:
            errors.append(f"{stage_name} contract must declare required_fields")
        if not spec.snapshot_fields:
            errors.append(f"{stage_name} contract must declare snapshot_fields")
        if spec.schema_validator is None:
            errors.append(f"{stage_name} contract must provide a schema_validator")
        if not spec.invariants:
            errors.append(f"{stage_name} contract must declare at least one invariant")
        invariant_codes = [invariant.code for invariant in spec.invariants]
        if len(invariant_codes) != len(set(invariant_codes)):
            errors.append(f"{stage_name} contract reuses invariant codes within the same stage")
        for invariant in spec.invariants:
            emitted_codes = invariant.emitted_codes or (invariant.code,)
            if invariant.code not in emitted_codes:
                errors.append(f"{stage_name} invariant `{invariant.code}` must be included in its emitted code set")
            for code in emitted_codes:
                if not isinstance(code, StageFailureCode):
                    errors.append(f"{stage_name} contract uses unknown invariant code `{code}`")
        for field_name in spec.snapshot_fields:
            if "." in field_name:
                errors.append(f"{stage_name} snapshot field `{field_name}` must stay top-level for schema coverage")
    return errors


def _validate_report_plan_payload(output: Any, context: dict[str, Any]) -> list[str]:
    del context
    return validate_report_plan(output["sections"])


def _validate_claim_payload(output: Any, context: dict[str, Any]) -> list[str]:
    del context
    return validate_claim_records(output["claims"])


def _validate_evidence_map_payload(output: Any, context: dict[str, Any]) -> list[str]:
    errors = validate_claim_records(output["claims"])
    claim_ids = {claim.claim_id for claim in output["claims"]}
    source_ids = {source.source_id for source in context["evidence"].sources}
    for citation in output["citations"]:
        errors.extend(validate_citation_record(citation, claim_ids, source_ids))
    return errors


def _validate_guard_payload(output: Any, context: dict[str, Any]) -> list[str]:
    del context
    errors = validate_claim_records(output["claims"])
    errors.extend(validate_report_draft(output["draft"]))
    errors.extend(
        validate_audit_artifacts(
            AuditArtifacts(
                contradictions=list(output["contradictions"]),
                gaps=list(output["gaps"]),
            ),
            output["claims"],
        )
    )
    return errors


def _intent_shape_hints(stage: str, output: IntentResult, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    if output.report_shape_hints:
        return []
    return [_failure(stage, StageFailureCode.INTENT_SHAPE_HINTS_REQUIRED, "intent classification must emit at least one report shape hint.")]


def _high_risk_domain(stage: str, output, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    if output.risk_tier != "high" or output.high_stakes_domains:
        return []
    return [_failure(stage, StageFailureCode.RISK_HIGH_TIER_REQUIRES_DOMAIN, "high-risk classification must name at least one high-stakes domain.")]


def _budget_research_note(stage: str, output: BudgetPlan, context: dict[str, Any]) -> list[StageContractFailure]:
    request: RunRequest = context["request"]
    expected = (
        "synthetic_validation_only"
        if request.evidence_mode == "synthetic"
        else "live_full_candidate" if output.full_dr_equivalent else "live_scoped_only"
    )
    if output.research_completeness_note == expected:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.BUDGET_RESEARCH_NOTE_MISMATCH,
            f"budget research completeness note must be `{expected}` for the current request/evidence mode.",
            field="research_completeness_note",
        )
    ]


def _adapter_mirrors_request(stage: str, output: DomainAdapter, context: dict[str, Any]) -> list[StageContractFailure]:
    request: RunRequest = context["request"]
    failures: list[StageContractFailure] = []
    for field_name in ("topic", "reader", "use_context"):
        if getattr(output, field_name) != getattr(request, field_name):
            failures.append(
                _failure(
                    stage,
                    StageFailureCode.ADAPTER_REQUEST_MIRROR_MISMATCH,
                    f"domain adapter `{field_name}` must mirror the request.",
                    field=field_name,
                )
            )
    return failures


def _adapter_limitations(stage: str, output: DomainAdapter, context: dict[str, Any]) -> list[StageContractFailure]:
    budget: BudgetPlan = context["budget"]
    missing_limits = [item for item in budget.limitations if item not in output.known_limits]
    if not missing_limits:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.ADAPTER_LIMITATIONS_NOT_PROPAGATED,
            "domain adapter must carry forward every budget limitation into known_limits.",
            field="known_limits",
        )
    ]


def _strategy_aligns_adapter(stage: str, output: SourceStrategy, context: dict[str, Any]) -> list[StageContractFailure]:
    adapter: DomainAdapter = context["adapter"]
    failures: list[StageContractFailure] = []
    if output.source_priority != adapter.source_priority:
        failures.append(
            _failure(
                stage,
                StageFailureCode.STRATEGY_PRIORITY_MUST_ALIGN_ADAPTER,
                "source strategy priority must stay aligned with the domain adapter priority.",
                field="source_priority",
            )
        )
    return failures


def _strategy_role_map_aligns_adapter(stage: str, output: SourceStrategy, context: dict[str, Any]) -> list[StageContractFailure]:
    adapter: DomainAdapter = context["adapter"]
    if output.required_source_roles_by_claim_kind == adapter.source_roles_required_by_claim_kind:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.STRATEGY_ROLE_MAP_MUST_ALIGN_ADAPTER,
            "source strategy claim-kind role map must stay aligned with the domain adapter.",
            field="required_source_roles_by_claim_kind",
        )
    ]


def _evidence_lineage(stage: str, output: CollectedEvidence, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    source_ids = {source.source_id for source in output.sources}
    missing = sorted(
        {
            source_id
            for finding in output.findings
            for source_id in finding.source_ids
            if source_id not in source_ids
        }
    )
    if not missing:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.EVIDENCE_FINDING_SOURCE_LINEAGE,
            "evidence findings must only reference ingested source IDs.",
            field="findings",
        )
    ]


def _report_plan_sections(stage: str, output: Any, context: dict[str, Any]) -> list[StageContractFailure]:
    adapter: DomainAdapter = context["adapter"]
    keys = [section.key for section in output["sections"]]
    failures: list[StageContractFailure] = []
    if "uncertainty" not in keys:
        failures.append(
            _failure(stage, StageFailureCode.REPORT_PLAN_UNCERTAINTY_REQUIRED, "report plan must include an `uncertainty` section.")
        )
    if "decision_layer" not in keys:
        failures.append(
            _failure(stage, StageFailureCode.REPORT_PLAN_DECISION_LAYER_REQUIRED, "report plan must include a `decision_layer` section.")
        )
    if "Options or comparison table" in adapter.required_tables and "options" not in keys:
        failures.append(
            _failure(
                stage,
                StageFailureCode.REPORT_PLAN_OPTIONS_SECTION_REQUIRED,
                "report plan must include an `options` section when the adapter requires a comparison table.",
            )
        )
    return failures


def _draft_aligns_plan(stage: str, output: ReportDraft, context: dict[str, Any]) -> list[StageContractFailure]:
    report_plan: list[ReportSectionPlan] = context["report_plan"]
    expected_keys = [section.key for section in report_plan]
    actual_keys = [section.key for section in output.sections]
    if expected_keys == actual_keys:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.DRAFT_SECTIONS_MUST_ALIGN_PLAN,
            "draft sections must stay aligned with the report plan order and membership.",
            field="sections",
        )
    ]


def _draft_limitations_visible(stage: str, output: ReportDraft, context: dict[str, Any]) -> list[StageContractFailure]:
    budget: BudgetPlan = context["budget"]
    adapter: DomainAdapter = context["adapter"]
    expected_lines = [line for line in [*budget.limitations, *adapter.known_limits] if line]
    if not expected_lines:
        return []
    uncertainty_text = " ".join(unit.text for unit in output.units if unit.section_key == "uncertainty")
    if all(line in uncertainty_text for line in expected_lines):
        return []
    return [
        _failure(
            stage,
            StageFailureCode.DRAFT_LIMITATIONS_VISIBLE,
            "draft uncertainty section must surface every declared limitation/known limit.",
            field="units",
        )
    ]


def _claim_coverage(stage: str, output: Any, context: dict[str, Any]) -> list[StageContractFailure]:
    draft: ReportDraft = context["draft"]
    claim_unit_ids = {unit.unit_id for unit in draft.units if unit.is_claim}
    mapped_unit_ids = {claim.unit_id for claim in output["claims"]}
    if claim_unit_ids == mapped_unit_ids:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.CLAIM_LEDGER_COVERAGE_MISMATCH,
            "claim extractor must cover every claim-bearing draft unit exactly once.",
            field="claims",
        )
    ]


def _claim_normalization(stage: str, output: Any, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    for claim in output["claims"]:
        if claim.normalized_claim != normalize_text(claim.exact_text_span):
            return [
                _failure(
                    stage,
                    StageFailureCode.CLAIM_NORMALIZATION_MISMATCH,
                    "claim normalized text must be derived from exact_text_span.",
                    field="normalized_claim",
                )
            ]
    return []


def _citation_coverage(stage: str, output: Any, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    expected_pairs = {
        (claim.claim_id, source_id)
        for claim in output["claims"]
        for source_id in claim.source_ids
    }
    actual_pairs = {(citation.claim_id, citation.source_id) for citation in output["citations"]}
    if expected_pairs == actual_pairs:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.EVIDENCE_MAP_CITATION_COVERAGE_MISMATCH,
            "evidence mapping must emit one citation record per claim/source pair.",
            field="citations",
        )
    ]


def _guard_excludes_unsupported_high_risk(stage: str, output: Any, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    for claim in output["claims"]:
        if claim.risk_level == "high" and claim.support_status not in {"supported", "scoped_absence"} and claim.included_in_report:
            return [
                _failure(
                    stage,
                    StageFailureCode.GUARD_HIGH_RISK_UNSUPPORTED_EXCLUDED,
                    "high-risk claims below the support bar must be moved out of reader-facing prose.",
                    field="claims",
                )
            ]
    return []


def _guard_sync(stage: str, output: Any, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    draft_units = {unit.unit_id: unit for unit in output["draft"].units}
    for claim in output["claims"]:
        unit = draft_units.get(claim.unit_id)
        if unit is None:
            return [
                _failure(
                    stage,
                    StageFailureCode.GUARD_CLAIM_DRAFT_SYNC_BROKEN,
                    "guard output must keep claims synchronized with draft units.",
                    field="draft",
                )
            ]
        if unit.include_in_report != claim.included_in_report or unit.support_status_hint != claim.support_status:
            return [
                _failure(
                    stage,
                    StageFailureCode.GUARD_CLAIM_DRAFT_SYNC_BROKEN,
                    "guard output must keep claim include/support flags synchronized with draft units.",
                    field="draft",
                )
            ]
    return []


def _tone_weak_claims(stage: str, output: ReportDraft, context: dict[str, Any]) -> list[StageContractFailure]:
    claims: list[ClaimLedgerRow] = context["claims"]
    claim_by_unit_id = {claim.unit_id: claim for claim in claims}
    for unit in output.units:
        claim = claim_by_unit_id.get(unit.unit_id)
        if claim is None or not unit.include_in_report:
            continue
        if claim.support_status == "weak" and not unit.text.startswith("Current checked materials suggest"):
            return [
                _failure(
                    stage,
                    StageFailureCode.TONE_WEAK_CLAIM_PREFIX_REQUIRED,
                    "tone control must soften included weak claims with the standard prefix.",
                    field="units",
                )
            ]
    return []


def _tone_scoped_absence(stage: str, output: ReportDraft, context: dict[str, Any]) -> list[StageContractFailure]:
    claims: list[ClaimLedgerRow] = context["claims"]
    claim_by_unit_id = {claim.unit_id: claim for claim in claims}
    for unit in output.units:
        claim = claim_by_unit_id.get(unit.unit_id)
        if claim is None or not unit.include_in_report:
            continue
        if claim.support_status == "scoped_absence" and not unit.text.startswith("Within the checked scope"):
            return [
                _failure(
                    stage,
                    StageFailureCode.TONE_SCOPED_ABSENCE_REWRITE_REQUIRED,
                    "tone control must restate included scoped absences with explicit scope wording.",
                    field="units",
                )
            ]
    return []


def _metrics_target_misses(stage: str, output: MetricsSnapshot, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    expected_misses = sorted(key for key, passed in output.target_results.items() if not passed)
    if sorted(output.target_misses) == expected_misses:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.METRICS_TARGET_MISSES_ALIGN_RESULTS,
            "metrics target_misses must match the failed entries in target_results.",
            field="target_misses",
        )
    ]


def _release_synthetic(stage: str, output: ReleaseGateDecision, context: dict[str, Any]) -> list[StageContractFailure]:
    budget: BudgetPlan = context["budget"]
    if budget.evidence_mode != "synthetic" or output.status != "complete":
        return []
    return [
        _failure(
            stage,
            StageFailureCode.RELEASE_SYNTHETIC_NOT_COMPLETE,
            "synthetic runs must not return a `complete` release decision.",
            field="status",
        )
    ]


def _release_blocked_reason(stage: str, output: ReleaseGateDecision, context: dict[str, Any]) -> list[StageContractFailure]:
    del context
    if output.status != "blocked" or output.blocking_reasons:
        return []
    return [
        _failure(
            stage,
            StageFailureCode.RELEASE_BLOCKED_REASON_REQUIRED,
            "blocked release decisions must include blocking_reasons.",
            field="blocking_reasons",
        )
    ]


def _semantic_invariant(*categories: str) -> Callable[[str, Any, dict[str, Any]], list[StageContractFailure]]:
    def _evaluator(stage: str, output: Any, context: dict[str, Any]) -> list[StageContractFailure]:
        findings = detect_semantic_leakage(
            output,
            anchor_values=semantic_anchor_values(context.get("request"), context.get("evidence")),
            categories=categories or None,
            extra_patterns=context.get("semantic_patterns"),
        )
        return [
            StageContractFailure(
                stage=stage,
                code=finding.code,
                message=f"{stage} contains {finding.category.replace('_', ' ')} leakage via `{finding.phrase}`.",
                field="",
            )
            for finding in findings
        ]

    return _evaluator


def _failure(
    stage: str,
    code: StageFailureCode,
    message: str,
    *,
    field: str = "",
    downstream_stage: str = "",
) -> StageContractFailure:
    return StageContractFailure(
        stage=stage,
        code=code,
        message=message,
        field=field,
        downstream_stage=downstream_stage,
    )


def _resolve_path(value: Any, field_name: str) -> Any:
    current = value
    for part in field_name.split("."):
        if isinstance(current, dict):
            current = current.get(part, MISSING)
        else:
            current = getattr(current, part, MISSING)
        if current is MISSING:
            return MISSING
    return current


def _is_missing(value: Any) -> bool:
    if value is MISSING or value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    return False


def _snapshot_value(value: Any) -> Any:
    if value is MISSING:
        return None
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {
            "count": len(value),
            "keys": sorted(str(key) for key in value.keys()),
        }
    if isinstance(value, (list, tuple, set, frozenset)):
        return {
            "count": len(value),
            "item_type": type(next(iter(value), None)).__name__ if value else None,
        }
    if hasattr(value, "to_dict"):
        return _snapshot_value(value.to_dict())
    return type(value).__name__


STAGE_CONTRACTS: dict[str, StageContractSpec] = {
    "intent_classifier": StageContractSpec(
        artifact_type="IntentResult",
        required_fields=("intent_label", "decision_focus", "reader_task", "report_shape_hints"),
        downstream_must_have_fields={
            "risk_tier_classifier": ("intent_label", "reader_task"),
            "domain_adapter_generator": ("decision_focus", "reader_task"),
        },
        snapshot_fields=("intent_label", "decision_focus", "reader_task", "report_shape_hints"),
        schema_validator=lambda output, context: validate_intent_classification(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.INTENT_SHAPE_HINTS_REQUIRED,
                description="Intent stage must emit at least one shape hint.",
                evaluator=_intent_shape_hints,
            ),
        ),
    ),
    "risk_tier_classifier": StageContractSpec(
        artifact_type="RiskTierResult",
        required_fields=("risk_tier", "rationale"),
        downstream_must_have_fields={
            "scope_budget_planner": ("risk_tier",),
            "domain_adapter_generator": ("risk_tier",),
        },
        snapshot_fields=("risk_tier", "high_stakes_domains"),
        schema_validator=lambda output, context: validate_risk_classification(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.RISK_HIGH_TIER_REQUIRES_DOMAIN,
                description="High-risk classifications must name a high-stakes domain.",
                evaluator=_high_risk_domain,
            ),
        ),
    ),
    "scope_budget_planner": StageContractSpec(
        artifact_type="BudgetPlan",
        required_fields=(
            "requested_mode",
            "effective_mode",
            "effective_budget",
            "target_profile",
            "report_status_implication",
            "research_completeness_note",
        ),
        downstream_must_have_fields={
            "domain_adapter_generator": ("limitations", "research_completeness_note"),
            "report_planner": ("target_profile",),
        },
        snapshot_fields=(
            "requested_mode",
            "effective_mode",
            "full_dr_equivalent",
            "research_completeness_note",
            "limitations",
            "target_profile",
        ),
        schema_validator=lambda output, context: validate_budget_plan(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.BUDGET_RESEARCH_NOTE_MISMATCH,
                description="Budget stage must align research note with request/evidence mode.",
                evaluator=_budget_research_note,
            ),
        ),
    ),
    "domain_adapter_generator": StageContractSpec(
        artifact_type="DomainAdapter",
        required_fields=(
            "topic",
            "reader",
            "use_context",
            "source_priority",
            "required_decision_layer",
            "required_tables",
            "known_limits",
            "source_roles_required_by_claim_kind",
        ),
        downstream_must_have_fields={
            "source_strategy_builder": ("source_priority", "source_roles_required_by_claim_kind"),
            "report_planner": ("required_decision_layer", "required_tables"),
            "draft_generator": ("known_limits",),
        },
        snapshot_fields=(
            "topic",
            "risk_tier",
            "source_priority",
            "required_decision_layer",
            "required_tables",
            "known_limits",
        ),
        schema_validator=lambda output, context: validate_domain_adapter(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.ADAPTER_REQUEST_MIRROR_MISMATCH,
                description="Adapter must mirror request metadata.",
                evaluator=_adapter_mirrors_request,
            ),
            StageInvariantSpec(
                code=StageFailureCode.ADAPTER_LIMITATIONS_NOT_PROPAGATED,
                description="Adapter must preserve budget limitations.",
                evaluator=_adapter_limitations,
            ),
            StageInvariantSpec(
                code=StageFailureCode.SEMANTIC_FIXTURE_NOUN_LEAK,
                description="Adapter must not leak foreign fixture nouns or unrelated risk phrases.",
                evaluator=_semantic_invariant("fixture_specific_noun", "risk_phrase"),
                emitted_codes=(
                    StageFailureCode.SEMANTIC_FIXTURE_NOUN_LEAK,
                    StageFailureCode.SEMANTIC_RISK_PHRASE_LEAK,
                ),
            ),
        ),
    ),
    "source_strategy_builder": StageContractSpec(
        artifact_type="SourceStrategy",
        required_fields=("source_priority", "required_source_roles_by_claim_kind", "compatibility_notes"),
        downstream_must_have_fields={
            "claim_extractor": ("required_source_roles_by_claim_kind",),
            "evidence_mapper": ("required_source_roles_by_claim_kind",),
        },
        snapshot_fields=("source_priority", "required_source_roles_by_claim_kind", "compatibility_notes"),
        schema_validator=lambda output, context: validate_source_strategy(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.STRATEGY_PRIORITY_MUST_ALIGN_ADAPTER,
                description="Strategy must stay aligned with the adapter.",
                evaluator=_strategy_aligns_adapter,
            ),
            StageInvariantSpec(
                code=StageFailureCode.STRATEGY_ROLE_MAP_MUST_ALIGN_ADAPTER,
                description="Strategy claim-kind role map must stay aligned with the adapter.",
                evaluator=_strategy_role_map_aligns_adapter,
            ),
        ),
    ),
    "evidence_ingestion": StageContractSpec(
        artifact_type="CollectedEvidence",
        required_fields=("sources", "findings", "source_counts_by_role"),
        downstream_must_have_fields={
            "draft_generator": ("findings", "sources"),
            "evidence_mapper": ("sources",),
        },
        snapshot_fields=("sources", "findings", "source_counts_by_role", "quality_notes"),
        schema_validator=lambda output, context: validate_evidence_collection(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.EVIDENCE_FINDING_SOURCE_LINEAGE,
                description="Evidence findings must map back to ingested sources.",
                evaluator=_evidence_lineage,
            ),
        ),
    ),
    "report_planner": StageContractSpec(
        artifact_type="ReportSectionPlan[]",
        required_fields=("sections",),
        downstream_must_have_fields={"draft_generator": ("sections",)},
        snapshot_fields=("sections",),
        schema_validator=_validate_report_plan_payload,
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.REPORT_PLAN_UNCERTAINTY_REQUIRED,
                description="Report plan must include key control sections.",
                evaluator=_report_plan_sections,
                emitted_codes=(
                    StageFailureCode.REPORT_PLAN_UNCERTAINTY_REQUIRED,
                    StageFailureCode.REPORT_PLAN_DECISION_LAYER_REQUIRED,
                    StageFailureCode.REPORT_PLAN_OPTIONS_SECTION_REQUIRED,
                ),
            ),
        ),
    ),
    "draft_generator": StageContractSpec(
        artifact_type="ReportDraft",
        required_fields=("title", "sections", "units"),
        downstream_must_have_fields={
            "claim_extractor": ("units",),
            "tone_control": ("units",),
        },
        snapshot_fields=("title", "sections", "units"),
        schema_validator=lambda output, context: validate_report_draft(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.DRAFT_SECTIONS_MUST_ALIGN_PLAN,
                description="Draft sections must stay aligned with the plan.",
                evaluator=_draft_aligns_plan,
            ),
            StageInvariantSpec(
                code=StageFailureCode.DRAFT_LIMITATIONS_VISIBLE,
                description="Draft must keep declared limitations visible.",
                evaluator=_draft_limitations_visible,
            ),
        ),
    ),
    "claim_extractor": StageContractSpec(
        artifact_type="ClaimLedgerRow[]",
        required_fields=("claims",),
        downstream_must_have_fields={
            "evidence_mapper": ("claims",),
            "contradiction_absence_guard": ("claims",),
        },
        snapshot_fields=("claims",),
        schema_validator=_validate_claim_payload,
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.CLAIM_LEDGER_COVERAGE_MISMATCH,
                description="Claim extractor must cover every draft claim unit.",
                evaluator=_claim_coverage,
            ),
            StageInvariantSpec(
                code=StageFailureCode.CLAIM_NORMALIZATION_MISMATCH,
                description="Claim normalized text must match exact text.",
                evaluator=_claim_normalization,
            ),
        ),
    ),
    "evidence_mapper": StageContractSpec(
        artifact_type="EvidenceMapPayload",
        required_fields=("claims", "citations"),
        downstream_must_have_fields={
            "contradiction_absence_guard": ("claims",),
            "release_gate": ("citations",),
        },
        snapshot_fields=("claims", "citations"),
        schema_validator=_validate_evidence_map_payload,
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.EVIDENCE_MAP_CITATION_COVERAGE_MISMATCH,
                description="Evidence mapping must emit citations for every claim/source pair.",
                evaluator=_citation_coverage,
            ),
        ),
    ),
    "contradiction_absence_guard": StageContractSpec(
        artifact_type="GuardPayload",
        required_fields=("claims", "draft"),
        downstream_must_have_fields={
            "tone_control": ("draft", "claims"),
            "metrics_builder": ("claims",),
        },
        snapshot_fields=("claims", "draft", "contradictions", "gaps"),
        schema_validator=_validate_guard_payload,
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.GUARD_HIGH_RISK_UNSUPPORTED_EXCLUDED,
                description="Guard must exclude unsupported high-risk claims from the report.",
                evaluator=_guard_excludes_unsupported_high_risk,
            ),
            StageInvariantSpec(
                code=StageFailureCode.GUARD_CLAIM_DRAFT_SYNC_BROKEN,
                description="Guard must keep claims and draft units synchronized.",
                evaluator=_guard_sync,
            ),
        ),
    ),
    "tone_control": StageContractSpec(
        artifact_type="ReportDraft",
        required_fields=("title", "sections", "units"),
        downstream_must_have_fields={
            "metrics_builder": ("units",),
            "release_gate": ("units",),
        },
        snapshot_fields=("title", "sections", "units"),
        schema_validator=lambda output, context: validate_report_draft(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.TONE_WEAK_CLAIM_PREFIX_REQUIRED,
                description="Tone control must soften included weak claims.",
                evaluator=_tone_weak_claims,
            ),
            StageInvariantSpec(
                code=StageFailureCode.TONE_SCOPED_ABSENCE_REWRITE_REQUIRED,
                description="Tone control must make scoped absence language explicit.",
                evaluator=_tone_scoped_absence,
            ),
            StageInvariantSpec(
                code=StageFailureCode.SEMANTIC_FIXTURE_NOUN_LEAK,
                description="Tone-controlled draft must stay semantically isolated.",
                evaluator=_semantic_invariant(
                    "fixture_specific_noun",
                    "risk_phrase",
                    "regulation_wording",
                    "overclaim_phrasing",
                ),
                emitted_codes=(
                    StageFailureCode.SEMANTIC_FIXTURE_NOUN_LEAK,
                    StageFailureCode.SEMANTIC_RISK_PHRASE_LEAK,
                    StageFailureCode.SEMANTIC_REGULATION_WORDING_LEAK,
                    StageFailureCode.SEMANTIC_OVERCLAIM_PHRASING_LEAK,
                ),
            ),
        ),
    ),
    "metrics_builder": StageContractSpec(
        artifact_type="MetricsSnapshot",
        required_fields=("total_claim_count", "included_claim_count", "excluded_claim_count", "target_results", "target_misses"),
        downstream_must_have_fields={"release_gate": ("audit_complete", "citation_trace_complete", "target_misses")},
        snapshot_fields=(
            "total_claim_count",
            "included_claim_count",
            "excluded_claim_count",
            "unresolved_high_risk_claim_count",
            "target_misses",
        ),
        schema_validator=lambda output, context: validate_metrics(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.METRICS_TARGET_MISSES_ALIGN_RESULTS,
                description="Metrics target_misses must match failed target results.",
                evaluator=_metrics_target_misses,
            ),
        ),
    ),
    "release_gate": StageContractSpec(
        artifact_type="ReleaseGateDecision",
        required_fields=("status", "reasons"),
        downstream_must_have_fields={"bundle_renderer": ("status", "reasons")},
        snapshot_fields=("status", "reasons", "blocking_reasons", "unresolved_gaps"),
        schema_validator=lambda output, context: validate_release_decision(output),
        invariants=(
            StageInvariantSpec(
                code=StageFailureCode.RELEASE_SYNTHETIC_NOT_COMPLETE,
                description="Synthetic runs must never return a complete status.",
                evaluator=_release_synthetic,
            ),
            StageInvariantSpec(
                code=StageFailureCode.RELEASE_BLOCKED_REASON_REQUIRED,
                description="Blocked releases must include blocking reasons.",
                evaluator=_release_blocked_reason,
            ),
        ),
    ),
}
