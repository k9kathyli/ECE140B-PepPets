#!/usr/bin/env python
import time
import serial

# Source: https://pimylifeup.com/raspberry-pi-serial/

ser = serial.Serial(
        port='/dev/ttyAM0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

while 1:
        x=ser.readline()
        print(x)