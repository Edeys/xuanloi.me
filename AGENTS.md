# AGENTS.md
## New Blog Post Workflow
- If user says “new blog post” without topic/title: ask for topic/title first.
- Pick branch name: short slug from topic/title.
- Scaffold file: `src/content/blog/<year>/<slug>.md`.
- Frontmatter: only set `title` from user input; keep required placeholders minimal (`description: "TBD"`, `draft: true`, `pubDatetime: <today>`).
- No body content; no invented outline.
- Open editor: `code <new-post-path>`.

---

## Deploy Website (xuanloi.me)

Site deployed to DNCloud CP-2 hosting (103.116.38.9, cPanel). No SSH — FTP only.

### Auto deploy (after code changes)
```bash
npm run deploy
```
Or: `python scripts/deploy.py`

### How it works
1. `npm run build` → `dist/`
2. Create ZIP of new content (skip unchanged images)
3. Upload ZIP + PHP extractor via FTP
4. PHP auto-extracts, deletes old `.prerender` + `_astro` cache, self-destructs
5. Verify `llms.txt` and `robots.txt` live

### Manual deploy
```bash
npm run build
# Then upload dist/* to /public_html via FileZilla or cPanel File Manager
```

### Hosting details
- IP: 103.116.38.9
- cPanel: https://vn9.dncloud.net:2083/ (ktixknjc)
- Root: `/public_html/`
- Site runs Astro SSR via Node.js hosted on LiteSpeed
- After deploy, restart Node.js via cPanel → Setup Node.js App → Restart
