from __future__ import annotations

from pathlib import Path

from runtime_bootstrap import ensure_runtime_namespace

ROOT = Path(__file__).resolve().parents[1]
ensure_runtime_namespace()

from cleanroom_runtime.pipeline import run_pipeline  # noqa: E402
from cleanroom_runtime.models import PipelineBundle, RunRequest  # noqa: E402


def run_multigenre_pipeline(request: RunRequest, output_dir: Path | None = None) -> PipelineBundle:
    return run_pipeline(request, output_dir=output_dir)
