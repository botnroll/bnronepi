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
    one.move_rpm(10, 0)  # Forward
    CYCLE_INTERVAL = 0.1
    
    for speed_rpm in range(350, 455, 1):
        time_alarm = time.time() + CYCLE_INTERVAL
        counter = 0
        while(True):
            if(time.time() >=  time_alarm):
                time_alarm +=  CYCLE_INTERVAL
                one.move_rpm(speed_rpm, 0)
                left_encoder = one.read_left_encoder();
                print("encoder: ", left_encoder, " rpm: ", speed_rpm);
                counter += 1
                if (counter >=5):
                    break    
        if (left_encoder >= (290 * 4)):
            break
        
    one.stop()
    print("Max rpm: ", speed_rpm)

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
