"""
 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 Helps finding the number of pulses per revolution of an encoder
"""

import time
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

SPEED = 200

def wait_any_button_push():
    while one.read_button() == 0:
        pass
    time.sleep(0.5)
    while one.read_button() != 0:
        pass
    time.sleep(0.5)

def setup():
    one.stop()  # stop motors
    one.lcd1 (" Push any button")
    one.lcd2 ("    to start    ")
    wait_any_button_push()
    one.lcd1 (" Push any button")
    one.lcd2 ("    to stop     ")
    one.move_rpm(SPEED, 0)
    left_encoder = 0
    one.read_left_encoder() # reset
    CYCLE_INTERVAL = 0.025
    time_alarm = time.time() + CYCLE_INTERVAL

    while(True):
        if(time.time() >=  time_alarm):
            time_alarm +=  CYCLE_INTERVAL
            if one.read_button() != 0:
                break
            left_encoder += one.read_left_encoder()

    one.brake(100, 100)
    one.lcd1 ("  Total pulses  ")
    one.lcd2 (left_encoder)

def loop():
    pass


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
