"""
This example shows how to use a PID controller to control the wheel speeds of Bot'n Roll ONE A
The minimum speed is about 250 mm/s and the max speed is 850 mm/s for a reference battery of 12V.
Note that these values might change depending on the battery you're using and its current charge.
You can specify your own PID params, kp, ki, kd.
This example uses the default values and an update period of 200ms.
Note if you change the update period you need to tune the PID params.
"""

from pid_controller import PIDController
from control_utils import ControlUtils
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
TICKS_PER_REV = 80
MIN_SPEED_MMPS = 0
MAX_SPEED_MMPS = 850

left_pid = PIDController(1.5, 0.5, 0)
right_pid = PIDController(1.5, 0.5, 0)
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


class Timer:
    """
    class to track time
    """

    def start(self, timer_interval_ms=200):
        """
        sets the timer with a specific time interval
        """
        self._interval = timer_interval_ms

    def update(self):
        """
        updates time using the time interval
        """
        self._time += self._interval

    def now(self):
        """
        returns current time
        """
        return self._time

    _time = 0
    _interval = 200


timer = Timer()


def update():
    """
    update speeds from time to time
    """
    timer.update()
    update_speeds()


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
    ref_ticks = cut.compute_ticks_from_speed(desired_speed_mmps, milliseconds_update)
    left_pid.change_set_point(ref_ticks)
    right_pid.change_set_point(ref_ticks)

    print_value("ref_ticks: ", ref_ticks)
    time.sleep(0.5)
    one.reset_left_encoder()
    one.reset_right_encoder()
    timer.start(milliseconds_update)


def loop():
    """
    loop method
    """
    time.sleep(2)
    # after 2s change the setpoint speed
    desired_speed = 1
    desired_speed_mmps = convert_to_mmps(desired_speed)
    ref_ticks = cut.compute_ticks_from_speed(desired_speed_mmps, milliseconds_update)
    left_pid.change_set_point(ref_ticks)
    right_pid.change_set_point(ref_ticks)
    print_value("ref_ticks: ", ref_ticks)
    time.sleep(3)

    # Disable Timer1 interrupt
    # TODO
    one.stop()
    while True:
        pass


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()