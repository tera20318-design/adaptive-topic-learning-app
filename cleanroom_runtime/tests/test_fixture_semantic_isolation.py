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
from cleanroom_runtime.stage_contracts import validate_stage_output  # noqa: E402
from cleanroom_runtime.utils import normalize_text  # noqa: E402

from support import make_request  # noqa: E402


FIXTURE_SEMANTIC_PATTERNS = {
    "fixture_specific_noun": (
        "supplement x",
        "semaglutide",
        "premium cash sweep",
        "document ai intake tools",
        "finance software vendors",
        "fertility travel reimbursement",
    ),
    "risk_phrase": (
        "safe for all adults using semaglutide",
        "guarantees an 8 percent annual yield with no downside risk",
        "legally guarantees reimbursement for every out-of-state fertility treatment trip",
        "universal margin-expansion claim across every listed vendor",
    ),
    "regulation_wording": (
        "universal fda safety clearance",
        "blanket regulator approval",
        "federal law that requires every employer to reimburse all fertility travel",
        "sec investor alert warns against marketing cash products as guaranteed high-yield investments",
    ),
    "overclaim_phrasing": (
        "definitely safe with glp-1 drugs for all adults",
        "universal share winner",
        "blanket product approval",
        "every out-of-state fertility treatment trip",
    ),
}


class FixtureSemanticIsolationTests(unittest.TestCase):
    def test_core_runtime_files_do_not_leak_fixture_specific_semantics(self) -> None:
        source_root = ROOT / "src" / "cleanroom_runtime"
        core_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(source_root.rglob("*"))
            if path.is_file() and path.suffix in {".py", ".md"}
        )
        normalized = normalize_text(core_text)

        for category, phrases in FIXTURE_SEMANTIC_PATTERNS.items():
            with self.subTest(category=category):
                for phrase in phrases:
                    self.assertNotIn(normalize_text(phrase), normalized)

    def test_fixture_specific_noun_leakage_is_rejected(self) -> None:
        failures = _tone_failures("The runtime summary reuses supplement X as if it were core behavior.")
        self.assertIn("SEMANTIC_FIXTURE_NOUN_LEAK", {failure.code for failure in failures})

    def test_fixture_specific_risk_phrase_leakage_is_rejected(self) -> None:
        failures = _tone_failures("This draft guarantees an 8 percent annual yield with no downside risk.")
        self.assertIn("SEMANTIC_RISK_PHRASE_LEAK", {failure.code for failure in failures})

    def test_fixture_specific_regulation_wording_leakage_is_rejected(self) -> None:
        failures = _tone_failures("The checked packet amounts to blanket regulator approval for every workflow.")
        self.assertIn("SEMANTIC_REGULATION_WORDING_LEAK", {failure.code for failure in failures})

    def test_fixture_specific_overclaim_phrasing_leakage_is_rejected(self) -> None:
        failures = _tone_failures("The checked packet proves a universal share winner.")
        self.assertIn("SEMANTIC_OVERCLAIM_PHRASING_LEAK", {failure.code for failure in failures})


def _tone_failures(text: str):
    request = make_request()
    evidence = CollectedEvidence(
        sources=[SourcePacket(source_id="SRC-001", title="Checked source", source_role="government_context")],
        findings=[],
        source_counts_by_role={"government_context": 1},
        quality_notes=[],
    )
    draft = ReportDraft(
        title="Semantic isolation draft",
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
        semantic_patterns=FIXTURE_SEMANTIC_PATTERNS,
    )


if __name__ == "__main__":
    unittest.main()
