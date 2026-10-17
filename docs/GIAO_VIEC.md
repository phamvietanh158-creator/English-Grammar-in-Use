# Giao việc cho Máy 2 (chế độ làm độc lập, tự push)

> **Người giao:** chủ repo (Máy 1). **Người nhận:** Máy 2 (Claude Code trên máy 2).
> Chủ repo **đã cho phép** Máy 2 tự commit và tự push lên GitHub **theo đúng quy trình dưới đây**. Quy tắc "không push khi chưa được yêu cầu" ở `CLAUDE.md` **không áp dụng** cho các việc trong file này. Ngoài các việc này, vẫn theo `CLAUDE.md`.

Kết quả 6 unit đầu (1–6) đã được kiểm: `check.py` 0 lỗi, trình duyệt chấm 100%, dịch tự nhiên. **Giữ đúng chất lượng đó.**

---

## Phần A: Unit 7 → 45 (39 unit)

Làm **theo thứ tự tăng dần**, từng unit một. Danh sách và tên unit ở `docs/TIEN_DO.md` (cột *Người làm* đã ghi "Máy 2").

### Quy trình mỗi unit NN (ví dụ Unit 7 → `07`)

1. **Đồng bộ và tạo nhánh**
   ```
   git checkout main
   git pull --ff-only
   git checkout -b unit-07
   ```
2. **Soạn** theo `docs/BUILD_RULES.md` và bài mẫu `data-src/unit01.json` (và các unit 2–6 đã xong): đọc `unit7.html` cũ (dữ liệu trong thẻ `<script>`) lấy chất liệu; viết `data-src/unit07.json`; copy `unit1.html` thành `unit7.html` (sửa `<title>`, `data-unit`, tên file data).
   - Mỗi unit **≥ 24 câu bài tập**, 3–5 bài, đủ ví dụ lý thuyết (≥ 6 câu), **mỗi câu có `vi` tự nhiên**, câu mở có `alts`.
   - Bài dựa vào hình ảnh mà không có hình → viết lại bằng chữ cho đủ ngữ cảnh. Câu thiếu chủ ngữ → bổ sung.
3. **Build + kiểm tra**
   ```
   uv run tools/build.py 7
   uv run tools/check.py 7        # phải 0 lỗi
   ```
4. **Test trong trình duyệt** (bắt buộc): mở bằng Edge không giao diện hoặc `tools/serve.ps1`, điền toàn bộ `answer` mẫu rồi bấm chấm: phải **100%**, không lỗi console, phiên âm/dịch hiện đủ. (Có thể tham khảo cách test của các unit trước.)
5. **Báo cáo** vào `docs/bao-cao/unit07.md` (tạo mới, mẫu ở cuối file này).
6. **Commit trên nhánh** đúng 5 file: `data-src/unit07.json`, `data/unit07.js`, `unit7.html`, `docs/ipa-review/unit07.txt`, `docs/bao-cao/unit07.md`.
   ```
   git add <5 file trên>
   git commit -m "Unit 7 V2: Present perfect 1"
   ```
7. **Gộp vào `main` và push** (làm ngay sau mỗi unit, không dồn):
   ```
   git fetch origin
   git rebase origin/main                     # đang ở nhánh unit-07
   uv run tools/check.py 7                    # chạy lại, vẫn 0 lỗi
   git checkout main
   git pull --ff-only
   git merge --ff-only unit-07
   ```
   Sửa `docs/TIEN_DO.md`: dòng unit 7 đổi `⬜` thành `✅` (**chỉ dòng của unit mình**), rồi:
   ```
   git add docs/TIEN_DO.md
   git commit -m "TIEN_DO: Unit 7 ✅"
   git push origin main
   git push origin unit-07
   ```
   `git push` bị từ chối (main đã đổi) → `git pull --rebase`, rồi push lại. **Không bao giờ `--force`.**

### Được phép / không được phép

