# merge step for the 1-minute Grafana exports
# step 1: load one export and tidy it into useful columns
import os
import numpy as np
import pandas as pd
from pyproj import Transformer

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

CENTER_LAT = 37.353612      # same center as v3-template.py
CENTER_LON = -122.879874
METERS_PER_NM = 1852

to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32610")   # UTM zone 10, the center's zone
CENTER_X, CENTER_Y = to_utm.transform(CENTER_LAT, CENTER_LON)


def load_export(path):
    d = pd.read_csv(path)

    # time: epoch ms in UTC -> local time (the dashboard is UTC-7)
    d["time"] = pd.to_datetime(d["Time"], unit="ms", utc=True).dt.tz_convert("Etc/GMT+7")

    # motor: 0 W = off (drifting), above 0 = on, blank = no data that minute
    d["motor"] = "unknown"
    d.loc[d["motor_power"] == 0, "motor"] = "off"
    d.loc[d["motor_power"] > 0, "motor"] = "on"

    # wind: rebuild the direction from the averaged sin and cos (safe across north)
    d["wind_from_deg"] = np.degrees(np.arctan2(d["wind_from_sin"], d["wind_from_cos"])) % 360
    # the wind's push split into east and north (wind FROM 0 deg pushes TOWARD 180 deg)
    toward = np.radians(d["wind_from_deg"] + 180)
    d["wind_push_east_kn"] = d["wind_speed_kn"] * np.sin(toward)
    d["wind_push_north_kn"] = d["wind_speed_kn"] * np.cos(toward)

    # position: nm east (x) and north (y) of the center
    x, y = to_utm.transform(d["lat"].to_numpy(), d["lon"].to_numpy())
    d["x_nm"] = (x - CENTER_X) / METERS_PER_NM
    d["y_nm"] = (y - CENTER_Y) / METERS_PER_NM
    d.loc[d["lat"].isna(), ["x_nm", "y_nm"]] = np.nan    # no GPS -> no position

    return d[["time", "motor", "motor_power", "wind_speed_kn", "wind_from_deg",
              "wind_push_east_kn", "wind_push_north_kn", "x_nm", "y_nm"]]


if __name__ == "__main__":
    d = load_export(os.path.join(DATA_DIR, "1min_2026-04-17_to_2026-04-29.csv"))
    print(d["motor"].value_counts())
    print(d.head(8).to_string(float_format="%.3f"))
