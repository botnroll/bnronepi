"""
This example shows how to use a PID controller to control the wheel speeds of Bot'n Roll ONE A
The minimum speed is about 250 mm/s and the max speed is 850 mm/s for a reference battery of 12V.
Note that these values might change depending on the battery you're using and its current charge.
You can specify your own PID params, kp, ki, kd.
This example uses the default values and an update period of 200ms.
Note if you change the update period you need to tune the PID params.
Important: Please run motors calibrate routine but instead of setting the power to when
the wheels start moving set it to when they stop moving.
This allows PID more room to control the speeds at lower values.
"""

from onepi.one import BnrOneA
from onepi.utils.drive_pid import DrivePid
import time

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def test_move_pid():
    """
    test the move_pid class by setting the wheels to move
    at a certain speed for a small period of time
    """
    one_pid = DrivePid()
    one_pid.move(300, 300)
    time.sleep(3)
    one_pid.move(0, 0)
    time.sleep(1)
    one_pid.stop()

def setup():
    """
    setup method
    """
    test_move_pid()

def loop():
    """
    loop method
    """
    one.stop()
    time.sleep(1)


def main():
    setup()
    #while True:
    #    loop()


if __name__ == "__main__":
    main()