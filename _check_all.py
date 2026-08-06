import subprocess

ssh = ['ssh', '-i', r'C:\Users\xuanl\.ssh\do-9router', 'root@129.212.238.158']

routes = [
    ("Homepage", "https://xuanloi.me/"),
    ("Posts list", "https://xuanloi.me/posts/"),
    ("Tags list", "https://xuanloi.me/tags/"),
    ("About", "https://xuanloi.me/about/"),
    ("Search", "https://xuanloi.me/search/"),
    ("Post 2026", "https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/"),
    ("Post old", "https://xuanloi.me/posts/2026/cang-lon-cang-kho-yeu/"),
    ("Admin", "https://xuanloi.me/admin/"),
    ("RSS", "https://xuanloi.me/rss.xml"),
    ("Sitemap", "https://xuanloi.me/sitemap-index.xml"),
    ("Robots", "https://xuanloi.me/robots.txt"),
    ("404 page", "https://xuanloi.me/this-does-not-exist/"),
    ("Avatar img", "https://xuanloi.me/assets/avatar_round.webp"),
]

for name, url in routes:
    p = subprocess.run(ssh + [f"curl -sI {url} 2>&1 | head -1"], capture_output=True, timeout=15)
    status = p.stdout.decode("utf-8", errors="replace").strip()
    bad = "403" in status or "404" in status and "this-does-not-exist" not in url
    marker = "FAIL" if bad else "OK"
    print(f"[{marker:4s}] {status:50s} {name} ({url})")
