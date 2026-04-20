from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = ROOT / "tests"
for candidate in (ROOT, SRC, TESTS):
    rendered = str(candidate)
    if rendered not in sys.path:
        sys.path.insert(0, rendered)

from runtime_bootstrap import ensure_runtime_namespace  # noqa: E402


ensure_runtime_namespace()

from cleanroom_runtime.ingestion import execute_live_lite_request, prepare_live_lite_request  # noqa: E402
from support import make_request  # noqa: E402


class LiveLiteExecutionTests(unittest.TestCase):
    def test_prepare_request_validates_before_runtime_entry(self) -> None:
        request = make_request(evidence_mode="live")
        prepared_request, load_result = prepare_live_lite_request(request, _packet_payloads(), as_of_date="2026-04-21")

        self.assertEqual(len(prepared_request.source_packets), 2)
        self.assertEqual(len(load_result.rejected_packets), 1)
        self.assertTrue(any(issue.code == "SCHEMA_VALIDATION_FAILED" for issue in load_result.issues))
        self.assertTrue(any(issue.code == "DEDUPE_COLLISION_NOTE" for issue in load_result.issues))

    def test_execute_live_lite_request_renders_packet_audit_artifacts(self) -> None:
        request = make_request(
            topic="Live-lite packet execution",
            use_context="decide whether the checked packet set is ready for action",
            evidence_mode="live",
        )
        with tempfile.TemporaryDirectory() as tempdir:
            output_dir = Path(tempdir)
            bundle = execute_live_lite_request(
                request,
                _packet_payloads(),
                as_of_date="2026-04-21",
                output_dir=output_dir,
            )

            audit_path = output_dir / "packet-ingestion-audit.json"
            tsv_path = output_dir / "packet-ingestion-audit.tsv"
            self.assertTrue(audit_path.exists())
            self.assertTrue(tsv_path.exists())
            audit = json.loads(audit_path.read_text(encoding="utf-8"))

        self.assertEqual(audit["accepted_count"], 2)
        self.assertEqual(audit["rejected_count"], 1)
        self.assertEqual(audit["salvaged_count"], 1)
        self.assertGreaterEqual(audit["stale_count"], 1)
        self.assertGreaterEqual(audit["dedupe_collision_count"], 2)
        self.assertTrue(any(item["disposition"] == "rejected" for item in audit["packet_summaries"]))
        self.assertTrue(any(item["disposition"] == "salvaged" for item in audit["packet_summaries"]))
        self.assertTrue(any("Live-lite ingestion:" in reason for reason in bundle.release_gate.reasons))
        self.assertTrue(any("stale-source warnings" in note for note in bundle.evidence.quality_notes))


def _packet_payloads() -> list[dict[str, object]]:
    return [
        {
            "source_id": "SRC-001",
            "title": "Packet A",
            "source_role": "official_regulator",
            "citation": "Packet A",
            "publisher": "Generic publisher",
            "published_on": "2024-01-01",
            "url": "https://example.test/shared",
            "summary": "The checked source supports a bounded answer.",
            "dedupe": {
                "dedupe_key": "shared-key",
                "canonical_url": "https://example.test/shared",
            },
            "staleness": {
                "stale_status": "stale",
                "stale_reason": "A newer retrieval date is required for a live-lite decision.",
            },
            "provenance": {
                "packet_origin": "live_lite_packet",
                "adapter_name": "live_lite_loader",
                "retrieval_scope": "packet_only",
                "canonical_url": "https://example.test/shared",
                "canonical_id": "SRC-001",
                "source_locator": "https://example.test/shared",
                "retrieved_at": "2024-01-01",
                "observed_at": "2024-01-01",
                "metadata_consistent": True,
                "citation_trace_complete": True,
                "role_inference_status": "declared",
                "grounding_status": "grounded",
            },
            "findings": [
                {
                    "finding_id": "SRC-001-finding-001",
                    "statement": "The checked packet supports a bounded fact.",
                    "claim_kind": "fact",
                    "risk_level": "medium",
                    "section_hint": "direct_answer",
                    "source_ids": ["SRC-001"],
                    "source_roles": ["official_regulator"],
                    "grounding_kind": "direct_quote",
                    "source_excerpt": "The checked packet supports a bounded fact.",
                    "source_span_label": "paragraph 1",
                    "source_span_start": 0,
                    "source_span_end": 40,
                }
            ],
        },
        {
            "source_id": "SRC-002",
            "title": "Packet B",
            "source_role": "official_regulator",
            "citation": "Packet B",
            "publisher": "Generic publisher",
            "published_on": "2026-03-01",
            "url": "https://example.test/shared?copy=1",
            "summary": "A related packet preserves one usable grounded finding.",
            "dedupe": {
                "dedupe_key": "shared-key",
                "canonical_url": "https://example.test/shared",
            },
            "provenance": {
                "packet_origin": "live_lite_packet",
                "adapter_name": "live_lite_loader",
                "retrieval_scope": "packet_only",
                "canonical_url": "https://example.test/shared",
                "canonical_id": "SRC-002",
                "source_locator": "https://example.test/shared?copy=1",
                "retrieved_at": "2026-03-05",
                "observed_at": "2026-03-01",
                "metadata_consistent": True,
                "citation_trace_complete": True,
                "role_inference_status": "declared",
                "grounding_status": "grounded",
            },
            "findings": [
                {
                    "finding_id": "SRC-002-finding-001",
                    "statement": "The second packet supports a bounded qualification.",
                    "claim_kind": "fact",
                    "risk_level": "medium",
                    "section_hint": "findings",
                    "source_ids": ["SRC-002"],
                    "source_roles": ["official_regulator"],
                    "grounding_kind": "direct_quote",
                    "source_excerpt": "The second packet supports a bounded qualification.",
                    "source_span_label": "paragraph 2",
                    "source_span_start": 0,
                    "source_span_end": 50,
                },
                {
                    "finding_id": "SRC-002-finding-bad"
                }
            ],
        },
        {
            "source_id": "SRC-003",
            "source_role": "official_regulator",
            "citation": "Rejected packet",
            "publisher": "Generic publisher",
            "published_on": "2026-03-01",
            "url": "https://example.test/rejected",
            "provenance": {
                "packet_origin": "live_lite_packet",
                "adapter_name": "live_lite_loader",
                "retrieval_scope": "packet_only"
            },
            "findings": []
        },
    ]


if __name__ == "__main__":
    unittest.main()
