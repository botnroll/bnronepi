import threading
import sys
import tty
import termios
import time

"""
This version of PID controller doesn't use Main program running...real speeds in mm per second
"""

import time
import signal
import keyboard
import threading
from onepi.one import BnrOneA
from onepi.utils.pid_params import PidParams
from onepi.utils.plot_chart import PlotChart
from onepi.utils.pid_controller import PidController

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

kp = 0.02
ki = 0.07  # 0.7
kd = 0.03
pid_params = PidParams(kp, ki, kd)
right_pid_controller = PidController(pid_params, -800, 800)
left_pid_controller = PidController(pid_params, -800, 800)


def update_pid_params():
    """
    updates pid params using keyboard
    """
    global file_descriptors
    global kp, ki, kd, right_pid_controller, left_pid_controller
    # Save the current terminal settings
    file_descriptors = termios.tcgetattr(sys.stdin)
    # Set the terminal to raw mode
    tty.setcbreak(sys.stdin)

    def update_pid():
        right_pid_controller.set_pid_params(PidParams(kp, ki, kd))
        left_pid_controller.set_pid_params(PidParams(kp, ki, kd))
        # print("kp,ki,kd: ", kp, ki, kd)

    try:
        while True:
            char = sys.stdin.read(1)[0]
            if char == "P":
                kp = int((kp * 100) + 1)
                kp /= 100
                update_pid()
            if char == "p":
                kp = int((kp * 100) - 1)
                kp /= 100
                update_pid()
            if char == "I":
                ki = int((ki * 100) + 1)
                ki /= 100
                update_pid()
            if char == "i":
                ki = int((ki * 100) - 1)
                ki /= 100
                update_pid()
            if char == "D":
                kd = int((kd * 100) + 1)
                kd /= 100
                update_pid()
            if char == "d":
                kd = int((kd * 100) - 1)
                kd /= 100
                update_pid()
    finally:
        # Restore the terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, file_descriptors)


thread = threading.Thread(target=update_pid_params)
thread.start()


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
    global plotter
    left_power = 0
    right_power = 0
    count = 0
    while count < 50:
        count = count + 1
        # left_encoder = one.read_left_encoder()
        # left_encoder = maybe_change_sign(left_encoder, left_power)
        # left_power = left_pid_controller.compute_output(left_encoder)

        right_encoder = one.read_right_encoder()
        right_encoder = maybe_change_sign(right_encoder, right_power)
        right_power = right_pid_controller.compute_output(right_encoder)

        one.move_calibrate(0, right_power)
        # time.sleep(0.05)  # ms

        # print_pair("left_encoder, leftPower: ", left_encoder, int(left_power))
        plotter.update_buffers(right_pid_controller.get_setpoint(), right_encoder)
        print(
            "setpoint, right_encoder, right_power: (kp, ki, kd) ",
            right_pid_controller.get_setpoint(),
            right_encoder,
            int(right_power),
            "(",
            right_pid_controller.get_pid_params().kp,
            ",",
            right_pid_controller.get_pid_params().ki,
            ",",
            right_pid_controller.get_pid_params().kd,
            ")",
        )


def setup():
    """
    setup function
    """
    global right_pid_controller
    global left_pid_controller
    global plotter
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
    plotter = PlotChart()
    plotter.show_plot()
    while True:
        right_pid_controller.change_setpoint(50 * 10)
        test_pid()
        right_pid_controller.change_setpoint(5 * 10)
        test_pid()
    one.stop()


def loop():
    one.stop()
    time.sleep(1)


def main():
    global file_descriptors

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        # Restore the terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, file_descriptors)
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()


if __name__ == "__main__":
    main()
