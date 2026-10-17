# Tiến độ EGIU V2

> **Cách nhận bài:** sửa file này ngay trên GitHub (✏️ → điền tên vào cột *Người làm*, đổi ⬜ thành 🟡 → *Commit changes* thẳng vào `main`). Chi tiết quy trình: [CONTRIBUTING.md](../CONTRIBUTING.md).
> **Quy ước:** mỗi người nhận **tối đa 2 unit** cùng lúc · chỉ nhận unit thuộc **đợt đang mở** · làm xong hoặc bỏ thì cập nhật lại dòng của mình.

**Trạng thái:** ⬜ Chưa ai nhận · 🟡 Đang làm · 🔵 Đã gửi PR, chờ duyệt · ✅ Đã merge · 🔒 Chưa mở

**"V2" nghĩa là gì:** unit đã chuyển sang dữ liệu `data-src/unitNN.json` có **IPA + dịch nghĩa + giọng đọc UK/US**, chấm điểm bằng engine chung (`assets/`). Unit chưa ✅ vẫn chạy bình thường bằng bản cũ.

---

## Lộ trình

| Đợt | Nội dung | Điều kiện | Trạng thái |
|-----|----------|-----------|:---------:|
| 0 | Engine chung + công cụ `build.py`/`check.py` + unit 1 làm mẫu + bộ luật | | ✅ Xong |
| **1** | **Unit 2–11** (Present/Past, Present perfect đầu) | Đợt 0 | 🟢 **Đang mở** |
| **2** | **Unit 12–25** (Present perfect & past, Future) | Đợt 0 | 🟢 **Đang mở** |
| **3** | **Unit 26–45** (Modals, if/wish, Passive) | Đợt 0 | 🟢 **Đang mở** |
| 4 | **Phần "Nền tảng"**: chuyển *Essential Grammar in Use* (115 unit, sách scan) thành phần học riêng A1–A2 | Chốt 3 unit mẫu (mục 4 của [KE_HOACH.md](KE_HOACH.md)) | 🔒 Chưa mở |
| 5 | **Bài tập bổ sung từ sách Ms Hoa** (mục "Luyện tập thêm" cuối mỗi unit + Final test) | Đợt 1–3 xong ≥ 50% | 🔒 Chưa mở |
| 6 | **MP3 UK/US sinh sẵn** (giọng đọc đồng nhất mọi máy, nghe offline) | Chạy song song được | 🔒 Chưa mở |
| 7 | Unit 46–145 (mở rộng phần còn lại của sách Murphy) | Đợt 1–3 xong | 🔒 Chưa mở |

**Thứ tự nên làm:** theo số unit tăng dần nếu có thể (unit sau hay nhắc lại kiến thức unit trước), nhưng làm song song vẫn được vì mỗi unit là một file riêng, không đụng nhau.

---

## Bảng unit (1–45)

