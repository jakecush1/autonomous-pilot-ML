#!/usr/bin/env python3
import sys
import pandas as pd
import ast

SECTORS = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
df = pd.read_csv('../data/noaa_grid_9x9.csv')

# turns the text "(37.47, -122.97)" into two numbers
def read_corner(text):
    lat, lon = text.strip("()").split(",")
    return float(lat), float(lon)


# given a lat and lon, find which square it is in
def location(lat, lon):
    for i, row in df.iterrows():                      # go through the squares one at a time
        top_lat, left_lon = read_corner(row["top_left"])
        bottom_lat, right_lon = read_corner(row["bottom_right"])

        # is the point between this square's top and bottom, and between its left and right?
        if bottom_lat <= lat < top_lat and left_lon <= lon < right_lon:
            return int(row["square_id"])

    return None                                       # no square matched, so it's off the grid

def wind_sector(deg):
    slice_number = int((int(deg) % 360) // 45)
    return SECTORS[slice_number]

def wind_strength(knots):
    wind_strength = knots

    return wind_strength

def good_or_bad(q_num, wind_kn, wind_letter):
    bad = [1,2,3,4,5,6,7,8,9,10,11,12,16,17,18,19,20,26,27,28,35,36,37,44,45,46,53,54,55,56,62,63,64,65,66,70,71,72,73,74,75,76,77,78,79,80,81]
    if q_num in bad:
        return False
    
    return True

def prompt_user():
    text = input("Input USV lat, lon: ")
    lat, lon = text.split(",")             # "37.431827, -122.786952" -> ["37.431827", " -122.786952"]
    lat, lon = float(lat), float(lon)      # text -> numbers
    square_num = location(lat, lon)

    if square_num is None:
        print("USV is outside the grid")
        return False
    else:
        input_angle = input("input wind degree: ").strip()
        wind_letter = wind_sector(input_angle)
        input_kn = input("input wind strength: ").strip()
        wind_kn = wind_strength(input_kn)
        print(f"USV in square: {square_num}")
        print(f"Wind: {wind_letter}{wind_kn}")

def main():
    prompt_user()


if __name__ == "__main__":
    main()