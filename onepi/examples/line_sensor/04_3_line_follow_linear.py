"""
 This code example is in the public domain.
 http://www.botnroll.com

IMPORTANT!!!!
Before you use this example you MUST calibrate the line sensor.
Use example 04_1_line_calibration first!!!

Line reading provides a linear value between -100 to 100
Line follow:
Motors speed varies according to a linear function.
Linear Gain must be adjusted.
You can adjust the speed limit of the wheel that is outside the curve.
Press push button 3 (PB3) to enter control configuration menu.
"""

import json
import time
from one import BnrOneA

one = BnrOneA(0, 0)  # declaration of object variable to control the Bot'n Roll ONE A

max_linear_speed = 60
gain = 1.10  # Linear gain
speed_boost = 8    # Curve outside wheel max speed limit
filename = "config_line_follow.json"

def set_max_speed():
    temp_vel = max_linear_speed
    while button != 3:
        one.lcd2("   VelMax:", temp_vel)
        button = one.read_button()
        if button == 1:
            temp_vel += 1
            time.sleep(0.150)
        if button == 2:
            temp_vel -= 1
            time.sleep(0.150)
    while button == 3:  # Wait PB3 to be released
        button = one.read_button()
    max_linear_speed = temp_vel

def set_speed_boost():
    temp_boost = speed_boost
    while button != 3:
        one.lcd2("  Curve Boost:", temp_boost)
        button = one.read_button()
        if button == 1:
            temp_boost += 1
            time.sleep(0.150)
        if button == 2:
            temp_boost -= 1
            time.sleep(0.150)
    while button == 3:  # Wait PB3 to be released
        button = one.read_button()
    speed_boost = temp_boost


def set_linear_gain():
    temp_gain = int(gain * 1000.0)
    while button != 3:
        one.lcd2(" Line Gain:", temp_gain)
        button = one.read_button()
        if button == 1:
            temp_gain += 10
            time.sleep(0.150)
        if button == 2:
            temp_gain -= 10
            time.sleep(0.150)
    while button == 3:  # Wait PB3 to be released
        button = one.read_button()
    gain = temp_gain / 1000.0


def menu():
    button = 0
    temp = 0.0
    one.stop()
    one.lcd1("  Menu Config:")
    one.lcd2("PB1+ PB2- PB3ok")
    time.sleep(0.250)
    while one.read_button() == 3:  # Wait PB3 to be released
        time.sleep(0.150)

    set_max_speed()     # Maximum speed
    set_speed_boost()   # Outside wheel speed boost
    set_linear_gain()   # Linear gain KLine
    save_config()       # Save values to configuration file

    one.lcd1("Line  Following!")
    one.lcd2("www.botnroll.com")
    time.sleep(0.250)


def load_config():
    """
    Read config values from file.
    max_linear_speed, speed_boost and gain
    """
    with open(filename) as f:
        data = json.load(f)

    # Access values from JSON file
    max_linear_speed = data["max_linear_speed"]
    speed_boost = data["speed_boost"]
    gain = data["gain"]


def save_config():
    """
    Save config values to file.
    max_linear_speed, speed_boost and gain
    """
    data = {
        "max_linear_speed": max_linear_speed,
        "speed_boost": speed_boost,
        "gain": gain,
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
    one.min_battery(10.5)           # safety voltage for discharging the battery
    one.stop()                      # stop motors
    load_config()
    one.lcd1("Line Follow Lin.")
    one.lcd2(" Press a button ")
    while one.read_button() == 0:   # Wait a button to be pressed
        pass
    while one.read_button() != 0:   # Wait for button release
        pass


def loop():
    line = one.read_line()
    vel_m1 = max_linear_speed + line * gain     # Linear function for Motor1
    vel_m2 = max_linear_speed - line * gain     # Linear function for Motor2

    # Limit motors maximum and minimum speed
    vel_m1 = cap_value(vel_m1, -1, max_linear_speed + speed_boost)
    vel_m2 = cap_value(vel_m2, -1, max_linear_speed + speed_boost)

    one.move(vel_m1, vel_m2)

    # Configuration menu
    if one.read_button() == 3:
        menu()  # PB3 to enter menu


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
