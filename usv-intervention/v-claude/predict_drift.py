#!/usr/bin/env python3
# Predicts where the USV will be in an hour (and optionally further ahead) using the trained
# drift model in drift_model.json.
#
# Inputs: the USV's position now, the wind now, and (optionally) its position one and two hours
# ago, which is how the pilot sees past drift: as points on the track. The model uses as much as
# it is given: two past hours > one past hour > wind and position only.
#
# Run from this folder, either with arguments:
#   python predict_drift.py --lat 37.4113 --lon -122.7982 --wind-kn 13 --wind-from 318 \
#       --last-lat 37.4150 --last-lon -122.8020 --last2-lat 37.4190 --last2-lon -122.8060 --hours 3
# or with none, and it will ask for each value (press Enter to skip a past position).
import argparse
import math
from drift_model import (load_models, predict, to_xy, to_latlon, wind_push, compass_direction)

LIMIT_NM = 10.0         # the contract limit
LANE_X_NM = 6.5         # traffic lane starts about 6.8 nm east of center


def parse_args():
    parser = argparse.ArgumentParser(description="predict the USV's drift over the next hour(s)")
    parser.add_argument("--lat", type=float, help="USV latitude now")
    parser.add_argument("--lon", type=float, help="USV longitude now")
    parser.add_argument("--wind-kn", type=float, help="true wind speed now, knots")
    parser.add_argument("--wind-from", type=float, help="direction the wind blows FROM, degrees true")
    parser.add_argument("--last-lat", type=float, help="latitude one hour ago (motor off since)")
    parser.add_argument("--last-lon", type=float, help="longitude one hour ago")
    parser.add_argument("--last2-lat", type=float, help="latitude two hours ago (motor off since)")
    parser.add_argument("--last2-lon", type=float, help="longitude two hours ago")
    parser.add_argument("--hours", type=int, default=1, help="how many hours ahead to predict (default 1)")
    return parser.parse_args()


def ask(prompt, optional=False):
    text = input(prompt).strip()
    if text == "" and optional:
        return None
    return float(text)


def ask_latlon(prompt, optional=False):
    text = input(prompt).strip()
    if text == "" and optional:
        return None, None
    lat, lon = text.split(",")
    return float(lat), float(lon)


def main():
    args = parse_args()
    if args.lat is None:                              # nothing given: ask for everything
        args.lat, args.lon = ask_latlon("USV lat, lon now: ")
        args.wind_kn = ask("wind speed now (kn): ")
        args.wind_from = ask("wind blowing FROM (deg): ")
        args.last_lat, args.last_lon = ask_latlon("lat, lon one hour ago (Enter if motor was on): ", optional=True)
        if args.last_lat is not None:
            args.last2_lat, args.last2_lon = ask_latlon("lat, lon two hours ago (Enter to skip): ", optional=True)

    models = load_models()

    # inputs now
    x, y = to_xy(args.lat, args.lon)
    push_east, push_north = wind_push(args.wind_kn, args.wind_from)
    values = {"start_x_nm": x, "start_y_nm": y,
              "wind_push_east_kn": push_east, "wind_push_north_kn": push_north}

    # past drift, from the past positions on the track
    if args.last_lat is not None:
        last_x, last_y = to_xy(args.last_lat, args.last_lon)
        values["last_moved_east_nm"] = x - last_x
        values["last_moved_north_nm"] = y - last_y
        if args.last2_lat is not None:
            last2_x, last2_y = to_xy(args.last2_lat, args.last2_lon)
            values["last2_moved_east_nm"] = last_x - last2_x
            values["last2_moved_north_nm"] = last_y - last2_y

    print(f"now: {math.hypot(x, y):.2f} nm from center ({x:.2f} nm east, {y:.2f} nm north), "
          f"wind {args.wind_kn:g} kn from {args.wind_from:g} deg")
    if "last_moved_east_nm" in values:
        e, n = values["last_moved_east_nm"], values["last_moved_north_nm"]
        print(f"last hour: drifted {math.hypot(e, n):.2f} nm toward {compass_direction(e, n):.0f} deg")

    # roll forward hour by hour; wind is held constant and each prediction becomes the next "last hour"
    for hour in range(1, args.hours + 1):
        east, north, tier = predict(models, values)
        x, y = x + east, y + north
        lat, lon = to_latlon(x, y)
        distance = math.hypot(x, y)
        print(f"+{hour} h: drift {math.hypot(east, north):.2f} nm toward {compass_direction(east, north):.0f} deg "
              f"-> {lat:.5f}, {lon:.5f}  ({distance:.2f} nm from center)  [model: {tier}]")
        if distance > LIMIT_NM:
            print("      outside the 10 nm zone!")
        elif x > LANE_X_NM:
            print("      in the traffic lane!")
        # next hour's inputs
        values.update({"start_x_nm": x, "start_y_nm": y,
                       "last2_moved_east_nm": values.get("last_moved_east_nm"),
                       "last2_moved_north_nm": values.get("last_moved_north_nm"),
                       "last_moved_east_nm": east, "last_moved_north_nm": north})
        values = {k: v for k, v in values.items() if v is not None}


if __name__ == "__main__":
    main()
