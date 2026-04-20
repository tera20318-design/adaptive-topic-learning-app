#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

import easyocr
import fitz
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OCR selected pages from a scanned PDF into cache folders."
    )
    parser.add_argument("--pdf", type=Path, required=True, help="Target PDF path.")
    parser.add_argument(
        "--cache-dir",
        type=Path,
        required=True,
        help="Output directory containing pages/ and raw_text/ subdirectories.",
    )
    parser.add_argument(
        "--pages",
        required=True,
        help="1-based page spec such as 1-3,5,8-10",
    )
    parser.add_argument("--force", action="store_true", help="Re-run OCR even if cached.")
    return parser.parse_args()


def parse_page_spec(spec: str) -> list[int]:
    pages: set[int] = set()
    for chunk in spec.split(","):
        token = chunk.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if start > end:
                start, end = end, start
            pages.update(range(start, end + 1))
        else:
            pages.add(int(token))
    if not pages:
        raise SystemExit("No pages were selected.")
    return sorted(pages)


def render_page_image(doc: fitz.Document, page_index: int, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        return

    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
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
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def ocr_page(reader: easyocr.Reader, image_path: Path, text_path: Path, force: bool) -> str:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    if text_path.exists() and not force:
        return text_path.read_text(encoding="utf-8")

    items = reader.readtext(str(image_path), detail=1, paragraph=False)
    raw_text = "\n".join(group_ocr_lines(items)).strip()
    normalized = normalize_page_text(raw_text)
    text_path.write_text(normalized + "\n", encoding="utf-8")
    return normalized


def main() -> None:
    args = parse_args()
    pdf_path = args.pdf if args.pdf.is_absolute() else args.pdf.resolve()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    pages = parse_page_spec(args.pages)
    reader = easyocr.Reader(["ja", "en"], gpu=False)
    page_dir = args.cache_dir / "pages"
    text_dir = args.cache_dir / "raw_text"

    with fitz.open(pdf_path) as doc:
        for page_number in pages:
            if not 1 <= page_number <= doc.page_count:
                raise SystemExit(f"Page out of range: {page_number} / {doc.page_count}")
            page_index = page_number - 1
            image_path = page_dir / f"{page_number:04d}.png"
            text_path = text_dir / f"{page_number:04d}.txt"
            render_page_image(doc, page_index, image_path)
            ocr_page(reader, image_path, text_path, force=args.force)
            print(f"OCR OK: page {page_number:04d}")


if __name__ == "__main__":
    main()
