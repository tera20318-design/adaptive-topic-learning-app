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
    ClaimLedgerRow,
    CitationLedgerRow,
    DomainAdapter,
    DomainDecisionContext,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
)


class DecisionUsableQualityTests(unittest.TestCase):
    def test_checklist_items_must_align_with_reader_task(self) -> None:
        result = assess_decision_usable(
            _draft(
                checklist_lines=["Move quickly.", "Stay concise."],
                decision_lines=["Next action: review the packet text against the cited sources before deciding."],
            ),
            [_claim("claim-001", "fact", "medium", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(reader_action="ground the review in the packet text before deciding"),
        )

        self.assertTrue(any(finding.code == "checklist_not_aligned_to_reader_task" for finding in result.findings))

    def test_next_action_must_be_specific(self) -> None:
        result = assess_decision_usable(
            _draft(decision_lines=["Next step: do more research as needed."]),
            [_claim("claim-001", "fact", "medium", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(),
        )

        self.assertIn("next_action_or_next_research_present", result.failed_checks)

    def test_document_review_outputs_require_direct_grounding(self) -> None:
        result = assess_decision_usable(
            _draft(direct_answer_text="The answer is mixed for the reader."),
            [_claim("claim-001", "fact", "medium", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(use_context="review the document packet for grounded findings"),
        )

        self.assertTrue(any(finding.code == "document_review_without_grounding" for finding in result.findings))

    def test_recommendation_outputs_require_visible_risk_disclosure(self) -> None:
        result = assess_decision_usable(
            _draft(include_risk_disclosure=False),
            [_claim("claim-001", "recommendation", "medium", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(),
        )

        self.assertTrue(any(finding.code == "guidance_without_risk_disclosure" for finding in result.findings))

    def test_uncertainty_must_be_non_generic(self) -> None:
        result = assess_decision_usable(
            _draft(uncertainty_text="History is complex, interpretations vary, and more research is needed."),
            [_claim("claim-001", "fact", "low", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(),
        )

        self.assertIn("uncertainty_present", result.failed_checks)

    def test_comparison_quality_accepts_explicit_tradeoff_table(self) -> None:
        result = assess_decision_usable(
            _draft(include_tradeoff_table=True),
            [_claim("claim-001", "comparison", "medium", "supported")],
            [_citation("claim-001")],
            adapter=_adapter(required_tables=["Verification checklist", "Options or comparison table"]),
        )

        self.assertFalse(any(finding.code == "missing_tradeoff_table" for finding in result.findings))


def _draft(
    *,
    direct_answer_text: str = "The checked material supports a bounded answer for the reader.",
    decision_lines: list[str] | None = None,
    checklist_lines: list[str] | None = None,
    uncertainty_text: str = "Uncertainty remains wherever the checked materials do not establish exhaustive coverage outside the declared scope.",
    include_risk_disclosure: bool = True,
    include_tradeoff_table: bool = False,
) -> ReportDraft:
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
            text=direct_answer_text,
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
            text=(decision_lines or ["Next action: verify the cited support against the release decision before acting."])[0],
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
            text=(checklist_lines or ["Verify the packet text against the cited support before deciding."])[0],
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
            text=uncertainty_text,
            claim_kind="scope_boundary",
            risk_level="medium",
            source_ids=[],
            source_roles=[],
            confidence=0.9,
            is_claim=False,
        ),
    ]
    for index, line in enumerate((decision_lines or [])[1:], start=6):
        units.append(
            ReportUnit(
                unit_id=f"unit-{index:03d}",
                section_key="decision_layer",
                section_title="Checks before you act",
                text=line,
                claim_kind="advice",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.8,
                is_claim=False,
            )
        )
    for index, line in enumerate((checklist_lines or [])[1:], start=16):
        units.append(
            ReportUnit(
                unit_id=f"unit-{index:03d}",
                section_key="checklist",
                section_title="Verification checklist",
                text=line,
                claim_kind="advice",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.8,
                is_claim=False,
            )
        )
    if include_risk_disclosure:
        units.append(
            ReportUnit(
                unit_id="unit-030",
                section_key="uncertainty",
                section_title="Limitations and uncertainty",
                text="Risk disclosure: the downside and suitability still depend on the reader's constraints and tolerance for loss.",
                claim_kind="scope_boundary",
                risk_level="medium",
                source_ids=[],
                source_roles=[],
                confidence=0.9,
                is_claim=False,
            )
        )
    if include_tradeoff_table:
        sections.append(ReportSectionPlan(key="options", title="Options compared", purpose=""))
        units.extend(
            [
                ReportUnit(
                    unit_id="unit-040",
                    section_key="options",
                    section_title="Options compared",
                    text="Option | Main tradeoff | Downside",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
                ReportUnit(
                    unit_id="unit-041",
                    section_key="options",
                    section_title="Options compared",
                    text="Option A | Lower setup cost tradeoff | Higher maintenance downside",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
                ReportUnit(
                    unit_id="unit-042",
                    section_key="options",
                    section_title="Options compared",
                    text="Option B | Higher setup cost tradeoff | Lower maintenance downside",
                    claim_kind="comparison",
                    risk_level="medium",
                    source_ids=[],
                    source_roles=[],
                    confidence=0.8,
                    is_claim=False,
                ),
            ]
        )
    return ReportDraft(title="Synthetic quality draft", sections=sections, units=units)


def _claim(claim_id: str, claim_kind: str, risk_level: str, support_status: str) -> ClaimLedgerRow:
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
        matched_source_roles=["official_regulator"] if support_status == "supported" and risk_level == "high" else ["government_context"],
        support_status=support_status,
        confidence=0.9,
        caveat_required=support_status != "supported",
        suggested_tone="standard",
        required_fix="",
        included_in_report=True,
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


def _adapter(*, reader_action: str = "verify the checked support before deciding", required_tables: list[str] | None = None, use_context: str = "test decision usable quality") -> DomainAdapter:
    return DomainAdapter(
        topic="Synthetic topic",
        reader="reviewer",
        use_context=use_context,
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
            primary_decision="support a bounded decision",
            failure_cost="high",
            time_horizon="near-term",
            reader_action=reader_action,
        ),
        required_decision_layer=["What is safe to say"],
        required_tables=required_tables or ["Verification checklist"],
        must_not_overgeneralize=["Do not treat weak support as complete."],
        known_limits=[],
        source_roles_required_by_claim_kind={"regulatory": ["official_regulator"]},
    )


if __name__ == "__main__":
    unittest.main()
