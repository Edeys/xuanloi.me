# Nhiem vu AO Worker: Sua toan bo loi audit trong xuanloi.me

Hay doc ky va thuc hien tuan tu cac muc duoi day trong worktree hien tai:

### 1. src/layouts/PostDetails.astro
- Dong the </script> truoc <style> tai dong ~419.
- Sua logic tinh prevPost / nextPost:
  const prevPost = currentPostIndex > 0 ? allPosts[currentPostIndex - 1] : null;
  const nextPost = (currentPostIndex >= 0 && currentPostIndex < allPosts.length - 1) ? allPosts[currentPostIndex + 1] : null;
- Link prevPost & nextPost them trailing slash: href={`/posts/${prevPost.slug}/`} va href={`/posts/${nextPost.slug}/`}.
- Nut cuon len dau trang #back-to-top: sua thanh window.scrollTo({ top: 0, behavior: "smooth" }).
- Nut sao chep code trong attachCopyButtons: dich "Copy" -> "Sao chep", "Copied" -> "Da sao chep".

### 2. src/pages/index.astro
- Di chuyen 2 the <StructuredData> vao ben trong the <Layout> (ngay sau dong mo <Layout ...>).
- Sua link avatar /about thanh /about/.

### 3. src/components/Header.astro
- Dong the <span> tai dong 106 boc nut tim kiem <LinkButton href="/search" ...> truoc khi dong </li>.
- Doi href cac menu thanh co trailing slash: href="/posts/", href="/about/", href="/archives/", href="/search/".
- Doi "Bo qua noi dung" thanh "Chuyen den noi dung chinh".

### 4. src/components/NewsletterForm.astro
- The <form>: Them action="/api/subscribe" va method="POST".
- The input ten: Them name="name" va aria-label="Ho va ten".
- The input email: Them name="email" va aria-label="Dia chi email".
- Them honeypot input an ngay dau form: <input type="text" name="website" class="hidden" tabindex="-1" autocomplete="off" />.
- The <p id="subscribe-msg": Them role="alert" va aria-live="polite".
- Script submit:
  + Disable ca nut bam va 2 o input khi dang gui.
  + Kiem tra res.ok, boc await res.json() trong try/catch an toan. Neu server tra ve loi HTML hoac khong parse duoc, hien thi thong diep loi than thien tieng Viet.
  + Mo lai disabled cho nut bam va cac o input khi co loi.

### 5. src/pages/404.astro & src/pages/500.astro
- Them noindex={true} cho <Layout>.
- Trong 404.astro: Bo sung goi y nut "Xem bai viet" (/posts/) va "Tim kiem" (/search/).

### 6. src/pages/admin.astro
- Sua logic tao slug: import slugifyStr tu @/utils/slugify de khong bi mat chu tieng Viet co dau.
- Them nut / link "Quay lai trang chu" (/).

### 7. src/components/ShareLinks.astro & src/constants.ts
- Bo sung Twitter/X, LinkedIn va nut Copy Link.
- Nhan props title?: string, description?: string.
- Dung encodeURIComponent(URL.href) cho moi link chia se.
- Them text=${encodeURIComponent(title || '')} cho Twitter va Telegram.
- Them target="_blank" va rel="noopener noreferrer" cho cac link chia se ben ngoai.
- Them nut "Sao chep lien ket" (Copy to clipboard va hien thi thong bao da sao chep).

### 8. src/utils/getPath.ts
- Dam bao duong dan tra ve luon co dau / o cuoi (chuan trailing slash always).

### 9. Don dep route thua
- Xoa src/pages/posts/[page].astro.
- Xoa src/pages/posts/[...page].astro.
- Xoa src/pages/page/[page].astro (va thu muc src/pages/page).

### 10. src/pages/tags/[tag]/[...page].astro & src/components/TableOfContents.astro
- Xoa dong 41 <h1 slot="title" transition:name={tag}>{`Tag:${tag}`}</h1> trong src/pages/tags/[tag]/[...page].astro.
- Xoa dau cham . cung sau {item.text} va {child.text} trong src/components/TableOfContents.astro.

### 11. Kiem tra & Commit
- Chay npm run build de kiem tra toan bo trang build thanh cong khong loi.
- Chay git add . va git commit -m "fix: resolve audit issues for layout, routes, forms, buttons and share links".
- Bao cao hoan thanh.
