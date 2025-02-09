"""
 Latest update: 05-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

 Reads and displays values for bearing, roll and pitch from the CMPS11 device if connected to the robot.
 - bearing range [0-65535]
 - roll range [0-255]
 - pitch range [0-255]
"""


import time
from smbus import (
    SMBus,
)  # for I2C communication (https://www.abelectronics.co.uk/kb/article/1094/i2c-part-4---programming-i-c-with-python)

from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A+

COMPASS_ADDRESS = 0x60  # CMPS11 I2C address


def read_bearing():
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2cbus.write_byte(COMPASS_ADDRESS, 0x1)  # request bearing data
    bearing = i2cbus.read_word_data(COMPASS_ADDRESS, 2)
    return bearing


def read_pitch():
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2cbus.write_byte(COMPASS_ADDRESS, 0x4)  # request pitch data
    pitch = i2cbus.read_byte(COMPASS_ADDRESS)
    return pitch


def read_roll():
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2cbus.write_byte(COMPASS_ADDRESS, 0x5)  # request roll data
    roll = i2cbus.read_byte(COMPASS_ADDRESS)
    return roll


def setup():
    one.stop()  # stop motors
    time.sleep(0.5)


def loop():
    bearing = read_bearing()
    roll = read_roll()
    pitch = read_pitch()

    print("Bearing:", int(bearing))
    print("   roll:", int(roll))
    print("  pitch:", int(pitch))

    one.lcd1("Bearing: ", bearing)
    one.lcd2("Rol:", int(roll), "Pit:", int(pitch))

    time.sleep(0.050)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
