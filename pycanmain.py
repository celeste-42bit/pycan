# --------------------------------------------
# PyCan V.: 0.0.5 Build 18
# #main
# Copyright (C) 2022 celeste-42bit
# https://github.com/celeste-42bit/pycan
# firmware : rp2-pico-20210202-v1.14.uf2
# --------------------------------------------

from bmp280 import *
from machine import Pin, I2C
import utime
import csv

ERROR = -3  # hPa

# init I2C
i2c_obj = I2C(0,              # I2C id
                 scl = scl,
                 sda = sda,
                 freq = 1000000)
# scan 4 devices
scan = I2C.scan(i2c_obj)
print("I2C scan result : ", scan)  # 118 in decimal is same as 0x76 in hexadecimal
if scan != []:
    print("I2C connection successfull")
else:
    print("No devices found !")
# objectify the BMP280-module
bmp280_obj = BMP280(i2c_obj,
                       addr = 0x76,  # change it 
                       use_case = BMP280_CASE_DROP)

# sensor config ---------------------------------
bmp280_obj.power_mode = BMP280_POWER_NORMAL
bmp280_obj.oversample = BMP280_OS_HIGH
bmp280_obj.temp_os = BMP280_TEMP_OS_8
bmp280_obj.press_os = BMP280_TEMP_OS_4
bmp280_obj.standby = BMP280_STANDBY_250
bmp280_obj.iir = BMP280_IIR_FILTER_2
# -----------------------------------------------

def altitude_HYP(hPa , temperature):
    # Hypsometric Equation (Temp compensated) (Max Altitude < 11 Km above sea level)
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25 # hPa
    #TODO IMPORTANT: implement a way to input the actual pressure at sea level, according to flight weather!
    pressure_ratio = sea_level_pressure/local_pressure  # sea level pressure = 1013.25 hPa
    alt = (((pressure_ratio**(1/5.257)) - 1) * temperature ) / 0.0065
    return alt

def w2csv(row):
    with open("data.csv", "w", encoding='UTF8') as f:
        # writer = csv.writer(f)
        csv.writer.writerow(row)
        print("WRT")

def createcsvrow(data):  # pass data as list!
    # TODO: create row out of data list!
    # -----------------------------------------
    # for now, do that:
    row = data
    print(row)
    w2csv(row)
    # -----------------------------------------


# MAIN LOOP FOR IN_FLIGHT RUN --------------------------------------------



while True:
    # accquire temp
    temperature_c = bmp280_obj.temperature  # degree celcius
    temperature_k = temperature_c + 273.15  # degree kelvin
    # accquire pressure
    pressure = ( bmp280_obj.pressure * 0.01 ) + ERROR  # hPa
    # accquire alt values from IBF
    altitude = altitude_HYP(pressure, temperature_k)



# MAIN LOOP FOR IN_FLIGHT RUN --------------------------------------------