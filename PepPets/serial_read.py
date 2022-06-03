import time
import serial

ser = serial.Serial(port='/dev/serial0', baudrate = 9600, timeout=1)

while 1:
    x=ser.readline()
    print(x)