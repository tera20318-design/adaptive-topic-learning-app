from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.models import (  # noqa: E402
    AbsenceScope,
    ClaimLedgerRow,
    CollectedEvidence,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    RunRequest,
    SourceFinding,
    SourcePacket,
    SourcePacketProvenance,
)
from cleanroom_runtime.stages.contradiction_absence_guard import apply_contradiction_absence_guard  # noqa: E402


class ContradictionHardeningV3Tests(unittest.TestCase):
    def test_stale_authoritative_yields_to_fresh_authoritative_on_same_subject(self) -> None:
        claims, _, contradictions, gaps = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    exact_text_span="The checked rule remains in force for the bounded workflow.",
                    claim_kind="regulatory",
                    risk_level="high",
                    subject_key="bounded workflow rule",
                    source_ids=["SRC-001"],
                    source_roles=["official_regulator"],
                    freshness_tag="stale",
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    exact_text_span="The checked rule does not apply to the bounded workflow.",
                    claim_kind="regulatory",
                    risk_level="high",
                    subject_key="bounded workflow rule",
                    source_ids=["SRC-002"],
                    source_roles=["official_regulator"],
                    freshness_tag="fresh",
                ),
            ],
            draft=_draft(
                [
                    ("unit-001", "The checked rule remains in force for the bounded workflow.", "high", "SRC-001", "official_regulator"),
                    ("unit-002", "The checked rule does not apply to the bounded workflow.", "high", "SRC-002", "official_regulator"),
                ]
            ),
            request=_request(),
            evidence=_evidence(
                sources=[
                    _source("SRC-001", "official_regulator", published_on="2024-02-01", stale=True, jurisdiction="US"),
                    _source("SRC-002", "official_regulator", published_on="2026-03-01", jurisdiction="US"),
                ]
            ),
        )

        stale_claim = next(claim for claim in claims if claim.claim_id == "claim-001")
        fresh_claim = next(claim for claim in claims if claim.claim_id == "claim-002")

        self.assertEqual(stale_claim.support_status, "weak")
        self.assertFalse(stale_claim.included_in_report)
        self.assertTrue(stale_claim.caveat_required)
        self.assertEqual(fresh_claim.support_status, "supported")
        self.assertTrue(fresh_claim.caveat_required)
        self.assertTrue(any(entry.contradiction_class == "fresh_authoritative_override" for entry in contradictions))
        self.assertTrue(any(gap.gap_type == "stale_current_tension" for gap in gaps))

    def test_stale_authoritative_vs_fresh_lower_role_requires_caveat(self) -> None:
        claims, _, contradictions, gaps = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    exact_text_span="The checked rule applies to the workflow.",
                    claim_kind="regulatory",
                    risk_level="high",
                    subject_key="workflow-rule",
                    source_ids=["SRC-001"],
                    source_roles=["official_regulator"],
                    freshness_tag="stale",
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    exact_text_span="The checked rule does not apply to the workflow.",
                    claim_kind="regulatory",
                    risk_level="high",
                    subject_key="workflow-rule",
                    source_ids=["SRC-002"],
                    source_roles=["secondary_media"],
                    freshness_tag="fresh",
                ),
            ],
            draft=_draft(
                [
                    ("unit-001", "The checked rule applies to the workflow.", "high", "SRC-001", "official_regulator"),
                    ("unit-002", "The checked rule does not apply to the workflow.", "high", "SRC-002", "secondary_media"),
                ]
            ),
            request=_request(),
            evidence=_evidence(
                sources=[
                    _source("SRC-001", "official_regulator", published_on="2024-01-11", stale=True, jurisdiction="US"),
                    _source("SRC-002", "secondary_media", published_on="2026-03-11", jurisdiction="US"),
                ]
            ),
        )

        authoritative_claim = next(claim for claim in claims if claim.claim_id == "claim-001")
        lower_claim = next(claim for claim in claims if claim.claim_id == "claim-002")

        self.assertEqual(authoritative_claim.support_status, "supported")
        self.assertTrue(authoritative_claim.caveat_required)
        self.assertEqual(lower_claim.support_status, "weak")
        self.assertFalse(lower_claim.included_in_report)
        self.assertTrue(
            any(entry.contradiction_class == "stale_authoritative_vs_fresh_lower_role_tension" for entry in contradictions)
        )
        self.assertTrue(
            any(gap.gap_type == "stale_current_tension" and gap.release_impact == "needs_revision" for gap in gaps)
        )

    def test_mixed_subject_boundary_does_not_inflate_contradiction(self) -> None:
        claims, _, contradictions, _ = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    exact_text_span="The checked rule applies.",
                    claim_kind="regulatory",
                    risk_level="high",
                    source_ids=["SRC-001"],
                    source_roles=["official_regulator"],
                    origin_finding_ids=["finding-001"],
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    exact_text_span="The checked rule does not apply.",
                    claim_kind="regulatory",
                    risk_level="high",
                    source_ids=["SRC-002"],
                    source_roles=["official_regulator"],
                    origin_finding_ids=["finding-002"],
                ),
            ],
            draft=_draft(
                [
                    ("unit-001", "The checked rule applies.", "high", "SRC-001", "official_regulator"),
                    ("unit-002", "The checked rule does not apply.", "high", "SRC-002", "official_regulator"),
                ]
            ),
            request=_request(),
            evidence=_evidence(
                sources=[
                    _source("SRC-001", "official_regulator", published_on="2026-03-01", jurisdiction="US"),
                    _source("SRC-002", "official_regulator", published_on="2026-03-02", jurisdiction="US"),
                ],
                findings=[
                    _finding("finding-001", "subject-alpha|workflow-a"),
                    _finding("finding-002", "subject-alpha|workflow-b"),
                ],
            ),
        )

        self.assertEqual(contradictions, [])
        self.assertTrue(all(claim.support_status == "supported" for claim in claims))

    def test_authoritative_absence_without_explicit_scope_statement_blocks(self) -> None:
        claims, _, _, gaps = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    exact_text_span="No checked official source required the waiver.",
                    claim_kind="absence",
                    risk_level="high",
                    source_ids=["SRC-001"],
                    source_roles=["official_regulator"],
                    absence_type="not_found_in_official_source_checked",
                    absence_scope=AbsenceScope(
                        subject="",
                        scope_label="",
                        basis="not_found_in_official_source_checked",
                        checked_source_ids=["SRC-001"],
                        checked_roles=["official_regulator"],
                        scope_note="Checked source IDs exist, but the scope statement was omitted.",
                    ),
                )
            ],
            draft=_draft([("unit-001", "No checked official source required the waiver.", "high", "SRC-001", "official_regulator")], claim_kind="absence"),
            request=_request(),
            evidence=_evidence(
                sources=[_source("SRC-001", "official_regulator", published_on="2026-03-01", jurisdiction="US")]
            ),
        )

        self.assertEqual(claims[0].support_status, "missing")
        self.assertFalse(claims[0].included_in_report)
        self.assertTrue(
            any(gap.gap_type == "authoritative_absence_missing_scope_statement" and gap.blocking for gap in gaps)
        )

    def test_historical_source_used_as_current_without_caveat_creates_revision_gap(self) -> None:
        claims, _, contradictions, gaps = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    exact_text_span="The 2019 archive review currently settles the route history.",
                    claim_kind="fact",
                    risk_level="medium",
                    subject_key="route-history",
                    source_ids=["SRC-001"],
                    source_roles=["academic_review"],
                )
            ],
            draft=_draft([("unit-001", "The 2019 archive review currently settles the route history.", "medium", "SRC-001", "academic_review")], claim_kind="fact"),
            request=_request(),
            evidence=_evidence(
                sources=[_source("SRC-001", "academic_review", published_on="2019-07-09", stale=True, jurisdiction="JP")]
            ),
        )

        self.assertEqual(contradictions, [])
        self.assertTrue(claims[0].caveat_required)
        self.assertTrue(
            any(gap.gap_type == "historical_source_used_as_current" and gap.release_impact == "needs_revision" for gap in gaps)
        )

    def test_mixed_jurisdiction_conflict_does_not_collapse_into_same_subject_contradiction(self) -> None:
        claims, _, contradictions, _ = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    exact_text_span="The checked notice rule applies.",
                    claim_kind="regulatory",
                    risk_level="high",
                    subject_key="notice-rule",
                    source_ids=["SRC-001"],
                    source_roles=["official_regulator"],
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    exact_text_span="The checked notice rule does not apply.",
                    claim_kind="regulatory",
                    risk_level="high",
                    subject_key="notice-rule",
                    source_ids=["SRC-002"],
                    source_roles=["official_regulator"],
                ),
            ],
            draft=_draft(
                [
                    ("unit-001", "The checked notice rule applies.", "high", "SRC-001", "official_regulator"),
                    ("unit-002", "The checked notice rule does not apply.", "high", "SRC-002", "official_regulator"),
                ]
            ),
            request=_request(jurisdiction=""),
            evidence=_evidence(
                sources=[
                    _source("SRC-001", "official_regulator", published_on="2026-03-01", jurisdiction="US"),
                    _source("SRC-002", "official_regulator", published_on="2026-03-02", jurisdiction="CA"),
                ]
            ),
        )

        self.assertEqual(contradictions, [])
        self.assertTrue(all(claim.support_status == "supported" for claim in claims))


