import { getCollection } from "astro:content";
import type { APIRoute } from "astro";
import getSortedPosts from "@/utils/getSortedPosts";

export const GET: APIRoute = async () => {
  const posts = await getCollection("blog");
  const sortedPosts = getSortedPosts(posts);

  let markdownContent = `# Lưu trữ\n\n`;
  markdownContent += `Tổng số bài viết: ${sortedPosts.length}\n\n`;

  // Group posts by year
  const postsByYear = sortedPosts.reduce(
    (acc, post) => {
      const year = post.data.pubDatetime.getFullYear();
      if (!acc[year]) acc[year] = [];
      acc[year].push(post);
      return acc;
    },
    {} as Record<number, typeof sortedPosts>,
  );

  // Sort years descending
  const years = Object.keys(postsByYear).sort((a, b) => Number(b) - Number(a));

  markdownContent += `## Bài viết theo năm\n\n`;

  for (const year of years) {
    const count = postsByYear[Number(year)].length;
    markdownContent += `- [${year}](/posts.md#${year}) (${count} bài${count !== 1 ? "" : ""})\n`;
  }

  markdownContent += `\n---\n\n[Quay lại trang chủ](/index.md) | [Tất cả bài viết](/posts.md)`;

  return new Response(markdownContent, {
    status: 200,
    headers: {
      "Content-Type": "text/markdown; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
};
