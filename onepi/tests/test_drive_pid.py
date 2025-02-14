"""
This test uses the PID controller to control the speed of the wheels on the robot
It sets both wheels moving at the same time for a few seconds
using the PID controller.
It then changes the speed a few times and finally stops both wheels.
"""

import time
import signal
from onepi.one import BnrOneA
from onepi.utils.drive_pid import DrivePid
from onepi.utils.pid_params import PidParams

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A+
pid_params = PidParams()
drive_pid = DrivePid()

def test_drive_pid():
    """
    test the drive_pid class by setting the wheels to move
    at a certain speed for a small period of time
    """
    
    print("move: 200, 200")
    drive_pid.move(200, 200)
    time.sleep(3)
    print("move: 0,0")
    drive_pid.move(0, 0)
    time.sleep(3)
    print("move: 400, 400")
    drive_pid.move(400, 400)
    time.sleep(3)
    print("move: 700, 700")
    drive_pid.move(700, 700)
    time.sleep(3)


def setup():
    """
    setup function
    """
    one.stop()
    one.set_min_battery_V(9.6)
    one.lcd1(" Test drive pid ")
    one.lcd2("                ")
    time.sleep(0.2)
    test_drive_pid()
    drive_pid.stop()
    one.stop()


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        print("stop and exit")
        drive_pid.stop()
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    """
    main function
    """
    setup()


if __name__ == "__main__":
    main()
