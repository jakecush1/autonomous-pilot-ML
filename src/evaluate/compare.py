# step 4: one table + chart comparing every model in evaluation/results/results.json
import json
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # src/, so this file also runs on its own
from models.linear_reg import RESULTS
from cmn import data_prep as dp

ORDER = ["no_drift", "persistence", "linear_reg", "lstm", "transformer"]


def main():
    res = json.load(open(RESULTS))
    rows = [{"model": m, "split": s, **res[m][s]} for m in ORDER if m in res for s in ["val", "test"]]
    table = pd.DataFrame(rows).pivot(index="model", columns="split",
                                     values=["median_m", "p90_m", "r2"]).reindex([m for m in ORDER if m in res])
    print(f"position error after {dp.H} min (metres), lower is better\n")
    print(table.round(2).to_string())

    test = table.xs("test", axis=1, level=1)
    ax = test[["median_m", "p90_m"]].plot.bar(figsize=(8, 4.5), rot=0)
    ax.set_ylabel(f"error after {dp.H} min (m)")
    ax.set_title(f"Drift prediction, test deployment (Oct 16-23), H = {dp.H} min")
    ax.legend(["median", "90th percentile"])
    plt.tight_layout()
    plt.savefig(os.path.join(dp.RESULTS_DIR, "comparison.png"), dpi=150)


if __name__ == "__main__":
    main()
