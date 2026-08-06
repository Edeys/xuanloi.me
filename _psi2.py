import urllib.request, json, sys
sys.stdout.reconfigure = lambda: None

API_KEY = "AIzaSyCVzKlJ_VRRYNHyiak7HfPAVJuUcTx8o5U"

for strategy in ["mobile", "desktop"]:
    url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me/&strategy={strategy}&key={API_KEY}"
    print(f"\n{'='*40} {strategy.upper()} {'='*40}")
    try:
        req = urllib.request.urlopen(url, timeout=60)
        d = json.loads(req.read())
        lh = d["lighthouseResult"]
        cats = lh["categories"]
        audits = lh["audits"]
        
        print(f"Performance: {round(cats['performance']['score']*100)}")
        print(f"Accessibility: {round(cats['accessibility']['score']*100)}")
        print(f"Best-Practices: {round(cats['best-practices']['score']*100)}")
        print(f"SEO: {round(cats['seo']['score']*100)}")
        
        print("\nTop Opportunities:")
        opps = [(k, v) for k, v in audits.items() 
                if v.get("details", {}).get("type") == "opportunity" 
                and v.get("details", {}).get("overallSavingsMs")]
        opps.sort(key=lambda x: x[1]["details"]["overallSavingsMs"], reverse=True)
        for k, v in opps[:10]:
            ms = v["details"]["overallSavingsMs"]
            title = v.get("title", k)
            print(f"  [{ms}ms] {title}")
            items = v.get("details", {}).get("items", [])
            for item in items[:2]:
                u = item.get("url", "") or ""
                if not u:
                    node = item.get("node", {})
                    u = node.get("nodeLabel", "") if isinstance(node, dict) else ""
                if u:
                    print(f"    {u[:120]}")
        
        print("\nDiagnostics (<1.0):")
        diags = [(k, v) for k, v in audits.items() 
                 if v.get("details", {}).get("type") == "diagnostic" 
                 and v.get("score") is not None and v.get("score") < 1]
        diags.sort(key=lambda x: x[1]["score"])
        for k, v in diags[:8]:
            print(f"  [{round(v['score']*100)}%] {v.get('title', k)}")
        
        # Post page
        url2 = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me/posts/2026/17-cau-hoi-thay-doi-cuoc-doi/&strategy={strategy}&key={API_KEY}"
        req2 = urllib.request.urlopen(url2, timeout=60)
        d2 = json.loads(req2.read())
        lh2 = d2["lighthouseResult"]
        cats2 = lh2["categories"]
        audits2 = lh2["audits"]
        print(f"\n--- POST PAGE ({strategy}) ---")
        print(f"Performance: {round(cats2['performance']['score']*100)}")
        opps2 = [(k, v) for k, v in audits2.items() 
                if v.get("details", {}).get("type") == "opportunity" 
                and v.get("details", {}).get("overallSavingsMs")]
        opps2.sort(key=lambda x: x[1]["details"]["overallSavingsMs"], reverse=True)
        for k, v in opps2[:5]:
            ms = v["details"]["overallSavingsMs"]
            print(f"  [{ms}ms] {v.get('title', k)}")
        
    except Exception as e:
        import traceback
        print(f"  Error: {e}")
        traceback.print_exc()

print("\nDONE")
