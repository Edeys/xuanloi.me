import re
with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','r',encoding='utf-8') as f:
    s = f.read()
s = s.replace('  : {};\n};', '  : {};')
with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','w',encoding='utf-8') as f:
    f.write(s)
print('cleaned')
