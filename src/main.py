#!/usr/bin/env python3
"""Runs the project: every step in order, or only the steps you name.

    python src/main.py                every step
    python src/main.py fits           linear regressions for every window N and horizon H
    python src/main.py prep           build the 60-minute windows:  data/raw -> data/preprocessed
    python src/main.py baselines      no drift, persistence and linear regression
    python src/main.py lstm           train and score the LSTM
    python src/main.py transformer    train and score the transformer
    python src/main.py compare        results table and chart

Trained models are saved in output/, scores and charts in evaluation/results/.
"""
import os
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)

FIT_WINDOWS = [1, 5, 10, 30, 60]      # N, minutes: drift speed is measured over this window
FIT_HORIZONS = [1, 30, 60]            # H, minutes: how far ahead the linear fit predicts


def banner(text):
    print(f"\n=== {text} ===", flush=True)


def fits():
    """the two exploratory linear regressions (Section 3.2 of the Milestone 3 report)"""
    # each fit is its own script; here the plots are saved without opening a window
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONWARNINGS="ignore::UserWarning")
    for n in FIT_WINDOWS:
        banner(f"wind speed -> drift speed, window N = {n} min")
        script = os.path.join(SRC, "linear_fits", "drift_vs_wind.py")
        subprocess.run([sys.executable, script, str(n)], check=True, env=env)
    for h in FIT_HORIZONS:
        banner(f"past drift + wind -> movement over the next H = {h} min")
        script = os.path.join(SRC, "linear_fits", "drift_prediction.py")
        subprocess.run([sys.executable, script, str(h)], check=True, env=env)


def prep():
    banner("build the windows: data/raw -> data/preprocessed")
    from cmn import data_prep
    data_prep.main()


def baselines():
    banner("baselines and linear regression")
    from models import linear_reg
    linear_reg.main()


def lstm():
    banner("LSTM")
    from models import nn_models
    nn_models.train("lstm")


def transformer():
    banner("transformer")
    from models import nn_models
    nn_models.train("transformer")


def compare():
    banner("comparison of all models")
    from evaluate import compare as comparison
    comparison.main()


STEPS = {"fits": fits, "prep": prep, "baselines": baselines,
         "lstm": lstm, "transformer": transformer, "compare": compare}


def main():
    names = sys.argv[1:] or list(STEPS)
    unknown = [n for n in names if n not in STEPS]
    if unknown:
        sys.exit(f"unknown step: {', '.join(unknown)}\n{__doc__}")
    for name in names:
        STEPS[name]()


if __name__ == "__main__":
    main()
