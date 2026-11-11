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


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import glob

def to_knots(m):
    return m / M_PER_MIN_PER_KN

# folders are found from this file's location, so the script runs from anywhere
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")   # top folder of the repository
PLOTS = os.path.join(ROOT, "evaluation", "results", "linear_fits")            # where the plots are saved

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

# ---------------------------------------------------------------- speed
# Distance moved since the previous row = speed in m/min (rows are 1 min apart)

# can tune minutes 1-60, larger time frame could reduce gps noise
# default is 10; to try another window, pass it when running:  python src/linear_fits/drift_vs_wind.py 30
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
print("time: ", N, "mins")
df["speed"] = np.hypot(df["x_m"].diff(N), df["y_m"].diff(N)) / N   # still m/min
# df["speed"] = np.hypot(df["x_m"].diff(), df["y_m"].diff())

# If two rows aren't exactly 1 minute apart (file boundary, telemetry gap),
# that "speed" is wrong -> blank it out
df.loc[df["Time"].diff() != 60_000, "speed"] = np.nan

# Faster than 3 kn (~93 m/min) can't be drift -> it's a tow/transit. Blank it.
df.loc[df["speed"] > 93, "speed"] = np.nan

# ---------------------------------------------------------------- filter
# Keep only motor-OFF rows with no missing values
drift = df[df["motor_power"] < 1].dropna()

# ---------------------------------------------------------------- X and y
X = drift[["wind_speed_kn"]]   # input: 2-D table, one column
y = drift["speed"]             # answer: 1-D, one value per row

# ---------------------------------------------------------------- fit
model = LinearRegression()
model.fit(X, y)

print("rows used:", len(X))
print("w =", model.coef_)
print("b =", model.intercept_)
print("R² =", model.score(X, y))

# Predict drift speed at 5 kn and 15 kn
print("predicted at 5 & 15 kn:", model.predict(pd.DataFrame({"wind_speed_kn": [5, 15]})))

# ---------------------------------------------------------------- plot
fig, ax = plt.subplots()

ax.scatter(X["wind_speed_kn"], y, s=2, alpha=0.3, label="data")

wind_range = pd.DataFrame({"wind_speed_kn": np.linspace(0, 20, 100)})
ax.plot(wind_range["wind_speed_kn"], model.predict(wind_range),
        color="red", label="fitted line")

ax.set_xlabel("Wind speed (kn)")
ax.set_ylabel("Drift speed (m/min)")
ax.set_title("Does wind drive drift?")
ax.legend()

# Right-hand axis in knots. 1 kn = 1852 m/h = 30.87 m/min
M_PER_MIN_PER_KN = 1852 / 60
ax2 = ax.secondary_yaxis(
    "right",
    functions=(lambda m: m / M_PER_MIN_PER_KN,   # m/min -> kn
               lambda kn: kn * M_PER_MIN_PER_KN) # kn -> m/min
)
ax2.set_ylabel("Drift speed (kn)")

w = model.coef_[0]
b = model.intercept_
r2 = model.score(X, y)
ax.text(0.02, 0.98,
        f"w = {w:.3f}\nb = {b:.2f}\nR² = {r2:.3f}\nN = {N} min",
        transform=ax.transAxes, va="top",
        bbox=dict(facecolor="white", alpha=0.8))

os.makedirs(PLOTS, exist_ok=True)
plt.savefig(os.path.join(PLOTS, f"{N}min-drift_plot.png"), dpi=150)
plt.show()
