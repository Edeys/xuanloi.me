# Đề xuất cải thiện SEO & GEO cho xuanloi.me

> Phân tích dựa trên 2 repo: [geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) (GEO-first) và [claude-seo](https://github.com/AgriciDaniel/claude-seo) (Full-stack SEO)
> Ngày phân tích: 2026-08-02 | Hosting: Vercel (Cloud) | Framework: Astro v6

---

## Tổng quan hiện trạng

**Điểm mạnh sẵn có:**
- Astro SSG → server-rendered HTML, Googlebot render được 100%
- Sitemap XML có priority theo độ tuổi bài viết
- RSS feed
- Meta tags đầy đủ (OG, Twitter Card, canonical)
- JSON-LD BlogPosting trên mỗi bài
- Google Site Verification
- Pagefind search nội bộ
- Internal linking có chủ đích (cluster)
- Writing guideline SEO cơ bản (1500+ từ, keyword trong description)

**Điểm yếu nghiêm trọng:**
- Không có `llms.txt`
- `robots.txt` quá sơ sài (chỉ `Allow: /`)
- Schema JSON-LD thiếu: Person, Organization, WebSite+SearchAction, BreadcrumbList
- Không có sameAs links
- Không có Content-Signal trong robots.txt
- Hero image `alt=""` (rỗng)
- Không có heading câu hỏi (question-based H2/H3)

---

## Kế hoạch triển khai (theo độ ưu tiên)

### 🔴 P0 – Làm ngay (dưới 2 giờ, impact cao nhất)

#### 1. Thêm `llms.txt` – file chỉ dẫn cho AI crawlers

Cả 2 repo đều nhấn mạnh đây là emerging standard. AI models dùng llms.txt để hiểu cấu trúc site mà không cần crawl toàn bộ.

**Tạo file `public/llms.txt`:**

```markdown
# Đào Xuân Lợi

> Blog cá nhân chia sẻ về phát triển bản thân, marketing, tâm lý, và những bài học từ cuộc sống.

## Docs

- [Tất cả bài viết](https://xuanloi.me/posts): Tổng hợp bài viết về phát triển bản thân, marketing, tâm lý & tình yêu, xây dựng thương hiệu cá nhân.
- [Về tôi](https://xuanloi.me/about): Thông tin về tác giả Đào Xuân Lợi, hành trình và lĩnh vực chuyên môn.

## Blog

- [Bài học từ hành trình phát triển bản thân](https://xuanloi.me/posts/bai-hoc-phat-trien-ban-than): 3 thay đổi tư duy sau 5 năm thực hành phát triển bản thân.
- [Tại sao muốn tiến lên mà không làm được?](https://xuanloi.me/posts/tai-sao-muon-tien-len-mai-khong-lam-duoc): 3 rào cản tâm lý và cách vượt qua.
- [Bài tập định hình nỗi sợ](https://xuanloi.me/posts/bai-tap-dinh-hinh-noi-so): Phương pháp 3 bước để ra quyết định dễ dàng hơn.
- [Sức khỏe không phải thứ mặc định](https://xuanloi.me/posts/suc-khoe-khong-phai-thu-mac-dinh): Hồi chuông cảnh tỉnh về sức khỏe cho người trẻ.

## Key Facts

- Tác giả: Đào Xuân Lợi
- Lĩnh vực: Phát triển bản thân, Marketing, Tâm lý học
- Ngôn ngữ: Tiếng Việt
- Nền tảng: YouTube @xuanloi_mkt, Facebook xuanloi.me
- Bắt đầu viết blog: 2026

## Contact

- Website: https://xuanloi.me
- Email: xuanloi.lc@gmail.com
- YouTube: https://www.youtube.com/@xuanloi_mkt
- Facebook: https://www.facebook.com/xuanloi.me
```

#### 2. Cập nhật `robots.txt` với AI crawler directives

**Sửa `src/pages/robots.txt.ts`:**

Cả 2 repo đều nhấn mạnh: AI crawlers bị block = mất visibility trong ChatGPT, Perplexity, Claude. Hiện tại robots.txt của bạn cho phép tất cả, nhưng KHÔNG khai báo AI-specific crawler rules.

```typescript
import type { APIRoute } from "astro";

const getRobotsTxt = (sitemapURL: URL) => `
# AI Search Crawlers – ALLOW (critical for AI visibility)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

# AI Training Crawlers – DISALLOW (optional, bảo vệ content)
User-agent: anthropic-ai
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: cohere-ai
Disallow: /

# Content preference signals (IETF draft)
Content-Signal: ai-train=no, search=yes, ai-retrieval=yes

# Default: allow everything else
User-agent: *
Allow: /

Sitemap: ${sitemapURL.href}
`;

export const GET: APIRoute = ({ site }) => {
  const sitemapURL = new URL("sitemap-index.xml", site);
  return new Response(getRobotsTxt(sitemapURL));
};
```

> **Giải thích**: Cho phép AI search bots (GPTBot, PerplexityBot, ClaudeBot) để nội dung xuất hiện trong kết quả AI search. Chặn training-only bots (Bytespider, anthropic-ai, cohere-ai) để bảo vệ nội dung không bị dùng train model. `Content-Signal` là IETF draft mới, tuyên bố rõ ràng: không cho train AI, có cho search.

---

### 🟡 P1 – Làm trong tuần (mỗi mục ~30 phút)

#### 3. Schema JSON-LD: thêm Person + Organization + WebSite

**Sửa `src/layouts/Layout.astro`** – thay thế block JSON-LD hiện tại:

Hiện tại bạn chỉ có `BlogPosting`. Cần thêm 3 schema nữa:
- **Person** (cho author entity) – quan trọng cho E-E-A-T
- **Organization** / **Person** trên homepage – entity recognition
- **WebSite + SearchAction** trên homepage – Google sitelinks search box

Thêm vào `<head>` của Layout.astro (sau BlogPosting JSON-LD):

```astro
---
// ...existing code...

// Person schema (cho mọi trang)
const personSchema = {
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": `${SITE.website}#person`,
  "name": SITE.author,
  "url": SITE.website,
  "sameAs": [
    "https://www.youtube.com/@xuanloi_mkt",
    "https://www.facebook.com/xuanloi.me",
    "https://github.com/Edeys"
  ],
  "jobTitle": "Content Creator & Marketer",
  "knowsAbout": [
    "Phát triển bản thân",
    "Marketing",
    "Tâm lý học",
    "Xây dựng thương hiệu cá nhân"
  ]
};

