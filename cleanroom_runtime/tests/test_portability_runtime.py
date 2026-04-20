from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

from runtime_bootstrap import ROOT, SRC, TESTS, ensure_repo_paths


ensure_repo_paths(include_tests=True)

from scripts.runtime_entrypoints import ensure_entrypoint_paths, regenerate_vertical_slices_main  # noqa: E402


ABSOLUTE_PATH_PATTERN = re.compile(r"([A-Za-z]:\\|/Users/|/home/|/tmp/)")


class PortabilityRuntimeTests(unittest.TestCase):
    def test_runtime_bootstrap_is_idempotent(self) -> None:
        ensure_repo_paths(include_tests=True)
        first_counts = {candidate: sys.path.count(str(candidate)) for candidate in (ROOT, SRC, TESTS)}

        ensure_repo_paths(include_tests=True)
        second_counts = {candidate: sys.path.count(str(candidate)) for candidate in (ROOT, SRC, TESTS)}

        self.assertEqual(first_counts, second_counts)
        self.assertTrue(all(count >= 1 for count in second_counts.values()))

    def test_script_entrypoints_are_normalized_around_shared_runtime_main(self) -> None:
        ensure_entrypoint_paths()
        self.assertTrue(callable(regenerate_vertical_slices_main))

        script_text = (ROOT / "scripts" / "regenerate_vertical_slices.py").read_text(encoding="utf-8")
        test_script_text = (ROOT / "tests" / "regenerate_multigenre_vertical_slices.py").read_text(encoding="utf-8")

        self.assertIn("regenerate_vertical_slices_main", script_text)
        self.assertIn("regenerate_vertical_slices_main", test_script_text)

    def test_live_lite_docs_and_reports_use_repo_relative_paths_only(self) -> None:
        for path in (
            ROOT / "live_lite_ingestion_plan.md",
            ROOT / "portability_cleanup_report.md",
            ROOT / "next_priorities.md",
            ROOT / "stage_contracts.md",
        ):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(ABSOLUTE_PATH_PATTERN.search(text))

    def test_normalized_source_packet_schema_is_present_and_shaped(self) -> None:
        schema = json.loads((ROOT / "normalized_source_packet.schema.json").read_text(encoding="utf-8"))
        core_schema = json.loads((ROOT / "core" / "schemas" / "normalized_source_packet.schema.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["title"], "NormalizedSourcePacket")
        self.assertEqual(schema["type"], "object")
        self.assertEqual(schema["required"], ["source_id", "title", "provenance"])
        self.assertIn("findings", schema["properties"])
        self.assertIn("source_role", schema["properties"])
        self.assertIn("provenance", schema["properties"])
        self.assertIn("role_assignment", schema["properties"])
        self.assertIn("dedupe", schema["properties"])
        self.assertIn("ingestion_health", schema["properties"])
        self.assertIn("staleness", schema["properties"])
        self.assertIn("$defs", schema)
        self.assertIn("sourceFinding", schema["$defs"])
        self.assertIn("absenceScope", schema["$defs"])
        self.assertIn("findingTraceability", schema["$defs"])
        self.assertEqual(core_schema["title"], schema["title"])
        self.assertIn("roleAssignment", core_schema["$defs"])


if __name__ == "__main__":
    unittest.main()
