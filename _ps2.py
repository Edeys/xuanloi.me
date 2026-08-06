import urllib.request
import json

API_KEY = "AIzaSyCVzKlJ_VRRYNHyiak7HfPAVJuUcTx8o5U"
url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me/&strategy=mobile&key=" + API_KEY

req = urllib.request.urlopen(url, timeout=60)
d = json.loads(req.read())
lh = d.get("lighthouseResult", {})
cats = lh.get("categories", {})

print("=== SCORES ===")
for c, v in cats.items():
    s = v.get("score")
    print(f"  {c}: {round(s*100) if s else 0}")

audits = lh.get("audits", {})
print(f"Total audits: {len(audits)}")

opps = []
for k, v in audits.items():
    det = v.get("details", {})
    if det.get("type") == "opportunity" and det.get("overallSavingsMs"):
        opps.append((k, v, det["overallSavingsMs"]))

opps.sort(key=lambda x: -x[2])
print(f"Opportunities: {len(opps)}")
for k, v, ms in opps[:10]:
    t = v.get("title", k)
    print(f"  [{ms}ms] {t}")
    for item in v.get("details", {}).get("items", [])[:2]:
        u = item.get("url", "")
        if not u:
            node = item.get("node", {})
            u = node.get("nodeLabel", "") if isinstance(node, dict) else ""
        if u:
            print(f"    {u[:120]}")

print("\n=== KEY METRICS ===")
metrics = ["first-contentful-paint", "largest-contentful-paint", "total-blocking-time", 
           "cumulative-layout-shift", "speed-index", "interactive",
           "unused-javascript", "render-blocking-resources", "unused-css-rules",
           "uses-text-compression", "uses-rel-preconnect", "efficient-animated-content",
           "duplicated-javascript", "legacy-javascript", "preload-lcp-image",
           "total-byte-weight", "dom-size", "critical-request-chains",
           "mainthread-work-breakdown", "bootup-time", "font-display"]
for m in metrics:
    a = audits.get(m)
    if a:
        s = a.get("score")
        nv = a.get("numericValue", 0)
        tv = a.get("title", m)
        pct = round(s*100) if s is not None else "N/A"
        print(f"  [{pct}%] {tv}")
        if nv:
            if nv > 1000:
                print(f"    {nv/1000:.2f}s / {nv:.0f}ms")
            else:
                print(f"    {nv}")
