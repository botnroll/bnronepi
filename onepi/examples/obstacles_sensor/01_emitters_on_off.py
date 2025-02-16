"""
 Latest update: 04-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
Infra-Red obstacle detection LEDs (IRE1 and IRE2) are switched ON and OFF
every second in this example code.
For Race of Champions start, IR LEDs must be OFF.
Messages are printed on the LCD and terminal accordingly.
WARNING!!!
Infra-Red light can damage your eyes if you look to emitting IR LED's.
You will not be able to see the LED's emitting light because human eyes
cannot see infra-red light.
You can see the IR LED's light using a camera (from you cell phone or
smart-phone, for example).
Placing an obstacle 2cm in front of the LEDS should switch IRS1 and IRS2 ON.
"""

import time
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)


def setup():
    one.stop()  # stop motors


def loop():
    on = 1
    off = 0
    one.obstacle_emitters(on)  # activate IR emitter LEDs
    print("IR Emitters ON ")  # print data on terminal
    one.lcd2(" IR Emitters ON ")  # print text on LCD line 2
    time.sleep(1)  # wait 1 second
    one.obstacle_emitters(off)  # deactivate IR emitter LEDs
    print("IR Emitters OFF")  # print data on serial monitor.
    one.lcd2(" IR Emitters OFF ")  # print text on LCD line 2
    time.sleep(1)  # wait 1 second


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
