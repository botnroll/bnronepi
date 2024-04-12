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
from collections import namedtuple
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

max_linear_speed = 60  # (mm/s)
speed_conversion_factor = 1  # conversion factor from real speeds to percentage
file_name = "config_pure_pursuit.json"
filename = os.path.join(os.path.dirname(__file__), file_name)
line_sensor_pos_x = 30  # (mm) distance from the wheel axis
line_sensor_width = 50  # (mm)
Point = namedtuple("Point", ["x", "y"])
target = Point(line_sensor_pos_x, 0)
axis_width = 200  # (mm)
y_tolerance = 5  # (mm) tolerance to move at full speed
MAX_SPEED = 100.0


def pure_pursuit(axis_width_in, v_max, local_target, y_tolerance_in):
    v_left = v_max
    v_right = v_max
    if abs(local_target.y) < y_tolerance_in:
        return (v_left, v_right)
    else:
        distance = math.dist({0, 0}, {local_target.x, local_target.y})
        rho = (distance * distance) / (2.0 * (local_target.y))
        calc1 = rho - (axis_width_in / 2.0)
        calc2 = rho + (axis_width_in / 2.0)
        if rho > 0:
            v_left = calc1 / calc2 * v_max
            v_right = v_max
        else:
            v_left = v_max
            v_right = calc2 / calc1 * v_max
    if local_target.x < 0:
        temp = -v_left
        v_left = -v_right
        v_right = temp

    return (v_left, v_right)


def load_config():
    """
    Read config values from file.
    """

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            # Access values from JSON file
            max_linear_speed = data["max_linear_speed"]
            line_sensor_pos_x = data["line_sensor_pos_x"]
            speed_conversion_factor = data["speed_conversion_factor":]
            return (max_linear_speed, line_sensor_pos_x, speed_conversion_factor)

    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        print(f"The file '{filename}' doesn't exist. Using default values.")
    return (0, 0, 0)


def save_config(
    new_max_linear_speed_in, line_sensor_pos_x_in, speed_conversion_factor_in
):
    """
    Save config values to file.
    """
    data = {
        "max_linear_speed": new_max_linear_speed_in,
        "line_sensor_pos_x": line_sensor_pos_x_in,
        "speed_conversion_factor": speed_conversion_factor_in,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def setup():
    global max_linear_speed, line_sensor_pos_x, speed_conversion_factor
    one.min_battery(10.5)  # safety voltage for discharging the battery
    one.stop()  # stop motors
    (max_linear_speed, line_sensor_pos_x, speed_conversion_factor) = load_config()
    one.lcd1("Line Follow PID.")
    one.lcd2(" Press a button ")
    while one.read_button() == 0:  # Wait a button to be pressed
        pass
    while one.read_button() != 0:  # Wait for button release
        pass


def convert_to_percentage(real_speed):
    global speed_conversion_factor
    return real_speed * speed_conversion_factor


def loop():
    global target, line_sensor_width, axis_width, y_tolerance
    line = one.read_line()
    target.y = line * line_sensor_width
    (v_left, v_right) = pure_pursuit(axis_width, max_linear_speed, target, y_tolerance)
    left_cmd = convert_to_percentage(v_left)
    right_cmd = convert_to_percentage(v_right)
    one.move(left_cmd, right_cmd)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
