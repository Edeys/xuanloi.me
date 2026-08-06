# Cẩm nang SEO & GEO cho xuanloi.me

> Tổng hợp từ [geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) (GEO-first) và [claude-seo](https://github.com/AgriciDaniel/claude-seo) (Full-stack SEO).
> Phiên bản: 2026-08-02 | Dành cho AI agent và người quản trị.

---

## PHẦN 1: Playbook kỹ thuật (đã implement)

### 1.1 AI Crawler Access (`geo-crawlers` + `seo-technical`)

**Nguồn:** geo-seo-claude/skills/geo-crawlers + claude-seo/skills/seo-technical

**Đã làm:** `robots.txt` cho phép 10 AI crawlers, thêm `Content-Signal`.

**Kiểm tra định kỳ (mỗi 3 tháng):**
- [ ] `curl https://xuanloi.me/robots.txt` → có đủ GPTBot, ClaudeBot, PerplexityBot
- [ ] Vào [Google Rich Results Test](https://search.google.com/test/rich-results) kiểm tra page bất kỳ
- [ ] Kiểm tra `Content-Signal` còn đúng chính sách không (hiện tại: train=yes, search=yes)

### 1.2 llms.txt (`geo-llmstxt`)

**Nguồn:** geo-seo-claude/skills/geo-llmstxt

**Đã làm:** `public/llms.txt` + `public/llms-full.txt`

**Cập nhật khi:** Thêm bài mới → thêm vào `llms-full.txt`. Mỗi 10 bài mới → review `llms.txt` chọn bài tiêu biểu.

### 1.3 Structured Data (`geo-schema` + `seo-schema`)

**Nguồn:** geo-seo-claude/skills/geo-schema + claude-seo/skills/seo-schema

**Đã làm:**
- Homepage: Person + WebSite + SearchAction
- Blog post: BlogPosting + BreadcrumbList + Person (@id ref)
- `sameAs` links: YouTube, Facebook, GitHub
- `knowsAbout` trên Person: 6 chủ đề

**Schema types KHÔNG nên dùng (từ claude-seo):**
- `FAQPage` — Google retired rich results May 2026
- `HowTo` — retired Sep 2023
- `SpecialAnnouncement`, `CourseInfo`, `ClaimReview` — deprecated

**Khi viết bài mới tự động có:** BlogPosting + BreadcrumbList (Astro tự render từ `PostDetails.astro`)

---

## PHẦN 2: Playbook viết bài (áp dụng mỗi lần viết)

### 2.1 AI Citability Checklist (`geo-citability`)

**Nguồn:** geo-seo-claude/skills/geo-citability (Princeton, Georgia Tech, IIT Delhi research)

**Checklist trước khi publish:**

```
[ ] ANSWER-FIRST: Mỗi H2 mở đầu bằng 1-2 câu trả lời trực tiếp
[ ] SELF-CONTAINED: Mỗi passage 134-167 từ đọc riêng vẫn hiểu
[ ] ĐỊNH NGHĨA: ≥1 câu dạng "X là..." trong mỗi section chính
[ ] DATA POINTS: ≥3 số liệu/thống kê cụ thể trong toàn bài
[ ] HEADING CÂU HỎI: Dùng H2/H3 dạng câu hỏi thay vì statement
[ ] BẢNG/DANH SÁCH: ≥1 bảng so sánh hoặc danh sách có cấu trúc
```

**Ví dụ đạt chuẩn:**
> Content delivery networks (CDNs) là hệ thống máy chủ phân tán, lưu trữ và phân phối nội dung web từ các vị trí địa lý gần người dùng cuối. CDN giúp giảm độ trễ trung bình 50-70%. Ba nhà cung cấp lớn nhất 2025: Cloudflare (20% website), Amazon CloudFront, Akamai.

**Ví dụ KHÔNG đạt:**
> Nếu bạn từng thắc mắc tại sao website này nhanh hơn website kia... có một công nghệ thú vị... để tôi giải thích...

### 2.2 E-E-A-T Framework (`seo-content`)

**Nguồn:** claude-seo/skills/seo-content (Google QRG Sep 2025)

**Trọng số:** Trust (30%) > Expertise (25%) = Authoritativeness (25%) > Experience (20%)

| Yếu tố | Cách thể hiện trên xuanloi.me |
|---|---|
| **Experience** | Kể chuyện thật, kinh nghiệm cá nhân, before/after, số liệu tự làm |
| **Expertise** | Byline Đào Xuân Lợi rõ ràng, link về /about, chủ đề đúng chuyên môn |
| **Authoritativeness** | Cited bởi người khác, brand mentions YouTube/Facebook, backlinks |
| **Trust** | HTTPS, ngày đăng + ngày cập nhật, contact info, chính sách rõ ràng |

**Who/How/Why test (Google canonical heuristic):**
- **Who** tạo ra? → Có byline, link về /about
- **How** tạo ra? → Viết từ trải nghiệm thật, có dẫn chứng
- **Why** tồn tại? → Để giúp người đọc, không phải để câu SEO

### 2.3 Content Freshness

**Nguồn:** Cả 2 repo — content < 3 tháng được AI cite gấp 3 lần

- [ ] Bài mới < 3 tháng: ưu tiên share, promote
- [ ] Bài 3-6 tháng: review, cập nhật nếu cần, đổi `modDatetime`
- [ ] Bài > 6 tháng: cân nhắc rewrite hoặc thêm "Cập nhật [tháng/năm]"

### 2.4 Question-Based Headings

**Nguồn:** Cả 2 repo — 92% AI Overview citations từ top-10 pages, heading câu hỏi khớp query pattern

**Pattern:**
- ❌ "Tác hại của thức khuya"
- ✅ "Thức khuya có hại thế nào? Và tại sao người trẻ vẫn thức khuya?"
- ❌ "Cách xây thương hiệu cá nhân"
- ✅ "Làm sao xây thương hiệu cá nhân khi bắt đầu từ số 0?"

### 2.5 Internal Linking

**Nguồn:** claude-seo/seo-content — 3-5 internal links per 1000 từ

- Luôn dùng đường dẫn `/posts/slug` (không relative)
- Link chéo giữa các bài cùng cluster
- Anchor text mô tả (không "click here")

---

## PHẦN 3: Chiến lược dài hạn (6-12 tháng)

### Giai đoạn 1: Nền móng (tháng 1-2) ✅ ĐÃ XONG

- [x] llms.txt + llms-full.txt
- [x] AI crawler robots.txt rules + Content-Signal
- [x] Schema Person + WebSite + BlogPosting + BreadcrumbList
- [x] Fix duplicate JSON-LD
- [x] Alt text cho hero image
- [x] Deploy tự động (`npm run deploy`)

### Giai đoạn 2: Content optimization (tháng 2-4)

- [ ] Reformatted 5 bài viết hiện có theo citability checklist
- [ ] Tất cả bài mới viết theo checklist từ đầu
- [ ] Thêm ít nhất 1 bảng/danh sách có cấu trúc mỗi bài
- [ ] Mỗi bài có ≥1 internal link đến bài khác
- [ ] Cập nhật `SEO-WORKFLOW.md` thành thói quen viết

### Giai đoạn 3: Brand building (tháng 3-6)

- [ ] **YouTube**: Đăng video 2-4 lần/tháng, mention blog trong description
- [ ] **Facebook**: Cross-post bài viết, tham gia group chất lượng
- [ ] **LinkedIn**: Tạo profile, cross-post bài về marketing/sự nghiệp
- [ ] **Spiderum/Viblo**: Repost bài chọn lọc (có canonical về xuanloi.me)
- [ ] **Podcast/Interview**: Xuất hiện trên podcast tiếng Việt về phát triển bản thân

### Giai đoạn 4: Authority signals (tháng 6-12)

- [ ] **Original research**: Làm 1 survey nhỏ về chủ đề của blog, publish kết quả
- [ ] **Wikipedia tiếng Việt**: Đóng góp bài về marketing/tâm lý
- [ ] **Wikidata**: Tạo entry cho personal brand (khi đủ nổi bật)
- [ ] **Backlinks**: Guest post trên blog khác, trả lời báo chí

---

## PHẦN 4: Metrics & theo dõi

### Chỉ số kỹ thuật (kiểm tra hàng tuần)
- [ ] Google Search Console: index status, lỗi crawl
- [ ] `curl https://xuanloi.me/llms.txt` → 200
- [ ] `curl https://xuanloi.me/robots.txt` → có GPTBot
- [ ] Rich Results Test: không lỗi schema

### Chỉ số tăng trưởng (theo dõi hàng tháng)
- [ ] Google Search Console: clicks, impressions, CTR, position
- [ ] Google Analytics (nếu có): sessions, bounce rate, time on page
- [ ] YouTube: subscribers, views từ link blog
- [ ] Facebook: reach, engagement, clicks về blog

### Chỉ số GEO (theo dõi hàng quý)
- [ ] Tìm tên mình + chủ đề trên ChatGPT/Copilot → có được cite không?
- [ ] Tìm trên Perplexity → có xuất hiện không?
- [ ] Google AI Overviews: có bài nào được chọn không?
- [ ] Brand mentions: search "Đào Xuân Lợi" hoặc "xuanloi.me" trên Google

---

## PHẦN 5: Quy trình viết bài mới

```
BƯỚC 1: Lên outline theo citability checklist (5 phút)
  - Chọn 3-5 câu hỏi làm H2 heading
  - Mỗi H2: 1 câu answer-first + 134-167 từ self-contained

BƯỚC 2: Viết nháp (30-60 phút)
  - Viết như nói chuyện với 1 người
  - Nhét ≥3 data point/số liệu
  - ≥1 bảng so sánh hoặc danh sách
  - ≥1 internal link

BƯỚC 3: Review SEO (5 phút)
  - [ ] Description ≠ title, chứa keyword chính, <160 ký tự
  - [ ] Tags toàn tiếng Việt không dấu
  - [ ] pubDatetime format ISO-8601 +07:00
  - [ ] Internal links dùng /posts/slug

BƯỚC 4: Deploy (tự động)
  $ npm run deploy

BƯỚC 5: Promote (trong 24h)
  - Đăng Facebook + group
  - Thêm link vào description YouTube video liên quan
  - Gửi newsletter (nếu có)
```

---

## PHẦN 6: Những thứ KHÔNG làm (myth-busting từ 2 repo)

| Điều KHÔNG nên | Lý do | Nguồn |
|---|---|---|
| Nhồi nhét keyword | Google không dùng keyword density làm ranking factor | claude-seo |
| Dùng FAQPage schema | Google retired rich results May 2026 | claude-seo |
| Chunking content cho AI | Google explicitly says "chunking for AI is ineffective" | claude-seo/geo |
| Viết content bằng AI không edit | Google phạt low-quality scaled content | claude-seo |
| Mua backlinks | Google Penguin phạt, mất trust | claude-seo |
| Đổi slug bài cũ không redirect | Mất traffic, 404 | Best practice |
| Block tất cả AI crawlers | Mất visibility trong ChatGPT, Perplexity | geo-seo-claude |
| Coi GEO là môn riêng | Google: "GEO = SEO fundamentals applied to AI surfaces" | claude-seo/geo |

---

## Tài liệu tham khảo

- [Google AI Optimization Guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Schema.org](https://schema.org/)
- [llms.txt spec](https://llmstxt.org/)
- [Content-Signal IETF draft](https://contentsignals.org/)
- [Google Search Central](https://developers.google.com/search)
- geo-seo-claude: `~/.claude/skills/geo/` (nếu đã cài)
- claude-seo: `~/.claude/skills/seo/` (nếu đã cài)
