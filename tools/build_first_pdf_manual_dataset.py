#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


SOURCE_PDF = "2026-04-02 11_59_54 PM からスキャン.pdf"
TRANSCRIPT_DIR = Path("tmp_first_pdf_transcripts")
OUTPUT_PATH = Path("app/questions-first-pdf.json")


CHAPTER_BY_PAGE = {
    1: "1.8 利用機器",
    2: "1.9 管理・測定",
    4: "2.1-2.2 単位・検出器",
    5: "2.2 エックス線（放射線）検出器",
    7: "2.4 個人被ばく線量計",
    8: "2.4 個人被ばく線量計",
    15: "3.7 人体組織への放射線影響",
    16: "3.7 人体組織への放射線影響",
    22: "4.2 関係法令",
    24: "4.2 関係法令",
    25: "4.2 関係法令",
}

SKIP_KEYS = {
    (4, "6"),
    (2, "38"),
}

PAGE_OVERRIDES = {
    38: {"source_pdf_page": 15, "book_page": 38},
    40: {"source_pdf_page": 16, "book_page": 40},
}

CORRECTIONS = {
    (2, "35"): {
        "text": "前問において、他の条件は一定にして鋼板の厚さを40mmにした時の、点P30および点P150の空気カーマ率を、各々、K30及びK150とすると、正しい関係はどれか。",
        "choices": [
            "(1) K30 > K'30, K150 > K'150",
            "(2) K30 > K'30, K150 < K'150",
            "(3) K30 = K'30, K150 = K'150",
            "(4) K30 < K'30, K150 > K'150",
            "(5) K30 < K'30, K150 < K'150",
        ],
    },
    (2, "36"): {
        "text": (
            "工業用エックス線装置を用い、鋼板に垂直にエックス線を照射した。"
            "後方散乱線の強度の変化に関する次の記述のうち、正しいものの組合せは"
            "(1)〜(5)のうちどれか。\n"
            "A. 鋼板の厚さを厚くすると増加するが、ある程度以上では飽和する。\n"
            "B. 管電圧を上げても飽和する厚さはあまり変化しない。\n"
            "C. 散乱型厚さ計では、この後方散乱線の厚さに対する変化と同じ原理を利用している。\n"
            "D. 鋼板を同じ厚さのアルミニウムに変えると減少する。"
        ),
        "choices": ["(1) A, B", "(2) A, C", "(3) B, C", "(4) B, D", "(5) C, D"],
    },
    (2, "37"): {
        "text": (
            "安全管理に関わる区域について関連のある線量率の値で適切なものの組合せは"
            "(1)〜(5)のうちどれか。\n"
            "A. 管理区域 ------- 3月間1.3mSv\n"
            "B. 放射線装置室 ------- 1週間1mSv\n"
            "C. 立入禁止区域 ------- 1時間0.5mSv\n"
            "D. 事故区域 ------- 年間20mSv"
        ),
        "choices": ["(1) A, B", "(2) A, C", "(3) B, C", "(4) B, D", "(5) C, D"],
    },
    (15, "30"): {
        "text": (
            "ヒトの放射線感受性に関する次の記述のうち、正しいものの組み合わせはどれか。\n"
            "A. 小児の骨の放射線感受性は成人と同じである。\n"
            "B. 小腸のクリプト（腺窩）細胞は、絨毛先端部の細胞より放射線感受性が高い。\n"
            "C. 皮膚の基底細胞層は、角質層より放射線感受性が高い。\n"
            "D. 眼の角膜は、水晶体より放射線感受性が高い。"
        ),
        "choices": ["(1) A, B", "(2) A, C", "(3) B, C", "(4) B, D", "(5) C, D"],
    },
    (15, "31"): {
        "text": (
            "ヒトの放射線被ばくに関する次の記述のうち、正しいものの組み合わせはどれか。\n"
            "A. 放射線による骨髄障害の治療には骨髄移植が有効である。\n"
            "B. 全身被ばく線量が10Gyを超えると骨髄死が生じ始める。\n"
            "C. 放射線宿酔は1〜2Gyの全身被ばくで出現する。\n"
            "D. 骨髄死が生じるのは被ばく後5〜7日である。"
        ),
        "choices": ["(1) A, B", "(2) A, C", "(3) B, C", "(4) B, D", "(5) C, D"],
    },
    (15, "32"): {
        "text": (
            "哺乳動物における放射線による腸死に関する次の記述のうち、正しいものの組み合わせはどれか。\n"
            "A. 半致死線量程度の被ばくの場合にみられる。\n"
            "B. 線量率効果がみられる。\n"
            "C. 被ばく後、死亡するまでの期間は4週間である。\n"
            "D. 骨髄死が生じる線量より高い被ばく線量でみられる。"
        ),
        "choices": ["(1) A, B", "(2) A, C", "(3) B, C", "(4) B, D", "(5) C, D"],
    },
    (16, "38"): {
        "text": (
            "放射線の水晶体への影響に関する次の記述のうち、正しいものの組み合わせはどれか。\n"
            "A. 放射線による白内障の誘発にはしきい線量が存在する。\n"
            "B. 白内障の発生頻度は線量率には関係しない。\n"
            "C. 白内障の重篤度は被ばく線量とともに増加する。\n"
            "D. 水晶体前面の上皮は定常系組織である。"
        ),
        "choices": ["(1) A, B", "(2) A, C", "(3) B, C", "(4) B, D", "(5) C, D"],
    },
}

