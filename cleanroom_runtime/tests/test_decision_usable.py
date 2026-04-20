from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.core.gates.decision_usable import assess_decision_usable  # noqa: E402
from cleanroom_runtime.models import (  # noqa: E402
    AbsenceScope,
    CitationLedgerRow,
    ClaimLedgerRow,
    DomainAdapter,
    DomainDecisionContext,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
)


class DecisionUsableTests(unittest.TestCase):
    def test_reader_facing_draft_can_pass_decision_usable_rubric(self) -> None:
        result = assess_decision_usable(_draft(), [_claim("claim-001", "fact", "medium", "supported")], [_citation("claim-001")], adapter=_adapter())

        self.assertTrue(result.decision_usable)
        self.assertEqual(result.failed_checks, [])
        self.assertEqual(result.findings, [])

    def test_rubric_flags_missing_reader_layers_and_internal_headings(self) -> None:
        draft = ReportDraft(
            title="Synthetic draft",
            sections=[
                ReportSectionPlan(key="scope", title="Internal pipeline summary", purpose=""),
                ReportSectionPlan(key="decision_layer", title="Checks before you act", purpose=""),
            ],
            units=[
                ReportUnit(
                    unit_id="unit-001",
                    section_key="scope",
                    section_title="Internal pipeline summary",
                    text="This section stays vague about what the run covers.",
                    claim_kind="scope_boundary",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.9,
                    is_claim=False,
                )
            ],
        )

        result = assess_decision_usable(draft, [_claim("claim-001", "fact", "medium", "supported")], [_citation("claim-001")], adapter=_adapter())

        self.assertIn("direct_answer_present", result.failed_checks)
        self.assertIn("scope_and_exclusions_present", result.failed_checks)
        self.assertIn("no_internal_pipeline_headings", result.failed_checks)
        self.assertTrue(any("reader decision layer" in reason for reason in result.revision_reasons))

    def test_comparison_semantics_without_tradeoff_table_adds_revision_finding(self) -> None:
        result = assess_decision_usable(
            _draft(include_options=True),
            [_claim("claim-001", "comparison", "medium", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(required_tables=["Verification checklist", "Options or comparison table"]),
        )

        self.assertFalse(result.decision_usable)
        self.assertTrue(any(finding.code == "missing_tradeoff_table" for finding in result.findings))
        self.assertFalse(any(finding.blocks_release for finding in result.findings if finding.code == "missing_tradeoff_table"))

    def test_medical_guidance_without_authoritative_support_blocks(self) -> None:
        result = assess_decision_usable(
            _draft(),
            [
                _claim(
                    "claim-001",
                    "medical",
                    "high",
                    "supported",
                    matched_source_roles=[],
                )
            ],
            [
                CitationLedgerRow(
                    citation_id="citation-001",
                    claim_id="claim-001",
                    report_section="What the evidence supports",
                    source_id="SRC-001",
                    source_role="trade_media",
                    source_title="Synthetic source",
                    support_status="supported",
                    included_in_report=True,
                )
            ],
            adapter=_adapter(),
        )

        self.assertTrue(any(finding.code == "medical_without_authoritative_support" and finding.blocks_release for finding in result.findings))

    def test_medium_risk_finance_guidance_without_disclosure_needs_revision(self) -> None:
        result = assess_decision_usable(
            _draft(include_risk_disclosure=False),
            [_claim("claim-001", "financial", "medium", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(),
        )

        finding = next(finding for finding in result.findings if finding.code == "financial_without_risk_disclosure")
        self.assertFalse(finding.blocks_release)

    def test_high_risk_scoped_search_absence_blocks(self) -> None:
        result = assess_decision_usable(
            _draft(),
            [
                _claim(
                    "claim-001",
                    "absence",
                    "high",
                    "scoped_absence",
                    absence_scope=AbsenceScope(
                        subject="the target condition",
                        scope_label="scoped search",
                        basis="not_found_in_scoped_search",
                        checked_source_ids=["SRC-001"],
                    ),
                    matched_source_roles=["official_regulator"],
                )
            ],
            [_citation("claim-001")],
            adapter=_adapter(),
        )

        self.assertTrue(any(finding.code == "scoped_search_absence_in_mainline" and finding.blocks_release for finding in result.findings))


def _draft(*, include_options: bool = False, include_risk_disclosure: bool = True) -> ReportDraft:
    sections = [
        ReportSectionPlan(key="direct_answer", title="Direct answer", purpose=""),
        ReportSectionPlan(key="scope", title="Scope and exclusions", purpose=""),
        ReportSectionPlan(key="decision_layer", title="Checks before you act", purpose=""),
        ReportSectionPlan(key="checklist", title="Verification checklist", purpose=""),
        ReportSectionPlan(key="uncertainty", title="Limitations and uncertainty", purpose=""),
    ]
    units = [
        ReportUnit(
            unit_id="unit-001",
            section_key="direct_answer",
            section_title="Direct answer",
            text="The checked material supports a bounded answer for the reader.",
            claim_kind="scope_boundary",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            is_claim=False,
        ),
        ReportUnit(
            unit_id="unit-002",
            section_key="scope",
            section_title="Scope and exclusions",
            text="Excluded from this run are unchecked jurisdictions, unchecked dates, and claims that still need stronger support.",
            claim_kind="scope_boundary",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            is_claim=False,
        ),
        ReportUnit(
            unit_id="unit-003",
            section_key="decision_layer",
            section_title="Checks before you act",
            text="Next action: verify support before acting.",
            claim_kind="advice",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.8,
            is_claim=False,
        ),
        ReportUnit(
            unit_id="unit-004",
            section_key="checklist",
            section_title="Verification checklist",
            text="Verify claim-kind source-role fit before acting on any high-risk statement.",
            claim_kind="advice",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.8,
            is_claim=False,
        ),
        ReportUnit(
            unit_id="unit-005",
            section_key="uncertainty",
            section_title="Limitations and uncertainty",
            text="Uncertainty remains wherever the checked materials do not establish exhaustive coverage outside the declared scope.",
            claim_kind="scope_boundary",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            is_claim=False,
        ),
    ]
    if include_risk_disclosure:
        units.append(
            ReportUnit(
                unit_id="unit-006",
                section_key="uncertainty",
                section_title="Limitations and uncertainty",
                text="Risk disclosure: downside and suitability still depend on the reader's constraints.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            )
        )
    if include_options:
        sections.append(ReportSectionPlan(key="options", title="Options compared", purpose=""))
        units.extend(
            [
                ReportUnit(
                    unit_id="unit-007",
                    section_key="options",
                    section_title="Options compared",
                    text="Option A favors lower setup cost.",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
                ReportUnit(
                    unit_id="unit-008",
                    section_key="options",
                    section_title="Options compared",
                    text="Option B favors lower operating overhead.",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
            ]
        )
    return ReportDraft(title="Synthetic draft", sections=sections, units=units)


def _claim(
    claim_id: str,
    claim_kind: str,
    risk_level: str,
    support_status: str,
    *,
    absence_scope=None,
    matched_source_roles: list[str] | None = None,
) -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id=claim_id,
        unit_id=claim_id.replace("claim", "unit"),
        report_section="What the evidence supports",
        exact_text_span="Synthetic claim text.",
        normalized_claim="synthetic claim text.",
        claim_kind=claim_kind,
        risk_level=risk_level,
        source_ids=["SRC-001"],
        source_roles=["official_regulator" if risk_level == "high" else "government_context"],
        evidence_count=1,
        required_source_roles=["official_regulator"] if risk_level == "high" else ["government_context"],
        matched_source_roles=matched_source_roles if matched_source_roles is not None else (["official_regulator"] if support_status == "supported" and risk_level == "high" else []),
        support_status=support_status,
        confidence=0.9,
        caveat_required=support_status != "supported",
        suggested_tone="standard",
        required_fix="",
        included_in_report=True,
        absence_scope=absence_scope,
    )


def _citation(claim_id: str) -> CitationLedgerRow:
    return CitationLedgerRow(
        citation_id="citation-001",
        claim_id=claim_id,
        report_section="What the evidence supports",
        source_id="SRC-001",
        source_role="official_regulator",
        source_title="Synthetic source",
        support_status="supported",
        included_in_report=True,
    )


def _adapter(*, required_tables: list[str] | None = None) -> DomainAdapter:
    return DomainAdapter(
        topic="Synthetic topic",
        reader="reviewer",
        use_context="test decision usable",
        output_type="report",
        risk_tier="high",
        temporal_sensitivity="medium",
        jurisdiction_sensitivity="medium",
        source_priority=["official_regulator"],
        high_risk_claim_types=["regulatory"],
        likely_failure_modes=["role mismatch"],
        domain_specific_risks=["unsupported high-risk claim"],
        common_misunderstandings=["claim capture is not support"],
        boundary_concepts=["capture vs support"],
        decision_context=DomainDecisionContext(
            primary_decision="release or block",
            failure_cost="high",
            time_horizon="near-term",
            reader_action="verify support",
        ),
        required_decision_layer=["What is safe to say"],
        required_tables=required_tables or ["Verification checklist"],
        must_not_overgeneralize=["Do not treat weak support as complete."],
        known_limits=[],
        source_roles_required_by_claim_kind={"regulatory": ["official_regulator"]},
    )


if __name__ == "__main__":
    unittest.main()
