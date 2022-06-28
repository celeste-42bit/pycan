# --------------------------------------------
# pycancsv V.: 0.0.2 Build 1
# #csvwriter
# Copyright (C) 2022 celeste-42bit
# REPO: https://github.com/celeste-42bit/pycan
# DOCS: https://github.com/celeste-42bit/pycan/docs.md
# firmware : rp2-pico-20210202-v1.14.uf2
# --------------------------------------------

from os.path import getsize
import time

start_time = time.time()


def w2csv(row):
    if getsize("data.csv") == 0:
        with open("data.csv", "w", encoding="UTF8") as f:
            try:
                compact = str(time.time()) + " " + str(row) + "\n"
                f.write(compact)
                print(str(time.time()), "W-N: ", str(row))  # debug only! TODO remove!
            except Exception as e:
                pass
    else:
        with open("data.csv", "a", encoding="UTF8") as f:
            try:
                compact = str(time.time()) + " " + str(row) + "\n"  # TODO write time into list by using list.append()
                f.write(compact)
                print(str(time.time()), "W-A: ", str(row))  # debug only! TODO remove!
            except Exception as e:
                pass
