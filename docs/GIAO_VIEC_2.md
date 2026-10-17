# Giao việc giai đoạn 2 cho Máy 2 (làm độc lập, tự push)

> **Người giao:** chủ repo (Máy 1). **Người nhận:** Máy 2 (Claude Code trên máy 2).
> Chủ repo **đã cho phép** Máy 2 tự commit, tự gộp vào `main` và tự push **theo quy trình dưới đây**, và **cho phép sửa engine (`assets/`), `tools/`, `index.html` trong phạm vi file này** (khác với `GIAO_VIEC.md` giai đoạn 1 vốn cấm). Ngoài các việc trong file này vẫn theo `CLAUDE.md`.

**Bối cảnh:** giai đoạn 1 xong (45/45 unit V2, `check.py` 0 lỗi, trình duyệt 100%, bản đồ sách Essential đã lập). Giai đoạn 2 gồm 5 việc, chia 4 pha. Pha 1 phải xong và gộp vào `main` **trước** khi làm pha 2.

```
Pha 0  Dọn dẹp (độc lập, làm ngay)
Pha 1  Engine: dạng bài trắc nghiệm "choose" + hạ tầng nhiều bộ bài (unit / ess / topic)   ← tuần tự, tự làm
Pha 2  4 việc chạy SONG SONG (nên dùng subagent):
        2A  Bộ "Ôn theo chủ đề" 1–10        (từ Ngu_phap_TA: 100 hàng điền + 50 trắc nghiệm)
        2B  Bộ "Ôn theo chủ đề" 11–20
        2C  Bộ "Nền tảng" (Essential): 3 unit mẫu + báo cáo khả thi
        2D  Soát IPA toàn bộ 45 unit + bổ sung lý thuyết Unit 42
Pha 3  Tích hợp, cập nhật tài liệu, báo cáo tổng kết
```

---

## Quy ước chung (áp dụng cho mọi pha)

**Công cụ kiểm tra bắt buộc trước mỗi lần gộp vào `main`:**
```
uv run tools/check.py                 # mọi bộ bài: 0 lỗi
uv run tools/test_units.py            # kiểm thử trình duyệt: TẤT CẢ trang đạt (hiện 45/45)
```
`test_units.py` điền đáp án mẫu rồi chấm từng trang, đạt khi 100% và không lỗi JS. Sửa engine mà **bất kỳ trang nào rớt thì không được gộp**. (Bài test này kiểm tra engine và sự nhất quán dữ liệu, **không** kiểm tra đáp án có đúng ngữ pháp hay không. Việc đó phải tự soát.)

**Git:**
- Mỗi pha/việc làm trên nhánh riêng (`engine-v3`, `topics-01-10`, `topics-11-20`, `essential-pilot`, `ipa-review`), nhánh con trong **git worktree riêng** nếu dùng subagent (xem mục "Subagent").
- Gộp: `git fetch origin && git rebase origin/main` (trên nhánh việc) → chạy 2 công cụ kiểm tra → `git checkout main && git pull --ff-only && git merge --ff-only <nhánh>` → `git push origin main`. Push bị từ chối thì `git pull --rebase` rồi push lại. **Không `--force`.**
- Commit nhỏ, thông điệp tiếng Việt rõ nghĩa; thêm dòng `Co-Authored-By` theo hướng dẫn của hệ thống.
- **Dừng và ghi lại (đừng đoán)** khi: conflict không chắc cách xử lý; công cụ báo lỗi lạ; một việc kẹt sau 3 lần thử. Ghi vào báo cáo rồi làm việc khác không phụ thuộc.
- **Nếu một lệnh bị hệ thống/quyền từ chối (ví dụ xoá nhánh trên GitHub): KHÔNG tìm cách lách.** Ghi lệnh nguyên văn vào báo cáo cho chủ repo tự chạy.

