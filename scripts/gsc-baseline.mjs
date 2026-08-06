#!/usr/bin/env node
/**
 * gsc-baseline.mjs — Pull Google Search Console baseline for xuanloi.me
 * Uses service account JWT (Node builtin crypto, no packages needed).
 *
 * Setup:
 *   1. Create service account + JSON key in Google Cloud Console
 *   2. Add service account email to GSC property (Settings > Users > Add)
 *   3. Save key as scripts/gsc-config.json (gitignored):
 *      { "key": "<path-to-key-json>", "siteUrl": "sc-domain:xuanloi.me", "days": 90 }
 *
 * Usage:
 *   node scripts/gsc-baseline.mjs            # pull baseline -> GSC-BASELINE.csv
 *   node scripts/gsc-baseline.mjs --queries  # also include query dimension
 *   node scripts/gsc-baseline.mjs --pages    # only show pages (no queries)
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { createPrivateKey, sign } from "node:crypto";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const CONFIG = join(__dir, "gsc-config.json");
const SITE_KEY = "sc-domain:xuanloi.me";

const DAYS = 90;
const POST_PREFIX = "https://xuanloi.me/posts/";

function fatal(msg) {
  console.error(`\n[GSC] ${msg}\n`);
  process.exit(1);
}

if (!existsSync(CONFIG)) {
  fatal(
    "Missing scripts/gsc-config.json. Create:\n" +
      '  { "key": "D:/path/to/service-account-key.json", "days": 90 }\n' +
      "See instructions in the top of this script."
  );
}

const cfg = JSON.parse(readFileSync(CONFIG, "utf-8"));
const KEY_PATH = cfg.key;
if (!KEY_PATH || !existsSync(KEY_PATH)) fatal(`Key file not found: ${KEY_PATH}`);

const key = JSON.parse(readFileSync(KEY_PATH, "utf-8"));
const siteUrl = cfg.siteUrl || SITE_KEY;
const days = cfg.days || DAYS;

function makeJwt() {
  const now = Math.floor(Date.now() / 1000);
  const header = Buffer.from(JSON.stringify({ alg: "RS256", typ: "JWT" })).toString("base64url");
  const claims = Buffer.from(
    JSON.stringify({
      iss: key.client_email,
      scope: "https://www.googleapis.com/auth/webmasters.readonly",
      aud: "https://oauth2.googleapis.com/token",
      iat: now,
      exp: now + 3600,
    })
  ).toString("base64url");
  const sig = sign("RSA-SHA256", Buffer.from(`${header}.${claims}`), createPrivateKey(key.private_key));
  return `${header}.${claims}.${sig.toString("base64url")}`;
}

async function getToken() {
  const r = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer",
      assertion: makeJwt(),
    }),
  });
  const j = await r.json();
  if (!j.access_token) fatal(`Token exchange failed: ${JSON.stringify(j)}`);
  return j.access_token;
}

async function queryGSC(token, body) {
  const r = await fetch(`https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/searchAnalytics/query`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const j = await r.json();
  if (!r.ok) fatal(`API error ${r.status}: ${JSON.stringify(j)}`);
  return j.rows || [];
}

const end = new Date();
const start = new Date();
start.setDate(end.getDate() - days);
const fmt = (d) => d.toISOString().slice(0, 10);

async function main() {
  console.log(`[GSC] ${siteUrl} | ${fmt(start)} → ${fmt(end)}`);
  const token = await getToken();
  console.log("[GSC] Token OK");

  const withQueries = process.argv.includes("--queries");
  const pagesOnly = process.argv.includes("--pages");

  // Pull per-page aggregated
  let pageRows = await queryGSC(token, {
    startDate: fmt(start),
    endDate: fmt(end),
    dimensions: ["page"],
    rowLimit: 25000,
  });

  // Pull page+query for keyword insights (only on pages we care about)
  let queryRows = [];
  if (withQueries) {
    const postPages = pageRows
      .filter((r) => r.keys[0] && r.keys[0].startsWith(POST_PREFIX))
      .slice(0, 100); // GSC dim filters max 100 filters in one call... chunk by 25
    const chunks = [];
    for (let i = 0; i < postPages.length; i += 25) chunks.push(postPages.slice(i, i + 25));
    for (const chunk of chunks) {
      const rows = await queryGSC(token, {
        startDate: fmt(start),
        endDate: fmt(end),
        dimensions: ["page", "query"],
        rowLimit: 25000,
        dimensionFilterGroups: [
          {
            groupType: "AND",
            filters: chunk.map((r) => ({
              dimension: "page",
              operator: "equals",
              expression: r.keys[0],
            })),
          },
        ],
      });
      queryRows = queryRows.concat(rows);
    }
  }

  const lines = [];
  lines.push("page,clicks,impressions,ctr,position" + (withQueries ? ",top_query,query_clicks,query_impressions" : ""));
  for (const r of pageRows) {
    const url = r.keys[0];
    const row = [
      url,
      r.clicks ?? 0,
      r.impressions ?? 0,
      r.ctr ? (r.ctr * 100).toFixed(2) : "0.00",
      r.position ? r.position.toFixed(1) : "",
    ];
    if (withQueries) {
      const qs = queryRows
        .filter((q) => q.keys[0] === url)
        .sort((a, b) => (b.clicks ?? 0) - (a.clicks ?? 0));
      const t = qs[0];
      row.push(t ? t.keys[1] : "", t ? String(t.clicks ?? 0) : "", t ? String(t.impressions ?? 0) : "");
    }
    lines.push(row.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(","));
  }

  const out = join(__dir, "..", "GSC-BASELINE.csv");
  writeFileSync(out, "\ufeff" + lines.join("\n"), "utf-8");

  console.log(`[GSC] ${pageRows.length} rows (${postPagesOnly(pageRows, withQueries, queryRows)}) -> ${out}`);
}

function postPagesOnly(pageRows, withQueries, queryRows) {
  const posts = pageRows.filter((r) => r.keys[0].startsWith(POST_PREFIX));
  const qc = queryRows.length;
  return `${posts.length} post pages, ${qc} query rows`;
}

main().catch((e) => fatal(e.message));
