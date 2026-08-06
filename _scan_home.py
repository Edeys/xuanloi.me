import urllib.request, re
r = urllib.request.urlopen("https://xuanloi.me/", timeout=30)
html = r.read().decode("utf-8")
srcs = set()
for m in re.finditer(r'src="([^"]+)"', html):
    srcs.add(m.group(1))
print("=== SRC URLs found ===")
for s in sorted(srcs):
    print(" ", s)
hrefs = set()
for m in re.finditer(r'href="([^"]+)"', html):
    h = m.group(1)
    if h.startswith("/") and not h.endswith(".xml"):
        hrefs.add(h)
print("\n=== Local HREFs ===")
for h in sorted(hrefs)[:20]:
    print(" ", h)
# Check for prefetch/modulepreload
for m in re.finditer(r'<link[^>]+(modulepreload|prefetch)[^>]+href="([^"]+)"', html):
    print("\n  PRELOAD: ", m.group(0)[:200])
