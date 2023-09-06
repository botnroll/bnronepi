"""
 Latest update: 05-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

This example demonstrates the use of the Gripper.

NOTE:
Gripper1 values vary between  80 - 160 (upwards - downwards) - (130 corresponds to Horizontal)
Gripper2 values vary between  18 - 120 (closed - open)

On the Raspberry Pi side the output pins are GPIO17 and GPIO18 (corresponding to pins 11 and 12).
On the Bot'n Roll side the gripper should be connected to pins 2 and 3.
Press PB1 to increase the angle and PB2 to decrease it.
Press PB3 to change selection of servo.
"""

import time
from one import BnrOneA
import RPi.GPIO as GPIO
import time

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

GPIO.setmode(GPIO.BCM)

servo_pin_1 = 17  # Use the GPIO pin you've connected to
servo_pin_2 = 18  # Use the GPIO pin you've connected to

GPIO.setup(servo_pin_1, GPIO.OUT)
GPIO.setup(servo_pin_2, GPIO.OUT)

gripper1 = GPIO.PWM(servo_pin_1, 50)  # 50 Hz frequency
gripper2 = GPIO.PWM(servo_pin_2, 50)  # 50 Hz frequency

pos_servo_1 = 140
pos_servo_2 = 120
servo = 1


def setup():
    one.stop()  # stop motors
    one.lcd1("Bot'n Roll ONE A")
    one.lcd2("www.botnroll.com")
    time.sleep(1)

    gripper1.start(0)  # Initialization
    gripper2.start(0)


def set_angle(servo_motor, angle):
    duty_cycle = 2 + (angle / 18)  # Map angle to duty cycle
    servo_motor.ChangeDutyCycle(duty_cycle)


def gripper_open():
    set_angle(gripper2, 120)


def gripper_close():
    set_angle(gripper2, 18)


def cap_value(value, lower_limit, upper_limit):
    """
    Caps the value to lower and upper limits
    """
    value = max(value, lower_limit)
    value = min(value, upper_limit)
    return value


def change_angle():
    if servo == 1:
        set_angle(gripper1, pos_servo_1)
    elif servo == 2:
        set_angle(gripper2, pos_servo_2)


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
    msg = "Gripper 1: " + str(pos_servo_1) + "    Gripper 2: " + str(pos_servo_2) + "    Servo = " + str(servo)
    print(msg, end="     \r")
    time.sleep(0.2)


def main():
    setup()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        gripper1.stop()
        gripper2.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
