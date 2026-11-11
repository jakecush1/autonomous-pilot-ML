#!/usr/bin/env python3
# Renames new Grafana exports in raw/ to <data type>_<first date>_to_<last date>.csv,
# named by the dates IN the data rather than the download date.
# Exact copies of a file that's already there are moved to raw/duplicates/ instead of renamed.
#
# Run from the data folder:   python rename_raw.py            (renames)
#                             python rename_raw.py --dry-run  (only prints what it would do)
import hashlib
import os
import re
import shutil
import sys
import pandas as pd

RAW_DIR = "raw"
DUPLICATES_DIR = os.path.join(RAW_DIR, "duplicates")

# Grafana panel name (the part before "-data-") -> short name used in the file name
DATA_TYPES = {
    "Torqeedo Motor Power": "torqeedo_motor_power",
    "Motor Power consumption": "motor_power_consumption",
    "True Wind Angle": "wind_angle",
    "True Wind Speed": "wind_speed",
    "Coordinates (gps_location)": "gps_location",
    "Coordinates (navigation.location)": "navigation_location",
}

# files already following the convention, e.g. wind_angle_2026-08-06_to_2026-08-12.csv
ALREADY_NAMED = re.compile(r"^[a-z0-9_]+_\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2}\.csv$")


# fingerprint of a file's contents, used to spot exact copies
def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# "True Wind Speed-data-as-joinbyfield-2026-10-13 14_24_04.csv" -> "wind_speed"
def data_type(file_name):
    panel = file_name.split("-data-")[0]
    if panel in DATA_TYPES:
        return DATA_TYPES[panel]
    # unknown panel: lowercase it and turn anything that isn't a letter or number into "_"
    return re.sub(r"[^a-z0-9]+", "_", panel.lower()).strip("_")


# "2026-08-06_to_2026-08-12", from the first and last times in the file
def date_range(path):
    times = pd.to_datetime(pd.read_csv(path)["Time"])
    return f"{times.min():%Y-%m-%d}_to_{times.max():%Y-%m-%d}"


dry_run = "--dry-run" in sys.argv

# fingerprints of the files that are already named properly
known = {}                                        # hash -> file name
for name in os.listdir(RAW_DIR):
    if ALREADY_NAMED.match(name):
        known[file_hash(os.path.join(RAW_DIR, name))] = name

changes = 0
for name in sorted(os.listdir(RAW_DIR)):
    path = os.path.join(RAW_DIR, name)
    if not name.endswith(".csv") or ALREADY_NAMED.match(name):
        continue

    # exact copy of a file we already have -> move it aside
    fingerprint = file_hash(path)
    if fingerprint in known:
        print(f"duplicate of {known[fingerprint]}: {name} -> duplicates/")
        if not dry_run:
            os.makedirs(DUPLICATES_DIR, exist_ok=True)
            shutil.move(path, os.path.join(DUPLICATES_DIR, name))
        changes = changes + 1
        continue

    new_name = f"{data_type(name)}_{date_range(path)}.csv"
    if os.path.exists(os.path.join(RAW_DIR, new_name)):
        print(f"SKIPPED {name}: {new_name} already exists with different data")
        continue

    print(f"{name} -> {new_name}")
    if not dry_run:
        os.rename(path, os.path.join(RAW_DIR, new_name))
    known[fingerprint] = new_name             # so a second copy of it is caught too
    changes = changes + 1

if changes == 0:
    print("nothing to rename")
elif dry_run:
    print("(dry run, nothing changed)")
