"""
 This code example is in the public domain. 
 http://www.botnroll.com

 Description:
 This program detects automatic start on the race challenge.

 Start Race Detection
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)


def automatic_start():
    active = one.read_ir_sensors()  # read actual IR sensors state
    result = False
    if not active:  # If not active
        tempo_A = time.time()  # read time
        while not active:  # while not active
            active = one.read_ir_sensors()  # read actual IR sensors state
            elapsed_time = time.time() - tempo_A
            if elapsed_time > 0.050:  # if not active for more than 50ms
                result = True  # start Race
                break
    return result


def setup():
    off = 0
    one.stop()  # stop motors
    one.lcd1("IR testing")  # print on LCD line 1
    one.lcd2("STOP")  # print on LCD line 2
    one.obstacle_emitters(off)  # deactivate obstacles IR emitters
    time.sleep(4)  # time to stabilize IR sensors (DO NOT REMOVE!!!)
    start = False
    while not start:
        start = automatic_start()
    one.move(50, 50)  # the robot moves forward
    one.lcd2("GO")  # remove when racing for best performance!


def loop():
    pass


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
