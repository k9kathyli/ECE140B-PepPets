#!/usr/bin/env python
import time
import serial
from threading import Thread

ser = serial.Serial(port='/dev/serial0', baudrate = 9600, timeout = 1)

def write():
    try:
        while True:
            ser.write(b"Kathy")
            ser.flush()
            print("sending")
            time.sleep(1)
    except KeyboardInterrupt:
        ser.close()

def read():
    while 1:
        x=ser.readline()
        print(x)

writeMsg = Thread(target=write)
readMsg = Thread(target=read)

writeMsg.start()
readMsg.start()