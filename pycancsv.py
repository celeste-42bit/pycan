# --------------------------------------------
# pycancsv V.: 0.0.1 Build 0
# #csvwriter
# Copyright (C) 2022 celeste-42bit
# https://github.com/celeste-42bit/pycan
# firmware : rp2-pico-20210202-v1.14.uf2
# --------------------------------------------

from os.path import getsize
import time

start_time = time.time()

def w2csv(row):
    if getsize("data.csv") == 0:
        with open("data.csv", "w", encoding="UTF8") as f:
            f.write(time.time() , " ", row, "\n")
            print("WRT-N")  # write-new
    else:
        with open("data.csv", "a", encoding="UTF8") as f:
            f.write(time.time(), " ", row, "\n")
            print("WRT-A")  # write-append