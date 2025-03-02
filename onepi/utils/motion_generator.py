"""
This module provides a class to enable the robot move for specified distance or
angle at a given speed. This is the stepping stone to create advanced motion
patterns such as polygons, spirals, combined motions, etc.
"""

import math
from onepi.one import BnrOneAPlus
from onepi.utils.robot_params import RobotParams
from onepi.utils.control_utils import PoseSpeeds
from onepi.utils.control_utils import ControlUtils


class MotionGenerator:
    """
    Class that enables moving in curved or straight lines by specifying the
    distance and or angle and speed of the desired motion
    """

    STRAIGHT_MOTION = 32767
    TICKS_LEFT_LOW_SPEED = 4000
    MIN_SPEED_MMPS = 100

    def __init__(self, one: BnrOneAPlus, slip_factor=1.0, robot_params=RobotParams()):
        self._slip_factor = slip_factor
        self._axis_length_mm = robot_params.axis_length_mm
        self._cut = ControlUtils(robot_params)
        self._one = one

    def _reset_encoders(self):
        """
        Resets both encoders
        """
        self._one.reset_encoders()

    def _compute_pose_speeds(self, speed, radius_of_curvature_mm, direction=1):
        """
        calculates the angular speed given the linear speed,
        the radius of curvature and the direction
        """
        linear_speed = speed
        if radius_of_curvature_mm != 0:
            if radius_of_curvature_mm == self.STRAIGHT_MOTION:  # straight motion
                angular_speed_rad = 0
                linear_speed = speed
            else:
                angular_speed_rad = direction * (speed / radius_of_curvature_mm)
        else:
            angular_speed_rad = direction * (speed / (self._axis_length_mm / 2))
            linear_speed = 0

        return PoseSpeeds(linear_speed, angular_speed_rad)

    def _maybe_slow_down(
        self,
        pose_speeds,
        speed,
        pulses_remaining,
        slow_down_thresh,
        radius_of_curvature_mm,
        direction,
    ):
        """
        Note: At the moment slowing down doesn't work for rotations only
        """
        if (
            (pulses_remaining < self.TICKS_LEFT_LOW_SPEED)
            and (pulses_remaining < slow_down_thresh)
            and (pulses_remaining > 0)
        ):
            ratio = pulses_remaining / self.TICKS_LEFT_LOW_SPEED
            slow_speed = speed * ratio
            slow_speed = max(self.MIN_SPEED_MMPS, slow_speed)  # cap to min
            print("ratio: ", ratio, " speed ", slow_speed)
            pose_speeds = self._compute_pose_speeds(
                slow_speed, radius_of_curvature_mm, direction
            )
        return pose_speeds

    def _move_and_slow_down(
        self,
        total_pulses,
        speed=50,
        direction=1,
        radius_of_curvature_mm=0,
        slow_down_thresh=TICKS_LEFT_LOW_SPEED,
    ):
        """
        @brief Moves and slows down when pulses remaining are less than slow_down_thresh
        If slow_down_thresh is set to zero (or negative number) it does not slow down.
        By default it starts slowing down when a full rotation (TICKS_LEFT_LOW_SPEED) remains.
        The slow down is a quadratic function of the form y = a * x^2

        @param total_pulses number of pulses necessary from the encoders (average) to complete the manoeuvre
        @param speed
        @param direction of curve in case of a curved motion
        @param radius_of_curvature_mm (positive for CW and negative values for CCW rotations)
        @param slow_down_thresh number of ticks to when the robot should start reducing speed
        @param straight boolean specifying if this is a straight line or not
        """

        pose_speeds = self._compute_pose_speeds(
            speed, radius_of_curvature_mm, direction
        )

        encoder_count = 0
        # print("encoder_count: ", encoder_count, " total: ", total_pulses, " slow coeff: ", coeff)

        while encoder_count < total_pulses:
            left_encoder = abs(self._one.read_left_encoder())
            right_encoder = abs(self._one.read_right_encoder())
            encoder_count += (left_encoder + right_encoder) / 2.0
            pulses_remaining = round(total_pulses - encoder_count, 0)
            print(
                "pulses_remaining",
                pulses_remaining,
                "left_enc:",
                left_encoder,
                "right_enc:",
                right_encoder,
            )
            if pulses_remaining < 0:
                break
            pose_speeds = self._maybe_slow_down(
                pose_speeds,
                pose_speeds.linear_mmps,
                pulses_remaining,
                slow_down_thresh,
                radius_of_curvature_mm,
                direction,
            )
            wheel_speeds_mmps = self._cut.compute_wheel_speeds(
                pose_speeds.linear_mmps, pose_speeds.angular_rad
            )
            wheel_speeds_rpm = self._cut.compute_speeds_rpm(wheel_speeds_mmps)
            self._one.move_rpm(wheel_speeds_rpm.left, wheel_speeds_rpm.right)

        self._one.brake(100, 100)

    def _get_sign(self, value):
        if value >= 0:
            return 1
        return -1

    def _check_wheel_speed_limit(self, speed):
        if speed > 100 or speed < -100:
            print("******** ERROR ******** speed out of limits: ", speed)

    def _check_speed_limits(self, pose_speeds: PoseSpeeds):
        wheel_speeds = self._cut.compute_wheel_speeds(
            pose_speeds.linear_mmps, pose_speeds.angular_rad
        )
        self._check_wheel_speed_limit(wheel_speeds.left)
        self._check_wheel_speed_limit(wheel_speeds.right)

    def _apply_slip(self, value):
        return round(value / self._slip_factor, 0)

    def move_straight_at_speed(self, distance, speed=50, slow_down_distance=0):
        """
        moves the robot for the given distance at the given speed.
        If slow down distance is provided then it slows down once the
        remaining distance is less than the slow_down_distance
        """
        abs_distance = abs(distance)
        abs_slow_down_distance = abs(slow_down_distance)
        total_pulses = self._cut.compute_pulses_from_distance(abs_distance)
        total_pulses = self._apply_slip(total_pulses)
        slow_down_pulses = self._cut.compute_pulses_from_distance(
            abs_slow_down_distance
        )
        self._reset_encoders()
        self._move_and_slow_down(
            total_pulses, speed, 1, self.STRAIGHT_MOTION, slow_down_pulses
        )

    def rotate_angle_deg_at_speed(
        self, angle_deg, speed=50, radius_of_curvature_mm=0, slow_down_thresh_deg=0
    ) -> PoseSpeeds:
        """
        rotate the robot the specified angle at the given speed
        and with the radius of curvature provided
        if radius_of_curvature_mm is set to STRAIGHT_MOTION
        then the robot moves in a straight line
        """
        total_pulses = self._cut.compute_pulses_from_angle_and_curvature(
            math.radians(angle_deg), radius_of_curvature_mm
        )
        total_pulses = self._apply_slip(total_pulses)
        print("total_pulses: ", total_pulses)
        slow_down_pulses_thresh = self._cut.compute_pulses_from_angle_and_curvature(
            math.radians(slow_down_thresh_deg), radius_of_curvature_mm
        )
        print("slow_down_pulses_thresh: ", slow_down_pulses_thresh)
        self._reset_encoders()
        self._move_and_slow_down(
            total_pulses,
            abs(speed),
            self._get_sign(angle_deg),
            abs(radius_of_curvature_mm),
            slow_down_pulses_thresh,
        )
