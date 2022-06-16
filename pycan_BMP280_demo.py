# --------------------------------------------
# PyCan V.: 0.0.4 Build 16
# Copyright (C) 2022 celeste-42bit
# https://github.com/celeste-42bit/pycan
# firmware : rp2-pico-20210202-v1.14.uf2
# --------------------------------------------

from bmp280 import *
from machine import Pin, I2C
import utime

# Calibration error
ERROR = -3 # hPa 

# I2C pin decl
scl = Pin(1)
sda = Pin(0)

# init I2C
i2c_obj = I2C(0,              # I2C id
                 scl = scl,
                 sda = sda,
                 freq = 1000000)


# scan 4 devices
scan = I2C.scan(i2c_obj)
print("I2C scan result : ", scan) # 118 in decimal is same as 0x76 in hexadecimal
if scan != []:
    print("I2C connection successfull")
else:
    print("No devices found !")


# objectify sensor
bmp280_obj = BMP280(i2c_obj,
                       addr = 0x76, # change it 
                       use_case = BMP280_CASE_DROP)

# sensor config ---------------------------------

bmp280_obj.power_mode = BMP280_POWER_NORMAL

bmp280_obj.oversample = BMP280_OS_HIGH

bmp280_obj.temp_os = BMP280_TEMP_OS_8

bmp280_obj.press_os = BMP280_TEMP_OS_4


bmp280_obj.standby = BMP280_STANDBY_250

bmp280_obj.iir = BMP280_IIR_FILTER_2

# -----------------------------------------------

print("BMP Object created successfully !")
utime.sleep(2) # change it as per requirement
print("\n")


# claculate altitude

def altitude_HYP(hPa , temperature):
    # Hypsometric Equation (Temp compensated) (Max Altitude < 11 Km above sea level)
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25 # hPa      
    pressure_ratio = sea_level_pressure/local_pressure # sea level pressure = 1013.25 hPa
    alt = (((pressure_ratio**(1/5.257)) - 1) * temperature ) / 0.0065
    return alt


# altitude from international barometric formula, given in BMP 280 datasheet
def altitude_IBF(pressure):
    local_pressure = pressure    # Unit : hPa
    sea_level_pressure = 1013.25 # Unit : hPa
    
    pressure_ratio = local_pressure / sea_level_pressure
    
    alt = 44330*(1-(pressure_ratio**(1/5.255)))
    return alt
    

while True:
    # accquire temp
    temperature_c = bmp280_obj.temperature # degree celcius
    
    # c to k
    temperature_k = temperature_c + 273.15
    
    # accquire pressure
    pressure = bmp280_obj.pressure  # pascal
    
    # Pa to hPa
    pressure_hPa = ( pressure * 0.01 ) + ERROR # hPa
    
    # accquire alt values from HYP formula (preferred)
    h = altitude_HYP(pressure_hPa, temperature_k)
    
    # accquire alt values from IBF
    altitude = altitude_IBF(pressure_hPa)
    
    print("-----------------------------------------------------------------")
    print("Temperature : ",temperature_c," Degree Celcius")
    print("Pressure : ",pressure," Pascal (Pa)")
    print("Pressure : ",pressure_hPa," hectopascal (hPa) or millibar (mb)")
    print("Altitude (HMF) : ", h ," meter")
    print("Altitude (IBF) : ", altitude ," meter")
    print("-----------------------------------------------------------------")
    print(h)
    print(h)
    
    # bmp280_object.print_calibration()
    # bmp280_object.load_test_calibration()
    print("\n")
    utime.sleep(0.3)

