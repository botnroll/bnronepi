"""
 Latest update: 12-04-2024

 This code example is in the public domain.
 http://www.botnroll.com

IMPORTANT!!!!
Before you use this example you MUST calibrate the motors
"""

import json
import math
import os
import time
from collections import namedtuple
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

max_linear_speed = 600  # (mm/s)
speed_conversion_factor = 1  # conversion factor from real speeds to percentage
file_name = "config_speed_factor.json"
filename = os.path.join(os.path.dirname(__file__), file_name)
MAX_SPEED = 50.0
TICKS_PER_REV = 1500  # encoder ticks per revolution
WHEEL_DIAMETER_MM = 63  # mm


def load_config():
    """
    Read config values from file.
    """

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            # Access values from JSON file
            speed_conversion_factor = data["speed_conversion_factor":]
            return speed_conversion_factor

    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        print(f"The file '{filename}' doesn't exist. Using default values.")
    return 1


def save_config(speed_conversion_factor_in):
    """
    Save config values to file.
    """
    data = {
        "speed_conversion_factor": speed_conversion_factor_in,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def determine_speed(speed_in, wheel_diameter, ticks_per_rev, motion_duration_s=1):
    one.stop()
    one.move(10, 10)
    time.sleep(0.1)
    one.move(speed_in, speed_in)
    time.sleep(0.5)  # allow enough time for wheels to reach max speed
    one.read_left_encoder()  # reset encoder
    one.read_right_encoder()  # reset encoder
    time.sleep(motion_duration_s)
    left_count = one.read_left_encoder()
    right_count = one.read_right_encoder()
    one.stop()
    average_count = (left_count + right_count) / 2.0
    print("average_count: ", average_count)
    revolutions = average_count / ticks_per_rev
    wheel_perimeter = wheel_diameter * math.pi
    distance = wheel_perimeter * revolutions
    speed_mmps = distance / motion_duration_s  #
    one.lcd1("distance ", distance)
    one.lcd2("speed: ", speed_mmps)
    print("distance: ", distance)
    print("speed: ", speed_mmps)
    time.sleep(2)
    return speed_mmps


def calibrate_speed_factor():
    global speed_conversion_factor, max_speed_mmps
    global MAX_SPEED, WHEEL_DIAMETER_MM, TICKS_PER_REV
    max_speed_mmps = determine_speed(MAX_SPEED, WHEEL_DIAMETER_MM, TICKS_PER_REV)
    speed_conversion_factor = max_speed_mmps / MAX_SPEED
    save_config(speed_conversion_factor)


def convert_to_percentage(real_speed):
    global speed_conversion_factor
    return real_speed * speed_conversion_factor


def within_tolerance(value_in, value_ref, tolerance):
    if (value_ref - tolerance) <= value_in <= (value_ref + tolerance):
        return True
    return False


def verify_calibration():
    global speed_conversion_factor, max_speed_mmps
    global MAX_SPEED, WHEEL_DIAMETER_MM, TICKS_PER_REV

    tolerance = 2  # tolerance percentage
    half_max_speed_mmps = max_speed_mmps / 2.0
    # verify linearity of the speed conversion
    speed_mmps = determine_speed(MAX_SPEED / 2.0, WHEEL_DIAMETER_MM, TICKS_PER_REV)
    print("half_max_speed_mmps: ", speed_mmps)
    real_speed_tolerance = (tolerance * max_speed_mmps) / 100.0
    error = speed_mmps - half_max_speed_mmps
    print("error: ", error)
    one.lcd2("error = ", error)
    if within_tolerance(speed_mmps, half_max_speed_mmps, real_speed_tolerance):
        one.lcd1("Calibration OK")
    else:
        one.lcd1("Calibration Failed")


def wait_user_input():
    while one.read_button() == 0:  # Wait a button to be pressed
        pass
    while one.read_button() != 0:  # Wait for button release
        pass


def setup():
    one.min_battery(10.5)  # safety voltage for discharging the battery
    one.stop()  # stop motors
    one.lcd1("Speed calibration")
    one.lcd2(" Press a button ")
    wait_user_input()
    calibrate_speed_factor()
    wait_user_input()
    verify_calibration()


def loop():
    one.stop()
    time.sleep(1)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
