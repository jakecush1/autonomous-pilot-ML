# step 1: baselines + linear regression
# drift(next H) = A · [past drift, wind now, mean wind] + c       (2 outputs: east, north)
# regression, not classification: the target is a distance in metres, not a category
import json
import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # src/, so this file also runs on its own
from cmn import data_prep as dp

RESULTS = os.path.join(dp.RESULTS_DIR, "results.json")


def save_results(name, scores):
    """adds one model's val/test scores to evaluation/results/results.json (shared by all scripts)"""
    os.makedirs(dp.RESULTS_DIR, exist_ok=True)
    allres = json.load(open(RESULTS)) if os.path.exists(RESULTS) else {}
    allres[name] = scores
    json.dump(allres, open(RESULTS, "w"), indent=2)


def main():
    data = dp.load()
    Xtr, ytr, _ = data["train"]
    F = {s: dp.summary_features(data[s][0]) for s in data}

    # baseline 1: it stays where it is
    zero = {s: dp.score(data[s][1], np.zeros_like(data[s][1])) for s in ["val", "test"]}
    # baseline 2: persistence - next hour's drift = last hour's drift
    persist = {s: dp.score(data[s][1], F[s][:, :2]) for s in ["val", "test"]}

    model = LinearRegression().fit(F["train"], ytr)
    linreg = {s: dp.score(data[s][1], model.predict(F[s])) for s in ["val", "test"]}

    print(pd.DataFrame(model.coef_.T, index=dp.SUMMARY_NAMES, columns=["east", "north"]).round(3))
    print("intercept (east, north) m:", model.intercept_.round(1))
    for name, res in [("no_drift", zero), ("persistence", persist), ("linear_reg", linreg)]:
        save_results(name, res)
        print(f"{name:12s} val median {res['val']['median_m']:5.0f} m  p90 {res['val']['p90_m']:5.0f} m"
              f"  | test median {res['test']['median_m']:5.0f} m  p90 {res['test']['p90_m']:5.0f} m")


if __name__ == "__main__":
    main()
