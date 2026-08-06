# Quy trình viết + tối ưu SEO bài viết cho xuanloi.me

## 1. Viết bài mới

### Format frontmatter chuẩn

```yaml
---
title: "Tiêu đề bài viết — có thể kèm subtitle sau dấu gạch ngang"
description: "1-2 câu tóm tắt, chứa keyword chính, đủ hấp dẫn để click. Tối đa 160 ký tự."
pubDatetime: YYYY-MM-DDTHH:MM:SS+07:00
tags: ["tag1", "tag2", "tag3"]  # tất cả bằng tiếng Việt, không dấu
---
```

### Quy tắc đặt tên file (slug)
- Tiếng Việt không dấu, dùng `-` thay khoảng trắng
- Ví dụ: `17-cau-hoi-thay-doi-cuoc-doi.md`
- **Không đặt trong thư mục con** — để ở `src/content/blog/` (routing tự xử lý)
- Viết content tối thiểu **1500 từ**, lý tưởng **2000-4000 từ**

---

## 2. Checklist SEO (làm sau khi viết xong)

### □ Nội dung
- [ ] Bài dài > 1500 từ
- [ ] Có ít nhất 1 câu hỏi ở cuối để khuyến khích comment
- [ ] Viết như đang nói với 1 người, không viết cho "ai cũng"
- [ ] Có internal link đến ít nhất 1 bài khác

### □ Frontmatter
- [ ] `description` chứa keyword chính và không trùng với title
- [ ] `pubDatetime` format ISO-8601 với `+07:00`
- [ ] `tags` toàn bộ bằng tiếng Việt (không dấu)
- [ ] `canonicalURL` chỉ dùng khi repost từ nơi khác

### □ Internal links
- [ ] **Luôn dùng đường dẫn `/posts/slug-cua-bai-viet`** (không dùng `../../` relative)
- [ ] Link chéo giữa các bài cùng chủ đề (cluster)
- [ ] Cluster hiện tại:
  - **Phát triển bản thân**: `17-cau-hoi-thay-doi-cuoc-doi` ↔ `so-chon-sai-nghe` ↔ `self-help-trap` ↔ `tai-sao-muon-tien-len-mai-khong-lam-duoc`
  - **Thương hiệu cá nhân**: `vi-sao-nguoi-gioi-lai-kho-len-tieng-nhat` ↔ `not-to-do-list-xay-thuong-hieu-ca-nhan`

---

## 3. Build + Deploy

```bash
# Build
npm run build

# Deploy (từ Windows, không có rsync)
tar -czf - -C dist . | ssh -i ~/.ssh/do-9router root@129.212.238.158 "tar -xzf - -C /var/www/xuanloi.me/"

# Reload nginx
ssh -i ~/.ssh/do-9router root@129.212.238.158 "nginx -t && systemctl reload nginx"

# Verify
curl -sI https://xuanloi.me/
```

---

## 4. Commit lên GitHub

```bash
# Stage specific files (không dùng git add .)
git add src/content/blog/...

# Commit
git commit -m "msg"

# Push
git push origin main
```

---

## 5. Lưu ý quan trọng

- **Không dùng `layout:` trong frontmatter** — Astro content collection tự động dùng route template
- **Không xoá file cũ khi rename slug** — dùng `git mv` để git track được lịch sử
- **Kiểm tra internal links** sau mỗi lần rename/move file — nếu đổi slug phải update link ở tất cả bài khác
- **Vite 6 patch** cần reapply sau mỗi `npm install` (file `node_modules/astro/dist/core/build/static-build.js`)
- **Thời gian đăng bài** lý tưởng: 8:00-10:00 sáng giờ Việt Nam (`+07:00`)

---

## 6. AI Citability Checklist (GEO Optimization)

> Dựa trên nghiên cứu từ Princeton, Georgia Tech, IIT Delhi (2024-2025).
> AI models (ChatGPT, Claude, Perplexity, Google AI Overviews) trích xuất passage dựa trên các tiêu chí cụ thể.

### Trước khi publish, kiểm tra từng H2 section:

- [ ] **Answer-first:** Mỗi H2 section mở đầu bằng 1-2 câu trả lời trực tiếp, không dẫn dắt dài dòng
- [ ] **Passage tự chứa (self-contained):** Mỗi đoạn 134-167 từ có thể đọc riêng vẫn hiểu — không phụ thuộc vào ngữ cảnh xung quanh
- [ ] **Định nghĩa rõ ràng:** Có ít nhất 1 câu dạng "X là..." hoặc "X có nghĩa là..." trong mỗi section chính
- [ ] **Data point:** Có ít nhất 3 số liệu/sự kiện/thống kê cụ thể trong toàn bài
- [ ] **Heading hierarchy:** H1 → H2 → H3 rõ ràng, không skip level
- [ ] **Bảng/danh sách:** Có ít nhất 1 bảng so sánh hoặc danh sách có cấu trúc trong toàn bài

### Question-based headings (ưu tiên dùng câu hỏi cho H2/H3)

AI search engines match query patterns. Dùng heading dạng câu hỏi sẽ tăng tỉ lệ được cite.

- **Thay vì:** "Tác hại của việc thức khuya"
  → **Dùng:** "Thức khuya có tác hại gì? Và tại sao người trẻ vẫn tiếp tục làm vậy?"
- **Thay vì:** "Cách xây dựng thương hiệu cá nhân"
  → **Dùng:** "Làm sao để xây dựng thương hiệu cá nhân khi bạn bắt đầu từ con số 0?"
- **Thay vì:** "Lợi ích của việc đọc sách"
  → **Dùng:** "Đọc sách có thực sự giúp bạn thông minh hơn không?"

### Ví dụ passage đạt chuẩn citability (134-167 từ)

> Content delivery networks (CDNs) là hệ thống máy chủ phân tán, lưu trữ và phân phối nội dung web từ các vị trí địa lý gần người dùng cuối. CDN giúp giảm độ trễ trung bình 50-70% bằng cách phục vụ assets từ edge servers thay vì một origin server duy nhất. Ba nhà cung cấp CDN lớn nhất tính đến 2025 là Cloudflare (phục vụ khoảng 20% tổng số website), Amazon CloudFront, và Akamai Technologies.

- ✅ Từ: 134-167 → OK (~58 từ tiếng Việt, ~100 từ tiếng Anh tương đương)
- ✅ Self-contained: đọc riêng vẫn hiểu
- ✅ Định nghĩa: "CDNs là..."
- ✅ Data point: 3 số liệu cụ thể (50-70%, 20%, 3 nhà cung cấp)

### Ví dụ passage KHÔNG đạt chuẩn

> Nếu bạn từng thắc mắc tại sao một số website tải nhanh hơn những website khác, câu trả lời có thể sẽ làm bạn ngạc nhiên. Có một công nghệ tuyệt vời đã tồn tại được một thời gian. Nó đã thay đổi cách chúng ta nghĩ về hiệu suất web. Để tôi giải thích cách nó hoạt động và tại sao bạn nên quan tâm đến nó cho doanh nghiệp của mình.

- ❌ Không self-contained: không nêu rõ chủ đề
- ❌ 0 data point
- ❌ Không có định nghĩa
- ❌ Dẫn dắt dài, không answer-first

### Tại sao quan trọng

- AI-referred traffic growth: +527% year-over-year (SparkToro 2025)
- AI traffic conversion rate: 4.4x cao hơn organic (Gartner)
- 92% AI Overview citations đến từ top-10 ranking pages
- Brand mentions tương quan với AI visibility mạnh gấp 3 lần backlinks (Ahrefs 2025)
