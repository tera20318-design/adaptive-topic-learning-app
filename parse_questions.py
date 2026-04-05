#!/usr/bin/env python3
"""
OCRテキスト → 問題JSON 変換スクリプト (改良版)

構造パターン:
  【型本】] or [補脇=...] or 「重可』] → 問題ヘッダー (ラベル)
  続く行                               → 問題文 / 補足
  (])  行                              → 選択肢① (OCR: (】)(ぶ)等)
  (ぃ) 行                              → 選択肢②
  (") 行                               → 選択肢③ (OCR: ("の)(e)(eu)等)
  (』) 行                              → 選択肢④ (OCR: (の)(ご)(oo)等)
  (mo) 行                              → 選択肢⑤ (OCR: (mu)(oo)等)

戦略:
  「選択肢マーカー3行以上が連続する塊」を見つけ、その直前の行群を問題文とする。
  OCRノイズが多いため全問 needs_review: true とし、手動修正前提とする。
"""

import re
import json
import os
from pathlib import Path
from dataclasses import dataclass, field

INPUT_DIR  = Path("ocr_output")
OUTPUT_FILE = Path("app/questions.json")
MIN_CHOICES = 3   # 最低この数の選択肢があれば問題とみなす
STEM_LOOKBACK = 15  # 問題文として遡る最大行数

# =========================================================
# 選択肢マーカー検出
# =========================================================
# OCRで (１)(ア) → (])(ぃ)(") etc に化ける
# 3〜5択の問題が多い
CHOICE_PATTERN = re.compile(
    r'^\s*'
    r'\('
    r'('
    r'[\]】\)）]'           # ① パターン: (]) (】) (）) etc
    r'|[ぃぃい][uo]?'       # ② パターン: (ぃ) (ぃu) (い)
    r'|[""\'"の]|e[u】]?|eu' # ③ パターン: (") (e) (eu) (の) ("の)
    r"|[''ご』のoo]"         # ④ パターン: (') (ご) (の) (oo)
    r'|mo|mu|oo'             # ⑤ パターン: (mo) (mu)
    r')'
    r'\)'
    r'\s*(.*)',
    re.UNICODE
)

# もう少し広めに: (英数字1-6文字) で始まる行も候補として
CHOICE_LOOSE = re.compile(r'^\s*\(([^\)\s]{1,5})\)\s*(.*)', re.UNICODE)

# ページ区切り
PAGE_RE  = re.compile(r'^\[Page\s*(\d+)\]')
# ドキュメント区切り
DOC_RE   = re.compile(r'^#\s*(\S+)')
# 問題ヘッダー: 【...】, [...], 「...」で始まる行
QHEADER_RE = re.compile(r'^[【\[「](.{1,20})[】\]」]')

# =========================================================
# データクラス
# =========================================================
@dataclass
class RawQuestion:
    doc: str
    page: int
    header: str = ""
    stem_lines: list = field(default_factory=list)
    choice_lines: list = field(default_factory=list)  # [(marker, text), ...]

# =========================================================
# パーサー本体
# =========================================================
def is_choice_line(line: str) -> tuple[bool, str, str]:
    """(マッチしたか, マーカー文字, テキスト)"""
    m = CHOICE_PATTERN.match(line)
    if m:
        return True, m.group(1), m.group(2).strip()
    # ゆるいパターンでも試す
    m2 = CHOICE_LOOSE.match(line)
    if m2:
        marker = m2.group(1)
        # 意味のありそうなマーカーだけ
        if len(marker) <= 4 and not marker.isdigit():
            return True, marker, m2.group(2).strip()
    return False, "", ""

def parse_file(path: Path, doc_name: str) -> list[RawQuestion]:
    """1ファイルから RawQuestion のリストを返す"""
    text = path.read_text(encoding='utf-8', errors='replace')
    lines = text.splitlines()

    questions: list[RawQuestion] = []
    current_page = 0
    current_header = ""

    # スライディングウィンドウで "選択肢ブロック" を検出
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # ページ更新
        pm = PAGE_RE.match(line)
        if pm:
            current_page = int(pm.group(1))
            i += 1
            continue

        # 問題ヘッダー
        hm = QHEADER_RE.match(line)
        if hm:
            current_header = line.strip()

        # 選択肢ブロックを探す
        ok, marker, text = is_choice_line(line)
        if ok:
            # 連続する選択肢行を収集
            choice_lines = [(marker, text)]
            j = i + 1
            while j < n and j < i + 40:
                ok2, m2, t2 = is_choice_line(lines[j])
                if ok2:
                    choice_lines.append((m2, t2))
                    j += 1
                elif lines[j].strip() == "":
                    # 空行をまたいでも継続 (OCRでは空行挿入されることが多い)
                    # ただし3行連続空行は終了
                    empty_count = 0
                    k = j
                    while k < n and lines[k].strip() == "":
                        empty_count += 1
                        k += 1
                    if empty_count >= 3:
                        break
                    j = k
                    continue
                else:
                    # 選択肢でも空行でもない行: 前の選択肢のテキスト続きの可能性
                    # ページ区切りや新しい問題ヘッダーなら終了
                    sl = lines[j].strip()
                    if PAGE_RE.match(sl) or QHEADER_RE.match(sl):
                        break
                    # 長すぎる行や次の行に選択肢マーカーがある場合は
                    # 前の選択肢の続きとして追加
                    if choice_lines:
                        last_m, last_t = choice_lines[-1]
                        # 次の行が選択肢マーカーなら継続
                        next_is_choice = (j + 1 < n and is_choice_line(lines[j + 1])[0])
                        if next_is_choice or len(sl) < 100:
                            choice_lines[-1] = (last_m, (last_t + " " + sl).strip())
                            j += 1
                            continue
                    j += 1
                    break

            if len(choice_lines) >= MIN_CHOICES:
                # 問題文: ブロック直前 STEM_LOOKBACK 行を遡る
                stem_start = max(0, i - STEM_LOOKBACK)
                stem_lines = []
                for k in range(stem_start, i):
                    sl = lines[k].strip()
                    if sl and not PAGE_RE.match(sl) and not DOC_RE.match(sl):
                        # 選択肢マーカーだらけの行は除外
                        if not is_choice_line(sl)[0]:
                            stem_lines.append(sl)

                rq = RawQuestion(
                    doc=doc_name,
                    page=current_page,
                    header=current_header,
                    stem_lines=stem_lines,
                    choice_lines=choice_lines,
                )
                questions.append(rq)
                current_header = ""
                i = j
                continue

        i += 1

    return questions

