import urllib.request, json, sys
sys.stdout.reconfigure = lambda: None

API_KEY = "AIzaSyCVzKlJ_VRRYNHyiak7HfPAVJuUcTx8o5U"
URLS = [
    "https://xuanloi.me/",
    "https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/",
]

for target_url in URLS:
    print(f"\n{'='*60}")
    print(f"PageSpeed: {target_url}")
    print(f"{'='*60}")
    
    url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={urllib.request.quote(target_url, safe='')}&strategy=mobile&key={API_KEY}"
    
    try:
        req = urllib.request.urlopen(url, timeout=60)
        d = json.loads(req.read())
        lh = d.get("lighthouseResult", {})
        cats = lh.get("categories", {})
        audits = lh.get("audits", {})
        
        print("\nSCORES:")
        cat_names = {"performance": "Performance", "accessibility": "Accessibility", 
                     "best-practices": "Best Practices", "seo": "SEO"}
        for c, v in cats.items():
            s = v.get("score")
            score_val = round(s * 100) if s is not None else 0
            print(f"  {cat_names.get(c, c)}: {score_val}")
        
        print("\nTOP OPPORTUNITIES (biggest savings):")
        opps = [(k, v) for k, v in audits.items() 
                if v.get("details", {}).get("type") == "opportunity" 
                and v.get("details", {}).get("overallSavingsMs")]
        opps.sort(key=lambda x: x[1]["details"]["overallSavingsMs"], reverse=True)
        for k, v in opps[:8]:
            ms = v["details"]["overallSavingsMs"]
            print(f"  [{ms}ms] {v.get('title', k)}")
            items = v.get("details", {}).get("items", [])
            for item in items[:2]:
                url_str = item.get("url", "") or item.get("node", {}).get("nodeLabel", "") or ""
                if url_str:
                    print(f"    - {url_str[:100]}")
        
        print("\nDIAGNOSTICS (opportunities >50ms):")
        for k, v in opps:
            ms = v["details"]["overallSavingsMs"]
            if ms >= 50:
                print(f"  [{ms}ms] {v.get('title', k)}")
        
        print("\nFAILED AUDITS:")
        failed = [(k, v) for k, v in audits.items() 
                  if v.get("score") == 0 and v.get("scoreDisplayMode") == "binary"]
        for k, v in failed[:5]:
            print(f"  FAIL: {v.get('title', k)}")
            print(f"    {v.get('description', '')[:200]}")
        
    except Exception as e:
        print(f"  Error: {e}")

print("\n\nDONE")
