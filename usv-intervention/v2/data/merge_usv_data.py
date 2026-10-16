#!/usr/bin/env python3
# Combines the Grafana exports (motor power, true wind speed, true wind angle, GPS location)
# into one hourly table, saves the hours when the motor was off, and builds drift samples:
# one row per hour of drifting, with the wind and how far the USV moved.
#
# Each hourly row covers the hour STARTING at its time: "01:00" = 01:00 to 02:00.
import math
import numpy as np
import pandas as pd
from pyproj import Transformer

# ---- input files: add a new block for each new export ----
EXPORTS = [
    {   # Oct 3 - 12, 2026 (hourly motor power)
        "power": "raw/torqeedo_motor_power_2026-10-03_to_2026-10-12.csv",
        "wind_speed": "raw/wind_speed_2026-10-03_to_2026-10-12.csv",
        "wind_angle": "raw/wind_angle_2026-10-03_to_2026-10-12.csv",
        "gps": "raw/gps_location_2026-10-03_to_2026-10-12.csv",
    },
    {   # Aug 6 - 12, 2026 (hourly motor power)
        "power": "raw/torqeedo_motor_power_2026-08-06_to_2026-08-12.csv",
        "wind_speed": "raw/wind_speed_2026-08-06_to_2026-08-12.csv",
        "wind_angle": "raw/wind_angle_2026-08-06_to_2026-08-12.csv",
        "gps": "raw/gps_location_2026-08-06_to_2026-08-12.csv",
    },
]

# ---- output files ----
ALL_HOURS_FILE = "usv_hourly.csv"
MOTOR_OFF_FILE = "usv_motor_off.csv"
DRIFT_FILE = "usv_drift_samples.csv"

# ---- zone settings (same as usv_safety_check.py) ----
CENTER_LAT = 37.353612      # old buoy 46012 position = center of the op zone
CENTER_LON = -122.879874
METERS_PER_NM = 1852


# turns text like "835 mW" or "86.2 W" into watts
# (the 10-minute export labels its values Wh, but they match the hourly watts, so they're treated as watts)
def to_watts(text):
    number, unit = text.split()
    number = float(number)
    if unit == "mW" or unit == "mWh":
        return number / 1000
    if unit == "kW" or unit == "kWh":
        return number * 1000
    return number                             # W or Wh


# turns text like "7.12 kn" or "307 °" into just the number
def to_number(text):
    number, unit = text.split()
    return float(number)


