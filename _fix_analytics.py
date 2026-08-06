import re

with open(r"D:\Dự Án Cá Nhân\xuanloi.me\src\components\Analytics.astro", "r", encoding="utf-8") as f:
    s = f.read()

# Replace the load event + setTimeout with interaction-based lazy loading
old = r"""  window.addEventListener('load', function() {
    setTimeout(initAnalytics, 1000);
  });"""

new = r"""  // Load analytics only on first user interaction (scroll/click/tap)
  // to avoid impacting LCP and Core Web Vitals
  var loaded = false;
  function loadOnce() {
    if (loaded) return;
    loaded = true;
    initAnalytics();
    document.removeEventListener('scroll', loadOnce);
    document.removeEventListener('click', loadOnce);
    document.removeEventListener('touchstart', loadOnce);
    document.removeEventListener('mousemove', loadOnce);
  }
  document.addEventListener('scroll', loadOnce, { once: true });
  document.addEventListener('click', loadOnce, { once: true });
  document.addEventListener('touchstart', loadOnce, { once: true });
  document.addEventListener('mousemove', loadOnce, { once: true });
  // Fallback: load after 4 seconds if no interaction
  setTimeout(loadOnce, 4000);"""

s = s.replace(old, new)

with open(r"D:\Dự Án Cá Nhân\xuanloi.me\src\components\Analytics.astro", "w", encoding="utf-8") as f:
    f.write(s)

print("Analytics updated to interaction-based lazy loading")
