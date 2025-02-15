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
kp = 800
ki = 250
kd = 100


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
            one.set_pid(kp, ki, kd)
    
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
                kp = kp  + correction
                update_pid()
            if char == "p":
                kp = kp - correction
                update_pid()
            if char == "I":
                ki = ki + correction
                update_pid()
            if char == "i":
                ki = ki - correction
                update_pid()
            if char == "D":
                kd = kd + correction
                update_pid()
            if char == "d":
                kd = kd - correction
                update_pid()
            time.sleep(0.5)

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

def test_pid(setpoint):
    """
    test pid function for 5 seconds by setting the wheel speed
    """
    global chart_plotter, stop_execution
    global kp, ki, kd
    left_power = 0
    right_power = 0
    count = 0
    time_previous = time.time()
    while count < 50 and not stop_execution:
        count = count + 1        
        right_encoder = one.read_right_encoder()
        
        var1 = one.read_debug(0)
        var2 = one.read_debug(1)
        var3 = one.read_debug(2)
        var4 = one.read_debug(3)
        var5 = one.read_debug_float()
        
        one.move(0, setpoint)
        chart_plotter.update_buffers([setpoint, right_encoder/20.0, 0, 0, var5/10.0])
        time_now = time.time()

        time_elapsed_ms = int((time_now - time_previous) * 1000)
        if time_elapsed_ms < 200:
            time.sleep((200-time_elapsed_ms)/1000.0)
            time_elapsed_ms = int((time.time() - time_previous) * 1000)
        time_previous = time.time()
        print(
            "setpoint, r_enc, r_power: (kp, ki, kd), var1, var2, var3, var4, var5, time(ms) ",
            setpoint,
            right_encoder,
            int(right_power),
            "(", kp, ",", ki, ",", kd, ")",
            var1,
            ",",
            var2,
            ",",
            var3,
            ",",
            var4,
            ",",
            round(var5, 2),
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
    global chart_plotter, stop_execution
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
    chart_plotter = ChartPlotter(5, 100)
    chart_plotter.set_title("Tuning PID controller")
    chart_plotter.set_axis_labels("Time (x200 ms)", "Value")
    chart_plotter.set_y_limits(-50, 150)
    chart_plotter.set_series_labels(["setpoint", "enc", " ", " ", "errI"])
    chart_plotter.show_plot()
    
    stop_execution = False
    my_thread = StoppableThread(target=update_pid_params)
    my_thread.start()

    while not stop_execution:
        setpoint = 80
        test_pid(setpoint)
        setpoint = 10
        test_pid(setpoint)
    one.stop()


def loop():
    one.stop()
    time.sleep(1)


# function to stop the robot on exiting with CTRL+C
def stop_and_exit(sig, frame):
    global my_thread, chart_plotter
    global stop_execution
    
    print("Exiting application")
    stop_execution = True
    my_thread.stop()
    my_thread.join()
    one.stop()
    time.sleep(0.01)
    chart_plotter.close_plot()
    sys.exit(0)

signal.signal(signal.SIGINT, stop_and_exit)

def main():
    setup()


if __name__ == "__main__":
    main()
