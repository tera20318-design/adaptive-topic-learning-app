from __future__ import annotations

import json
import unittest
from pathlib import Path


FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"
EXPECTED_FIXTURE_STEMS = {
    "technical_overview",
    "legal_regulatory_overview",
    "medical_health_explanation",
    "financial_product_comparison",
    "market_business_analysis",
    "historical_cultural_topic",
    "user_provided_document_review",
}
HIGH_STAKES_STEMS = {
    "legal_regulatory_overview",
    "medical_health_explanation",
    "financial_product_comparison",
    "user_provided_document_review",
}
ALLOWED_GATE_VALUES = {"allow", "review", "block"}
REQUIRED_ROOT_KEYS = {
    "topic",
    "reader",
    "use_context",
    "output_type",
    "requested_mode",
    "expected_domain_adapter_traits",
    "known_failure_modes",
    "required_source_roles",
    "required_claims",
    "prohibited_overclaims",
    "expected_gate_behavior",
    "source_packets",
}
REQUIRED_PACKET_KEYS = {
    "source_id",
    "title",
    "source_role",
    "published_on",
    "jurisdiction",
    "quality_flags",
    "summary",
    "findings",
}
REQUIRED_FINDING_KEYS = {
    "finding_id",
    "statement",
    "claim_kind",
    "risk_level",
    "section_hint",
    "decision_note",
    "risk_tags",
    "failure_modes",
    "misunderstandings",
    "boundary_concepts",
    "confidence",
    "support_status_hint",
}


def load_fixtures() -> dict[str, dict]:
    fixtures: dict[str, dict] = {}
    for path in sorted(FIXTURES_DIR.glob("*.json")):
        fixtures[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return fixtures


class RegressionFixtureStructureTests(unittest.TestCase):
    def test_expected_fixture_types_are_present(self) -> None:
        fixtures = load_fixtures()
        self.assertTrue(EXPECTED_FIXTURE_STEMS.issubset(fixtures.keys()))
        self.assertGreaterEqual(len(fixtures), 7)

    def test_fixtures_have_required_root_shape(self) -> None:
        for name, fixture in load_fixtures().items():
            self.assertTrue(REQUIRED_ROOT_KEYS.issubset(fixture.keys()), name)
            self.assertTrue(isinstance(fixture["expected_domain_adapter_traits"], list) and fixture["expected_domain_adapter_traits"], name)
            self.assertTrue(isinstance(fixture["known_failure_modes"], list) and fixture["known_failure_modes"], name)
            self.assertTrue(isinstance(fixture["required_source_roles"], list) and fixture["required_source_roles"], name)
            self.assertTrue(isinstance(fixture["required_claims"], list) and fixture["required_claims"], name)
            self.assertTrue(isinstance(fixture["prohibited_overclaims"], list) and fixture["prohibited_overclaims"], name)
            self.assertIn(fixture["expected_gate_behavior"], ALLOWED_GATE_VALUES, name)
            self.assertTrue(isinstance(fixture["source_packets"], list) and fixture["source_packets"], name)

    def test_high_stakes_fixtures_require_authoritative_role(self) -> None:
        for name, fixture in load_fixtures().items():
            if name not in HIGH_STAKES_STEMS:
                continue
            self.assertIn("authoritative", fixture["required_source_roles"], name)

    def test_source_packets_and_findings_are_structured(self) -> None:
        for name, fixture in load_fixtures().items():
            for packet in fixture["source_packets"]:
                self.assertTrue(REQUIRED_PACKET_KEYS.issubset(packet.keys()), name)
                self.assertIsInstance(packet["quality_flags"], list, name)
                self.assertTrue(isinstance(packet["findings"], list) and packet["findings"], name)
                for finding in packet["findings"]:
                    self.assertTrue(REQUIRED_FINDING_KEYS.issubset(finding.keys()), name)
                    self.assertGreaterEqual(finding["confidence"], 0, name)
                    self.assertLessEqual(finding["confidence"], 1, name)


if __name__ == "__main__":
    unittest.main()
