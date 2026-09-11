# Dự Án xuanloi.me — Toàn Bộ Thông Tin

> **Cập nhật lần cuối:** 2026-08-06 — khớp trạng thái deploy hiện tại.

## 1. Tổng Quan

- **Website:** https://xuanloi.me/
- **Mô tả:** Blog cá nhân tiếng Việt về cuộc sống, marketing
- **Fork từ:** steipete/steipete.me (Astro-based personal site)
- **Ngôn ngữ:** 100% tiếng Việt
- **Font:** Geist (hỗ trợ tiếng Việt đầy đủ)
- **GitHub:** https://github.com/Edeys/xuanloi.me.git
- **Local path:** `D:\Websites\xuanloi.me` (lưu ý: bản local hiện tại **không phải git repo** — đã tách khỏi .git)

---

## 2. Hosting — DNCloud CP-2 (hiện tại)

| Thông số | Giá trị |
|----------|---------|
| **Hosting** | DNCloud CP-2, cPanel |
| **IP (origin)** | `<HOSTING_IP>` |
| **cPanel** | https://vn9.dncloud.net:2083/ (user: `<CPANEL_USER>`) |
| **Root** | `/public_html/` |
| **Access** | FTP only (không có SSH) |
| **Web server** | LiteSpeed — chạy Astro SSR qua Node.js |
| **Sau khi deploy** | Restart Node.js qua cPanel → Setup Node.js App → Restart |

---

## 3. DNS & Cloudflare

| Record | Loại | Giá trị | Ghi chú |
|--------|------|---------|---------|
| `xuanloi.me` | A | qua Cloudflare (104.21.24.34 / 172.67.216.188) | **Proxy BẬT** |
| `www.xuanloi.me` | A | qua Cloudflare (104.21.24.34 / 172.67.216.188) | Hoạt động tốt |

- **DNS Provider:** Cloudflare
- **Cloudflare proxy:** ĐANG BẬT — traffic tới user qua Cloudflare edge, origin ẩn là <HOSTING_IP>
- Vì Cloudflare proxy bật, mọi thay đổi hosting/SSL ở origin đều được Cloudflare che — site luôn phục vụ qua edge.

---

## 4. SSL

