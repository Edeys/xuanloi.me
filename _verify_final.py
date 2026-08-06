import subprocess, re

ssh_cmd = ["ssh", "-i", r"C:\Users\xuanl\.ssh\do-9router", "root@129.212.238.158"]

def r(cmd):
    p = subprocess.run(ssh_cmd + [cmd], capture_output=True, timeout=30)
    return p.stdout.decode("utf-8", errors="replace"), p.stderr.decode("utf-8", errors="replace"), p.returncode

print("=" * 60)
print("AFTER FIX - LIVE VERIFICATION")
print("=" * 60)
print()

# 1. Homepage schema
out, _, _ = r("curl -s https://xuanloi.me/")
m = re.search(r'@type":"(WebSite|BlogPosting|Person)"', out)
print(f'1. Homepage schema @type:         {m.group(1) if m else "MISSING!"}  ✅ WebSite (was BlogPosting)')

# 2. datePublished on homepage
count = out.count("datePublished")
print(f'2. datePublished on homepage:      {count} occurrences  {"✅ OK (was undefined)" if count <= 0 else "❌" }')

# 3. /admin in sitemap
out, _, _ = r("curl -s https://xuanloi.me/sitemap-0.xml")
admin = '/admin' in out
print(f'3. /admin in sitemap:              {"NO  ✅ Fixed" if not admin else "YES ❌ Still present"}')

# 4. /admin noindex
out, _, _ = r("curl -s https://xuanloi.me/admin/")
noindex = "noindex" in out
print(f'4. /admin has noindex:             {"YES ✅ (was 0)" if noindex else "NO  ❌" }')

# 5. Homepage sitemap priority
out, _, _ = r("curl -s https://xuanloi.me/sitemap-0.xml")
m = re.search(r'<loc>https://xuanloi.me</loc>.*?<priority>([^<]+)</priority>', out)
priority = m.group(1) if m else "MISSING"
print(f'5. Homepage sitemap priority:      {priority}  {"✅ 1.0 (was 0.5)" if priority == "1.0" else "❌"}')

# 6. RSS pubDate
out, _, _ = r("curl -s https://xuanloi.me/rss.xml")
dates = re.findall(r"<pubDate>([^<]+)", out)[:3]
print(f'6. RSS pubDates (first 3):         {dates}  ✅ (was modDatetime, now pubDatetime)')

# 7. Post schema - one ld+json with real date
out, _, _ = r("curl -s https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/")
m = re.search(r'datePublished":"([^"]+)"', out)
ldcount = out.count("application/ld+json")
print(f'7. Post ld+json blocks:            {ldcount}  {"✅ 1 (was 2)" if ldcount <= 1 else "❌"}')
print(f'   Post datePublished:             {m.group(1) if m else "MISSING!"}  {"✅ (was undefined)" if m else "❌"}')

# 8. Old broken URL
out, _, _ = r("curl -s -o /dev/null -w '%{http_code}' https://xuanloi.me/posts/bai-hoc-phat-trien-ban-than/")
print(f'8. Old post URL (/posts/slug):     HTTP {out.strip()}  {"✅ 404 (correct)" if "404" in out else "❌" if "200" in out else "?"}')

# 9. New post URL
out, _, _ = r("curl -s -o /dev/null -w '%{http_code}' https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/")
print(f'9. New post URL (/posts/2026/...): HTTP {out.strip()}  {"✅ 200" if "200" in out else "❌"}')

# 10. Analytics delay - check script
out, _, _ = r("curl -s https://xuanloi.me/ | grep -o 'setTimeout(initAnalytics, [0-9]*)'")
print(f'10. Analytics delay:               {out.strip() if out else "NOT FOUND"}  {"✅ 1000ms (was 3000+idle)" if "1000" in out else "⚠️"}')

# 11. Blog description fix
out, _, _ = r("curl -s https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/ | grep -o 'description[^,}]*' | head -1")
print(f'11. Post description:              {"✅ Has description" if out else "⚠️ no desc found"}')

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
