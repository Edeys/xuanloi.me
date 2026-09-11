# Instructions for Claude

This document contains important instructions and notes for Claude when working on this project.

## CRITICAL GUIDELINES

### NEVER CREATE BLOG POSTS WITHOUT CONSENT

- **NEVER CREATE BLOG POSTS WITHOUT EXPLICIT CONSENT** from the user (Xuân Lợi)
- Do not write or propose new blog content unless specifically requested
- Only help with editing or fixing existing posts when asked

### USE GSED INSTEAD OF SED

- **ALWAYS USE `gsed` INSTEAD OF `sed`** - For better compatibility across platforms
- `gsed` provides GNU sed features that are more consistent across Linux and macOS
- If editing files with sed-like operations, use `gsed` to ensure reliable results

### ALWAYS USE LATEST DEPENDENCIES

- **NEVER DOWNGRADE DEPENDENCIES** - Always use the latest stable versions
- **ALWAYS USE TOOLING TO CHECK VERSIONS** - Never guess or assume versions
- Run `npm outdated` to see what packages need updating
- Run `npm view [package] version` to check the latest published version
- When fixing dependency issues, always upgrade to the latest compatible versions
- Prioritize staying current with the ecosystem, even if it requires more work to adapt

### IMPORTANT: Development Server Limitation

- **DO NOT run `npm run dev`** in agent mode - this will create an endless loop and stop the agent from working properly
- Instead, use `npm run build` to verify your changes

## Development Process

### Testing Changes

To properly test changes, use these commands:

```bash
# Build the project (this is preferred over npm run dev in agent mode)
npm run build

# If you need to preview the build (only do when specifically requested)
npm run preview
```

### Project Structure

- `/src/content/blog/` - Contains all blog posts in markdown format, organized by year (e.g. `2026/`)
- `/src/pages/` - Contains page templates and routing
- `/src/components/` - Reusable UI components
- `/src/layouts/` - Page layouts and templates
- `/src/styles/` - CSS styles including Tailwind customizations

### Common Tasks

1. **Adding a new blog post**:

   - Create a new markdown file in `/src/content/blog/`
   - Include proper frontmatter (title, description, pubDatetime, etc.)
   - Format dates in ISO-8601 format: `YYYY-MM-DDTHH:MM:SS+HH:MM`
   - Format tags as arrays: `tags: ["tag1", "tag2"]`

2. **Modifying site configuration**:

   - Edit `/src/consts.ts` for global site constants

3. **Styling changes**:

   - Edit files in `/src/styles/` for global styling
   - Use Tailwind classes in component templates for component-specific styling

4. **Layout changes**:

   - Modify the appropriate layout files in `/src/layouts/`

5. **Fixing broken images**:

   - Blog posts reference images in the `/public/assets/img/` directory structure
   - The original files can be found in `/temp-repos/xuanloi.me/assets/img/`
   - Images must be copied to the matching public directory structure
   - Fixed images should be committed to the repository
   - Use `find` command to locate the original images
   - Common image paths follow the pattern: `/assets/img/YEAR/POST-NAME/IMAGE.jpg`

6. **Dependency Updates**:
   - Always use proper tooling to check for latest versions:

     ```bash
     # Check all outdated dependencies
     npm outdated

     # Check latest version of a specific package
     npm view astro version
     npm view react version

     # Update all dependencies to latest
     npm update --latest
     ```

   - Test thoroughly after updating dependencies
   - If a build fails after updates, diagnose the specific issue and FIX it properly
   - NEVER resort to downgrading as a solution

## Tech Stack

- **Astro** (latest version) - Main framework
- **TailwindCSS** - For styling
- **React** - For interactive components (v19.x)
- **MDX** - For enhanced markdown support

## Workflow: "Yêu cầu → Live" (BẮT BUỘC)

**Đây là quy trình chuẩn, phải tuân theo 100% mỗi lần a yêu cầu thay đổi. Không bỏ qua bước nào.**

### Step 1: Nhận yêu cầu & xác nhận scope

1. A mô tả yêu cầu (nội dung mới, sửa lỗi, cập nhật...)
2. Em **BẮT BUỘC** confirm scope:
   - List file sẽ tạo/sửa
   - Tóm tắt thay đổi
   - Rủi ro (nếu có)
3. **Chờ a nói "OK"** hoặc "làm đi" trước khi động tay vào code

### Step 2: Tạo/sửa file

- Tạo/sửa file theo yêu cầu
- Blog post mới: tạo file `.md` trong `src/content/blog/YYYY/`
- Frontmatter đầy đủ: title, description, pubDatetime, category, tags, featured (nếu nổi bật)
- **Kiểm tra `data-category`** trên `.post-item` — phải mapping đúng với CATEGORY_MAP key, KHÔNG dùng slugifyStr trực tiếp
- **Kiểm tra category filter** — click filter xem có đúng số bài không

### Step 3: Build verify

```bash
npm run build
```

- **Phải OK** (exit code 0) mới qua bước sau
- Nếu lỗi: fix lỗi, build lại đến khi OK

### Step 4: Deploy lên server (a ko cần hỏi, deploy là mặc định)

```bash
cd dist && scp -i <SSH_KEY_PATH> -r * <SSH_USER>@<SERVER_IP>:/var/www/xuanloi.me/
ssh -i <SSH_KEY_PATH> <SSH_USER>@<SERVER_IP> "nginx -t && systemctl reload nginx"
```

