# Hướng dẫn thành viên: làm unit EGIU V2

Mỗi người nhận unit, làm trên **nhánh riêng**, tự kiểm tra bằng `check.py` và Edge, rồi gửi **Pull Request (PR)**. Trưởng nhóm duyệt và merge.

| Tài liệu | Dùng để |
|----------|---------|
| [docs/BUILD_RULES.md](docs/BUILD_RULES.md) | **Luật** soạn unit: định dạng JSON, 3 dạng bài, IPA, dịch |
| [docs/TIEN_DO.md](docs/TIEN_DO.md) | **Nhận unit** và xem tiến độ |
| [docs/KE_HOACH.md](docs/KE_HOACH.md) | Kế hoạch tổng, kiến trúc, lộ trình |
| [data-src/unit01.json](data-src/unit01.json) + [unit1.html](unit1.html) | **Bài mẫu** để copy |

---

## Quy trình 1 unit (6 bước)

```
① Nhận unit → ② Tạo nhánh → ③ Soạn JSON → ④ build + check → ⑤ Gửi PR → ⑥ Duyệt & merge
 TIEN_DO.md    unit-07       copy unit01     0 lỗi + Edge     GitHub      trưởng nhóm
```

### ⓪ Chuẩn bị (làm 1 lần)

1. Có tài khoản GitHub, báo trưởng nhóm để được mời (Settings → Collaborators), mở email bấm **Accept invitation**.
2. Cài **Git** và **uv** (uv: `winget install astral-sh.uv`). Không cần cài Python hay thư viện, `uv` tự lo.
3. Tải repo:
   ```bash
   git clone https://github.com/phamvietanh158-creator/English-Grammar-in-Use.git
   cd English-Grammar-in-Use
   ```
4. Dùng **Microsoft Edge** để nghe thử (có giọng Natural UK/US tốt nhất).

### ① Nhận unit

Mở [docs/TIEN_DO.md](docs/TIEN_DO.md) trên GitHub → ✏️ → ở dòng unit muốn làm: điền **tên bạn**, đổi ⬜ thành 🟡 → **Commit changes** (thẳng vào `main`). Chỉ nhận unit ⬜ thuộc **đợt đang mở**; tối đa 2 unit cùng lúc.

### ② Tạo nhánh

```bash
git checkout main
git pull
git checkout -b unit-07
```
Tên nhánh: `unit-` + số unit 2 chữ số.

### ③ Soạn dữ liệu

1. **Lấy chất liệu từ bản cũ:** nội dung hiện nằm trong `unit7.html` (mảng dữ liệu trong thẻ `<script>`). Giữ nguyên ý bài, sửa các lỗi bài cũ (xem BUILD_RULES mục 3).
2. **Copy bài mẫu:**
   ```bash
   cp data-src/unit01.json data-src/unit07.json
   cp unit1.html unit7.html        # rồi sửa <title>, data-unit="7", data/unit07.js
   ```
3. Viết lại **toàn bộ** `unit07.json` theo [BUILD_RULES.md](docs/BUILD_RULES.md): lý thuyết có ví dụ, 3–5 bài tập, **mỗi câu có bản dịch `vi`**. Chỉ sửa file của unit mình.
4. Dùng AI soạn nháp được (Claude/ChatGPT), nhưng **bản dịch, đáp án và IPA phải tự soát**.

> 🚫 **Không sửa** `assets/`, `tools/`, `index.html` hay unit người khác trong PR unit. Engine thiếu tính năng thì mở **Issue** trên GitHub và mô tả.

### ④ Build và tự kiểm tra

```bash
uv run tools/build.py 7      # sinh data/unit07.js + docs/ipa-review/unit07.txt
uv run tools/check.py 7      # phải 0 lỗi ❌
```
1. Mở `docs/ipa-review/unit07.txt`: soát các từ; từ sai thì ghi vào `tools/ipa_overrides.json` (đã tra Cambridge) rồi `build.py` lại.
2. Nhấp đúp `tools/serve.bat`, mở bằng Edge `http://localhost:8765/unit7.html`:
   - bật **Phiên âm** và **Dịch nghĩa**, bấm 🔊 🐢, đổi 🇬🇧/🇺🇸;
   - điền đáp án đúng và sai, bấm **Chấm điểm**;
   - F12 → Console không lỗi đỏ; F12 → biểu tượng điện thoại → 375px không tràn ngang.

### ⑤ Gửi PR

```bash
git add data-src/unit07.json data/unit07.js unit7.html docs/ipa-review/unit07.txt
git commit -m "Unit 7 V2: Present perfect 1"
git push -u origin unit-07
```
Trên GitHub bấm **Compare & pull request**; điền mẫu PR (checklist). Đổi trạng thái unit trong `TIEN_DO.md` thành 🔵.

### ⑥ Duyệt & merge (trưởng nhóm)

1. `git fetch && git checkout unit-07`, chạy `check.py 7` và mở `unit7.html` xem thử.
2. Rà nhanh 3 thứ máy không bắt được: **bản dịch** vài câu bất kỳ, **IPA** 3–4 từ tra Cambridge, **đáp án** có câu mở nào còn thiếu `alts`.
3. Góp ý bằng comment trong PR; người làm sửa và push tiếp lên cùng nhánh.
4. Đạt thì **Squash and merge**, xoá nhánh, cập nhật `TIEN_DO.md` thành ✅, bỏ `avail:false` (nếu có) ở `index.html`.

---

## Hỏi nhanh

| Tình huống | Cách xử lý |
|------------|-----------|
| `git pull` báo conflict ở `TIEN_DO.md` | Hai người sửa cùng lúc. Giữ cả hai dòng thay đổi rồi commit lại |
| Nhánh cũ, `main` đã có thay đổi mới | `git checkout unit-07` → `git merge main` |
| `data/unit07.js` conflict | Không sửa tay: chạy lại `uv run tools/build.py 7` rồi commit |
| Không nghe được giọng UK | Dùng Edge; hoặc Windows Settings → Time & language → Speech → thêm English (United Kingdom) |
| `check.py` báo "cũ hơn" | Chạy `build.py N` sau mỗi lần sửa `unitNN.json` |
| File xuống dòng bị đổi (CRLF/LF) | `.gitattributes` đã ép LF; nếu vẫn lạ: `git add --renormalize .` |
| Muốn thêm từ vào `ipa_overrides.json` | Được, nhưng phải đã tra Cambridge; dòng này dùng chung, nhớ `git pull` trước để khỏi conflict |
