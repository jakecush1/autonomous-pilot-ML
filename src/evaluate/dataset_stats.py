# Table 1 of the Milestone 4 report: statistics of the whole dataset (development + final test deployments).
# Minutes that two files share (Jun 3-6) are counted once.
#
# usage:  python src/main.py stats     (or: python src/evaluate/dataset_stats.py)
import glob
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # src/
from cmn import data_prep as dp

KN = 1852 / 60    # 1 kn in m/min


def main():
    files = sorted(glob.glob(os.path.join(dp.DATA_DIR, "*.csv")) + glob.glob(os.path.join(dp.HOLDOUT_DIR, "*.csv")))
    raw = pd.concat([pd.read_csv(f) for f in files]).sort_values("Time").drop_duplicates("Time")
    prep = pd.concat([dp.load_file(f) for f in files]).sort_values("Time").drop_duplicates("Time")
    n = len(raw)
    t = pd.to_datetime(raw["Time"], unit="ms")

    print(f"deployments (files)        {len(files)}  ({t.min():%b %d} - {t.max():%b %d, %Y})")
    print(f"records (1 per minute)     {n:,}  ({n / 1440:.1f} days)")
    print(f"with GPS fix               {raw['lat'].notna().sum():,}  ({raw['lat'].notna().sum() / 1440:.1f} days)")
    print(f"missing values             {raw.isna().any(axis=1).mean():.1%} of records")
    print(f"motor off                  {(raw['motor_power'] == 0).sum() / raw['motor_power'].notna().sum():.1%} of minutes with a motor reading")
    good = prep["good"].to_numpy()
    print(f"valid drift minutes        {good.sum():,}  ({good.sum() / 1440:.1f} days)   (after filling gaps of up to {dp.MAX_GAP} min)")

    data = dp.load()
    dev = len(data["train"][0]) + len(data["val"][0])
    print(f"samples (dev / final test) {dev:,} / {len(data['test'][0]):,}   (total {dev + len(data['test'][0]):,})")
    y = np.concatenate([data[s][1] for s in data])
    d = np.hypot(*y.T)
    print(f"target, next-hour drift    median {np.median(d):,.0f} m, 90th pct {np.percentile(d, 90):,.0f} m, max {d.max():,.0f} m")

    speed = np.hypot(prep["dx"], prep["dy"])[good] / KN
    print(f"drift speed (valid min)    median {np.median(speed):.2f} kn")
    w = raw["wind_speed_kn"].dropna()
    print(f"wind speed                 mean {w.mean():.1f} kn, max {w.max():.1f} kn")
    ok = raw["wind_from_sin"].notna()
    deg = np.degrees(np.arctan2(raw["wind_from_sin"], raw["wind_from_cos"])) % 360   # compass bearing the wind comes from
    nw = (deg >= 292.5) & (deg < 337.5)                                # the NW sector of an 8-point compass
    print(f"wind direction             {nw[ok].mean():.0%} from the NW (8-point compass sector)")


if __name__ == "__main__":
    main()
