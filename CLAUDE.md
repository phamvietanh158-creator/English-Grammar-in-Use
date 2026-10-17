# EGIU: English Grammar in Use (web app luyện ngữ pháp)

Trao đổi với người dùng bằng **tiếng Việt**.

## Kiến trúc V2
- `assets/egiu-core.*` và `assets/egiu-unit.js`: engine dùng chung. **Không sửa** khi đang làm một unit; thiếu tính năng thì báo người dùng để mở Issue.
- Mỗi unit: `data-src/unitNN.json` (nguồn, người viết) → `uv run tools/build.py N` sinh `data/unitNN.js` (thêm IPA). Trang `unitN.html` chỉ là vỏ mỏng, copy từ `unit1.html`.
- Luật soạn: `docs/BUILD_RULES.md` (đọc đầy đủ trước khi soạn). Tiến độ/đợt: `docs/TIEN_DO.md`. Kế hoạch: `docs/KE_HOACH.md`. Quy trình nhóm: `CONTRIBUTING.md`.
- Sách gốc (PDF, scan) ở `LYTHUYET/`, **không đưa lên git**.

## Khi được yêu cầu "làm unit N"
1. Kiểm tra `docs/TIEN_DO.md`: unit phải thuộc đợt đang mở; đang ở nhánh `unit-NN` (chưa thì tạo từ `main`).
2. Đọc bản cũ `unitN.html` (dữ liệu trong thẻ script) để lấy chất liệu, đọc bộ luật và bài mẫu `data-src/unit01.json`.
3. Viết `data-src/unitNN.json` (mỗi câu có `vi`), copy `unit1.html` thành `unitN.html` (sửa title, `data-unit`, tên file data).
4. `uv run tools/build.py N` rồi `uv run tools/check.py N` đến 0 lỗi; mở `docs/ipa-review/unitNN.txt` soát IPA. Nếu không chắc một từ, **liệt kê cho người dùng tra lại, không đoán**; không tự ý thêm vào `ipa_overrides.json` những từ chưa chắc.
5. Xem thử bằng Edge không giao diện hoặc `tools/serve.ps1` (cổng 8765): không lỗi console, điền đáp án mẫu và chấm được.
6. Báo người dùng: kết quả `check.py`, các từ IPA cần tra, các câu dịch còn băn khoăn.
7. Chỉ commit file của unit mình. Không push, không tạo PR khi người dùng chưa yêu cầu. **Ngoại lệ:** khi người dùng bảo làm theo `docs/GIAO_VIEC.md` (giai đoạn 1) hoặc `docs/GIAO_VIEC_2.md` (giai đoạn 2) thì được tự gộp vào `main` và push đúng quy trình trong file đó (và chỉ cho các việc trong file đó). Giai đoạn 2 còn cho phép sửa engine/tools/index trong Pha 1.

## Lưu ý kỹ thuật
- Máy Windows: chạy Python bằng `uv run` (lệnh `python` trong PATH là bản giả của Microsoft Store). Console cp1252: script đã `reconfigure(encoding="utf-8")`.
- Trang mở bằng `file://` phải chạy được: **không dùng `fetch`** cho dữ liệu (đó là lý do dữ liệu là `.js`).
- `localStorage`: `egiu_done` (mảng id unit đã xong, giữ nguyên định dạng cũ để `index.html` đọc), `egiu_scores`, `egiu_prefs`.
- Sách Ms Hoa: có `LYTHUYET/[Ebook] ….txt` (đã có chữ). Sách Murphy Essential: PDF scan, đọc bằng cách render trang ra PNG (PyMuPDF qua `uv run --with pymupdf`) rồi xem ảnh; đối chiếu đáp án cuối sách.
