with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','r',encoding='utf-8') as f:
    s = f.read()

# Change: always use WebSite schema, not BlogPosting (PostDetails handles it)
s = s.replace(
    'const schemaType = pubDatetime ? "BlogPosting" : "WebSite";',
    'const schemaType = "WebSite";'
)
s = s.replace(
    'const schemaData = pubDatetime\n  ? {\n      title,\n      description,\n      author,\n      pubDatetime,\n      modDatetime,\n      url: canonicalURL.toString(),\n      ogImage: socialImageURL.toString(),\n      tags: [] as string[],\n    }\n  : {};',
    'const schemaData = {};'
)

with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','w',encoding='utf-8') as f:
    f.write(s)

print('Fixed')
