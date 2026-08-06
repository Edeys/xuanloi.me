// master-uisfx.cjs — Apply all uisfx changes in one pass
const { readFileSync, writeFileSync } = require('fs');
const { resolve } = require('path');

const DIR = resolve('D:/Dự Án Cá Nhân/xuanloi.me');
const NL = '\n'; // consistent LF for matching

function patch(filePath, rules) {
  const full = resolve(DIR, filePath);
  let c = readFileSync(full, 'utf8').replace(/\r\n/g, NL);
  rules.forEach(([from, to]) => {
    if (!c.includes(from)) {
      console.warn('  MISS: ' + filePath + ' — ' + JSON.stringify(from).slice(0,60));
    } else {
      c = c.replace(from, to);
    }
  });
  writeFileSync(full, c, 'utf8');
  console.log('OK ' + filePath);
}

console.log('\n=== Phase 1: Component data attributes ===\n');

// ─── LinkButton ───
patch('src/components/LinkButton.astro', [[
  '      aria-label={ariaLabel}\n      title={title}',
  '      data-uisfx-hover="hover"\n      aria-label={ariaLabel}\n      title={title}'
]]);

// ─── Link ───
patch('src/components/Link.astro', [[
  '  {...isExternal && { target: "_blank", rel: "noopener noreferrer" }}',
  '  data-uisfx-hover="hover"\n  {...isExternal && { target: "_blank", rel: "noopener noreferrer" }}'
]]);

// ─── Card ───
patch('src/components/Card.astro', [[
  'class="inline-block text-lg font-medium text-accent decoration-dashed underline-offset-4 focus-visible:no-underline focus-visible:underline-offset-0"',
  'class="inline-block text-lg font-medium text-accent decoration-dashed underline-offset-4 focus-visible:no-underline focus-visible:underline-offset-0"\n      data-uisfx="select" data-uisfx-hover="hover"'
]]);

// ─── Header ───
patch('src/components/Header.astro', [
  [
    '  <a\n    id="skip-to-content"\n    href="#main-content"',
    '  <a\n    id="skip-to-content"\n    data-uisfx="focus"\n    href="#main-content"'
  ],
  [
    '      <a\n        href="/"\n        class="absolute py-1 text-2xl',
    '      <a\n        href="/"\n        data-uisfx="navigate"\n        data-uisfx-hover="hover"\n        class="absolute py-1 text-2xl'
  ],
  [
    '<a href="/posts" class:list={{ "active-nav": isActive("/posts") }}',
    '<a href="/posts" class:list={{ "active-nav": isActive("/posts") }} data-uisfx="navigate" data-uisfx-hover="hover"'
  ],
  [
    '<a href="/about" class:list={{ "active-nav": isActive("/about") }}',
    '<a href="/about" class:list={{ "active-nav": isActive("/about") }} data-uisfx="navigate" data-uisfx-hover="hover"'
  ],
  [
    '            <LinkButton\n              href="/search"',
    '            <span data-uisfx="focus">\n              <LinkButton\n                href="/search"'
  ],
  [
    '              </LinkButton>\n          </li>\n          {\n            SITE.lightAndDarkMode',
    '              </LinkButton>\n            </span>\n          </li>\n          {\n            SITE.lightAndDarkMode'
  ],
]);

// ─── Socials ───
patch('src/components/Socials.astro', [[
  '<div class:list={["flex-wrap justify-center gap-1", { flex: centered }]}>',
  '<div class:list={["flex-wrap justify-center gap-1", { flex: centered }]} data-uisfx="press">'
]]);

// ─── ShareLinks ───
patch('src/components/ShareLinks.astro', [[
  'class="flex flex-col flex-wrap items-center justify-center gap-2 sm:gap-1 sm:items-start"',
  'class="flex flex-col flex-wrap items-center justify-center gap-2 sm:gap-1 sm:items-start"\n  data-uisfx="press"'
]]);

// ─── Pagination ───
patch('src/components/Pagination.astro', [
  [
    '    <nav class="mt-auto mb-8 flex justify-center" aria-label="Pagination">\n      <LinkButton\n        disabled={!page.url.prev}',
    '    <nav class="mt-auto mb-8 flex justify-center" aria-label="Pagination">\n      <span data-uisfx="back">\n        <LinkButton\n          disabled={!page.url.prev}'
  ],
  [
    '      <LinkButton\n        disabled={!page.url.next}',
    '      <span data-uisfx="forward">\n        <LinkButton\n          disabled={!page.url.next}'
  ],
  [
    '      </LinkButton>\n    </nav>',
    '      </LinkButton>\n      </span>\n      </span>\n    </nav>'
  ],
]);

// ─── BackButton ───
patch('src/components/BackButton.astro', [
  [
    '      <LinkButton\n        id="back-button"',
    '      <span data-uisfx="back">\n        <LinkButton\n          id="back-button"'
  ],
  [
    '      </LinkButton>\n    </div>',
    '      </LinkButton>\n      </span>\n    </div>'
  ],
]);

// ─── Breadcrumb ───
patch('src/components/Breadcrumb.astro', [
  ['<a href="/" class="opacity-80">', '<a href="/" class="opacity-80" data-uisfx="navigate" data-uisfx-hover="hover">'],
  ['class="capitalize opacity-70">', 'class="capitalize opacity-70" data-uisfx="navigate" data-uisfx-hover="hover">'],
]);

