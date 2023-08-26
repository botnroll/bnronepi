"""
 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 An external IR 40khz source can be detected by the IR sensors.
 Another Bot´n Roll ONE A emitting IR will be detected.
 This function can be used to remote control the robot with IR.
 This function is used in the race challenge to detect the start of the race!

 IR sensors
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def setup():
    on = 1
    one.stop()  # stop motors
    one.obstacle_emitters(on)  # activate IR emitter LEDs


def loop():
    ir_sensors = one.read_ir_sensors()  # read actual IR sensors state
    print("IR Sensors ", ir_sensors, " " * 10, end="\r")  # print data on terminal.
    one.lcd2("IR Sensors:", ir_sensors)  # print text on LCD line 2


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
