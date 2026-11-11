#!/usr/bin/env bash
# one-command run: sets up the environment (first time only), then the whole pipeline
# usage:  bash quickstart.sh
set -euo pipefail
cd "$(dirname "$0")"

PY=${PYTHON:-python3.13}          # torch may not support the newest python yet
if [ ! -d .venv ]; then
    "$PY" -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
fi

.venv/bin/python data_prep.py
.venv/bin/python linear_reg.py
.venv/bin/python nn_models.py lstm
.venv/bin/python nn_models.py transformer
.venv/bin/python compare.py