| Unit | File | Nội dung | Nhóm | Đợt | Người làm | Trạng thái |
|:---:|------|----------|------|:---:|-----------|:---------:|
| 1 | unit1.html | Present continuous (I am doing) | Present and past | 0 | | ✅ |
| 2 | unit2.html | Present simple (I do) | Present and past | 1 | Máy 2 | ✅ |
| 3 | unit3.html | Present continuous and present simple 1 | Present and past | 1 | Máy 2 | ✅ |
| 4 | unit4.html | Present continuous and present simple 2 | Present and past | 1 | Máy 2 | ✅ |
| 5 | unit5.html | Past simple (I did) | Present and past | 1 | Máy 2 | ✅ |
| 6 | unit6.html | Past continuous (I was doing) | Present and past | 1 | Máy 2 | ✅ |
| 7 | unit7.html | Present perfect 1 (I have done) | Present perfect and past | 1 | Máy 2 | ✅ |
| 8 | unit8.html | Present perfect 2 (I have done) | Present perfect and past | 1 | Máy 2 | ✅ |
| 9 | unit9.html | Present perfect continuous (I have been doing) | Present perfect and past | 1 | Máy 2 | ✅ |
| 10 | unit10.html | Present perfect continuous and simple | Present perfect and past | 1 | Máy 2 | ✅ |
| 11 | unit11.html | how long have you (been) ... ? | Present perfect and past | 1 | Máy 2 | ✅ |
| 12 | unit12.html | for and since / when and how long | Present perfect and past | 2 | Máy 2 | ✅ |
| 13 | unit13.html | Present perfect and past 1 | Present perfect and past | 2 | Máy 2 | ✅ |
| 14 | unit14.html | Present perfect and past 2 | Present perfect and past | 2 | Máy 2 | ✅ |
| 15 | unit15.html | Past perfect (I had done) | Present perfect and past | 2 | Máy 2 | ✅ |
| 16 | unit16.html | Past perfect continuous (I had been doing) | Present perfect and past | 2 | Máy 2 | ✅ |
| 17 | unit17.html | have and have got | Present perfect and past | 2 | Máy 2 | ✅ |
| 18 | unit18.html | used to (do) | Present perfect and past | 2 | Máy 2 | ✅ |
| 19 | unit19.html | Present tenses for the future | Future | 2 | Máy 2 | ✅ |
| 20 | unit20.html | I'm going to (do) | Future | 2 | Máy 2 | ✅ |
| 21 | unit21.html | will and shall 1 | Future | 2 | Máy 2 | ✅ |
| 22 | unit22.html | will and shall 2 | Future | 2 | Máy 2 | ✅ |
| 23 | unit23.html | I will and I'm going to | Future | 2 | Máy 2 | ✅ |
| 24 | unit24.html | will be doing and will have done | Future | 2 | Máy 2 | ✅ |
| 25 | unit25.html | when I do and when I've done / if and when | Future | 2 | Máy 2 | ✅ |
| 26 | unit26.html | can, could and (be) able to | Modals | 3 | Máy 2 | ✅ |
| 27 | unit27.html | could (do) and could have (done) | Modals | 3 | Máy 2 | ✅ |
| 28 | unit28.html | must and can't | Modals | 3 | Máy 2 | ✅ |
| 29 | unit29.html | may and might 1 | Modals | 3 | Máy 2 | ✅ |
| 30 | unit30.html | may and might 2 | Modals | 3 | Máy 2 | ✅ |
| 31 | unit31.html | have to and must | Modals | 3 | Máy 2 | ✅ |
| 32 | unit32.html | must mustn't needn't | Modals | 3 | Máy 2 | ✅ |
| 33 | unit33.html | should 1 | Modals | 3 | Máy 2 | ✅ |
| 34 | unit34.html | should 2 | Modals | 3 | Máy 2 | ✅ |
| 35 | unit35.html | I'd better / it's time | Modals | 3 | Máy 2 | ✅ |
| 36 | unit36.html | would | Modals | 3 | Máy 2 | ⬜ |
| 37 | unit37.html | can/could/would you ...? (Requests, offers) | Modals | 3 | Máy 2 | ⬜ |
| 38 | unit38.html | if I do ... and if I did ... | if and wish | 3 | Máy 2 | ⬜ |
| 39 | unit39.html | if I knew ... / I wish I knew ... | if and wish | 3 | Máy 2 | ⬜ |
| 40 | unit40.html | if I had known ... / I wish I had known ... | if and wish | 3 | Máy 2 | ⬜ |
| 41 | unit41.html | wish | if and wish | 3 | Máy 2 | ⬜ |
| 42 | unit42.html | Passive 1 (is done / was done) | Passive | 3 | Máy 2 | ⬜ |
| 43 | unit43.html | Passive 2 (be done / been done / being done) | Passive | 3 | Máy 2 | ⬜ |
| 44 | unit44.html | Passive 3 | Passive | 3 | Máy 2 | ⬜ |
| 45 | unit45.html | it is said that ... / he is said to ... | Passive | 3 | Máy 2 | ⬜ |

---

## Ghi chú

- **Unit 1** đã xong làm mẫu (cũng sửa 5 lỗi của bản cũ: bài "picture" không có hình, nút nghe lỗi dấu nháy, bài nối câu không hiện lựa chọn, v.v.).
- Khi merge, trưởng nhóm đổi ⬜/🔵 thành ✅ và **bỏ cờ `avail:false`** nếu có ở `index.html` (chỉ trưởng nhóm sửa `index.html`).
- Unit 46–145 chưa có file; sẽ thêm vào bảng khi mở đợt 7.
