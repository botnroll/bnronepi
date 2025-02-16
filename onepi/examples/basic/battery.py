"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
Reads the battery voltage and prints its value on the LCD and Serial Monitor.
Also configures the minimum battery voltage that causes the robot to
stop if voltage is below the defined value.
It is VERY important that you define this minimum voltage correctly
to preserve your robot's battery life.
"""

import time
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+


def setup():
    one.stop()  # stop motors
    one.min_battery(
        10.5
    )  # define de minimum battery voltage. Robot stops if voltage is below the specified value!


def loop():
    battery = round(one.read_battery(), 2)  # read battery voltage
    one.lcd2("Battery V: ", battery)  # print data on LCD line 2
    print("Battery V: ", battery)
    time.sleep(0.2)  # wait 200 milliseconds


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
