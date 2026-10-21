#!/usr/bin/env bash
# Usage: ./update.sh ["commit message"]
set -e
cd "$(dirname "$0")"

msg="${1:-update $(date '+%Y-%m-%d %H:%M')}"

git add -A
if git diff --cached --quiet; then
  echo "Nothing to commit."
else
  git commit -m "$msg"
fi
git push origin HEAD
