#!/usr/bin/env python3
"""Fix all remaining tasks 2-8 in one pass."""
import os

base = r'D:\Dự Án Cá Nhân\xuanloi.me'

# TASK 2: Fix sitemap homepage priority (trailing slash)
astro_config = os.path.join(base, 'src\..', 'astro.config.mjs')
# Actually let me just use the right path
astro_config = r'D:\Dự Án Cá Nhân\xuanloi.me\astro.config.mjs'

with open(astro_config, 'r', encoding='utf-8') as f:
    cfg = f.read()

# Fix: strip trailing slash from SITE.website in sitemap logic
old_check = "if (url === SITE.website || url === SITE.website + \"/\")"
new_check = "if (url === SITE.website.replace(/\\/$/, \"\") || url === SITE.website.replace(/\\/$/, \"\") + \"/\")"
cfg = cfg.replace(old_check, new_check)

# TASK 3: Exclude /admin from sitemap
old_filter = '# Always exclude archives if not showing them'
new_filter_add = '# Always exclude admin pages\n        if (page.includes(\"/admin\")) return false;\n\n        ' + old_filter
cfg = cfg.replace(old_filter, new_filter_add)

with open(astro_config, 'w', encoding='utf-8') as f:
    f.write(cfg)

print('TASK 2-3 done: sitemap fixed')

# TASK 3b: Add noindex to admin page
admin_page = os.path.join(base, 'src', 'pages', 'admin.astro')
with open(admin_page, 'r', encoding='utf-8') as f:
    admin = f.read()

# Add noindex meta after Layout opening
admin = admin.replace(
    '<Layout>',
    '<Layout>\n  <Fragment slot="head">\n    <meta name="robots" content="noindex, nofollow" />\n  </Fragment>'
)

with open(admin_page, 'w', encoding='utf-8') as f:
    f.write(admin)

print('TASK 3b done: admin noindex added')

# TASK 4: Fix RSS pubDate
rss_file = os.path.join(base, 'src', 'pages', 'rss.xml.ts')
with open(rss_file, 'r', encoding='utf-8') as f:
    rss = f.read()

rss = rss.replace(
    'new Date(data.modDatetime ?? data.pubDatetime)',
    'new Date(data.pubDatetime)'
)

with open(rss_file, 'w', encoding='utf-8') as f:
    f.write(rss)

print('TASK 4 done: RSS pubDate fixed')

# TASK 5: Fix analytics delay
analytics_file = os.path.join(base, 'src', 'components', 'Analytics.astro')
with open(analytics_file, 'r', encoding='utf-8') as f:
    analytics = f.read()

old_delay = """  window.addEventListener('load', function() {
    setTimeout(function() {
      (window.requestIdleCallback || setTimeout)(initAnalytics, 3000);
    }, 3000);
  });"""
new_delay = """  window.addEventListener('load', function() {
    setTimeout(initAnalytics, 1000);
  });"""
analytics = analytics.replace(old_delay, new_delay)

with open(analytics_file, 'w', encoding='utf-8') as f:
    f.write(analytics)

print('TASK 5 done: analytics delay reduced')

# TASK 6: Clean root static files from git and add to gitignore
gitignore = os.path.join(base, '.gitignore')
with open(gitignore, 'r', encoding='utf-8') as f:
    gi = f.read()

new_entries = """
# Root stale build artifacts (local only - these are dups from dist)
/404.html
/500.html
/about.md
/archives.md
/index.html
/index.md
/posts.md
/rss.xml
/sitemap-0.xml
/sitemap-index.xml
/robots.txt
/toggle-theme.js
/og.png
/favicon.svg
/site.webmanifest
/game-audio.mp3
"""
if '/404.html' not in gi:
    gi += new_entries

with open(gitignore, 'w', encoding='utf-8') as f:
    f.write(gi)

print('TASK 6 done: gitignore updated')

# TASK 7: Fix format script for Windows
pkg_file = os.path.join(base, 'package.json')
with open(pkg_file, 'r', encoding='utf-8') as f:
    pkg = f.read()

old_format = '"format": "git ls-files \'*.js\' \'*.mjs\' \'*.cjs\' \'*.ts\' \'*.tsx\' \'*.json\' | xargs oxfmt --write",'
new_format = '"format": "oxfmt --write \\"src/**/*.ts\\" \\"src/**/*.tsx\\" \\"src/**/*.mjs\\" \\"src/**/*.js\\" astro.config.mjs package.json",'
old_format_check = '"format:check": "git ls-files \'*.js\' \'*.mjs\' \'*.cjs\' \'*.ts\' \'*.tsx\' \'*.json\' | xargs oxfmt --check",'
new_format_check = '"format:check": "oxfmt --check \\"src/**/*.ts\\" \\"src/**/*.tsx\\" \\"src/**/*.mjs\\" \\"src/**/*.js\\" astro.config.mjs package.json",'

pkg = pkg.replace(old_format, new_format)
pkg = pkg.replace(old_format_check, new_format_check)

with open(pkg_file, 'w', encoding='utf-8') as f:
    f.write(pkg)

print('TASK 7 done: format script fixed')

# TASK 8: Fix blog post description mismatch
post_file = os.path.join(base, 'src', 'content', 'blog', '2026', '17-cau-hoi-thay-doi-cuoc-doi.md')
with open(post_file, 'r', encoding='utf-8') as f:
    post = f.read()

post = post.replace(
    'description: "9 câu hỏi đã thay đổi cách mình sống và làm việc trong gần 10 năm qua — về bản thân, sự nghiệp và cuộc sống."',
    'description: "17 câu hỏi đã thay đổi cách mình sống và làm việc trong gần 10 năm qua — về bản thân, sự nghiệp và cuộc sống."'
)

with open(post_file, 'w', encoding='utf-8') as f:
    f.write(post)

print('TASK 8 done: blog description fixed')
print('ALL TASKS 2-8 COMPLETE')
