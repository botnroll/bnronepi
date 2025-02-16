"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
Read the Push Buttons state and print the result on the robot LCD and Terminal
Press PB1, PB2 or PB3 to interact with Bot'n Roll ONE A+
"""

import time
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+


def setup():
    one.stop()  # stop motors


def loop():
    pbutton = one.read_button()  # read the Push Button value
    one.lcd2(" Push Button: ", pbutton)  # print data on LCD line 2
    print(" Push Button: ", pbutton, end="   \r")  # print data on terminal.
    time.sleep(0.1)  # wait 100 milliseconds


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
