import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import glob

H = 30   # horizon: predict 60 minutes ahead (and look 60 minutes back)

# ---------------------------------------------------------------- load
files = glob.glob("../../../data/*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df = df.sort_values("Time").drop_duplicates(subset="Time").reset_index(drop=True)
# print(files)
# print(len(df))

R = 6371000
lat0 = df["lat"].mean()
df["x_m"] = np.radians(df["lon"]) * R * np.cos(np.radians(lat0))  # east
df["y_m"] = np.radians(df["lat"]) * R                              # north

# ---------------------------------------------------------------- past drift (feature)
# calculate difference from location 60mins ago, to now
# diff = location 60 mins ago - location now
df["past_dx"] = df["x_m"].diff(H)
df["past_dy"] = df["y_m"].diff(H)

# ---------------------------------------------------------------- future drift (target)
# TODO 1: metres moved east and north over the NEXT H minutes
df["future_dx"] = df["x_m"].shift(-H) - df["x_m"]
df["future_dy"] = df["y_m"].shift(-H) - df["y_m"]

# ---------------------------------------------------------------- wind vector (feature)
# TODO 2: east and north wind components
df["wind_e"] = df["wind_from_cos"] * df["wind_speed_kn"]
df["wind_n"] = df["wind_from_sin"] * df["wind_speed_kn"]

# ---------------------------------------------------------------- clean
# Past and future windows must both be exactly H minutes (no gaps / file joins)
past_ok   = df["Time"].diff(H) == H * 60_000
future_ok = (df["Time"].shift(-H) - df["Time"]) == H * 60_000

# Motor must be OFF for the whole past hour AND the whole next hour.
# (Otherwise past or future movement includes driving, not just drift.)
motor_on = (df["motor_power"] >= 1).astype(int)
motor_off_past   = motor_on.rolling(H).sum() == 0
motor_off_future = motor_on.shift(-H).rolling(H).sum() == 0

# Tow filter: > 93 m/min ≈ > 5,580 m in an hour
fast_past   = np.hypot(df["past_dx"],   df["past_dy"])   > 93 * H
fast_future = np.hypot(df["future_dx"], df["future_dy"]) > 93 * H

keep = past_ok & future_ok & motor_off_past & motor_off_future & ~fast_past & ~fast_future

FEATURES = ["past_dx", "past_dy", "wind_e", "wind_n"]
TARGETS  = ["future_dx", "future_dy"]
data = df.loc[keep, FEATURES + TARGETS].dropna()
print("rows:", len(data))

# ---------------------------------------------------------------- fit
# TODO 3: make X and y from `data`, create the model, fit it
X = data[FEATURES]
# print(X)
y = data[TARGETS]
# print(y)
model = LinearRegression()
model.fit(X,y)


# # TODO 4: print the weights as a readable table
print(pd.DataFrame(model.coef_.T, index=FEATURES, columns=["east", "north"]).round(3))
print("intercept (east, north):", model.intercept_.round(1))
print("R² (training):", model.score(X, y))


import matplotlib.pyplot as plt

pred = model.predict(X)                      # shape (rows, 2): east, north
r2 = model.score(X, y)

# Error in metres: distance between predicted and actual 1-hour endpoint
err_m = np.hypot(pred[:, 0] - y["future_dx"], pred[:, 1] - y["future_dy"])

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# ---- Panels 1 & 2: predicted vs actual, east and north
for ax, i, name in [(axes[0], 0, "east"), (axes[1], 1, "north")]:
    actual = y.iloc[:, i]
    ax.scatter(actual, pred[:, i], s=2, alpha=0.3)
    lim = [actual.min(), actual.max()]
    ax.plot(lim, lim, color="red", label="perfect (y = x)")
    ax.set_xlabel(f"Actual {name} drift next {H} min (m)")
    ax.set_ylabel(f"Predicted {name} drift (m)")
    ax.set_title(f"{name.capitalize()}")
    ax.set_aspect("equal")
    ax.legend()

# ---- Panel 3: how far off is the predicted position?
axes[2].hist(err_m, bins=60)
axes[2].axvline(np.median(err_m), color="red",
                label=f"median {np.median(err_m):.0f} m")
axes[2].axvline(np.percentile(err_m, 90), color="orange",
                label=f"90th pct {np.percentile(err_m, 90):.0f} m")
axes[2].set_xlabel("Position error after 1 h (m)")
axes[2].set_ylabel("Count")
axes[2].set_title("Prediction error")
axes[2].legend()

fig.suptitle(f"Drift model v2  |  H = {H} min  |  R² = {r2:.3f}  |  rows = {len(X)}")
fig.tight_layout()
plt.savefig(f"{H}min_drift_r2:{r2:.2f}.png", dpi=150)
plt.show()