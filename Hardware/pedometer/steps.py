# Import SMBus I2C and sleep module
import smbus
import math
from time import sleep

# MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

bus = smbus.SMBus(1) 	# Or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address


def MPU_Init():
    # write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)


def read_raw_data(addr):
    # Accelero value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)

    # For range +-2g, divide 16384
    value = ((high << 8) | low) / 16384.0

    return value


MPU_Init()

while True:
    # Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    vector = math.sqrt(pow(acc_x, 2) + pow(acc_y, 2) + pow(acc_z, 2))

    # print(vector)
    print("Ax=%.2f" % acc_x, "\tAy=%.2f" % acc_y, "\tAz=%.2f" % acc_z)
    sleep(0.17)
