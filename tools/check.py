# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Kiểm tra dữ liệu unit trước khi gửi PR (không cần mạng, không cần cài gì thêm).

    uv run tools/check.py            # tất cả data-src/unit*.json
    uv run tools/check.py 1 23       # chỉ unit 1 và 23

Lỗi (❌) làm lệnh thoát mã 1. Cảnh báo (⚠️) cần sửa hoặc ghi lý do vào PR.
Luật đầy đủ: docs/BUILD_RULES.md
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
KINDS = {"fill", "write", "match"}


def check(src: Path):
    errs, warns = [], []
    E = lambda m: errs.append(m)
    W = lambda m: warns.append(m)
    try:
        d = json.loads(src.read_text("utf-8"))
    except Exception as ex:  # noqa: BLE001
        return [f"JSON hỏng: {ex}"], []

    m = re.fullmatch(r"unit(\d+)", src.stem)
    if not m or d.get("id") != int(m.group(1)):
        E(f'"id" ({d.get("id")}) không khớp tên file {src.name}')
    if not d.get("title"):
        E('thiếu "title"')
    blocks = d.get("theory", {}).get("blocks", [])
    if not blocks:
        E("theory.blocks rỗng")

    def need_vi(s, where):
        if not s.get("vi"):
            E(f"{where}: thiếu bản dịch tiếng Việt (vi)")
        elif s["vi"].strip().lower() == s.get("en", "").strip().lower():
            W(f"{where}: vi giống en (chưa dịch?)")
        if s.get("en", "").count("**") % 2:
            E(f"{where}: dấu ** không cân")

    n_ex = 0
    for bi, b in enumerate(blocks):
        for si, s in enumerate(b.get("ex", [])):
            n_ex += 1
            if not s.get("en"):
                E(f"theory[{bi}].ex[{si}]: thiếu en")
            need_vi(s, f"theory[{bi}].ex[{si}]")
    if n_ex < 3:
        W(f"lý thuyết chỉ có {n_ex} câu ví dụ (nên ≥ 6)")

    exs = d.get("exercises", [])
    if not exs:
        E("không có bài tập")
    ids = [e.get("id") for e in exs]
    if len(ids) != len(set(ids)):
        E("id bài tập bị trùng")
    total = 0
    for ex in exs:
        eid = ex.get("id", "?")
        if ex.get("kind") not in KINDS:
            E(f"bài {eid}: kind phải thuộc {sorted(KINDS)}")
            continue
        if not ex.get("title") or not ex.get("instr"):
            E(f"bài {eid}: thiếu title/instr")
        if ex["kind"] == "match":
            keys = [l.get("k") for l in ex.get("left", [])]
            nums = [r.get("n") for r in ex.get("right", [])]
            total += len(keys)
            if set(ex.get("ans", {})) != set(keys):
                E(f"bài {eid}: ans phải có đủ mọi khoá của left")
            for k, n in ex.get("ans", {}).items():
                if n not in nums:
                    E(f"bài {eid}: ans[{k}]={n} không có trong right")
            for s in ex.get("left", []) + ex.get("right", []):
                need_vi(s, f"bài {eid} {s.get('k') or s.get('n')}")
        else:
            its = ex.get("items", [])
            total += len(its)
            for i, it in enumerate(its, 1):
                w = f"bài {eid} câu {i}"
                if not it.get("answer"):
                    E(f"{w}: thiếu answer")
                if ex["kind"] == "fill" and "pre" not in it and "suf" not in it:
                    E(f"{w}: bài điền cần pre và/hoặc suf")
                if ex["kind"] == "write" and not it.get("context"):
                    E(f"{w}: bài viết cần context")
                if re.match(r"^\s*\d+[.)]?\s", it.get("pre", "") + " "):
                    W(f"{w}: pre bắt đầu bằng số thứ tự (renderer tự đánh số)")
                full = " ".join(x for x in (it.get("pre", ""), it["answer"], it.get("suf", "")) if x)
                if ex["kind"] == "fill" and not it.get("hint"):
                    W(f"{w}: thiếu hint")
                if not it.get("exp"):
                    W(f"{w}: thiếu exp (giải thích)")
                need_vi({"en": full, "vi": it.get("vi", "")}, w)
    if total and total < 20:
        W(f"chỉ có {total} câu bài tập (nên ≥ 24)")

    js = ROOT / "data" / (src.stem + ".js")
    if not js.exists():
        E(f"chưa có {js.relative_to(ROOT)}: chạy  uv run tools/build.py {d.get('id')}")
    else:
        # so mã băm nội dung (không dùng thời gian file: sau git clone thời gian là ngẫu nhiên)
        want = hashlib.sha1(src.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:12]
        m2 = re.match(r"// src-sha1: (\w+)", js.read_text("utf-8"))
        if not m2 or m2.group(1) != want:
            E(f"{js.name} không khớp {src.name} (sửa JSON mà chưa build?): chạy  uv run tools/build.py {d.get('id')}")
    shell = ROOT / f"unit{d.get('id')}.html"
    if not shell.exists() or "assets/egiu-unit.js" not in shell.read_text("utf-8"):
        E(f"{shell.name} chưa phải bản vỏ V2 (copy unit1.html, đổi data-unit và <title>)")
    return errs, warns


if __name__ == "__main__":
    wanted = {f"unit{int(a):02d}" for a in sys.argv[1:]}
    bad = 0
    for f in sorted((ROOT / "data-src").glob("unit*.json")):
        if wanted and f.stem not in wanted:
            continue
        errs, warns = check(f)
        print(f"{'❌' if errs else '✅'} {f.name}: {len(errs)} lỗi, {len(warns)} cảnh báo")
        for e in errs:
            print("   ❌", e)
        for w in warns:
            print("   ⚠️ ", w)
        bad += bool(errs)
    sys.exit(1 if bad else 0)
