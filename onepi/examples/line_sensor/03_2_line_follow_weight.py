"""
 Latest update: 04-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Line Following:
15 possible values for line position:-100 -87 -75 -62 -50 -37 -25 0 +25 +37 +50 +62 +75 +87 +100
The speed of the motors is set differently for each case.
"""

import time
import signal
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

M1 = 1  # Motor1
M2 = 2  # Motor2

THRESHOLD = 300  # THRESHOLD value to distinguish between black and white

V25 = 3  # Speed for line value 25
V37 = 6
V50 = 9
V62 = 12
V75 = 20
V87 = 22
V100 = 25

VEL = 20


def read_line():
    line_value = 0
    sensor_count = 0
    if one.read_adc(0) > THRESHOLD:  # Test Sensor1
        line_value -= 100
        sensor_count += 1
    if one.read_adc(1) > THRESHOLD:  # Test Sensor2
        line_value -= 75
        sensor_count += 1
    if one.read_adc(2) > THRESHOLD:
        line_value -= 50
        sensor_count += 1
    if one.read_adc(3) > THRESHOLD:
        line_value -= 25
        sensor_count += 1
    if one.read_adc(4) > THRESHOLD:
        line_value += 25
        sensor_count += 1
    if one.read_adc(5) > THRESHOLD:
        line_value += 50
        sensor_count += 1
    if one.read_adc(6) > THRESHOLD:
        line_value += 75
        sensor_count += 1
    if one.read_adc(7) > THRESHOLD:  # Test Sensor8
        line_value += 100
        sensor_count += 1

    if sensor_count > 2:
        line_value = -1
    elif sensor_count > 0:
        line_value = line_value / sensor_count
    return line_value


def setup():
    one.stop()  # stop motors
    one.set_min_battery_V(10.5)  # Battery protection (lower voltage)
    time.sleep(1)


def loop():
    line = read_line()
    print("  Line:", line, end="     \r")

    if line == -100:
        one.move(VEL - V100, VEL + V100)
    elif line == -87:
        one.move(VEL - V87, VEL + V87)
    elif line == -75:
        one.move(VEL - V75, VEL + V75)
    elif line == -62:
        one.move(VEL - V62, VEL + V62)
    elif line == -50:
        one.move(VEL - V50, VEL + V50)
    elif line == -37:
        one.move(VEL - V37, VEL + V37)
    elif line == -25:
        one.move(VEL - V25, VEL + V25)
    elif line == 0:
        one.move(VEL, VEL)
    elif line == 25:
        one.move(VEL + V25, VEL - V25)
    elif line == 37:
        one.move(VEL + V37, VEL - V37)
    elif line == 50:
        one.move(VEL + V50, VEL - V50)
    elif line == 62:
        one.move(VEL + V62, VEL - V62)
    elif line == 75:
        one.move(VEL + V75, VEL - V75)
    elif line == 87:
        one.move(VEL + V87, VEL - V87)
    elif line == 100:
        one.move(VEL + V100, VEL - V100)


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
