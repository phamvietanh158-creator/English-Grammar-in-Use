# Kế hoạch nâng cấp English Grammar in Use (EGIU V2)

Mục tiêu: giữ nguyên kiểu bài tập hiện nay, **bổ sung phiên âm (IPA), nghe câu chuẩn giọng Anh/Mỹ, dịch nghĩa**, thêm bài tập từ sách Ms Hoa, và (nếu khả thi) mở thêm phần mới từ *Essential Grammar in Use*. Nhiều máy cùng làm, mỗi máy một unit, gộp qua git.

## 1. Đánh giá tính khả thi (đã kiểm chứng trên máy)

| Hạng mục | Kết luận | Bằng chứng / ghi chú |
|----------|----------|----------------------|
| **Phiên âm IPA** | ✅ Khả thi, tự động 90–95% | `phonemizer` + espeak-ng (offline, cài bằng `uv`) cho IPA giọng Anh. Thô: dùng `ɛ ɹ ɡ`, sai /æ/ (ra `a`), đặt trọng âm sai chỗ. `tools/build.py` đã chuẩn hoá về kiểu Cambridge + danh sách ngoại lệ. Còn lại phải **soát tay** các từ báo trong `docs/ipa-review/` |
| **Nghe câu chuẩn hơn** | ✅ Khả thi | Dùng lại bộ chọn giọng của PRONOUNCE (Edge "Sonia/Libby/Ryan Online" cho UK, "Aria/Jenny" cho US; pitch 1.0, rate ≥ 0.7). Bản cũ chỉ gọi giọng mặc định, nên nghe méo. Giai đoạn sau: MP3 sinh sẵn (đợt 6) để mọi máy nghe giống nhau |
| **Dịch nghĩa** | ✅ Khả thi | Viết tay/AI soạn, người làm soát. Tốn công nhất: ~100 câu/unit |
| **Sách Ms Hoa (Ngữ pháp trong giao tiếp)** | ✅ Khả thi, dễ | PDF có lớp chữ; file `.txt` 16.000 dòng đã có sẵn, có mục "B. Bài tập luyện tập / C. Bài tập thực hành" và phần ĐÁP ÁN. Dạng bài: chia động từ, trắc nghiệm A–D, tìm lỗi sai (thiên về luyện thi). Cần đối chiếu đáp án thủ công vì thứ tự trong txt có thể lệch |
| **Sách Essential Grammar in Use (Murphy)** | ✅ Khả thi nhưng tốn công | PDF 299 trang, **100% ảnh scan, không có chữ** (không chuyển Markdown được). Nhưng **đọc bằng mắt được**: đã thử render trang 13 (Unit 3) ở 80 dpi, đọc rõ toàn bộ chữ, bảng, câu ví dụ. Quy trình: render trang → đọc → gõ lại thành JSON → đối chiếu bảng đáp án cuối sách. Không OCR tự động (chưa cài Tesseract; và đọc bằng mắt chính xác hơn) |
| **Hình minh hoạ** | ⚠️ Hạn chế | Bài trong Murphy dựa vào tranh ("What is happening in each picture?"). Không chép được ảnh; phải **viết lại bằng chữ** (như đã làm với bài 1.1 của Unit 1) hoặc bỏ bài đó |
| **Bản quyền** | ⚠️ Rủi ro | Cả hai sách đều có bản quyền. Repo GitHub hiện công khai và đã chứa bài tập bám sát Murphy. Khuyến nghị: **đặt repo ở chế độ private** hoặc viết lại ví dụ/bài tập bằng lời của mình; PDF gốc ở `LYTHUYET/` đã được `.gitignore`, không đưa lên git |

**Quan trọng về *Essential Grammar in Use***: đây là bản **sơ cấp (A1–A2)**, khác bản *English Grammar in Use* trung cấp (B1–B2, 145 unit) mà web app đang bám theo. Nên không nhồi vào chung 145 unit; nên làm thành **một phần học riêng "Nền tảng"** (xem đợt 4), mở ở trang chủ thành tab riêng. Với người đi làm trình độ trung cấp thì phần này dùng để ôn lại gốc, không bắt buộc.

## 2. Kiến trúc (đã dựng xong ở đợt 0)

```
EN_IN_USE/
├─ index.html                 trang chủ (chỉ trưởng nhóm sửa)
├─ unit1.html … unit45.html   vỏ mỏng: nạp assets + data của đúng unit đó
├─ assets/
│   ├─ egiu-core.css/.js      giọng đọc UK/US, tuỳ chọn, chấm đáp án (KHÔNG sửa khi làm unit)
│   └─ egiu-unit.js           dựng trang từ dữ liệu: lý thuyết, 3 dạng bài, chấm điểm, lưu tiến độ
├─ data-src/unitNN.json       ★ NGUỒN: người làm chỉ sửa file này (en + vi, không ghi IPA)
├─ data/unitNN.js             sinh tự động từ data-src (có IPA); commit cùng PR
├─ tools/
│   ├─ build.py               sinh IPA + data/unitNN.js + báo cáo từ cần soát
│   ├─ check.py               kiểm tra chất lượng unit (như `?check` của PRONOUNCE)
│   ├─ ipa_overrides.json     từ espeak đọc sai → IPA đã tra Cambridge (dùng chung mọi unit)
│   └─ serve.ps1/.bat         máy chủ xem thử cổng 8765
├─ docs/  KE_HOACH · BUILD_RULES · TIEN_DO · ipa-review/
└─ LYTHUYET/                  2 cuốn PDF (chỉ trên máy, .gitignore)
```

