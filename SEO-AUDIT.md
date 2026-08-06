# SEO-AUDIT — xuanloi.me (2026-08-06)

Audit 17 bài viết bằng skill `viet-content-seo-geo-v5` (script score.mjs).
Ngưỡng đạt: **SEO ≥ 75 · AEO ≥ 70 · GEO ≥ 70**.

> **Lưu ý keyword:** keyword dùng trong audit này được **tự suy từ title/H1**. Điểm số thực tế thay đổi theo keyword chuẩn — cần đối chiếu với query thật trong Google Search Console (bước tiếp theo).

## 1. Bảng điểm tổng

| # | Bài | Slug (file) | SEO | AEO | GEO | Trạng thái |
|---|---|---|---|:--:|:--:|:--:|---|
| 1 | Vì sao người giỏi lại khó lên tiếng nhất | vi-sao-nguoi-gioi-lai-kho-len-tieng-nhat | **84** | **75** | **74** | ✅ ĐẠT cả 3 |
| 2 | Bắt đầu với marketing số | bat-dau-voi-marketing-so | **76** | **75** | 50 | ⚠️ 2/3 |
| 3 | Not-To-Do List thương hiệu cá nhân | not-to-do-list-xay-thuong-hieu-ca-nhan | 65 | 48 | 48 | ❌ |
| 4 | 8 thứ tốt hơn cả miễn phí thời AI | 8-thu-tot-hon-ca-mien-phi-trong-thoi-tri-tue-nhan-tao | 63 | 54 | 54 | ❌ |
| 5 | Tuổi trẻ không tiền, không người hậu thuẫn | tuoi-tre-khong-tien-khong-nguoi-hau-thuan | 59 | 60 | 53 | ❌ |
| 6 | Bài học phát triển bản thân | bai-hoc-phat-trien-ban-than | 58 | 68 | 53 | ❌ |
| 7 | Khoảnh khắc nhận ra sức khỏe bị hỏng | khoanh-khac-nhan-ra-suc-khoe-bi-hong | 58 | 60 | 38 | ❌ |
| 8 | 23 bản nháp, 8 tháng, 0 bài đăng | 23-ban-nhap-8-thang-0-bai-dang | 57 | 66 | 51 | ❌ |
| 9 | Bài tập định hình nỗi sợ | bai-tap-dinh-hinh-noi-so | 56 | 51 | 49 | ❌ |
| 10 | 17 câu hỏi thay đổi cuộc đời | 17-cau-hoi-thay-doi-cuoc-doi | 54 | 62 | 53 | ❌ |
| 11 | Đầu tư đất nông nghiệp — cái bẫy | dau-tu-nong-nghiep-cai-bay-cua-nhung-nguoi-nghi-minh-thong-minh | 54 | 54 | 54 | ❌ |
| 12 | Càng lớn càng khó yêu | cang-lon-cang-kho-yeu | 48 | 62 | 57 | ❌ |
| 13 | Self-help trap | self-help-trap | 48 | 56 | 57 | ❌ |
| 14 | Chọn sai nghề | so-chon-sai-nghe | 48 | 36 | 39 | ❌ |
| 15 | Vì sao muốn tiến lên mà không làm được | tai-sao-muon-tien-len-mai-khong-lam-duoc | 42 | 35 | 34 | ❌ |
| 16 | Tỷ phú xe ôm — đất nông nghiệp | ty-phu-xe-om-chan-ly-ve-dat-nong-nghiep | 42 | 35 | 34 | ❌ |
| 17 | Đêm không ngủ vì kịch bản trong đầu | dem-khong-ngu-vi-kich-ban-trong-dau | 38 | 41 | 36 | ❌ |
| | **Trung bình toàn site** | | **56** | **55** | **49** | |

**Kết quả:** 1/17 bài đạt cả 3 ngưỡng · 2/17 đạt SEO · 2/17 đạt AEO · 1/17 đạt GEO.

## 2. Lỗi phổ biến (tần suất trên 17 bài)

