"""
 Latest update: 04-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

IMPORTANT!!!!
Before you use this example you MUST calibrate the line sensor. Use example _04_1_Calibrate.ino first!!!

Line reading provides a linear value between -100 to 100
Line follow:
Motors speed varies according to a quadratic function.
Sinusoidal function gain must be adjusted.
You can adjust the speed limit of the wheel that is outside the curve.
Press push button 3 (PB3) to enter control configuration menu.
"""

import os
import math
import json
import time
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

max_linear_speed = 55
# function gain -> Lower Gain, higher output
gain = 40.0  #  function gain
speed_boost = 4  # Curve outside wheel max speed limit
file_name = "config_line_follow_cosine.json"
filename = os.path.join(os.path.dirname(__file__), file_name)


def load_config():
    """
    Read config values from file.
    max_linear_speed, speed_boost and gain
    """
    global max_linear_speed
    global speed_boost
    global gain
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            # Access values from JSON file
            max_linear_speed = data["max_linear_speed"]
            speed_boost = data["speed_boost"]
            gain = data["gain"]

    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        print(f"The file '{filename}' doesn't exist. Using default values.")


def save_config(new_max_linear_speed, new_speed_boost, new_gain):
    """
    Save config values to file.
    max_linear_speed, speed_boost and gain
    """
    data = {
        "max_linear_speed": new_max_linear_speed,
        "speed_boost": new_speed_boost,
        "gain": new_gain,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def cap_value(value, lower_limit, upper_limit):
    """
    Caps the value to lower and upper limits
    """
    if value < lower_limit:
        return lower_limit
    elif value > upper_limit:
        return upper_limit
    else:
        return value


def setup():
    one.min_battery(10.5)  # safety voltage for discharging the battery
    one.stop()  # stop motors
    load_config()  # read control values from file
    one.lcd1("Line Follow Wave")
    one.lcd2(" Press a button ")
    while one.read_button() == 0:  # Wait a button to be pressed
        pass
    while one.read_button() != 0:  # Wait for button release
        pass


def loop():
    vel_m1 = 0
    vel_m2 = 0
    line = one.read_line()
    if line <= 0:
        vel_m1 = max_linear_speed * math.cos(line / gain)  # function for motor 1
        vel_m2 = max_linear_speed + max_linear_speed - vel_m1
    else:
        vel_m2 = max_linear_speed * math.cos(line / gain)  # function for motor 2
        vel_m1 = max_linear_speed + max_linear_speed - vel_m2

    # Limit motors maximum and minimum speed
    vel_m1 = cap_value(vel_m1, -1, max_linear_speed + speed_boost)
    vel_m2 = cap_value(vel_m2, -1, max_linear_speed + speed_boost)

    print(
        " Line:",
        int(line),
        "   M1:",
        int(vel_m1),
        "   M2:",
        int(vel_m2),
        end="       \r",
    )
    one.move(vel_m1, vel_m2)

    # Configuration menu
    if one.read_button() == 3:
        menu()  # PB3 to enter menu


def set_max_speed(new_max_linear_speed):
    button = 0
    while button != 3:
        one.lcd2("   VelMax:", new_max_linear_speed)
        button = one.read_button()
        if button == 1:
            new_max_linear_speed += 1
            time.sleep(0.150)
        if button == 2:
            new_max_linear_speed -= 1
            time.sleep(0.150)
    while button == 3:  # Wait PB3 to be released
        button = one.read_button()
    return new_max_linear_speed


def set_speed_boost(new_speed_boost):
    button = 0
    while button != 3:
        one.lcd2("  Curve Boost:", new_speed_boost)
        button = one.read_button()
        if button == 1:
            new_speed_boost += 1
            time.sleep(0.150)
        if button == 2:
            new_speed_boost -= 1
            time.sleep(0.150)
    while button == 3:  # Wait PB3 to be released
        button = one.read_button()
    return new_speed_boost


def set_linear_gain(new_gain):
    new_gain = int(new_gain * 1000.0)
    button = 0
    while button != 3:
        one.lcd2(" Line Gain:", new_gain)
        button = one.read_button()
        if button == 1:
            new_gain += 10
            time.sleep(0.150)
        if button == 2:
            new_gain -= 10
            time.sleep(0.150)
    while button == 3:  # Wait PB3 to be released
        button = one.read_button()
    return new_gain / 1000.0


def menu():
    global max_linear_speed
    global speed_boost
    global gain

    one.stop()
    one.lcd1("  Menu Config:")
    one.lcd2("PB1+ PB2- PB3ok")
    time.sleep(0.250)
    while one.read_button() == 3:  # Wait PB3 to be released
        time.sleep(0.150)

    max_linear_speed = set_max_speed(max_linear_speed)  # Maximum speed
    speed_boost = set_speed_boost(speed_boost)  # Outside wheel speed boost
    gain = set_linear_gain(gain)  # Linear gain KLine
    save_config(
        max_linear_speed, speed_boost, gain
    )  # Save values to configuration file

    one.lcd1("Line  Following!")
    one.lcd2("www.botnroll.com")
    time.sleep(0.250)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
