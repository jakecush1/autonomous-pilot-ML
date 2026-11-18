# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt
# import glob

# files = glob.glob("../../data/*.csv")   # every .csv in a folder called data/
# # print(files)                      # check it found what you expected

# df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
# df = df.sort_values("Time").drop_duplicates(subset="Time").reset_index(drop=True)

# # Convert lat/lon to metres so distances make sense
# # earth is 6371km or 6371000m radius
# R = 6371000
# lat0 = df["lat"].mean()
# df["x_m"] = np.radians(df["lon"]) * R * np.cos(np.radians(lat0))  # east
# df["y_m"] = np.radians(df["lat"]) * R                              # north

# # Speed over the last minute, in m/min (rows are 1 minute apart)
# df["speed"] = np.hypot(df["x_m"].diff(), df["y_m"].diff())
# df.loc[df["Time"].diff() != 60_000, "speed"] = np.nan

# # Keep only rows where the motor is OFF (otherwise it's not drift)
# drift = df[df["motor_power"] < 1].dropna()

# drift_clean = drift.dropna()
# # print(drift_clean)
# # TODO 1: make X (wind speed, 2-D!) and y (speed)
# # print(drift_clean[["wind_speed_kn"]])
# X = drift_clean[["wind_speed_kn"]]
# # # df["x_m"].diff() => this row, minus the previous row
# y = drift_clean["speed"]
# # print(y)

# # # # # TODO 2: create and fit the model
# model = LinearRegression()
# model.fit(X,y)

# # # # TODO 3: print the slope and intercept
# print("w =", model.coef_,)
# print("b =", model.intercept_)

# # # TODO 4: predict drift speed at 5 kn and 15 kn
# print(model.predict(pd.DataFrame({"wind_speed_kn": [5, 15]})))

# i = df["speed"].idxmax()
# print(df.loc[i-3:i+3, ["Time", "lat", "lon", "motor_power", "speed"]])
# print(pd.to_datetime(df.loc[i, "Time"], unit="ms"))

# print((df["speed"] > 93).sum())


# # 1. Scatter: each dot = one motor-off minute
# plt.scatter(X["wind_speed_kn"], y, s=2, alpha=0.3, label="data")

# # 2. The learned line: predict speed across a range of wind speeds
# wind_range = pd.DataFrame({"wind_speed_kn": np.linspace(0, 20, 100)})
# plt.plot(wind_range["wind_speed_kn"], model.predict(wind_range),
#          color="red", label="fitted line")

# # 3. Labels, then show
# plt.xlabel("Wind speed (kn)")
# plt.ylabel("Drift speed (m/min)")
# plt.title("Does wind drive drift?")
# plt.legend()
# plt.show()


# ================================================================ current version
# What does wind contribute to the drift? Two views on the same motor-off minutes:
#   SPEED:      drift speed ~ wind speed                          (how fast, ignoring direction)
#   DIRECTION:  angle between drift and downwind,
#               downwind part of the drift ~ wind speed,
#               vector fit: drift (east, north) = W · wind push (east, north) + c      c = average current
# The speed fit is only printed, as a comparison; the PNG shows the two direction plots:
# evaluation/results/linear_fits/{N}min-drift_vs_wind.png
#
# usage:  python src/linear_fits/drift_vs_wind.py 30      (N = window in minutes, default 60)
import os
import sys
import glob
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# folders are found from this file's location, so the script runs from anywhere
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")   # top folder of the repository
PLOTS = os.path.join(ROOT, "evaluation", "results", "linear_fits")            # where the plot is saved

M_PER_MIN_PER_KN = 1852 / 60    # 1 kn = 1852 m/h = 30.87 m/min

# ---------------------------------------------------------------- load
files = glob.glob(os.path.join(ROOT, "data", "raw", "*.csv"))   # every .csv in the data/raw folder
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Files may load in any order and may overlap -> sort by time, drop repeats
df = df.sort_values("Time").drop_duplicates(subset="Time").reset_index(drop=True)

# ---------------------------------------------------------------- lat/lon -> metres
# Earth radius is 6371 km = 6,371,000 m
R = 6371000
lat0 = df["lat"].mean()
df["x_m"] = np.radians(df["lon"]) * R * np.cos(np.radians(lat0))  # east
df["y_m"] = np.radians(df["lat"]) * R                              # north

