#!/usr/bin/env python
import time
import serial

ser = serial.Serial(port='/dev/serial0', baudrate = 9600, timeout = 1)

def write():
    ser.write(b"hello")

while True:
    write()
    ser.flush()
    time.sleep(1)