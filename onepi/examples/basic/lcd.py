"""
 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 Print a message on the robot LCD.
"""


import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def setup():
    one.stop()  # stop motors


def loop():
    one.lcd1(" LCD Test OK !! ")  # print data on LCD line 1
    one.lcd2("www.botnroll.com")  # print data on LCD line 2
    print("Message sent to LCD!")  # print data on terminal.
    time.sleep(1)  # wait 1 second


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
