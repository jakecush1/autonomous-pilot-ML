#!/usr/bin/env python3
import math
from pyproj import Transformer

# Same idea as usv.py, but instead of using a set quadrant with a csv of locations, we are using utm
# which converts lat/lon to distance from center point, and works in a cartesian plan instead 

# zone settings
CENTER_LAT = 37.353612      # old buoy 46012 position = center of the op zone
CENTER_LON = -122.879874
METERS_PER_NM = 1852
SECTORS = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}  # wind division names

# safety settings
LIMIT_NM = 10.0         # the contract limit
EDGE_NM = 9.0           # past this = close to the limit
OUTER_NM = 6.0          # past this, wind pushing the USV outward needs action
LANE_X_NM = 6.5         # traffic lane starts about 6.8nm east of center; 6nm leaves a buffer
WIND_MEDIUM = 10        # kn

WINDWARD_WIDTH = 60     # degrees either side of where the wind is pushing (a quarter of the circle)

# Using UTM zones so that this can be more reusable and is not stuck to the one location in Half Moon Bay
# instead of having preset squares, use the USV's distance and direction from the center

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
    # always use the center's zone, so every point is measured on the same grid
    utm_zone = get_utm_zone(CENTER_LAT, CENTER_LON)
    to_utm = Transformer.from_crs("EPSG:4326", utm_zone)

    center_x, center_y = to_utm.transform(CENTER_LAT, CENTER_LON)   # center in meters
    x, y = to_utm.transform(lat, lon)                               # point in meters

    x_nm = (x - center_x) / METERS_PER_NM     # nm east of center (west is negative)
    y_nm = (y - center_y) / METERS_PER_NM     # nm north of center (south is negative)
    return x_nm, y_nm

def wind_sector(deg):
    slice_number = int((float(deg) % 360) // 45)
    return SECTORS[slice_number]

def wind_strength(knots):
    wind_strength = float(knots)
    return wind_strength

# windward is upwind from point of reference (being the center), returns T if within 45 deg width
def is_windward(x, y, wind_deg):
    distance = math.hypot(x, y)
    if distance < 1:
        return False    # if close to center direction of wind not important

    # compass direction from center to USV
    usv_bearing = math.degrees(math.atan2(x, y)) % 360 

    # opposite of wind_deg -> direction wind is pushing
    pushing_toward = (wind_deg) % 360

    # print(f"bearing:{usv_bearing}; toward:{pushing_toward}")

    gap = abs(usv_bearing - pushing_toward)
    if gap > 180:
        gap = 360 - gap 

    return gap <= WINDWARD_WIDTH

# checks the USV's position and wind; returns what's wrong, or None if it's safe to drift
# def check_usv(x, y, wind_deg, wind_kn):
def check_usv_location(x, y):
    distance = math.hypot(x, y)               # straight-line nm from the center

    # checked in order of importance: the first problem found is returned
    if distance > LIMIT_NM:
        return "Outside the 10nm zone!"
    if x > LANE_X_NM:
        return "Traffic lane!"
    if distance > EDGE_NM:
        return "Close to the 10nm limit!"
    if distance > OUTER_NM:
        return "Greater than 6nm from center"

    return None

def prompt_user():
    text = input("Input USV lat, lon: ")
    lat, lon = text.split(",")
    lat, lon = float(lat), float(lon)

    # print(f"---Step 2: Drift Prediction---")
    input_angle = input("input wind degree: ").strip()
    wind_deg = float(input_angle)
    wind_letter = wind_sector(wind_deg)
    # input_kn = input("input wind strength: ").strip()
    # wind_kn = wind_strength(input_kn)

    x, y = to_xy(lat, lon)
    distance = math.hypot(x, y)
    print(f"USV is {distance:.1f}nm from center ({x:.1f}nm east, {y:.1f}nm north)")
    # print(f"Wind: {wind_letter}{wind_kn}")

    if is_windward(x, y, wind_deg):
        print("USV is windward = good")
    else:
        print("USV is leeward = bad")

    # warning = check_usv(x, y, wind_deg, wind_kn)
    warning = check_usv_location(x, y)
    if warning is None:
        print("Safe")
    else:
        print(f"Attention: {warning}")
    return warning

def main():
    prompt_user()


if __name__ == "__main__":
    main()