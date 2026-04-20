from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.ingestion import (  # noqa: E402
    load_normalized_packet_schema,
    load_normalized_source_packets,
    validate_normalized_source_packet_collection,
)


class LiveLiteIngestionTests(unittest.TestCase):
    def test_loader_accepts_valid_packet_and_marks_stale_sources(self) -> None:
        result = load_normalized_source_packets([_valid_packet(published_on="2024-01-01")], as_of_date="2026-04-20")

        self.assertEqual(len(result.packets), 1)
        packet = result.packets[0]
        self.assertTrue(packet.provenance.stale)
        self.assertIn("stale source", packet.quality_flags)
        self.assertTrue(any(issue.code == "STALE_SOURCE_FLAGGED" for issue in result.issues))

    def test_schema_validation_blocks_packet_before_runtime_entry(self) -> None:
        packet = _valid_packet()
        del packet["provenance"]["retrieval_scope"]

        result = load_normalized_source_packets([packet], as_of_date="2026-04-20")

        self.assertEqual(len(result.packets), 0)
        self.assertEqual(len(result.rejected_packets), 1)
        self.assertTrue(any(issue.code == "SCHEMA_VALIDATION_FAILED" for issue in result.issues))

    def test_collection_can_partially_succeed_when_some_packets_are_malformed(self) -> None:
        good = _valid_packet()
        bad = _valid_packet(source_id="SRC-002", title="")

        result = load_normalized_source_packets([good, bad], as_of_date="2026-04-20")

        self.assertEqual(len(result.packets), 1)
        self.assertEqual(len(result.rejected_packets), 1)
        self.assertTrue(result.blocking_issues)

    def test_loader_keeps_packet_when_only_one_finding_is_malformed(self) -> None:
        packet = _valid_packet()
        packet["findings"].append({"finding_id": "broken"})

        result = load_normalized_source_packets([packet], as_of_date="2026-04-20")

        self.assertEqual(len(result.packets), 1)
        self.assertEqual(len(result.packets[0].findings), 1)
        self.assertTrue(result.packets[0].provenance.partial)
        self.assertTrue(any(issue.code == "MALFORMED_FINDING" for issue in result.issues))

    def test_loader_binds_source_role_without_inferring_authority_from_metadata(self) -> None:
        raw_document_packet = _valid_packet(source_role=None)
        raw_document_packet["provenance"]["packet_origin"] = "raw_document"
        raw_document_packet["provenance"]["role_inference_status"] = "inferred"

        inferred_authority_packet = _valid_packet(source_id="SRC-002", title="Ambiguous role", source_role="official_regulator")
        inferred_authority_packet["provenance"]["role_inference_status"] = "inferred"

        result = load_normalized_source_packets([raw_document_packet, inferred_authority_packet], as_of_date="2026-04-20")

        self.assertEqual(result.packets[0].source_role, "user_provided_source")
        self.assertEqual(result.packets[1].source_role, "unknown")
        self.assertTrue(any(issue.code == "ROLE_INFERENCE_BOUNDARY" for issue in result.issues))

    def test_loader_supports_json_file_payload(self) -> None:
        payload = [_valid_packet(), _valid_packet(source_id="SRC-002", url="https://example.test/source?variant=2")]

        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "packets.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = load_normalized_source_packets(path, as_of_date="2026-04-20")

        self.assertEqual(len(result.packets), 2)

    def test_loader_accepts_v2_nested_provenance_contract_fields(self) -> None:
        packet = _valid_packet()
        packet["role_assignment"] = {
            "declared_source_role": "official_regulator",
            "effective_source_role": "official_regulator",
            "assignment_method": "declared",
            "assignment_basis": "carried from normalized packet input",
            "assignment_confidence": 1.0,
            "review_required": False,
        }
        packet["dedupe"] = {
            "dedupe_key": "checked-source",
            "dedupe_basis": "canonical_url",
            "dedupe_confidence": 0.92,
            "content_fingerprint": "digest-001",
            "dedupe_cluster_id": "cluster-001",
            "merged_from_packet_ids": ["SRC-001-variant"],
        }
        packet["ingestion_health"] = {
            "fetch_status": "ok",
            "parse_status": "ok",
            "metadata_consistent": True,
            "citation_trace_complete": True,
            "grounding_status": "grounded",
        }
        packet["staleness"] = {
            "stale_status": "current",
            "stale_as_of": "2026-04-20",
        }
        packet["findings"][0]["traceability"] = {
            "support_excerpt": "The checked source supports a bounded statement.",
            "locator_type": "label",
            "locator_value": "paragraph 1",
            "excerpt_format": "text/plain",
            "excerpt_hash": "hash-001",
            "extraction_method": "direct_quote",
            "extraction_confidence": 1.0,
            "derived_from_packet_id": "SRC-001",
            "derived_from_content_digest": "digest-001",
        }

        result = load_normalized_source_packets([packet], as_of_date="2026-04-20")

        self.assertEqual(len(result.packets), 1)
        loaded = result.packets[0]
        self.assertEqual(loaded.provenance.dedupe_key, "checked-source")
        self.assertIn("SRC-001-variant", loaded.provenance.dedupe_parent_ids)
        self.assertEqual(loaded.findings[0].source_excerpt, "The checked source supports a bounded statement.")
        self.assertEqual(loaded.findings[0].source_span_label, "paragraph 1")
        self.assertEqual(loaded.findings[0].grounding_kind, "direct_quote")

    def test_collection_validator_uses_schema_v2_requirements(self) -> None:
        schema = load_normalized_packet_schema()
        errors = validate_normalized_source_packet_collection([{"source_id": "SRC-001"}], schema=schema)

        self.assertTrue(any("title is required" in error for error in errors))
        self.assertTrue(any("provenance is required" in error for error in errors))


def _valid_packet(
    *,
    source_id: str = "SRC-001",
    title: str = "Checked source",
    source_role: str | None = "official_regulator",
    published_on: str = "2026-03-01",
    url: str = "https://example.test/source",
) -> dict[str, object]:
    packet: dict[str, object] = {
        "source_id": source_id,
        "title": title,
        "citation": title,
        "publisher": "Generic publisher",
        "published_on": published_on,
        "url": url,
        "summary": "Bounded summary for ingestion tests.",
        "findings": [
            {
                "finding_id": f"{source_id}-finding-001",
                "statement": "The checked source supports a bounded statement.",
                "claim_kind": "fact",
                "risk_level": "medium",
                "source_ids": [source_id],
                "source_roles": [source_role] if source_role else [],
                "grounding_kind": "direct_quote",
                "source_excerpt": "The checked source supports a bounded statement.",
                "source_span_label": "paragraph 1",
                "source_span_start": 0,
                "source_span_end": 47
            }
        ],
        "provenance": {
            "packet_origin": "live_lite_packet",
            "adapter_name": "live_lite_loader",
            "retrieval_scope": "packet_only",
            "canonical_url": url,
            "canonical_id": source_id,
            "source_locator": url,
            "retrieved_at": "2026-03-05",
            "observed_at": published_on,
            "metadata_consistent": True,
            "citation_trace_complete": True,
            "role_inference_status": "declared" if source_role else "ambiguous",
            "grounding_status": "grounded"
        }
    }
    if source_role is not None:
        packet["source_role"] = source_role
    return packet


if __name__ == "__main__":
    unittest.main()