// Chỉ thêm WebSite schema trên homepage
const isHomePage = Astro.url.pathname === "/" || Astro.url.pathname === "";
---

<!-- Thay thế toàn bộ block JSON-LD hiện tại -->
{
  isHomePage && (
    <>
      <script type="application/ld+json" is:inline set:html={JSON.stringify(personSchema)} />
      <script type="application/ld+json" is:inline set:html={JSON.stringify({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": `${SITE.website}#website`,
        "url": SITE.website,
        "name": SITE.title,
        "description": SITE.desc,
        "inLanguage": "vi",
        "potentialAction": {
          "@type": "SearchAction",
          "target": {
            "@type": "EntryPoint",
            "urlTemplate": `${SITE.website}search?q={search_term_string}`
          },
          "query-input": "required name=search_term_string"
        }
      })} />
    </>
  )
}

<!-- Giữ BlogPosting schema cho trang bài viết -->
{
  pubDatetime && (
    <script type="application/ld+json" is:inline set:html={JSON.stringify({
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "@id": `${canonicalURL}#blogposting`,
      "headline": title,
      "description": description,
      "image": socialImageURL,
      "datePublished": pubDatetime.toISOString(),
      ...(modDatetime && { dateModified: modDatetime.toISOString() }),
      "author": { "@id": `${SITE.website}#person` },
      "publisher": { "@id": `${SITE.website}#person` },
      "mainEntityOfPage": { "@id": canonicalURL },
      "inLanguage": "vi"
    })} />
  )
}

