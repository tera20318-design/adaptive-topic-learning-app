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
    SourcePacket,
)
from cleanroom_runtime.stages.contradiction_absence_guard import apply_contradiction_absence_guard  # noqa: E402


class ContradictionHardeningV2Tests(unittest.TestCase):
    def test_same_subject_authoritative_conflict_marks_blocking_signal(self) -> None:
        claims, _, contradictions, _ = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    normalized_claim="the requirement applies",
                    claim_kind="regulatory",
                    subject_key="requirement-x",
                    source_roles=["official_regulator"],
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    normalized_claim="the requirement does not apply",
                    claim_kind="regulatory",
                    subject_key="requirement-x",
                    source_roles=["official_regulator"],
                ),
            ],
            draft=_draft(["unit-001", "unit-002"]),
            request=_request(),
            evidence=_evidence(
                [
                    _source("SRC-001", "official_regulator", published_on="2026-01-01"),
                    _source("SRC-002", "official_regulator", published_on="2026-01-01"),
                ]
            ),
        )

        self.assertEqual(claims[0].support_status, "contradicted")
        self.assertEqual(claims[1].support_status, "contradicted")
        self.assertFalse(claims[0].included_in_report)
        self.assertFalse(claims[1].included_in_report)
        self.assertTrue(
            any(
                entry.contradiction_class == "same_subject_authoritative_conflict"
                and entry.subject_relation == "same_subject"
                and entry.severity == "critical"
                and entry.severity_score >= 90
                for entry in contradictions
            )
        )

    def test_different_subject_claims_do_not_create_same_subject_conflict(self) -> None:
        claims, _, contradictions, _ = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    normalized_claim="the requirement applies",
                    claim_kind="regulatory",
                    subject_key="requirement-x",
                    source_roles=["official_regulator"],
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    normalized_claim="the requirement does not apply",
                    claim_kind="regulatory",
                    subject_key="requirement-y",
                    source_roles=["official_regulator"],
                ),
            ],
            draft=_draft(["unit-001", "unit-002"]),
            request=_request(),
            evidence=_evidence(
                [
                    _source("SRC-001", "official_regulator", published_on="2026-01-01"),
                    _source("SRC-002", "official_regulator", published_on="2026-01-01"),
                ]
            ),
        )

        self.assertEqual(claims[0].support_status, "supported")
        self.assertEqual(claims[1].support_status, "supported")
        self.assertEqual(contradictions, [])

    def test_fresh_authoritative_source_overrides_stale_authoritative_source(self) -> None:
        claims, _, contradictions, _ = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    normalized_claim="the status applies",
                    claim_kind="regulatory",
                    subject_key="status-z",
                    source_roles=["official_regulator"],
                    freshness_tag="fresh",
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    normalized_claim="the status does not apply",
                    claim_kind="regulatory",
                    subject_key="status-z",
                    source_roles=["official_regulator"],
                    freshness_tag="stale",
                ),
            ],
            draft=_draft(["unit-001", "unit-002"]),
            request=_request(),
            evidence=_evidence(
                [
                    _source("SRC-001", "official_regulator", published_on="2026-02-01"),
                    _source("SRC-002", "official_regulator", published_on="2024-02-01"),
                ]
            ),
        )

        fresh_claim = next(claim for claim in claims if claim.claim_id == "claim-001")
        stale_claim = next(claim for claim in claims if claim.claim_id == "claim-002")

        self.assertEqual(fresh_claim.support_status, "supported")
        self.assertTrue(fresh_claim.caveat_required)
        self.assertEqual(stale_claim.support_status, "weak")
        self.assertFalse(stale_claim.included_in_report)
        self.assertTrue(
            any(entry.contradiction_class == "fresh_authoritative_override" for entry in contradictions)
        )

    def test_stale_authoritative_vs_fresh_lower_role_creates_tension_not_override(self) -> None:
        claims, _, contradictions, _ = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    normalized_claim="the condition applies",
                    claim_kind="regulatory",
                    subject_key="condition-a",
                    source_roles=["official_regulator"],
                    freshness_tag="stale",
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    normalized_claim="the condition does not apply",
                    claim_kind="regulatory",
                    subject_key="condition-a",
                    source_roles=["secondary_media"],
                    freshness_tag="fresh",
                ),
            ],
            draft=_draft(["unit-001", "unit-002"]),
            request=_request(),
            evidence=_evidence(
                [
                    _source("SRC-001", "official_regulator", published_on="2024-02-01"),
                    _source("SRC-002", "secondary_media", published_on="2026-02-01"),
                ]
            ),
        )

        authoritative_claim = next(claim for claim in claims if claim.claim_id == "claim-001")
        lower_role_claim = next(claim for claim in claims if claim.claim_id == "claim-002")

        self.assertEqual(authoritative_claim.support_status, "supported")
        self.assertTrue(authoritative_claim.caveat_required)
        self.assertEqual(lower_role_claim.support_status, "weak")
        self.assertTrue(
            any(
                entry.contradiction_class == "stale_authoritative_vs_fresh_lower_role_tension"
                for entry in contradictions
            )
        )

    def test_scoped_search_absence_stays_weaker_than_checked_authoritative_absence(self) -> None:
        claims, _, _, gaps = apply_contradiction_absence_guard(
            claims=[
                _claim(
                    claim_id="claim-001",
                    unit_id="unit-001",
                    normalized_claim="no requirement found",
                    claim_kind="absence",
                    subject_key="requirement-b",
                    source_roles=["official_regulator"],
                    absence_type="not_found_in_scoped_search",
                    absence_scope=AbsenceScope(
                        subject="requirement-b",
                        scope_label="keyword search",
                        basis="not_found_in_scoped_search",
                        checked_source_ids=["SRC-001"],
                    ),
                ),
                _claim(
                    claim_id="claim-002",
                    unit_id="unit-002",
                    normalized_claim="no requirement found in checked authority",
                    claim_kind="absence",
                    subject_key="requirement-c",
                    source_roles=["official_regulator"],
                    absence_type="not_found_in_official_source_checked",
                    absence_scope=AbsenceScope(
                        subject="requirement-c",
                        scope_label="checked authority",
                        basis="not_found_in_official_source_checked",
                        checked_source_ids=["SRC-002"],
                    ),
                ),
            ],
            draft=_draft(["unit-001", "unit-002"], claim_kind="absence"),
            request=_request(),
            evidence=_evidence(
                [
                    _source("SRC-001", "official_regulator", published_on="2026-01-01"),
                    _source("SRC-002", "official_regulator", published_on="2026-01-01"),
                ]
            ),
        )

        scoped_search_claim = next(claim for claim in claims if claim.claim_id == "claim-001")
        authoritative_absence_claim = next(claim for claim in claims if claim.claim_id == "claim-002")

        self.assertEqual(scoped_search_claim.support_status, "missing")
        self.assertEqual(authoritative_absence_claim.support_status, "scoped_absence")
        self.assertTrue(any(gap.gap_type == "scoped_search_absence" and gap.blocking for gap in gaps))
        self.assertFalse(any(gap.gap_type == "authoritative_checked_absence" for gap in gaps))


