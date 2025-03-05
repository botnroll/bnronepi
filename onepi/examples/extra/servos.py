"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

This example demonstrates the use of the Gripper.

NOTE:
Gripper1 values vary between  80 - 160 (upwards - downwards) - (130 corresponds to Horizontal)
Gripper2 values vary between  18 - 120 (closed - open)

On the Raspberry Pi side the output pins are GPIO12 and GPIO13.
On the Bot'n Roll side the gripper should be connected to pins 2 and 3.
Press PB1 to increase the angle and PB2 to decrease it.
Press PB3 to change selection of servo.
To reduce jittering this example uses pigpio. You might need to run:
 $ sudo pigpiod
 $ export PIGPIO_ADDR=soft, export PIGPIO_PORT=8888
"""

import time
from onepi.one import BnrOneAPlus
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory


one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

GPIO.setmode(GPIO.BCM)  # Use GPIO numbering

servo1 = Servo(
    12,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.5 / 1000,
    pin_factory=PiGPIOFactory(),
)
servo2 = Servo(
    13,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.5 / 1000,
    pin_factory=PiGPIOFactory(),
)

pos_servo_1 = 100
pos_servo_2 = 100
servo = 1


def setup():
    one.stop()  # stop motors
    one.lcd1("Bot'n Roll ONE A+")
    one.lcd2("www.botnroll.com")
    servo1.min()
    servo2.min()
    time.sleep(1)
    servo1.max()
    servo2.max()
    time.sleep(1)
    servo1.mid()
    servo2.mid()
    time.sleep(1)


def cap_value(value, lower_limit, upper_limit):
    """
    Caps the value to lower and upper limits
    """
    value = max(value, lower_limit)
    value = min(value, upper_limit)
    return value


def change_angle():
    global pos_servo_1
    global pos_servo_2
    if servo == 1:
        pos_servo_1 = cap_value(pos_servo_1, 0, 200)
        servo1.value = (pos_servo_1 / 100) - 1
    elif servo == 2:
        pos_servo_2 = cap_value(pos_servo_2, 0, 200)
        servo2.value = (pos_servo_2 / 100) - 1


def loop():
    global pos_servo_1
    global pos_servo_2
    global servo
    button = one.read_button()
    if button == 1:
        if servo == 1:
            pos_servo_1 += 5
        else:
            pos_servo_2 += 5
        change_angle()
    elif button == 2:
        if servo == 1:
            pos_servo_1 -= 5
        else:
            pos_servo_2 -= 5
        change_angle()
    elif button == 3:
        servo += 1
        if servo > 2:
            servo = 1
        one.lcd1("   Servo = " + str(servo))
        one.lcd2("")
        time.sleep(1)

    pos_servo_1 = cap_value(pos_servo_1, 0, 200)
    pos_servo_2 = cap_value(pos_servo_2, 0, 200)

    one.lcd1("Gripper 1: ", pos_servo_1)
    one.lcd2("Gripper 2: ", pos_servo_2)
    msg = (
        "Gripper 1: "
        + str(pos_servo_1)
        + "    Gripper 2: "
        + str(pos_servo_2)
        + "    Servo = "
        + str(servo)
    )
    print(msg, end="     \r")
    time.sleep(0.2)


def main():
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
