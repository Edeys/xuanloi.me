# Dự Án xuanloi.me — Toàn Bộ Thông Tin

## 1. Tổng Quan

- **Website:** https://xuanloi.me/
- **Mô tả:** Blog cá nhân tiếng Việt về cuộc sống, marketing
- **Fork từ:** steipete/steipete.me (Astro-based personal site)
- **Ngôn ngữ:** 100% tiếng Việt
- **Font:** Geist (hỗ trợ tiếng Việt đầy đủ)
- **GitHub:** https://github.com/Edeys/xuanloi.me.git

---

## 2. Server — DigitalOcean

| Thông số | Giá trị |
|----------|---------|
| **Hostname** | `ubuntu-s-1vcpu-1gb-sgp1` |
| **OS** | Ubuntu 24.04 (trixie/sid) — kernel 6.8.0-124-generic |
| **Spec** | 1 vCPU, 1GB RAM, 25GB SSD |
| **Region** | Singapore (sgp1) |
| **Public IP** | `129.212.238.158/20` — eth0 |
| **Private IP** | `10.15.0.8/16` — eth0 |
| **SSH User** | `root` |
| **SSH Key** | `~/.ssh/do-9router` (local machine) |
| **SSH Command** | `ssh -i ~/.ssh/do-9router root@129.212.238.158` |

---

## 3. DNS

| Record | Loại | Giá trị | Ghi chú |
|--------|------|---------|---------|
| `xuanloi.me` | A | `129.212.238.158` | Direct — **không** Cloudflare proxy |
| `www.xuanloi.me` | A | `129.212.238.158` | Hiện NXDOMAIN (chưa add) |

- **DNS Provider:** Mặc định của DigitalOcean (hoặc nơi đăng ký domain)
- **Cloudflare:** Đã disable proxy, DNS trỏ thẳng vào IP server

---

## 4. SSL — Let's Encrypt

| Thông số | Giá trị |
|----------|---------|
| **Tool** | Certbot 2.9.0 |
| **Authenticator** | nginx |
| **Domain** | xuanloi.me (có www trong config nhưng chưa renew, chỉ chính thức 1 domain) |
| **Cert path** | `/etc/letsencrypt/live/xuanloi.me/` |
| **Fullchain** | `/etc/letsencrypt/live/xuanloi.me/fullchain.pem` |
| **Private key** | `/etc/letsencrypt/live/xuanloi.me/privkey.pem` |
| **Auto-renew** | Có (certbot tự động, cron/thử systemd timer) |
| **Account ID** | `9227605b948899a83356b626eb0c5da6` |
| **Key type** | ECDSA |

---

## 5. Nginx

- **Version:** nginx 1.24.0 (Ubuntu)
- **Config:** `/etc/nginx/sites-enabled/xuanloi.me`
- **Root:** `/var/www/xuanloi.me`
- **Index:** `index.html`
- **HTTP (80):** Redirect 301 → HTTPS
- **HTTPS (443):** Serve static files, SSL via Let's Encrypt
- **Cấu trúc config:**
  ```
  server {
      server_name xuanloi.me www.xuanloi.me;
      root /var/www/xuanloi.me;
      index index.html;
      location / {
          try_files $uri $uri.html $uri/ =404;
      }
      listen [::]:443 ssl ipv6only=on; # managed by Certbot
      listen 443 ssl; # managed by Certbot
      ssl_certificate /etc/letsencrypt/live/xuanloi.me/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/xuanloi.me/privkey.pem;
      include /etc/letsencrypt/options-ssl-nginx.conf;
      ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
  }
  # HTTP → HTTPS redirect (do certbot tạo)
  server {
      listen 80;
      listen [::]:80;
      server_name xuanloi.me www.xuanloi.me;
      return 301 https://$host$request_uri;
  }
  ```

### Permissions — Lưu ý quan trọng

Khi copy file mới lên server qua SCP, thư mục `_astro/` có thể bị set quyền `drwx------` → Nginx không đọc được CSS/JS. Luôn chạy sau khi deploy:

```bash
ssh -i ~/.ssh/do-9router root@129.212.238.158 \
  "chmod 755 /var/www/xuanloi.me/_astro && find /var/www/xuanloi.me/_astro -type f -exec chmod 644 {} +"
```

---

## 6. Local Project

| Thông số | Giá trị |
|----------|---------|
| **Local path** | `D:\Dự Án Cá Nhân\xuanloi.me` |
| **Remote** | `origin → https://github.com/Edeys/xuanloi.me.git` |
| **Branch** | `main` (hoặc master) |
| **Package manager** | npm (lock: package-lock.json, nhưng package.json ghi pnpm@10.33.2) |
| **Node version** | >= 24.0.0 |
| **Astro version** | ^6.3.1 (đang dùng 6.4.8) |

### Scripts

```bash
npm run dev          # astro dev — chạy local dev server
npm run build        # astro build && pagefind --site dist — build ra thư mục dist/
npm run preview      # astro preview — preview bản build
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
| `dist/` | Build output (được SCP lên server) |

---

## 7. Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| **Framework** | Astro 6.4.8 |
| **CSS** | Tailwind CSS v4.1.18 |
| **UI Components** | React 19 + Astro islands |
| **MDX** | @astrojs/mdx |
| **Search** | Pagefind v1.5.2 |
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

```bash
# Bước 1: Build
cd "D:\Dự Án Cá Nhân\xuanloi.me"
npm run build

# Bước 2: SCP lên server
scp -i ~/.ssh/do-9router -r dist/* root@129.212.238.158:/var/www/xuanloi.me/

# Bước 3: Fix permissions (quan trọng!)
ssh -i ~/.ssh/do-9router root@129.212.238.158 \
  "chmod 755 /var/www/xuanloi.me/_astro && find /var/www/xuanloi.me/_astro -type f -exec chmod 644 {} +"

# Bước 4: Reload nginx
ssh -i ~/.ssh/do-9router root@129.212.238.158 "systemctl reload nginx"
```

**Hay dùng deploy.sh (nếu có):** `npm run deploy`

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
- [x] Set up Nginx + Let's Encrypt SSL trên server
- [x] Fix permissions `_astro/` nhiều lần

### Cần làm tiếp:
- [ ] Viết thêm blog posts (content/blog/*.md)
- [ ] Add www.xuanloi.me DNS record (hiện NXDOMAIN)
- [ ] Reapply Vite 6 patch nếu cài lại node_modules

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

## 13. Docker Container Folder

⚠️ **Lưu ý:** Project nằm trong thư mục chứa nhiều dự án:
`D:\Dự Án Cá Nhân\Website bán đất\`

Bên trong đó có:
- `xuanloi.me/` — empty clone, ignore (dùng path `D:\Dự Án Cá Nhân\xuanloi.me`)
- `dat-dak-nong/` — dự án khác
- `fonts/` — fonts dùng chung
