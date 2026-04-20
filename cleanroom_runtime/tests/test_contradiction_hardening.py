from __future__ import annotations

import unittest

from runtime_bootstrap import ensure_repo_paths


ensure_repo_paths(include_tests=True)

from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from support import make_finding, make_packet, make_request  # noqa: E402


class ContradictionHardeningTests(unittest.TestCase):
    def test_same_subject_authoritative_conflict_blocks_release(self) -> None:
        request = make_request(
            topic="Same-subject authoritative contradiction",
            use_context="decide whether the checked rule applies to the same bounded workflow",
            packets=[
                make_packet(
                    "SRC-001",
                    "official_regulator",
                    published_on="2026-03-01",
                    findings=[
                        make_finding(
                            "finding-001",
                            "The checked rule applies to the bounded workflow.",
                            "regulatory",
                            "high",
                            "direct_answer",
                            source_ids=["SRC-001"],
                            subject_key="bounded workflow rule applicability",
                        )
                    ],
                ),
                make_packet(
                    "SRC-002",
                    "legal_text",
                    published_on="2026-03-02",
                    findings=[
                        make_finding(
                            "finding-002",
                            "The checked rule does not apply to the bounded workflow.",
                            "regulatory",
                            "high",
                            "analysis",
                            source_ids=["SRC-002"],
                            subject_key="bounded workflow rule applicability",
                        )
                    ],
                ),
            ],
        )

        bundle = run_pipeline(request)

        self.assertEqual(bundle.release_gate.status, "blocked")
        self.assertTrue(any(entry.contradiction_class == "same_subject_authoritative_conflict" for entry in bundle.contradictions))

    def test_different_subject_conflict_language_does_not_create_false_contradiction(self) -> None:
        request = make_request(
            topic="Different subject separation",
            use_context="review two different subject statements without conflating them",
            packets=[
                make_packet(
                    "SRC-003",
                    "government_context",
                    findings=[
                        make_finding(
                            "finding-003",
                            "The checked process does not cover subject alpha.",
                            "fact",
                            "medium",
                            "findings",
                            source_ids=["SRC-003"],
                            subject_key="subject alpha",
                        )
                    ],
                ),
                make_packet(
                    "SRC-004",
                    "government_context",
                    findings=[
                        make_finding(
                            "finding-004",
                            "The checked process covers subject beta.",
                            "fact",
                            "medium",
                            "analysis",
                            source_ids=["SRC-004"],
                            subject_key="subject beta",
                        )
                    ],
                ),
            ],
        )

        bundle = run_pipeline(request)

        self.assertEqual(bundle.metrics.contradiction_count, 0)

    def test_stale_current_tension_is_recorded(self) -> None:
        request = make_request(
            topic="Stale current tension",
            use_context="review the checked source set before using the older rule statement",
            packets=[
                make_packet(
                    "SRC-005",
                    "official_regulator",
                    published_on="2024-02-01",
                    findings=[
                        make_finding(
                            "finding-005",
                            "The checked rule applies to the bounded workflow.",
                            "regulatory",
                            "high",
                            "direct_answer",
                            source_ids=["SRC-005"],
                            subject_key="bounded workflow freshness",
                        )
                    ],
                ),
                make_packet(
                    "SRC-006",
                    "official_regulator",
                    published_on="2026-03-01",
                    findings=[
                        make_finding(
                            "finding-006",
                            "The checked rule does not apply to the bounded workflow.",
                            "regulatory",
                            "high",
                            "analysis",
                            source_ids=["SRC-006"],
                            subject_key="bounded workflow freshness",
                        )
                    ],
                ),
            ],
        )

        bundle = run_pipeline(request)

        self.assertTrue(any(entry.contradiction_class in {"stale_current_tension", "same_subject_authoritative_conflict"} for entry in bundle.contradictions))
        self.assertEqual(bundle.release_gate.status, "blocked")


if __name__ == "__main__":
    unittest.main()
