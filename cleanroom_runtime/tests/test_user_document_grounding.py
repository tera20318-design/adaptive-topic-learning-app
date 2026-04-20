from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime_bootstrap import ensure_repo_paths


ensure_repo_paths(include_tests=True)

from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from support import make_finding, make_packet, make_raw_document, make_request  # noqa: E402


class UserDocumentGroundingTests(unittest.TestCase):
    def test_raw_document_input_becomes_grounded_source_packet(self) -> None:
        request = make_request(
            topic="Document grounded review runtime",
            use_context="review the uploaded document before a reader acts on it",
            raw_documents=[
                make_raw_document(
                    "DOC-001",
                    title="Uploaded memo",
                    content=(
                        "Clause 1: The checked document states a bounded condition for the current workflow.\n"
                        "Clause 2: The checked document states that unresolved exceptions still need counsel review."
                    ),
                )
            ],
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle = run_pipeline(request, Path(tmp_dir))
            report_text = Path(tmp_dir, "final_report.md").read_text(encoding="utf-8")

        self.assertEqual(bundle.evidence.sources[0].source_role, "user_provided_source")
        self.assertEqual(bundle.evidence.sources[0].provenance.packet_origin, "raw_document")
        self.assertTrue(any(finding.grounding_kind == "direct_quote" for finding in bundle.evidence.findings))
        self.assertGreater(bundle.metrics.document_grounded_claim_count, 0)
        self.assertTrue(any(citation.source_finding_ids for citation in bundle.citations))
        self.assertIn("The checked document states:", report_text)
        self.assertIn(bundle.release_gate.status, {"needs_revision", "provisional"})

    def test_user_document_only_high_risk_claim_is_blocked_for_scope_overreach(self) -> None:
        request = make_request(
            topic="Document overreach review",
            use_context="review the uploaded draft before telling readers it settles the rule",
            packets=[
                make_packet(
                    "DOC-ONLY-001",
                    "user_provided_source",
                    findings=[
                        make_finding(
                            "finding-001",
                            "The uploaded draft conclusively settles the legal requirement for every reader.",
                            "legal",
                            "high",
                            "direct_answer",
                            source_ids=["DOC-ONLY-001"],
                            source_excerpt="The uploaded draft uses broad legal language without external grounding.",
                            grounding_kind="paraphrase",
                            subject_key="uploaded draft legal scope",
                        )
                    ],
                )
            ],
        )

        bundle = run_pipeline(request)

        self.assertEqual(bundle.release_gate.status, "blocked")
        self.assertTrue(any(gap.gap_type == "user_excerpt_extrapolation" for gap in bundle.gaps))


if __name__ == "__main__":
    unittest.main()
