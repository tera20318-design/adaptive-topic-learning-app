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


class RealishPacketsV3Tests(unittest.TestCase):
    def test_fixtures_cover_v3_realish_packet_pressure(self) -> None:
        technical_request = json.loads((ROOT / "fixtures" / "technical_overview" / "request.json").read_text(encoding="utf-8"))
        technical_packets = json.loads((ROOT / "fixtures" / "technical_overview" / "synthetic_sources.json").read_text(encoding="utf-8"))
        legal_request = json.loads((ROOT / "fixtures" / "legal_regulatory" / "request.json").read_text(encoding="utf-8"))
        legal_packets = json.loads((ROOT / "fixtures" / "legal_regulatory" / "synthetic_sources.json").read_text(encoding="utf-8"))
        historical_request = json.loads((ROOT / "fixtures" / "historical_cultural" / "request.json").read_text(encoding="utf-8"))
        historical_packets = json.loads((ROOT / "fixtures" / "historical_cultural" / "synthetic_sources.json").read_text(encoding="utf-8"))
        document_request = json.loads((ROOT / "fixtures" / "user_document_review" / "request.json").read_text(encoding="utf-8"))
        document_packets = json.loads((ROOT / "fixtures" / "user_document_review" / "synthetic_sources.json").read_text(encoding="utf-8"))

        self.assertIn("incomplete_provenance", technical_request["scenario_tags"])
        self.assertIn("canonical_url_variants", technical_request["scenario_tags"])
        self.assertIn("mixed_jurisdiction_confusion", legal_request["scenario_tags"])
        self.assertIn("historical_as_current_temptation", historical_request["scenario_tags"])
        self.assertIn("cross_document_summary_temptation", document_request["scenario_tags"])

        self.assertTrue(
            any(
                packet.get("provenance", {}).get("metadata_missing_fields")
                and packet.get("provenance", {}).get("citation_trace_complete") is False
                for packet in technical_packets
            )
        )
        self.assertTrue(
            any(
                packet.get("provenance", {}).get("canonical_url")
                and packet.get("provenance", {}).get("original_url")
                and packet.get("provenance", {}).get("canonical_url") != packet.get("provenance", {}).get("original_url")
                for packet in technical_packets
            )
        )
        self.assertTrue(
            any(
                finding.get("source_excerpt")
                and not finding.get("source_span_label")
                for packet in technical_packets
                for finding in packet.get("findings", [])
            )
        )
        self.assertTrue(
            any(
                packet["source_role"] in {"official_regulator", "legal_text"}
                and packet.get("provenance", {}).get("stale")
                for packet in historical_packets
            )
        )
        self.assertTrue(
            any(
                packet["source_role"] in {"secondary_media", "professional_body"}
                and packet.get("published_on", "").startswith("2026")
                for packet in historical_packets
            )
        )
        self.assertTrue(
            any(
                packet["jurisdiction"] != legal_request["request"]["jurisdiction"]
                for packet in legal_packets
            )
        )
        self.assertTrue(
            any(
                "cross-document summary" in flag.casefold()
                for packet in document_packets
                for flag in packet.get("quality_flags", [])
            )
        )

    def test_v3_fixture_packets_include_salvage_and_scope_collision_signals(self) -> None:
        legal_packets = json.loads((ROOT / "fixtures" / "legal_regulatory" / "synthetic_sources.json").read_text(encoding="utf-8"))
        document_packets = json.loads((ROOT / "fixtures" / "user_document_review" / "synthetic_sources.json").read_text(encoding="utf-8"))

        authoritative_packets = [
            packet
            for packet in legal_packets
            if packet["source_role"] in {"official_regulator", "legal_text"}
        ]
        scope_notes = [
            finding.get("absence_scope", {}).get("scope_note", "")
            for packet in authoritative_packets
            for finding in packet.get("findings", [])
            if isinstance(finding.get("absence_scope"), dict)
        ]

        self.assertGreaterEqual(len(authoritative_packets), 2)
        self.assertTrue(any("scope" in note.casefold() for note in scope_notes))
        self.assertTrue(
            any(
                "salvage" in flag.casefold() or "can still be salvaged" in flag.casefold()
                for packet in authoritative_packets
                for flag in packet.get("quality_flags", [])
            )
        )
        self.assertTrue(
            any(
                "paragraph" in finding.get("source_excerpt", "").casefold()
                or "summary paragraph" in finding.get("source_excerpt", "").casefold()
                for packet in document_packets
                for finding in packet.get("findings", [])
            )
        )


if __name__ == "__main__":
    unittest.main()
