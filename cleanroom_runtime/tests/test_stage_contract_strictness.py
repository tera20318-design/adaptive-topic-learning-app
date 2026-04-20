from __future__ import annotations

import unittest

from runtime_bootstrap import ensure_repo_paths


ensure_repo_paths()

from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.stage_contracts import (  # noqa: E402
    STAGE_CONTRACTS,
    audit_stage_output,
    stage_failure_codes,
    stage_snapshot_schema,
    validate_stage_contract_registry,
    validate_stage_snapshot,
)
from cleanroom_runtime.types import StageFailureCode, STAGE_SNAPSHOT_SCHEMA_VERSION  # noqa: E402

from support import make_finding, make_packet, make_request  # noqa: E402


class StageContractStrictnessTests(unittest.TestCase):
    def test_stage_contract_registry_remains_strict(self) -> None:
        self.assertEqual(validate_stage_contract_registry(), [])
        self.assertTrue(all(spec.strictness == "strict" for spec in STAGE_CONTRACTS.values()))

    def test_failure_code_enum_covers_declared_contract_codes(self) -> None:
        enum_codes = set(stage_failure_codes())
        declared_codes = {
            StageFailureCode.REQUIRED_FIELD_MISSING,
            StageFailureCode.DOWNSTREAM_FIELD_MISSING,
            StageFailureCode.SCHEMA_VALIDATION_FAILED,
        }
        for spec in STAGE_CONTRACTS.values():
            for invariant in spec.invariants:
                declared_codes.update(invariant.emitted_codes or (invariant.code,))

        self.assertEqual(stage_snapshot_schema()["snapshot_schema_version"], STAGE_SNAPSHOT_SCHEMA_VERSION)
        self.assertEqual(set(stage_snapshot_schema()["failure_code_enum"]), {code.value for code in enum_codes})
        self.assertEqual(declared_codes, enum_codes)

    def test_missing_required_field_fails_cleanly_without_validator_crash(self) -> None:
        failures, snapshot = audit_stage_output("report_planner", {})

        self.assertIn(StageFailureCode.REQUIRED_FIELD_MISSING, {failure.code for failure in failures})
        self.assertNotIn(StageFailureCode.SCHEMA_VALIDATION_FAILED, {failure.code for failure in failures})
        self.assertFalse(snapshot.contract_ok)

    def test_pipeline_snapshots_validate_against_snapshot_schema(self) -> None:
        bundle = run_pipeline(
            make_request(
                packets=[
                    make_packet(
                        "SRC-001",
                        "government_context",
                        findings=[
                            make_finding(
                                "finding-001",
                                "The runtime keeps claim handling bounded to the checked packet.",
                                "fact",
                                "medium",
                                "findings",
                                source_ids=["SRC-001"],
                            )
                        ],
                    )
                ]
            )
        )

        self.assertTrue(bundle.stage_snapshots)
        self.assertEqual(
            [error for snapshot in bundle.stage_snapshots for error in validate_stage_snapshot(snapshot)],
            [],
        )
        self.assertTrue(
            all(set(snapshot.summary.keys()) == set(STAGE_CONTRACTS[snapshot.stage].snapshot_fields) for snapshot in bundle.stage_snapshots)
        )
if __name__ == "__main__":
    unittest.main()
