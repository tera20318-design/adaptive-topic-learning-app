from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pseudo_pro_v2.stage_contracts import STAGE_CONTRACTS, STAGE_FAILURE_CODES, STAGE_SNAPSHOT_REQUIRED_FIELDS  # noqa: E402
from pseudo_pro_v2.validators import validate_stage_contract_registry_inputs, validate_stage_snapshot_payload  # noqa: E402


class StageContractsTests(unittest.TestCase):
    def test_stage_contract_registry_is_machine_checkable(self) -> None:
        self.assertEqual(validate_stage_contract_registry_inputs(), [])

    def test_required_stages_exist(self) -> None:
        expected = {
            "intent_classifier",
            "risk_tier_classifier",
            "scope_budget_planner",
            "domain_adapter_generator",
            "source_strategy_builder",
            "evidence_collector",
            "report_planner",
            "draft_writer",
            "claim_extractor",
            "evidence_mapper",
            "contradiction_absence_guard",
            "tone_controller",
            "release_gate",
            "bundle_renderer",
        }
        self.assertTrue(expected.issubset(set(STAGE_CONTRACTS)))

    def test_stage_failure_codes_are_known(self) -> None:
        for contract in STAGE_CONTRACTS.values():
            for failure_code in contract["failure_codes"]:
                self.assertIn(failure_code, STAGE_FAILURE_CODES)

    def test_stage_snapshot_validator_rejects_missing_fields(self) -> None:
        errors = validate_stage_snapshot_payload({"stage_name": "draft_writer"})
        self.assertTrue(errors)
        self.assertIn("stage snapshot missing required fields", errors[0])

    def test_stage_snapshot_validator_accepts_full_payload(self) -> None:
        snapshot = {
            "stage_name": "draft_writer",
            "inputs_summary": {"request": "ok"},
            "outputs_summary": {"units": 3},
            "failure_codes": [],
            "invariants_checked": ["section titles remain reader-facing"],
        }
        self.assertEqual(validate_stage_snapshot_payload(snapshot), [])
        self.assertEqual(set(snapshot), STAGE_SNAPSHOT_REQUIRED_FIELDS)


if __name__ == "__main__":
    unittest.main()
