#!/usr/bin/env bash
# Run ONCE, after creating the empty repo  mamismusings/mamismusings.github.io  on GitHub.
set -euo pipefail
cd "$(dirname "$0")/.."
[ -d .git ] || git init -q -b main
git add -A
git commit -q -m "Mami's Musings: first sketches" || true
git remote get-url origin >/dev/null 2>&1 || git remote add origin https://github.com/mamismusings/mamismusings.github.io.git
git push -u origin main
echo
echo "Now on GitHub: repo Settings → Pages → Build and deployment → Source: GitHub Actions"
