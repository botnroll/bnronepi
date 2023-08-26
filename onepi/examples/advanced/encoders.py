"""
 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 Read single channel encoders attached to Bot'n Roll ONE A wheels.
 This example sets the robot moving at a constant speed.")
 It reads the encoders and displays the readings in the lcd and terminal.
 Use PB1 to increase the speed and PB2 to decrease the speed of the motors.
 Motors will automatically stop after left encoder count gets over 495.
 To reset press PB3 and change the motor speeed with PB1 and PB2.

 Encoders
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

speed_1 = 35
speed_2 = 35


def setup():
    one.stop()
    # stop motors
    one.lcd1("Bot'n Roll ONE A")
    one.lcd2("www.botnroll.com")

    print("This example sets the robot moving at a constant speed.")
    print("It reads the encoders and displays the readings in the lcd and terminal.")
    print("Use PB1 to increase the speed and PB2 to decrease the speed of the motors.")
    print("Motors will automatically stop after left encoder count gets over 495.")
    print(
        "To reset press PB3 and change the motor speeed with PB1 and PB2.", end="\n\n"
    )

    time.sleep(3)
    one.read_left_encoder()
    one.read_right_encoder()


def loop():
    global speed_1, speed_2
    encoder_left = one.read_left_encoder_increment()
    encoder_right = one.read_right_encoder_increment()
    button = one.read_button()
    if button == 1:
        speed_1 += 1
        speed_2 += 1
    elif button == 2:
        speed_1 -= 1
        speed_2 -= 1
    elif button == 3:
        speed_1 = 0
        speed_2 = 0
        encoder_left = one.read_left_encoder()
        encoder_right = one.read_right_encoder()
    one.lcd1("L:", encoder_left, "vel:", speed_1)
    one.lcd2("R:", encoder_right, "vel:", speed_2)
    print(
        "Left:",
        encoder_left,
        " vel:",
        speed_1,
        " ||  Right:",
        encoder_right,
        " vel:",
        speed_2,
        " " * 10,
        end="\r",
    )
    if encoder_left >= 495:
        speed_1 = 0
        speed_2 = 0
    one.move(speed_1, speed_2)
    time.sleep(0.05)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
