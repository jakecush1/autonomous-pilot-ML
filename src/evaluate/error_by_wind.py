# RQ3: does each model's error depend on wind strength?
# Scores every model on the final test set (November), split by the mean wind over each sample's input hour.
# Reads the trained LSTM / Transformer from output/ and refits the linear regressions (deterministic);
# nothing is trained or tuned on the test set.
#
# usage:  python src/main.py windbands     (or: python src/evaluate/error_by_wind.py)
import json
import os
import sys
import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LinearRegression

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # src/
from cmn import data_prep as dp
from models.nn_models import MODELS

BANDS = [(0, 10, "< 10 kn"), (10, 15, "10-15 kn"), (15, np.inf, ">= 15 kn")]
OUT = os.path.join(dp.RESULTS_DIR, "error_by_wind.json")


def nn_predict(name, data, X):
    """predictions of a saved LSTM / Transformer, scaled with the same train stats as in training"""
    Xtr, ytr, _ = data["train"]
    x_mu, x_sd = Xtr.reshape(-1, Xtr.shape[2]).mean(0), Xtr.reshape(-1, Xtr.shape[2]).std(0)
    y_mu, y_sd = ytr.mean(0), ytr.std(0)
    model = MODELS[name](Xtr.shape[2])
    model.load_state_dict(torch.load(os.path.join(dp.OUTPUT_DIR, f"{name}.pt")))
    model.eval()
    with torch.no_grad():
        return model(torch.tensor((X - x_mu) / x_sd, dtype=torch.float32)).numpy() * y_sd + y_mu


def main():
    data = dp.load()
    Xtr, ytr, _ = data["train"]
    X, y, _ = data["test"]
    F_tr, F = dp.summary_features(Xtr), dp.summary_features(X)

    preds = {
        "persistence": F[:, :2],
        "linear_reg": LinearRegression().fit(F_tr, ytr).predict(F),
        "linear_reg_no_wind": LinearRegression().fit(F_tr[:, :2], ytr).predict(F[:, :2]),
        "lstm": nn_predict("lstm", data, X),
        "transformer": nn_predict("transformer", data, X),
    }
    wind = np.hypot(X[:, :, 2], X[:, :, 3]).mean(axis=1)      # mean wind speed over the input hour, kn
    err = {m: np.hypot(*(p - y).T) for m, p in preds.items()}  # endpoint error, m

    rows, out = [], {}
    for lo, hi, label in BANDS:
        sel = (wind >= lo) & (wind < hi)
        out[label] = {"n": int(sel.sum()), "share": float(sel.mean())}
        for m, e in err.items():
            out[label][m] = {"median_m": float(np.median(e[sel])), "p90_m": float(np.percentile(e[sel], 90))}
            rows.append({"wind": label, "model": m, "n": int(sel.sum()),
                         "median_m": np.median(e[sel]), "p90_m": np.percentile(e[sel], 90)})
    os.makedirs(dp.RESULTS_DIR, exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)

    table = pd.DataFrame(rows).pivot(index="model", columns="wind", values=["median_m", "p90_m"])
    table = table.reindex(list(preds))[[(v, b[2]) for v in ["median_m", "p90_m"] for b in BANDS]]
    print("final test set: endpoint error after 60 min (m) by mean wind over the input hour")
    print("samples per band:", {b: out[b]["n"] for b in out})
    Xv = data["val"][0]                                         # how windy was the validation week (early stopping)?
    wind_val = np.hypot(Xv[:, :, 2], Xv[:, :, 3]).mean(axis=1)
    print("validation week, share of samples per band:",
          {label: f"{((wind_val >= lo) & (wind_val < hi)).mean():.0%}" for lo, hi, label in BANDS})
    print(table.round(0).to_string())


if __name__ == "__main__":
    main()
