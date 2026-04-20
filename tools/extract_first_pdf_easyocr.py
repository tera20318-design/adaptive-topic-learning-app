#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import easyocr
import fitz
from PIL import Image


DEFAULT_OUTPUT = Path("app/questions-first-pdf.json")
DEFAULT_CACHE_DIR = Path("ocr_output/easyocr_first_pdf")
DEFAULT_UPDATED_AT = "2026/04/09"
PDF_GLOB = r"OneDrive*\*11_59_54*スキャン.pdf"
CHAPTER_RE = re.compile(r"(?m)^(\d+\.\d+\s+[^\n]{2,60})$")
OPTION_LINE_RE = re.compile(r"^\((?P<num>[1-5])\)\s*(?P<text>.*)$")


@dataclass
class PageArtifact:
    page_number: int
    image_path: Path
    raw_text_path: Path
    normalized_text: str


@dataclass
class QuestionBlock:
    number: int
    chapter: str
    page_number: int
    header_line: str
    lines: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract first scanned PDF questions into app/questions-first-pdf.json."
    )
    parser.add_argument("--pdf", type=Path, help="Target PDF. Defaults to the first matching OneDrive scan.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help=f"Output JSON. Default: {DEFAULT_OUTPUT}")
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR, help=f"Image/OCR cache directory. Default: {DEFAULT_CACHE_DIR}")
    parser.add_argument("--updated-at", default=DEFAULT_UPDATED_AT, help=f"meta.updatedAt value. Default: {DEFAULT_UPDATED_AT}")
    parser.add_argument("--max-pages", type=int, default=0, help="Limit OCR to the first N pages for trial runs.")
    parser.add_argument("--force", action="store_true", help="Re-run OCR even if cached text files already exist.")
    return parser.parse_args()


def discover_pdf(explicit: Path | None) -> Path:
    if explicit is not None:
        pdf = explicit if explicit.is_absolute() else explicit.resolve()
        if not pdf.exists():
            raise SystemExit(f"PDF not found: {pdf}")
        return pdf

    matches = sorted(Path.home().glob(PDF_GLOB))
    if not matches:
        raise SystemExit(f"No PDF matched: {Path.home()}\\{PDF_GLOB}")
    return matches[0]


