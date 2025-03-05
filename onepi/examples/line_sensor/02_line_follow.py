"""
 Latest update: 04-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

 Line Following:
 Test which sensor detects the line by comparing sensor values.
 The motors speed is set depending on which sensor is detecting the line.
"""

import time
import signal
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

M1 = 1  # Motor1
M2 = 2  # Motor2

THRESHOLD = 300  # THRESHOLD value to distinguish between black and white


def setup():
    one.stop()  # stop motors
    # Battery protection (lower voltage)
    bat_min = 10.5
    one.set_min_battery_V(bat_min)
    one.lcd1(" Bot'n Roll ONE")
    # Wait for a button to be pressed to move motors
    while one.read_button() == 0:
        one.lcd2("Press a button!")
        time.sleep(0.050)

    one.move(40, 40)
    one.lcd2("Line Following!")


def loop():
    # Read the 8 sensors
    sensor0 = one.read_adc(0)
    sensor1 = one.read_adc(1)
    sensor2 = one.read_adc(2)
    sensor3 = one.read_adc(3)
    sensor4 = one.read_adc(4)
    sensor5 = one.read_adc(5)
    sensor6 = one.read_adc(6)
    sensor7 = one.read_adc(7)

    # From left to centre
    if sensor0 > THRESHOLD:  # 10000000
        one.move(-7, 40)
    elif sensor1 > THRESHOLD:  # 01000000
        one.move(5, 40)
    elif sensor2 > THRESHOLD:  # 00100000
        one.move(20, 40)
    elif sensor3 > THRESHOLD:  # 00010000
        one.move(40, 40)
    # From right to centre
    elif sensor7 > THRESHOLD:  # 00000001
        one.move(40, -7)
    elif sensor6 > THRESHOLD:  # 00000010
        one.move(40, 5)
    elif sensor5 > THRESHOLD:  # 00000100
        one.move(40, 20)
    elif sensor4 > THRESHOLD:  # 00001000
        one.move(40, 40)
    else:
        one.stop()


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
