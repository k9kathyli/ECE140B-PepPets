#!/usr/bin/env python
import time
import serial

# Source: https://pimylifeup.com/raspberry-pi-serial/

ser = serial.Serial(
        port='/dev/ttyAM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter=0

def write_message(message):
    while True:
            ser.write(message)
            time.sleep(1)