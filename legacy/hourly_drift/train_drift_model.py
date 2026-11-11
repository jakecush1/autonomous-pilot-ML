#!/usr/bin/env python3
# Trains a linear regression to predict how far the USV drifts in the next hour,
# and compares it with two simple guesses.
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ---- 1. load the drift samples ----
data = pd.read_csv("usv_drift_samples.csv")
data = data.dropna()        # keep only hours that have a "last hour" drift, so every model is tested on the same hours

# ---- 2. split by time: learn from August, test on October ----
train = data[data["start_time"] < "2026-09-01"]
test = data[data["start_time"] >= "2026-09-01"]

# what we want to predict: how far it moves east and north in the hour
TARGET = ["moved_east_nm", "moved_north_nm"]


# ---- 3. the score: average distance (nm) between where we said it would be and where it really was ----
def average_error(predicted_east, predicted_north):
    miss_east = test["moved_east_nm"] - predicted_east
    miss_north = test["moved_north_nm"] - predicted_north
    return np.hypot(miss_east, miss_north).mean()


# ---- 4. two simple guesses the model has to beat ----
no_drift = average_error(0, 0)
same_as_last_hour = average_error(test["last_moved_east_nm"], test["last_moved_north_nm"])

# ---- 5. model A: wind only ----
WIND = ["wind_push_east_kn", "wind_push_north_kn"]
wind_model = LinearRegression()
wind_model.fit(train[WIND], train[TARGET])               # the training step
predicted = wind_model.predict(test[WIND])               # one row per test hour: column 0 = east, column 1 = north
wind_only = average_error(predicted[:, 0], predicted[:, 1])

# ---- 6. model B: wind + last hour's drift ----
BOTH = WIND + ["last_moved_east_nm", "last_moved_north_nm"]
both_model = LinearRegression()
both_model.fit(train[BOTH], train[TARGET])
predicted = both_model.predict(test[BOTH])
wind_and_last_hour = average_error(predicted[:, 0], predicted[:, 1])

# ---- 7. results ----
print(f"trained on {len(train)} August hours, tested on {len(test)} October hours")
print("average error after one hour (nm):")
print(f"  no drift:           {no_drift:.3f}")
print(f"  same as last hour:  {same_as_last_hour:.3f}")
print(f"  wind only:          {wind_only:.3f}")
print(f"  wind + last hour:   {wind_and_last_hour:.3f}")

print()
print("what the wind-only model learned")
print("  rows: moved east, moved north | columns: wind push east, wind push north")
print(wind_model.coef_.round(4))
print("  constant part (nm per hour east, north):", wind_model.intercept_.round(3))
