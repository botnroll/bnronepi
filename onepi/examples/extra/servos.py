"""
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

one = BnrOneA(0, 0)  # declaration of object variable to control the Bot'n Roll ONE A

Pos_Servo1 = 90
Pos_Servo2 = 90
Servo = 1


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
    global Pos_Servo1
    global Pos_Servo2
    global Servo

    button = one.read_button()
    if button == 1:  # Pan
        if Servo == 1:
            Pos_Servo1 += 10
        else:
            Pos_Servo2 += 10
    elif button == 2:  # Tilt
        if Servo == 1:
            Pos_Servo1 -= 5
        else:
            Pos_Servo2 -= 5
    elif button == 3:
        Servo += 1
        if Servo > 2:
            Servo = 1

    Pos_Servo1 = cap_value(Pos_Servo1, 0, 200)
    Pos_Servo2 = cap_value(Pos_Servo2, 0, 200)

    one.lcd1("Position 1: ", Pos_Servo1)
    one.lcd2("Position 2: ", Pos_Servo2)
    if Servo == 1:
        one.servo1(Pos_Servo1)
    elif Servo == 2:
        one.servo2(Pos_Servo2)
    time.sleep(0.1)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