def render_page_image(doc: fitz.Document, page_index: int, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        return

    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # These phone scans are landscape pages photographed sideways.
    if image.width > image.height:
        image = image.rotate(90, expand=True)

    width, height = image.size
    image = image.crop((32, 20, width - 24, height - 24))
    image.save(output_path)


def group_ocr_lines(items: list[tuple]) -> list[str]:
    rows: list[tuple[float, float, float, str]] = []
    for box, text, _conf in items:
        xs = [point[0] for point in box]
        ys = [point[1] for point in box]
        rows.append((sum(ys) / len(ys), min(xs), max(ys) - min(ys), text))

    rows.sort()
    grouped: list[dict] = []
    for y, x, height, text in rows:
        if not grouped or abs(y - grouped[-1]["y"]) > max(grouped[-1]["height"], height) * 0.55:
            grouped.append({"y": y, "height": height, "parts": [(x, text)]})
        else:
            grouped[-1]["parts"].append((x, text))

    return [
        " ".join(part for _x, part in sorted(group["parts"])).strip()
        for group in grouped
        if any(part.strip() for _x, part in group["parts"])
    ]


def normalize_page_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u3000", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    text = re.sub(r"[（]\s*([1-5])\s*[）]", r"(\1)", text)
    text = re.sub(r"(?<=\d)\s*/\s*(?=\d)", "/", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def ocr_page(reader: easyocr.Reader, image_path: Path, text_path: Path, force: bool) -> str:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    if text_path.exists() and not force:
        return text_path.read_text(encoding="utf-8")

    items = reader.readtext(str(image_path), detail=1, paragraph=False)
    raw_text = "\n".join(group_ocr_lines(items)).strip()
    text_path.write_text(raw_text + "\n", encoding="utf-8")
    return raw_text


def build_page_artifacts(pdf_path: Path, cache_dir: Path, max_pages: int, force: bool) -> list[PageArtifact]:
    reader = easyocr.Reader(["ja", "en"], gpu=False)
    page_dir = cache_dir / "pages"
    ocr_dir = cache_dir / "raw_text"

    artifacts: list[PageArtifact] = []
    with fitz.open(pdf_path) as doc:
        page_count = doc.page_count if max_pages <= 0 else min(doc.page_count, max_pages)
        for page_index in range(page_count):
            image_path = page_dir / f"{page_index + 1:04d}.png"
            raw_text_path = ocr_dir / f"{page_index + 1:04d}.txt"
            render_page_image(doc, page_index, image_path)
            raw_text = ocr_page(reader, image_path, raw_text_path, force=force)
            artifacts.append(
                PageArtifact(
                    page_number=page_index + 1,
                    image_path=image_path,
                    raw_text_path=raw_text_path,
                    normalized_text=normalize_page_text(raw_text),
                )
            )
    return artifacts


def clean_segment(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -_:;,.、。")


def extract_example_number(line: str, previous: int | None) -> int | None:
    if "例題" not in line:
        return None

    digits = "".join(re.findall(r"\d", line))
    if digits:
        number = int(digits[:3])
        if previous is not None and number < previous and number < 10:
            return previous + 1
        return number

    return (previous + 1) if previous is not None else None


def find_option_start(lines: list[str]) -> int | None:
    markers = [
        (index, int(match.group("num")))
        for index, line in enumerate(lines)
        if (match := OPTION_LINE_RE.match(line))
    ]
    for marker_index, (line_index, number) in enumerate(markers):
        if number != 1:
            continue
        expected = 2
        run_length = 1
        for _next_line_index, next_number in markers[marker_index + 1:]:
            if next_number == expected:
                expected += 1
                run_length += 1
            elif next_number == 1:
                break
        if run_length >= 4:
            return line_index
    return None


def collect_blocks(artifacts: list[PageArtifact]) -> list[QuestionBlock]:
    blocks: list[QuestionBlock] = []
    current_chapter = "先頭PDF OCR"
    current_block: QuestionBlock | None = None
    previous_number: int | None = None

    for artifact in artifacts:
        for raw_line in artifact.normalized_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            chapter_match = CHAPTER_RE.match(line)
            if chapter_match:
                current_chapter = chapter_match.group(1).strip()

            if "例題" in line:
                number = extract_example_number(line, previous_number)
                if number is not None:
                    if current_block is not None:
                        blocks.append(current_block)
                    current_block = QuestionBlock(
                        number=number,
                        chapter=current_chapter,
                        page_number=artifact.page_number,
                        header_line=line,
                    )
                    previous_number = number
                    continue

            if current_block is not None:
                current_block.lines.append(line)

    if current_block is not None:
        blocks.append(current_block)
    return blocks


def split_stem_and_choices(block: QuestionBlock) -> tuple[str, list[str]] | None:
    lines = [line for line in block.lines if line]
    option_start = find_option_start(lines)
    if option_start is None:
        return None

    prelude = clean_segment(" ".join(lines[:option_start]))
    first_choice_prefix = ""
    if "。" in prelude:
        stem, first_choice_prefix = prelude.rsplit("。", 1)
        stem = stem.strip() + "。"
        first_choice_prefix = clean_segment(first_choice_prefix)
    else:
        stem = prelude

    choices: list[str] = []
    current_choice_parts: list[str] = []
    current_number: int | None = None

    for line in lines[option_start:]:
        match = OPTION_LINE_RE.match(line)
        if match:
            if current_number is not None:
                choices.append(clean_segment(" ".join(current_choice_parts)))
            current_number = int(match.group("num"))
            current_choice_parts = [match.group("text").strip()]
            if current_number == 1 and first_choice_prefix:
                current_choice_parts.insert(0, first_choice_prefix)
            continue

        if current_number is not None:
            current_choice_parts.append(line)

    if current_number is not None:
        choices.append(clean_segment(" ".join(current_choice_parts)))

    choices = [choice for choice in choices if choice]
    if len(choices) < 4:
        return None

    return stem, choices[:5]


def extract_questions(artifacts: list[PageArtifact], source_pdf: str) -> list[dict]:
    images_by_page = {artifact.page_number: artifact.image_path for artifact in artifacts}
    questions: list[dict] = []

    for next_id, block in enumerate(collect_blocks(artifacts), start=1):
        parsed = split_stem_and_choices(block)
        if parsed is None:
            continue
        stem, choices = parsed
        image_path = images_by_page[block.page_number]
        questions.append(
            {
                "id": f"fp{next_id:04d}",
                "chapter": block.chapter,
                "page": block.page_number,
                "header": f"例題{block.number}",
                "text": stem,
                "choices": choices,
                "answer": None,
                "explanation": "",
                "needs_review": True,
                "source_pdf": source_pdf,
                "source_page": block.page_number,
                "source_image": f"../{image_path.as_posix()}",
            }
        )

    return questions


def write_dataset(output_path: Path, pdf_path: Path, updated_at: str, questions: list[dict]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": {
            "title": "エックス線作業主任者 学習問題集（先頭PDF実OCR試作）",
            "version": "2.1",
            "source": "easyocr から実PDFを再抽出",
            "sourcePdf": pdf_path.name,
            "updatedAt": updated_at,
            "total_questions": len(questions),
            "needs_review_count": sum(1 for question in questions if question.get("needs_review")),
            "notes": [
                "先頭PDFを easyocr で直接読み直した試作データです。",
                "正解・解説は未設定です。原本ページ画像を見ながらレビューできます。",
            ],
        },
        "questions": questions,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    pdf_path = discover_pdf(args.pdf)
    artifacts = build_page_artifacts(pdf_path, args.cache_dir, args.max_pages, force=args.force)
    questions = extract_questions(artifacts, pdf_path.name)
    write_dataset(args.output, pdf_path, args.updated_at, questions)

    print(f"pdf={pdf_path.name}")
    print(f"pages={len(artifacts)}")
    print(f"questions={len(questions)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
