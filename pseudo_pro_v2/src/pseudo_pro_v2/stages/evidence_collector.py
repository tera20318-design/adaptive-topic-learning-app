from __future__ import annotations

from collections import Counter

from pseudo_pro_v2.models import CollectedEvidence, RunRequest


def collect_evidence(request: RunRequest) -> CollectedEvidence:
    findings = []
    quality_notes = []
    role_counts = Counter()

    for source in request.source_packets:
        role_counts[source.source_role] += 1
        if "outdated" in source.quality_flags:
            quality_notes.append(f"{source.source_id} is flagged outdated.")
        if source.source_role == "vendor_first_party":
            quality_notes.append(f"{source.source_id} is vendor-first-party material.")
        for finding in source.findings:
            if not finding.source_ids:
                finding.source_ids = [source.source_id]
            if not finding.source_roles:
                finding.source_roles = [source.source_role]
            findings.append(finding)

    return CollectedEvidence(
        sources=request.source_packets,
        findings=findings,
        source_counts_by_role=dict(role_counts),
        quality_notes=quality_notes,
    )
