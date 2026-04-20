from __future__ import annotations

import json
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
from cleanroom_runtime.ingestion_boundary import normalize_source_packets, packet_integrity_notes  # noqa: E402
from cleanroom_runtime.models import RawDocumentInput  # noqa: E402


class UserDocumentGroundingV2Tests(unittest.TestCase):
    def test_raw_text_and_markdown_excerpts_become_direct_grounded_packets(self) -> None:
        document = RawDocumentInput(
            document_id="DOC-RAW-001",
            title="Uploaded note",
            content="# Draft\n- Coverage stays limited to approved travel.\n- Outside approval is still required.",
            content_type="text/markdown",
            provided_at="2026-04-20",
            excerpt_label="upload:note",
        )

        packets = normalize_source_packets(document_packets_from_raw_documents([document]))

        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(packet.provenance.packet_origin, "raw_document")
        self.assertEqual(packet.provenance.adapter_name, "document_grounding")
        self.assertEqual(packet.provenance.source_locator, "upload:note")
        self.assertEqual(packet.provenance.grounding_status, "grounded")
        self.assertTrue(packet.provenance.citation_trace_complete)
        self.assertEqual(len(packet.provenance.content_digest), 64)
        self.assertIn("jurisdiction", packet.provenance.metadata_missing_fields)
        self.assertIn("url", packet.provenance.metadata_missing_fields)
        self.assertEqual(packet.summary, "- Coverage stays limited to approved travel.")
        self.assertEqual(len(packet.findings), 2)

        for finding in packet.findings:
            with self.subTest(finding=finding.finding_id):
                self.assertEqual(finding.grounding_kind, "direct_quote")
                self.assertIn("document_grounded", finding.tags)
                self.assertTrue(finding.source_excerpt)
                self.assertIsNotNone(finding.source_span_start)
                self.assertIsNotNone(finding.source_span_end)
                self.assertLess(finding.source_span_start, finding.source_span_end)
                self.assertEqual(
                    document.content[finding.source_span_start : finding.source_span_end],
                    finding.source_excerpt,
                )

    def test_empty_or_fragmentary_document_is_marked_partial_and_malformed(self) -> None:
        document = RawDocumentInput(
            document_id="DOC-RAW-EMPTY",
            title="Uploaded empty note",
            content=" \nshort\n",
            provided_at="2026-04-20",
        )

        packet = document_packets_from_raw_documents([document])[0]
        notes = packet_integrity_notes(packet)

        self.assertEqual(packet.findings, [])
        self.assertTrue(packet.provenance.partial)
        self.assertTrue(packet.provenance.malformed)
        self.assertEqual(packet.provenance.grounding_status, "partial")
        self.assertFalse(packet.provenance.citation_trace_complete)
        self.assertTrue(any("partial evidence packet" in note for note in notes))
        self.assertTrue(any("malformed source caution" in note for note in notes))

    def test_fixture_keeps_grounding_and_extrapolation_pressure_visible(self) -> None:
        fixture_packets = json.loads((ROOT / "fixtures" / "user_document_review" / "synthetic_sources.json").read_text(encoding="utf-8"))
        user_packets = [packet for packet in fixture_packets if packet["source_role"] == "user_provided_source"]
        legal_packets = [packet for packet in fixture_packets if packet["source_role"] == "legal_text"]

        self.assertEqual(len(user_packets), 1)
        self.assertEqual(len(legal_packets), 1)
        self.assertTrue(any("draft" in flag.casefold() for flag in user_packets[0].get("quality_flags", [])))
        self.assertTrue(any("not itself legal authority" in flag.casefold() for flag in user_packets[0].get("quality_flags", [])))
        self.assertTrue(
            any(
                {"high_risk_claim", "overgeneralization_trap", "weak_evidence"} <= set(finding.get("tags", []))
                for finding in user_packets[0].get("findings", [])
            )
        )
        self.assertTrue(
            any(
                finding.get("absence_type") == "not_found_in_checked_scope"
                for packet in legal_packets
                for finding in packet.get("findings", [])
            )
        )

    def test_document_grounding_plan_records_guardrails_and_remaining_gap(self) -> None:
        text = (ROOT / "document_grounding_plan.md").read_text(encoding="utf-8")

        self.assertIn("raw text or markdown-like excerpt content", text)
        self.assertIn("Direct grounding does not imply authoritative support.", text)
        self.assertIn("Out-of-scope extrapolation is disallowed", text)
        self.assertIn("Synthetic document grounding can prove the contract path", text)
        self.assertIn("remaining runtime work", text.casefold())


if __name__ == "__main__":
    unittest.main()
