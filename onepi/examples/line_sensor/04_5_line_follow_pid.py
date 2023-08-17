"""
 This code example is in the public domain.
 http://www.botnroll.com
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)  # declaration of object variable to control the Bot'n Roll ONE A


def setup():
    one.stop()  # stop motors


def loop():


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()

