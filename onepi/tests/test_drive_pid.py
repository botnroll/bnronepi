import time
import signal
from onepi.one import BnrOneA
from onepi.utils.drive_pid import DrivePID

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def test_move_pid():
    """
    test the move_pid class by setting the wheels to move
    at a certain speed for a small period of time
    """
    move_pid = DrivePID()
    print("move: 200, 200")
    move_pid.move(200, 200)
    time.sleep(3)
    print("move: 0,0")
    move_pid.move(0, 0)
    time.sleep(3)
    print("move: 400, 400")
    move_pid.move(400, 400)
    time.sleep(3)
    print("move: 800, 800")
    move_pid.move(800, 800)
    time.sleep(3)
    print("stop")
    move_pid.stop()


def setup():
    """
    setup function
    """
    one.stop()
    one.min_battery(9.6)
    one.lcd1(" Test drive_pid  ")
    one.lcd2("________________")
    test_move_pid()
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
