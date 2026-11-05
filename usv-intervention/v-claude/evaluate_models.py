#!/usr/bin/env python3
# Compares ways of predicting the next hour's drift, so we can see what each input adds and
# whether the model beats the simple guesses. Scores every model two ways:
#
#   * leave-one-export-out: train on all date ranges but one, test on the one left out, repeat
#     for each range. Every sample gets tested by a model that never saw its date range.
#   * time split: train on everything before Sep 1, test on October.
#
# The score is the distance (nm) between where the model said the USV would be after an hour
# and where it really was. Mean, median and the 80th percentile are shown.
#
# Run from this folder:   python evaluate_models.py
import numpy as np
import pandas as pd
from drift_model import (TARGET, WIND, POSITION, LAST_HOUR, TWO_HOURS_AGO, TIERS,
                         load_samples, fit, predict_with)

SPLIT_DATE = "2026-09-01"

# the inputs to compare, from simplest to richest
CANDIDATES = {
    "wind only": WIND,
    "wind + position": WIND + POSITION,
    "last hour only": LAST_HOUR,
    "wind + last hour": WIND + LAST_HOUR,
    "wind + position + last hour": TIERS["one_past_hour"],
    "wind + last two hours": WIND + LAST_HOUR + TWO_HOURS_AGO,
    "wind + position + last two hours": TIERS["two_past_hours"],
}


def miss_nm(rows, predicted_east, predicted_north):
    return np.hypot(rows["moved_east_nm"] - predicted_east, rows["moved_north_nm"] - predicted_north)


def predict_rows(model, rows):
    x = rows[model["inputs"]].to_numpy(dtype=float)
    out = x @ np.array(model["coef"]).T + np.array(model["intercept"])
    return out[:, 0], out[:, 1]


def leave_one_export_out(rows, inputs):
    miss = pd.Series(np.nan, index=rows.index)
    for export in rows["export"].unique():
        train = rows[rows["export"] != export]
        test = rows[rows["export"] == export]
        east, north = predict_rows(fit(train, inputs), test)
        miss[test.index] = miss_nm(test, east, north)
    return miss


def time_split(rows, inputs):
    train = rows[rows["start_time"] < SPLIT_DATE]
    test = rows[rows["start_time"] >= SPLIT_DATE]
    east, north = predict_rows(fit(train, inputs), test)
    return miss_nm(test, east, north)


def line(name, miss, extra=""):
    return (f"  {name:34s} mean {miss.mean():.3f}   median {miss.median():.3f}   "
            f"80% within {miss.quantile(0.8):.3f}{extra}")


def compare(rows, title):
    print(f"\n{title}: {len(rows)} samples from {rows['export'].nunique()} exports")
    print("  one-hour miss in nm, leave-one-export-out | time split (train before Sep, test Oct)")
    print(line("no drift", miss_nm(rows, 0, 0)))
    if rows[LAST_HOUR].notna().all().all():
        print(line("same as last hour", miss_nm(rows, rows[LAST_HOUR[0]], rows[LAST_HOUR[1]])))
    for name, inputs in CANDIDATES.items():
        if not rows[inputs].notna().all().all():
            continue                                              # this subset lacks an input
        cv = leave_one_export_out(rows, inputs)
        ts = time_split(rows, inputs)
        print(line(name, cv, f"   | Oct mean {ts.mean():.3f} (n={len(ts)})"))


samples = load_samples()
compare(samples, "ALL SAMPLES (no past drift needed)")
compare(samples.dropna(subset=LAST_HOUR), "SAMPLES WITH LAST HOUR'S DRIFT")
compare(samples.dropna(subset=LAST_HOUR + TWO_HOURS_AGO), "SAMPLES WITH THE LAST TWO HOURS' DRIFT")

# ---- two hours ahead: predict hour 1, then feed that prediction in as "last hour" for hour 2 ----
# (wind is held at its current value, as it would be in live use)
print("\nTWO HOURS AHEAD (one-past-hour tier rolled forward, leave-one-export-out)")
with_last = samples.dropna(subset=LAST_HOUR)
next_sample = {row.start_time: row for row in samples.itertuples()}
inputs = TIERS["one_past_hour"]
misses, persist, none = [], [], []
for export in with_last["export"].unique():
    model = fit(with_last[with_last["export"] != export], inputs)
    for row in with_last[with_last["export"] == export].itertuples():
        second = next_sample.get(row.end_time)
        if second is None or second.drift_stretch != row.drift_stretch:
            continue
        values = {name: getattr(row, name) for name in inputs}
        e1, n1 = predict_with(model, values)
        values.update({"start_x_nm": row.start_x_nm + e1, "start_y_nm": row.start_y_nm + n1,
                       "last_moved_east_nm": e1, "last_moved_north_nm": n1})
        e2, n2 = predict_with(model, values)
        true_east = row.moved_east_nm + second.moved_east_nm
        true_north = row.moved_north_nm + second.moved_north_nm
        misses.append(np.hypot(true_east - (e1 + e2), true_north - (n1 + n2)))
        persist.append(np.hypot(true_east - 2 * row.last_moved_east_nm, true_north - 2 * row.last_moved_north_nm))
        none.append(np.hypot(true_east, true_north))
for name, miss in [("no drift", none), ("same as last hour, twice", persist), ("model", misses)]:
    print(line(name, pd.Series(miss)))
print(f"  ({len(misses)} two-hour stretches)")
