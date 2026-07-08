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

## Workflow: "Yêu cầu → Live"

Quy trình chuẩn khi a yêu cầu chỉnh sửa website:

1. **A mô tả yêu cầu** — sửa cái gì, file nào, link gì, nội dung gì
2. **Em xác nhận scope** — list file sẽ sửa/tạo, tóm tắt thay đổi, rủi ro. A confirm "OK làm" trước khi em sửa
3. **Em sửa local + build verify** — `npm run build` phải OK mới qua bước sau
4. **Em deploy luôn** — a không cần hỏi, deploy là bước mặc định của workflow. SCP `dist/` từ local lên `/var/www/xuanloi.me` qua SSH key `~/.ssh/do-9router`, sau đó reload nginx
5. **Em verify** — curl/check xuanloi.me xác nhận site update
6. **Commit history** — sau khi verify OK, em commit + push code lên GitHub (a chọn push hay không)

### Nguyên tắc cứng

- **Không tự ý** xoá, chạy lệnh phá hoại — luôn hỏi trước
- **Không push** bất kỳ thứ gì nhạy cảm (key, password, token) lên repo, kể cả private
- **Không sáng tạo** thêm feature ngoài yêu cầu
- **Mỗi thay đổi** phải build OK trước khi deploy
- **A có quyền rollback** — nếu a thấy site hỏng, em revert ngay
- **Avatar/ảnh cá nhân**: tuyệt đối KHÔNG tự ý xử lý ảnh (nén, crop, đổi nền, bo tròn). Nếu cần thay đổi avatar, chỉ dùng lại ảnh đã commit trong git history. Dùng `git show <commit>:public/assets/avatar_round.webp` để restore ảnh gốc. Nếu a đưa ảnh mới, phải để a tự xử lý và đưa đường dẫn, em chỉ copy vào project.
- **PageSpeed tối ưu**: KHÔNG nén ảnh avatar hay ảnh đại diện cá nhân vì PageSpeed. Chỉ tối ưu code (CSS, JS, HTML, font), không động vào ảnh nhân vật chính.
- **Đổi nội dung text**: đúng chính tả a yêu cầu, không suy luận hay tự sửa. Nếu đã deploy xong mà a yêu cầu sửa tiếp — sửa file, build, deploy lại. Không commit cho đến khi a OK hết.

### Deploy method

- **Manual SCP** từ local: `rsync -avz --delete -e "ssh -i ~/.ssh/do-9router" dist/ root@129.212.238.158:/var/www/xuanloi.me/`
- Sau đó SSH vào server chạy: `nginx -t && systemctl reload nginx`
- Verify: `curl -sI https://xuanloi.me/`

## Deployment Context

- **Live site**: https://xuanloi.me (HTTPS, Let's Encrypt, www.xuanloi.me cũng serve)
- **Server**: DigitalOcean droplet, Ubuntu 24.04, IP 129.212.238.158, user root
- **Web root**: `/var/www/xuanloi.me` (Nginx serves static files)
- **Nginx config**: `/etc/nginx/sites-enabled/xuanloi.me`
- **SSL certs**: `/etc/letsencrypt/live/xuanloi.me/`
- **Local source**: `D:\Dự Án Cá Nhân\xuanloi.me`
- **Local SSH key**: `~/.ssh/do-9router` (chmod 600, server 1)
- **Vite 6 patch**: `node_modules/astro/dist/core/build/static-build.js` — cần reapply sau mỗi `npm install`
- **Repo**: https://github.com/Edeys/xuanloi.me (a quản lý visibility)
