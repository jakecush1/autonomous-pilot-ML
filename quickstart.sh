#!/usr/bin/env bash
# one-command run: sets up the environment (first time only), then runs every step of the project
# usage:  bash quickstart.sh            everything
#         bash quickstart.sh fits       one step: fits | prep | baselines | lstm | transformer | compare
set -euo pipefail
cd "$(dirname "$0")"

# python 3.13 if it is installed, otherwise python3 (torch may not support the newest python yet);
# to pick another one:  PYTHON=python3.12 bash quickstart.sh
PY=${PYTHON:-$(command -v python3.13 || command -v python3)}
if [ ! -d .venv ]; then
    "$PY" -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt      # takes a moment when everything is already installed

.venv/bin/python src/main.py "$@"
