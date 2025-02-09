"""
 Latest update: 04-09-2023

 This code example is in the public domain.
 http://www.botnroll.com


Every sensor have a specific weigh:
  S1  S2  S3  S4  S5  S6  S7  S8
-100 -75 -50 -25 +25 +50 +75 +100
Verifies which sensors detect the line (black > THRESHOLD:) and the result is the average weigh of these sensors.
Note: Only 1 or 2 sensors are expected to detect the line at the same time.
The 15 possible results for the line position are:
-100 -87 -75 -62 -50 -37 -25 0 +25 +37 +50 +62 +75 +87 +100
"""

import time
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A+

M1 = 1  # Motor1
M2 = 2  # Motor2

THRESHOLD = 300  # THRESHOLD value to distinguish between black and white


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
    one.lcd1(" Bot'n Roll ONE")
    one.lcd2("  Line Reading")
    time.sleep(1)


def loop():
    line = read_line()  # Read line
    print("Line:", line, end="     \r")  # Print on terminal
    one.lcd2("  Line:", line)  # Print on LCD
    time.sleep(0.05)  # Remove delay to follow the line


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