| Tần suất | Tiêu chí | Lăng kính | Trọng số | Vấn đề |
|---:|---|---|:--:|---|
| 100% | `slug` | SEO | 6 | Slug thiếu keyword |
| 100% | `images` | SEO | 7 | Không bài nào có ảnh + alt |
| 100% | `faq` | AEO | 12 | Không bài nào có khối `## FAQ` |
| 100% | `schema` | GEO | 9 | Không có FAQ structured data |
| 94% | `outbound` / `sources` | SEO/GEO | 6+12 | Không dẫn nguồn ngoài (đã chốt bỏ qua) |
| 94% | `summary` | AEO | 7 | Thiếu khối Key takeaways / "Tóm lại" |
| 94% | `quotable` | GEO | 14 | Mở bài không trích-dẫn-được |
| 88% | `kwInHeading` | SEO | 7 | Keyword không nằm trong heading |
| 88% | `internalLinks` | SEO | 8 | < 2 internal link |
| 88% | `howto` | AEO | 8 | Thiếu chuỗi ≥ 3 bước đánh số |
| 88% | `freshness` | GEO | 7 | Thiếu dòng "Cập nhật lần cuối" |
| 82% | `answerUpfront` | AEO | 16 | Mở bài lan man, không trả lời thẳng |
| 82% | `questionHeadings` | AEO | 12 | Heading khẳng định, không phải câu hỏi |
| 76% | `title` | SEO | 12 | Title > 60 ký tự hoặc thiếu keyword |
| 71% | `queryMatch` | AEO | 9 | Keyword không ở heading/đoạn đầu |

## 3. Thứ tự ưu tiên xử lý (ROI)

Mỗi bài sửa theo thứ tự vá điểm của skill (mục E checklist): quick-answer đầu bài → FAQ → heading câu hỏi → internal link → ảnh/alt → meta/title/slug → freshness.

**Đợt 1 (3 bài, gồm bài đạt + bài có tiềm năng nhất):**
1. `vi-sao-nguoi-gioi-lai-kho-len-tieng-nhat` — đã đạt, chỉ vá lỗi lẻ (ảnh, FAQ, slug) để giữ chuẩn
2. `not-to-do-list-xay-thuong-hieu-ca-nhan` — dài nhất (12.4KB), chủ đề search được, AEO/GEO thấp
3. `tuoi-tre-khong-tien-khong-nguoi-hau-thuan` — chủ đề có lượng tìm kiếm, điểm trung bình

**Đợt 2 (4 bài):** `bat-dau-voi-marketing-so` (đạt 2/3), `8-thu-tot-hon-ca-mien-phi-trong-thoi-tri-tue-nhan-tao`, `17-cau-hoi-thay-doi-cuoc-doi`, `23-ban-nhap-8-thang-0-bai-dang`

**Đợt 3 (5 bài):** `bai-hoc-phat-trien-ban-than`, `khoanh-khac-nhan-ra-suc-khoe-bi-hong`, `bai-tap-dinh-hinh-noi-so`, `dau-tu-nong-nghiep-cai-bay-cua-nhung-nguoi-nghi-minh-thong-minh`, `cang-lon-cang-kho-yeu`

**Đợt 4 (4 bài còn lại):** `self-help-trap`, `so-chon-sai-nghe`, `tai-sao-muon-tien-len-mai-khong-lam-duoc`, `ty-phu-xe-om-chan-ly-ve-dat-nong-nghiep`, `dem-khong-ngu-vi-kich-ban-trong-dau`

> ⚠️ Nên hoán đổi thứ tự nếu GSC cho thấy bài khác đang có traffic cao — ưu tiên bài có rank nhưng điểm thấp.

## 4. Dự kiến điểm sau tối ưu

Với việc vá đúng 7 nhóm lỗi trên (bỏ qua `outbound`/`sources` theo quyết định đã chốt):

| Lăng kính | Trước (TB) | Sau (mục tiêu) | Ngưỡng |
|---|:--:|:--:|:--:|
| SEO | 56 | 80–90 | ≥ 75 |
| AEO | 55 | 75–85 | ≥ 70 |
| GEO | 49 | 65–75 | ≥ 70 (không chắc vì thiếu `sources` 12đ) |

## 5. Baseline GSC cần xuất (chờ user)

Trước khi sửa bài nào, xuất từ Google Search Console (90 ngày, bộ lọc trang = `xuanloi.me/posts/*`): clicks, impressions, CTR, avg position theo từng URL → lưu thành `GSC-BASELINE.csv` để đối chiếu sau 2–8 tuần.
