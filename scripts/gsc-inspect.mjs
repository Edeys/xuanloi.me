#!/usr/bin/env node
/**
 * gsc-inspect.mjs — Submit sitemap + inspect URL index status via GSC API.
 * Reuses service account JWT auth (same as gsc-baseline.mjs).
 * Usage: node scripts/gsc-inspect.mjs [--inspect] [--submit]
 */
import { readFileSync, existsSync } from "node:fs";
import { createPrivateKey, sign } from "node:crypto";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const CONFIG = join(__dir, "gsc-config.json");
const SITE_KEY = "sc-domain:xuanloi.me";
const POSTS = [
  "vi-sao-nguoi-gioi-lai-kho-len-tieng-nhat",
  "so-chon-sai-nghe",
  "self-help-trap",
  "not-to-do-list-xay-thuong-hieu-ca-nhan",
  "17-cau-hoi-thay-doi-cuoc-doi",
  "cang-lon-cang-kho-yeu",
  "bat-dau-voi-marketing-so",
  "8-thu-tot-hon-ca-mien-phi-trong-thoi-tri-tue-nhan-tao",
  "23-ban-nhap-8-thang-0-bai-dang",
  "bai-hoc-phat-trien-ban-than",
  "khoanh-khac-nhan-ra-suc-khoe-bi-hong",
  "bai-tap-dinh-hinh-noi-so",
  "dau-tu-nong-nghiep-cai-bay-cua-nhung-nguoi-nghi-minh-thong-minh",
  "tuoi-tre-khong-tien-khong-nguoi-hau-thuan",
  "tai-sao-muon-tien-len-mai-khong-lam-duoc",
  "ty-phu-xe-om-chan-ly-ve-dat-nong-nghiep",
  "dem-khong-ngu-vi-kich-ban-trong-dau",
];
const ROOT_POSTS = ["bat-dau-voi-marketing-so", "bai-hoc-phat-trien-ban-than", "khoanh-khac-nhan-ra-suc-khoe-bi-hong", "bai-tap-dinh-hinh-noi-so", "tai-sao-muon-tien-len-mai-khong-lam-duoc"];
const BLOG_URL = (slug) => ROOT_POSTS.includes(slug) ? `https://xuanloi.me/posts/${slug}/` : `https://xuanloi.me/posts/2026/${slug}/`;

function fatal(msg) { console.error(`\n[GSC] ${msg}\n`); process.exit(1); }
if (!existsSync(CONFIG)) fatal("Missing scripts/gsc-config.json");
const cfg = JSON.parse(readFileSync(CONFIG, "utf-8"));
const key = JSON.parse(readFileSync(cfg.key, "utf-8"));
const siteUrl = cfg.siteUrl || SITE_KEY;

const SCOPE = process.argv.includes("--submit") || process.argv.includes("--inspect")
  ? "https://www.googleapis.com/auth/webmasters"
  : "https://www.googleapis.com/auth/webmasters.readonly";

function makeJwt() {
  const now = Math.floor(Date.now() / 1000);
  const header = Buffer.from(JSON.stringify({ alg: "RS256", typ: "JWT" })).toString("base64url");
  const claims = Buffer.from(JSON.stringify({
    iss: key.client_email,
    scope: SCOPE,
    aud: "https://oauth2.googleapis.com/token",
    iat: now, exp: now + 3600,
  })).toString("base64url");
  const sig = sign("RSA-SHA256", Buffer.from(`${header}.${claims}`), createPrivateKey(key.private_key));
  return `${header}.${claims}.${sig.toString("base64url")}`;
}

async function getToken() {
  const r = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: makeJwt() }),
  });
  const j = await r.json();
  if (!j.access_token) fatal(`Token failed: ${JSON.stringify(j)}`);
  return j.access_token;
}

const doSubmit = process.argv.includes("--submit");
const doInspect = process.argv.includes("--inspect");

async function main() {
  const token = await getToken();
  console.log("[GSC] Auth OK\n");

  if (doSubmit) {
    // Sitemaps need write scope; try submit (readonly scope may reject)
    try {
      const r = await fetch(`https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/sitemaps/https%3A%2F%2Fxuanloi.me%2Fsitemap-index.xml`, {
        method: "PUT",
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log(`[GSC] Sitemap submit: HTTP ${r.status} ${r.status === 200 ? "OK (submitted)" : await r.text()}`);
    } catch (e) {
      console.log(`[GSC] Sitemap submit failed: ${e.message}`);
    }
  }

  // List current sitemaps
  const lr = await fetch(`https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/sitemaps`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const lj = await lr.json();
  if (lr.ok) {
    console.log("[GSC] Sitemaps in GSC:");
    for (const s of lj.sitemap || []) {
      console.log(`  ${s.path} | submitted=${s.isPending ? "pending" : "ok"} | lastDownloaded=${s.lastDownloaded || "never"} | errors=${s.errors || 0}`);
    }
  } else {
    console.log(`[GSC] List sitemaps: HTTP ${lr.status} ${JSON.stringify(lj)}`);
  }
  console.log();

  if (doInspect) {
    console.log(`[GSC] Inspecting ${POSTS.length} URLs (URL Inspection API)...\n`);
    const ok = [];
    for (const slug of POSTS) {
      const url = BLOG_URL(slug);
      const r = await fetch(`https://searchconsole.googleapis.com/webmasters/v3/urlInspection/index/inspect`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ inspectionUrl: url, siteUrl }),
      });
      const j = await r.json();
      if (r.ok && j.inspectionResult) {
        const d = j.inspectionResult;
        const state = d.indexStatusResult?.coverageState || "?";
        const verdict = d.indexStatusResult?.robotsTxtState || "?";
        const indexing = d.indexStatusResult?.indexingState || "?";
        const lastCrawl = d.indexStatusResult?.lastCrawlTime || "-";
        const firstSeen = d.indexStatusResult?.pageFetchState || "?";
        ok.push({ slug, state, verdict, indexing, lastCrawl: (lastCrawl || "").slice(0, 10) });
        console.log(`${state.padEnd(28)} ${verdict.padEnd(12)} ${indexing.padEnd(12)} crawled=${(lastCrawl || "-").slice(0, 10)}  /posts/${slug}`);
      } else {
        console.log(`ERR ${url}: ${JSON.stringify(j).slice(0, 160)}`);
      }
      await new Promise((res) => setTimeout(res, 250)); // rate limit
    }
    console.log(`\n[GSC] Done: ${ok.length}/${POSTS.length} inspected`);
  }
}

main().catch((e) => fatal(e.message));