| Thông số | Giá trị |
|----------|---------|
| **SSL cho user** | Cloudflare edge certificate (issuer: Let's Encrypt YE2), tự gia hạn |
| **SSL origin** | Không bắt buộc (Cloudflare gọi origin qua HTTP hoặc self-signed) |
| **Trạng thái** | OK — còn hạn > 60 ngày (kiểm tra 2026-08-06) |

---

## 5. Kiến Trúc Chạy Site

```
User → Cloudflare (proxy, SSL edge) → DNCloud CP-2 <HOSTING_IP>
                                        └─ LiteSpeed + Node.js (Astro SSR)
                                           └─ /public_html/
```

---

## 6. Local Project

| Thông số | Giá trị |
|----------|---------|
| **Local path** | `D:\Websites\xuanloi.me` |
| **Remote** | https://github.com/Edeys/xuanloi.me.git (bản local hiện tại không có .git) |
| **Package manager** | npm (lock: package-lock.json) |
| **Node version** | >= 24.0.0 |
| **Astro version** | ^6.4.8 |

### Scripts

```bash
npm run dev          # astro dev — chạy local dev server
npm run build        # astro build && pagefind --site dist — build ra thư mục dist/
npm run deploy       # python scripts/deploy.py — build + FTP lên DNCloud
npm run preview      # astro preview — preview bản build
npm run lint         # oxlint
```

### Thư mục quan trọng

| Path | Mô tả |
|------|-------|
| `src/` | Source code chính |
| `src/pages/` | Astro pages |
| `src/layouts/Layout.astro` | Layout chính (theme toggle script) |
| `src/components/` | Components (Header, Footer, Card, Socials...) |
| `src/config` | Config: `consts.ts` (SITE, SOCIAL_LINKS, NAV_LINKS) |
| `src/content/blog/` | Blog posts (Markdown/MDX) |
| `src/styles/global.css` | CSS global (Tailwind v4 + theme variables) |
| `dist/` | Build output |
| `scripts/deploy.py` | Script deploy tự động (chứa FTP credentials) |

---

## 7. Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| **Framework** | Astro 6.4.8 (SSR) |
| **CSS** | Tailwind CSS v4.1.18 |
| **UI Components** | React 19 + Astro islands |
| **MDX** | @astrojs/mdx |
| **Search** | Pagefind v1.4.0 |
| **Analytics** | @vercel/analytics, @vercel/speed-insights |
| **Icons** | Tabler Icons (inline SVG) |
| **Syntax highlight** | Shiki (min-light / night-owl) |
| **RSS** | @astrojs/rss |
| **Sitemap** | @astrojs/sitemap |
| **Font** | Geist (variable woff2) |
| **OG image** | Satori + @resvg/resvg-js |

---

## 8. Vite 6 Patch — Cực kỳ quan trọng

**Vấn đề:** Astro 6.4.8 + Vite 6 không gọi plugin hook `buildApp` → build bị lỗi/lỗi thiếu file.

**Fix:** Patch thủ công file:
`node_modules/astro/dist/core/build/static-build.js`

Thêm `buildApp` vào mảng plugin hooks. **Phải reapply nếu `node_modules` bị xoá/cài lại.**

---

## 9. Deploy Workflow

### Auto deploy (khuyến nghị)
```bash
npm run deploy
# Hoặc: python scripts/deploy.py
```

Quy trình `scripts/deploy.py`:
1. `npm run build` → `dist/`
2. Tạo ZIP (bỏ qua images không thay đổi để tiết kiệm dung lượng)
3. Upload ZIP + PHP extractor qua FTP (`/public_html/`)
4. Gọi `/_deploy.php` → PHP tự extract, xoá cache cũ `.prerender` + `_astro`, tự hủy
5. Xác nhận `llms.txt` và `robots.txt` còn hoạt động

⚠️ Sau deploy: restart Node.js app qua cPanel → Setup Node.js App → Restart (LiteSpeed cần restart để nhận file mới).

### Manual deploy
```bash
npm run build
# Upload dist/* lên /public_html qua FileZilla hoặc cPanel File Manager
# Restart Node.js app trong cPanel
```

---

## 10. Template Modification History

### Đã làm:
- [x] Fork từ steipete/steipete.me
- [x] Xoá ~70 bài English gốc, giữ lại 3 bài Vietnamese mẫu
- [x] Xoá steipete images, game-audio.mp3, .vscode/
- [x] Stripped @vite-pwa/astro, Twitter widgets, Astro Dev Toolbar
- [x] Chuyển UI sang tiếng Việt (Header, Footer, Hero, About, nav)
- [x] Cập nhật SITE config: title "Xuân Lợi", lang "vi", timezone
- [x] Social links: YouTube, Facebook (cá nhân + fanpage), GitHub, Zalo, phone, RSS
- [x] Xoá Twitter/X, BlueSky, LinkedIn khỏi social links
- [x] Fix double-layout crash (xoá `layout` khỏi MDX frontmatter)
- [x] Fix JSON-LD `datePublished:"undefined"`
- [x] Patch static-build.js cho Vite 6
- [x] Chuyển từ DigitalOcean (<SERVER_IP>, nginx + Let's Encrypt) → DNCloud CP-2 (<HOSTING_IP>, LiteSpeed + Node.js SSR)
- [x] Bật Cloudflare proxy cho xuanloi.me + www
- [x] Viết `scripts/deploy.py` tự động hóa deploy FTP
- [x] SSL quản lý bởi Cloudflare edge (không cần quản lý cert origin)

### Cần làm tiếp:
- [ ] Viết thêm blog posts (content/blog/*.md)
- [ ] Reapply Vite 6 patch nếu cài lại node_modules
- [ ] (Tùy chọn) Khôi phục git repo local + push lên GitHub

---

## 11. Cấu Trúc Blog Post

Mỗi post trong `src/content/blog/` cần frontmatter:

```yaml
---
title: "Tiêu đề bài viết"
description: "Mô tả ngắn"
pubDatetime: 2026-07-01
tags: ["tag1", "tag2"]
featured: true/false   # optional, để hiện trong Featured section
---
```

---

## 12. Theme

| Chế độ | Accent Color | Background |
|--------|-------------|------------|
| **Light** | `#006cac` (xanh dương) | `#fdfdfd` |
| **Dark** | `#ff6b01` (cam) | `#212737` |

Theme toggle script trong `src/layouts/Layout.astro`:
- Áp dụng class ngay lập tức (tránh flash)
- Đính event listener sau DOMContentLoaded
- Xử lý `astro:after-swap` cho view transitions

---

## 13. Lịch Sử Hosting (tham khảo)

Trước đây site chạy trên **DigitalOcean**:
- IP cũ: `<SERVER_IP>` (sgp1, Ubuntu 24.04, 1 vCPU/1GB)
- Nginx + Let's Encrypt certbot, root `/var/www/xuanloi.me`
- **Đã ngừng dùng** — hiện deploy trên DNCloud CP-2 (xem mục 2)
