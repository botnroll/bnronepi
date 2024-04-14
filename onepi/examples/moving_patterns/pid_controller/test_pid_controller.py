import time
from onepi.one import BnrOneA
from pid_controller import pid_controller

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

kp = 0.65  # 2.5. error^3 -> 0.65
ki = 1.4  # 3.5
kd = 0  # 0.5
right_pid_controller = pid_controller(kp, ki, kd)
left_pid_controller = pid_controller(kp, ki, kd)


def print_value(text, value):
    print(text, value)


def print_pair(text, value1, value2):
    print(text, value1, ", ", value2)


def setup():
    global right_pid_controller
    global left_pid_controller
    one.stop()
    one.min_battery(9.6)

    one.lcd1("  PID Control")
    one.lcd2("______v1.0______")
    time.sleep(1)  # ms
    one.reset_left_encoder()
    one.reset_right_encoder()

    ref_speed = 7
    right_pid_controller.change_set_point(0)  # min 10, max 70
    left_pid_controller.change_set_point(ref_speed)


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


def loop():
    left_power = 0
    right_power = 0
    count = 0
    while count < 100:
        count += 1
        left_encoder = one.read_left_encoder()
        left_encoder = maybe_change_sign(left_encoder, left_power)
        left_power = left_pid_controller.compute_output(left_encoder)

        right_encoder = one.read_left_encoder()
        right_encoder = maybe_change_sign(right_encoder, right_power)
        right_power = right_pid_controller.compute_output(right_encoder)

        one.move(left_power, right_power)
        time.sleep(0.2)  # ms

        print_pair("left_encoder, leftPower: ", left_encoder, int(left_power))
        # print_pair("right_encoder, right_power: ", right_encoder, int(right_power))
    one.stop()
    time.sleep(1)