def _request() -> RunRequest:
    return RunRequest(
        topic="Synthetic topic",
        reader="Synthetic reader",
        use_context="Synthetic context",
        desired_depth="scoped",
        mode="scoped",
        evidence_mode="live_lite",
    )


def _draft(unit_ids: list[str], *, claim_kind: str = "regulatory") -> ReportDraft:
    return ReportDraft(
        title="Synthetic draft",
        sections=[ReportSectionPlan(key="direct_answer", title="Direct answer", purpose="")],
        units=[
            ReportUnit(
                unit_id=unit_id,
                section_key="direct_answer",
                section_title="Direct answer",
                text=f"Synthetic text for {unit_id}.",
                claim_kind=claim_kind,
                risk_level="high",
                source_ids=[f"SRC-{index + 1:03d}"],
                source_roles=["official_regulator"],
                confidence=0.9,
            )
            for index, unit_id in enumerate(unit_ids)
        ],
    )


def _claim(
    *,
    claim_id: str,
    unit_id: str,
    normalized_claim: str,
    claim_kind: str,
    subject_key: str,
    source_roles: list[str],
    freshness_tag: str = "",
    absence_type: str = "",
    absence_scope: AbsenceScope | None = None,
) -> ClaimLedgerRow:
    return ClaimLedgerRow(
        claim_id=claim_id,
        unit_id=unit_id,
        report_section="Direct answer",
        exact_text_span=normalized_claim,
        normalized_claim=normalized_claim,
        claim_kind=claim_kind,
        risk_level="high",
        source_ids=[claim_id.replace("claim", "SRC")],
        source_roles=list(source_roles),
        evidence_count=1,
        required_source_roles=["official_regulator"],
        matched_source_roles=["official_regulator"] if "official_regulator" in source_roles else [],
        support_status="supported",
        confidence=0.9,
        caveat_required=False,
        suggested_tone="standard",
        required_fix="",
        subject_key=subject_key,
        freshness_tag=freshness_tag,
        absence_type=absence_type,
        absence_scope=absence_scope,
    )


def _source(source_id: str, source_role: str, *, published_on: str) -> SourcePacket:
    return SourcePacket(
        source_id=source_id,
        title=f"Source {source_id}",
        source_role=source_role,
        published_on=published_on,
    )


def _evidence(sources: list[SourcePacket]) -> CollectedEvidence:
    return CollectedEvidence(sources=sources, findings=[])


if __name__ == "__main__":
    unittest.main()
