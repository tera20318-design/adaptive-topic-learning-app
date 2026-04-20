from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SRC = ROOT / "src"
for candidate in (TESTS, SRC):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from runtime_bootstrap import ensure_runtime_namespace


ensure_runtime_namespace()

from cleanroom_runtime.ingestion.document_grounding import document_packets_from_raw_documents  # noqa: E402
from cleanroom_runtime.models import (  # noqa: E402
    ClaimLedgerRow,
    CollectedEvidence,
    RawDocumentInput,
    RunRequest,
    SourcePacket,
    SourceStrategy,
    TargetProfile,
)
from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.stages.evidence_mapper import map_claims_to_evidence  # noqa: E402


class UserDocumentGroundingV3Tests(unittest.TestCase):
    def test_multiline_document_block_becomes_direct_multispan_finding(self) -> None:
        document = RawDocumentInput(
            document_id="DOC-RAW-V3-001",
            title="Uploaded review draft",
            content=(
                "# Draft\n"
                "Coverage stays limited to approved travel\n"
                "when approval exists.\n\n"
                "Outside approval remains required."
            ),
            content_type="text/markdown",
            provided_at="2026-04-21",
            excerpt_label="upload:v3",
        )

        packet = document_packets_from_raw_documents([document])[0]
        first_finding = packet.findings[0]

        self.assertEqual(first_finding.grounding_marker, "direct_document_multispan")
        self.assertEqual(first_finding.source_span_labels, ["line 2", "line 3"])
        self.assertEqual(len(first_finding.source_span_starts), 2)
        self.assertEqual(len(first_finding.source_span_ends), 2)
        self.assertIn("direct_document_grounding", first_finding.tags)
        self.assertIn("scope_limited_document", first_finding.tags)
        self.assertIn("multi_span_grounding", first_finding.tags)
        for start, end in zip(first_finding.source_span_starts, first_finding.source_span_ends, strict=False):
            self.assertEqual(document.content[start:end], document.content[start:end].strip())
        self.assertIn("checked document excerpt span(s)", first_finding.grounding_scope_note)
        self.assertIn("separate evidence units", " ".join(packet.provenance.grounding_notes))

    def test_mapper_rejects_unsupported_synthesis_across_separate_document_spans(self) -> None:
        packet = SourcePacket(
            source_id="DOC-SYNTH-V3-001",
            title="Uploaded memo",
            source_role="user_provided_source",
        )
        evidence = CollectedEvidence(
            sources=[packet],
            findings=document_packets_from_raw_documents(
                [
                    RawDocumentInput(
                        document_id="DOC-SYNTH-V3-001",
                        title="Uploaded memo",
                        content="Line one states coverage stays limited.\n\nLine two states approval still applies.",
                        provided_at="2026-04-21",
                    )
                ]
            )[0].findings,
        )
        claim = ClaimLedgerRow(
            claim_id="claim-001",
            unit_id="unit-001",
            report_section="Direct answer",
            report_section_key="direct_answer",
            exact_text_span="The memo allows travel and waives approval.",
            normalized_claim="the memo allows travel and waives approval.",
            claim_kind="fact",
            risk_level="medium",
            source_ids=["DOC-SYNTH-V3-001"],
            source_roles=["user_provided_source"],
            evidence_count=1,
            required_source_roles=["user_provided_source"],
            matched_source_roles=["user_provided_source"],
            support_status="supported",
            confidence=0.7,
            origin_finding_ids=[finding.finding_id for finding in evidence.findings],
            included_in_report=True,
        )
        strategy = SourceStrategy(
            source_priority=["user_provided_source"],
            required_source_roles_by_claim_kind={"fact": ["user_provided_source"]},
        )

        mapped_claims, citations = map_claims_to_evidence([claim], evidence, strategy)

        self.assertEqual(mapped_claims[0].support_status, "weak")
        self.assertTrue(
            any("separate checked document findings" in reason for reason in mapped_claims[0].blocking_reasons)
        )
        self.assertEqual(citations[0].trace_status, "mismatch")
        self.assertTrue(citations[0].source_span_starts)

    def test_document_review_mode_keeps_checked_paragraphs_separate(self) -> None:
        document = RawDocumentInput(
            document_id="DOC-RAW-V3-REVIEW",
            title="Uploaded review packet",
            content=(
                "Paragraph one states the checked exception remains scoped.\n"
                "Paragraph one keeps the approval condition visible.\n\n"
                "Paragraph two says a separate review remains required."
            ),
            provided_at="2026-04-21",
            review_mode="document_review",
        )

        packet = document_packets_from_raw_documents([document])[0]

        self.assertEqual(len(packet.findings), 2)
        self.assertIn("Document-review mode keeps checked blocks separate", " ".join(packet.quality_flags))
        self.assertIn("document_review_mode", packet.findings[0].tags)
        self.assertIn("document-review mode", " ".join(packet.provenance.grounding_notes).casefold())

    def test_pipeline_keeps_document_review_claims_span_grounded(self) -> None:
        request = RunRequest(
            topic="Document review span grounding",
            reader="reviewer",
            use_context="Review the uploaded document and stay within the checked text",
            desired_depth="decision",
            jurisdiction="US",
            mode="scoped",
            evidence_mode="synthetic",
            question="What does the uploaded document state directly?",
            raw_documents=[
                RawDocumentInput(
                    document_id="DOC-PIPE-V3-001",
                    title="Uploaded procedure note",
                    content=(
                        "Approved travel stays limited to listed trips\n"
                        "and still requires manager confirmation.\n\n"
                        "Exceptions remain subject to separate review."
                    ),
                    content_type="text/plain",
                    provided_at="2026-04-21",
                    excerpt_label="upload:pipe-v3",
                )
            ],
            target_profile=TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=0),
        )

        bundle = run_pipeline(request)
        included_claims = [claim for claim in bundle.claims if claim.included_in_report]
        document_citations = [citation for citation in bundle.citations if citation.source_role == "user_provided_source"]

        self.assertTrue(included_claims)
        self.assertTrue(document_citations)
        self.assertTrue(bundle.metrics.document_grounded_claim_count > 0)
        for claim in included_claims:
            with self.subTest(claim=claim.claim_id):
                self.assertEqual(claim.trace_status, "linked")
                self.assertEqual(claim.claim_span_start, 0)
                self.assertEqual(claim.claim_span_end, len(claim.exact_text_span))
                self.assertTrue(claim.origin_finding_ids)
                self.assertTrue(claim.finding_span_starts)
                self.assertTrue(claim.finding_span_ends)
                self.assertTrue(claim.grounding_marker.startswith("direct_document_"))
        for citation in document_citations:
            with self.subTest(citation=citation.citation_id):
                self.assertEqual(citation.trace_status, "linked")
                self.assertIsNotNone(citation.claim_span_start)
                self.assertIsNotNone(citation.claim_span_end)
                self.assertTrue(citation.source_finding_ids)
                self.assertTrue(citation.source_excerpt)
                self.assertTrue(citation.source_span_starts)
                self.assertTrue(citation.source_span_ends)
                self.assertTrue(citation.grounding_marker.startswith("direct_document_"))


if __name__ == "__main__":
    unittest.main()
