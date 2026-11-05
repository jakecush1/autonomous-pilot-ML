#!/usr/bin/env python3
# Shared pieces of the v3 drift model: the input columns, fitting, saving/loading, predicting,
# and the lat/lon <-> nm-from-center conversions. Used by train_drift_model.py,
# evaluate_models.py and predict_drift.py.
#
# The model is one linear regression per "tier" of inputs:
#
#     drift(t+1) = A · wind(t) + B · position(t) + C · drift(t) + D · drift(t-1) + c
#
# where drift is (nm east, nm north) moved in an hour, wind is its push split east/north (kn),
# position is nm east/north of the center. A, B, C, D and c are learned from the drift samples.
# The richest tier (two past hours of drift) is used when its inputs are known; otherwise the
# model falls back to the one-past-hour tier, then to wind + position alone (first hour after
# the motor stops, when no drift has been seen yet).
import json
import math
import os
import numpy as np
import pandas as pd
from pyproj import Transformer
from sklearn.linear_model import LinearRegression

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES_FILE = os.path.join(HERE, "data", "usv_drift_samples.csv")
MODEL_FILE = os.path.join(HERE, "drift_model.json")

# ---- zone settings (same as the rest of the project) ----
CENTER_LAT = 37.353612      # old buoy 46012 position = center of the op zone
CENTER_LON = -122.879874
METERS_PER_NM = 1852

# ---- columns ----
TARGET = ["moved_east_nm", "moved_north_nm"]                  # what we predict
WIND = ["wind_push_east_kn", "wind_push_north_kn"]
POSITION = ["start_x_nm", "start_y_nm"]
LAST_HOUR = ["last_moved_east_nm", "last_moved_north_nm"]
TWO_HOURS_AGO = ["last2_moved_east_nm", "last2_moved_north_nm"]

# the tiers, richest first: predict() uses the first one whose inputs are all known
TIERS = {
    "two_past_hours": WIND + POSITION + LAST_HOUR + TWO_HOURS_AGO,
    "one_past_hour": WIND + POSITION + LAST_HOUR,
    "no_past_drift": WIND + POSITION,
}


# ---- geography ----
def get_utm_zone(lat, lon):
    zone = int((lon + 180) // 6) + 1          # -122.88 -> zone 10
    code = (32600 if lat >= 0 else 32700) + zone
    return f"EPSG:{code}"


UTM = get_utm_zone(CENTER_LAT, CENTER_LON)
TO_UTM = Transformer.from_crs("EPSG:4326", UTM)
FROM_UTM = Transformer.from_crs(UTM, "EPSG:4326")
CENTER_X, CENTER_Y = TO_UTM.transform(CENTER_LAT, CENTER_LON)


# lat, lon -> nm east (x) and nm north (y) of the center
def to_xy(lat, lon):
    x, y = TO_UTM.transform(lat, lon)
    return (x - CENTER_X) / METERS_PER_NM, (y - CENTER_Y) / METERS_PER_NM


# nm east/north of the center -> lat, lon
def to_latlon(x_nm, y_nm):
    return FROM_UTM.transform(CENTER_X + x_nm * METERS_PER_NM, CENTER_Y + y_nm * METERS_PER_NM)


# wind speed (kn) and the direction it blows FROM (deg) -> its push east and north (kn)
def wind_push(speed_kn, from_deg):
    toward = math.radians((from_deg + 180) % 360)
    return speed_kn * math.sin(toward), speed_kn * math.cos(toward)


# compass direction (0 = north, 90 = east) of a movement east and north
def compass_direction(east, north):
    return math.degrees(math.atan2(east, north)) % 360


# ---- data ----
def load_samples(path=SAMPLES_FILE):
    return pd.read_csv(path, parse_dates=["start_time", "end_time"])


# ---- fitting ----
# fits one linear regression and returns it as a plain dict (easy to save as JSON and to read)
def fit(samples, inputs):
    rows = samples.dropna(subset=inputs + TARGET)
    model = LinearRegression().fit(rows[inputs], rows[TARGET])
    return {
        "inputs": list(inputs),
        "coef": model.coef_.round(6).tolist(),               # 2 rows (east, north) x len(inputs) columns
        "intercept": model.intercept_.round(6).tolist(),     # [east, north]
        "n_samples": int(len(rows)),
    }


def fit_all_tiers(samples):
    return {name: fit(samples, inputs) for name, inputs in TIERS.items()}


def save_models(models, path=MODEL_FILE):
    with open(path, "w") as f:
        json.dump(models, f, indent=2)


def load_models(path=MODEL_FILE):
    with open(path) as f:
        return json.load(f)


# ---- predicting ----
# values: dict of input column -> number. Returns (east, north) nm moved in the next hour.
def predict_with(model, values):
    x = np.array([values[name] for name in model["inputs"]], dtype=float)
    coef = np.array(model["coef"])
    east, north = coef @ x + np.array(model["intercept"])
    return float(east), float(north)


# picks the richest tier whose inputs are all present (and not NaN) in values
def choose_tier(values):
    for name, inputs in TIERS.items():
        if all(name_ in values and values[name_] is not None and not pd.isna(values[name_]) for name_ in inputs):
            return name
    raise ValueError("wind push and position are needed at least: " + ", ".join(WIND + POSITION))


# predicts the next hour's drift from whatever is known; returns (east, north, tier used)
def predict(models, values):
    tier = choose_tier(values)
    east, north = predict_with(models[tier], values)
    return east, north, tier
