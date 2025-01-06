import time
import signal
from onepi.one import BnrOneA
from onepi.utils.drive_pid import DrivePID

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def test_drive_pid():
    """
    test the drive_pid class by setting the wheels to move
    at a certain speed for a small period of time
    """
    while(True):
        drive_pid = DrivePID()
        print("move: 200, 200")
        drive_pid.move(200, 200)
        time.sleep(3)
        print("move: 0,0")
        drive_pid.move(0, 0)
        time.sleep(3)
        # print("move: 400, 400")
        # drive_pid.move(400, 400)
        # time.sleep(3)
        # print("move: 700, 700")
        # drive_pid.move(700, 700)
        # time.sleep(3)
        # print("stop")
        # drive_pid.stop()


def setup():
    """
    setup function
    """
    one.stop()
    one.min_battery(9.6)
    one.lcd1(" Test drive_pid  ")
    one.lcd2("________________")
    test_drive_pid()
    one.stop()


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
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