ANSWER_SOURCE_PDFS = {
    "pdf4": {
        "file": "2026-04-03 12_13_14 AM からスキャン.pdf",
        "cache_dir": "easyocr_answers_pdf4",
    },
    "pdf5": {
        "file": "2026-04-03 12_15_44 AM からスキャン.pdf",
        "cache_dir": "easyocr_answers_pdf5",
    },
}

ANSWER_OVERRIDES = {
    (1, "30"): {
        "answer_choice": 2,
        "answer_source": "pdf4",
        "answer_page": 10,
        "explanation": "エックス線厚さ計は、後方散乱線が減少ではなく増加する性質を利用する。",
    },
    (1, "31"): {
        "answer_choice": 3,
        "answer_source": "pdf4",
        "answer_page": 11,
        "explanation": "エックス線応力測定装置は回折を利用する。ほかの組合せは原理が対応していない。",
    },
    (2, "36"): {
        "answer_choice": 2,
        "answer_source": "pdf4",
        "answer_page": 12,
        "explanation": "AとCが正しい。後方散乱線は厚さとともに増えて飽和し、散乱型厚さ計はその厚さ依存を利用する。",
    },
    (2, "37"): {
        "answer_choice": 1,
        "answer_source": "pdf4",
        "answer_page": 12,
        "explanation": "AとBが正しい。管理区域は3か月1.3mSv、放射線装置室の常時立入場所は1週間1mSvが基準になる。",
    },
    (4, "5"): {
        "answer_choice": 5,
        "answer_source": "pdf4",
        "answer_page": 15,
        "explanation": "誤りは(5)。実効線量はエックス線やガンマ線に限らず、放射線の種類や臓器影響を考慮した量である。",
    },
    (5, "10"): {
        "answer_choice": 3,
        "answer_source": "pdf4",
        "answer_page": 18,
        "explanation": "正しいのは(3)。GM計数管では消滅ガスとしてアルコールやハロゲンを加え、偽パルスを防ぐ。",
    },
    (5, "11"): {
        "answer_choice": 2,
        "answer_source": "pdf4",
        "answer_page": 18,
        "explanation": "光の測定が必要なのはA・C・Eで、選択肢(2)になる。",
    },
    (5, "12"): {
        "answer_choice": 3,
        "answer_source": "pdf4",
        "answer_page": 18,
        "explanation": "エネルギー分析に使えるのはA・D・Fで、選択肢(3)になる。",
    },
    (5, "13"): {
        "answer_choice": 3,
        "answer_source": "pdf4",
        "answer_page": 19,
        "explanation": "正しいのは(3)。シンチレータの光は光電子増倍管で電子信号に変換・増倍される。",
    },
    (7, "23"): {
        "answer_choice": 5,
        "answer_source": "pdf4",
        "answer_page": 23,
        "explanation": "正しいのは(5)。フィルムバッジは湿度やかぶりの影響を受けやすく、方向依存性も小さくない。",
    },
    (7, "24"): {
        "answer_choice": 1,
        "answer_source": "pdf4",
        "answer_page": 23,
        "explanation": "正しいのは(1)。PD型は装着者が直読できるが、PC型は別途チャージャーやリーダーを用いる。",
    },
    (8, "25"): {
        "answer_choice": 5,
        "answer_source": "pdf4",
        "answer_page": 23,
        "explanation": "正しいのは(5)。A=フィルムバッジ、B=蛍光ガラス線量計、C=直読式ポケット線量計の組合せになる。",
    },
    (8, "26"): {
        "answer_choice": 3,
        "answer_source": "pdf4",
        "answer_page": 24,
        "explanation": "誤りは(3)。OSL線量計は光で読み出すが、その説明をアニーリングとするのは不適切。",
    },
    (15, "29"): {
        "answer_choice": 4,
        "answer_source": "pdf5",
        "answer_page": 8,
        "explanation": "放射線感受性の高い順として正しいのは(4)である。",
    },
    (15, "30"): {
        "answer_choice": 3,
        "answer_source": "pdf5",
        "answer_page": 8,
        "explanation": "正しい組合せはB・Cで(3)。クリプト細胞と皮膚基底細胞は感受性が高い。",
    },
    (15, "31"): {
        "answer_choice": 2,
        "answer_source": "pdf5",
        "answer_page": 9,
        "explanation": "正しい組合せはA・Cで(2)。骨髄障害には骨髄移植が有効で、放射線宿酔は1Gy前後でも起こりうる。",
    },
    (15, "32"): {
        "answer_choice": 4,
        "answer_source": "pdf5",
        "answer_page": 9,
        "explanation": "正しい組合せはB・Dで(4)。腸死は骨髄死より高線量で起こり、線量率効果もみられる。",
    },
    (16, "35"): {
        "answer_choice": 4,
        "answer_source": "pdf5",
        "answer_page": 10,
        "explanation": "誤りは(4)。血小板の減少は出血傾向、赤血球の減少は貧血の原因になる。",
    },
    (16, "36"): {
        "answer_choice": 5,
        "answer_source": "pdf5",
        "answer_page": 10,
        "explanation": "少ない線量で現れる順に並べると、正しい並びは(5)になる。",
    },
    (16, "37"): {
        "answer_choice": 2,
        "answer_source": "pdf5",
        "answer_page": 10,
        "explanation": "皮膚障害のしきい線量と発症時期を照合すると、正しいのは(2)だけである。",
    },
    (16, "38"): {
        "answer_choice": 2,
        "answer_source": "pdf5",
        "answer_page": 11,
        "explanation": "正しい組合せはA・Cで(2)。白内障にはしきい線量があり、重篤度は線量とともに増す。",
    },
    (22, "1"): {
        "answer_choice": 2,
        "answer_source": "pdf5",
        "answer_page": 20,
        "explanation": "正しいのは(2)。この条件では総括安全衛生管理者の選任が必要になる。",
    },
    (22, "2"): {
        "answer_choice": 5,
        "answer_source": "pdf5",
        "answer_page": 20,
        "explanation": "正しいのは(5)。労働者数ごとの安全衛生管理体制の条件を当てはめると(5)だけが合う。",
    },
    (22, "3"): {
        "answer_choice": 3,
        "answer_source": "pdf5",
        "answer_page": 21,
        "explanation": "正しいのは(3)。エックス線装置の設置計画は工事開始30日前までに所轄労働基準監督署長へ届け出る。",
    },
    (24, "12"): {
        "answer_choice": 1,
        "answer_source": "pdf5",
        "answer_page": 26,
        "explanation": "構造規格に定められていないのは(1)の設置年月である。",
    },
    (24, "13"): {
        "answer_choice": 1,
        "answer_source": "pdf5",
        "answer_page": 26,
        "explanation": "該当するのは(1)。放射線装置室で使い、かつ管電圧が150kVを超える場合に自動警報装置が必要になる。",
    },
    (24, "14"): {
        "answer_choice": 3,
        "answer_source": "pdf5",
        "answer_page": 26,
        "explanation": "正しい組合せは(3)。事故時は退避や医師の診察が必要で、誤った運用が含まれる選択肢は除かれる。",
    },
    (25, "18"): {
        "answer_choice": 4,
        "answer_source": "pdf5",
        "answer_page": 28,
        "explanation": "正しい組合せは(4)。BとDが正しく、AとCは測定主体と頻度の規定が誤りである。",
    },
    (25, "19"): {
        "answer_choice": 3,
        "answer_source": "pdf5",
        "answer_page": 29,
        "explanation": "正しいのは(3)。健康診断項目には省略できる場合がある。",
    },
}


