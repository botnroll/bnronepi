"""
 Latest update: 05-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
Robot moves avoiding obstacles. Wheel speeds are set depending on the sensor readings.
e.g. If the left sensor reports a value higher than the right sensor, then the speed of
the oposite wheel (right wheel in this case) will be reduced by an amount proportional
to that sensor reading (multiplied by a constant gain kL)
"""

import time
import signal
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

left_motor = 0
right_motor = 0
kL = 2.70  # Linear gain
vel = 60


def setup():
    on = 1
    one.stop()  # stop motors
    one.obstacle_emitters(on)  # activate IR emitters
    one.lcd1("Obstacles  Range")
    one.lcd2("Press a Button!!")
    while one.read_button() == 0:  # Wait a button to be pressed
        pass
    while one.read_button() != 0:  # Wait for button release
        pass


def loop():
    left_range = one.read_left_range()  # read left obstacle sensor range
    right_range = one.read_right_range()  # read right obstacle sensor range
    one.lcd1("Range Left : ", left_range)
    one.lcd2("Range Right: ", right_range)

    if left_range > right_range:
        right_motor = vel - (left_range * kL)
        left_motor = vel

    elif left_range < right_range:
        right_motor = vel
        left_motor = vel - (right_range * kL)

    elif left_range == right_range:
        right_motor = vel
        left_motor = vel

    one.move(left_motor, right_motor)
    time.sleep(0.025)  # The robot has new readings every 25ms (40 readings per second)


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
