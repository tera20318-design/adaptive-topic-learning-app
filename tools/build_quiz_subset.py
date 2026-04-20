#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_INPUT = Path("app/questions.json")
DEFAULT_OUTPUT = Path("app/questions-first-pdf.json")
DEFAULT_UPDATED_AT = "2026/04/09"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a smaller quiz dataset from app/questions.json."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Source questions JSON. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output subset JSON. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--source-pdf",
        required=True,
        help="Exact source_pdf value to keep.",
    )
    parser.add_argument(
        "--title",
        default="エックス線作業主任者 学習問題集（1ファイル試作）",
        help="Dataset title written into meta.title.",
    )
    parser.add_argument(
        "--updated-at",
        default=DEFAULT_UPDATED_AT,
        help=f"meta.updatedAt value. Default: {DEFAULT_UPDATED_AT}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    source_questions = payload.get("questions", [])

    subset = [
        question
        for question in source_questions
        if question.get("source_pdf") == args.source_pdf
    ]
    subset.sort(
        key=lambda question: (
            question.get("chapter", ""),
            question.get("source_page", 0),
            question.get("id", ""),
        )
    )

    output = {
        "meta": {
            "title": args.title,
            "version": "1.0",
            "source": "app/questions.json から抽出",
            "sourcePdf": args.source_pdf,
            "updatedAt": args.updated_at,
            "total_questions": len(subset),
            "needs_review_count": sum(
                1 for question in subset if question.get("needs_review")
            ),
            "notes": [
                "1ファイルのみを切り出した試作用データです。",
                "正解は未設定のため、回答後はレビュー表示になります。",
            ],
        },
        "questions": subset,
    }

    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"wrote {args.output}")
    print(f"source_pdf={args.source_pdf}")
    print(f"questions={len(subset)}")


if __name__ == "__main__":
    main()
