"""
 Latest update: 04-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Line Following:
15 possible values for line position:
-100 -87 -75 -62 -50 -37 -25 0 +25 +37 +50 +62 +75 +87 +100
The speed of the motors is adjusted using a linear approach and gain (k)
"""

import time
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object to control the Bot'n Roll ONE A

M1 = 1  # Motor1
M2 = 2  # Motor2

THRESHOLD = 300  # THRESHOLD value to distinguish between black and white

V25 = 10  # Speed for line value 25
V37 = 15
V50 = 20
V62 = 25
V75 = 30
V87 = 30
V100 = 35

VEL = 40


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
    one.min_battery(10.5)  # Battery protection (lower voltage)
    time.sleep(1)


def loop():
    line = read_line()
    print("Line", line, end="     \r")
    k = 0.45  # Linear gain to control motor speed

    vel_M1 = VEL + (line * k)
    vel_M2 = VEL - (line * k)

    one.move(vel_M1, vel_M2)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
