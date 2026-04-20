from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.models import (  # noqa: E402
    ClaimLedgerRow,
    CollectedEvidence,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    RunRequest,
)
from cleanroom_runtime.stages.contradiction_absence_guard import apply_contradiction_absence_guard  # noqa: E402
from cleanroom_runtime.stages.evidence_semantics import build_claim_audit_rows  # noqa: E402


class ContradictionAbsenceGuardTests(unittest.TestCase):
    def test_unsupported_high_risk_claim_stays_in_audit_when_excluded(self) -> None:
        claims, _, _, _ = apply_contradiction_absence_guard(
            claims=[
                ClaimLedgerRow(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    report_section="Direct answer",
                    exact_text_span="Synthetic claim text.",
                    normalized_claim="synthetic claim text.",
                    claim_kind="regulatory",
                    risk_level="high",
                    source_ids=["SRC-001"],
                    source_roles=["academic_review"],
                    evidence_count=1,
                    required_source_roles=["official_regulator"],
                    matched_source_roles=[],
                    support_status="weak",
                    confidence=0.9,
                    caveat_required=True,
                    suggested_tone="tentative",
                    required_fix="Add role-matched support.",
                    blocking_reasons=["claim-001 role mismatch"],
                )
            ],
            draft=_draft(),
            request=_request(),
            evidence=CollectedEvidence(),
        )

        audit_rows = build_claim_audit_rows(claims)

        self.assertEqual(len(audit_rows), 1)
        self.assertFalse(claims[0].included_in_report)
        self.assertIn("claim-001", audit_rows[0].blocking_reasons[0])

    def test_search_based_absence_without_scope_trips_false_negative_guard(self) -> None:
        claims, draft, _, gaps = apply_contradiction_absence_guard(
            claims=[
                ClaimLedgerRow(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    report_section="Direct answer",
                    exact_text_span="Synthetic absence.",
                    normalized_claim="synthetic absence.",
                    claim_kind="absence",
                    risk_level="high",
                    source_ids=["SRC-001"],
                    source_roles=["official_regulator"],
                    evidence_count=1,
                    required_source_roles=["official_regulator"],
                    matched_source_roles=["official_regulator"],
                    support_status="supported",
                    confidence=0.9,
                    caveat_required=False,
                    suggested_tone="scoped_absence",
                    required_fix="",
                )
            ],
            draft=_draft(claim_kind="absence"),
            request=_request(jurisdiction="US"),
            evidence=CollectedEvidence(),
        )

        self.assertEqual(claims[0].support_status, "missing")
        self.assertFalse(claims[0].included_in_report)
        self.assertEqual(draft.units[0].support_status_hint, "missing")
        self.assertTrue(any(gap.gap_type == "absence_false_negative_risk" for gap in gaps))
        self.assertTrue(any("false negative" in reason for reason in claims[0].blocking_reasons))


def _request(*, jurisdiction: str = "") -> RunRequest:
    return RunRequest(
        topic="Synthetic topic",
        reader="Synthetic reader",
        use_context="Synthetic use context",
        desired_depth="scoped",
        jurisdiction=jurisdiction,
        mode="scoped",
        evidence_mode="live",
    )


def _draft(*, claim_kind: str = "regulatory") -> ReportDraft:
    return ReportDraft(
        title="Synthetic draft",
        sections=[ReportSectionPlan(key="direct_answer", title="Direct answer", purpose="")],
        units=[
            ReportUnit(
                unit_id="unit-001",
                section_key="direct_answer",
                section_title="Direct answer",
                text="Synthetic claim text.",
                claim_kind=claim_kind,
                risk_level="high",
                source_ids=["SRC-001"],
                source_roles=["official_regulator"],
                confidence=0.9,
            )
        ],
    )


if __name__ == "__main__":
    unittest.main()
