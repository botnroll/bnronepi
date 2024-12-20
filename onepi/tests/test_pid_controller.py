"""
This version of PID controller doesn't use real speeds in mm per second
"""

import time
import signal
from onepi.one import BnrOneA
from onepi.utils.pid_params import PidParams
from onepi.utils.pid_controller import PidController

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

kp = 0.02
ki = 0.7
kd = 0.03
pid_params = PidParams(kp, ki, kd)
right_pid_controller = PidController(pid_params, -800, 800)
left_pid_controller = PidController(pid_params, -800, 800)


def print_value(text, value):
    """
    prints text and value
    """
    print(text, value)


def print_pair(text, value1, value2):
    """
    prints the text and input values separated by comma
    """
    print(text, value1, ", ", value2)


def maybe_change_sign(absValue, refValue):
    """
    brief sets the sign of the output value to match the sign of refValue
    param absValue
    param refValue
    return int
    """
    if refValue < 0:
        return -absValue
    return absValue


def test_pid():
    """
    test pid function for 5 seconds by setting the wheel speed
    """
    left_power = 0
    right_power = 0
    count = 0
    while count < 50:
        count = count + 1
        # left_encoder = one.read_left_encoder()
        # left_encoder = maybe_change_sign(left_encoder, left_power)
        # left_power = left_pid_controller.compute_output(left_encoder)

        right_encoder = one.read_right_encoder()
        # right_encoder = maybe_change_sign(right_encoder, right_power)
        right_power = right_pid_controller.compute_output(right_encoder)

        one.move(0, right_power)
        time.sleep(0.1)  # ms

        # print_pair("left_encoder, leftPower: ", left_encoder, int(left_power))

        print(
            "setpoint, right_encoder, right_power: ",
            right_pid_controller.get_setpoint(),
            right_encoder,
            int(right_power),
        )


def setup():
    """
    setup function
    """
    global right_pid_controller
    global left_pid_controller
    one.stop()
    one.min_battery(9.6)

    one.lcd1("Test PID Control")
    one.lcd2("______v1.0______")
    time.sleep(1)  # ms
    one.reset_left_encoder()
    one.reset_right_encoder()

    set_speed = 30
    setpoint = set_speed * 10  # emulate conversion from speed to encoder readings
    print("setpoint:", setpoint)
    left_pid_controller.change_setpoint(setpoint)
    right_pid_controller.change_setpoint(setpoint)

    test_pid()
    right_pid_controller.change_setpoint(10 * 10)
    test_pid()
    right_pid_controller.change_setpoint(50 * 10)
    test_pid()
    right_pid_controller.change_setpoint(5 * 10)
    test_pid()
    one.stop()


def loop():
    one.stop()
    time.sleep(1)


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()


if __name__ == "__main__":
    main()
onepi / utils / drive_pid.py
