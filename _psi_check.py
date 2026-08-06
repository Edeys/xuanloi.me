import urllib.request, json

API_KEY = "AIzaSyCVzKlJ_VRRYNHyiak7HfPAVJuUcTx8o5U"
url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me/&strategy=mobile&key=" + API_KEY

req = urllib.request.urlopen(url, timeout=60)
d = json.loads(req.read())
lh = d["lighthouseResult"]
cats = lh["categories"]
audits = lh["audits"]

print("SCORES:")
for c, v in cats.items():
    s = v.get("score")
    print(f"  {c}: {round(s*100) if s else 0}")

print("\nKEY METRICS:")
metrics = ["first-contentful-paint", "largest-contentful-paint", "total-blocking-time",
           "cumulative-layout-shift", "speed-index", "interactive"]
for m in metrics:
    a = audits.get(m)
    if a:
        nv = a.get("numericValue", 0)
        s = a.get("score")
        tv = a.get("title", m)
        sc = round(s*100) if s is not None else "N/A"
        val = f"{nv/1000:.2f}s" if nv else "N/A"
        print(f"  [{sc}%] {tv}: {val}")

print("\nCOMPARISON (BEFORE vs NOW):")
print(f"  Performance: 78 -> {round(cats['performance']['score']*100)}")
lcp_now = (audits.get("largest-contentful-paint") or {}).get("numericValue", 0)
print(f"  LCP:         5.03s -> {lcp_now/1000:.2f}s" if lcp_now else "  LCP: N/A")
fcp_now = (audits.get("first-contentful-paint") or {}).get("numericValue", 0)
print(f"  FCP:         1.09s -> {fcp_now/1000:.2f}s" if fcp_now else "  FCP: N/A")
