import time
from onepi.one import BnrOneA
from onepi.utils.move_pid import MovePid

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def test_move_pid():
    """
    test the move_pid class by setting the wheels to move
    at a certain speed for a small period of time
    """
    move_pid = MovePid()
    move_pid.move(200, 200)
    time.sleep(3)
    move_pid.move(0, 0)
    time.sleep(1)
    move_pid.stop()


def setup():
    """
    setup function
    """
    one.stop()
    one.min_battery(9.6)
    one.lcd1(" Test move_pid  ")
    one.lcd2("________________")
    test_move_pid()
    one.stop()


def main():
    """
    main function
    """
    setup()


if __name__ == "__main__":
    main()
