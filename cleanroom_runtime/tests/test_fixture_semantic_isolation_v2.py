from __future__ import annotations

import unittest

from runtime_bootstrap import ROOT, ensure_repo_paths


ensure_repo_paths()

from cleanroom_runtime.models import (  # noqa: E402
    ClaimLedgerRow,
    CollectedEvidence,
    ReportDraft,
    ReportSectionPlan,
    ReportUnit,
    SourcePacket,
)
from cleanroom_runtime.semantic_isolation import detect_semantic_leakage, semantic_pattern_catalog  # noqa: E402
from cleanroom_runtime.stage_contracts import validate_stage_output  # noqa: E402
from cleanroom_runtime.types import StageFailureCode  # noqa: E402
from cleanroom_runtime.utils import normalize_text  # noqa: E402

from support import make_request  # noqa: E402


V2_PATTERNS = {
    "fixture_specific_noun": (
        "supplement x",
        "premium cash sweep",
        "document ai intake tools",
        "fertility travel reimbursement",
    ),
    "risk_phrase": (
        "guarantees an 8 percent annual yield with no downside risk",
        "safe for all adults using semaglutide",
    ),
    "regulation_wording": (
        "blanket regulator approval",
        "federal law that requires every employer to reimburse all fertility travel",
    ),
    "overclaim_phrasing": (
        "universal share winner",
        "definitely safe with glp 1 drugs for all adults",
    ),
}


class FixtureSemanticIsolationV2Tests(unittest.TestCase):
    def test_v2_pattern_catalog_merges_defaults_and_fixture_patterns(self) -> None:
        catalog = semantic_pattern_catalog(extra_patterns=V2_PATTERNS)

        self.assertIn("supplement x", catalog["fixture_specific_noun"])
        self.assertIn("pseudo pro v2", catalog["fixture_specific_noun"])
        self.assertIn("blanket regulator approval", catalog["regulation_wording"])

    def test_v2_detection_handles_case_and_punctuation_variants(self) -> None:
        cases = [
            ("The runtime summary treats Supplement-X as a core capability.", StageFailureCode.SEMANTIC_FIXTURE_NOUN_LEAK),
            ("This draft GUARANTEES an 8 percent annual yield with no downside risk.", StageFailureCode.SEMANTIC_RISK_PHRASE_LEAK),
            ("The checked packet amounts to blanket regulator approval.", StageFailureCode.SEMANTIC_REGULATION_WORDING_LEAK),
            ("The checked packet proves a universal share winner.", StageFailureCode.SEMANTIC_OVERCLAIM_PHRASING_LEAK),
        ]

        for text, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                failures = _tone_failures(text, request=make_request())
                self.assertIn(expected_code, {failure.code for failure in failures})

    def test_fixture_noun_anchor_in_request_context_is_not_flagged(self) -> None:
        request = make_request(
            topic="Supplement X review",
            use_context="summarize only the checked Supplement X packet",
        )
        findings = detect_semantic_leakage(
            "Within the checked packet, Supplement X remains a reader-provided subject.",
            anchor_values=[request],
            extra_patterns=V2_PATTERNS,
            categories=("fixture_specific_noun",),
        )

        self.assertEqual(findings, [])

    def test_core_runtime_files_do_not_leak_v2_fixture_semantics(self) -> None:
        source_root = ROOT / "src" / "cleanroom_runtime"
        core_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(source_root.rglob("*"))
            if path.is_file() and path.suffix in {".py", ".md"}
        )
        normalized = normalize_text(core_text)

        for phrases in V2_PATTERNS.values():
            for phrase in phrases:
                self.assertNotIn(normalize_text(phrase), normalized)


def _tone_failures(text: str, *, request):
    evidence = CollectedEvidence(
        sources=[SourcePacket(source_id="SRC-001", title="Checked source", source_role="government_context")],
        findings=[],
        source_counts_by_role={"government_context": 1},
        quality_notes=[],
    )
    draft = ReportDraft(
        title="Semantic isolation v2 draft",
        sections=[ReportSectionPlan(key="findings", title="What the evidence supports", purpose="")],
        units=[
            ReportUnit(
                unit_id="unit-001",
                section_key="findings",
                section_title="What the evidence supports",
                text=text,
                claim_kind="fact",
                risk_level="medium",
                source_ids=["SRC-001"],
                source_roles=["government_context"],
                confidence=0.8,
            )
        ],
    )
    claims = [
        ClaimLedgerRow(
            claim_id="claim-001",
            unit_id="unit-001",
            report_section="What the evidence supports",
            exact_text_span=text,
            normalized_claim=normalize_text(text),
            claim_kind="fact",
            risk_level="medium",
            source_ids=["SRC-001"],
            source_roles=["government_context"],
            evidence_count=1,
            required_source_roles=["government_context"],
            matched_source_roles=["government_context"],
            support_status="supported",
            confidence=0.8,
            caveat_required=False,
            suggested_tone="standard",
            required_fix="",
            included_in_report=True,
        )
    ]
    return validate_stage_output(
        "tone_control",
        draft,
        request=request,
        evidence=evidence,
        claims=claims,
        semantic_patterns=V2_PATTERNS,
    )


if __name__ == "__main__":
    unittest.main()
