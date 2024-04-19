"""
This example shows how to use a PID controller to control the wheel speeds of Bot'n Roll ONE A
The minimum speed is about 250 mm/s and the max speed is 850 mm/s for a reference battery of 12V.
Note that these values might change depending on the battery you're using and its current charge.
You can specify your own PID params, kp, ki, kd.
This example uses the default values and an update period of 200ms.
Note if you change the update period you need to tune the PID params.
"""

from onepi.utils.pid_controller import PIDController
from onepi.utils.control_utils import ControlUtils
from onepi.utils.simple_timer import SimpleTimer
from onepi.one import BnrOneA

import time

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

# Define variables
left_speed = 0
right_speed = 0
previous_left_speed = 0
previous_right_speed = 0
milliseconds_update = 200

AXIS_LENGHTH_MM = 163.0
WHEEL_DIAMETER_MM = 65.0
TICKS_PER_REV = 1490
MIN_SPEED_MMPS = 0
MAX_SPEED_MMPS = 850

left_pid = PIDController(0.5, 0, 0)
right_pid = PIDController(0.5, 0, 0)
cut = ControlUtils(AXIS_LENGHTH_MM, WHEEL_DIAMETER_MM, TICKS_PER_REV)


def print_pair(text, value1, value2):
    """
    prints pair of values
    """
    print(text, value1, ",", value2)


def print_value(text, value):
    """
    prints value
    """
    print(text, value)

def maybe_set_to_zero(current, previous):
    """
    detects when current value is of different sign from previous
    returns 0 if they are of different sign
    returns current value otherwise
    """
    if (current * previous) < 0:
        return 0  # return 0 as there was a change of sign
    return current


def compute_left_speed():
    """
    computes left speed
    """
    global left_speed, previous_left_speed
    left_encoder = one.read_left_encoder()
    left_encoder = cut.maybe_change_sign(left_encoder, left_speed, previous_left_speed)
    previous_left_speed = left_speed
    left_speed = left_pid.compute_output(left_encoder)
    left_speed = maybe_set_to_zero(left_speed, previous_left_speed)
    print("left_speed = ", left_speed)
    return left_speed


def compute_right_speed():
    """
    computes right speed
    """
    global right_speed, previous_right_speed
    right_encoder = one.read_right_encoder()
    right_encoder = cut.maybe_change_sign(
        right_encoder, right_speed, previous_right_speed
    )
    previous_right_speed = right_speed
    right_speed = right_pid.compute_output(right_encoder)
    right_speed = maybe_set_to_zero(right_speed, previous_right_speed)
    return right_speed


def update_speeds():
    """
    update wheel speeds
    """
    global left_speed
    global right_speed
    left_speed = compute_left_speed()
    right_speed = compute_right_speed()
    one.move(left_speed, right_speed)


def convert_to_mmps(desired_speed):
    """
    converts desired speed in percentage to real speed in mmps
    """
    if desired_speed == 0:
        return 0

    if desired_speed < 0:
        return cut.convert_range(
            desired_speed, -100, 0, -MAX_SPEED_MMPS, -MIN_SPEED_MMPS
        )

    if desired_speed > 0:
        return cut.convert_range(desired_speed, 0, 100, MIN_SPEED_MMPS, MAX_SPEED_MMPS)
    
    return 0

def test_move():
    print("wait 2s")
    time.sleep(2)
    # after 2s change the setpoint speed
    print("==== change setpoint ====")
    desired_speed = 2
    desired_speed_mmps = convert_to_mmps(desired_speed)
    print ("desired_speed_mmps= ", desired_speed_mmps)
    ref_ticks = cut.compute_ticks_from_speed(desired_speed_mmps, milliseconds_update)
    left_pid.change_set_point(ref_ticks)
    right_pid.change_set_point(ref_ticks)
    print_value("ref_ticks: ", ref_ticks)
    time.sleep(3)
    print("==== done ====")
    
def setup():
    """
    setup method
    """
    one.stop()
    one.min_battery(10.5)
    one.lcd1("....MovePID.....")
    one.lcd2(".....Start......")

    desired_speed = 20
    desired_speed_mmps = convert_to_mmps(desired_speed)
    print("desired_speed_mmps= ", desired_speed_mmps)
    ref_ticks = cut.compute_ticks_from_speed(desired_speed_mmps, milliseconds_update)
    left_pid.change_set_point(ref_ticks)
    right_pid.change_set_point(ref_ticks)

    print_value("ref_ticks: ", ref_ticks)
    time.sleep(0.5)
    one.reset_left_encoder()
    one.reset_right_encoder()
    my_timer = SimpleTimer(increment=milliseconds_update/1000.0, function=update_speeds)
    my_timer.start()
    test_move()
    my_timer.stop()


def loop():
    """
    loop method
    """
    one.stop()


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()