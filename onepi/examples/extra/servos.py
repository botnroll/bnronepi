"""
 Latest update: 05-09-2023
 
 This code example is in the public domain.
 http://www.botnroll.com

This example demonstrates the use of Pan&Tilt (using servos)

NOTE:
Servo1 values vary between  10 - 170 (right - left) -> PAN
Servo2 values vary between  30 - 130 (upwards - head down) -> TILT
Avoid using the servos on the limit values.
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

pos_servo_1 = 90
pos_servo_2 = 90
servo = 1


def setup():
    one.stop()  # stop motors
    one.lcd1(" Bot'n Roll ONE")
    one.lcd2("www.botnroll.com")
    one.servo1(90)  # Central position 0º - 180º
    one.servo2(90)  # Central position 0º - 180º
    time.sleep(1)


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


def loop():
    global pos_servo_1
    global pos_servo_2
    global servo

    button = one.read_button()
    if button == 1:  # Pan
        if servo == 1:
            pos_servo_1 += 10
        else:
            pos_servo_2 += 10
    elif button == 2:  # Tilt
        if servo == 1:
            pos_servo_1 -= 5
        else:
            pos_servo_2 -= 5
    elif button == 3:
        servo += 1
        if servo > 2:
            servo = 1
        one.lcd1("   Servo = " + str(servo))
        one.lcd2("")
        time.sleep(1)

    pos_servo_1 = cap_value(pos_servo_1, 0, 200)
    pos_servo_2 = cap_value(pos_servo_2, 0, 200)

    one.lcd1("Position 1: ", pos_servo_1)
    one.lcd2("Position 2: ", pos_servo_2)
    if servo == 1:
        one.servo1(pos_servo_1)
    elif servo == 2:
        one.servo2(pos_servo_2)
    print("Position 1: ", pos_servo_1, "  Position 2: ", pos_servo_2, "  Servo = ", servo, end="     \r")
    time.sleep(0.1)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
