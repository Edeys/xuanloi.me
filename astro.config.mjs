// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap, { ChangeFreqEnum } from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import { remarkLazyLoadImages } from "./src/utils/remarkLazyLoadImages.mjs";
import { SITE } from "./src/config.ts";

// https://astro.build/config
export default defineConfig({
  site: SITE.website,
  output: "static",
  trailingSlash: "always",
  build: {
    inlineStylesheets: "always",
  },
  devToolbar: {
    enabled: false,
  },
  i18n: {
    defaultLocale: "vi",
    locales: ["vi"],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  markdown: {
    remarkPlugins: [
      remarkToc,
      // @ts-ignore - TypeScript has issues with remark plugin tuple syntax
      [remarkCollapse, { test: "Table of contents" }],
      remarkLazyLoadImages,
    ],
    shikiConfig: {
      // For more themes, visit https://shiki.style/themes
      themes: { light: "min-light", dark: "night-owl" },
      wrap: true,
    },
  },
  integrations: [
    mdx(),
    sitemap({
      filter: (page) => {
        // Always exclude archives if not showing them
        if (!SITE.showArchives && page.endsWith("/archives")) return false;

        // Exclude utility pages (no search-engine value)
        if (page.includes("/admin") || page.includes("/search") || page.includes("/thank-you"))
          return false;

        // Exclude pagination pages (duplicate content)
        if (page.match(/\/page\/\d+\/?$/) || page.match(/\/posts\/\d+\/?$/)) return false;

        return true;
      },
      serialize: (item) => {
        const url = item.url;

        // Set defaults
        item.changefreq = ChangeFreqEnum.MONTHLY;
        item.priority = 0.5;

        // Homepage - highest priority, frequent updates
        if (url === SITE.website || url === SITE.website + "/") {
          item.priority = 1.0;
          item.changefreq = ChangeFreqEnum.DAILY;
          item.lastmod = new Date().toISOString();
        }
        // Main section pages
        else if (url.endsWith("/posts") || url.endsWith("/about") || url.endsWith("/search")) {
          item.priority = 0.9;
          item.changefreq = ChangeFreqEnum.WEEKLY;
        }
        // Recent blog posts (2024-2025)
        else if (url.includes("/posts/2025") || url.includes("/posts/2024")) {
          item.priority = 0.8;
          item.changefreq = ChangeFreqEnum.WEEKLY;
        }
        // Somewhat recent posts (2020-2023)
        else if (
          url.includes("/posts/2023") ||
          url.includes("/posts/2022") ||
          url.includes("/posts/2021") ||
          url.includes("/posts/2020")
        ) {
          item.priority = 0.6;
          item.changefreq = ChangeFreqEnum.MONTHLY;
        }
        // Older posts (2010-2019)
        else if (url.includes("/posts/201")) {
          item.priority = 0.4;
          item.changefreq = ChangeFreqEnum.YEARLY;
        }
        // Tag pages - low priority
        else if (url.includes("/tags/")) {
          item.priority = 0.1;
          item.changefreq = ChangeFreqEnum.YEARLY;
        }
        // Pagination pages
        else if (url.match(/\/page\/\d+$/)) {
          item.priority = 0.4;
          item.changefreq = ChangeFreqEnum.WEEKLY;
        }

        // Note: lastmod dates for individual posts would need to be set
        // from the actual post data, which requires more complex integration

        return item;
      },
    }),
  ],
  vite: {
    resolve: {
      alias: {
        "@": "/src",
      },
    },
    plugins: [tailwindcss()],
    optimizeDeps: {
      exclude: ["@resvg/resvg-js"],
    },
  },
});
