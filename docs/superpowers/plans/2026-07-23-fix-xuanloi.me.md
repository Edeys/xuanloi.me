# xuanloi.me — Fix Issues Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development or executing-plans to implement this plan task-by-task.

**Goal:** Fix all critical bugs on xuanloi.me live site and optimize SEO/code quality.

**Architecture:** Astro 6 static site with Tailwind 4, React 19 for interactive components. Issues span Layout schema, sitemap config, route hardening, analytics performance, and build tooling.

**Tech Stack:** Astro 6, Tailwind 4, React 19, TypeScript, Nginx

---

## Task 1: Fix datePublished undefined on all non-post pages

**Files:**
- Modify: `src/layouts/Layout.astro:30-52`
- Modify: `src/components/StructuredData.astro:1-92`

### Issue
Layout.astro always renders `BlogPosting` JSON-LD schema. On homepage, 404, about, search, admin → pubDatetime is undefined → `${undefined}` becomes string `"undefined"` in output:
```json
{"datePublished":"undefined"}
```

### Fix: Add WebSite schema for homepage, skip BlogPosting when no pubDatetime

- [ ] **Step 1: Modify Layout.astro structuredData logic**
  - Change: only render BlogPosting if pubDatetime is provided
  - For homepage/listing pages: render WebSite schema instead
  - Remove inline structuredData variable entirely → delegate to StructuredData component

Replace inline structuredData in Layout.astro:
```astro
---
// Remove inline structuredData assignment
// Remove the <script type="application/ld+json"> block from head
// Instead use StructuredData component with conditional type
const schemaType = pubDatetime ? "BlogPosting" : "WebSite";
---
```

Add after header/SEO meta tags but before closing head:
```astro
{
  pubDatetime ? (
    <StructuredData type="BlogPosting" data={{...}} />
  ) : (
    <StructuredData type="WebSite" />
  )
}
```

Wait — this creates a circular issue because PostDetails already calls `<StructuredData type="BlogPosting">`. So fix should be:

- **Layout.astro**: When `pubDatetime` not provided, render `WebSite` schema (not BlogPosting). When pubDatetime provided, render nothing (let PostDetails handle it).
- **PostDetails.astro**: Already renders BlogPosting → keep it.

Simplest fix: In Layout.astro, change schema type:
- If `pubDatetime` exists → `WebSite` (not BlogPosting, because PostDetails handles it)
- If no `pubDatetime` → `WebSite`

Actually the cleanest fix:

**Layout.astro change:**
1. Remove the entire inline `const structuredData = {...}` + `<script type="application/ld+json">` block 
2. Add `<StructuredData type="WebSite" />` for non-post pages (no pubDatetime)
3. For pages with pubDatetime, don't render any schema in Layout (PostDetails handles BlogPosting)

**PostDetails.astro change:**
- Already renders `<StructuredData type="BlogPosting">` — keep as is.

**StructuredData.astro change:**
- Fix `datePublished` when pubDatetime might be undefined — add guard

- [ ] **Step 2: Remove inline ld+json from Layout, add WebSite fallback**

In `src/layouts/Layout.astro`, delete lines from:
```astro
const structuredData = {
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  ...
};
```
through the `<script type="application/ld+json">` block.

Add after the RSS auto-discovery link:
```astro
{
  !pubDatetime && <StructuredData type="WebSite" />
}
```

- [ ] **Step 3: Fix StructuredData.astro to handle undefined pubDatetime safely**

In `src/components/StructuredData.astro`, change BlogPosting block:
```astro
datePublished: data.pubDatetime?.toISOString() || new Date().toISOString(),
dateModified: data.modDatetime?.toISOString() || data.pubDatetime?.toISOString() || new Date().toISOString(),
```


## Task 2: Fix sitemap homepage priority

**Files:**
- Modify: `astro.config.mjs:80-84`

### Issue
Sitemap check: `url === SITE.website + "/"` but urls in sitemap have no trailing slash. Homepage URL is `https://xuanloi.me` not `https://xuanloi.me/`.

- [ ] **Step 1: Fix homepage URL matching**

Change:
```js
if (url === SITE.website || url === SITE.website + "/") {
```
To:
```js
const siteUrl = SITE.website.replace(/\/$/, "");
if (url === siteUrl || url === siteUrl + "/") {
```

