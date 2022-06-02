import serial
serial = serial.Serial('/dev/ttyS0', 9600)

serial.write(b'get data')
sentData = serial.readLine()

print(sentData)