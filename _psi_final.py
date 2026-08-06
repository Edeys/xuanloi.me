import urllib.request, json, time
time.sleep(3)
url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me/posts/2026/tuoi-tre-khong-tien-khong-nguoi-hau-thuan&strategy=mobile"
resp = urllib.request.urlopen(url, timeout=60)
data = json.loads(resp.read())
cats = data.get("lighthouseResult", {}).get("categories", {})
for k, v in cats.items():
    s = v.get("score", 0)
    print(f"{k}: {round(s * 100)}")
aud = data.get("lighthouseResult", {}).get("audits", {})
for m in ["first-contentful-paint","largest-contentful-paint","total-blocking-time","cumulative-layout-shift","speed-index"]:
    a = aud.get(m, {})
    dv = a.get("displayValue", "N/A")
    sc = a.get("score", "N/A")
    print(f"{m}: {dv} (score={sc})")
