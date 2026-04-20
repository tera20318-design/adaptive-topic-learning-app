from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SRC = ROOT / "src"
for candidate in (TESTS, SRC):
    rendered = str(candidate)
    if rendered not in sys.path:
        sys.path.insert(0, rendered)

from multigenre_fixtures import load_fixture  # noqa: E402
from multigenre_runtime import run_multigenre_pipeline  # noqa: E402
from support import make_packet, make_request  # noqa: E402

from cleanroom_runtime.models import AbsenceScope, SourceFinding  # noqa: E402
from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402


class AbsenceScopeRewriteTests(unittest.TestCase):
    def test_checked_authoritative_absence_is_rewritten_with_explicit_scope(self) -> None:
        fixture = load_fixture("historical_cultural", variant="positive")
        bundle = run_multigenre_pipeline(fixture.request)

        scoped_claims = [
            claim
            for claim in bundle.claims
            if claim.included_in_report and claim.claim_kind == "absence" and claim.support_status == "scoped_absence"
        ]

        self.assertTrue(scoped_claims)
        for claim in scoped_claims:
            with self.subTest(claim=claim.claim_id):
                self.assertIn("Within the checked scope", claim.exact_text_span)
                self.assertIsNotNone(claim.absence_scope)
                self.assertIn(claim.absence_scope.subject, claim.exact_text_span)
                self.assertFalse(
                    any(
                        gap.claim_id == claim.claim_id and gap.gap_type == "authoritative_checked_absence"
                        for gap in bundle.gaps
                    )
                )

        self.assertEqual(bundle.release_gate.status, "complete")

    def test_unstateable_high_risk_absence_is_demoted_to_audit_only(self) -> None:
        packet_finding = SourceFinding(
            finding_id="finding-absence-001",
            statement="No checked authoritative source establishes the excluded condition.",
            claim_kind="absence",
            risk_level="high",
            section_hint="uncertainty",
            source_ids=["SRC-ABS-001"],
            source_roles=["official_regulator"],
            absence_type="not_found_in_official_source_checked",
            absence_scope=AbsenceScope(
                subject="",
                scope_label="",
                basis="not_found_in_official_source_checked",
                checked_source_ids=["SRC-ABS-001"],
                checked_roles=["official_regulator"],
                scope_note="Unsafe scope placeholder.",
            ),
            grounding_kind="direct_quote",
            source_excerpt="The checked source does not establish the excluded condition.",
            source_span_start=0,
            source_span_end=60,
            subject_key="bounded absence subject",
        )
        request = make_request(
            topic="Scoped absence rewrite guard",
            use_context="Ensure unsafe authoritative absence stays audit-only",
            mode="scoped",
            evidence_mode="live",
            packets=[
                make_packet(
                    "SRC-ABS-001",
                    "official_regulator",
                    title="Checked authoritative source",
                    findings=[packet_finding],
                )
            ],
        )

        bundle = run_pipeline(request)
        absence_claims = [claim for claim in bundle.claims if claim.claim_kind == "absence"]

        self.assertEqual(len(absence_claims), 1)
        claim = absence_claims[0]
        self.assertFalse(claim.included_in_report)
        self.assertIn(claim.support_status, {"missing", "weak"})
        self.assertTrue(
            any(gap.claim_id == claim.claim_id and "scope" in gap.gap_type for gap in bundle.gaps)
        )
        self.assertIn(bundle.release_gate.status, {"blocked", "needs_revision"})


if __name__ == "__main__":
    unittest.main()
