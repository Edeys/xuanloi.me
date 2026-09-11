import type { APIRoute } from "astro";

const getRobotsTxt = (sitemapURL: URL) => `
# AI Search Crawlers — ALLOW (critical for AI search visibility)
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

# Common Crawl — ALLOW (powers open web datasets)
User-agent: CCBot
Allow: /

# AI Training Crawlers — ALLOW (opt-in to AI model training)
User-agent: anthropic-ai
Allow: /

User-agent: Bytespider
Allow: /

User-agent: cohere-ai
Allow: /

# Content Preference Signals (IETF draft)
Content-Signal: ai-train=yes, search=yes, ai-retrieval=yes

# Default: allow all other crawlers
User-agent: *
Allow: /
Disallow: /admin
Disallow: /search
Disallow: /api/
Disallow: /thank-you

Sitemap: ${sitemapURL.href}
`;

export const GET: APIRoute = ({ site }) => {
  const sitemapURL = new URL("sitemap-index.xml", site);
  return new Response(getRobotsTxt(sitemapURL));
};
