import subprocess, re

ssh = ['ssh', '-i', r'C:\Users\xuanl\.ssh\do-9router', 'root@129.212.238.158']
def run(cmd):
    p = subprocess.run(ssh + [cmd], capture_output=True, timeout=30)
    return p.stdout.decode('utf-8', errors='replace').strip()

# Check sitemap admin URLs
sitemap = run('curl -s https://xuanloi.me/sitemap-0.xml')
admin_matches = re.findall(r'<loc>(.*admin[^<]*)</loc>', sitemap)
print('Sitemap admin URLs:', admin_matches)

# Check homepage entry
home_matches = re.findall(r'<loc>[^<]*xuanloi\.me[^<]*</loc>.*?</url>', sitemap, re.DOTALL)
for h in home_matches:
    if '<loc>https://xuanloi.me</loc>' in h:
        print('Homepage sitemap entry:', h[:200])

# Check post page structured data
post = run('curl -s https://xuanloi.me/posts/17-cau-hoi-thay-doi-cuoc-doi/')
ldmatches = re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', post, re.DOTALL)
for i, m in enumerate(ldmatches):
    print(f'ld+json block {i}:', m[:300])

# Check /admin in sitemap more carefully
admin_any = 'admin' in sitemap.lower()
print(f'/admin appears in sitemap anywhere: {admin_any}')

# Check astro config changes are correct
print()
print('Checking local astro.config.mjs sitemap filter...')
with open(r'D:\Dự Án Cá Nhân\xuanloi.me\astro.config.mjs', 'r', encoding='utf-8') as f:
    cfg = f.read()
if 'page.includes("/admin")' in cfg:
    print('Sitemap admin filter: PRESENT')
    idx = cfg.index('/admin')
    print('Context:', cfg[idx-30:idx+80])
else:
    print('Sitemap admin filter: MISSING')
    idx = cfg.find('filter:')
    if idx > 0:
        print('Filter context:', cfg[idx:idx+300])
