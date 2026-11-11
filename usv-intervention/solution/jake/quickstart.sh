#!/usr/bin/env bash
# one-command run of the linear regressions (Section 3.2 of the Milestone 3 report):
# sets up the environment (first time only), then runs both fits for every window / horizon
# usage:  bash quickstart.sh
set -euo pipefail
cd "$(dirname "$0")"

# python 3.13 if it is installed (same as rowan/quickstart.sh), otherwise python3;
# to pick another one:  PYTHON=python3.12 bash quickstart.sh
PY=${PYTHON:-$(command -v python3.13 || command -v python3)}
if [ ! -d .venv ]; then
    "$PY" -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
fi
PYTHON_BIN="$PWD/.venv/bin/python"

export MPLBACKEND=Agg                        # save each plot as a PNG instead of opening a window
export PYTHONWARNINGS=ignore::UserWarning    # hides matplotlib's "cannot show the plot" notice

# 1. does wind speed drive drift?   drift speed = w * wind speed + b,  speed measured over N minutes
cd linear-reg/drift-vs-wind
for N in 1 5 10 30 60; do
    echo
    echo "=== wind speed -> drift speed, window N = $N min ==="
    "$PYTHON_BIN" linear-reg.py "$N"
done

# 2. past drift + wind -> movement east and north over the next H minutes
cd ../drift-prediction
for H in 1 30 60; do
    echo
    echo "=== past drift + wind -> movement over the next H = $H min ==="
    "$PYTHON_BIN" future.py "$H"
done

echo
echo "Done. The R² values above are the ones in the report; each plot is saved next to its script."