# =========================================================
# JSON 変換
# =========================================================
def rq_to_json(rq: RawQuestion, q_id: int) -> dict:
    stem = "\n".join(rq.stem_lines).strip()
    choices = []
    nums = ["①", "②", "③", "④", "⑤", "⑥"]
    for idx, (marker, text) in enumerate(rq.choice_lines):
        label = nums[idx] if idx < len(nums) else f"({idx+1})"
        choices.append(f"{label}　{text}" if text else label)

    return {
        "id": f"q{q_id:04d}",
        "chapter": rq.doc,
        "page": rq.page,
        "header": rq.header,
        "text": stem if stem else "(問題文を確認してください)",
        "choices": choices,
        "answer": None,      # 手動設定
        "explanation": "",   # 手動設定
        "needs_review": True,
    }

# =========================================================
# デモ問題 (アプリ動作確認用)
# =========================================================
DEMO_QUESTIONS = [
    {
        "id": "demo_001",
        "chapter": "★ デモ問題",
        "page": 0,
        "header": "",
        "text": "これはデモ問題です。正しい選択肢を選んでください。\n\n実際の問題は questions.json を編集して追加できます。",
        "choices": ["①　選択肢A（正解）", "②　選択肢B", "③　選択肢C", "④　選択肢D"],
        "answer": 0,
        "explanation": "選択肢①が正解です。これはデモ用の解説です。",
        "needs_review": False,
    },
    {
        "id": "demo_002",
        "chapter": "★ デモ問題",
        "page": 0,
        "header": "",
        "text": "2問目のデモ問題です。どれが正しいでしょうか？",
        "choices": ["①　誤りの選択肢", "②　これが正解", "③　誤りの選択肢", "④　誤りの選択肢"],
        "answer": 1,
        "explanation": "②が正解です。",
        "needs_review": False,
    },
]

# =========================================================
# メイン
# =========================================================
def main():
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    all_raw: list[RawQuestion] = []

    # 各ドキュメントファイルを処理 (集約ファイルは除外)
    EXCLUDE = {"all_documents_raw.txt", "all_documents_clean.txt"}
    txt_files = sorted(f for f in INPUT_DIR.glob("*.txt") if f.name not in EXCLUDE)
    if not txt_files:
        print(f"警告: {INPUT_DIR}/ に .txt ファイルが見つかりません")
    else:
        for f in txt_files:
            # "001_2026-04-02_11_59_54_PM" → "第01章"
            stem = f.stem
            m = re.match(r'^(\d+)_', stem)
            doc_name = f"第{int(m.group(1)):02d}章" if m else stem
            rqs = parse_file(f, doc_name)
            print(f"  {f.name}: {len(rqs)} 件検出")
            all_raw.extend(rqs)

    print(f"\n合計検出: {len(all_raw)} 件")

    # JSON変換
    parsed_qs = [rq_to_json(rq, i + 1) for i, rq in enumerate(all_raw)]

    # デモ問題 + OCR解析問題
    all_qs = DEMO_QUESTIONS + parsed_qs

    output = {
        "meta": {
            "title": "学習問題集",
            "version": "1.0",
            "source": str(INPUT_DIR),
            "total_questions": len(all_qs),
            "demo_count": len(DEMO_QUESTIONS),
            "ocr_parsed": len(parsed_qs),
            "needs_review_count": sum(1 for q in all_qs if q.get("needs_review")),
            "notes": [
                "needs_review: true の問題はOCR自動抽出のため手動確認が必要です",
                "answer は 0始まりインデックス (null = 未設定)",
                "chapter はソースファイル名 (変更可)",
                "header はOCR上の問題ラベル (参考用)",
            ],
        },
        "questions": all_qs,
    }

    OUTPUT_FILE.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n出力: {OUTPUT_FILE}")
    print(f"  総問題数 : {len(all_qs)}")
    print(f"  デモ     : {len(DEMO_QUESTIONS)}")
    print(f"  OCR解析  : {len(parsed_qs)}")
    print(f"  要確認   : {sum(1 for q in all_qs if q.get('needs_review'))}")
    print()
    if parsed_qs:
        print("サンプル (最初の2件):")
        for q in parsed_qs[:2]:
            print(f"  [{q['chapter']} p{q['page']}] {q['text'][:60]}...")
            for c in q['choices']:
                print(f"    {c[:50]}")
    else:
        print("⚠ OCR解析で問題が検出できませんでした。")
        print("  questions.json を直接編集して問題を追加してください。")

if __name__ == "__main__":
    main()
