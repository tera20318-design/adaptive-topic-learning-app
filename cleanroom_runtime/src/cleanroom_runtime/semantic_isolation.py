from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable

from .types import StageFailureCode


SEMANTIC_LEAKAGE_PATTERNS: dict[str, tuple[str, ...]] = {
    "fixture_specific_noun": (
        "pseudo pro v2",
        "research os v2",
        "microsoft ai tour tokyo",
        "mame17",
        "first pdf manual dataset",
    ),
    "risk_phrase": (
        "medical diagnosis",
        "clinical treatment plan",
        "investment advice",
        "securities recommendation",
    ),
    "regulation_wording": (
        "the regulation definitely applies",
        "guaranteed compliance",
        "fully compliant with all applicable laws",
        "regulator approved for all use cases",
    ),
    "overclaim_phrasing": (
        "complete and exhaustive",
        "definitive answer",
        "no further verification is needed",
        "fully settles the question",
    ),
}

SEMANTIC_LEAKAGE_CODES: dict[str, StageFailureCode] = {
    "fixture_specific_noun": StageFailureCode.SEMANTIC_FIXTURE_NOUN_LEAK,
    "risk_phrase": StageFailureCode.SEMANTIC_RISK_PHRASE_LEAK,
    "regulation_wording": StageFailureCode.SEMANTIC_REGULATION_WORDING_LEAK,
    "overclaim_phrasing": StageFailureCode.SEMANTIC_OVERCLAIM_PHRASING_LEAK,
}

ANCHORABLE_CATEGORIES = frozenset({"fixture_specific_noun", "risk_phrase"})


@dataclass(frozen=True, slots=True)
class SemanticLeakageFinding:
    category: str
    code: StageFailureCode
    phrase: str
    text: str


def detect_semantic_leakage(
    value: Any,
    *,
    anchor_values: Iterable[Any] | None = None,
    categories: Iterable[str] | None = None,
    extra_patterns: dict[str, Iterable[str]] | None = None,
) -> list[SemanticLeakageFinding]:
    selected_categories = list(categories or SEMANTIC_LEAKAGE_PATTERNS.keys())
    merged_patterns = _merged_patterns(extra_patterns)
    candidate_texts = _collect_strings(value)
    anchor_texts = _collect_strings(anchor_values or [])
    normalized_anchor_texts = [_normalize_for_match(text) for text in anchor_texts if text.strip()]
    findings: list[SemanticLeakageFinding] = []
    seen: set[tuple[str, str, str]] = set()

    for text in candidate_texts:
        normalized_text = _normalize_for_match(text)
        if not normalized_text:
            continue
        for category in selected_categories:
            for phrase in merged_patterns.get(category, ()):
                normalized_phrase = _normalize_for_match(phrase)
                if normalized_phrase not in normalized_text:
                    continue
                if category in ANCHORABLE_CATEGORIES and any(normalized_phrase in anchor for anchor in normalized_anchor_texts):
                    continue
                key = (category, normalized_phrase, normalized_text)
                if key in seen:
                    continue
                seen.add(key)
                findings.append(
                    SemanticLeakageFinding(
                        category=category,
                        code=SEMANTIC_LEAKAGE_CODES[category],
                        phrase=phrase,
                        text=text,
                    )
                )
    return findings


def semantic_anchor_values(*values: Any) -> list[Any]:
    anchors: list[Any] = []
    for value in values:
        if value is None:
            continue
        anchors.append(value)
    return anchors


def semantic_pattern_catalog(*, extra_patterns: dict[str, Iterable[str]] | None = None) -> dict[str, tuple[str, ...]]:
    return _merged_patterns(extra_patterns)


def _collect_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if value is None:
        return strings
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        for item in value.values():
            strings.extend(_collect_strings(item))
        return strings
    if isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            strings.extend(_collect_strings(item))
        return strings
    if hasattr(value, "to_dict"):
        return _collect_strings(value.to_dict())
    if hasattr(value, "__dict__"):
        return _collect_strings(vars(value))
    return strings


def _merged_patterns(extra_patterns: dict[str, Iterable[str]] | None) -> dict[str, tuple[str, ...]]:
    merged: dict[str, tuple[str, ...]] = {
        category: tuple(patterns)
        for category, patterns in SEMANTIC_LEAKAGE_PATTERNS.items()
    }
    if not extra_patterns:
        return merged
    for category, patterns in extra_patterns.items():
        merged[category] = tuple(dict.fromkeys([*merged.get(category, ()), *(pattern for pattern in patterns if pattern)]))
    return merged


def _normalize_for_match(value: str) -> str:
    lowered = value.casefold()
    cleaned = re.sub(r"[^a-z0-9]+", " ", lowered)
    return " ".join(cleaned.split())
