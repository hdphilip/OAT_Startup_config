#!/usr/bin/env python3


import smbus
import math
import time


# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
REG_CONFIG   = 0x1A #  5Hz bandwidth (lowest) for smoothing
REG_ACCEL_XOUT_H = 0x3B
REG_TEMP_OUT_H   = 0x41
REG_PWR_MGMT_1   = 0x6B
REG_WHO_AM_I     = 0x75
 
def read_byte(adr):
    return bus.read_byte_data(address, adr)
 
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val
 
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
 
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68 # This is the address value read via the i2cdetect command
bus.write_byte_data(address, REG_PWR_MGMT_1 , 0)  # Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, REG_CONFIG , 6)      # Reduce BW to 5HZ 
 

accel_xout = read_word_2c(0x3b)
accel_yout = read_word_2c(0x3d)
accel_zout = read_word_2c(0x3f)

accel_xout_scaled = accel_xout / 4096   # 16384.0 8192
accel_yout_scaled = accel_yout / 4096
accel_zout_scaled = accel_zout / 4096

Xang = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
Yang = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

Xang = Xang - .2  # RA calibration error
Yang = Yang + 2.3  # RA calibration error

Xa = "%.1f" %Xang
Ya = "%.1f" %Yang
   

print (Xa,Ya)
  




