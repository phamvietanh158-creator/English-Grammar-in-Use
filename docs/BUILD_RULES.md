# Luật soạn unit (EGIU V2)

Làm theo [unit1.html](../unit1.html) + [data-src/unit01.json](../data-src/unit01.json) (bài mẫu). Chạy `uv run tools/check.py N` đến khi 0 lỗi.

## 1. File của một unit

| File | Ai viết | Ghi chú |
|------|---------|---------|
| `data-src/unitNN.json` | **người làm** | Nguồn. NN = 2 chữ số (`unit07.json`) |
| `data/unitNN.js` | `build.py` sinh | Có IPA. Commit cùng PR, không sửa tay |
| `unitN.html` | copy từ `unit1.html` | Chỉ đổi `<title>` và `data-unit="N"`, và tên file `data/unitNN.js` |
| `docs/ipa-review/unitNN.txt` | `build.py` sinh | Danh sách từ + IPA để soát |

## 2. Cấu trúc JSON

```jsonc
{
  "id": 7,                          // khớp tên file
  "title": "Present perfect 1 (I have done)",
  "theory": {
    "title": "…",
    "blocks": [                     // mỗi block: h (tiêu đề), p (chữ), table, ex (câu ví dụ) — đều tuỳ chọn
      { "h": "A · Công thức",
        "table": { "head": ["…"], "rows": [["…", "…"]] } },
      { "h": "B · Dùng khi nào?", "p": "Giải thích bằng tiếng Việt, dùng **đậm**.",
        "ex": [ { "en": "I've **lost** my keys.", "vi": "Tôi làm mất chìa khoá rồi.", "note": "(tuỳ chọn)" } ] }
    ]
  },
  "exercises": [ /* 3 dạng dưới đây */ ]
}
```

`**…**` trong `en`/`p` = in đậm (đọc và IPA tự bỏ dấu `**`). Không dùng HTML.

### Dạng `fill` (điền vào chỗ trống)
```json
{ "id": "7.1", "kind": "fill", "title": "…", "instr": "Tiếng Việt, ngắn.",
  "items": [ { "pre": "She", "suf": "a picture.", "hint": "take", "answer": "is taking",
               "alts": ["…"], "vi": "Cô ấy đang chụp ảnh.", "exp": "Giải thích 1 dòng" } ] }
```
- Câu đầy đủ = `pre + answer + suf` (máy tự ghép để sinh IPA/đọc; `vi` là **bản dịch cả câu đầy đủ**).
- **Không ghi số thứ tự** vào `pre` (engine tự đánh số).
- `hint` = từ gợi ý; `exp` = giải thích sau khi chấm.
- Viết tắt/đầy đủ tự được chấp nhận (`I'm` = `I am`, `isn't` = `is not`). Đáp án khác hợp lệ → thêm vào `alts`.

### Dạng `write` (viết cả câu)
```json
{ "id": "7.3", "kind": "write", "title": "…", "instr": "…",
  "items": [ { "context": "What's the matter?", "hint": "why / you / cry",
               "answer": "Why are you crying?", "alts": [], "vi": "Sao bạn lại khóc?", "exp": "…" } ] }
```
Câu mở nhiều đáp án đúng: **bắt buộc** liệt kê các `alts` hợp lý (người học đi làm sẽ bực nếu đúng mà bị chấm sai).

### Dạng `match` (nối câu)
```json
{ "id": "7.2", "kind": "match", "title": "…", "instr": "…",
  "left":  [ { "k": "a", "en": "…", "vi": "…" } ],
  "right": [ { "n": "1", "en": "…", "vi": "…" } ],
  "ans": { "a": "3" } }
```
`ans` phải đủ mọi khoá của `left`; số trong `ans` phải có ở `right`.

Mỗi unit: **3–5 bài, ≥ 24 câu**, đủ 3 dạng khi hợp lý. Có `source` (tuỳ chọn, ghi trong bài) nếu lấy ý từ sách khác: ví dụ `"source": "Ms Hoa, tr. 120"`.

## 3. Luật nội dung

1. **Bản dịch (`vi`)**: tiếng Việt **tự nhiên**, đúng nghĩa; không dịch từng chữ. Bài điền: dịch cả câu đầy đủ. Câu hội thoại dịch theo giọng nói.
2. **Bài dựa vào hình**: sách gốc có tranh mà ta không có → viết lại câu để **đủ chủ ngữ và ngữ cảnh bằng chữ** (xem bài 1.1 của Unit 1), hoặc bỏ. Cấm để câu thiếu thông tin ("___ the road").
3. **Ví dụ trong bài tập nên xoay quanh công việc/đời sống người đi làm** khi có thể (họp, email, báo cáo, đi công tác) — nhưng giữ đúng trọng tâm ngữ pháp của unit.
4. **Giải thích (`exp`)**: tiếng Việt, 1 dòng, nêu **quy tắc** chứ không chỉ lặp lại đáp án.
5. **Độ chính xác**: đáp án phải đúng theo ngữ pháp chuẩn Anh–Anh/Anh–Mỹ. Nếu khác nhau giữa UK và US, ghi cả hai (vào `alts`) và nói rõ trong `exp`.
6. **Bản quyền**: không chép nguyên văn đoạn dài từ sách. Lý thuyết viết lại bằng lời mình; câu ví dụ/bài tập có thể bám ý nhưng nên thay chi tiết. Ghi `source` khi lấy ý.

## 4. IPA

- IPA do máy sinh (giọng Anh, kiểu Cambridge). **Bắt buộc soát** `docs/ipa-review/unitNN.txt`: tra Cambridge Dictionary với các từ lạ/đồng âm/từ riêng (tên người, địa danh).
- Từ sai → thêm vào `tools/ipa_overrides.json` (dạng `"từ chữ thường": "IPA"`), rồi chạy lại `build.py`. Chỉ ghi khi **đã tra**, không đoán.
- Câu báo "không ghép được từng từ" (có số, viết tắt): soát cả câu.
- Giới hạn đã biết: IPA là dạng từ điển + dạng yếu cơ bản của espeak; không thể hiện nối âm/giảm âm của lời nói nhanh. Có chữ `r` nối (`weather is` → `/ˈweðər ɪz/`) là đúng chủ ý.

## 5. Checklist trước khi gửi PR

Có trong [.github/pull_request_template.md](../.github/pull_request_template.md). Tóm tắt: `check.py` 0 lỗi · đã `build.py` · soát IPA · xem thử bằng Edge (bật phiên âm + dịch, nghe UK/US, chấm thử) · Console không lỗi đỏ · 375px không tràn ngang · cập nhật `TIEN_DO.md`.
