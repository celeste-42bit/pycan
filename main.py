# --------------------------------------------
# PyCan V.: 0.1.6 Build 12 [^]
# #main
# Copyright (C) 2022 celeste-42bit
# REPO: https://github.com/celeste-42bit/pycan
# DOCS: https://github.com/celeste-42bit/pycan/docs.md
# firmware : rp2-pico-20210202-v1.14.uf2
# --------------------------------------------

from pycanbmp import *
from machine import Pin, I2C
import utime
import time
from pycancsv import w2csv, header

# manual error correction --------------------
ERROR = 0  # hPa
alt_ERROR = 0  # m
# --------------------------------------------

sda = Pin(0)
scl = Pin(1)  # change due to interference?! TODO find out!
led = Pin(25, Pin.OUT)  # LED = writing to storage
led.off()
# init I2C
i2c_obj = I2C(0,              # I2C id
                 scl = scl,
                 sda = sda,
                 freq = 1000000)
# scan 4 devices
scan = I2C.scan(i2c_obj)
print("I2C Scan : ", scan)  # 118 in decimal is same as 0x76 in hexadecimal
if scan != []:
    print("I2C connection successfull")
else:
    print("ERROR: No devices found !")
    w2csv("Terminated, no I2C device found!")
    exit()

# objectify the BMP280-module
bmp280_obj = BMP280(i2c_obj, addr = 0x76, use_case = BMP280_CASE_DROP)

# bmp280 sensor config ------------------------
bmp280_obj.power_mode = BMP280_POWER_NORMAL
bmp280_obj.oversample = BMP280_OS_HIGH
bmp280_obj.temp_os = BMP280_TEMP_OS_8
bmp280_obj.press_os = BMP280_TEMP_OS_4
bmp280_obj.standby = BMP280_STANDBY_250
bmp280_obj.iir = BMP280_IIR_FILTER_2
# ---------------------------------------------

def calc_alt_HYP(hPa , temperature):  # TODO compare the hypsometric equasion to the International one. Which one suits our needs more?
    # Hypsometric Equation (Temp compensated) (Max Altitude < 11 Km above sea level)
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25 # hPa
    #TODO IMPORTANT: implement a way to input the actual pressure at sea level, according to flight weather!
    pressure_ratio = sea_level_pressure/local_pressure  # sea level pressure = 1013.25 hPa
    alt = (((pressure_ratio**(1/5.257)) - 1) * temperature ) / 0.0065
    return alt

def flash():
    led.toggle()
    time.sleep(0.05)
    led.toggle()

def tempc():  # temperature accquire celsius, returns [°C]
    temp_c = bmp280_obj.temperature  # TODO can I return this expression? "return bmp280_obj.temperature"
    return temp_c
    
def tempk():  # temperature accquire kelvin, returns [K]
    temp_k = bmp280_obj.temperature + 273.15
    return temp_k

def pressure():
    pressure = ( bmp280_obj.pressure * 0.01 ) + ERROR  # hPa
    return pressure

def altitude():
    altitude = calc_alt_HYP(pressure(), tempk()) + alt_ERROR
    return altitude

header()

# MAIN LOOP FOR IN_FLIGHT RUN --------------------------------------------

while True:
    # write to CSV
    data = [altitude(), pressure(), tempc()]
    w2csv(data)
    flash()  # already pauses for 0.05s (50ms)
    # only enable following lines for debug --------
    # print(str(time.time()) + str(data))
    # print(writemode)
    # ----------------------------------------------

# MAIN LOOP FOR IN_FLIGHT RUN --------------------------------------------
