import type { APIRoute } from "astro";

export const GET: APIRoute = async () => {
  const markdownContent = `# Đào Xuân Lợi

Chia sẻ về cuộc sống, marketing và những điều tôi học được trên hành trình của mình.

## Điều hướng

- [Về tôi](/about.md)
- [Bài viết mới](/posts.md)
- [RSS Feed](/rss.xml)

## Liên kết

- YouTube: [@xuanloi_mkt](https://www.youtube.com/@xuanloi_mkt)
- GitHub: [@Edeys](https://github.com/Edeys)
- Email: xuanloi.lc@gmail.com

---

*Đây là phiên bản markdown của xuanloi.me. Truy cập [xuanloi.me](https://xuanloi.me) để trải nghiệm đầy đủ.*`;

  return new Response(markdownContent, {
    status: 200,
    headers: {
      "Content-Type": "text/markdown; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
};
