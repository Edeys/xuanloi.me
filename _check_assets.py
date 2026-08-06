import urllib.request, json, re
# Get homepage HTML
r = urllib.request.urlopen("https://xuanloi.me/", timeout=30)
html = r.read().decode("utf-8")
print("=== Homepage raw size:", len(html.encode("utf-8")), "bytes ===")
print("=== External scripts ===")
for m in re.finditer(r'<script[^>]*src="([^"]+)"', html):
    print(" ", m.group(1))
print("=== Stylesheets ===")
for m in re.finditer(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"', html):
    print(" ", m.group(1))
print("=== Preloads ===")
for m in re.finditer(r'<link[^>]*rel="preload"[^>]*>', html):
    print(" ", m.group(0)[:200])
print("=== Preconnects ===")
for m in re.finditer(r'<link[^>]*rel="preconnect"[^>]*>', html):
    print(" ", m.group(0)[:200])
print("=== Images ===")
for m in re.finditer(r'<img[^>]*src="([^"]+)"', html):
    print(" ", m.group(1))
print("=== Inline <style> size ===")
for m in re.finditer(r'<style[^>]*>(.*?)</style>', html, re.DOTALL):
    print("  ", len(m.group(1)), "bytes")
