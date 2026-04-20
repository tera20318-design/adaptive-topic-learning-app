from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SRC = ROOT / "src"
for candidate in (ROOT, TESTS, SRC):
    rendered = str(candidate)
    if rendered not in sys.path:
        sys.path.insert(0, rendered)

from runtime_bootstrap import ensure_runtime_namespace  # noqa: E402


ensure_runtime_namespace()

from cleanroom_runtime.ingestion import execute_live_lite_request  # noqa: E402
from support import make_request  # noqa: E402
from test_live_lite_execution import _packet_payloads  # noqa: E402


class LiveLiteExecutionV1Tests(unittest.TestCase):
    def test_live_lite_execution_keeps_salvage_visibility_in_audit_and_gate(self) -> None:
        request = make_request(
            topic="Live-lite execution v1",
            use_context="Review accepted packets and keep rejected or salvaged packet visibility explicit",
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

            audit_json = json.loads((output_dir / "packet-ingestion-audit.json").read_text(encoding="utf-8"))
            audit_tsv = (output_dir / "packet-ingestion-audit.tsv").read_text(encoding="utf-8")

        self.assertTrue(bundle.metrics.ingestion_audit_visible)
        self.assertEqual(audit_json["salvaged_count"], 1)
        self.assertEqual(audit_json["rejected_count"], 1)
        self.assertTrue(any(item["disposition"] == "salvaged" for item in audit_json["packet_summaries"]))
        self.assertIn("source_id", audit_tsv)
        self.assertTrue(any("Live-lite ingestion:" in reason for reason in bundle.release_gate.reasons))
        self.assertTrue(any("stale-source warnings" in note for note in bundle.evidence.quality_notes))
        self.assertFalse(
            any("Packet salvage occurred without a visible ingestion audit summary." in reason for reason in bundle.release_gate.reasons)
        )


if __name__ == "__main__":
    unittest.main()
