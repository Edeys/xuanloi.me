path = r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for line in lines:
    # Skip old structuredData block
    if 'const structuredData = {' in line:
        out.append('const schemaType = pubDatetime ? "BlogPosting" : "WebSite";\n')
        out.append('const schemaData = pubDatetime\n')
        out.append('  ? {\n')
        out.append('      title,\n')
        out.append('      description,\n')
        out.append('      author,\n')
        out.append('      pubDatetime,\n')
        out.append('      modDatetime,\n')
        out.append('      url: canonicalURL.toString(),\n')
        out.append('      ogImage: socialImageURL.toString(),\n')
        out.append('      tags: [] as string[],\n')
        out.append('    }\n')
        out.append('  : {};\n')
        continue
    # Skip ALL lines of the old structuredData block
    if '"@context"' in line or '"@type": "BlogPosting"' in line or 'headline:' in line or 'image: `${social' in line or 'datePublished:' in line or '...(modDatetime' in line or 'author: [' in line or '"@type": "Person"' in line or 'name: `${author}`' in line or '...(profile' in line or '    },' in line or '  ],' in line:
        continue

    # Replace ld+json script block
    if '<!-- Google JSON-LD Structured data -->' in line:
        out.append('    <!-- Google JSON-LD Structured data -->\n')
        out.append('    <StructuredData type={schemaType} data={schemaData} />\n')
        continue
    if 'type="application/ld+json"' in line or 'is:inline' in line or 'JSON.stringify(structuredData)' in line or '    />' == line.strip():
        continue

    # Add StructuredData import after Analytics
    if 'import Analytics from' in line and 'StructuredData' not in line:
        out.append(line)
        out.append('import StructuredData from "@/components/StructuredData.astro";\n')
        continue

    out.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(out)

print('OK')

# Quick verify
with open(path, 'r', encoding='utf-8') as f:
    v = f.read()
print('Has StructuredData import:', 'import StructuredData' in v)
print('Has schemaType:', 'schemaType' in v)
print('Has <StructuredData:', '<StructuredData' in v)
print('NO datePublished undefined:', 'datePublished: `$${pubDatetime?.toISOString()}`' not in v)
