#!/usr/bin/env bash
# Preview the site on this Mac at http://localhost:4000
# Shows EVERYTHING, including scheduled sketches and drafts (they get a small label).
#   tools/preview.sh          -> everything
#   tools/preview.sh --live   -> only what the public site shows right now
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v bundle >/dev/null; then
  echo "Ruby/Bundler not found. Run once:  brew install ruby  (then follow brew's PATH note)"; exit 1
fi
bundle config set --local path vendor/bundle >/dev/null
bundle install --quiet
if [ "${1:-}" = "--live" ]; then
  bundle exec jekyll serve --livereload
else
  bundle exec jekyll serve --livereload --future --unpublished
fi
