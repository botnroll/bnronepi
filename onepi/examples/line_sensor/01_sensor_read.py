"""
 This code example is in the public domain.
 http://www.botnroll.com
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

M1 = 1  # Motor1
M2 = 2  # Motor2


def setup():
    one.stop()  # stop motors
    one.lcd1(" Bot'n Roll ONE")
    one.lcd2(" Sensor Reading")
    time.sleep(1)


def loop():
    # Read values from the 8 sensors
    sensor0 = one.read_adc(0)
    sensor1 = one.read_adc(1)
    sensor2 = one.read_adc(2)
    sensor3 = one.read_adc(3)
    sensor4 = one.read_adc(4)
    sensor5 = one.read_adc(5)
    sensor6 = one.read_adc(6)
    sensor7 = one.read_adc(7)

    # Print values on the LCD
    one.lcd1(sensor0, sensor1, sensor2, sensor3)
    one.lcd2(sensor4, sensor5, sensor6, sensor7)

    # print values in the terminal
    print(sensor0, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7)

    # This delay must be removed when the robot follows the line
    time.sleep(0.1)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
