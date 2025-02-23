"""
 Latest update: 23-02-2025

 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 Sets the motor moving with different wheel speeds 
 by giving commands in rpm
"""

import time
import signal
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

def setup():
    one.stop()  # stop motors
    one.lcd2("    Forward ")  # print data on LCD line 2
    one.move_rpm(10, 10)  # Forward
    # 310 pulses per 25 ms
    for i in range(200, 405, 5):
        for j in range(5):
            one.move_rpm(i, i)
            left_encoder = one.read_left_encoder();
            print("encoder: ", left_encoder, " rpm: ", i);
            if (left_encoder >= 295):
                break
            time.sleep(0.1)
    one.stop()
    print("Max rpm: ", i)

def loop():
    pass


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
