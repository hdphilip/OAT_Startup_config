#!/usr/bin/env python3

import time
import os
import serial
import sys, importlib
from mpu6050 import Xa
from mpu6050 import Ya

target_DEC = 40
target_RA  = 0
DEC_steps_per_degree = 314.2
RA_steps_per_degree = 314.2


print("COM port set to /dev/ttyUSB0")
print("Disabling #DTR for /dev/ttyUSB0")
serialport = "/dev/ttyUSB0"
os.system('stty -F /dev/ttyUSB0 -hupcl')
print("Opening serial port on " + serialport + '...')
ser = serial.Serial(serialport, 19200, timeout = 1)
time.sleep(1)#wait for reboot

#//////////////////////////
# RA Alignment
#//////////////////////////

importlib.reload(sys.modules.get('mpu6050', sys))

Xa = float(Xa)  # convert int to float 

RA_steps = ((target_RA - Xa) * RA_steps_per_degree )
RA_error = target_RA - Xa
RA_error = "%.1f" %RA_error # Cleans up the display
RA_steps = "%.1f" %RA_steps # Cleans up the display

print ("\n Current RA angle Before Adjustment " +str(Xa) + " Degrees")
print ("\n Target RA angle - Current angle " + str(RA_error) + "   Degrees" )
print ("\n RA Steps per Degrees  " + str(RA_steps_per_degree))
print ("\n Steps to reach Goal " + str(RA_steps))

move_RA_stepper = (':MXr' + str(RA_steps) + '#') # configures the Measde command

ser.write(str.encode(move_RA_stepper))
response = ser.read(1)
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('\n RA successfully Homed!')
else: print('\n Could not Home RA...')
time.sleep(7)  # wait for Dec to complete it's move

#//////////////////////////
# Dec Alignment
#//////////////////////////

importlib.reload(sys.modules.get('mpu6050', sys))

Ya = float(Ya)  # convert int to float 

dec_steps = ((target_DEC - Ya) * DEC_steps_per_degree )
dec_error = target_DEC - Ya
dec_error = "%.1f" %dec_error # Cleans up the display
dec_steps = "%.1f" %dec_steps # Cleans up the display

print ("\n Current Dec angle Before Adjustment " +str(Ya) + " Degrees")
print ("\n Target Dec angle - Current angle " + str(dec_error) + "   Degrees" )
print ("\n DEC Steps per Degrees  " + str(DEC_steps_per_degree))
print ("\n Steps to reach Goal " + str(dec_steps))

move_dec_stepper = (':MXd' + str(dec_steps) + '#')

ser.write(str.encode(move_dec_stepper))
response = ser.read(1)
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('\n DEC successfully Homed!')
else: print('\n Could not Home DEC...')
time.sleep(15)  # wait for Dec to complete it's move

importlib.reload(sys.modules.get('mpu6050', sys))  # Display new RA and DEC values

#////////////////////////////////////
# Stop and exit
#///////////////////////////////////
print('\n Stoping all motors...')
ser.write(str.encode(':Q#'))

ser.close() 

print("/// OAT configuration is Completed ///")