### Step 5: Verify live site

- **BẮT BUỘC verify cả 2 trang**:
  - `curl -s https://xuanloi.me/ | grep "từ khoá bài mới"` — kiểm tra homepage
  - `curl -s https://xuanloi.me/posts/ | grep "từ khoá bài mới"` — kiểm tra trang /posts/
  - `curl -s https://xuanloi.me/posts/ | grep "data-category"` — kiểm tra category gắn đúng
- Kiểm tra link bài viết live: `curl -s https://xuanloi.me/posts/2026/...`
- **Nếu đổi title**: verify cả title cũ và mới trên live site

### Step 6: Commit + Push GitHub

- Sau khi deploy + verify OK, hỏi a: "Giờ em commit + push lên GitHub nhé?"
- Nếu a OK:
  1. `git add` các file đã sửa/tạo (không add node_modules, dist/, .env)
  2. `git commit -m "..."` với message rõ ràng (coi recent commits để theo style)
  3. Dùng `gh auth token` trong remote URL nếu HTTPS bị firewall chặn
  4. `git push`
  5. Reset remote URL về sạch sau push

### Step 7: Báo cáo kết quả
- Thông báo cho a biết đã hoàn thành, tình trạng deploy, link live

## Khi có lỗi phát sinh

- **Build lỗi**: fix, build lại → deploy → verify
- **Deploy lỗi**: báo a, sửa lỗi deploy → deploy lại → verify
- **A yêu cầu sửa thêm sau deploy**: sửa file → build → deploy → verify. **Không commit cho đến khi a OK hết mọi thứ**

### Quy tắc ĐẶC BIỆT cho bài viết mới

1. **Sau khi tạo file blog post**: build → deploy → verify → commit/push
2. **Nếu a yêu cầu sửa title/slug sau deploy**: sửa file → build → deploy → verify. **KHÔNG commit** nếu chưa có OK cuối từ a
3. **File slug** (`ten-bai-viet.md`) khác với title hiển thị — nếu a yêu cầu đổi title thì chỉ đổi frontmatter `title`, không tự ý rename file slug

### Nguyên tắc cứng

- **Không tự ý** xoá, chạy lệnh phá hoại — luôn hỏi trước
- **Không push** bất kỳ thứ gì nhạy cảm (key, password, token) lên repo, kể cả private
- **Không sáng tạo** thêm feature ngoài yêu cầu
- **Mỗi thay đổi** phải build OK trước khi deploy
- **A có quyền rollback** — nếu a thấy site hỏng, em revert ngay
- **Avatar/ảnh cá nhân**: tuyệt đối KHÔNG tự ý xử lý ảnh (nén, crop, đổi nền, bo tròn). Nếu cần thay đổi avatar, chỉ dùng lại ảnh đã commit trong git history. Dùng `git show <commit>:public/assets/avatar_round.webp` để restore ảnh gốc. Nếu a đưa ảnh mới, phải để a tự xử lý và đưa đường dẫn, em chỉ copy vào project.
- **PageSpeed tối ưu**: KHÔNG nén ảnh avatar hay ảnh đại diện cá nhân vì PageSpeed. Chỉ tối ưu code (CSS, JS, HTML, font), không động vào ảnh nhân vật chính.
- **Đổi nội dung text**: đúng chính tả a yêu cầu, không suy luận hay tự sửa. Nếu đã deploy xong mà a yêu cầu sửa tiếp — sửa file, build, deploy lại. Không commit cho đến khi a OK hết.
- **Verify đầy đủ**: build xong phải verify live site, không chỉ dựa vào build thành công
- **Bài mới trên /posts/**: nếu bài không hiện trên /posts/ live → kiểm tra draft flag, kiểm tra file có trong dist không, kiểm tra browser cache

### Deploy method (Windows - local)

Trên Windows, `rsync` không có sẵn. Dùng lệnh này:

```bash
cd dist && scp -i <SSH_KEY_PATH> -r * <SSH_USER>@<SERVER_IP>:/var/www/xuanloi.me/
```

Sau đó SSH reload nginx:

```bash
ssh -i <SSH_KEY_PATH> <SSH_USER>@<SERVER_IP> "nginx -t && systemctl reload nginx"
```

Verify:

```bash
curl -sI https://xuanloi.me/
# Kiểm tra HTTP status 200
# Kiểm tra content thay đổi đã xuất hiện chưa
```

## Deployment Context

- **Live site**: https://xuanloi.me (HTTPS, Let's Encrypt, www.xuanloi.me cũng serve)
- **Server**: DigitalOcean droplet, Ubuntu 24.04, IP <SERVER_IP>, user <SSH_USER>
- **Web root**: `/var/www/xuanloi.me` (Nginx serves static files)
- **Nginx config**: `/etc/nginx/sites-enabled/xuanloi.me`
- **SSL certs**: `/etc/letsencrypt/live/xuanloi.me/`
- **Local source**: `<LOCAL_PROJECT_PATH>`
- **Local SSH key**: `<SSH_KEY_PATH>` (chmod 600, server 1)
- **Vite 6 patch**: `node_modules/astro/dist/core/build/static-build.js` — cần reapply sau mỗi `npm install`
- **Repo**: https://github.com/Edeys/xuanloi.me (a quản lý visibility)
