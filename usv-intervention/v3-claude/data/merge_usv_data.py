#!/usr/bin/env python3
# v3-claude version of merge_usv_data.py.
#
# Combines the Grafana exports (GPS location, true wind speed, true wind angle, motor power)
# into one HOURLY table, saves the hours when the motor was off, and builds drift samples:
# one row per hour of drifting, with the wind, the position, the last hours' drift, and how far
# the USV moved.
#
# Differences from v3/data/merge_usv_data.py:
#   * The hourly rows come from the GPS export. Its "Motor Power" column is the hourly average
#     motor power for every date range, so motor-off hours are found even where the motor-power
#     panel was exported at 2-hour, 20-minute or 2-minute steps. (The old script only used the
#     motor-power file and so got 0 drift samples from May 20 - Jun 4 and Oct 17 - 21.)
#   * Wind readings at any time step are resampled to hourly: readings inside the hour are
#     vector-averaged; readings coarser than an hour (the 2-hour May export) are spread over the
#     hours they cover. "wind_readings" says how many readings went into each hour.
#   * Drift samples also carry the drift two hours ago, the position at the start of the hour,
#     and how many hours the USV had already been drifting.
#
# Each hourly row covers the hour STARTING at its time: "01:00" = 01:00 to 02:00 (Grafana labels
# its time buckets by their start).
#
# Run from this folder:   python merge_usv_data.py [raw folder]
# The raw folder defaults to ../../v3/data/raw so the exports are not copied twice.
import glob
import math
import os
import sys
import numpy as np
import pandas as pd
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "v3", "data", "raw")

# ---- output files (written next to this script) ----
ALL_HOURS_FILE = os.path.join(HERE, "usv_hourly.csv")
MOTOR_OFF_FILE = os.path.join(HERE, "usv_motor_off.csv")
DRIFT_FILE = os.path.join(HERE, "usv_drift_samples.csv")

# ---- settings ----
CENTER_LAT = 37.353612      # old buoy 46012 position = center of the op zone
CENTER_LON = -122.879874
METERS_PER_NM = 1852
MOTOR_OFF_MAX_W = 0.0       # an hour counts as "motor off" when its average motor power is at most this
                            # (0 = strictly off; a few hours sit at 0.1 - 2 W, probably seconds of motor use)


# turns text like "835 mW" or "86.2 W" into watts
def to_watts(text):
    number, unit = str(text).split()
    number = float(number)
    if unit in ("mW", "mWh"):
        return number / 1000
    if unit in ("kW", "kWh"):
        return number * 1000
    return number                             # W or Wh


# turns text like "7.12 kn" or "307 °" into just the number
def to_number(text):
    number, unit = str(text).split()
    return float(number)


