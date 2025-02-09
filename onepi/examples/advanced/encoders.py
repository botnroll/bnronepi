"""
 Latest update: 10-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 Read single channel encoders attached to Bot'n Roll ONE A+ wheels.
 This example sets the robot moving at a constant speed.")
 It reads the encoders and displays the readings in the lcd and terminal.
 Use PB1 to increase the speed and PB2 to decrease the speed of the motors.
 Motors will automatically stop after left encoder count gets over 495.
 To reset press PB3 and change the motor speeed with PB1 and PB2.

 Encoders
"""

import time
import signal
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A+

speed_1 = 10
speed_2 = 10
TARGET_PULSES = 3000


def setup():
    one.stop()
    one.min_battery(0)

    # stop motors
    one.lcd1("Bot'n Roll ONE A+")
    one.lcd2("www.botnroll.com")

    print("This example sets the robot moving at a constant speed.")
    print("It reads the encoders and displays the readings in the lcd and terminal.")
    print("Use PB1 to increase the speed and PB2 to decrease the speed of the motors.")
    print(
        "Motors will automatically stop after left encoder count gets over TARGET_PULSES."
    )
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
        time.sleep(0.1)
    elif button == 2:
        speed_1 -= 1
        speed_2 -= 1
        time.sleep(0.1)
    elif button == 3:
        encoder_left = one.read_left_encoder() # reset encoders
        encoder_right = one.read_right_encoder()
    read_encoders()
    one.lcd1("L:", encoder_left, "vel:", speed_1)
    one.lcd2("R:", encoder_right, "vel:", speed_2)
    if encoder_left >= TARGET_PULSES or \
        encoder_right >= TARGET_PULSES:
        one.stop()
    else:
        one.move(speed_1, speed_2)
    time.sleep(0.05)

def read_encoders():
    global encoder_left
    global encoder_right
    encoder_left = one.read_left_encoder_increment()
    encoder_right = one.read_right_encoder_increment()
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
        
def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