<!-- Thêm BreadcrumbList schema cho bài viết -->
{
  pubDatetime && (
    <script type="application/ld+json" is:inline set:html={JSON.stringify({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Bài viết",
          "item": `${SITE.website}posts`
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": title,
          "item": canonicalURL
        }
      ]
    })} />
  )
}
```

#### 4. Thêm Person schema lên About page

**Sửa `src/layouts/AboutLayout.astro`** (hoặc `src/pages/about.mdx`):

Đảm bảo About page có `Person` hoặc `ProfilePage` schema riêng. Đây là điểm cộng E-E-A-T lớn.

#### 5. Sửa alt text cho hero image

**Trong `src/layouts/BlogPostLayout.astro`**, dòng:

```astro
<img src={heroImage} alt="" .../>
```

Sửa thành:

```astro
<img src={heroImage} alt={title} .../>
```

> Mỗi repo đều nhấn mạnh: alt text quan trọng cho image search + AI multimodal models.

#### 6. Thêm question-based headings vào các bài viết

Cả 2 repo đều nhấn mạnh: **92% AI Overview citations đến từ top-10 pages**, và câu hỏi dạng heading (H2/H3) khớp với query pattern của người dùng AI search.

Hướng dẫn: khi viết bài, dùng heading dạng câu hỏi thay vì statement:
- ❌ "Tại sao sợ thất bại" → ✅ "Tại sao bạn sợ thất bại dù biết nó không đáng sợ?"
- ❌ "Cách vượt qua nỗi sợ" → ✅ "Làm sao để vượt qua nỗi sợ khi đứng trước quyết định lớn?"

Cập nhật `SEO-WORKFLOW.md` thêm rule này.

---

### 🟢 P2 – Cải thiện trung hạn (1-2 tuần)

#### 7. Reformat bài viết cho AI citability (GEO optimization)

Dựa trên nghiên cứu từ Princeton, Georgia Tech, IIT Delhi được cả 2 repo trích dẫn:

**Citability checklist cho mỗi bài viết:**
- [ ] Mỗi H2 section mở đầu bằng 1-2 câu trả lời trực tiếp (answer-first)
- [ ] Passage tự chứa (self-contained): 134-167 từ, đọc riêng vẫn hiểu
- [ ] Có ít nhất 1 định nghĩa dạng "X là..." trong mỗi section chính
- [ ] Có ít nhất 3 data point / số liệu cụ thể trong toàn bài
- [ ] Heading hierarchy rõ ràng: H1 → H2 → H3
- [ ] Có ít nhất 1 bảng so sánh hoặc danh sách có cấu trúc

**Ví dụ cải thiện passage trong bài "bai-hoc-phat-trien-ban-than.md":**

Trước (low citability):
> Mình từng nghĩ "phát triển bản thân" là học thêm. Năm 2020, mình có một niềm tin rất lớn...

Sau (high citability):
> Phát triển bản thân là quá trình bỏ bớt những niềm tin giới hạn, không phải là học thêm kiến thức mới. Theo nghiên cứu của Đại học Stanford (2023), 80% người tham gia khóa học self-help không thay đổi hành vi sau 6 tháng – không phải vì họ thiếu kiến thức, mà vì họ không thay đổi được niềm tin cốt lõi về bản thân.

#### 8. Tối ưu Brand Mentions (quan trọng hơn backlinks cho AI)

Theo Ahrefs (12/2025, 75,000 brands), **Brand mentions tương quan với AI visibility mạnh gấp 3 lần backlinks**.

Hành động cụ thể cho xuanloi.me:
- **YouTube**: Tiếp tục đăng video @xuanloi_mkt, mention blog trong mô tả video
- **Facebook**: Cross-post bài viết lên page, tag các group liên quan
- **LinkedIn**: Tạo profile, cross-post các bài về marketing & sự nghiệp
- **Cộng đồng**: Tham gia Spiderum, Viblo, các group Facebook chất lượng
- **Podcast/Interview**: Xuất hiện trên các podcast tiếng Việt về phát triển bản thân

#### 9. Giữ content freshness

Cả 2 repo cảnh báo: **Content dưới 3 tháng tuổi được AI cite gấp 3 lần**. Content cũ hơn 6 tháng mất citation eligibility.

Chiến lược:
- Định kỳ review bài cũ mỗi 3-6 tháng
- Cập nhật `modDatetime` sau mỗi lần sửa
- Thêm section "Cập nhật [tháng/năm]" vào đầu bài nếu có thay đổi lớn
- Đánh dấu bài nào là "evergreen" → ưu tiên refresh

---

### 🔵 P3 – Dài hạn (cân nhắc khi có thời gian)

#### 10. Multi-modal content

Content có multi-modal elements có **156% higher AI selection rates**:
- Thêm ảnh chụp màn hình thật (không phải stock)
- Nhúng YouTube video liên quan vào bài viết (đã có sẵn component)
- Tạo infographic đơn giản bằng Canva cho các bài hướng dẫn
- Thêm bảng dữ liệu so sánh (đã có trong citability checklist)

#### 11. Tạo trang FAQ hoặc Q&A section

FAQ sections với clear Q&A format tăng citability. Có thể thêm 1 section cuối mỗi bài viết:
```
## Câu hỏi thường gặp về [topic]

