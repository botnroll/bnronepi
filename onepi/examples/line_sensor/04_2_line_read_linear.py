"""
Latest update: 04-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

IMPORTANT!!!!
Before you use this example you MUST calibrate the line sensor.
Use example 04_1_line_calibration first!!!

Line reading returns a value between -100 to 100 where:
  * 0 (zero) corresponds to the line being centred
  * -100 (negative 100) when the line is at the far left side
  * +100 (positive 100) when the line is at the far right side
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def setup():
    one.stop()  # stop motors
    one.min_battery(10.5)  # safety voltage for discharging the battery
    one.lcd1("== Line read == ")
    time.sleep(1)


def loop():
    line = int(one.read_line())  # read line value [-100, 100]
    print("Line: ", line, end="    \r")
    one.lcd2("   Line: ", line)
    time.sleep(0.050)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
