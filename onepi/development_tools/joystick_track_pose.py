import signal
import time

from onepi.utils.joystick_reader import JoystickReader
from onepi.utils.control_utils import ControlUtils, PoseSpeeds, WheelSpeeds
from onepi.utils.drive_pid import DrivePid
from onepi.one import BnrOneA

def main():
    joystick_reader = JoystickReader()
    cut = ControlUtils()
    drive_pid = DrivePid()

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        drive_pid.stop()
        time.sleep(0.01)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    def apply_filter(speed):
        if abs(speed) < 50:
            speed = 0
        return speed


    while True:
        # get joystick values
        linear_speed, angular_speed = joystick_reader.get_axis_values()

        max_linear_speed = 500   #mm per sec
        max_angular_speed = 3.14 #rads per sec

        # invert signs and normalise to real speeds
        linear_speed *= -max_linear_speed
        angular_speed *= -max_angular_speed

        # convert from pose speeds to wheel speeds
        wheel_speeds = cut.compute_wheel_speeds(linear_speed, angular_speed)

        drive_pid.move(apply_filter(wheel_speeds.left), apply_filter(wheel_speeds.right))

        print(f"linear: {linear_speed:.2f}, angular: {angular_speed:.2f}, \
                left: {wheel_speeds.left:.2f}, right: {wheel_speeds.right:.2f}", end='         \r')
        
        time.sleep(0.1)


if __name__ == "__main__":
    main()