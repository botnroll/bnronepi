import time
import signal
from onepi.one import BnrOneA
from onepi.utils.pid_controller import PIDController
from onepi.utils.control_utils import ControlUtils
import csv

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

kp = 1  # 2.5. error^3 -> 0.65
ki = 0.7  # 1.4   3.5
kd = 0.2  # 0.5


MIN_SPEED_MMPS = -850
MAX_SPEED_MMPS = 850

update_time_ms = 100

right_pid_controller = PIDController(kp, ki, kd, MIN_SPEED_MMPS, MAX_SPEED_MMPS)
left_pid_controller = PIDController(kp, ki, kd, MIN_SPEED_MMPS, MAX_SPEED_MMPS)
cut = ControlUtils()

timestamp = 0


def print_value(text, value):
    print(text, value)


def print_pair(text, value1, value2):
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
    global right_pid_controller
    global left_pid_controller
    global cut
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

        one.move(0, right_power)
        time.sleep(0.1)  # ms

        # print_pair("left_encoder, leftPower: ", left_encoder, int(left_power))
        print_pair("right_encoder, right_power: ", right_encoder, int(right_power))


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

    ref_speed_mmps = 200
    num_pulses = cut.compute_pulses_from_speed(ref_speed_mmps, update_time_ms)
    print("setpoint pulses:", int(num_pulses))
    right_pid_controller.change_set_point(num_pulses)  # min 10, max 70
    # left_pid_controller.change_set_point(num_pulses)
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
    right_pid_controller.change_set_point(num_pulses)  # min 10, max 70
    input_data = num_pulses
    # compute pid
    right_power = 0
    for i in range(0, 50):

        right_encoder = one.read_right_encoder()
        right_encoder = maybe_change_sign(right_encoder, right_power)
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
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    # step_response()
    setup()
    # while True:
    #    loop()


if __name__ == "__main__":
    main()
