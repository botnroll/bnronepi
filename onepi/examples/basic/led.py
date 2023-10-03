"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
The LED is switched ON and OFF every second.
A message is sent to the Serial Monitor accordingly.
"""

import time
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

HIGH = 1
LOW = 0


def setup():
    one.stop()  # stop motors


def loop():
    one.led(HIGH)  # turn LED ON
    print("LED ON")  # print data on terminal
    time.sleep(1)  # wait 1 second
    one.led(LOW)  # turn LED OFF
    print("LED OFF")  # print data on terminal
    time.sleep(1)  # wait 1 second


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
