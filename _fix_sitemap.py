with open(r'D:\Dự Án Cá Nhân\xuanloi.me\astro.config.mjs','r',encoding='utf-8') as f:
    s = f.read()

old = '// Always exclude archives if not showing them'
new = "// Always exclude admin pages\n        if (page.includes(\"/admin\")) return false;\n\n        " + old
s = s.replace(old, new)

with open(r'D:\Dự Án Cá Nhân\xuanloi.me\astro.config.mjs','w',encoding='utf-8') as f:
    f.write(s)

print('Admin filter added:', 'page.includes("/admin")' in s)
print('Homepage priority fixed:', 'SITE.website.replace(/\/$/, "")' in s)
