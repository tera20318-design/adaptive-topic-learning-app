from __future__ import annotations

import argparse
import csv
import re
import subprocess
import tempfile
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import fitz
from PIL import Image


INPUT_DIR = Path(r"C:\Users\tera2\OneDrive - 公益財団法⼈　広島市産業振興センター")
OUTPUT_DIR = Path(__file__).with_name("ocr_output")
TESSDATA_DIR = Path(r"C:\Users\tera2\tessdata")
TESSERACT_EXE = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
MERGED_RAW_PATH = OUTPUT_DIR / "all_documents_raw.txt"
MERGED_CLEAN_PATH = OUTPUT_DIR / "all_documents_clean.md"


@dataclass(frozen=True)
class PdfJob:
    pdf_path: Path
    output_stem: str
    page_dir: Path
    final_txt: Path
    page_count: int


def safe_slug(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return slug or "document"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OCR scanned PDF files into UTF-8 text.")
    parser.add_argument(
        "--pdf",
        type=Path,
        help="Process a single PDF file instead of the first PDF in the input folder.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Number of page workers to run in parallel. Default: 2",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=2.0,
        help="Render scale for each page before OCR. Default: 2.0",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process every PDF in the input folder instead of just one.",
    )
    return parser.parse_args()


def validate_environment() -> None:
    if not INPUT_DIR.exists():
        raise SystemExit(f"Input folder not found: {INPUT_DIR}")
    if not TESSERACT_EXE.exists():
        raise SystemExit(f"Tesseract not found: {TESSERACT_EXE}")
    if not TESSDATA_DIR.exists():
        raise SystemExit(f"Tessdata folder not found: {TESSDATA_DIR}")


def discover_pdfs(args: argparse.Namespace) -> list[Path]:
    if args.pdf is not None:
        pdf = args.pdf
        if not pdf.is_absolute():
            pdf = (Path.cwd() / pdf).resolve()
        if not pdf.exists():
            raise SystemExit(f"PDF not found: {pdf}")
        return [pdf]

    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDF files found in {INPUT_DIR}")
    if args.all:
        return pdfs
    return [pdfs[0]]


def build_jobs(pdfs: list[Path]) -> list[PdfJob]:
    jobs: list[PdfJob] = []
    for index, pdf_path in enumerate(pdfs, start=1):
        output_stem = f"{index:03d}_{safe_slug(pdf_path.stem)}"
        page_dir = OUTPUT_DIR / output_stem / "pages"
        final_txt = OUTPUT_DIR / f"{output_stem}.txt"
        doc = fitz.open(str(pdf_path))
        try:
            jobs.append(
                PdfJob(
                    pdf_path=pdf_path,
                    output_stem=output_stem,
                    page_dir=page_dir,
                    final_txt=final_txt,
                    page_count=doc.page_count,
                )
            )
        finally:
            doc.close()
    return jobs


def render_page_to_image(pdf_path: Path, page_number: int, scale: float) -> Image.Image:
    doc = fitz.open(str(pdf_path))
    try:
        page = doc[page_number]
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    finally:
        doc.close()

    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # These scans are sideways. Rotating once here makes the Japanese OCR
    # much more usable and lets us skip more expensive auto-rotation logic.
    return image.rotate(-90, expand=True)


def ocr_page(pdf_path: Path, page_number: int, scale: float) -> str:
    image = render_page_to_image(pdf_path, page_number, scale)

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        image_path = td_path / "page.png"
        out_base = td_path / "ocr"
        image.save(image_path)

        cmd = [
            str(TESSERACT_EXE),
            str(image_path),
            str(out_base),
            "-l",
            "jpn_vert+eng",
            "--tessdata-dir",
            str(TESSDATA_DIR),
            "--psm",
            "5",
            "--oem",
            "1",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(
                f"Tesseract failed for page {page_number + 1}:\n{proc.stderr.strip()}"
            )

        txt_path = out_base.with_suffix(".txt")
        return txt_path.read_text(encoding="utf-8", errors="replace").strip()


def page_text_path(page_dir: Path, page_number: int) -> Path:
    return page_dir / f"{page_number + 1:04d}.txt"


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_text(text, encoding="utf-8")
    tmp_path.replace(path)


def normalize_for_merge(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\x0c", "").replace("\u3000", " ")
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if re.fullmatch(r"\[Page \d+\]", line):
            continue
        if re.fullmatch(r"[0-9０-９]+", line):
            continue
        line = re.sub(r"[ \t]+", " ", line)
        lines.append(line)
    return "\n".join(lines).strip()


def write_merged_files(jobs: list[PdfJob]) -> None:
    raw_parts: list[str] = []
    clean_parts: list[str] = []

    for job in jobs:
        raw_text = job.final_txt.read_text(encoding="utf-8", errors="replace").strip()
        raw_parts.append(f"===== {job.output_stem} =====\n{raw_text}")

        clean_parts.append(f"# {job.output_stem}")
        for page_number in range(job.page_count):
            page_path = page_text_path(job.page_dir, page_number)
            page_text = page_path.read_text(encoding="utf-8", errors="replace").strip()
            clean_page = normalize_for_merge(page_text)
            clean_parts.append(f"## Page {page_number + 1}")
            clean_parts.append(clean_page or "(empty)")
            clean_parts.append("")

    write_text_atomic(MERGED_RAW_PATH, "\n\n".join(raw_parts).strip() + "\n")
    write_text_atomic(MERGED_CLEAN_PATH, "\n".join(clean_parts).strip() + "\n")


def process_job(job: PdfJob, workers: int, scale: float) -> None:
    job.page_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[{job.output_stem}] {job.pdf_path.name} ({job.page_count} pages)")

    pending_pages: list[int] = []
    for page_number in range(job.page_count):
        if not page_text_path(job.page_dir, page_number).exists():
            pending_pages.append(page_number)

    if pending_pages:
        print(f"  OCR pages to run: {len(pending_pages)}")
    else:
        print("  All page cache files already exist; rebuilding final text.")

    completed = 0
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(ocr_page, job.pdf_path, page_number, scale): page_number
            for page_number in pending_pages
        }
        for future in as_completed(futures):
            page_number = futures[future]
            text = future.result()
            page_path = page_text_path(job.page_dir, page_number)
            write_text_atomic(page_path, text)
            completed += 1
            print(f"  saved page {page_number + 1}/{job.page_count} ({completed}/{len(pending_pages)})")

    ordered_pages: list[str] = []
    for page_number in range(job.page_count):
        page_path = page_text_path(job.page_dir, page_number)
        if not page_path.exists():
            raise RuntimeError(f"Missing page cache after OCR: {page_path}")
        page_text = page_path.read_text(encoding="utf-8", errors="replace").strip()
        ordered_pages.append(f"[Page {page_number + 1}]\n{page_text}")

    final_text = "\n\n".join(ordered_pages)
    write_text_atomic(job.final_txt, final_text)
    print(f"  wrote {job.final_txt}")


def write_manifest(jobs: list[PdfJob]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT_DIR / "manifest.tsv"
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["index", "source_pdf", "output_txt", "page_count"])
        for index, job in enumerate(jobs, start=1):
            writer.writerow([index, job.pdf_path.name, job.final_txt.name, job.page_count])
    print(f"\nManifest: {manifest_path}")


def main() -> None:
    args = parse_args()
    validate_environment()

    pdfs = discover_pdfs(args)
    jobs = build_jobs(pdfs)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for job in jobs:
        process_job(job, workers=args.workers, scale=args.scale)

    write_merged_files(jobs)
    write_manifest(jobs)
    print(f"\nDone. Text files are in {OUTPUT_DIR}")
    print(f"  merged raw: {MERGED_RAW_PATH}")
    print(f"  merged clean: {MERGED_CLEAN_PATH}")


if __name__ == "__main__":
    main()
