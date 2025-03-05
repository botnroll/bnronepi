"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 This program detects a button click and moves for the RoboParty Fun Challenge.

"""

import time
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

def setup():
    one.stop()  # stop motors
    one.lcd1(" FUN CHALLENGE")  # print on LCD line 1


def loop():
    one.lcd2(" Press a button!")  # print on LCD line 1
    while one.read_button() == 0:
        time.sleep(0.050)
    one.lcd2("    Moving!!!    ")  # print on LCD line 1
    one.move(80, 80)
    time.sleep(1.5)
    one.brake()
    time.sleep(0.1)
    one.move(-80, -80)
    time.sleep(2)
    one.brake()
    time.sleep(0.1)


def main():
    try:
        setup()
        while True:
            loop()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
