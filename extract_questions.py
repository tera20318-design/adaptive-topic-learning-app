#!/usr/bin/env python3
"""
PDF → Claude Vision → questions.json 変換スクリプト

使い方:
  python extract_questions.py

環境変数:
  ANTHROPIC_API_KEY  (必須)

動作:
  OneDrive内のPDFを1ページずつPNG変換し、
  Claude に問題・選択肢・正解・解説を抽出させて questions.json に保存する。
  途中で止まっても resume.json から再開できる。
"""

import base64
import json
import os
import sys
import time
import pathlib
import fitz  # PyMuPDF

import anthropic

# ===== 設定 =====
PDF_DIR   = pathlib.Path("C:/Users/tera2/OneDrive - 公益財団法⼈　広島市産業振興センター")
OUT_FILE  = pathlib.Path("app/questions.json")
RESUME    = pathlib.Path("extract_resume.json")
DPI_SCALE = 2.0   # 解像度倍率 (2.0 = 144dpi相当)
MODEL     = "claude-opus-4-6"

PROMPT = """この画像は日本語の学習問題集のページです。
ページ内にある**すべての問題**を抽出してください。

以下のJSON配列形式で返してください。コードブロック(```)は不要です。

[
  {
    "text": "問題文（問題番号を含む）",
    "choices": ["①選択肢A", "②選択肢B", "③選択肢C", "④選択肢D", "⑤選択肢E"],
    "answer": 0,
    "explanation": "解説や正解の根拠（ページ内にあれば）"
  }
]

ルール:
- answer は 0始まりのインデックス（①が正解なら0）
- 正解が画像内に記載されていない場合は answer を null にする
- 解説がなければ explanation を "" にする
- 問題がないページ（目次・表紙等）は空配列 [] を返す
- 選択肢の番号・記号（①②③ / ABC / 1234）はそのまま含める
"""

# ===== デモ問題 =====
DEMO_QUESTIONS = [
    {
        "id": "demo_001",
        "chapter": "★ デモ問題",
        "page": 0,
        "text": "これはデモ問題です。正しい選択肢を選んでください。",
        "choices": ["①選択肢A（正解）", "②選択肢B", "③選択肢C", "④選択肢D"],
        "answer": 0,
        "explanation": "①が正解です。デモ用の解説です。",
        "needs_review": False,
        "source_pdf": "",
        "source_page": 0,
    }
]


def page_to_b64(pdf_path: pathlib.Path, page_idx: int) -> str:
    doc = fitz.open(pdf_path)
    page = doc[page_idx]
    mat = fitz.Matrix(DPI_SCALE, DPI_SCALE)
    pix = page.get_pixmap(matrix=mat)
    data = pix.tobytes("png")
    doc.close()
    return base64.standard_b64encode(data).decode()


def extract_from_page(client: anthropic.Anthropic, b64: str) -> list[dict]:
    msg = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": b64,
                    },
                },
                {"type": "text", "text": PROMPT},
            ],
        }],
    )
    raw = msg.content[0].text.strip()
    # コードブロックが付いていたら除去
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        raw = raw.rsplit("```", 1)[0]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"    JSON解析失敗: {raw[:100]}")
        return []


def load_resume() -> dict:
    if RESUME.exists():
        return json.loads(RESUME.read_text(encoding="utf-8"))
    return {"done": [], "questions": []}


def save_resume(state: dict):
    RESUME.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("エラー: ANTHROPIC_API_KEY 環境変数を設定してください")
        print("  set ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"PDFが見つかりません: {PDF_DIR}")
        sys.exit(1)

    state = load_resume()
    done_set = set(state["done"])
    all_questions = state["questions"]

    q_id = len(all_questions) + 1

    for pdf in pdfs:
        doc = fitz.open(pdf)
        n_pages = doc.page_count
        doc.close()

        # 章名: "001" 形式
        idx = pdfs.index(pdf) + 1
        chapter = f"第{idx:02d}章"

        for page_idx in range(n_pages):
            key = f"{pdf.name}:{page_idx}"
            if key in done_set:
                continue

            print(f"[{chapter} p{page_idx+1}/{n_pages}] {pdf.name[:30]}...", end=" ", flush=True)

            try:
                b64 = page_to_b64(pdf, page_idx)
                items = extract_from_page(client, b64)
                print(f"{len(items)}問")

                for item in items:
                    q = {
                        "id": f"q{q_id:04d}",
                        "chapter": chapter,
                        "page": page_idx + 1,
                        "text": item.get("text", ""),
                        "choices": item.get("choices", []),
                        "answer": item.get("answer", None),
                        "explanation": item.get("explanation", ""),
                        "needs_review": item.get("answer") is None,
                        "source_pdf": pdf.name,
                        "source_page": page_idx + 1,
                    }
                    all_questions.append(q)
                    q_id += 1

                done_set.add(key)
                state["done"] = list(done_set)
                state["questions"] = all_questions
                save_resume(state)

                # レート制限対策
                time.sleep(0.5)

            except anthropic.RateLimitError:
                print("レート制限 - 60秒待機")
                time.sleep(60)
                # 再試行
                b64 = page_to_b64(pdf, page_idx)
                items = extract_from_page(client, b64)
                for item in items:
                    q = {
                        "id": f"q{q_id:04d}",
                        "chapter": chapter,
                        "page": page_idx + 1,
                        "text": item.get("text", ""),
                        "choices": item.get("choices", []),
                        "answer": item.get("answer", None),
                        "explanation": item.get("explanation", ""),
                        "needs_review": item.get("answer") is None,
                        "source_pdf": pdf.name,
                        "source_page": page_idx + 1,
                    }
                    all_questions.append(q)
                    q_id += 1
                done_set.add(key)
                state["done"] = list(done_set)
                state["questions"] = all_questions
                save_resume(state)

            except Exception as e:
                print(f"エラー: {e}")
                time.sleep(2)
                continue

    # questions.json に書き出し
    output = {
        "meta": {
            "title": "学習問題集",
            "version": "2.0",
            "source": "Claude Vision抽出",
            "total_questions": len(DEMO_QUESTIONS) + len(all_questions),
            "needs_review_count": sum(1 for q in all_questions if q.get("needs_review")),
        },
        "questions": DEMO_QUESTIONS + all_questions,
    }
    OUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n完了: {OUT_FILE}")
    print(f"  総問題数: {len(DEMO_QUESTIONS) + len(all_questions)}")
    print(f"  正解設定済み: {sum(1 for q in all_questions if q.get('answer') is not None)}")
    print(f"  要確認: {sum(1 for q in all_questions if q.get('needs_review'))}")

    # 中間ファイル削除
    if RESUME.exists():
        RESUME.unlink()


if __name__ == "__main__":
    main()
