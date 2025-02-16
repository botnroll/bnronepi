"""
 Latest update: 05-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
Read obstacle sensors range distance for left and right IR sensors.
Range varies from 0 to 25:
 -> 0 means no obstacle is detected
 -> 25 means obstacle is very close to the sensor
The robot has new readings every 25ms (40 readings per second)
Note: Valid for TSSP4056 IR sensors shipped with robots from 2023.
"""

import time
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+


def setup():
    on = 1
    one.stop()  # stop motors
    one.obstacle_emitters(on)  # activate IR emitters


def loop():
    left_range = one.read_left_range()  # read left obstacle sensor range
    right_range = one.read_right_range()  # read right obstacle sensor range
    one.lcd1("Range Left : ", left_range)
    one.lcd2("Range Right: ", right_range)
    print("L: ", left_range, "   R: ", right_range, end="      \r")
    time.sleep(0.025)  # The robot has new readings every 25ms (40 readings per second)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
