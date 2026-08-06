with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','r',encoding='utf-8') as f:
    s = f.read()

# Step 1: Add import
old_import = 'import Analytics from "@/components/Analytics.astro";'
new_import = old_import + '\nimport StructuredData from "@/components/StructuredData.astro";'
s = s.replace(old_import, new_import, 1)

# Step 2: Replace the structuredData const block
start = s.find('const structuredData = {')
end_marker = '      ...(profile && { url: profile }),\n    },\n  ],\n};'
end = s.find(end_marker)
assert end != -1
end += len(end_marker)
old_block = s[start:end]
new_block = '''const schemaType = pubDatetime ? "BlogPosting" : "WebSite";
const schemaData = pubDatetime
  ? {
      title,
      description,
      author,
      pubDatetime,
      modDatetime,
      url: canonicalURL.toString(),
      ogImage: socialImageURL.toString(),
      tags: [] as string[],
    }
  : {};'''
s = s[:start] + new_block + s[end:]

# Step 3: Replace ld+json script block
old_script = '''    <!-- Google JSON-LD Structured data -->
    <script
      type="application/ld+json"
      is:inline
      set:html={JSON.stringify(structuredData)}
    />'''
new_script = '''    <!-- Google JSON-LD Structured data -->
    <StructuredData type={schemaType} data={schemaData} />'''
s = s.replace(old_script, new_script)

with open(r'D:\Dự Án Cá Nhân\xuanloi.me\src\layouts\Layout.astro','w',encoding='utf-8') as f:
    f.write(s)

print('Done')
print('StructuredData import:', 'import StructuredData' in s)
print('schemaType:', 'schemaType' in s)
print('No more const structuredData:', 'const structuredData' not in s)
print('No more JSON.stringify(structuredData):', 'JSON.stringify(structuredData)' not in s)
print('No more application/ld+json inline:', 'type="application/ld+json"' not in s)