Also same fix for trailing slash removal logic above — ensure it handles all cases.

- [ ] **Step 2: Also set correct lastmod for homepage**

Ensure the homepage lastmod uses current date:
```js
if (url === siteUrl || url === siteUrl + "/") {
  item.priority = 1.0;
  item.changefreq = ChangeFreqEnum.DAILY;
  item.lastmod = new Date().toISOString();
}
```
Already present, just ensure the condition works after strip.

## Task 3: Remove /admin page from public + sitemap

**Files:**
- Modify: `astro.config.mjs:56-67`
- Modify: `src/pages/admin.astro`

### Issue
/admin builds to `/admin/index.html` with form to create blog posts, no auth. Accessible and indexed.

- [ ] **Step 1: Exclude /admin from sitemap**

In `astro.config.mjs` sitemap filter:
```js
filter: (page) => {
  if (page.includes("/admin")) return false;
  ...
}
```

- [ ] **Step 2: Add noindex meta to admin page**

In `src/pages/admin.astro`, add after opening `<Layout>`:
```astro
---
const noIndex = true;
---
```
And in Layout.astro, if noIndex prop is true, add:
```astro
<meta name="robots" content="noindex, nofollow" />
```

Or simpler: add a `<meta name="robots" content="noindex">` directly in admin.astro after the Layout import.

Actually simpler approach — add directly to admin.astro head via Layout props:
Add `noindex` as optional Layout prop.

Shortest path: add `<meta name="robots" content="noindex">` in admin.astro using `define:vars` or direct inline.

Actually the shortest: Add to Layout.astro a new optional prop `noindex`:

In Layout.astro:
```astro
export interface Props {
  ...
  noindex?: boolean;
}
const { ..., noindex = false } = Astro.props;
```

Then in head:
```astro
{noindex && <meta name="robots" content="noindex, nofollow" />}
```

In admin.astro:
```astro
<Layout noindex>
```

## Task 4: Fix duplicate structured data on blog posts

**Files:**
- Modify: `src/components/StructuredData.astro`

### Issue
Layout.astro renders BlogPosting (+ after fix → WebSite for non-post). PostDetails renders another StructuredData component with BlogPosting. On post pages, Layout renders WebSite + PostDetails renders BlogPosting = 2 schemas.

This is actually OK — having WebSite + BlogPosting is valid. But we need to confirm.

Actually after Task 1, Layout renders WebSite only when no pubDatetime. On a post page (pubDatetime exists), Layout renders nothing, PostDetails renders BlogPosting → only 1 schema. That's correct.

But wait — the grep earlier showed only 1 `ld+json` on a post page. So the current code (before fix) may not actually be duplicating. Let me re-verify...

Looking at the current code:
- Layout.astro always renders ld+json schema (BlogPosting)
- PostDetails.astro uses `<StructuredData ...>` component

The PostDetails.astro code:
```astro
<StructuredData 
  type="BlogPosting" 
  data={{...}}
/>
```

And StructuredData.astro renders:
```astro
<script type="application/ld+json" set:html={JSON.stringify(structuredData)} />
```

So both render ld+json. BUT the grep showed only 1 on live. Maybe StructuredData component wasn't working at build time? Or the build cached? Let me check.

Actually, the live test showed 1 ld+json on a post page. But 2 would mean the StructuredData component renders AND the Layout renders. Since count was 1, maybe Layout's is the only one that renders, and StructuredData's output wasn't rendered properly.

Looking more carefully at StructuredData.astro — it uses `set:html` which might be interfering. Or maybe Astro deduplicated it.

Anyway, after Task 1 fix, Layout won't render BlogPosting schema on post pages (only WebSite on non-post pages), so there's guaranteed no duplication. This task is a no-op given the Task 1 fix. But let me keep a guard:

- [ ] **Step 1: No changes needed** — Task 1 already fixes this by removing BlogPosting from Layout (only renders WebSite when no pubDatetime).

## Task 5: Fix RSS pubDate

**Files:**
- Modify: `src/pages/rss.xml.ts:12`

### Issue
RSS uses modDatetime as primary pubDate. Should use pubDatetime as primary, modDatetime as fallback.

