with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','r',encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    if 'import Analytics' in lines[i] and 'StructuredData' not in lines[i]:
        new_lines.append(lines[i])
        new_lines.append('import StructuredData from "@/components/StructuredData.astro";\n')
        i += 1
        continue
    if i == 34:
        new_lines.append('const schemaType = pubDatetime ? "BlogPosting" : "WebSite";\n')
        new_lines.append('const schemaData = pubDatetime\n')
        new_lines.append('  ? {\n')
        new_lines.append('      title,\n')
        new_lines.append('      description,\n')
        new_lines.append('      author,\n')
        new_lines.append('      pubDatetime,\n')
        new_lines.append('      modDatetime,\n')
        new_lines.append('      url: canonicalURL.toString(),\n')
        new_lines.append('      ogImage: socialImageURL.toString(),\n')
        new_lines.append('      tags: [] as string[],\n')
        new_lines.append('    }\n')
        new_lines.append('  : {};\n')
        i = 48
        continue
    if i == 99:
        new_lines.append('    <!-- Google JSON-LD Structured data -->\n')
        new_lines.append('    <StructuredData type={schemaType} data={schemaData} />\n')
        i = 105
        continue
    new_lines.append(lines[i])
    i += 1

with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','w',encoding='utf-8') as f:
    f.writelines(new_lines)

print('OK')
