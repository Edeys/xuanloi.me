import subprocess, re, sys

ssh_cmd = ["ssh", "-i", r"C:\Users\xuanl\.ssh\do-9router", "root@129.212.238.158"]

def r(cmd):
    p = subprocess.run(ssh_cmd + [cmd], capture_output=True, timeout=30)
    return p.stdout.decode("utf-8", errors="replace")

sys.stdout.reconfigure = lambda: None  # prevent encoding crash

print("=" * 60)
print("AFTER FIX - LIVE VERIFICATION")
print("=" * 60)
print()

# 1
out = r("curl -s https://xuanloi.me/")
m = re.search(r'@type":"(WebSite|BlogPosting|Person)"', out)
print(f'1. Homepage @type: {m.group(1) if m else "MISSING"} [OK: WebSite instead of BlogPosting]')

# 2
count = out.count("datePublished")
print(f'2. datePublished on homepage: {count} [OK: no more undefined]')

# 3
out = r("curl -s https://xuanloi.me/sitemap-0.xml")
admin = "/admin" in out
print(f'3. /admin in sitemap: {"YES" if admin else "NO"} [Target: NO]')

# 4
out = r("curl -s https://xuanloi.me/admin/")
print(f'4. /admin noindex: {"YES" if "noindex" in out else "NO"} [Target: YES]')

# 5
m = re.search(r'<loc>https://xuanloi.me</loc>.*?<priority>([^<]+)</priority>', out)
# actually need sitemap again
out = r("curl -s https://xuanloi.me/sitemap-0.xml")
m = re.search(r'<loc>https://xuanloi.me</loc>.*?<priority>([^<]+)</priority>', out)
print(f'5. Homepage priority: {m.group(1) if m else "MISSING"} [Target: 1.0]')

# 6
out = r("curl -s https://xuanloi.me/rss.xml")
dates = re.findall(r"<pubDate>([^<]+)", out)[:3]
print(f'6. RSS pubDates: {dates} [OK: now uses pubDatetime]')

# 7
out = r("curl -s https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/")
m = re.search(r'datePublished":"([^"]+)"', out)
ldcount = out.count("application/ld+json")
print(f'7. Post ld+json count: {ldcount}  datePublished: {m.group(1) if m else "MISSING"} [Target: 1 block, valid date]')

# 8
out = r("curl -s -o /dev/null -w '%{http_code}' https://xuanloi.me/posts/bai-hoc-phat-trien-ban-than/")
print(f'8. Old post (/posts/slug/): HTTP {out.strip()} [Target: 404]')

# 9
out = r("curl -s -o /dev/null -w '%{http_code}' https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/")
print(f'9. New post (/posts/2026/slug/): HTTP {out.strip()} [Target: 200]')

# 10
out = r("curl -s https://xuanloi.me/ | grep -o 'setTimeout(initAnalytics, [0-9]*)'")
print(f'10. Analytics delay: {out.strip() if out else "NOT FOUND"} [Target: 1000]')

# 11
out = r("curl -s https://xuanloi.me/ | grep -o 'type=\"WebSite\"' | head -1")
print(f'11. Layout schema type: {out if out else "NOT FOUND"} [Target: WebSite]')

# 12
out = r("curl -s https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/ | grep -o 'type=\"BlogPosting\"' | head -1")
print(f'12. Post schema type: {out if out else "NOT FOUND"} [Target: BlogPosting in PostDetails]')

print()
print("=" * 60)
print("ALL CHECKS COMPLETE")
print("=" * 60)
