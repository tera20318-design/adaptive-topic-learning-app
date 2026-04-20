from __future__ import annotations

import csv
from dataclasses import replace
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SRC = ROOT / "src"
for candidate in (TESTS, SRC):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from runtime_bootstrap import ensure_runtime_namespace


ensure_runtime_namespace()

from cleanroom_runtime.models import RawDocumentInput, TargetProfile  # noqa: E402
from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.stages.bundle_renderer import render_bundle  # noqa: E402
from cleanroom_runtime.stages.release_gate import decide_release_gate  # noqa: E402
from support import make_finding, make_packet, make_request  # noqa: E402


def _schema_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class TraceabilityV3Tests(unittest.TestCase):
    def test_schema_documents_span_based_v3_columns_as_rendered(self) -> None:
        claim_rows = _schema_rows(ROOT / "claim-ledger.schema.tsv")
        citation_rows = _schema_rows(ROOT / "citation-ledger.schema.tsv")
        claim_by_name = {row["column_name"]: row for row in claim_rows}
        citation_by_name = {row["column_name"]: row for row in citation_rows}

        for required in (
            "claim_span_start",
            "claim_span_end",
            "finding_span_labels",
            "finding_span_starts",
            "finding_span_ends",
            "grounding_marker",
            "grounding_scope_note",
        ):
            with self.subTest(column=required):
                self.assertIn(required, claim_by_name)
                self.assertEqual(claim_by_name[required]["current_surface"], "tsv_and_bundle")

        for required in (
            "claim_span_start",
            "claim_span_end",
            "source_span_labels",
            "source_span_starts",
            "source_span_ends",
            "grounding_marker",
            "grounding_scope_note",
        ):
            with self.subTest(column=required):
                self.assertIn(required, citation_by_name)
                self.assertEqual(citation_by_name[required]["current_surface"], "tsv_and_bundle")

    def test_rendered_ledgers_keep_span_based_traceability_columns(self) -> None:
        request = make_request(
            topic="Traceability v3 rendered ledgers",
            use_context="review the uploaded checked document without going beyond the grounded spans",
            raw_documents=[
                RawDocumentInput(
                    document_id="DOC-TRACE-V3-001",
                    title="Uploaded checked document",
                    content=(
                        "Paragraph one keeps the checked scope narrow.\n"
                        "Paragraph one still requires approval.\n\n"
                        "Paragraph two says separate review remains required."
                    ),
                    provided_at="2026-04-21",
                    review_mode="document_review",
                )
            ],
        )
        request.target_profile = TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=0)
        bundle = run_pipeline(request)

        with tempfile.TemporaryDirectory() as tempdir:
            render_bundle(bundle, Path(tempdir))
            claim_rows = _tsv_rows(Path(tempdir) / "claim-ledger.tsv")
            citation_rows = _tsv_rows(Path(tempdir) / "citation-ledger.tsv")

        self.assertTrue(claim_rows)
        self.assertTrue(citation_rows)
        claim_headers = set(claim_rows[0].keys())
        citation_headers = set(citation_rows[0].keys())
        self.assertTrue(
            {
                "normalized_claim",
                "claim_span_start",
                "claim_span_end",
                "finding_span_labels",
                "finding_span_starts",
                "finding_span_ends",
                "grounding_marker",
                "grounding_scope_note",
            }
            <= claim_headers
        )
        self.assertTrue(
            {
                "claim_span_start",
                "claim_span_end",
                "source_span_labels",
                "source_span_starts",
                "source_span_ends",
                "grounding_marker",
                "grounding_scope_note",
            }
            <= citation_headers
        )
        self.assertTrue(any(row["grounding_marker"].startswith("direct_document_") for row in claim_rows))
        self.assertTrue(any(row["source_span_starts"] for row in citation_rows))
        self.assertTrue(any("checked document" in row["grounding_scope_note"].casefold() for row in citation_rows))

    def test_release_gate_blocks_high_risk_claim_without_claim_span(self) -> None:
        bundle = run_pipeline(
            make_request(
                packets=[
                    make_packet(
                        "SRC-TRACE-V3-001",
                        "official_regulator",
                        findings=[
                            make_finding(
                                "finding-trace-v3-001",
                                "The checked rule remains bounded to the reviewed scope.",
                                "regulatory",
                                "high",
                                "direct_answer",
                                source_ids=["SRC-TRACE-V3-001"],
                                source_excerpt="The checked rule remains bounded to the reviewed scope.",
                                grounding_kind="paraphrase",
                                source_span_start=0,
                                source_span_end=56,
                                subject_key="reviewed-scope-rule",
                            )
                        ],
                    )
                ]
            )
        )
        tampered_claim = bundle.claims[0]
        tampered_claim.claim_span_start = None
        tampered_claim.claim_span_end = None
        tampered_metrics = replace(
            bundle.metrics,
            traceability_complete=True,
            trace_mismatch_count=0,
            citation_trace_complete=True,
            high_risk_traceability_mismatch_count=0,
        )

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
            decision_usable=None,
        )

        self.assertEqual(decision.status, "blocked")
        self.assertTrue(
            any("missing complete traceability" in issue.message.casefold() for issue in decision.claim_issues)
        )


if __name__ == "__main__":
    unittest.main()
