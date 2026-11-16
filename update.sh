#!/usr/bin/env bash
# Usage: ./update.sh ["commit message"]
#   no message -> "update YYYY-MM-DD HH:MM"
set -e
cd "$(dirname "$0")"

msg="$*"                                          # all arguments, so quotes are optional
[ -z "$msg" ] && msg="update $(date '+%Y-%m-%d %H:%M')"

git add -A
if git diff --cached --quiet; then
  echo "Nothing to commit."
else
  git commit -m "$msg"
fi
git push origin HEAD