# ---------------------------------------------------------------- drift velocity over the last N minutes
# a longer window averages out GPS noise; 60 min is the window used in the report
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
print("time: ", N, "mins")
df["drift_e"] = df["x_m"].diff(N) / N                    # m/min east
df["drift_n"] = df["y_m"].diff(N) / N                    # m/min north
df["speed"] = np.hypot(df["drift_e"], df["drift_n"])     # m/min, direction ignored

# ---------------------------------------------------------------- wind push vector
# wind_from_sin / wind_from_cos describe where the wind comes FROM (sin = east, cos = north).
# It pushes the boat the opposite way, so flip the sign. Units: kn
df["push_e"] = -df["wind_from_sin"] * df["wind_speed_kn"]
df["push_n"] = -df["wind_from_cos"] * df["wind_speed_kn"]

# ---------------------------------------------------------------- filter
# Keep a row only if the WHOLE N-minute span is clean (checking only the last minute
# lets gaps and motor-on minutes slip into the middle of the span):
#   - exactly N minutes since the row N rows back (no gaps / file joins inside the span)
#   - motor off for every minute of the span
#   - slower than 3 kn (~93 m/min); faster can't be drift, it's a tow/transit
#   - wind at least 1 kn, otherwise there is no wind direction to compare with
ok = df["Time"].diff(N) == N * 60_000
ok &= df["motor_power"].rolling(N + 1).max() < 1
ok &= df["speed"] < 93
ok &= df["wind_speed_kn"] >= 1
drift = df[ok].dropna(subset=["drift_e", "drift_n", "push_e", "push_n"]).copy()
print("rows used:", len(drift))

# ================================================================ 1. SPEED: drift speed ~ wind speed
X = drift[["wind_speed_kn"]]    # input: 2-D table, one column
y_speed = drift["speed"]        # answer: 1-D, one value per row

speed_model = LinearRegression()
speed_model.fit(X, y_speed)
w_s, b_s, r2_s = speed_model.coef_[0], speed_model.intercept_, speed_model.score(X, y_speed)
print("\n--- speed")
print(f"drift speed = {w_s:.3f} · wind + {b_s:.2f} m/min   R² = {r2_s:.3f}"
      f"   (slope = {w_s / M_PER_MIN_PER_KN * 100:.1f}% of wind speed)")
print("predicted at 5 & 15 kn:", speed_model.predict(pd.DataFrame({"wind_speed_kn": [5, 15]})).round(2))

# ================================================================ 2. DIRECTION
print("\n--- direction")
# angle of each vector, counter-clockwise from east; difference wrapped to -180..180
# negative = drift is to the RIGHT of downwind (clockwise), positive = to the LEFT
drift_angle = np.degrees(np.arctan2(drift["drift_n"], drift["drift_e"]))
down_angle = np.degrees(np.arctan2(drift["push_n"], drift["push_e"]))
drift["angle"] = (drift_angle - down_angle + 180) % 360 - 180

# circular mean (an ordinary mean breaks at -180/180: the mean of 179 and -179 should be 180, not 0)
mean_angle = np.degrees(np.angle(np.exp(1j * np.radians(drift["angle"])).mean()))
print(f"mean angle from downwind: {mean_angle:+.0f}°  (negative = right of the wind)")

# share of time drifting WITH the wind = drift direction within ±45° of downwind
# (if wind had no effect on direction, this would be 90/360 = 25%)
drift["with_wind"] = abs(drift["angle"]) < 45
drift["wind_band"] = pd.cut(drift["wind_speed_kn"], [1, 5, 10, 15, np.inf], right=False,
                            labels=["1-5 kn", "5-10 kn", "10-15 kn", ">= 15 kn"])
bands = drift.groupby("wind_band", observed=True)["with_wind"].agg(minutes="size", with_wind="mean")
bands["share_of_time"] = bands["minutes"] / len(drift)
bands.loc["all"] = [len(drift), drift["with_wind"].mean(), 1.0]
print("\nshare of time drifting with the wind (within ±45° of downwind; 25% = no wind effect)")
print(bands.to_string(formatters={"minutes": "{:.0f}".format, "with_wind": "{:.0%}".format,
                                  "share_of_time": "{:.0%}".format}))
print()

# downwind part of the drift: dot product with a unit vector pointing downwind
unit_e = drift["push_e"] / drift["wind_speed_kn"]
unit_n = drift["push_n"] / drift["wind_speed_kn"]
drift["downwind"] = drift["drift_e"] * unit_e + drift["drift_n"] * unit_n
drift["crosswind"] = -drift["drift_e"] * unit_n + drift["drift_n"] * unit_e     # + = left of downwind

