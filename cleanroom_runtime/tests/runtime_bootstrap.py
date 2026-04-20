from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = ROOT / "tests"
PACKAGE_NAME = "cleanroom_runtime"
PACKAGE_DIR = SRC / PACKAGE_NAME
CORE_PACKAGE_NAME = f"{PACKAGE_NAME}.core"
CORE_PACKAGE_DIR = PACKAGE_DIR / "core"


def ensure_repo_paths(*, include_tests: bool = False) -> None:
    candidates = [ROOT, SRC]
    if include_tests:
        candidates.append(TESTS)
    for candidate in reversed(candidates):
        rendered = str(candidate)
        if rendered not in sys.path:
            sys.path.insert(0, rendered)


def ensure_runtime_namespace() -> None:
    ensure_repo_paths(include_tests=True)
    if PACKAGE_NAME not in sys.modules:
        package = types.ModuleType(PACKAGE_NAME)
        package.__path__ = [str(PACKAGE_DIR)]
        package.__file__ = str(PACKAGE_DIR / "__init__.py")
        sys.modules[PACKAGE_NAME] = package
    if CORE_PACKAGE_NAME not in sys.modules:
        core_package = types.ModuleType(CORE_PACKAGE_NAME)
        core_package.__path__ = [str(CORE_PACKAGE_DIR)]
        core_package.__file__ = str(CORE_PACKAGE_DIR / "__init__.py")
        sys.modules[CORE_PACKAGE_NAME] = core_package
    _ensure_sourceless_module(
        "cleanroom_runtime.core.gates.decision_usable",
        CORE_PACKAGE_DIR / "gates" / "__pycache__",
        "decision_usable*.pyc",
    )


def _ensure_sourceless_module(module_name: str, cache_dir: Path, pattern: str) -> None:
    if module_name in sys.modules:
        return
    matches = sorted(cache_dir.glob(pattern))
    if not matches:
        return
    loader = importlib.machinery.SourcelessFileLoader(module_name, str(matches[-1]))
    spec = importlib.util.spec_from_loader(module_name, loader)
    if spec is None:
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    loader.exec_module(module)
