# Xuân Lợi - Personal Website

This is the source code for my personal website, built with [Astro](https://astro.build) and deployed on a DigitalOcean droplet via Nginx.

## About

Mình là Xuân Lợi. Blog cá nhân tiếng Việt về cuộc sống, marketing và những điều mình học được trên hành trình. Forked từ [steipete/steipete.me](https://github.com/steipete/steipete.me) — cảm ơn Peter Steinberger đã open-source codebase.

## Project Structure

```text
├── public/               # Static assets (images, fonts, favicon)
│   ├── assets/          # Images for blog posts
│   └── fonts/           # Web fonts
├── src/
│   ├── assets/          # Icons and images used in components
│   ├── components/      # Reusable UI components
│   │   └── ui/          # React components
│   ├── content/         # Content collections
│   │   └── blog/        # Blog posts in Markdown format (organized by year)
│   ├── layouts/         # Page layouts and templates
│   ├── pages/           # Routes and pages
│   ├── styles/          # Global styles and CSS
│   └── utils/           # Utility functions
├── astro.config.mjs     # Astro configuration
├── vercel.json          # Redirect rules (also used for Vercel compatibility)
├── package.json         # Project dependencies and scripts
├── tailwind.config.mjs  # Tailwind CSS configuration
└── LICENSE              # Dual license (CC BY 4.0 + MIT)
```

## Commands

| Command                | Action                                      |
| :--------------------- | :------------------------------------------ |
| `pnpm install`         | Installs dependencies                       |
| `pnpm run dev`         | Starts local dev server at `localhost:4321` |
| `pnpm run build`       | Build the production site to `./dist/`      |
| `pnpm run preview`     | Preview the build locally, before deploying |

## Deployment

This site is built with `npm run build` and deployed to a DigitalOcean droplet (Nginx serving static files in `/var/www/xuanloi.me`). See `XUANLOI_PROJECT_INFO.md` for full deploy workflow.

## License

This repository uses dual licensing:

- **Documentation & Blog Posts**: Licensed under [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/)
- **Code & Code Snippets**: Licensed under the [MIT License](LICENSE)

See the [LICENSE](LICENSE) file for full details.

## Special Thanks

Special thanks to [Sat Naing](https://github.com/satnaing) for creating the excellent [AstroPaper theme](https://astro-paper.pages.dev/) that served as the foundation for this website. Their thoughtful design and clean architecture made it a joy to build upon.
