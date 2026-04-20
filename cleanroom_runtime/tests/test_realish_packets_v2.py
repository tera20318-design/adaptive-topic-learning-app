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

from cleanroom_runtime.ingestion_boundary import normalize_source_packets, packet_integrity_notes  # noqa: E402
from cleanroom_runtime.models import SourceFinding, SourcePacket, SourcePacketProvenance  # noqa: E402


class RealishPacketsV2Tests(unittest.TestCase):
    def test_variant_urls_merge_into_one_normalized_packet_with_parent_lineage(self) -> None:
        packets = [
            SourcePacket(
                source_id="SRC-001",
                title="Primary source",
                source_role="official_regulator",
                url="https://example.org/source?id=1",
                findings=[
                    SourceFinding(
                        finding_id="finding-001",
                        statement="Older authoritative note.",
                        claim_kind="regulatory",
                        risk_level="high",
                    )
                ],
                provenance=SourcePacketProvenance(
                    canonical_url="https://example.org/source",
                    dedupe_key="example-source",
                    stale=True,
                    stale_reason="Older authoritative notice still circulates.",
                    metadata_consistent=False,
                    citation_trace_complete=False,
                    metadata_missing_fields=["retrieved_at"],
                ),
            ),
            SourcePacket(
                source_id="SRC-002",
                title="Mirror source",
                source_role="official_regulator",
                url="https://example.org/source?id=2",
                findings=[
                    SourceFinding(
                        finding_id="finding-002",
                        statement="Fragmentary mirror copy.",
                        claim_kind="fact",
                        risk_level="medium",
                    )
                ],
                provenance=SourcePacketProvenance(
                    canonical_url="https://example.org/source",
                    dedupe_key="example-source",
                    partial=True,
                    partial_reason="HTML snippet omitted appendix.",
                    malformed=True,
                    malformed_reason="Truncated markup.",
                    grounding_status="ambiguous",
                    role_inference_status="ambiguous",
                ),
            ),
        ]

        normalized = normalize_source_packets(packets)

        self.assertEqual(len(normalized), 1)
        packet = normalized[0]
        self.assertEqual(packet.provenance.dedupe_key, "example-source")
        self.assertEqual(packet.provenance.canonical_url, "https://example.org/source")
        self.assertIn("SRC-002", packet.provenance.dedupe_parent_ids)
        self.assertFalse(packet.provenance.metadata_consistent)
        self.assertFalse(packet.provenance.citation_trace_complete)
        self.assertTrue(packet.provenance.partial)
        self.assertTrue(packet.provenance.malformed)
        self.assertEqual(packet.provenance.grounding_status, "ambiguous")
        self.assertEqual(packet.provenance.role_inference_status, "ambiguous")
        self.assertEqual({finding.finding_id for finding in packet.findings}, {"finding-001", "finding-002"})

    def test_packet_integrity_notes_surface_realish_failure_modes(self) -> None:
        packet = SourcePacket(
            source_id="SRC-REALISH-001",
            title="Fragmentary packet",
            source_role="unknown",
            findings=[],
            provenance=SourcePacketProvenance(
                metadata_consistent=False,
                citation_trace_complete=False,
                partial=True,
                partial_reason="Only a fragmentary excerpt was preserved.",
                stale=True,
                stale_reason="The checked packet predates the fresher context packet.",
                malformed=True,
                malformed_reason="HTML wrapper was dropped.",
                metadata_missing_fields=["publisher", "published_on"],
                role_inference_status="ambiguous",
                grounding_status="ambiguous",
            ),
        )

        notes = packet_integrity_notes(packet)
        joined = " ".join(notes)

        self.assertIn("metadata inconsistency", joined)
        self.assertIn("citation trace is incomplete", joined)
        self.assertIn("partial evidence packet", joined)
        self.assertIn("stale source caution", joined)
        self.assertIn("malformed source caution", joined)
        self.assertIn("missing metadata fields", joined)
        self.assertIn("source-role inference is ambiguous", joined)
        self.assertIn("document grounding is ambiguous", joined)

    def test_fixture_suite_already_contains_realish_pressure_tags(self) -> None:
        technical_packets = json.loads((ROOT / "fixtures" / "technical_overview" / "synthetic_sources.json").read_text(encoding="utf-8"))
        user_doc_packets = json.loads((ROOT / "fixtures" / "user_document_review" / "synthetic_sources.json").read_text(encoding="utf-8"))
        historical_packets = json.loads((ROOT / "fixtures" / "historical_cultural" / "synthetic_sources.json").read_text(encoding="utf-8"))

        self.assertTrue(
            any(
                {"citation_trace_mismatch", "metadata_inconsistency"} <= set(finding.get("tags", []))
                for packet in technical_packets
                for finding in packet.get("findings", [])
            )
        )
        self.assertTrue(
            any(
                "not itself legal authority" in flag.casefold()
                or "document_grounding_ambiguity"
                in {
                    tag
                    for finding in packet.get("findings", [])
                    for tag in finding.get("tags", [])
                }
                for packet in user_doc_packets
                for flag in packet.get("quality_flags", [])
            )
        )
        self.assertTrue(
            any(
                {"conflicting_sources", "stale_vs_recent_tension"} & set(finding.get("tags", []))
                for packet in historical_packets
                for finding in packet.get("findings", [])
            )
        )


if __name__ == "__main__":
    unittest.main()
