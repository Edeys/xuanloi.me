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