def _request(*, jurisdiction: str = "US") -> RunRequest:
    return RunRequest(
        topic="Synthetic topic",
        reader="Synthetic reader",
        use_context="Synthetic context",
        desired_depth="decision",
        jurisdiction=jurisdiction,
        mode="scoped",
        evidence_mode="live_lite",
    )


def _draft(
    rows: list[tuple[str, str, str, str, str]],
    *,
    claim_kind: str = "regulatory",
) -> ReportDraft:
    return ReportDraft(
        title="Synthetic draft",
        sections=[ReportSectionPlan(key="direct_answer", title="Direct answer", purpose="")],
        units=[
            ReportUnit(
                unit_id=unit_id,
                section_key="direct_answer",
                section_title="Direct answer",
                text=text,
                claim_kind=claim_kind,
                risk_level=risk_level,
                source_ids=[source_id],
                source_roles=[source_role],
                confidence=0.9,
            )
            for unit_id, text, risk_level, source_id, source_role in rows
        ],
    )


def _claim(
    *,
    claim_id: str,
    unit_id: str,
    exact_text_span: str,
    claim_kind: str,
    risk_level: str,
    source_ids: list[str],
    source_roles: list[str],
    subject_key: str = "",
    freshness_tag: str = "",
    absence_type: str = "",
    absence_scope: AbsenceScope | None = None,
    origin_finding_ids: list[str] | None = None,
) -> ClaimLedgerRow:
    required_roles = ["official_regulator"] if risk_level == "high" else ["government_context"]
    matched_roles = [role for role in source_roles if role in required_roles]
    return ClaimLedgerRow(
        claim_id=claim_id,
        unit_id=unit_id,
        report_section="Direct answer",
        exact_text_span=exact_text_span,
        normalized_claim=exact_text_span.lower(),
        claim_kind=claim_kind,
        risk_level=risk_level,
        source_ids=list(source_ids),
        source_roles=list(source_roles),
        evidence_count=len(source_ids),
        required_source_roles=required_roles,
        matched_source_roles=matched_roles,
        support_status="supported",
        confidence=0.9,
        caveat_required=False,
        suggested_tone="standard",
        required_fix="",
        subject_key=subject_key,
        freshness_tag=freshness_tag,
        absence_type=absence_type,
        absence_scope=absence_scope,
        origin_finding_ids=list(origin_finding_ids or []),
        report_section_key="direct_answer",
    )


def _source(
    source_id: str,
    source_role: str,
    *,
    published_on: str,
    stale: bool = False,
    jurisdiction: str = "",
) -> SourcePacket:
    return SourcePacket(
        source_id=source_id,
        title=f"Source {source_id}",
        source_role=source_role,
        published_on=published_on,
        jurisdiction=jurisdiction,
        provenance=SourcePacketProvenance(stale=stale, stale_reason="Marked stale for contradiction hardening." if stale else ""),
    )


def _finding(finding_id: str, subject_scope_key: str) -> SourceFinding:
    return SourceFinding(
        finding_id=finding_id,
        statement=f"{finding_id} statement",
        claim_kind="regulatory",
        risk_level="high",
        subject_scope_key=subject_scope_key,
    )


def _evidence(
    *,
    sources: list[SourcePacket],
    findings: list[SourceFinding] | None = None,
) -> CollectedEvidence:
    return CollectedEvidence(sources=sources, findings=list(findings or []), source_counts_by_role={}, quality_notes=[])


if __name__ == "__main__":
    unittest.main()
