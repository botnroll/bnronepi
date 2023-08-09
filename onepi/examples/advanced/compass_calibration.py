"""
 This code example is in the public domain. 
 http://www.botnroll.com

 Description: 
 Performs compass calibration according to manufacturer's instructions.
 Connect the compas to a slot i2c. Make sure the compass is tighly attached to the robot.
 Place the robot on a flat surface free of obstacles so that it can rotate on spot without collisions.

 Compass calibration
"""

import time
from smbus import (
    SMBus,
)  # for I2C communication (https://www.abelectronics.co.uk/kb/article/1094/i2c-part-4---programming-i-c-with-python)

from one import BnrOneA

one = BnrOneA(0, 0)  # declaration of object variable to control the Bot'n Roll ONE A

# constants definition
min_speed = 30  # if motors have been calibrated change this to 1
compass_address = 0x60  # Define address of CMPS11


def read_bearing():
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2cbus.write_byte(compass_address, 0x1)  # request bearing data
    bearing = i2cbus.read_word_data(compass_address, 2)
    return bearing


def read_pitch():
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2cbus.write_byte(compass_address, 0x4)  # request pitch data
    pitch = i2cbus.read_byte(compass_address)
    return pitch


def read_roll():
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2cbus.write_byte(compass_address, 0x5)  # request roll data
    roll = i2cbus.read_byte(compass_address)
    return roll


def setup():
    one.stop()
    # stop motors
    time.sleep(0.5)


def calibrateCMPS11():
    one.move(-min_speed, min_speed)  # Slowly rotate the compass on the horizontal plane in all directions
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2cbus.write_byte(compass_address, 0)  # Send the register we wish to start reading from
    i2cbus.write_byte(compass_address, 0xF0)  # Calibration sequence byte 1
    time.sleep(0.03)

    i2cbus.write_byte(compass_address, 0)  # Send the register we wish to start reading from
    i2cbus.write_byte(compass_address, 0xF5)  # Calibration sequence byte 2
    time.sleep(0.03)

    i2cbus.write_byte(compass_address, 0)  # Send the register we wish to start reading from
    i2cbus.write_byte(compass_address, 0xF7)  # Calibration sequence byte 3
    time.sleep(0.03)

    one.move(-min_speed, min_speed)
    # Slowly rotate the compass on the horizontal plane in all directions
    time.sleep(15)

    i2cbus.write_byte(compass_address, 0)  # Send the register we wish to start reading from
    i2cbus.write_byte(compass_address, 0xF8)  # Exit calibration mode
    time.sleep(0.03)

    one.move(0, 0)
    # Stop rotation


def compassRead():
    bearing = read_bearing()
    roll = read_roll()
    pitch = read_pitch()

    print("Bearing:", bearing)
    print("   roll:", int(roll))
    print("   pitch:", int(pitch))

    one.lcd1("Bearing: ", bearing)
    text = "Rol:" + str(int(roll)) + "Pit:" + str(int(pitch))
    one.lcd2(text)


def loop():
    one.lcd1("   Press PB1   ")
    one.lcd2(" to calibrate  ")
    while one.read_button() != 1:
        time.sleep(0.05)

    one.lcd1("  Calibrating")
    one.lcd2("   Compass... ")
    time.sleep(0.1)
    calibrateCMPS11()

    one.lcd1("  Calibration")
    one.lcd2("    Finnished")
    time.sleep(0.1)

    while one.read_button() != 1:
        compassRead()
        time.sleep(0.1)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
