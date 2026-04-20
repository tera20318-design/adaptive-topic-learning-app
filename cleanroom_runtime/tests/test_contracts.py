from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.validators import validate_bundle_contracts, validate_domain_adapter, validate_metrics  # noqa: E402

from support import make_finding, make_packet, make_request  # noqa: E402


class ContractTests(unittest.TestCase):
    def test_pipeline_produces_contract_complete_bundle(self) -> None:
        request = make_request(
            packets=[
                make_packet(
                    "SRC-001",
                    "government_context",
                    findings=[
                        make_finding(
                            "finding-001",
                            "The runtime separates claim capture from support evaluation.",
                            "fact",
                            "medium",
                            "direct_answer",
                            source_ids=["SRC-001"],
                        )
                    ],
                )
            ]
        )

        bundle = run_pipeline(request)

        self.assertEqual(validate_domain_adapter(bundle.adapter), [])
        self.assertEqual(validate_bundle_contracts(bundle.draft, bundle.claims, bundle.citations, bundle.evidence), [])
        self.assertEqual(validate_metrics(bundle.metrics), [])
        self.assertTrue(bundle.metrics.audit_complete)
        self.assertEqual(bundle.release_gate.status, "needs_revision")

    def test_core_package_does_not_reference_legacy_packages_or_fixtures(self) -> None:
        forbidden = ("pseudo_pro_v2", "research_os_v2", "fixtures\\", "fixtures/")
        offenders: list[str] = []
        for path in (ROOT / "src" / "cleanroom_runtime").rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if any(token in text for token in forbidden):
                offenders.append(str(path))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
