import subprocess
ssh = ['ssh', '-i', r'C:\Users\xuanl\.ssh\do-9router', 'root@129.212.238.158']

def run(cmd):
    r = subprocess.run(ssh + [cmd], capture_output=True, text=True, timeout=30)
    return r.stdout, r.stderr, r.returncode

def curl(url, x='-s'):
    return run(f'curl {x} {url}')

print('=== AFTER FIX ===')
print()

# 1. Homepage schema type
out, _, _ = curl('https://xuanloi.me/')
import re
m = re.search(r'"@type":"([^"]+)"', out)
print('1. Homepage @type:', m.group(1) if m else 'NONE')

# 2. datePublished count on homepage
out, _, _ = curl('https://xuanloi.me/')
print('2. datePublished on homepage:', out.count('datePublished'))

# 3. /admin in sitemap
out, _, _ = curl('https://xuanloi.me/sitemap-0.xml')
print('3. /admin in sitemap:', out.count('/admin'))

# 4. /admin noindex
out, _, _ = curl('https://xuanloi.me/admin/')
print('4. /admin noindex count:', out.count('noindex'))

# 5. Homepage priority
out, _, _ = curl('https://xuanloi.me/sitemap-0.xml')
m = re.search(r'<url><loc>https://xuanloi.me</loc><changefreq>([^<]*)</changefreq><priority>([^<]*)</priority>', out)
print('5. Homepage priority:', m.groups() if m else 'NOT FOUND')

# 6. RSS pubDate first 3
out, _, _ = curl('https://xuanloi.me/rss.xml')
dates = re.findall(r'<pubDate>([^<]*)</pubDate>', out)[:3]
print('6. RSS pubDate first 3:', dates)

# 7. Old broken URL
out, err, _ = run('curl -sI https://xuanloi.me/posts/bai-hoc-phat-trien-ban-than/')
print('7. Old broken URL status:', out.split('\n')[0] if out else 'ERR')

# 8. New build dir /index.html
out, _, _ = curl('https://xuanloi.me/')
m = re.search(r'<title>([^<]+)</title>', out)
print('8. Homepage title:', m.group(1) if m else 'NONE')

# 9. Post page schema (should have BlogPosting with real date)
out, _, _ = curl('https://xuanloi.me/posts/17-cau-hoi-thay-doi-cuoc-doi/')
m = re.search(r'"datePublished":"([^"]+)"', out)
print('9. Post datePublished:', m.group(1) if m else 'NONE')
