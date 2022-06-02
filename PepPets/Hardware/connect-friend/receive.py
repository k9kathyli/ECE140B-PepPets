import serial
serial = serial.Serial('/dev/ttyS0', 9600)

receivedData = serial.readLine()
print(receivedData)