"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 This program detects automatic start on the race challenge.

 Start Race Detection
"""

import time
import signal
from onepi.one import BnrOneA

one = BnrOneA(0, 0)


def automatic_start():
    active = one.read_ir_sensors()  # read actual IR sensors state
    result = False
    if not active:  # If not active
        start_time = time.time()  # read time
        while not active:  # while not active
            active = one.read_ir_sensors()  # read actual IR sensors state
            elapsed_time = time.time() - start_time
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
    print("Race started!")


def loop():
    pass


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
