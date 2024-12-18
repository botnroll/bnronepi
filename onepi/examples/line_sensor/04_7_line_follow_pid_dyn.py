"""
 Latest update: 04-09-2023

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

import os
import json
import time
import signal
from pynput import keyboard
import threading
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

max_linear_speed = 60
speed_boost = 3  # Curve outside wheel max speed limit
kp = 1.3
ki = 0.0013
kd = 0.35  # PID control gains
file_name = "config_line_follow_pid_dyn.json"
filename = os.path.join(os.path.dirname(__file__), file_name)

integral_error = 0.0  # Integral error
differential_error = 0.0  # Differential error
previous_error = 0  # Previous proportional eror
MAX_SPEED = 100.0
stop = False
key_pressed = False


def wait_user_input():
    button = 0
    while button == 0:  # Wait a button to be pressed
        button = one.read_button()
    while one.read_button() != 0:  # Wait for button release
        pass
    return button


def set_max_speed(new_max_linear_speed):
    option = 0
    while option != 3:
        if option == 1:
            new_max_linear_speed += 1
        if option == 2:
            new_max_linear_speed -= 1
        new_max_linear_speed = cap_value(new_max_linear_speed, 0, 100)
        one.lcd1("   VelMax:", new_max_linear_speed)
        option = wait_user_input()
    return new_max_linear_speed


def set_speed_boost(new_speed_boost):
    option = 0
    while option != 3:
        if option == 1:
            new_speed_boost += 1
        if option == 2:
            new_speed_boost -= 1
        new_speed_boost = cap_value(new_speed_boost, 0, 20)
        one.lcd1(" Curve Boost:", new_speed_boost)
        option = wait_user_input()
    return new_speed_boost


def set_gain(new_gain, multiplier, increment, text, max_value, min_value=0):
    global key_pressed
    new_gain = int(new_gain * multiplier)
    max_value = max_value * multiplier
    option = 0
    while option != 3:
        if option == 1:
            new_gain += increment
            time.sleep(0.150)
        if option == 2:
            new_gain -= increment
            time.sleep(0.150)
        new_gain = cap_value(new_gain, min_value, max_value)

        if not key_pressed:
            one.lcd1(text + " Gain:", new_gain)
        option = wait_user_input()
    return new_gain / multiplier


def set_kp_gain(new_gain):
    return set_gain(new_gain, 100, 1, " Kp", 100)


def set_ki_gain(new_gain):
    return set_gain(new_gain, 100, 1, " Ki", 100)


def set_kd_gain(new_gain):
    return set_gain(new_gain, 100, 1, " Kd", 100)


def config_menu():
    global max_linear_speed, speed_boost, kp, ki, kd
    print("Menu")
    one.lcd2("1:Menu")
    time.sleep(1)
    one.lcd2("1:++ 2:--   3:OK")

    max_linear_speed = set_max_speed(max_linear_speed)  # Maximum speed
    speed_boost = set_speed_boost(speed_boost)  # Outside wheel speed boost
    kp = set_kp_gain(kp)
    ki = set_ki_gain(ki)
    kd = set_kd_gain(kd)
    save_config(
        max_linear_speed, speed_boost, kp, ki, kd
    )  # Save values to configuration file


def main_screen():
    one.lcd1("Line Follow PID")
    one.lcd2("www.botnroll.com")


def menu():
    print("Menu -> stop robot")
    one.stop()
    while one.read_button() != 0:
        pass
    option = 0
    while option != 3:
        one.lcd1("Line Follow PID")
        one.lcd2("1:Menu   3:Start")
        option = wait_user_input()
        if option == 1:
            config_menu()
    one.lcd2("         3:Start")
    time.sleep(1)
    main_screen()


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


def on_press(key):
    global stop, max_linear_speed, speed_boost, kp, ki, kd, one, key_pressed, executing_command
    key_pressed = True
    while executing_command:
        pass
    try:
        # print(f'Key {key.char} pressed')
        if key == keyboard.Key.left:
            one.stop()
            one.move(-max_linear_speed * 3 / 4.0, max_linear_speed * 3 / 4.0)
            time.sleep(0.3)
            one.stop()
        elif key == keyboard.Key.right:
            one.stop()
            one.move(max_linear_speed * 3 / 4.0, -max_linear_speed * 3 / 4.0)
            time.sleep(0.3)
            one.stop()
        elif key == keyboard.Key.up:
            one.stop()
            one.move(max_linear_speed * 2 / 3.0, max_linear_speed * 2 / 3.0)
            time.sleep(0.5)
            one.stop()
        elif key == keyboard.Key.down:
            one.stop()
            one.move(-max_linear_speed * 2 / 3.0, -max_linear_speed * 2 / 3.0)
            time.sleep(0.5)
            one.stop()
        elif key.char == "q":
            kp += 0.02
            kp = cap_value(kp, 0, 10)
        elif key.char == "a":
            kp -= 0.02
            kp = cap_value(kp, 0, 10)
        elif key.char == "w":
            ki = round(ki * 10) / 10
            ki += 0.1
            ki = cap_value(ki, 0, 10)
        elif key.char == "s":
            ki = round(ki * 10) / 10
            ki -= 0.1
            ki = cap_value(ki, 0, 10)
        elif key.char == "e":
            kd += 0.01
            kd = cap_value(kd, 0, 10)
        elif key.char == "d":
            kd -= 0.01
            kd = cap_value(kd, 0, 10)
        elif key.char == "p":
            max_linear_speed += 1
        elif key.char == "l":
            max_linear_speed -= 1
        elif key.char == "o":
            speed_boost += 1
        elif key.char == "k":
            speed_boost -= 1
        elif key.char == "g":
            stop = False
        elif key.char == "b":
            one.stop()
            stop = True
        save_config(max_linear_speed, speed_boost, kp, ki, kd)
    except AttributeError:
        print(f"Special key {key} pressed")
    key_pressed = False


def on_release(key):
    # print(f'Key {key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


listener_thread = threading.Thread(target=start_listener)
listener_thread.start()


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
    one.min_battery(12.5)  # safety voltage for discharging the battery
    one.stop()  # stop motors
    load_config()
    time.sleep(2)
    # menu()


def loop():
    global integral_error, differential_error, previous_error
    global max_linear_speed, speed_boost, kp, ki, kd, stop, key_pressed, executing_command

    if not key_pressed:
        executing_command = True
        line = one.read_line()  # Read the line sensor value [-100, 100]
        executing_command = False
    else:
        line = 0
    line_ref = 0  # Reference line value
    output = 0.0  # PID control output

    error = line_ref - line  # Proportional error
    integral_error += error  # Increment integral error
    integral_error = cap_value(integral_error, -3000, 3000)
    # Clean integral error if line value is zero or if line signal has changed
    if (error * previous_error) <= 0:
        integral_error = 0.0
    differential_error = error - previous_error  # Differential error
    output = (kp * error) + (ki / 100.0 * integral_error) + (kd * differential_error)

    output = cap_value(output, -MAX_SPEED, MAX_SPEED)
    previous_error = error

    # max_speed = (max_linear_speed * (1.0 - ((abs(error) / 100.0) / 2.0)))
    max_speed = max_linear_speed
    vel_m1 = max_speed - output
    vel_m2 = max_speed + output
    # Limit motors maximum and minimum speed
    vel_m1 = cap_value(vel_m1, -max_speed, max_speed)
    vel_m2 = cap_value(vel_m2, -max_speed, max_speed)

    print(
        " Line:",
        int(line),
        "   M1:",
        int(vel_m1),
        "   M2:",
        int(vel_m2),
        " max speed: ",
        int(max_speed),
        "error",
        int(error),
        "integral error",
        int(integral_error),
        "differential error",
        int(differential_error * 10) / 10.0,
        "kp",
        int(kp * 100) / 100,
        "ki",
        int(ki * 1000) / 1000,
        "kd",
        round(kd * 100) / 100,
        end="       \r",
    )
    if not key_pressed:
        if stop:
            executing_command = True
            one.stop()
            executing_command = False
        else:
            executing_command = True
            one.move(vel_m1, vel_m2)
            executing_command = False
    # time.sleep(0.05)

    # Configuration menu


#    if not key_pressed:
#        if one.read_button() == 3:
#            menu()  # PB3 to enter menu
#            integral_error = 0
#            previous_error = 0


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
