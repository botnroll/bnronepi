"""
 This code example is in the public domain.
 http://www.botnroll.com

IMPORTANT!!!!
Before you use this example you MUST calibrate the line sensor. Use example _04_1_Calibrate.ino first!!!
Line reading provides a linear value between -100 to 100

Line follow:
Motors speed varies using PID control.
Adjustable gains kp, ki and kd.
You can adjust the speed limit of the wheel that is outside the curve.
Press push button 3 (PB3) to enter control configuration menu.
"""

import json
import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

max_linear_speed = 60
speed_boost = 3  # Curve outside wheel max speed limit
kp = 1.3
ki = 0.0013
kd = 0.35  # PID control gains
filename = "config_line_follow_pid.json"

integral_error = 0.0  # Integral error
differential_error = 0.0  # Differential error
previous_proportional_error = 0  # Previous proportional eror
MAX_SPEED = 100.0


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


def set_gain(new_gain, multiplier, increment, text):
    new_gain = int(new_gain * multiplier)
    button = 0
    while button != 3:
        one.lcd2(text + " Gain:", new_gain)
        button = one.read_button()
        if button == 1:
            new_gain += increment
            time.sleep(0.150)
        if button == 2:
            new_gain -= increment
            time.sleep(0.150)
    while button == 3:  # Wait PB3 to be released
        button = one.read_button()
    return new_gain / multiplier


def set_kp_gain(new_gain):
    return set_gain(new_gain, 1000, 10, " Kp")


def set_ki_gain(new_gain):
    return set_gain(new_gain, 10000, 1, " Ki")


def set_kd_gain(new_gain):
    return set_gain(new_gain, 1000, 10, " Kd")


def menu():
    global max_linear_speed
    global speed_boost
    global kp
    global ki
    global kd

    one.stop()
    one.lcd1("  Menu Config:")
    one.lcd2("PB1+ PB2- PB3ok")
    time.sleep(0.250)
    while one.read_button() == 3:  # Wait PB3 to be released
        time.sleep(0.150)

    max_linear_speed = set_max_speed(max_linear_speed)  # Maximum speed
    speed_boost = set_speed_boost(speed_boost)  # Outside wheel speed boost
    kp = set_kp_gain(kp)  # Linear gain KLine
    ki = set_ki_gain(ki)
    kd = set_kd_gain(kd)
    save_config(
        max_linear_speed, speed_boost, kp, ki, kd
    )  # Save values to configuration file

    one.lcd1("Line  Following!")
    one.lcd2("www.botnroll.com")
    time.sleep(0.250)


def load_config():
    """
    Read config values from file.
    max_linear_speed, speed_boost and gain
    """
    global max_linear_speed
    global speed_boost
    global kp
    global ki
    global kd

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            # Access values from JSON file
            max_linear_speed = data["max_linear_speed"]
            speed_boost = data["speed_boost"]
            kp = data["kp"]
            ki = data["ki"]
            kd = data["kd"]

    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        print(f"The file '{filename}' doesn't exist. Using default values.")


def save_config(new_max_linear_speed, new_speed_boost, new_kp, new_ki, new_kd):
    """
    Save config values to file.
    max_linear_speed, speed_boost and gain
    """
    data = {
        "max_linear_speed": new_max_linear_speed,
        "speed_boost": new_speed_boost,
        "kp": new_kp,
        "ki": new_ki,
        "kd": new_kd,
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
    load_config()
    one.lcd1("Line Follow PID.")
    one.lcd2(" Press a button ")
    while one.read_button() == 0:  # Wait a button to be pressed
        pass
    while one.read_button() != 0:  # Wait for button release
        pass


def loop():
    global integral_error
    global differential_error
    global previous_proportional_error

    line = one.read_line()  # Read the line sensor value [-100, 100]
    line_ref = 0  # Reference line value
    proportional_error = 0  # Proportional error
    output = 0.0  # PID control output

    proportional_error = line_ref - line  # Proportional error
    differential_error = (
        proportional_error - previous_proportional_error
    )  # Differential error
    output = (
        (kp * proportional_error) + (ki * integral_error) + (kd * differential_error)
    )

    # Clean integral error if line value is zero or if line signal has changed
    if (proportional_error * previous_proportional_error) <= 0:
        integral_error = 0.0
    output = cap_value(output, -MAX_SPEED, MAX_SPEED)
    if output > MAX_SPEED:
        output = MAX_SPEED  # Limit the output value
    elif output < -MAX_SPEED:
        output = -MAX_SPEED
    else:
        integral_error += (
            proportional_error  # Increment integral error if output is within limits
        )

    previous_proportional_error = proportional_error

    vel_m1 = max_linear_speed - output
    vel_m2 = max_linear_speed + output
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
