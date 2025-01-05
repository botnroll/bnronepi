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

kp = 0.2
ki = 0.2  # 0.7
kd = 0.1
pid_params = PidParams(kp, ki, kd)
right_pid_controller = PidController(pid_params, -800, 800)
left_pid_controller = PidController(pid_params, -800, 800)


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


def update_pid_params():
    """
    updates pid params using keyboard
    """
    global stop_execution
    global kp, ki, kd, right_pid_controller, left_pid_controller
    # Save the current terminal settings
    file_descriptors = termios.tcgetattr(sys.stdin)
    # Set the terminal to raw mode
    tty.setcbreak(sys.stdin)

    def update_pid():
        if not stop_execution:
            right_pid_controller.set_pid_params(PidParams(kp, ki, kd))
            left_pid_controller.set_pid_params(PidParams(kp, ki, kd))
    

    try:
        while not stop_execution:
            char = sys.stdin.read(1)[0]
            if char == "P":
                kp = ((kp * 100) + 1)
                kp /= 100.0
                update_pid()
            if char == "p":
                kp = int((kp * 100) - 1)
                kp /= 100.0
                update_pid()
            if char == "I":
                ki = int((ki * 100) + 1)
                ki /= 100.0
                update_pid()
            if char == "i":
                ki = int((ki * 100) - 1)
                ki /= 100.0
                update_pid()
            if char == "D":
                kd = int((kd * 100) + 1)
                kd /= 100.0
                update_pid()
            if char == "d":
                kd = int((kd * 100) - 1)
                kd /= 100.0
                update_pid()
        
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
    global plotter, stop_execution
    left_power = 0
    right_power = 0
    count = 0
    time_previous = time.time()
    while count < 100 and not stop_execution:
        count = count + 1
        # left_encoder = one.read_left_encoder()
        # left_encoder = maybe_change_sign(left_encoder, left_power)
        # left_power = left_pid_controller.compute_output(left_encoder)

        right_encoder = one.read_right_encoder()
        right_encoder = maybe_change_sign(right_encoder, right_power)
        right_power = right_pid_controller.compute_output(right_encoder)

        one.move(0, right_power)
        # one.move_calibrate(0, right_power)
        # time.sleep(0.05)  # ms

        # print_pair("left_encoder, leftPower: ", left_encoder, int(left_power))
        plotter.update_buffers(right_pid_controller.get_setpoint(), right_encoder)
        time_now = time.time()

        time_elapsed_ms = int((time_now - time_previous) * 1000)
        if time_elapsed_ms < 100:
            time.sleep((100-time_elapsed_ms)/1000.0)
            time_elapsed_ms = int((time.time() - time_previous) * 1000)
        time_previous = time.time()
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
            time_elapsed_ms,
            "ms"
        )
        


def setup():
    """
    setup function
    """
    global right_pid_controller
    global left_pid_controller
    global plotter, stop_execution
    global my_thread
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
    plotter = PlotChart(100)
    plotter.show_plot()
    
    stop_execution = False
    my_thread = StoppableThread(target=update_pid_params)
    my_thread.start()

    while not stop_execution:
        right_pid_controller.change_setpoint(50 * 10)
        test_pid()
        right_pid_controller.change_setpoint(5 * 10)
        test_pid()
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