**Nội dung:** mọi câu phải có `vi` (dịch tự nhiên), IPA do `build.py` sinh, đáp án phải đúng ngữ pháp, câu mở có `alts`. IPA không chắc thì không đoán. Không chép nguyên văn dài từ sách (viết lại lý thuyết bằng lời mình, ví dụ có thể bám ý nhưng đổi chi tiết) — chi tiết ở `docs/BUILD_RULES.md` mục 3.

**Sau khi xong mỗi việc, thêm báo cáo** `docs/bao-cao/gd2-<tên việc>.md` (mẫu cuối file).

---

## Pha 0: Dọn dẹp (làm ngay, ~10 phút)

1. **Merge bản sửa của Ngu_phap_TA.** Repo khác: https://github.com/phamvietanh158-creator/Ngu_phap_TA
   ```
   git clone https://github.com/phamvietanh158-creator/Ngu_phap_TA.git .work/ngu_phap_ta
   cd .work/ngu_phap_ta
   git log --oneline origin/cai-thien -3        # nhánh cai-thien đã có 1 commit sửa lỗi
   git checkout main && git merge --ff-only origin/cai-thien && git push origin main
   ```
   (`.work/` đã `.gitignore` ở repo EGIU. Cần `git config user.name/email` trong bản clone đó nếu chưa có.) Đây là repo riêng của chủ repo, chủ repo đã đồng ý gộp. Chỉ gộp đúng nhánh `cai-thien`, không sửa thêm. Sau đó mở `https://phamvietanh158-creator.github.io/Ngu_phap_TA/` (sau ~1 phút) kiểm tra bài còn mở được.
2. **Xoá nhánh đã gộp ở repo EGIU** (44 nhánh `unit-02` đến `unit-45`; xác minh chúng đã nằm trong `main` bằng `git branch -r --merged origin/main` rồi mới xoá):
   ```
   git push origin --delete $(seq -f "unit-%02g" 2 45)
   ```
   Lệnh này trước đây từng bị hệ thống chặn. Nếu lần này vẫn bị chặn: **không lách**, ghi nguyên lệnh vào báo cáo cho chủ repo.
3. Xoá nhánh `cai-thien` của Ngu_phap_TA sau khi đã gộp (cùng quy tắc: bị chặn thì ghi báo cáo).

---

## Pha 1: Engine (tự làm tuần tự, nhánh `engine-v3`)

Đọc kỹ `assets/egiu-core.js`, `assets/egiu-unit.js`, `tools/build.py`, `tools/check.py`, `tools/test_units.py`, `index.html` trước khi sửa.

### 1.1 Dạng bài mới `choose` (trắc nghiệm một đáp án)

```jsonc
{ "id": "T1.2", "kind": "choose", "title": "…", "instr": "…",
  "items": [ {
    "stem": "I ___ answer the question.",        // chỗ trống là ___ (đúng 1 chỗ)
    "options": ["won't", "wouldn't", "don't"],  // 2–5 lựa chọn
    "answer": "won't",                            // phải trùng đúng 1 phần tử của options
    "why": { "wouldn't": "…", "don't": "…" },     // (tuỳ chọn) vì sao đáp án đó sai
    "vi": "Tôi sẽ không trả lời câu hỏi.",        // dịch CÂU ĐÚNG ĐẦY ĐỦ
    "exp": "…" } ] }                                // giải thích đáp án đúng, 1 dòng
```
Yêu cầu:
- Hiển thị: câu có chỗ trống + các lựa chọn dạng nút; chọn xong **có thể đổi cho đến khi bấm Chấm điểm** (nhất quán với các dạng bài khác: chấm một lần ở cuối, không chấm từng câu).
- Sau khi chấm: đánh dấu đúng/sai, hiện đáp án, hiện `why` của lựa chọn người học đã chọn (nếu sai) và `exp`; hiện câu đầy đủ kèm 🔊 🐢, IPA, dịch như các dạng khác.
- `build.py`: câu để sinh IPA = `stem` thay `___` bằng `answer` (gán vào `en`).
- `check.py`: kiểm `answer ∈ options`, `options` không trùng, đúng 1 chỗ `___`, có `vi`.
- `test_units.py`: thêm cách điền `choose` vào khối PROBE (bấm nút đáp án đúng).
- Không dùng `fetch`; trang mở bằng `file://` phải chạy được (xem `CLAUDE.md`).
- Truy cập: nút có `aria-pressed`/`role`, dùng được bằng bàn phím (Tab, Enter/Space); khổ 375px không tràn ngang; chế độ tối vẫn đọc rõ.

