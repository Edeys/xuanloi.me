with open(r"D:\Dự Án Cá Nhân\xuanloi.me\src\pages\index.astro", "r", encoding="utf-8") as f:
    s = f.read()

# Add preloadImage prop to Layout call
s = s.replace(
    '<Layout description={SITE.desc}>',
    '<Layout description={SITE.desc} preloadImage="/assets/avatar_round.webp">'
)

with open(r"D:\Dự Án Cá Nhân\xuanloi.me\src\pages\index.astro", "w", encoding="utf-8") as f:
    f.write(s)

print("index.astro updated")
