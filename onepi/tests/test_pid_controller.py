import time
from onepi.one import BnrOneA
from onepi.utils.pid_controller import PIDController

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

kp = 0.02
ki = 0.7
kd = 0.03
right_pid_controller = PIDController(kp, ki, kd, -800, 800)
left_pid_controller = PIDController(kp, ki, kd, -800, 800)


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
    left_power = 0
    right_power = 0
    count = 0
    while count < 50:
        count = count + 1
        #left_encoder = one.read_left_encoder()
        #left_encoder = maybe_change_sign(left_encoder, left_power)
        #left_power = left_pid_controller.compute_output(left_encoder)

        right_encoder = one.read_right_encoder()
        #right_encoder = maybe_change_sign(right_encoder, right_power)
        right_power = right_pid_controller.compute_output(right_encoder)

        one.move(0, right_power)
        time.sleep(0.1)  # ms

        # print_pair("left_encoder, leftPower: ", left_encoder, int(left_power))
        print_pair("right_encoder, right_power: ", right_encoder, int(right_power))


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

    set_speed = 30
    setpoint = set_speed * 10 # emulate conversion from speed to encoder readings
    print("setpoint:", setpoint)
    left_pid_controller.change_set_point(setpoint)
    right_pid_controller.change_set_point(setpoint)
    test_pid()
    one.stop()


def loop():
    one.stop()
    time.sleep(1)


def main():
    setup()
    #while True:
    #    loop()


if __name__ == "__main__":
    main()
