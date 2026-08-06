with open(r"D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro", "r", encoding="utf-8") as f:
    s = f.read()

# 1. Add preconnect for google-analytics and fonts.gstatic
s = s.replace(
    '<link rel="preconnect" href="https://connect.facebook.net" />',
    '<link rel="preconnect" href="https://connect.facebook.net" />\n    <link rel="preconnect" href="https://www.google-analytics.com" />\n    <link rel="preconnect" href="https://fonts.gstatic.com" />'
)

# 2. Add preloadImage prop
s = s.replace("noindex?: boolean;", "noindex?: boolean;\n  preloadImage?: string;")
s = s.replace(
    "noindex = false,\n} = Astro.props;",
    "noindex = false,\n  preloadImage,\n} = Astro.props;"
)

# 3. Add image preload after font preload
s = s.replace(
    '<link rel="preload" href="/fonts/atkinson-bold.woff2" as="font" type="font/woff2" crossorigin />',
    '<link rel="preload" href="/fonts/atkinson-bold.woff2" as="font" type="font/woff2" crossorigin />\n    {preloadImage && <link rel="preload" as="image" href={preloadImage} />}'
)

with open(r"D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro", "w", encoding="utf-8") as f:
    f.write(s)

print("Layout LCP fixes done")
