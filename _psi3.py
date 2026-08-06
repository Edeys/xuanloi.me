import urllib.request, json

API_KEY = "AIzaSyCVzKlJ_VRRYNHyiak7HfPAVJuUcTx8o5U"

# Get the raw categories available
url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://xuanloi.me/&strategy=mobile&key={API_KEY}"
req = urllib.request.urlopen(url, timeout=60)
d = json.loads(req.read())
lh = d.get("lighthouseResult", {})

cats = lh.get("categories", {})
print("Categories found:", list(cats.keys()))
print()
for c, v in cats.items():
    s = v.get("score")
    print(f"{c}: {round(s*100) if s else 0}")

audits = lh.get("audits", {})
print(f"\nTotal audits: {len(audits)}")

# Show all opportunities
opps = [(k, v) for k, v in audits.items() 
        if v.get("details", {}).get("type") == "opportunity" 
        and v.get("details", {}).get("overallSavingsMs")]
opps.sort(key=lambda x: x[1]["details"]["overallSavingsMs"], reverse=True)
print(f"\nOpportunities found: {len(opps)}")
for k, v in opps:
    ms = v["details"]["overallSavingsMs"]
    print(f"  [{ms}ms] {v.get("title", k)}")
    items = v.get("details", {}).get("items", [])
    for item in items[:2]:
        u = item.get("url", "")
        if not u:
            n = item.get("node", {})
            u = n.get("nodeLabel", "") if isinstance(n, dict) else ""
        if u:
            print(f"    {u[:120]}")

# Diagnostics
print("\nDiagnostics:")
diags = [(k, v) for k, v in audits.items() 
         if v.get("details", {}).get("type") == "diagnostic" 
         and v.get("score") is not None and v.get("score") < 1]
diags.sort(key=lambda x: x[1]["score"])
for k, v in diags[:10]:
    print(f"  [{round(v["score"]*100)}%] {v.get("title", k)}")

# Find rendering issues
print("\nRendering/font issues:")
for k, v in audits.items():
    if any(x in k for x in ["font", "render", "layout", "cumulative", "largest", "total-block", "interactive"]):
        sc = v.get("score")
        sc_str = f"[{round(sc*100)}%]" if sc is not None else "[N/A]"
        print(f"  {sc_str} {v.get("title", k)}: {v.get("displayValue", v.get("description", ""))[:100]}")
