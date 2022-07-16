# --------------------------------------------
# pycancsv V.: 0.0.2 Build 2
# #csvwriter
# Copyright (C) 2022 celeste-42bit
# REPO: https://github.com/celeste-42bit/pycan
# DOCS: https://github.com/celeste-42bit/pycan/docs.md
# firmware : rp2-pico-20210202-v1.14.uf2
# --------------------------------------------

import time

start_time = time.time()

def w2csv(row):  # row is the list of sensor data passed in to write into the file
    with open("data.csv", "a", encoding="UTF8") as f:
        try:
            cropped_row = str(row)
            compact = str(time.time() - start_time) + ", " + cropped_row[1:-1] + "\n"  # row[1:-1] removes the list brackets (1st and last char are being chopped off)
            # FORMAT: Time, Altitude, Pressure, Temperature
            f.write(compact)
            print(compact)  # debug only
        except Exception:
            pass

def header():
    with open("data.csv", "a", encoding="UTF-8") as f:
        try:
            f.write("Time, Altitude, Pressure, Temperature" + "\n")
        except Exception:
            pass