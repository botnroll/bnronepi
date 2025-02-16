# This tools allows you to control the robot using a joystick attached to the raspberry pi
# By using the joystick controllers you can control the robot in real time
# The estimated motion of the robot is plotted on the stage, which you can
# see in the screen on a separate figure

import signal
import time

from onepi.utils.joystick_reader import JoystickReader
from onepi.utils.control_utils import ControlUtils, PoseSpeeds, WheelSpeeds
from onepi.utils.drive_pid import DrivePid
from onepi.utils.pose_tracker import PoseTracker
from onepi.utils.stage import Stage
from onepi.one import BnrOneAPlus

def main():
    joystick_reader = JoystickReader()
    cut = ControlUtils()
    drive_pid = DrivePid()
    pose_tracker = PoseTracker()
    stage = Stage()

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

        left_encoder, right_encoder = drive_pid.move(apply_filter(wheel_speeds.left), apply_filter(wheel_speeds.right))
        pose = pose_tracker.update_location(left_encoder, right_encoder)
        stage.update_pose(pose)

        # There's a bug in that when using combined linear and angular speed the stage shows the robot turning the oposite way

        print(f"linear: {linear_speed:.2f}, angular: {angular_speed:.2f}, \
                left: {wheel_speeds.left:.2f}, right: {wheel_speeds.right:.2f}, \
                pose: {pose.x_mm:.0f}, {pose.y_mm:.0f}, {pose.theta_rad:.2f},", end='         \r')

        time.sleep(0.1)


if __name__ == "__main__":
    main()