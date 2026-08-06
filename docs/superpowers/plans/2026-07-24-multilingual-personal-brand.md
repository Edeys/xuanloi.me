# Multilingual Personal Brand Portal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild xuanloi.me as a multilingual (vi/en/ko) personal brand portal with domain redirect eddyloi.com → xuanloi.me, deployed via Vercel.

**Architecture:** Astro 6 static site with i18n routing (`/vi/`, `/en/`, `/ko/`), shared component system, content collections per locale, Vercel deployment with CI/CD.

**Tech Stack:** Astro 6, Tailwind 4, React 19, TypeScript, Zod, Vercel, pnpm

---

## Task 1: Set up multilingual project structure

**Files:**
- Modify: `astro.config.mjs`
- Create: `src/i18n/index.ts`
- Create: `src/i18n/ui.ts`
- Create: `src/i18n/utils.ts`
- Modify: `package.json`
- Create: `public/vi/`, `public/en/`, `public/ko/`

### 1.1 Install & configure Astro i18n
### 1.2 Create locale definitions (vi, en, ko)
### 1.3 Update astro.config.mjs for multilingual routing
### 1.4 Create locale switcher component
### 1.5 Set up shared layouts per locale

---

## Task 2: Domain redirects (eddyloi.com → xuanloi.me)

**Files:**
- Create: `vercel.json`

### 2.1 Create Vercel config with domain redirects
### 2.2 Add Vercel adapter to Astro

...

(truncated - saving full plan)