// ─── Tag ───
patch('src/components/Tag.astro', [[
  '<a\n    href={`/tags/',
  '<a\n    data-uisfx="select" data-uisfx-hover="hover"\n    href={`/tags/'
]]);

// ─── 404 ───
patch('src/pages/404.astro', [
  [
    '      <LinkButton\n        href="/"',
    '      <span data-uisfx="navigate">\n        <LinkButton\n          href="/"'
  ],
  [
    '      </LinkButton>\n    </div>\n  </main>',
    '      </LinkButton>\n      </span>\n    </div>\n  </main>'
  ],
]);

// ─── 500 ───
patch('src/pages/500.astro', [
  [
    '      <LinkButton href="/" class=',
    '      <span data-uisfx="navigate">\n        <LinkButton href="/" class='
  ],
  [
    '      </LinkButton>\n    </div>\n  </main>',
    '      </LinkButton>\n      </span>\n    </div>\n  </main>'
  ],
]);

console.log('\n=== Phase 2: Layout UISFX init ===\n');

// ─── Layout ───
let layout = readFileSync(resolve(DIR, 'src/layouts/Layout.astro'), 'utf8').replace(/\r\n/g, NL);
const uisfxScript = [
  '',
  '<script>',
  '  import { createUISFX, bindUISFX } from "uisfx";',
  '',
  '  let ui;',
  '',
  '  function initPlayer() {',
  '    if (ui) return ui;',
  '    ui = createUISFX({ pack: "zen", volume: 0.6, preferences: { key: "xuanloi:uisfx" } });',
  '    function unlock() {',
  '      ui.unlock();',
  '      document.removeEventListener("pointerdown", unlock);',
  '      document.removeEventListener("keydown", unlock);',
  '    }',
  '    document.addEventListener("pointerdown", unlock, { once: true });',
  '    document.addEventListener("keydown", unlock, { once: true });',
  '    bindUISFX(document, { player: ui });',
  '    return ui;',
  '  }',
  '',
  '  function hookCustomSounds() {',
  '    if (!ui) ui = initPlayer();',
  '',
  '    var themeBtn = document.getElementById("theme-btn");',
  '    if (themeBtn && !themeBtn.dataset.uisfxWired) {',
  '      themeBtn.dataset.uisfxWired = "1";',
  '      themeBtn.addEventListener("click", function() {',
  '        var cur = document.documentElement.getAttribute("data-theme");',
  '        ui.play(cur === "light" ? "toggle-on" : "toggle-off");',
  '      });',
  '    }',
  '',
  '    var menuBtn = document.getElementById("menu-btn");',
  '    if (menuBtn && !menuBtn.dataset.uisfxWired) {',
  '      menuBtn.dataset.uisfxWired = "1";',
  '      menuBtn.addEventListener("click", function() {',
  '        var exp = menuBtn.getAttribute("aria-expanded") === "true";',
  '        ui.play(exp ? "expand" : "collapse");',
  '      });',
  '    }',
  '',
  '    var nl = document.getElementById("subscribe-form");',
  '    if (nl && !nl.dataset.uisfxWired) {',
  '      nl.dataset.uisfxWired = "1";',
  '      nl.addEventListener("submit", function() { ui.play("send"); });',
  '    }',
  '',
  '    var modal = document.getElementById("subscribe-modal");',
  '    if (modal && !modal.dataset.uisfxWired) {',
  '      modal.dataset.uisfxWired = "1";',
  '      var obs = new MutationObserver(function(muts) {',
  '        for (var i = 0; i < muts.length; i++) {',
  '          var m = muts[i];',
  '          if (m.type === "attributes" && m.attributeName === "style") {',
  '            if (modal.style.opacity === "1") ui.play("success");',
  '          }',
  '        }',
  '      });',
  '      obs.observe(modal, { attributes: true, attributeFilter: ["style"] });',
  '    }',
  '',
  '    if (!document.body.dataset.uisfxSearchWired) {',
  '      document.body.dataset.uisfxSearchWired = "1";',
  '      document.addEventListener("focusin", function(e) {',
  '        if (e.target.classList.contains("pagefind-ui__search-input")) ui.play("focus");',
  '      });',
  '    }',
  '',
  '    if (!document.body.dataset.uisfxTocWired) {',
  '      document.body.dataset.uisfxTocWired = "1";',
  '      document.addEventListener("click", function(e) {',
  '        if (e.target.classList.contains("toc-link")) ui.play("select");',
  '      });',
  '    }',
  '  }',
  '',
  '  initPlayer();',
  '  hookCustomSounds();',
  '  document.addEventListener("astro:after-swap", hookCustomSounds);',
  '</script>',
].join(NL);

// Insert before </body>
layout = layout.replace('  </body>', '  ' + uisfxScript.split(NL).map(l => '  ' + l).join(NL) + NL + '  </body>');
writeFileSync(resolve(DIR, 'src/layouts/Layout.astro'), layout, 'utf8');
console.log('OK Layout.astro (script embedded before </body>)');

console.log('\n=== ALL DONE ===');
