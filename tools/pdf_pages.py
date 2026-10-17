# /// script
# requires-python = ">=3.9"
# dependencies = ["pymupdf"]
# ///
"""Render trang PDF ra PNG để xem (sách scan, không có lớp chữ).

Cách dùng:
    uv run tools/pdf_pages.py <pdf> <dpi> <trang...>
    uv run tools/pdf_pages.py sach.pdf 80 13 14 20-25
    uv run tools/pdf_pages.py sach.pdf 60 --sheet 3x2 13-18

- Số trang tính từ 1 (trang PDF, không phải số in trong sách). Có thể ghi khoảng "20-25".
- Mặc định mỗi trang một file: .work/pages/p013.png
- --sheet CxR: ghép nhiều trang vào một ảnh lưới (C cột x R hàng) để xem nhanh:
  .work/pages/sheet_p013-p018.png
"""
import sys
from pathlib import Path

import pymupdf as fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8")


def parse_pages(args, total):
    pages = []
    for a in args:
        if "-" in a:
            lo, hi = a.split("-", 1)
            pages.extend(range(int(lo), int(hi) + 1))
        else:
            pages.append(int(a))
    bad = [p for p in pages if p < 1 or p > total]
    if bad:
        sys.exit(f"Trang ngoài phạm vi 1-{total}: {bad}")
    return pages


def render(doc, page_no, dpi):
    zoom = dpi / 72
    return doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)


def main():
    argv = sys.argv[1:]
    sheet = None
    if "--sheet" in argv:
        i = argv.index("--sheet")
        cols, rows = (int(x) for x in argv[i + 1].lower().split("x"))
        sheet = (cols, rows)
        del argv[i : i + 2]
    if len(argv) < 3:
        sys.exit(__doc__)
    pdf, dpi, rest = argv[0], int(argv[1]), argv[2:]
    doc = fitz.open(pdf)
    pages = parse_pages(rest, doc.page_count)
    out = Path(".work/pages")
    out.mkdir(parents=True, exist_ok=True)

    if sheet is None:
        for p in pages:
            f = out / f"p{p:03d}.png"
            render(doc, p, dpi).save(f)
            print(f)
        return

    cols, rows = sheet
    per = cols * rows
    for start in range(0, len(pages), per):
        chunk = pages[start : start + per]
        pix = [render(doc, p, dpi) for p in chunk]
        w, h = max(x.width for x in pix), max(x.height for x in pix)
        canvas = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w * cols, h * rows), False)
        canvas.set_rect(canvas.irect, (255, 255, 255))
        for k, px in enumerate(pix):
            px.set_origin((k % cols) * w, (k // cols) * h)
            canvas.copy(px, px.irect)
        f = out / f"sheet_p{chunk[0]:03d}-p{chunk[-1]:03d}.png"
        canvas.save(f)
        print(f)


if __name__ == "__main__":
    main()
