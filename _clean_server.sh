#!/bin/bash
# Remove old _astro files (keep only the current build)
cd /var/www/xuanloi.me/_astro
CURRENT_CSS="Layout.yQ83rrje.css"
CURRENT_JS="client.o2tZFY6j.js ui-core.DyQfjjqj.js ClientRouter.astro_astro_type_script_index_0_lang.CAqDO0tx.js search.astro_astro_type_script_index_0_lang.osm0BDQ0.js"

# Show what will be removed
echo "=== Stale files to remove ==="
for f in *.css; do
  if [ "$f" != "$CURRENT_CSS" ] && [ "$f" != "search.DxDuckVZ.css" ]; then
    echo "CSS: $f"
    rm -f "$f"
  fi
done

# Remove game-audio.mp3 (from original steipete template, not used)
if [ -f /var/www/xuanloi.me/game-audio.mp3 ]; then
  echo "Removing game-audio.mp3 (953KB unused)"
  rm -f /var/www/xuanloi.me/game-audio.mp3
fi

echo "=== Cleaned _astro ==="
ls -la /var/www/xuanloi.me/_astro/
echo "=== Du -sh ==="
du -sh /var/www/xuanloi.me/
