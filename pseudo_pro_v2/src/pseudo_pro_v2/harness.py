from __future__ import annotations

import shutil
from pathlib import Path

from pseudo_pro_v2.pipeline import run_pipeline
from pseudo_pro_v2.runtime_paths import fixture_case_dir, generated_case_dir, package_root


DEFAULT_CASES = [
    "technical_overview",
    "legal_regulatory",
    "medical_health",
    "finance",
    "product_comparison",
    "business_market",
    "user_document_review",
    "historical_cultural",
]


def run_fixture_case(
    case_name: str,
    *,
    repo_root: Path | None = None,
    output_root: Path | None = None,
    clean_output: bool = True,
):
    root = repo_root or package_root()
    case_dir = fixture_case_dir(case_name, repo_root=root)
    output_dir = generated_case_dir(case_name, repo_root=root, output_root=output_root)
    request_path = case_dir / "request.json"
    source_packets_path = case_dir / "source_packets.json"

    if not request_path.exists() or not source_packets_path.exists():
        raise FileNotFoundError(f"Missing synthetic input for `{case_name}`.")
    if clean_output and output_dir.exists():
        shutil.rmtree(output_dir)

    bundle = run_pipeline(request_path, source_packets_path, output_dir)
    return bundle, output_dir
