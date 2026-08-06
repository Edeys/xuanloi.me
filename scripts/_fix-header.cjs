const { readFileSync, writeFileSync } = require('fs');
const NL = '\n';
const DIR = 'D:/Dự Án Cá Nhân/xuanloi.me';

let h = readFileSync(DIR + '/src/components/Header.astro', 'utf8').replace(/\r\n/g, NL);

h = h.replace(
  '              </LinkButton>\n          </li>\n          {\n            SITE.lightAndDarkMode',
  '              </LinkButton>\n            </span>\n          </li>\n          {\n            SITE.lightAndDarkMode'
);

if (!h.includes('            <span data-uisfx="focus">')) {
  h = h.replace(
    '            <LinkButton\n              href="/search"',
    '            <span data-uisfx="focus">\n              <LinkButton\n                href="/search"'
  );
}

writeFileSync(DIR + '/src/components/Header.astro', h, 'utf8');
console.log('Header fixed: span=' + h.includes('</span>') + ' sfx=' + h.includes('data-uisfx'));