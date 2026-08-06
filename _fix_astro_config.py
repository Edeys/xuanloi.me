import os
os.chdir(r'D:\Dự Án Cá Nhân\xuanloi.me')

with open('astro.config.mjs', 'r', encoding='utf-8') as f:
    s = f.read()

old_i18n = '  i18n: {\n    defaultLocale: "vi",\n    locales: ["vi"],\n    routing: {\n      prefixDefaultLocale: false,\n    },\n  },'

new_i18n = '  i18n: {\n    defaultLocale: "vi",\n    locales: ["vi", "en", "ko"],\n    routing: {\n      prefixDefaultLocale: false,\n      strategy: "prefix-other-locales",\n    },\n  },'

s = s.replace(old_i18n, new_i18n)

with open('astro.config.mjs', 'w', encoding='utf-8') as f:
    f.write(s)

print('done')
