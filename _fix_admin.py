import re

base = r'D:\Dự Án Cá Nhân\xuanloi.me'

# Fix Layout.astro: add noindex prop + render meta tag
layout_path = base + r'\src\layouts\Layout.astro'
with open(layout_path, 'r', encoding='utf-8') as f:
    s = f.read()

# Add noindex to Props interface
s = s.replace('scrollSmooth?: boolean;', 'scrollSmooth?: boolean;\n  noindex?: boolean;')
# Add noindex to destructure
s = s.replace('scrollSmooth = false,\n} = Astro.props;', 'scrollSmooth = false,\n  noindex = false,\n} = Astro.props;')
# Add noindex meta tag after canonical link  
s = s.replace('<link rel="canonical" href={canonicalURL} />', '<link rel="canonical" href={canonicalURL} />\n    {noindex && <meta name="robots" content="noindex, nofollow" />}')
# Also add after the og:url meta tag as backup for SEO
s = s.replace('<meta property="og:url" content={canonicalURL} />', '<meta property="og:url" content={canonicalURL} />\n    {noindex && <meta name="robots" content="noindex, nofollow" />}')

with open(layout_path, 'w', encoding='utf-8') as f:
    f.write(s)

print('Layout noindex prop added')

# Fix admin.astro: pass noindex prop  
admin_path = base + r'\src\pages\admin.astro'
with open(admin_path, 'r', encoding='utf-8') as f:
    s = f.read()

# Remove the Fragment approach, use prop instead
s = s.replace('<Layout>', '<Layout noindex>')
# Clean up the old Fragment approach
s = s.replace('  <Fragment slot="head">\n    <meta name="robots" content="noindex, nofollow" />\n  </Fragment>\n', '')

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(s)

print('Admin noindex via prop done')

# Verify
with open(layout_path, 'r', encoding='utf-8') as f:
    print('noindex in interface:', 'noindex?: boolean' in f.read())
with open(layout_path, 'r', encoding='utf-8') as f:
    print('noindex in destructure:', 'noindex = false' in f.read())
with open(admin_path, 'r', encoding='utf-8') as f:
    print('admin has noindex:', 'noindex' in f.read())
