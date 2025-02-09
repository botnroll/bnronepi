"""
This test version of PID control uses real speeds in mm per second
For that it needs the methods in ControlUtils class
"""

import time
import signal
from onepi.one import BnrOneA
from onepi.utils.pid_params import PidParams
from onepi.utils.pid_controller import PidController
from onepi.utils.control_utils import ControlUtils
import csv

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A+

pid_params = PidParams()

MIN_SPEED_MMPS = -850
MAX_SPEED_MMPS = 850

update_time_ms = 100

right_pid_controller = PidController(pid_params, MIN_SPEED_MMPS, MAX_SPEED_MMPS)
left_pid_controller = PidController(pid_params, MIN_SPEED_MMPS, MAX_SPEED_MMPS)
cut = ControlUtils()

timestamp = 0


def print_value(text, value):
    print(text, value)


def print_pair(text, value1, value2):
    print(text, value1, ", ", value2)


def test_pid():
    global right_pid_controller
    global left_pid_controller
    global cut
    left_power = 0
    right_power = 0
    count = 0
    time_previous = time.time()
    while count < 50:
        count = count + 1
        left_encoder = one.read_left_encoder()
        left_power = left_pid_controller.compute_output(left_encoder)

        right_encoder = one.read_right_encoder()
        right_power = right_pid_controller.compute_output(right_encoder)

        time_now = time.time()

        time_elapsed_ms = int((time_now - time_previous) * 1000)
        if time_elapsed_ms < 100:
            time.sleep((100-time_elapsed_ms)/1000.0)
            time_elapsed_ms = int((time.time() - time_previous) * 1000)
        time_previous = time.time()
        print(
            "setpoint, right_encoder, right_power, elapsed_time_ms",
            right_pid_controller.get_setpoint(),
            right_encoder,
            int(right_power),
            time_elapsed_ms,
            "ms"
        )
        
        one.move(0, right_power)


def setup():
    global right_pid_controller, left_pid_controller
    global cut, update_time_ms
    one.stop()
    one.min_battery(9.6)

    one.lcd1("  PID Control")
    one.lcd2("______v1.0______")
    time.sleep(1)  # ms
    one.reset_left_encoder()
    one.reset_right_encoder()

    while(True):
        ref_speed_mmps = 400
        num_pulses = cut.compute_pulses_from_speed(ref_speed_mmps, update_time_ms)
        print("setpoint pulses:", int(num_pulses))
        right_pid_controller.change_setpoint(num_pulses)
        left_pid_controller.change_setpoint(num_pulses)
        test_pid()

        ref_speed_mmps = 800
        num_pulses = cut.compute_pulses_from_speed(ref_speed_mmps, update_time_ms)
        print("setpoint pulses:", int(num_pulses))
        right_pid_controller.change_setpoint(num_pulses)
        left_pid_controller.change_setpoint(num_pulses)
        test_pid()

    one.stop()


def loop():
    one.stop()
    time.sleep(1)


data = []


def write_to_csv():
    global data

    with open("step_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def change_setpoint(ref_speed_mmps):
    global update_time_ms
    global data, cut, timestamp

    num_pulses = cut.compute_pulses_from_speed(ref_speed_mmps, update_time_ms)
    print("setpoint pulses:", int(num_pulses))
    right_pid_controller.change_setpoint(num_pulses)  # min 10, max 70
    input_data = num_pulses
    # compute pid
    right_power = 0
    for i in range(0, 50):

        right_encoder = one.read_right_encoder()
        right_power = right_pid_controller.compute_output(right_encoder)
        data.append([timestamp, input_data, right_encoder])
        timestamp += 100
        time.sleep(update_time_ms / 1000.0)

        one.move(0, right_power)


def step_response():
    one.reset_right_encoder()
    change_setpoint(0)
    change_setpoint(200)
    change_setpoint(0)
    one.stop()
    write_to_csv()


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    # step_response()
    setup()
    # while True:
    #    loop()


if __name__ == "__main__":
    main()
