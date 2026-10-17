# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Kiểm thử trình duyệt (Edge không giao diện): mở từng trang bài học, điền ĐÁP ÁN MẪU, bấm Chấm điểm.

    uv run tools/test_units.py              # mọi unit*.html (+ ess*.html, topic*.html nếu có)
    uv run tools/test_units.py 1 23 42      # chỉ unit 1, 23, 42
    uv run tools/test_units.py ess1 topic3  # trang theo tên file (không .html)

Đạt = điểm 100%, không lỗi JS, tiêu đề đúng. Thoát mã 1 nếu có trang không đạt.
Dùng làm "kiểm thử hồi quy" mỗi khi sửa engine (assets/): sau khi sửa phải chạy lại TOÀN BỘ và vẫn đạt hết.

Dạng bài mới (ví dụ "choose"): thêm cách điền đáp án vào PROBE bên dưới (phần FILL) để bài test biết cách làm.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
EDGES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

# Chèn vào cuối trang. Điền đáp án theo từng dạng bài, bấm #btnCheck, ghi kết quả vào <pre id="RES">.
PROBE = r"""<script>
(function () {
  var o = [];
  try {
    var n = document.body.dataset.unit;
    var key = /^\d+$/.test(n) ? +n : n;
    var U = EGIU_UNITS[key];
    U.exercises.forEach(function (ex, ei) {
      // ── FILL: cách điền đáp án mẫu cho từng dạng bài ──
      if (ex.kind === 'match') {
        ex.left.forEach(function (l) { document.querySelector('select[data-key="' + ei + '_' + l.k + '"]').value = ex.ans[l.k]; });
      } else if (ex.kind === 'fill' || ex.kind === 'write') {
        ex.items.forEach(function (it, ii) { document.querySelector('input[data-key="' + ei + '_' + ii + '"]').value = it.answer; });
      } else {
        o.push('KIND_CHUA_HO_TRO:' + ex.kind);
      }
    });
    document.getElementById('btnCheck').click();
    var ng = [];
    document.querySelectorAll('.item.checked .fb.ng').forEach(function (e) { ng.push(e.parentNode.dataset.key); });
    o.push('score=' + document.getElementById('scPct').textContent);
    o.push('ng=' + ng.join(','));
    o.push('nav=' + document.querySelector('.nav-title').textContent.replace(/\s+/g, '_'));
    o.push('ipa=' + document.querySelectorAll('.s-ipa').length);
    o.push('vi=' + document.querySelectorAll('.s-vi').length);
  } catch (e) { o.push('ERR=' + String(e.message).replace(/\s+/g, '_')); }
  document.body.insertAdjacentHTML('beforeend', '<pre id="RES">' + o.join(' ') + '</pre>');
})();
</script>"""


def find_edge() -> str:
    for p in EDGES:
        if Path(p).exists():
            return p
    for name in ("msedge", "chrome", "chromium"):
        if shutil.which(name):
            return shutil.which(name)
    sys.exit("Không tìm thấy Edge/Chrome.")


def pages(args):
    if not args:
        out = []
        for pat in ("unit*.html", "ess*.html", "topic*.html"):
            out += sorted(ROOT.glob(pat), key=lambda p: (len(p.stem), p.stem))
        return out
    out = []
    for a in args:
        name = f"unit{a}" if a.isdigit() else a
        p = ROOT / f"{name}.html"
        if not p.exists():
            sys.exit(f"Không có {p.name}")
        out.append(p)
    return out


def run(edge: str, page: Path):
    html = page.read_text("utf-8")
    if "data-unit=" not in html:
        return page.name, "BỎ QUA (không phải trang bài học)", True
    tmp = ROOT / f"_t_{page.name}"
    prof = tempfile.mkdtemp(prefix="egiu_edge_")
    try:
        i = html.rindex("</body>")
        tmp.write_text(html[:i] + PROBE + html[i:], "utf-8")
        r = subprocess.run(
            [edge, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--virtual-time-budget=5000",
             "--dump-dom", tmp.as_uri()],
            capture_output=True, timeout=120)
        dom = r.stdout.decode("utf-8", "replace")
        # dump-dom có thể chứa cả đoạn mã PROBE (chuỗi '<pre id="RES">' trong script): lấy kết quả CUỐI
        found = re.findall(r'<pre id="RES">([^<]*)</pre>', dom)
        if not found:
            return page.name, "KHÔNG CÓ KẾT QUẢ (trang không chạy được?)", False
        res = found[-1]
        ok = "score=100%" in res and "ERR=" not in res and "KIND_CHUA_HO_TRO" not in res and re.search(r"ng=(\s|$)", res) is not None
        return page.name, res, ok
    except subprocess.TimeoutExpired:
        return page.name, "QUÁ GIỜ", False
    finally:
        tmp.unlink(missing_ok=True)
        shutil.rmtree(prof, ignore_errors=True)


if __name__ == "__main__":
    edge = find_edge()
    todo = pages(sys.argv[1:])
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(lambda p: run(edge, p), todo))
    bad = 0
    for name, res, ok in results:
        print(f"{'✅' if ok else '❌'} {name}: {res if not ok else res.split(' nav=')[0]}")
        bad += not ok
    print(f"\nTổng: {len(results) - bad}/{len(results)} đạt")
    sys.exit(1 if bad else 0)
