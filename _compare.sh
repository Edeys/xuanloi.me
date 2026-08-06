#!/bin/bash
echo "=== Server metrics ==="
echo "HTML raw: $(wc -c < /var/www/xuanloi.me/posts/2026/tuoi-tre-khong-tien-khong-nguoi-hau-thuan/index.html) bytes"
echo "_astro CSS:"
ls -1 /var/www/xuanloi.me/_astro/*.css | while read f; do echo "  $(wc -c < $f) $(basename $f)"; done
echo "_astro JS:"
ls -1 /var/www/xuanloi.me/_astro/*.js | while read f; do echo "  $(wc -c < $f) $(basename $f)"; done
echo "Gzip test:"
curl -sL -o /dev/null -w "  gzipped: %{size_download} bytes, TTFB: %{time_starttransfer}s\n" -H 'Accept-Encoding: gzip' --compressed https://xuanloi.me/posts/2026/tuoi-tre-khong-tien-khong-nguoi-hau-thuan
echo "No-gzip test:"
curl -sL -o /dev/null -w "  raw: %{size_download} bytes, TTFB: %{time_starttransfer}s\n" https://xuanloi.me/posts/2026/tuoi-tre-khong-tien-khong-nguoi-hau-thuan
