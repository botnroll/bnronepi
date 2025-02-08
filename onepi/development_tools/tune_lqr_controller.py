"""
This version of LQR controller doesn't use real speeds in mm per second.
It just uses encoders count.
It allows you to change the Q and R params by using the keyboard
'Q' - increases the vel state penalty param
'q' - decreases the vel state penalty param
'R' - increases the control penalty param
'r' - decreases the control penalty param
It runs in a loop until you press CTRL-C and then Enter
You can see a plot showing how the response tracks the reference value.
The reference values changes periodically between two different values.
"""

import threading
import sys
import tty
import termios
import time
import signal
import keyboard
import numpy as np

from onepi.one import BnrOneA
from onepi.utils.chart_plotter import ChartPlotter
from onepi.utils.lqr_controller import LQRController


one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

Kt = 0.01
J = 0.01
B = 0.01

A = np.array([[0, 1], [0, -B/J]])
B = np.array([[0], [Kt/J]])
C = np.array([[1, 0]])
D = np.array([[0]])

# best so far
# q0, q1, r = 0.3 , 13.8 , 5.7 

# better at low, worst at high
# q0, q1, r = 0.5, 13.8, 7.5

q0 = 0.7 # velocity 
q1 = 13.8 # acceleration: A smaller Q reduces the emphasis on state errors, making the controller less sensitive to deviations.
r = 10  # A larger R value will reduce the control effort, making the system less aggressive.
# Increase R from 10 to 20 to reduce control effort and stabilize low-speed performance.
# Q = np.diag([0.5, 5])  # Adjust Q matrix to emphasize velocity control

# LQR design parameters
Q = np.diag([q0, q1])
R = np.array([[r]])

# Instantiate the LQR controller
right_lqr_controller = LQRController(A, B, C, D, Q, R)
left_lqr_controller = LQRController(A, B, C, D, Q, R)

# Desired speed (reference speed in encoder pulses per second)
desired_speed = 10
current_left_speed = one.read_left_encoder()
print("current_left_speed: ", current_left_speed)


class StoppableThread(threading.Thread):
    def __init__(self, target):
        super().__init__()
        self._stop_event = threading.Event()
        self.target = target

    def run(self):
        while not self._stop_event.is_set():
            self.target()
    
    def stop(self):
        self._stop_event.set()


def update_lqr_params():
    """
    updates lqr params using keyboard
    """
    global stop_execution
    global q0, q1, r, right_lqr_controller, left_lqr_controller
    # Save the current terminal settings
    file_descriptors = termios.tcgetattr(sys.stdin)
    # Set the terminal to raw mode
    tty.setcbreak(sys.stdin)

    def update_lqr():
        if not stop_execution:
            Q = np.diag([q0, q1])
            R = np.array([[r]])
            right_lqr_controller.set_lqr_params(Q, R)
            left_lqr_controller.set_lqr_params(Q, R)

    try:
        while not stop_execution:
            char = sys.stdin.read(1)[0]
            if char == "V":
                q0 += 0.1
                update_lqr()
            if char == "v":
                q0 -= 0.1
                if q0 < 0.0:
                    q0 = 0
                update_lqr()
            if char == "A":
                q1 += 0.1
                update_lqr()
            if char == "a":
                q1 -= 0.1
                if q1 < 0.0:
                    q1 = 0
                update_lqr()
            if char == "R":
                r += 0.1
                update_lqr()
            if char == "r":
                r -= 0.1
                if r < 0.10:
                    r = 0.1
                update_lqr()

        print("thread stopped")
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, file_descriptors)
        except:
            pass

    finally:
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, file_descriptors)
        except:
            pass


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

def test_lqr():
    """
    test lqr function for 5 seconds by setting the wheel speed
    """
    global plotter, stop_execution
    left_power = 0
    right_power = 0
    count = 0
    time_previous = time.time()
    while count < 100 and not stop_execution:
        count = count + 1
        left_encoder = one.read_left_encoder()
        left_state, left_power = left_lqr_controller.compute_output(left_encoder)

        # right_encoder = one.read_right_encoder()
        # right_state, right_power = right_lqr_controller.compute_output(right_encoder)

        one.move_raw(left_power, 0)
        # time.sleep(0.05)  # ms

        # print_pair("left_encoder, leftPower: ", left_encoder, int(left_power))
        plotter.update_buffers(left_lqr_controller.get_setpoint(), left_encoder)
        time_now = time.time()

        time_elapsed_ms = int((time_now - time_previous) * 1000)
        if time_elapsed_ms < 100:
            time.sleep((100-time_elapsed_ms)/1000.0)
            time_elapsed_ms = int((time.time() - time_previous) * 1000)
        time_previous = time.time()
        print(
            "setpoint, left_encoder, left_power: (q0, q1, r) ",
            left_lqr_controller.get_setpoint(),
            left_encoder,
            int(left_power),
            "(",
            round(q0, 3),
            ",",
            round(q1, 3),
            ",",
            round(r, 3),
            ")",
            time_elapsed_ms,
            "ms"
        )
        


def setup():
    """
    setup function
    """
    global right_lqr_controller
    global left_lqr_controller
    global plotter, stop_execution
    global my_thread
    one.stop()
    one.min_battery(9.6)

    one.lcd1("Test LQR Control")
    one.lcd2("______v1.0______")
    time.sleep(1)  # ms
    one.reset_left_encoder()
    one.reset_right_encoder()
    bat = one.read_battery()
    one.lcd2("bat:", round(bat,2))

    set_speed = 30
    setpoint = set_speed * 10  # emulate conversion from speed to encoder readings
    print("setpoint:", setpoint)
    left_lqr_controller.change_setpoint(setpoint)
    right_lqr_controller.change_setpoint(setpoint)
    plotter = ChartPlotter(100)
    plotter.show_plot()
    
    stop_execution = False
    my_thread = StoppableThread(target=update_lqr_params)
    my_thread.start()

    while not stop_execution:
        left_lqr_controller.change_setpoint(50 * 10)
        test_lqr()
        left_lqr_controller.change_setpoint(5 * 10)
        test_lqr()
    one.stop()


def loop():
    one.stop()
    time.sleep(1)


# function to stop the robot on exiting with CTRL+C
def stop_and_exit(sig, frame):
    global my_thread, plotter
    global stop_execution
    
    print("Exiting application")
    stop_execution = True
    my_thread.stop()
    my_thread.join()
    one.stop()
    time.sleep(0.01)
    plotter.close_plot()
    sys.exit(0)

signal.signal(signal.SIGINT, stop_and_exit)

def main():
    setup()


if __name__ == "__main__":
    main()