### 1.2 Nhiều bộ bài, không đụng nhau

Hiện chỉ có `unit1..145`. Thêm hai bộ mới, **dùng chung engine**, quy ước **id số riêng** để không trùng và để `egiu_done` (mảng id đã xong trong `localStorage`) dùng chung được:

| Bộ | id | Nguồn JSON | File sinh | Trang | `data-unit` |
|----|----|-----------|-----------|-------|-------------|
| English Grammar in Use (hiện có) | 1–145 | `data-src/unitNN.json` | `data/unitNN.js` | `unitN.html` | N |
| **Ôn theo chủ đề** (Ms Hoa) | 2001–2020 | `data-src/topicNN.json` | `data/topicNN.js` | `topicN.html` | 2000+N |
| **Nền tảng** (Essential, A1–A2) | 1001–1114 | `data-src/essNNN.json` | `data/essNNN.js` | `essN.html` | 1000+N |

Việc cần làm:
- `build.py` và `check.py`: nhận cả ba tiền tố `unit`, `topic`, `ess` (tên file ↔ id theo bảng trên; vỏ trang `topicN.html`/`essN.html` phải tồn tại và dùng `assets/egiu-unit.js`). `uv run tools/build.py topic3 ess2 7` và không tham số (tất cả) đều chạy được. Giữ nguyên hành vi cũ với `unit`.
- `test_units.py`: đã quét `unit*.html`, `ess*.html`, `topic*.html`; kiểm tra chạy đúng với id mới.
- `egiu-unit.js`: liên kết "← Trang chủ" đưa về đúng tab của bộ bài (ví dụ `index.html#topic`); thanh điều hướng hiển thị đúng nhãn ("Unit 5", "Chủ đề 3", "Nền tảng 12").
- **`index.html` (trang chủ): thêm 3 tab** — *English Grammar in Use* (như hiện nay), *Ôn theo chủ đề*, *Nền tảng (Essential)*. Mỗi tab có tìm kiếm riêng, nhóm theo chủ đề, thống kê "Đã làm x/tổng" riêng, tab nhớ lựa chọn (`localStorage`, bọc `try/catch`). Bộ bài chưa có file thì để thẻ mờ "Chưa có" như hiện nay. **Giữ nguyên** mọi unit đang chạy và dấu ✓ tiến độ. Bỏ liên kết ngoài "Ôn theo chủ đề →" (sang Ngu_phap_TA) và thay bằng tab nội bộ; giữ một liên kết nhỏ ở chân trang tới Ngu_phap_TA bản gốc.
- Tab phải chạy cả khi chưa có bài nào của bộ đó (khi ấy chỉ hiện danh sách mờ).

### 1.3 Tài liệu và kiểm thử
- Cập nhật `docs/BUILD_RULES.md` (dạng `choose`, ba bộ bài, bảng id), `CLAUDE.md`, `CONTRIBUTING.md` nếu quy trình đổi.
- Chạy `check.py` + `test_units.py`: **45/45 unit cũ vẫn đạt**, cộng ít nhất 1 trang mẫu `choose` (tạo tạm hoặc dùng bài thật ở Pha 2) đạt. Sau đó gộp `engine-v3` vào `main`, push.
- Từ lúc đó **engine đóng băng**: pha 2 không được sửa `assets/`, `tools/build.py`, `tools/check.py`, `index.html`. Cần sửa gì → ghi báo cáo và nhờ chủ repo.

