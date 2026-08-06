import urllib.request, json

API_KEY = "AIzaSyCVzKlJ_VRRYNHyiak7HfPAVJuUcTx8o5U"
url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me/&strategy=mobile&key=" + API_KEY

req = urllib.request.urlopen(url, timeout=60)
d = json.loads(req.read())
audits = d["lighthouseResult"]["audits"]

checks = [
    "lcp-lazy-loaded",
    "render-blocking-resources",
    "unused-css-rules",
    "unused-javascript",
    "total-byte-weight",
    "dom-size",
    "critical-request-chains",
    "redirects",
    "uses-responsive-images",
    "offscreen-images",
    "uses-webp-images",
    "uses-optimized-images",
    "preload-lcp-image",
    "uses-text-compression",
    "server-response-time",
    "mainthread-work-breakdown",
    "bootup-time",
    "duplicated-javascript",
    "legacy-javascript",
    "network-requests",
    "network-rtt",
    "prioritize-lcp-image",
    "non-composited-animations",
    "unsized-images",
]

for m in checks:
    a = audits.get(m)
    if a:
        s = a.get("score")
        dv = a.get("displayValue", "")
        title = a.get("title", m)
        sc = str(round(s*100))+"%" if s is not None else "N/A"
        print(f"[{sc}] {title}")
        if dv:
            print(f"  {dv}")
        items = a.get("details", {}).get("items", [])
        for item in items[:3]:
            u = item.get("url", "") or item.get("node", {}).get("nodeLabel", "") or ""
            if u:
                ms = item.get("wastedMs", "")
                byte = item.get("wastedBytes", "")
                info = f"  {u[:100]}"
                if ms:
                    info += f" ({ms}ms)"
                if byte:
                    info += f" ({byte} bytes)"
                print(info)
