#!/usr/bin/env bash
# One command to publish:  imports any photos in inbox/, shows the schedule,
# commits everything and pushes. GitHub then rebuilds the site; scheduled
# sketches go live by themselves at their publish_on time.
#   tools/publish.sh "optional commit message"
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/add_sketches.py
echo
python3 tools/schedule.py
echo
git add -A
if git diff --cached --quiet; then
  echo "Nothing new to publish."
else
  git commit -q -m "${1:-Update Mami's Musings}"
  git push -q
  echo "Pushed. Site rebuilds in ~1–2 minutes: https://mamismusings.github.io"
fi
