import urllib.request, json
url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me&strategy=mobile"
try:
    r = urllib.request.urlopen(url, timeout=60)
    d = json.loads(r.read())
    cats = d.get("lighthouseResult", {}).get("categories", {})
    for k, v in cats.items():
        s = v.get("score", 0)
        print(f"{k}: {round(s * 100)}")
    aud = d.get("lighthouseResult", {}).get("audits", {})
    for m in ["first-contentful-paint","largest-contentful-paint","total-blocking-time","cumulative-layout-shift","speed-index","interactive"]:
        a = aud.get(m, {})
        dv = a.get("displayValue", "N/A")
        sc = a.get("score", "N/A")
        print(f"{m}: {dv} (score={sc})")
    # Print failing audits
    print("\n--- FAILING AUDITS (score < 0.5) ---")
    for aid, audit in aud.items():
        score = audit.get("score")
        if score is not None and score < 0.5:
            title = audit.get("title", aid)
            savings = audit.get("details", {}).get("overallSavingsMs", 0)
            size = audit.get("details", {}).get("overallSavingsBytes", 0)
            print(f"  [{round(score*100)}] {title} (savings: {savings}ms / {size}B)")
except Exception as e:
    print(f"Error: {e}")