---

## Pha 2: Bốn việc song song (sau khi pha 1 đã lên `main`)

### Subagent (khuyến khích)
Mỗi việc 2A, 2B, 2C, 2D giao một subagent (tối đa 4 chạy cùng lúc). Quy tắc để không hỏng nhau:
- Mỗi subagent làm trong **worktree riêng**: `git worktree add .work/wt-<tên> -b <nhánh> origin/main`, chỉ sửa file thuộc việc của mình (bảng dưới), **không push, không gộp vào main**.
- Agent chính (bạn) chờ cả 4 xong rồi tích hợp tuần tự ở Pha 3, kiểm tra từng nhánh trước khi gộp.
- Giao việc cho subagent bằng prompt đầy đủ ngữ cảnh: đường dẫn file, luật `BUILD_RULES.md`, tiêu chí hoàn thành bên dưới. Subagent báo lại: kết quả `check.py`, `test_units.py`, danh sách còn nghi ngờ.

| Việc | Nhánh | File của riêng việc đó | File **không** được đụng |
|------|-------|------------------------|--------------------------|
| 2A | `topics-01-10` | `data-src/topic01..10.json`, `data/topic01..10.js`, `topic1..10.html`, `docs/ipa-review/topic01..10.txt`, `tools/import_nptA.py` (cả 2A và 2B dùng; 2A tạo, 2B chỉ chạy) | `ipa_overrides.json`, mọi file khác |
| 2B | `topics-11-20` | `data-src/topic11..20.json` … tương tự | như trên |
| 2C | `essential-pilot` | `data-src/ess002.json`, `ess003.json`, `ess050.json`, `data/ess*.js`, `ess2.html`, `ess3.html`, `ess50.html`, `docs/ESSENTIAL_PILOT.md` | mọi file khác |
| 2D | `ipa-review` | `tools/ipa_overrides.json`, `data/unit*.js` & `docs/ipa-review/unit*.txt` (sinh lại), `data-src/unit42.json` + `docs/IPA_REVIEW_TONG.md`, `docs/IPA_CAN_TRA.md` | engine, bộ bài khác |

Để tránh 2A và 2B cùng tạo `import_nptA.py`: **agent chính viết `tools/import_nptA.py` trước** (xong trước khi giao 2A/2B), hoặc 2A viết xong rồi mới giao 2B.

### Việc 2A + 2B: Bộ "Ôn theo chủ đề" (20 chủ đề, nguồn Ngu_phap_TA)

Nguồn: `https://github.com/phamvietanh158-creator/Ngu_phap_TA` (nhánh `main`, đã gộp ở Pha 0), file duy nhất `index.html` (20 bài `#lesson1`…`#lesson20`, mỗi bài: lý thuyết + 10 câu điền từ + 5 câu trắc nghiệm có giải thích từng lựa chọn). Mục tiêu: chuyển **toàn bộ** sang định dạng EGIU, có `vi` + IPA + giọng nghe.

Bảng chủ đề (1–20): Hiện tại đơn · Quá khứ đơn · Tương lai đơn · Be going to · Hiện tại tiếp diễn · Quá khứ tiếp diễn · Tương lai tiếp diễn · Hiện tại hoàn thành · Quá khứ hoàn thành · Tương lai hoàn thành · Mạo từ · Danh từ · Động từ khuyết thiếu · Tính từ · Trạng từ · Giới từ · Liên từ · Câu điều kiện · Mệnh đề quan hệ · Ôn tập tổng hợp.

