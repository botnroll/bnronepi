"""
 This code example is in the public domain.
 http://www.botnroll.com

IMPORTANT!!!!
Before you use this example you MUST calibrate the line sensor.
Use example 04_1_line_calibration first!!!

Line reading provides a linear value between -100 to 100
Line in the sensor varies from 0 to 9000
Reads the 8 sensors and stores the highest value sensor.
The nearest higher value sensor defines the line position between these
two sensors. Maximum and highest neighbour.
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def setup():
    one.stop()  # stop motors
    one.min_battery(10.5)  # safety voltage for discharging the battery


def loop():
    line = one.read_line()  # read line value [-100, 100]
    print("Line: ", line)
    one.lcd2("   Line: ", line)
    time.sleep(0.050)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
