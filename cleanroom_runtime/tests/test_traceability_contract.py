from __future__ import annotations

from dataclasses import replace
import unittest

from runtime_bootstrap import ensure_repo_paths


ensure_repo_paths(include_tests=True)

from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.stages.release_gate import decide_release_gate  # noqa: E402
from cleanroom_runtime.validators import validate_bundle_contracts  # noqa: E402
from support import make_finding, make_packet, make_request  # noqa: E402


class TraceabilityContractTests(unittest.TestCase):
    def test_pipeline_populates_claim_and_citation_traceability_fields(self) -> None:
        bundle = run_pipeline(
            make_request(
                packets=[
                    make_packet(
                        "SRC-001",
                        "government_context",
                        findings=[
                            make_finding(
                                "finding-001",
                                "The checked packet supports a bounded runtime statement.",
                                "fact",
                                "medium",
                                "findings",
                                source_ids=["SRC-001"],
                                source_excerpt="The checked packet supports a bounded runtime statement.",
                                grounding_kind="paraphrase",
                                source_span_start=0,
                                source_span_end=58,
                                subject_key="bounded runtime statement",
                            )
                        ],
                    )
                ]
            )
        )

        included_claims = [claim for claim in bundle.claims if claim.included_in_report]
        self.assertTrue(included_claims)
        self.assertTrue(all(claim.report_span_id and claim.report_line_start > 0 for claim in included_claims))
        self.assertTrue(all(claim.trace_status == "linked" for claim in included_claims))
        self.assertTrue(all(citation.source_finding_ids for citation in bundle.citations))
        self.assertTrue(all(citation.trace_status == "linked" for citation in bundle.citations if citation.included_in_report))

    def test_bundle_validator_rejects_tampered_traceability(self) -> None:
        bundle = run_pipeline(
            make_request(
                packets=[
                    make_packet(
                        "SRC-010",
                        "government_context",
                        findings=[
                            make_finding(
                                "finding-010",
                                "The checked packet supports another bounded statement.",
                                "fact",
                                "medium",
                                "findings",
                                source_ids=["SRC-010"],
                                source_excerpt="The checked packet supports another bounded statement.",
                                grounding_kind="paraphrase",
                                source_span_start=0,
                                source_span_end=56,
                                subject_key="another bounded statement",
                            )
                        ],
                    )
                ]
            )
        )

        tampered_claims = [replace(bundle.claims[0], exact_text_span="Tampered span text.")]
        tampered_citations = [replace(bundle.citations[0], source_finding_ids=[])]
        errors = validate_bundle_contracts(bundle.draft, tampered_claims, tampered_citations, bundle.evidence)

        self.assertTrue(any("exact_text_span" in error or "source_finding_ids" in error for error in errors))

    def test_release_gate_blocks_on_traceability_mismatch(self) -> None:
        bundle = run_pipeline(
            make_request(
                packets=[
                    make_packet(
                        "SRC-020",
                        "official_regulator",
                        findings=[
                            make_finding(
                                "finding-020",
                                "The checked rule remains bounded to the reviewed scope.",
                                "regulatory",
                                "high",
                                "direct_answer",
                                source_ids=["SRC-020"],
                                source_excerpt="The checked rule remains bounded to the reviewed scope.",
                                grounding_kind="paraphrase",
                                source_span_start=0,
                                source_span_end=56,
                                subject_key="reviewed scope rule",
                            )
                        ],
                    )
                ]
            )
        )
        tampered_metrics = replace(bundle.metrics, traceability_complete=False, trace_mismatch_count=1)
        decision = decide_release_gate(
            draft=bundle.draft,
            claims=bundle.claims,
            citations=bundle.citations,
            contradictions=bundle.contradictions,
            gaps=bundle.gaps,
            budget=bundle.budget,
            adapter=bundle.adapter,
            metrics=tampered_metrics,
            validation_errors=[],
            request=bundle.request,
            intent=bundle.intent,
            risk=bundle.risk,
        )

        self.assertEqual(decision.status, "blocked")
        self.assertTrue(any("Traceability is incomplete" in issue.message for issue in decision.claim_issues))


if __name__ == "__main__":
    unittest.main()
