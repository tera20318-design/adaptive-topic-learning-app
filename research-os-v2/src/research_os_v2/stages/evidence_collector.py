from __future__ import annotations

from datetime import date

from research_os_v2.models import CollectedEvidence, ResearchRequest


def collect_evidence(request: ResearchRequest) -> CollectedEvidence:
    findings = []
    counts_by_role: dict[str, int] = {}
    quality_notes: list[str] = []
    today = request.as_of_date or str(date.today())

    for source in request.source_packets:
        counts_by_role[source.source_role] = counts_by_role.get(source.source_role, 0) + 1
        if "outdated" in source.quality_flags:
            quality_notes.append(f"{source.source_id} is flagged outdated.")
        if source.source_role == "vendor_first_party":
            quality_notes.append(f"{source.source_id} is vendor-first-party material.")
        if source.published_on and source.published_on < str(int(today[:4]) - 5):
            quality_notes.append(f"{source.source_id} may be stale for date-sensitive topics.")
        findings.extend(source.findings)

    if not request.source_packets:
        quality_notes.append("No source packets were provided.")

    return CollectedEvidence(
        sources=request.source_packets,
        findings=findings,
        source_counts_by_role=counts_by_role,
        source_quality_notes=quality_notes,
    )
