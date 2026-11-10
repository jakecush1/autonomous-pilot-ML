# builds the drift dataset shared by all three models (linear reg, LSTM, transformer)
#
# one sample = one moment t while the USV is drifting (motor off)
#   input  (X_seq): the last H minutes, one row per minute:
#                   [dx, dy, wind_push_e, wind_push_n]
#                   dx, dy = metres moved east/north during that minute
#   target (y):     metres moved east/north over the NEXT H minutes
# predicted position in H minutes = position now + y
#
# split is by deployment (time), never random: neighbouring windows share
# 59 of their 60 minutes, so a random split would leak test answers into training
import os
import numpy as np
import pandas as pd

H = 60                  # minutes of history in, minutes ahead to predict
MAX_GAP = 5             # fill missing-data gaps up to this many minutes
TOW_M_PER_MIN = 93      # > 93 m/min (~3 kn) is being towed / under way, not drifting

CENTER_LAT = 37.353612  # same center as v3-template.py
CENTER_LON = -122.879874
EARTH_R = 6371000

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "..", "data")
CACHE = os.path.join(HERE, "outputs", f"windows_H{H}.npz")

# whole deployments per split; test is the latest deployment, only scored at the end
SPLITS = {
    "train": ["1min_2026-04-17_to_2026-04-29.csv",
              "1min_2026-05-19_to_2026-06-06.csv",
              "1min_2026-08-05_to_2026-08-14.csv"],
    "val":   ["1min_2026-10-03_to_2026-10-13.csv"],
    "test":  ["1min_2026-10-16_to_2026-10-23.csv"],
}
SEQ_FEATURES = ["dx", "dy", "wind_push_e", "wind_push_n"]


def load_file(path):
    d = pd.read_csv(path).sort_values("Time").reset_index(drop=True)

    # short gaps (missing rows) are filled so they don't break a 2-hour window
    num = ["wind_speed_kn", "wind_from_sin", "wind_from_cos", "lat", "lon"]
    d[num] = d[num].interpolate(limit=MAX_GAP, limit_area="inside")
    d["motor_power"] = d["motor_power"].ffill(limit=MAX_GAP)

    # position in metres east (x) / north (y) of the center (flat-earth is fine within 10 nm)
    d["x_m"] = np.radians(d["lon"] - CENTER_LON) * EARTH_R * np.cos(np.radians(CENTER_LAT))
    d["y_m"] = np.radians(d["lat"] - CENTER_LAT) * EARTH_R
    d["dx"] = d["x_m"].diff()
    d["dy"] = d["y_m"].diff()

    # wind: sin/cos are of the compass direction the wind comes FROM (sin = east, cos = north).
    # it pushes the boat the opposite way, so flip the sign
    d["wind_push_e"] = -d["wind_from_sin"] * d["wind_speed_kn"]
    d["wind_push_n"] = -d["wind_from_cos"] * d["wind_speed_kn"]

    # a minute is usable if the motor is off, we have data, and it isn't moving like a tow
    speed = np.hypot(d["dx"], d["dy"])
    d["good"] = ((d["motor_power"] == 0) & d[SEQ_FEATURES].notna().all(axis=1)
                 & (speed < TOW_M_PER_MIN))
    return d


def make_windows(d):
    good = d["good"].to_numpy()
    feats = d[SEQ_FEATURES].to_numpy(np.float32)
    x, y = d["x_m"].to_numpy(), d["y_m"].to_numpy()
    times = d["Time"].to_numpy()

    X_seq, Y, T = [], [], []
    # t is "now": minutes t-H+1..t are the history, t+1..t+H the future
    run = np.convolve(good, np.ones(2 * H, dtype=int), mode="valid")   # good minutes per 2H window
    for start in np.flatnonzero(run == 2 * H):
        t = start + H - 1
        X_seq.append(feats[t - H + 1: t + 1])
        Y.append([x[t + H] - x[t], y[t + H] - y[t]])
        T.append(times[t])
    return (np.array(X_seq, np.float32).reshape(-1, H, len(SEQ_FEATURES)),
            np.array(Y, np.float32).reshape(-1, 2), np.array(T))


def build():
    out = {}
    for split, files in SPLITS.items():
        parts = [make_windows(load_file(os.path.join(DATA_DIR, f))) for f in files]
        out[f"{split}_X"] = np.concatenate([p[0] for p in parts])
        out[f"{split}_y"] = np.concatenate([p[1] for p in parts])
        out[f"{split}_t"] = np.concatenate([p[2] for p in parts])
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    np.savez_compressed(CACHE, **out)
    return out


def load():
    """returns {split: (X_seq, y, time_ms)} for train / val / test"""
    data = dict(np.load(CACHE)) if os.path.exists(CACHE) else build()
    return {s: (data[f"{s}_X"], data[f"{s}_y"], data[f"{s}_t"]) for s in SPLITS}


def summary_features(X_seq):
    """flat features for linear regression: past-H drift + current wind + mean wind over the past H"""
    past = X_seq[:, :, :2].sum(axis=1)          # metres moved east/north over the past H min
    wind_now = X_seq[:, -1, 2:]
    wind_mean = X_seq[:, :, 2:].mean(axis=1)
    return np.hstack([past, wind_now, wind_mean])

SUMMARY_NAMES = ["past_dx", "past_dy", "wind_e_now", "wind_n_now", "wind_e_mean", "wind_n_mean"]


def score(y_true, y_pred):
    """position error after H minutes, in metres; plus R² over both axes"""
    err = np.hypot(*(y_pred - y_true).T)
    ss_res = ((y_true - y_pred) ** 2).sum()
    ss_tot = ((y_true - y_true.mean(axis=0)) ** 2).sum()
    return {"median_m": float(np.median(err)), "p90_m": float(np.percentile(err, 90)),
            "mean_m": float(err.mean()), "r2": float(1 - ss_res / ss_tot), "n": len(err)}


if __name__ == "__main__":
    build()                                      # rebuild the cache from the CSVs
    for split, (X, y, t) in load().items():
        print(f"{split:5s} windows={len(X):6d}  mean |future drift| = {np.hypot(*y.T).mean():.0f} m")
