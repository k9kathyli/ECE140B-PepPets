#!/usr/bin/env python
import time
import serial

ser = serial.Serial(port='/dev/serial1', baudrate = 9600, timeout = 1)

def write():
    ser.write(b"Kathy")

while True:
    write()
    ser.flush()
    time.sleep(1)