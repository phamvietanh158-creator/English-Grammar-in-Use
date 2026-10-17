# /// script
# requires-python = ">=3.10"
# dependencies = ["phonemizer", "espeakng-loader"]
# ///
"""Sinh data/unitNN.js từ data-src/unitNN.json.

Mỗi object có khoá "en" được thêm "ipa" (giọng Anh, ký hiệu kiểu Cambridge).
Object bài điền/viết (có "answer") tự nhận "en" = pre + answer + suf.
Chạy:  uv run tools/build.py            (tất cả unit)
       uv run tools/build.py 1 23       (chỉ unit 1 và 23)
Báo cáo từ cần soát lại: docs/ipa-review/unitNN.txt
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import espeakng_loader
from phonemizer import phonemize
from phonemizer.backend.espeak.wrapper import EspeakWrapper

EspeakWrapper.set_library(espeakng_loader.get_library_path())
EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = {k: v for k, v in json.loads((ROOT / "tools" / "ipa_overrides.json").read_text("utf-8")).items() if not k.startswith("_")}

# espeak → ký hiệu Cambridge Dictionary
CAMBRIDGE = str.maketrans({"ɛ": "e", "ɹ": "r", "ɡ": "g", "ɐ": "ə", "ɚ": "ə", "ᵻ": "ɪ", "ᵼ": "ɪ", "ɫ": "l"})
TOKEN = re.compile(r"[A-Za-z0-9']+")


CONS = re.compile(r"(tʃ|dʒ|[pbtdkgfvθðszʃʒhmnŋlrjw])")


def valid_onset(c: list[str]) -> bool:
    """Cụm phụ âm đầu âm tiết hợp lệ trong tiếng Anh (xấp xỉ)."""
    if len(c) == 1:
        return c[0] != "ŋ"
    if len(c) == 2:
        a, b = c
        return (b == "j" and a != "j") or (a == "s" and b in "ptkmnlwf") or (a in ("p", "b", "t", "d", "k", "g", "f", "θ", "ʃ") and b in "lrw")
    if len(c) == 3:
        return c[0] == "s" and c[1] in "ptk" and c[2] in ("l", "r", "w", "j")
    return False


def cambridge(word: str) -> str:
    """espeak → Cambridge: ký hiệu nguyên âm/phụ âm, /æ/, và đặt dấu trọng âm trước cả phụ âm đầu âm tiết."""
    w = word.translate(CAMBRIDGE)
    w = re.sub(r"a(?![ɪʊ])", "æ", w)  # espeak dùng 'a' cho /æ/; 'aɪ' 'aʊ' giữ nguyên
    out, i = "", 0
    while i < len(w):
        if w[i] in "ˈˌ":
            run = []  # các phụ âm ngay trước dấu, tính từ nguyên âm gần nhất
            while True:
                m = re.search(r"(tʃ|dʒ|[pbtdkgfvθðszʃʒhmnŋlrjw])$", out)
                if not m:
                    break
                run.insert(0, m.group(1))
                out = out[: m.start()]
            k = 0
            while k < len(run) and not valid_onset(run[k:]):
                k += 1
            out += "".join(run[:k]) + w[i] + "".join(run[k:])
        else:
            out += w[i]
        i += 1
    return out


def plain(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("**", "")).strip()


def phon(text: str) -> str:
    return phonemize(text, language="en-gb", backend="espeak", strip=True, with_stress=True)


def to_ipa(sentence: str, report: dict) -> str:
    text = plain(sentence)
    words = TOKEN.findall(text)
    if not words:
        return ""
    ipa_words = phon(" ".join(words)).split()
    if len(ipa_words) != len(words):  # số từ lệch (số, viết tắt…): không ghép được từng từ
        report["misaligned"].append(text)
        return " ".join(cambridge(x) for x in phon(text).split())
    out = []
    for w, i in zip(words, ipa_words):
        i = OVERRIDES.get(w.lower(), i)
        out.append(cambridge(i))
        report["words"].setdefault(w.lower(), out[-1])
    return " ".join(out)


def compose_en(d: dict) -> str | None:
    if isinstance(d.get("answer"), str) and "en" not in d:
        s = " ".join(x for x in (d.get("pre", ""), d["answer"], d.get("suf", "")) if x)
        return re.sub(r"\s+([.,!?])", r"\1", s)
    return None


def walk(node, report):
    if isinstance(node, dict):
        if (en := compose_en(node)) is not None:
            node["en"] = en
        if isinstance(node.get("en"), str) and "ipa" not in node:
            node["ipa"] = to_ipa(node["en"], report)
        for v in node.values():
            walk(v, report)
    elif isinstance(node, list):
        for v in node:
            walk(v, report)


def build(src: Path):
    data = json.loads(src.read_text("utf-8"))
    report = {"words": {}, "misaligned": []}
    walk(data, report)
    out = ROOT / "data" / (src.stem + ".js")
    out.parent.mkdir(exist_ok=True)
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # mã băm nội dung nguồn (bỏ khác biệt CRLF/LF) để check.py biết data/*.js có còn khớp không
    digest = hashlib.sha1(src.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:12]
    out.write_text(f"// src-sha1: {digest}\nwindow.EGIU_UNITS=window.EGIU_UNITS||{{}};window.EGIU_UNITS[{data['id']}]={body};\n", "utf-8")
    rep = ROOT / "docs" / "ipa-review"
    rep.mkdir(parents=True, exist_ok=True)
    lines = [f"# {src.stem}: IPA tự động (espeak en-GB → Cambridge). Soát nhanh các từ dưới đây.", ""]
    lines += [f"{w}\t/{i}/" for w, i in sorted(report["words"].items())]
    if report["misaligned"]:
        lines += ["", "# Câu không ghép được từng từ (có số/viết tắt) — soát cả câu:"] + report["misaligned"]
    (rep / (src.stem + ".txt")).write_text("\n".join(lines) + "\n", "utf-8")
    print(f"{src.name} -> {out.relative_to(ROOT)}  ({len(report['words'])} từ, {len(report['misaligned'])} câu lệch)")


if __name__ == "__main__":
    wanted = {f"unit{int(a):02d}" for a in sys.argv[1:]}
    for f in sorted((ROOT / "data-src").glob("unit*.json")):
        if not wanted or f.stem in wanted:
            build(f)