y_down = drift["downwind"]
down_model = LinearRegression()
down_model.fit(X, y_down)
w_d, b_d, r2_d = down_model.coef_[0], down_model.intercept_, down_model.score(X, y_down)
print(f"downwind drift = {w_d:.3f} · wind + {b_d:.2f} m/min   R² = {r2_d:.3f}"
      f"   (slope = {w_d / M_PER_MIN_PER_KN * 100:.1f}% of wind speed)")
print(f"mean downwind drift {y_down.mean():+.2f} m/min, mean crosswind drift {drift['crosswind'].mean():+.2f} m/min")

# vector fit: W turns and scales the wind push; c is the drift wind doesn't explain on average (current)
Xv = drift[["push_e", "push_n"]]
yv = drift[["drift_e", "drift_n"]]
vec_model = LinearRegression()
vec_model.fit(Xv, yv)
W, c, r2_v = vec_model.coef_, vec_model.intercept_, vec_model.score(Xv, yv)
turn = np.degrees(np.arctan2(W[1, 0] - W[0, 1], W[0, 0] + W[1, 1]))   # rotation part of W
print("W =", W.round(3).tolist(), "  c (m/min) =", c.round(2).tolist())
print(f"vector fit R² (both axes) = {r2_v:.3f}   W turns the wind push by {turn:+.0f}° (negative = clockwise)")

# ================================================================ plot: one PNG, two panels
fig, (ax_d, ax_h) = plt.subplots(1, 2, figsize=(12, 5))
wind_range = pd.DataFrame({"wind_speed_kn": np.linspace(0, 20, 100)})


def knots_axis(ax, label):
    """right-hand axis in knots"""
    ax2 = ax.secondary_yaxis("right", functions=(lambda m: m / M_PER_MIN_PER_KN,     # m/min -> kn
                                                 lambda kn: kn * M_PER_MIN_PER_KN))  # kn -> m/min
    ax2.set_ylabel(label)


def fit_box(ax, w, b, r2):
    ax.text(0.02, 0.98, f"w = {w:.3f}\nb = {b:.2f}\nR² = {r2:.3f}\nN = {N} min",
            transform=ax.transAxes, va="top", bbox=dict(facecolor="white", alpha=0.8))


# (a) only the part of the drift that goes WITH the wind
ax_d.scatter(X["wind_speed_kn"], y_down, s=2, alpha=0.3, label="data")
ax_d.plot(wind_range["wind_speed_kn"], down_model.predict(wind_range), color="red", label="fitted line")
ax_d.axhline(0, color="grey", lw=0.8)
ax_d.set_xlabel("Wind speed (kn)")
ax_d.set_ylabel("Downwind drift (m/min)   (< 0 = against the wind)")
ax_d.set_title("(a) Drift along the wind vs wind speed")
ax_d.legend(loc="lower right")
knots_axis(ax_d, "Downwind drift (kn)")
fit_box(ax_d, w_d, b_d, r2_d)

# (b) how far the drift direction is from downwind, light vs strong wind
bins = np.arange(-180, 181, 10)
strong = drift["wind_speed_kn"] >= 10
ax_h.hist(drift.loc[~strong, "angle"], bins=bins, density=True, alpha=0.5, label="wind < 10 kn")
ax_h.hist(drift.loc[strong, "angle"], bins=bins, density=True, alpha=0.5, label="wind ≥ 10 kn")
ax_h.axhline(1 / 360, color="grey", ls="--", lw=1, label="no wind effect")
ax_h.axvline(0, color="black", lw=0.8)
ax_h.axvline(mean_angle, color="red", lw=1.2, label=f"mean {mean_angle:+.0f}°")
ax_h.set_xticks(range(-180, 181, 45))
ax_h.set_xlabel("Drift direction minus downwind (°)   (< 0 = right of the wind)")
ax_h.set_ylabel("Share of minutes (density)")
ax_h.set_title("(b) Drift direction relative to the wind")
ax_h.legend(loc="upper left", fontsize=8)
ax_h.text(0.98, 0.98,
          f"vector fit R² = {r2_v:.3f}\nW turns wind {turn:+.0f}°\n"
          f"within ±45°: {np.mean(abs(drift['angle']) < 45):.0%}",
          transform=ax_h.transAxes, va="top", ha="right", bbox=dict(facecolor="white", alpha=0.8))

plt.tight_layout()
os.makedirs(PLOTS, exist_ok=True)
plt.savefig(os.path.join(PLOTS, f"{N}min-drift_vs_wind.png"), dpi=150)
plt.show()
