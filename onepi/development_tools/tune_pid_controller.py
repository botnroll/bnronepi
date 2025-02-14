import threading
import sys
import tty
import termios
import time

"""
This version of PID controller doesn't use real speeds in mm per second.
It just uses encoders count.
It allows you to change the kp, ki and kd params by using the keyboard
'P' - increases the kp param
'p' - decreases the kp param
'I' - increases the ki param
'i' - decreases the ki param
'D' - increases the kd param
'd' - decreases the kd param
It runs in a loop until you press CTRL-C and then Enter
You can see a plot showing how the response tracks the reference value.
The reference values changes periodically between two different values.
"""

import time
import signal
import keyboard
import threading
from onepi.one import BnrOneA
from onepi.utils.pid_params import PidParams
from onepi.utils.chart_plotter import ChartPlotter
from onepi.utils.pid_controller import PidController

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A+

# pid params that work well both free wheeling and under load at both high and low speeds
# minimum speed tested :
# kp = 0.070
# ki = 0.015
# kd = 0.000

# pid_params = PidParams(kp, ki, kd)
pid_params = PidParams()
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
        global kp, ki, kd
        if not stop_execution:
            if kp < 0.0:
                kp = 0.0
            if ki < 0.0:
                ki = 0.0
            if kd < 0.0:
                kd = 0.0
            right_pid_controller.set_pid_params(PidParams(kp, ki, kd))
            left_pid_controller.set_pid_params(PidParams(kp, ki, kd))
    

    try:
        correction = 5.0
        while not stop_execution:
            char = sys.stdin.read(1)[0]            
            if char == "C":
                correction += 1.0
                print("correction = ", correction)
                time.sleep(0.5)
            if char == "c":
                correction -= 1.0
                if correction < 0:
                    correction = 0 
                print("correction = ", correction)
                time.sleep(0.5)
            if char == "P":
                kp = ((kp * 1000) + correction)
                kp /= 1000.0
                update_pid()
            if char == "p":
                kp = int((kp * 1000) - correction)
                kp /= 1000.0
                update_pid()
            if char == "I":
                ki = int((ki * 1000) + correction)
                ki /= 1000.0
                update_pid()
            if char == "i":
                ki = int((ki * 1000) - correction)
                ki /= 1000.0
                update_pid()
            if char == "D":
                kd = int((kd * 1000) + correction / 5.0)
                kd /= 1000.0
                update_pid()
            if char == "d":
                kd = int((kd * 1000) - correction / 5.0)
                kd /= 1000.0
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

def test_pid():
    """
    test pid function for 5 seconds by setting the wheel speed
    """
    global plotter, stop_execution
    left_power = 0
    right_power = 0
    count = 0
    time_previous = time.time()
    while count < 50 and not stop_execution:
        count = count + 1
        # left_encoder = one.read_left_encoder()
        # left_power = left_pid_controller.compute_output(left_encoder)

        right_encoder = one.read_right_encoder()
        right_power = right_pid_controller.compute_output(right_encoder)

        #one.move(0, right_power)
        one.move_raw(0, right_power)
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
            round(right_pid_controller.get_pid_params().kp, 3),
            ",",
            round(right_pid_controller.get_pid_params().ki, 3),
            ",",
            round(right_pid_controller.get_pid_params().kd, 3),
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
    one.set_min_battery_V(9.6)

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
    plotter = ChartPlotter(100, "Time (x100) ms", "Speed (mm/s)")
    plotter.show_plot()
    
    stop_execution = False
    my_thread = StoppableThread(target=update_pid_params)
    my_thread.start()

    while not stop_execution:
        right_pid_controller.change_setpoint(50 * 10)
        test_pid()
        right_pid_controller.change_setpoint(10 * 10)
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