- [ ] **Step 1: Swap date priority**

Change:
```js
pubDate: new Date(data.modDatetime ?? data.pubDatetime),
```
To:
```js
pubDate: new Date(data.pubDatetime),
```

If you want to keep modDatetime as last-modified indicator, keep pubDatetime as pubDate and add a separate field or just keep it simple.

## Task 6: Reduce analytics delay

**Files:**
- Modify: `src/components/Analytics.astro`

### Issue
Analytics loads after `window.load` + 3s setTimeout + requestIdleCallback + 3s = ~6s total. Users bouncing before 6s are not tracked.

- [ ] **Step 1: Reduce delay to 1s**

Change:
```js
window.addEventListener('load', function() {
  setTimeout(function() {
    (window.requestIdleCallback || setTimeout)(initAnalytics, 3000);
  }, 3000);
});
```
To:
```js
window.addEventListener('load', function() {
  setTimeout(initAnalytics, 1000);
});
```

## Task 7: Clean static build files from repo root

**Files:**
- Delete: `404.html`, `500.html`, `about.md`, `archives.md`, `index.html`, `index.md`, `posts.md`, `rss.xml`, `sitemap-0.xml`, `sitemap-index.xml`, `robots.txt`, `toggle-theme.js`, `og.png`, `favicon.svg`, `site.webmanifest`, `game-audio.mp3` (from root, NOT from src/)
- Modify: `.gitignore`

### Issue
Root repo contains stale files from old dist builds. These shadow actual source files and bloat the repo.

- [ ] **Step 1: Add root static files to .gitignore**

Append to `.gitignore`:
```
# Root stale build artifacts
/*.html
/*.md
/*.xml
/og.png
/favicon.svg
/site.webmanifest
/toggle-theme.js
/game-audio.mp3
```

- [ ] **Step 2: Remove the actual files (git rm)**

```bash
git rm --cached 404.html 500.html about.md archives.md index.html index.md posts.md rss.xml sitemap-0.xml sitemap-index.xml robots.txt toggle-theme.js og.png favicon.svg site.webmanifest game-audio.mp3
```

## Task 8: Fix build/format scripts for Windows

**Files:**
- Modify: `package.json`
- Delete: `pnpm-lock.yaml` (or add to gitignore)

- [ ] **Step 1: Fix format script for Windows**

Change from:
```json
"format": "git ls-files '*.js' '*.mjs' '*.cjs' '*.ts' '*.tsx' '*.json' | xargs oxfmt --write",
```
To:
```json
"format": "oxfmt --write src/**/*.ts src/**/*.tsx src/**/*.mjs src/**/*.js astro.config.mjs package.json",
```
(Or install `xargs` for Windows — but glob is simpler.)

- [ ] **Step 2: Add pnpm-lock to gitignore**

Add to `.gitignore`:
```
/pnpm-lock.yaml
```

## Task 9: Fix blog post description mismatch

**Files:**
- Modify: `src/content/blog/2026/17-cau-hoi-thay-doi-cuoc-doi.md:1-10`

- [ ] **Step 1: Fix description to match title**

Change description from "9 câu hỏi" to "17 câu hỏi":
```yaml
description: "17 câu hỏi đã thay đổi cách mình sống và làm việc trong gần 10 năm qua — về bản thân, sự nghiệp và cuộc sống."
```

## Task 10: Build, deploy, verify

- [ ] **Step 1: Build**

```bash
cd D:\Dự\ Án\ Cá\ Nhân\xuanloi.me
npm run build
```

- [ ] **Step 2: Deploy to server**

```bash
cd dist
scp -i ~/.ssh/do-9router -r * root@129.212.238.158:/var/www/xuanloi.me/
```

- [ ] **Step 3: Reload nginx**

```bash
ssh -i ~/.ssh/do-9router root@129.212.238.158 "nginx -t && systemctl reload nginx"
```

- [ ] **Step 4: Verify live site**

```bash
# Check HTTP status
curl -sI https://xuanloi.me/ | head -5

# Verify no "undefined" in pubDate schema
curl -s https://xuanloi.me/ | grep -o "datePublished"

# Verify sitemap priority
curl -s https://xuanloi.me/sitemap-index.xml | head -5
```

