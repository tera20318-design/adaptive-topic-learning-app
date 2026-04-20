from __future__ import annotations

import csv
import sys
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

from cleanroom_runtime.models import CitationLedgerRow, ClaimLedgerRow, RawDocumentInput, RunRequest, TargetProfile  # noqa: E402
from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.validators import validate_citation_record, validate_claim_records  # noqa: E402


def _schema_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class TraceabilityV2Tests(unittest.TestCase):
    def test_claim_ledger_schema_documents_traceability_columns(self) -> None:
        rows = _schema_rows(ROOT / "claim-ledger.schema.tsv")
        by_name = {row["column_name"]: row for row in rows}

        for required in (
            "claim_id",
            "unit_id",
            "report_span_id",
            "exact_text_span",
            "normalized_claim",
            "origin_finding_ids",
            "trace_status",
            "report_line_start",
            "report_line_end",
        ):
            with self.subTest(column=required):
                self.assertIn(required, by_name)

        self.assertEqual(by_name["report_span_id"]["required"], "yes")
        self.assertEqual(by_name["trace_status"]["traceability_role"], "trace_integrity")
        self.assertEqual(by_name["origin_finding_ids"]["current_surface"], "tsv_and_bundle")

    def test_citation_ledger_schema_documents_traceability_columns(self) -> None:
        rows = _schema_rows(ROOT / "citation-ledger.schema.tsv")
        by_name = {row["column_name"]: row for row in rows}

        for required in (
            "citation_id",
            "claim_id",
            "report_span_id",
            "claim_span_start",
            "claim_span_end",
            "source_finding_ids",
            "source_excerpt",
            "source_span_start",
            "source_span_end",
            "trace_status",
            "provenance_complete",
        ):
            with self.subTest(column=required):
                self.assertIn(required, by_name)

        self.assertEqual(by_name["report_span_id"]["required"], "yes")
        self.assertEqual(by_name["provenance_complete"]["traceability_role"], "provenance_gate_hint")

    def test_claim_validator_requires_report_span_id_for_included_claims(self) -> None:
        claim = ClaimLedgerRow(
            claim_id="claim-001",
            unit_id="unit-001",
            report_section="Direct answer",
            report_section_key="direct_answer",
            report_span_id="",
            exact_text_span="Bounded supported statement.",
            normalized_claim="bounded supported statement.",
            claim_kind="fact",
            risk_level="medium",
            source_ids=["SRC-001"],
            source_roles=["government_context"],
            evidence_count=1,
            required_source_roles=["government_context"],
            matched_source_roles=["government_context"],
            support_status="supported",
            confidence=0.82,
            included_in_report=True,
            trace_status="linked",
        )
        claim.report_span_id = ""

        errors = validate_claim_records([claim])

        self.assertIn("claim claim-001 requires report_span_id when included_in_report is true", errors)

    def test_citation_validator_catches_trace_span_pairing_and_unknown_lineage(self) -> None:
        citation = CitationLedgerRow(
            citation_id="citation-001",
            claim_id="claim-001",
            report_section="Direct answer",
            source_id="SRC-UNKNOWN",
            source_role="government_context",
            source_title="Synthetic source",
            support_status="supported",
            included_in_report=True,
            report_span_id="",
            source_finding_ids=["finding-001"],
            source_span_start=10,
            source_span_end=None,
            trace_status="linked",
            provenance_complete=True,
        )

        errors = validate_citation_record(citation, {"claim-001"}, {"SRC-001"})

        self.assertIn("citation citation-001 requires report_span_id when included_in_report is true", errors)
        self.assertIn("citation.source_span_start and source_span_end must both be populated or both be omitted", errors)
        self.assertIn("citation citation-001 references unknown source_id 'SRC-UNKNOWN'", errors)

    def test_pipeline_should_link_prose_claims_and_grounded_citations_end_to_end(self) -> None:
        request = RunRequest(
            topic="Document grounding traceability check",
            reader="reviewer",
            use_context="Review the uploaded excerpt without extrapolating beyond the checked text",
            desired_depth="decision",
            jurisdiction="US",
            mode="scoped",
            evidence_mode="synthetic",
            question="What does the uploaded excerpt state directly?",
            raw_documents=[
                RawDocumentInput(
                    document_id="DOC-RAW-TRACE-001",
                    title="Uploaded excerpt",
                    content="Policy line one says coverage stays limited.\nPolicy line two says outside approval remains required.",
                    content_type="text/plain",
                    provided_at="2026-04-20",
                    excerpt_label="upload:trace",
                )
            ],
            target_profile=TargetProfile(min_sources=1, min_distinct_roles=1, min_high_risk_sources=0),
        )

        bundle = run_pipeline(request)

        self.assertTrue(bundle.metrics.traceability_complete)
        self.assertTrue(all(claim.trace_status == "linked" for claim in bundle.claims))
        self.assertTrue(all(claim.origin_finding_ids for claim in bundle.claims))
        self.assertTrue(all(citation.report_span_id for citation in bundle.citations))
        self.assertTrue(all(citation.source_finding_ids for citation in bundle.citations))
        self.assertTrue(all(citation.source_excerpt for citation in bundle.citations))
        self.assertTrue(all(citation.trace_status == "linked" for citation in bundle.citations))


if __name__ == "__main__":
    unittest.main()