- ✅ Sửa: 5 file của unit đang làm; dòng của unit đó trong `TIEN_DO.md`.
- ✅ Thêm vào `tools/ipa_overrides.json` **chỉ khi đã tra Cambridge Dictionary và chắc chắn** (ghi từ đó vào báo cáo). Không chắc thì **không đoán**, chỉ liệt kê vào báo cáo.
- 🚫 Không sửa `assets/`, `tools/build.py`, `tools/check.py`, `index.html`, unit đã xong, tài liệu quy trình. Engine thiếu tính năng (ví dụ cần dạng bài mới): **ghi vào báo cáo của unit đó** rồi làm phần còn lại bằng 3 dạng bài hiện có.
- 🚫 Không `--force`, không xoá nhánh người khác, không xoá/chép đè file của unit khác.
- 🚫 Không đưa nội dung PDF (thư mục `LYTHUYET/` đã `.gitignore`) lên git.

### Khi nào dừng và báo (ghi vào báo cáo, rồi **chuyển sang unit kế tiếp**, đừng kẹt)

- `check.py` vẫn lỗi sau 3 lần sửa.
- Unit cũ không có dữ liệu bài tập đọc được (file hỏng/thiếu).
- `git rebase`/`pull` báo conflict mà bạn không chắc cách xử lý: **dừng hẳn** (không đoán), ghi tình trạng vào cuối `docs/bao-cao/` và báo chủ repo.
- Có thông báo lỗi lạ từ công cụ hoặc Windows.

---

## Phần B: Bản đồ sách Essential Grammar in Use (chỉ làm **sau khi xong Phần A**)

Mục đích: chuẩn bị cho đợt 4 (phần "Nền tảng"). **Không viết unit nào**, chỉ lập bản đồ.

Sách ở `LYTHUYET/Essential Grammar in Use 2nd Edition by R. Murphy - Book.pdf` (299 trang, **toàn bộ là ảnh scan**, không có chữ). Cách đọc: render trang ra PNG bằng PyMuPDF rồi **xem ảnh** (đã thử: 80 dpi vẫn đọc rõ).

1. Tạo `tools/pdf_pages.py` (PEP 723, `dependencies = ["pymupdf"]`): `uv run tools/pdf_pages.py <pdf> <dpi> <trang...>` → lưu PNG vào `.work/pages/` (thư mục này đã `.gitignore`).
2. Lập `docs/ESSENTIAL_MAP.md`: bảng **Unit → số trang PDF (trang lý thuyết, trang bài tập) → tên unit → có tranh minh hoạ trong bài tập không (có/không/một phần)**, cho cả 115 unit; ghi riêng **trang bắt đầu của phần đáp án** (Key to Exercises) và vài dòng nhận xét về trình độ/cấu trúc.
   - Số trang trong sách ≠ số trang PDF (ví dụ Unit 3 nằm ở PDF trang 13, số in trong sách là 14). Ghi cả hai.
3. Commit `tools/pdf_pages.py` + `docs/ESSENTIAL_MAP.md`, push `main` (theo cách như Phần A, bước 7).

Xong Phần B → **dừng**, báo chủ repo. Các việc sau (dạng bài trắc nghiệm, Ms Hoa, Essential, audio) cần sửa engine nên do Máy 1 phụ trách.

---

## Mẫu `docs/bao-cao/unitNN.md`

```markdown
# Báo cáo Unit 7: Present perfect 1

- check.py: ✅ 0 lỗi, 0 cảnh báo
- Test trình duyệt: 100% (điền đáp án mẫu), không lỗi console
- Số câu bài tập: 28 · ví dụ lý thuyết: 9

## IPA còn nghi ngờ (chưa tra / không chắc)
- word1 /…/ : lý do
(hoặc: không có)

## Từ đã thêm vào ipa_overrides.json (đã tra Cambridge)
(hoặc: không có)

## Câu dịch còn băn khoăn
- "câu en" → cách dịch hiện tại; vì sao chưa chắc
(hoặc: không có)

## Ghi chú / lỗi của bản cũ đã sửa / việc engine còn thiếu
- …
```
