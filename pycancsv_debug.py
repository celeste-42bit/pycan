# --------------------------------------------
# pycancsv_debug DEBUG
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
                compact = str(time.time()) + " " + str(row) + "\n"
                f.write(compact)
                print(str(time.time()), "W-A: ", str(row))  # debug only! TODO remove!
            except Exception as e:
                pass


rows = [1, 0, "text", 4, 176, 63.5, 7, 22, 0o3221, 1]
w2csv(rows)