**Vì sao tách JSON và JS:** người làm chỉ gõ tiếng Anh + tiếng Việt, IPA do máy sinh nên mọi unit nhất quán. `data/unitNN.js` là file sinh ra để mở được bằng cách nhấp đúp (không cần server), nên vẫn commit.

**Chức năng người học thấy:** thanh công cụ dính trên cùng: 🇬🇧/🇺🇸 · ☑ Phiên âm · ☑ Dịch nghĩa (mặc định tắt, nhớ lựa chọn). Mọi câu có 🔊 và 🐢 (đọc chậm). Câu trong bài tập chỉ hiện phiên âm/dịch **sau khi chấm** (để không lộ đáp án).

## 3. Quy trình nhiều máy (giống PRONOUNCE)

Chi tiết từng bước ở [CONTRIBUTING.md](../CONTRIBUTING.md); luật soạn ở [BUILD_RULES.md](BUILD_RULES.md); nhận bài ở [TIEN_DO.md](TIEN_DO.md).

```
Nhận unit → tạo nhánh unit-07 → soạn data-src/unit07.json → build.py + check.py → PR → duyệt & merge
```

Mỗi unit là **một nhánh riêng và các file riêng** (`unit07.json`, `unit07.js`, `unit7.html`, `ipa-review/unit07.txt`), nên hai máy làm hai unit khác nhau **không bao giờ xung đột**. Chỗ duy nhất có thể xung đột là `TIEN_DO.md` (cách xử lý ghi ở CONTRIBUTING). `index.html` và `tools/ipa_overrides.json`: chỉ trưởng nhóm sửa, người làm gửi từ cần ghi đè qua PR riêng hoặc ghi vào PR của mình.

Yêu cầu mỗi máy: Git + `uv` (đã có), Edge. Không cần cài Python hay thư viện nào khác: `uv run tools/build.py` tự lo.

## 4. Lộ trình

| Đợt | Việc | Ra gì | Ghi chú |
|-----|------|-------|---------|
| **0 ✅** | Engine, `build.py`, `check.py`, tài liệu, **Unit 1 làm mẫu** | Khung chạy được, đã test tự động (chấm 35/36 đúng, lưu tiến độ) | Xong |
| **1** | Unit 2–11 | 10 unit có IPA + dịch + giọng chuẩn | Chuyển từ HTML cũ → JSON. Lấy chất liệu từ file `unitN.html` cũ (trong git: `git show main:unitN.html`) |
| **2** | Unit 12–25 | 14 unit | |
| **3** | Unit 26–45 | 20 unit | Hết 45 unit hiện có |
| **4** | Phần **"Nền tảng"** (Essential, 115 unit) | Tab riêng ở trang chủ | Bước 1: dựng bảng "unit → số trang PDF" + `tools/pdf_pages.py` render trang. Bước 2: **làm 3 unit mẫu** (đề xuất Unit 1, 3, 25) để chốt cách viết lại hình minh hoạ → mở cho cả nhóm |
| **5** | **Bài tập bổ sung Ms Hoa** | Mục "Luyện tập thêm" cuối mỗi unit (trắc nghiệm A–D, tìm lỗi sai) + **Final test** (bài tổng hợp các thì, đề cuối sách) | Cần thêm 2 dạng bài vào engine: `choose` (trắc nghiệm) và `error` (tìm lỗi sai). Ghép bài Ms Hoa vào unit theo chủ điểm (thì, modal, câu điều kiện, mệnh đề quan hệ, giới từ, liên từ…). Bài tổng hợp các thì → mục "Ôn tập" riêng |
| **6** | MP3 UK/US sinh sẵn | `audio/uk/*.mp3`, `audio/us/*.mp3` + khung `window.EGIU_AUDIO` đã có sẵn trong engine | Dùng giọng neural (edge-tts) lúc build. Ước ~80 câu × 45 unit × 2 giọng ≈ 7.000 file (~60–100 MB): nên cân nhắc Git LFS hoặc chỉ build khi deploy |
| **7** | Unit 46–145 | Phần còn lại sách Murphy trung cấp | Chỉ mở khi 1–3 xong; có thể lấy chất liệu từ bản scan nếu có thêm sách |

**Đề xuất về "bài cuối / mở phần khác"** (bạn hỏi): vì Essential đọc được, nên (a) mở **phần "Nền tảng"** như đợt 4; (b) mỗi nhóm unit có **bài cuối "Tổng hợp"** lấy từ Ms Hoa (đợt 5). Không thêm vào cuối danh sách 145 unit hiện có để khỏi lẫn trình độ.

## 5. Việc kế tiếp

1. **Bạn xem thử Unit 1 mới** (nhấp đúp `tools/serve.bat` → http://localhost:8765/unit1.html, dùng Edge) và cho ý kiến về: bố cục, mặc định tắt/bật phiên âm & dịch, cách hiện sau khi chấm.
2. Chốt xong thì mở đợt 1: có thể làm lần lượt từng unit trên một máy, hoặc chia máy theo [TIEN_DO.md](TIEN_DO.md).
3. Quyết định về bản quyền: repo private hay giữ public (mục 1).