def normalize_example_no(value: str | int) -> str:
    return str(value).strip()


def load_transcripts() -> list[dict]:
    items: list[dict] = []
    for path in sorted(TRANSCRIPT_DIR.glob("*.json")):
        if path.name == "pages_28_29_30.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        items.extend(data)
    return items


def remap_page(raw_page: int) -> tuple[int, int | None]:
    override = PAGE_OVERRIDES.get(raw_page)
    if override:
        return override["source_pdf_page"], override["book_page"]
    return raw_page, None


def build_questions() -> list[dict]:
    raw_items = load_transcripts()
    records: list[dict] = []

    for item in raw_items:
        raw_page = int(item["pdf_page"])
        source_pdf_page, book_page = remap_page(raw_page)
        example_no = normalize_example_no(item["example_no"])
        key = (source_pdf_page, example_no)
        if key in SKIP_KEYS:
            continue

        text = str(item.get("text", "")).strip()
        choices = [
            str(choice).strip()
            for choice in item.get("choices", [])
            if str(choice).strip()
        ]

        if key in CORRECTIONS:
            text = CORRECTIONS[key]["text"]
            choices = CORRECTIONS[key]["choices"]

        if not choices:
            continue

        records.append(
            {
                "source_pdf_page": source_pdf_page,
                "book_page": book_page,
                "example_no": example_no,
                "text": text,
                "choices": choices,
            }
        )

    records.sort(
        key=lambda record: (
            record["source_pdf_page"],
            int("".join(ch for ch in record["example_no"] if ch.isdigit()) or "0"),
        )
    )

    questions: list[dict] = []
    for index, record in enumerate(records, start=1):
        question = {
            "id": f"fp{index:04d}",
            "chapter": CHAPTER_BY_PAGE.get(
                record["source_pdf_page"], f"先頭PDF p.{record['source_pdf_page']}"
            ),
            "page": record["source_pdf_page"],
            "header": f"例題{record['example_no']}",
            "text": record["text"],
            "choices": record["choices"],
            "answer": None,
            "explanation": "",
            "needs_review": True,
            "source_pdf": SOURCE_PDF,
            "source_page": record["source_pdf_page"],
            "source_image": (
                f"../ocr_output/easyocr_first_pdf/pages/{record['source_pdf_page']:04d}.png"
            ),
        }
        answer_override = ANSWER_OVERRIDES.get(
            (record["source_pdf_page"], record["example_no"])
        )
        if answer_override:
            source_meta = ANSWER_SOURCE_PDFS[answer_override["answer_source"]]
            question["answer"] = answer_override["answer_choice"] - 1
            question["explanation"] = answer_override["explanation"]
            question["needs_review"] = False
            question["answer_source_pdf"] = source_meta["file"]
            question["answer_source_page"] = answer_override["answer_page"]
            question["answer_source_image"] = (
                f"../ocr_output/{source_meta['cache_dir']}/pages/"
                f"{answer_override['answer_page']:04d}.png"
            )
        if record["book_page"] is not None:
            question["book_page"] = record["book_page"]
        questions.append(question)

    return questions


def main() -> None:
    questions = build_questions()
    answered_count = sum(1 for question in questions if question["answer"] is not None)
    needs_review_count = sum(1 for question in questions if question["needs_review"])
    payload = {
        "meta": {
            "title": "エックス線作業主任者 学習問題集（先頭PDF実OCR試作）",
            "version": "4.0",
            "source": "サブエージェント目視転記 + easyocrページ画像 + 解答編OCR照合",
            "sourcePdf": SOURCE_PDF,
            "updatedAt": "2026/04/10",
            "total_questions": len(questions),
            "answer_key_count": answered_count,
            "needs_review_count": needs_review_count,
            "notes": [
                "先頭PDFの実画像から目視転記した試作データです。",
                "解答編PDFを照合して、本文一致で確認できた問題には正解と要約解説を付与しています。",
                "例題35（1.9 管理・測定）は解答編との対応が不一致のため未設定のまま残しています。",
                "問題画面の『原本ページ』リンクから元画像を開けます。",
            ],
        },
        "questions": questions,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUTPUT_PATH}")
    print(f"questions={len(questions)}")


if __name__ == "__main__":
    main()
