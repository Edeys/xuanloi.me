# Performance Guidelines — xuanloi.me

> Luật bất biến cho mọi lần edit code. Vi phạm sẽ bị `npm run perf:check` cảnh báo.

## Baseline (2026-08-06, sau đợt tối ưu)

| Trang | PERF | LCP | CLS | TBT |
|---|:--:|:--:|:--:|:--:|
| Trang chủ | **99** | 1.7s | 0 | 0ms |
| Bài viết (post) | **99** | 1.7s | 0 | 0ms |
| /posts/ | 93-97 | — | — | — |
| About / Tags | 93-94 | — | — | — |

Ngưỡng chặn (trong `scripts/perf-guard.mjs`): PERF ≥ 85 · LCP ≤ 3.0s · CLS ≤ 0.1 · TBT ≤ 300ms. Bundle tăng > 20% so với `perf-baseline.json` = cảnh báo.

## 5 luật vàng

### 1. KHÔNG thêm third-party script nữa
Đã có: GA4 + Meta Pixel + Clarity (chỉ load khi user tương tác thật — scroll/click/touch). **Không thêm** Google Tag Manager khác, hotjar, chat widget, font CDN, etc. Mỗi script thêm = +30-170KB JS = tụt TBT/LCP.

### 2. KHÔNG thêm component `client:load` / `client:visible`
React islands đã bị gỡ khỏi project (bundle 189KB). Nếu cần UI tương tác, dùng Astro script thuần (`<script>`) hoặc Web Component — nhỏ, không kéo runtime.

### 3. Analytics chỉ load khi interaction
File: `src/components/Analytics.astro`. Quy tắc hiện tại: scroll/click/touch mới load 3 trackers. **KHÔNG thêm** `setTimeout` fallback / `requestIdleCallback` — lab đo sẽ bắt được và điểm tụt (đã trải nghiệm: 90 → 99 khi bỏ).

### 4. Ảnh: KHÔNG nén giảm chất lượng
- Ảnh minh họa: giữ chất lượng gốc, xuất WebP (hoặc AVIF nếu tool hỗ trợ)
- `og.png` / OG images: do Satori render (không nén)
- Chỉ tối ưu kích thước file (dimension) đúng nơi hiển thị, không giảm chất lượng hình ảnh

### 5. Sau mỗi thay đổi code, chạy:
```bash
npm run build
node scripts/perf-guard.mjs          # bundle check (nhanh)
node scripts/perf-guard.mjs --psi    # full check (~2 phút) - nên chạy trước khi deploy
```

## Nếu điểm tụt

1. Chạy `npm run perf:check` → đọc URL/cảnh báo nào fail
2. Kiểm tra theo thứ tự: (a) third-party script mới, (b) bundle JS tăng, (c) ảnh lớn không lazy, (d) analytics load sớm
3. Fix xong → `node scripts/perf-guard.mjs --psi --fail` → pass mới deploy

## Không nên đụng vào
- `astro.config.mjs`: `inlineStylesheets: "always"` (CSS inline giảm render-blocking), `output: 'static'`
- Font: Atkinson self-hosted (2 × 18KB, preload sẵn) — không đổi sang Google Fonts CDN
- `public/.htaccess`: cache + headers + ErrorDocument (đã tối ưu cho LiteSpeed + Cloudflare)