# works out which UTM zone a point is in, in the form pyproj needs
def get_utm_zone(lat, lon):
    zone = int((lon + 180) // 6) + 1          # -122.88 -> zone 10
    if lat >= 0:
        code = 32600 + zone                   # northern hemisphere -> 32610
    else:
        code = 32700 + zone                   # southern hemisphere
    return f"EPSG:{code}"


# one transformer for the whole run (building it is slow)
TO_UTM = Transformer.from_crs("EPSG:4326", get_utm_zone(CENTER_LAT, CENTER_LON))
CENTER_X, CENTER_Y = TO_UTM.transform(CENTER_LAT, CENTER_LON)


# turns lat, lon into nm east (x) and nm north (y) of the center
def to_xy(lat, lon):
    x, y = TO_UTM.transform(lat, lon)
    return (x - CENTER_X) / METERS_PER_NM, (y - CENTER_Y) / METERS_PER_NM


# compass direction (0 = north, 90 = east) of a movement east and north
def compass_direction(east, north):
    return math.degrees(math.atan2(east, north)) % 360


# the usual gap between readings in a file, in hours (1.0 for hourly, 2.0, 0.333, 0.033...)
def time_step_hours(times):
    gaps = times.sort_values().diff().dropna().dt.total_seconds() / 3600
    return float(gaps.mode().iloc[0])


# ---- wind: readings at any time step -> one row per hour ----
def read_wind(speed_file, angle_file):
    speed = pd.read_csv(speed_file)
    angle = pd.read_csv(angle_file)
    wind = speed.merge(angle, on="Time")
    wind["time"] = pd.to_datetime(wind["Time"])
    wind["speed"] = wind["Average"].apply(to_number)
    wind["speed_min"] = wind["Min"].apply(to_number)
    wind["speed_max"] = wind["Max"].apply(to_number)
    wind["from_deg"] = wind["Wind Angle"].apply(to_number)

    # the wind's push split into east and north parts
    # (wind FROM 0 deg blows TOWARD 180 deg, so flip it first)
    toward = np.radians((wind["from_deg"] + 180) % 360)
    wind["push_east"] = wind["speed"] * np.sin(toward)
    wind["push_north"] = wind["speed"] * np.cos(toward)

    # which hour(s) each reading belongs to: a reading at 13:40 belongs to hour 13:00;
    # a 2-hour reading at 13:00 covers hours 13:00 and 14:00
    step = time_step_hours(wind["time"])
    hours_covered = max(1, int(round(step)))
    rows = []
    for _, reading in wind.iterrows():
        first_hour = reading["time"].floor("h")
        for k in range(hours_covered):
            rows.append({
                "time": first_hour + pd.Timedelta(hours=k),
                "speed": reading["speed"],
                "speed_min": reading["speed_min"],
                "speed_max": reading["speed_max"],
                "push_east": reading["push_east"],
                "push_north": reading["push_north"],
            })
    per_hour = pd.DataFrame(rows).groupby("time").agg(
        wind_speed_kn=("speed", "mean"),
        wind_speed_min_kn=("speed_min", "min"),
        wind_speed_max_kn=("speed_max", "max"),
        wind_push_east_kn=("push_east", "mean"),      # vector average, so the direction averages properly
        wind_push_north_kn=("push_north", "mean"),
        wind_readings=("speed", "size"),
    ).reset_index()
    # direction the averaged wind comes FROM
    toward_deg = np.degrees(np.arctan2(per_hour["wind_push_east_kn"], per_hour["wind_push_north_kn"]))
    per_hour["wind_from_deg"] = ((toward_deg + 180) % 360).round(1)
    per_hour["wind_step_hours"] = step
    return per_hour


# ---- motor power file: hours in which ANY reading was above the off threshold ----
# (only useful when the file is at least hourly; coarser files are ignored, the GPS hourly value is finer)
def read_motor_on_hours(power_file):
    raw = pd.read_csv(power_file)
    times = pd.to_datetime(raw["Time"])
    if time_step_hours(times) > 1.0:
        return set()
    column = "Motor Power" if "Motor Power" in raw.columns else "Motor"
    watts = raw[column].apply(to_watts)
    return set(times[watts > MOTOR_OFF_MAX_W].dt.floor("h"))


# ---- one date range -> hourly table ----
def read_export(files):
    gps = pd.read_csv(files["gps"])
    table = pd.DataFrame()
    table["time"] = pd.to_datetime(gps["Time"])
    table["latitude"] = gps["Latitude"]
    table["longitude"] = gps["Longitude"]
    table["motor_power_w"] = gps["Motor Power"].round(3)      # hourly average motor power

    motor_on_hours = read_motor_on_hours(files["power"]) if os.path.exists(files["power"]) else set()
    table["motor_off"] = (table["motor_power_w"] <= MOTOR_OFF_MAX_W) & ~table["time"].isin(motor_on_hours)

    wind = read_wind(files["wind_speed"], files["wind_angle"])
    table = table.merge(wind, on="time", how="left")

    xy = [to_xy(lat, lon) for lat, lon in zip(table["latitude"], table["longitude"])]
    table["x_nm"] = [round(x, 4) for x, y in xy]
    table["y_nm"] = [round(y, 4) for x, y in xy]
    table["distance_nm"] = np.hypot(table["x_nm"], table["y_nm"]).round(3)
    table["export"] = files["dates"]
    return table


# ---- 1. find every export in raw/ (named by rename_raw.py) and stack them, oldest first ----
EXPORTS = []
for gps_file in sorted(glob.glob(os.path.join(RAW_DIR, "gps_location_*.csv"))):
    dates = os.path.basename(gps_file)[len("gps_location_"):-len(".csv")]      # "2026-08-06_to_2026-08-12"
    EXPORTS.append({
        "dates": dates,
        "gps": gps_file,
        "power": os.path.join(RAW_DIR, f"torqeedo_motor_power_{dates}.csv"),
        "wind_speed": os.path.join(RAW_DIR, f"wind_speed_{dates}.csv"),
        "wind_angle": os.path.join(RAW_DIR, f"wind_angle_{dates}.csv"),
    })
if not EXPORTS:
    sys.exit(f"no gps_location_*.csv files found in {RAW_DIR}")

table = pd.concat([read_export(files) for files in EXPORTS])
table = table.drop_duplicates("time").sort_values("time").reset_index(drop=True)
for column in ["wind_speed_kn", "wind_speed_min_kn", "wind_speed_max_kn", "wind_push_east_kn", "wind_push_north_kn"]:
    table[column] = table[column].round(3)

# ---- 2. number each unbroken stretch of motor-off hours: 1, 2, 3... (0 = motor on) ----
stretch_ids = []
stretch = 0
for i in range(len(table)):
    off = table["motor_off"][i]
    continues = (i > 0 and table["motor_off"][i - 1]
                 and table["time"][i] - table["time"][i - 1] == pd.Timedelta(hours=1))
    if off and not continues:
        stretch = stretch + 1                 # a new drift stretch starts
    stretch_ids.append(stretch if off else 0)
table["drift_stretch"] = stretch_ids

# ---- 3. drift samples: two back-to-back hours, motor off in both, wind known at the start ----
samples = []
for i in range(len(table) - 1):
    now = table.iloc[i]
    later = table.iloc[i + 1]
    one_hour_apart = later["time"] - now["time"] == pd.Timedelta(hours=1)
    both_off = now["motor_off"] and later["motor_off"]
    if not (one_hour_apart and both_off and not pd.isna(now["wind_speed_kn"])):
        continue

    moved_east = later["x_nm"] - now["x_nm"]          # nm moved east in the hour
    moved_north = later["y_nm"] - now["y_nm"]         # nm moved north in the hour
    samples.append({
        "start_time": now["time"],
        "end_time": later["time"],
        "export": now["export"],
        "drift_stretch": now["drift_stretch"],
        "start_lat": now["latitude"],
        "start_lon": now["longitude"],
        "end_lat": later["latitude"],
        "end_lon": later["longitude"],
        "start_x_nm": now["x_nm"],                     # position at the start of the hour, nm from center
        "start_y_nm": now["y_nm"],
        "start_distance_nm": now["distance_nm"],
        "wind_speed_kn": now["wind_speed_kn"],         # wind at the START of the hour only:
        "wind_from_deg": now["wind_from_deg"],         # in live use, that's all we know when predicting
        "wind_push_east_kn": now["wind_push_east_kn"],
        "wind_push_north_kn": now["wind_push_north_kn"],
        "wind_readings": int(now["wind_readings"]),
        "moved_east_nm": round(moved_east, 4),
        "moved_north_nm": round(moved_north, 4),
        "drift_speed_kn": round(math.hypot(moved_east, moved_north), 4),        # nm in one hour = knots
        "drift_toward_deg": round(compass_direction(moved_east, moved_north), 1),
    })
drift = pd.DataFrame(samples)

# past drift: filled in when the earlier sample is the hour right before (blank otherwise)
by_start = {row["start_time"]: row for row in samples}
for lag, name in [(1, "last"), (2, "last2")]:
    east, north = [], []
    for row in samples:
        earlier = by_start.get(row["start_time"] - pd.Timedelta(hours=lag))
        same_stretch = earlier is not None and earlier["drift_stretch"] == row["drift_stretch"]
        east.append(earlier["moved_east_nm"] if same_stretch else None)
        north.append(earlier["moved_north_nm"] if same_stretch else None)
    drift[f"{name}_moved_east_nm"] = east
    drift[f"{name}_moved_north_nm"] = north

# how many hours of drifting came before this sample in the same stretch
drift["hours_drifting_before"] = drift.groupby("drift_stretch").cumcount()

# ---- 4. save ----
table.to_csv(ALL_HOURS_FILE, index=False)
motor_off = table[table["motor_off"]]
motor_off.to_csv(MOTOR_OFF_FILE, index=False)
drift.to_csv(DRIFT_FILE, index=False)

print(f"{len(table)} hours, {len(motor_off)} with the motor off, in {stretch} drift stretches")
print(f"{table['wind_speed_kn'].isna().sum()} hours have no wind")
print(f"{len(drift)} drift samples (one hour of drifting each), "
      f"{drift['last_moved_east_nm'].notna().sum()} with last hour's drift, "
      f"{drift['last2_moved_east_nm'].notna().sum()} with the last two hours'")
print()
print("per export:")
for dates in sorted(table["export"].unique()):
    hours = table[table["export"] == dates]
    n_samples = (drift["export"] == dates).sum()
    step = hours["wind_step_hours"].iloc[0]
    print(f"  {dates}: {len(hours):4d} hours, {hours['motor_off'].sum():4d} motor off, "
          f"{n_samples:4d} drift samples, wind every {step:g} h")