Cách làm:
1. Viết `tools/import_nptA.py` (PEP 723, chỉ thư viện chuẩn): đọc `index.html` của Ngu_phap_TA, tách mỗi bài thành JSON nháp `data-src/topicNN.json` (`id` = 2000+N, `theory.blocks` từ các bảng/ghi chú/chức năng, `exercises`: 1 bài `fill` + 1 bài `choose`). Công cụ **không** dịch; ô `vi` để trống hoặc gợi ý rồi người soát điền.
2. Hàng điền từ có **nhiều ô trống** (một câu 2–3 chỗ): engine `fill` chỉ có 1 ô. Cách xử lý: chuyển thành bài `write` (cả câu) với `hint`, hoặc tách thành nhiều câu độc lập. **Không được bỏ câu.** Ghi cách xử lý vào báo cáo.
3. Câu có đáp án rỗng "không dùng mạo từ" (bài Mạo từ): chuyển thành `choose` với lựa chọn `a / an / the / (không mạo từ)`.
4. Với mỗi câu: viết `vi` tự nhiên; đáp án nhiều dạng hợp lệ → `alts`; lý thuyết có đủ ví dụ có `vi` (≥ 6 ví dụ mỗi chủ đề — Ngu_phap_TA có nhiều chỗ chỉ nêu cấu trúc, hãy bổ sung ví dụ + dịch).
5. **Kiểm đáp án trắc nghiệm và điền từ một lần nữa** (nguồn có thể sai). Nếu thấy câu sai/hỏng (thiếu chỗ trống, thiếu "to", đáp án không đúng): **sửa** và ghi vào báo cáo từng chỗ đã sửa.
6. Mỗi chủ đề: `vỏ topicN.html` (copy `unit1.html`, sửa `<title>`, `data-unit="2000+N"`, tên file data), `build.py`, `check.py`, `test_units.py` đạt.
7. Báo cáo: số câu mỗi chủ đề, các câu đã sửa lỗi nguồn, từ IPA nghi ngờ.

Tiêu chí hoàn thành: 20 trang `topic1..20.html` đạt `check.py` + `test_units.py`; **200 hàng điền từ (chứa 300 ô trống) + 100 câu trắc nghiệm**, không mất câu nào (đối chiếu số lượng từng chủ đề: 10 hàng điền + 5 trắc nghiệm).

### Việc 2C: Bộ "Nền tảng" (Essential): 3 unit mẫu + báo cáo khả thi

Chưa làm cả 114 unit. Mục tiêu: **chốt cách làm** để chủ repo quyết có mở rộng hay không.

1. Dùng `docs/ESSENTIAL_MAP.md` + `tools/pdf_pages.py` (trang PDF = `2N+7` lý thuyết, `2N+8` bài tập; đáp án trong *Key to Exercises* PDF trang 263–290). PDF ở `LYTHUYET/…Murphy - Book.pdf` (scan, không có chữ → render ra PNG rồi **xem ảnh**).
2. Làm **3 unit**: Unit 2 (am/is/are questions, bài toàn chữ), Unit 3 (I am doing, bài có tranh), Unit 50 (work/working go/going do/doing, bài toàn chữ). Ra `ess002`, `ess003`, `ess050` đủ `json/js/html` như bộ unit (≥ 20 câu bài tập mỗi unit, lý thuyết viết lại bằng lời mình + dịch).
3. Đáp án lấy từ phần Key của sách, **đối chiếu từng câu**; câu hình ảnh: viết lại bằng chữ đủ ngữ cảnh (như Unit 1 V2).
4. Viết `docs/ESSENTIAL_PILOT.md`: thời gian làm mỗi unit; tỉ lệ bài phải viết lại vì hình (dựa cột "tranh" trong bản đồ); khó khăn khi đọc scan (câu mờ, chữ nhỏ, đáp án khó đối chiếu); rủi ro bản quyền; **đề xuất chia 114 unit thành đợt nào, ưu tiên unit nào, ước tính tổng công**, và cách chia cho 2 máy.
5. Báo cáo + `check.py`/`test_units.py` đạt.

