#!/usr/bin/env node
/**
 * perf-guard.mjs — Performance guard for xuanloi.me
 *
 * Two layers:
 *  1. LOCAL bundle check (fast, runs after every build):
 *     compares dist/_astro JS+CSS totals against perf-baseline.json.
 *  2. PSI check (slow, ~30-60s per URL; run with --psi):
 *     calls PageSpeed Insights API and compares against thresholds.
 *
 * Usage:
 *   node scripts/perf-guard.mjs              # bundle check (warn only)
 *   node scripts/perf-guard.mjs --psi        # bundle + PSI check
 *   node scripts/perf-guard.mjs --baseline   # write new perf-baseline.json
 *   node scripts/perf-guard.mjs --fail       # exit 1 on any violation
 *
 * Exit codes: 0 = ok (or warn-only), 1 = violation (with --fail), 2 = error.
 */
import { readFileSync, writeFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dir, "..");
const BASELINE_PATH = join(ROOT, "perf-baseline.json");

// Thresholds (lab, mobile, throttled)
const THRESHOLDS = {
  psiPerformance: 85, // Lighthouse performance score (0-100)
  lcpMs: 3000,        // Largest Contentful Paint
  cls: 0.1,           // Cumulative Layout Shift
  tbtMs: 300,         // Total Blocking Time
};

// Bundle growth limit vs baseline (%)
const BUNDLE_GROWTH_PCT = 20;

// URLs checked by --psi (home + one representative post)
const PSI_URLS = [
  "https://xuanloi.me/",
  "https://xuanloi.me/posts/2026/so-chon-sai-nghe/",
];

const PSI_KEY = process.env.PSI_API_KEY || "";
const useFail = process.argv.includes("--fail");
const runPsi = process.argv.includes("--psi");
const writeBaseline = process.argv.includes("--baseline");

let violations = 0;
const log = (level, msg) => console.log(`[perf-guard] ${level}: ${msg}`);
const kb = (n) => (n / 1024).toFixed(1);

async function bundleCheck() {
  const dir = join(ROOT, "dist", "_astro");
  if (!existsSync(dir)) {
    log("WARN", "dist/_astro not found - run `npm run build` first");
    return;
  }
  const entries = readdirSync(dir)
    .map((name) => {
      const st = statSync(join(dir, name));
      return { name, size: st.size, isFile: st.isFile() };
    })
    .filter((e) => e.isFile && /\.(js|css)$/.test(e.name));

  const totalJs = entries.filter((e) => e.name.endsWith(".js")).reduce((s, e) => s + e.size, 0);
  const totalCss = entries.filter((e) => e.name.endsWith(".css")).reduce((s, e) => s + e.size, 0);
  const total = totalJs + totalCss;

  log("INFO", `bundle: JS=${kb(totalJs)}KB CSS=${kb(totalCss)}KB total=${kb(total)}KB (${entries.length} files)`);

  if (writeBaseline) return { total, entries };

  if (!existsSync(BASELINE_PATH)) {
    log("WARN", "no perf-baseline.json yet - run `npm run perf:baseline`");
    return;
  }
  const baseline = JSON.parse(readFileSync(BASELINE_PATH, "utf-8"));
  const growth = ((total - baseline.bundleTotal) / baseline.bundleTotal) * 100;
  if (growth > BUNDLE_GROWTH_PCT) {
    violations++;
    log("FAIL", `bundle grew ${growth.toFixed(1)}% (${kb(baseline.bundleTotal)}KB -> ${kb(total)}KB), limit ${BUNDLE_GROWTH_PCT}%`);
  } else {
    log("OK", `bundle change ${growth >= 0 ? "+" : ""}${growth.toFixed(1)}% vs baseline`);
  }

  const top = [...entries].sort((a, b) => b.size - a.size).slice(0, 5);
  for (const e of top) {
    log("INFO", `  ${kb(e.size)}KB  ${e.name}`);
  }
}

async function psiCheck() {
  if (!PSI_KEY) {
    log("WARN", "PSI_API_KEY not set - skipping PSI check (set env PSI_API_KEY to enable)");
    return;
  }
  log("INFO", `PSI check (${PSI_URLS.length} URLs, ~30-60s each)...`);
  for (const url of PSI_URLS) {
    const api = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(url)}&strategy=mobile&key=${PSI_KEY}`;
    try {
      const resp = await fetch(api, { signal: AbortSignal.timeout(120000) });
      const data = await resp.json();
      const lh = data.lighthouseResult;
      if (!lh) {
        log("WARN", `${url}: API error ${JSON.stringify(data.error || {}).slice(0, 150)}`);
        continue;
      }
      const aud = lh.audits;
      const perf = Math.round((lh.categories.performance?.score ?? 0) * 100);
      const lcpMs = aud["largest-contentful-paint"]?.numericValue ?? 0;
      const lcp = aud["largest-contentful-paint"]?.displayValue ?? "N/A";
      const cls = aud["cumulative-layout-shift"]?.numericValue ?? 0;
      const tbt = aud["total-blocking-time"]?.numericValue ?? 0;

      log("INFO", `${url} | PERF=${perf} | LCP=${lcp} | CLS=${cls.toFixed(3)} | TBT=${tbt}ms`);

      if (perf < THRESHOLDS.psiPerformance) {
        violations++;
        log("FAIL", `${url}: PERF ${perf} < ${THRESHOLDS.psiPerformance}`);
      }
      if (lcpMs > THRESHOLDS.lcpMs) {
        violations++;
        log("FAIL", `${url}: LCP ${lcpMs}ms > ${THRESHOLDS.lcpMs}ms`);
      }
      if (cls > THRESHOLDS.cls) {
        violations++;
        log("FAIL", `${url}: CLS ${cls.toFixed(3)} > ${THRESHOLDS.cls}`);
      }
      if (tbt > THRESHOLDS.tbtMs) {
        violations++;
        log("FAIL", `${url}: TBT ${tbt}ms > ${THRESHOLDS.tbtMs}ms`);
      }
    } catch (e) {
      log("WARN", `${url}: ${e.message}`);
    }
  }
}

async function main() {
  console.log("=== perf-guard ===");

  if (writeBaseline) {
    const result = await bundleCheck();
    if (!result) process.exit(2);
    const baseline = {
      createdAt: new Date().toISOString(),
      bundleTotal: result.total,
      bundleFiles: result.entries.length,
      thresholds: THRESHOLDS,
    };
    writeFileSync(BASELINE_PATH, JSON.stringify(baseline, null, 2), "utf-8");
    log("OK", `baseline written: ${kb(result.total)}KB (${result.entries.length} files)`);
    process.exit(0);
  }

  await bundleCheck();
  if (runPsi) {
    await psiCheck();
  } else {
    log("INFO", "PSI check skipped (add --psi to include; ~1-2 min)");
  }

  if (violations > 0) {
    log("SUMMARY", `${violations} violation(s) found`);
    if (useFail) process.exit(1);
    log("INFO", "warn-only mode (--fail to block)");
  } else {
    log("OK", "all checks passed");
  }
  process.exit(0);
}

main().catch((e) => {
  console.error("[perf-guard] ERROR:", e.message);
  process.exit(2);
});