# works out which UTM zone a point is in, in the form pyproj needs
def get_utm_zone(lat, lon):
    zone = int((lon + 180) // 6) + 1          # -122.88 -> zone 10
    if lat >= 0:
        code = 32600 + zone                   # northern hemisphere -> 32610
    else:
        code = 32700 + zone                   # southern hemisphere
    return f"EPSG:{code}"


# turns lat, lon into nm east (x) and nm north (y) of the center
def to_xy(lat, lon):
    utm_zone = get_utm_zone(CENTER_LAT, CENTER_LON)
    to_utm = Transformer.from_crs("EPSG:4326", utm_zone)
    center_x, center_y = to_utm.transform(CENTER_LAT, CENTER_LON)
    x, y = to_utm.transform(lat, lon)
    x_nm = (x - center_x) / METERS_PER_NM
    y_nm = (y - center_y) / METERS_PER_NM
    return x_nm, y_nm


# compass direction (0 = north, 90 = east) of a movement east and north
def compass_direction(east, north):
    return math.degrees(math.atan2(east, north)) % 360


# reads a motor power export and returns one row per hour: time, motor_power_w, motor_off
# works with both formats: hourly "Motor Power" and 10-minute "Motor"
def read_motor_power(file):
    raw = pd.read_csv(file)

    # hourly export: one reading per hour already
    if "Motor Power" in raw.columns:
        hourly = pd.DataFrame()
        hourly["time"] = raw["Time"]
        hourly["motor_power_w"] = raw["Motor Power"].apply(to_watts)
        hourly["motor_off"] = hourly["motor_power_w"] == 0
        return hourly

    # 10-minute export: collect the readings for each hour
    hours = {}                                        # "2026-08-06 01:00:00" -> list of readings
    for time_text, power_text in zip(raw["Time"], raw["Motor"]):
        hour = time_text[:13] + ":00:00"              # "2026-08-06 01:40:00" -> "2026-08-06 01:00:00"
        if hour not in hours:
            hours[hour] = []
        hours[hour].append(to_watts(power_text))

    rows = []
    for hour, readings in hours.items():
        rows.append({
            "time": hour,
            "motor_power_w": round(sum(readings) / len(readings), 3),   # average for the hour
            "motor_off": len(readings) == 6 and max(readings) == 0,     # all six readings are 0
        })
    return pd.DataFrame(rows)


# builds the clean hourly table for one export
def read_export(files):
    power = read_motor_power(files["power"])
    speed = pd.read_csv(files["wind_speed"])
    angle = pd.read_csv(files["wind_angle"])
    gps = pd.read_csv(files["gps"])

    # line everything up by time (some hours have no GPS)
    data = power.merge(speed, left_on="time", right_on="Time")
    data = data.merge(angle, on="Time")
    data = data.merge(gps[["Time", "Latitude", "Longitude"]], on="Time", how="left")

    table = pd.DataFrame()
    table["time"] = data["time"]
    table["motor_power_w"] = data["motor_power_w"]
    table["motor_off"] = data["motor_off"]
    table["wind_speed_kn"] = data["Average"].apply(to_number)
    table["wind_speed_min_kn"] = data["Min"].apply(to_number)
    table["wind_speed_max_kn"] = data["Max"].apply(to_number)
    table["wind_from_deg"] = data["Wind Angle"].apply(to_number)

    # the wind's push split into east and north parts, ready for the drift model
    # (wind FROM 0 deg blows TOWARD 180 deg, so flip it first)
    toward = (table["wind_from_deg"] + 180) % 360
    table["wind_push_east_kn"] = (table["wind_speed_kn"] * np.sin(np.radians(toward))).round(3)
    table["wind_push_north_kn"] = (table["wind_speed_kn"] * np.cos(np.radians(toward))).round(3)

    # position, as lat/lon and as nm east/north of the center
    table["latitude"] = data["Latitude"]
    table["longitude"] = data["Longitude"]
    x_list = []
    y_list = []
    for lat, lon in zip(table["latitude"], table["longitude"]):
        if pd.isna(lat):
            x_list.append(None)               # no GPS this hour
            y_list.append(None)
        else:
            x, y = to_xy(lat, lon)
            x_list.append(round(x, 4))
            y_list.append(round(y, 4))
    table["x_nm"] = x_list
    table["y_nm"] = y_list
    table["distance_nm"] = np.hypot(table["x_nm"], table["y_nm"]).round(3)
    return table


# ---- 1. read every export and stack them into one table, oldest first ----
tables = []
for files in EXPORTS:
    tables.append(read_export(files))
table = pd.concat(tables).drop_duplicates("time").sort_values("time").reset_index(drop=True)
times = pd.to_datetime(table["time"])

# ---- 2. number each unbroken stretch of motor-off hours: 1, 2, 3... (0 = motor on) ----
stretch_ids = []
stretch = 0
for i in range(len(table)):
    off = table["motor_off"][i]
    continues = i > 0 and table["motor_off"][i - 1] and times[i] - times[i - 1] == pd.Timedelta(hours=1)
    if off and not continues:
        stretch = stretch + 1                 # a new drift stretch starts
    if off:
        stretch_ids.append(stretch)
    else:
        stretch_ids.append(0)
table["drift_stretch"] = stretch_ids

# ---- 3. drift samples: two back-to-back hours, motor off in both, GPS in both ----
samples = []
for i in range(len(table) - 1):
    now = table.iloc[i]
    later = table.iloc[i + 1]

    one_hour_apart = times[i + 1] - times[i] == pd.Timedelta(hours=1)
    both_off = now["motor_off"] and later["motor_off"]
    both_have_gps = not pd.isna(now["x_nm"]) and not pd.isna(later["x_nm"])
    if not (one_hour_apart and both_off and both_have_gps):
        continue

    moved_east = later["x_nm"] - now["x_nm"]          # nm moved east in the hour
    moved_north = later["y_nm"] - now["y_nm"]         # nm moved north in the hour

    # push_east = (now["wind_push_east_kn"] + later["wind_push_east_kn"]) / 2     # average wind over the two readings
    # push_north = (now["wind_push_north_kn"] + later["wind_push_north_kn"]) / 2
    push_east = now["wind_push_east_kn"]       # wind at the START of the hour only:
    push_north = now["wind_push_north_kn"]     # in live use, that's all we know when predicting

    samples.append({
        "start_time": now["time"],
        "end_time": later["time"],
        "start_lat": now["latitude"],
        "start_lon": now["longitude"],
        "end_lat": later["latitude"],
        "end_lon": later["longitude"],
        "wind_speed_kn": round((now["wind_speed_kn"] + later["wind_speed_kn"]) / 2, 2),
        "wind_from_deg": round((compass_direction(push_east, push_north) + 180) % 360, 1),
        "wind_push_east_kn": round(push_east, 3),
        "wind_push_north_kn": round(push_north, 3),
        "moved_east_nm": round(moved_east, 4),
        "moved_north_nm": round(moved_north, 4),
        "drift_speed_kn": round(math.hypot(moved_east, moved_north), 4),        # nm in one hour = knots
        "drift_toward_deg": round(compass_direction(moved_east, moved_north), 1),
        "drift_stretch": now["drift_stretch"],
    })
drift = pd.DataFrame(samples)

# ---- 4. save ----
table.to_csv(ALL_HOURS_FILE, index=False)
motor_off = table[table["motor_off"]]
motor_off.to_csv(MOTOR_OFF_FILE, index=False)
drift.to_csv(DRIFT_FILE, index=False)

print(f"{len(table)} hours, {len(motor_off)} with the motor off, in {stretch} drift stretches")
print(f"{table['latitude'].isna().sum()} hours have no GPS")
print(f"{len(drift)} drift samples (one hour of drifting each)")
