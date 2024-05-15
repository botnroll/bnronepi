"""
 Latest update: 12-04-2023

 This code example is in the public domain.
 http://www.botnroll.com

IMPORTANT!!!!
Before you use this example you MUST calibrate the line sensor. Use example _04_1_Calibrate.ino first!!!
Line reading provides a linear value between -100 to 100
"""

import json
import math
import os
import time
from collections import namedtuple
from onepi.one import BnrOneA
from onepi.utils.move_pid import MovePid

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

MAX_SPEED_MMPS = 800
max_linear_speed = 100  # (mm/s) it will be overriten by config value
speed_conversion_factor = 17.2  # conversion factor from percentage to real speeds
config_pure_pursuit = "config_pure_pursuit.json"
config_speed_factor = "config_speed_factor.json"
filename = os.path.join(os.path.dirname(__file__), config_pure_pursuit)
line_sensor_pos_x = 36  # 50  #65 #36  # (mm) distance from the wheel axis
line_sensor_width = 75  # (mm)
Point = namedtuple("Point", ["x", "y"])
target = Point(line_sensor_pos_x, 0)
axis_width = 165  # (mm)
y_tolerance = 0  # (mm) tolerance to move at full speed

one_pid = MovePid()


def pure_pursuit(axis_width_in, v_max, local_target, y_tolerance_in):
    v_left = v_max
    v_right = v_max
    l = axis_width_in
    if abs(local_target.y) <= y_tolerance_in:
        return (v_left, v_right)
    else:
        x = local_target.x
        y = local_target.y
        d = ((x * x) - (y * y)) / (2 * y)
        r = y + d
        ratio = ((2 * r) - l) / ((2 * r) + l)

        if abs(ratio) > 1.0:
            ratio = 1 / ratio
        if y > 0:
            v_right = v_max
            v_left = ratio * v_max
        else:
            v_left = v_max
            v_right = ratio * v_max
    return (v_left, v_right)


def load_config():
    """
    Read config values from file.
    """
    global config_pure_pursuit, config_speed_factor
    global max_linear_speed, line_sensor_pos_x, speed_conversion_factor

    try:
        with open(config_pure_pursuit, "r") as file:
            data = json.load(file)
            # Access values from JSON file
            max_linear_speed = data["max_linear_speed"]
            line_sensor_pos_x = data["line_sensor_pos_x"]

    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        print(f"The file '{config_pure_pursuit}' doesn't exist. Using default values.")

    try:
        with open(config_speed_factor, "r") as file:
            data = json.load(file)
            # Access values from JSON file
            speed_conversion_factor = data["speed_conversion_factor"]
            return 0

    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        print(f"The file '{config_speed_factor}' doesn't exist. Using default values.")
    return 1


def save_config():
    """
    Save config values to file.
    """
    global max_linear_speed, line_sensor_pos_x, config_pure_pursuit
    filename = config_pure_pursuit
    data = {
        "max_linear_speed": max_linear_speed,
        "line_sensor_pos_x": line_sensor_pos_x,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def convert_to_percentage(real_speed):
    global speed_conversion_factor
    return real_speed / speed_conversion_factor


def wait_user_input():
    button = 0
    while button == 0:  # Wait a button to be pressed
        button = one.read_button()
    while one.read_button() != 0:  # Wait for button release
        pass
    return button


def menu():
    global max_linear_speed
    one.stop()
    option = 0
    while option != 3:
        if option == 1:
            max_linear_speed += 5
            if max_linear_speed > MAX_SPEED_MMPS:
                max_linear_speed = MAX_SPEED_MMPS
        elif option == 2:
            max_linear_speed -= 5
            if max_linear_speed < 0:
                max_linear_speed = 0
        one.lcd1("max speed: ", max_linear_speed)
        one.lcd2("1:INC 2:DEC 3:OK")
        option = wait_user_input()

    one.lcd2("      DONE      ")
    save_config()
    time.sleep(1)


def setup():
    one.min_battery(10.5)  # safety voltage for discharging the battery
    one.stop()  # stop motors
    load_config()
    while True:
        one.lcd1("  Pure pursuit  ")
        one.lcd2("1-Menu  3-Start ")
        option = wait_user_input()
        if option == 1:
            menu()
        if option == 3:
            break
    one.lcd2("                ")


def loop():
    """
    While using one_pid do not use any other commands to the robot, e.g. sending
    text to lcd or reading sensor values. It causes move_pid to not work correctly
    as it uses a timer to send regular speed commands to the wheels
    """
    global max_linear_speed, target, line_sensor_width, axis_width, y_tolerance, one_pid
    line = 0
    while True:
        y_value = (-line * (line_sensor_width / 2.0)) / 100.0
        target = target._replace(y=y_value)
        (v_left, v_right) = pure_pursuit(axis_width, max_linear_speed, target, y_tolerance)
        line = one_pid.move(v_left, v_right, get_line=True)
        print("line: ", int(line), " speeds: ", int(v_left), ", ", int(v_right), "target: ", int(target.x), ", ", int(target.y))

def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