### Việc 2D: Soát IPA toàn bộ + bổ sung Unit 42

**IPA.** `build.py` sinh IPA tự động (espeak → Cambridge), đúng khoảng 90–95%. Cần soát cả 45 unit:
1. Gom danh sách từ duy nhất từ `docs/ipa-review/unit*.txt`.
2. **Phân loại sơ bộ bằng hiểu biết của bạn** các từ có nguy cơ sai: tên riêng, địa danh, viết tắt, từ đồng chữ khác âm (read, lead, live, wind, tear, bass…), từ vay, từ có nhiều cách đọc, từ ngoại lệ (colonel, island, Wednesday, comfortable, vegetable, …), hậu tố -ed/-s đọc /t d ɪd s z ɪz/.
3. Với các từ nghi sai: **tra Cambridge Dictionary** (`https://dictionary.cambridge.org/dictionary/english/<từ>`, lấy IPA **UK**) nếu có công cụ tra web; tra có chừng mực (không quá vài trăm từ, không gửi dồn dập). **Chắc chắn** thì thêm vào `tools/ipa_overrides.json` (`"từ chữ thường": "ipa"`). Không chắc hoặc không tra được thì **không ghi vào overrides**, ghi vào `docs/IPA_CAN_TRA.md` (từ, IPA hiện tại, lý do nghi ngờ).
4. Chạy lại `uv run tools/build.py` (tất cả) → các `data/unit*.js` và `docs/ipa-review/*` tự cập nhật. Chạy `check.py` + `test_units.py`.
5. `docs/IPA_REVIEW_TONG.md`: số từ duy nhất, số từ đã kiểm, số từ đã sửa, số còn nghi ngờ, các quy luật lỗi hệ thống của espeak phát hiện được (để sau này sửa trong `build.py`).

**Unit 42** (`data-src/unit42.json`): lý thuyết chỉ có 4 ví dụ (luật ≥ 6). Bổ sung ≥ 4 ví dụ có `vi` (ví dụ bảng quá khứ phân từ thường gặp, bị động với by, câu hỏi bị động), `build.py` lại, `check.py`/`test_units.py` đạt.

---

## Pha 3: Tích hợp và báo cáo

1. Kiểm tra lần lượt từng nhánh pha 2 (đọc file, chạy `check.py`, `test_units.py`), gộp vào `main` theo quy trình ở trên.
2. Cập nhật `docs/TIEN_DO.md`: thêm bảng cho **20 chủ đề** và **3 unit Nền tảng**; trạng thái đúng thực tế; lộ trình đợt 4/5 cập nhật.
3. Cập nhật `docs/KE_HOACH.md` (mục lộ trình, quyết định về Essential theo kết quả 2C).
4. Chạy lần cuối: `uv run tools/check.py` và `uv run tools/test_units.py` toàn bộ. Mở trang chủ kiểm 3 tab, kiểm `topic1.html` và `ess2.html` trên trang chạy thật (GitHub Pages cập nhật sau ~1 phút).
5. Viết `docs/bao-cao/gd2-tong-ket.md` (mẫu bên dưới) và push.

**Khi xong tất cả hoặc kẹt toàn bộ → dừng**, báo chủ repo. Không tự mở rộng sang việc khác (ví dụ làm hết 114 unit Essential, tạo MP3 âm thanh sinh sẵn) khi chưa được giao.

---

## Mẫu báo cáo

```markdown
# Báo cáo giai đoạn 2: <tên việc>

- Nhánh / commit đã gộp: …
- check.py: ✅ x/x · test_units.py: ✅ y/y (số trang)
- Đã làm: …
- Lỗi nguồn đã sửa (ghi từng chỗ): …
- Còn nghi ngờ / cần chủ repo quyết: …
- Lệnh bị chặn (ghi nguyên lệnh để chủ repo tự chạy): …
- Việc chưa làm và lý do: …
```
