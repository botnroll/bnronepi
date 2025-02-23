# This tools allows you to control the robot using a joystick attached to the raspberry pi
# By using the joystick controllers you can control the robot in real time
# The estimated motion of the robot is plotted on the stage, which you can
# see in the screen on a separate figure

import signal
import time

from onepi.utils.joystick_reader import JoystickReader
from onepi.utils.control_utils import ControlUtils, PoseSpeeds, WheelSpeeds
from onepi.utils.pose_tracker import PoseTracker
from onepi.utils.stage import Stage
from onepi.one import BnrOneAPlus

def main():
    joystick_reader = JoystickReader()
    cut = ControlUtils()
    pose_tracker = PoseTracker()
    stage = Stage()
    one = BnrOneAPlus()

    MIN_SPEED_RPM = 40
    MAX_LINEAR_SPEED_RPM = 150   #mm per sec
    MAX_ANGULAR_SPEED_RPM = 3.14/5.0 #rads per sec

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.01)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    def apply_filter(speed):
        if abs(speed) < MIN_SPEED_RPM:
            speed = 0
        return speed


    while True:
        # get joystick values
        linear_speed, angular_speed = joystick_reader.get_axis_values()

        # invert signs and normalise to real speeds
        linear_speed *= -MAX_LINEAR_SPEED_RPM
        angular_speed *= -MAX_ANGULAR_SPEED_RPM

        # convert from pose speeds to wheel speeds
        wheel_speeds = cut.compute_wheel_speeds(linear_speed, angular_speed)

        left_encoder, right_encoder = one.move_rpm_get_encoders(
            apply_filter(wheel_speeds.left), apply_filter(wheel_speeds.right))
         
        pose = pose_tracker.update_location(left_encoder, right_encoder)
        stage.update_pose(pose)

        print(f"linear: {linear_speed:.2f}, angular: {angular_speed:.2f}, \
                left_encoder: {left_encoder:.2f}, right_encoder: {right_encoder:.2f}, \
                left: {wheel_speeds.left:.2f}, right: {wheel_speeds.right:.2f}, \
                pose: {pose.x_mm:.0f}, {pose.y_mm:.0f}, {pose.theta_rad:.2f},", end='         \r')

        time.sleep(0.1)


if __name__ == "__main__":
    main()