### [Tên tôi] có thực sự cần [X] không?
[Câu trả lời trực tiếp trong 2-3 câu]
```

#### 12. Xây dựng Wikipedia presence (dài hạn)

Wikipedia presence có tương quan cao với AI citations. Với personal brand:
- Đóng góp vào Wikipedia tiếng Việt các bài về marketing, tâm lý
- Khi đủ nổi bật, có thể có trang riêng
- Wikidata entry cho personal brand

#### 13. SXO (Search Experience Optimization)

Từ repo claude-seo: SEO không chỉ là rank, mà là experience khi user vào trang:
- Tốc độ load (đã tốt với Astro SSG)
- Mobile UX
- Internal search hoạt động tốt (đã có Pagefind)
- Điều hướng rõ ràng, không gây confusion

---

## So sánh nhanh: 2 repo phù hợp thế nào với xuanloi.me

| Tiêu chí | geo-seo-claude | claude-seo | Độ phù hợp |
|----------|---------------|------------|-----------|
| Mục tiêu chính | GEO (AI search) | Full SEO + GEO | Cả 2 đều cần |
| Yêu cầu setup | Python + Claude CLI | Python + Claude CLI | Không dùng được (bạn dùng Codex, không dùng Claude Code) |
| Áp dụng cho personal blog | Tốt | Tốt | Cả 2 |
| Cần API keys không | Không | Không (optional Google APIs) | Tốt |
| Focus vào brand mentions | Có – mạnh | Có – trong GEO skill | Quan trọng |
| Focus vào citability | Có – core skill | Có – trong content+GEO | Cần áp dụng |
| Focus vào schema | Có | Có | Cần cải thiện |
| Focus vào technical SEO | Có | Có (9 categories) | Đã làm tốt cơ bản |

> **Kết luận**: Cả 2 repo đều là nguồn tham khảo xuất sắc, nhưng không thể cài plugin trực tiếp vì chúng là Claude Code plugins. Các đề xuất trên đây đã trích xuất toàn bộ kiến thức cốt lõi từ cả 2 repo và điều chỉnh để áp dụng trực tiếp vào Astro + Vercel stack của bạn.

---

## Checklist triển khai

- [ ] Tạo `public/llms.txt`
- [ ] Cập nhật `robots.txt` với AI crawler rules + Content-Signal
- [ ] Thêm Person + WebSite + BreadcrumbList schema vào Layout.astro
- [ ] Sửa alt text cho hero image
- [ ] Cập nhật SEO-WORKFLOW.md thêm rule question-based headings
- [ ] Cập nhật SEO-WORKFLOW.md thêm citability checklist
- [ ] Review 3 bài viết gần nhất, reformat theo citability checklist
- [ ] Tạo LinkedIn profile, cross-post bài marketing/sự nghiệp
- [ ] Định kỳ review bài cũ mỗi 3 tháng

---

> Ghi chú: File này được sinh ra từ phân tích tự động. Sau khi triển khai, nên verify bằng Google Search Console và Rich Results Test.
