import subprocess, re, sys

ssh = ['ssh', '-i', r'C:\Users\xuanl\.ssh\do-9router', 'root@129.212.238.158']

def run_ssh(cmd):
    p = subprocess.run(ssh + [cmd], capture_output=True, timeout=30)
    stdout = p.stdout.decode('utf-8', errors='replace').strip()
    stderr = p.stderr.decode('utf-8', errors='replace').strip()
    return stdout, stderr, p.returncode

print('=== AFTER FIX VERIFICATION ===')
print()

# 1. Homepage schema
out, _, _ = run_ssh('curl -s https://xuanloi.me/')
m = re.search(r'@type":"(WebSite|BlogPosting|Person)"', out)
print(f'1. Homepage @type: {m.group(1) if m else "MISSING"}')

# 2. datePublished count
print(f'2. datePublished on homepage count: {out.count("datePublished")}')

# 3. /admin in sitemap
out, _, _ = run_ssh('curl -s https://xuanloi.me/sitemap-0.xml')
print(f'3. /admin in sitemap count: {out.count("/admin")}')

# 4. /admin noindex
out, _, _ = run_ssh('curl -s https://xuanloi.me/admin/')
print(f'4. /admin noindex count: {out.count("noindex")}')

# 5. Homepage sitemap priority
out, _, _ = run_ssh('curl -s https://xuanloi.me/sitemap-0.xml')
m = re.search(r'<loc>https://xuanloi.me</loc><changefreq>([^<]+)</changefreq><priority>([^<]+)</priority>', out)
if m:
    print(f'5. Homepage priority: changefreq={m.group(1)} priority={m.group(2)}')
else:
    print(f'5. Homepage priority: PATTERN NOT MATCHED')

# 6. RSS pubDate
out, _, _ = run_ssh('curl -s https://xuanloi.me/rss.xml')
dates = re.findall(r'<pubDate>([^<]+)', out)[:3]
print(f'6. RSS pubDates: {dates}')

# 7. Old broken URL
out, _, _ = run_ssh('curl -sI https://xuanloi.me/posts/bai-hoc-phat-trien-ban-than/')
m = re.match(r'HTTP/[\d.]+\s+(\d+)', out)
print(f'7. Old path HTTP status: {m.group(1) if m else "NONE"}')

# 8. Post page schema
out, _, _ = run_ssh('curl -s https://xuanloi.me/posts/17-cau-hoi-thay-doi-cuoc-doi/')
m = re.search(r'datePublished":"([^"]+)', out)
print(f'8. Post datePublished: {m.group(1) if m else "MISSING"}')

# 9. Structured data count on post
print(f'9. ld+json blocks on post: {out.count("application/ld+json")}')

print()
print('=== ALL CHECKS COMPLETE ===')
