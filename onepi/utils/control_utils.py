"""
Collection of utility methods to perform useful conversions and calculations
"""

from onepi.utils.robot_params import RobotParams
import math


def cap_to_limits(value, min_value, max_value):
    """
    Cap input value within the given min and max limits
    """
    value = max(value, min_value)
    value = min(max_value, value)
    return value


class Pose:
    """
    Pose definition. Contains x, y and theta coordinates in a 2D coordinate system
     x coordinate points forward
     y coordinate points left
     theta_rad orientation positive direction is counterclockwise
    """

    x_mm = 0
    y_mm = 0
    theta_rad = 0

    def __init__(self, x_mm_in=0, y_mm_in=0, theta_rad_in=0):
        self.x_mm = x_mm_in
        self.y_mm = y_mm_in
        self.theta_rad = theta_rad_in

    def update_pose(self, delta_distance_mm, delta_theta_rad):
        self.x_mm += delta_distance_mm * math.cos(
            self.theta_rad + delta_theta_rad / 2.0
        )
        self.y_mm += delta_distance_mm * math.sin(
            self.theta_rad + delta_theta_rad / 2.0
        )
        self.theta_rad += delta_theta_rad


class PoseSpeeds:
    """
    Encodes the speed of the robot in terms of linear and angular speeds
    """

    linear_mmps = 0
    angular_rad = 0

    def __init__(self, linear=0, angular=0):
        self.linear_mmps = linear
        self.angular_rad = angular


class WheelSpeeds:
    """
    Encodes the speed of the robot in terms of left and right wheel speeds
    """

    left = 0
    right = 0

    def __init__(self, left_speed=0, right_speed=0):
        self.left = left_speed
        self.right = right_speed


class ControlUtils:
    """
    collection of methods to compute speeds, distance, pulses
    """

    _axis_length_mm = 163.0
    _wheel_diameter_mm = 65.0
    _pulses_per_rev = 2240
    _max_speed_mmps = 850
    _min_speed_mmps = 0
    _spot_rotation_delta = -14.5  # For spot rotations only
    _pi = 3.14159265

    def __init__(
        self,
        params=RobotParams(),
        min_speed_mmps=0,
    ):
        """
        constructor
        """
        self._axis_length_mm = params.axis_length_mm
        self._wheel_diameter_mm = params.wheel_diameter_mm
        self._pulses_per_rev = params.pulses_per_rev
        self._max_speed_mmps = (
            params.max_speed_rpm * self._pi * self._wheel_diameter_mm / 60
        )
        self._min_speed_mmps = min_speed_mmps

    def convert_range(self, x_value, x_min, x_max, y_min, y_max):
        """
        Converts a value x given in the range [x_min : x_max]
        to a new value in the range [y_min : y_max]
        """
        x_range = x_max - x_min
        y_range = y_max - y_min

        # Avoid division by zero
        if x_range == 0:
            return y_min + y_range / 2

        # Calculate the converted value
        y = ((x_value - x_min) / x_range) * y_range + y_min
        return y

    def compute_rev_from_pulses(self, pulses):
        """
        computes the expected number of pulses given
        the number of revolutions of the wheel
        """
        return float(pulses) / self._pulses_per_rev

    def compute_distance_from_rev(self, revolutions):
        """
        computes distance given the number of revolutions
        """
        distance_mm = self._pi * float(self._wheel_diameter_mm) * revolutions
        return distance_mm

    def compute_distance_from_pulses(self, pulses):
        """
        computes distance given the number of pulses
        """
        rev = self.compute_rev_from_pulses(pulses)
        return self.compute_distance_from_rev(rev)

    def compute_speed_from_distance(self, distance_mm, time_ms):
        """
        computes speed given the distance and time
        """
        return (distance_mm * 1000) / time_ms

    def compute_speed_from_pulses(self, num_pulses, time_ms):
        """
        computes speed given the number of pulses and time
        """
        revolutions = self.compute_rev_from_pulses(num_pulses)
        distance_mm = self.compute_distance_from_rev(revolutions)
        speed_mmps = self.compute_speed_from_distance(distance_mm, time_ms)
        return speed_mmps

    def compute_distance_from_speed(self, speed_mmps, time_ms):
        """
        computes the distance given the speed and time
        """
        distance_mm = (float(speed_mmps) * time_ms) / 1000.0
        return distance_mm

    def compute_revolutions_from_distance(self, distance_mm):
        """
        computes the number of revolutions expected for the wheel
        for a given distance
        """
        perimeter_of_circle = self._pi * float(self._wheel_diameter_mm)
        revolutions = distance_mm / perimeter_of_circle
        return revolutions

    def compute_arc_length(self, angle_rad, radius_of_curvature_mm):
        """
        Computes the arc length given the angle and radius of curvature
        """
        arc_length_mm = 0.0
        if abs(radius_of_curvature_mm) > 0.1:
            arc_length_mm = angle_rad * radius_of_curvature_mm
        else:
            arc_length_mm = (
                angle_rad * float(self._axis_length_mm + self._spot_rotation_delta)
            ) / 2.0
        return arc_length_mm

    def compute_pulses_from_rev(self, revolutions):
        """
        computes the expected number of pulses given
        the number of revolutions of the wheel
        """
        return round(self._pulses_per_rev * revolutions)

    def compute_pulses_from_speed(self, speed_mmps, time_ms):
        """
        computes number of pulses given speed and time
        """
        distance_mm = self.compute_distance_from_speed(speed_mmps, time_ms)
        revolutions = self.compute_revolutions_from_distance(distance_mm)
        num_pulses = self.compute_pulses_from_rev(revolutions)
        return num_pulses

    def compute_pulses_from_distance(self, distance):
        """
        computes number of pulses given distance
        """
        revolutions = self.compute_revolutions_from_distance(distance)
        num_pulses = self.compute_pulses_from_rev(revolutions)
        return num_pulses

    def compute_pulses_from_angle_and_curvature(
        self, angle_rad, radius_of_curvature_mm=0
    ):
        """
        computes number of pulses given the angle and radius of curvature curvature
        """
        abs_angle_rad = abs(angle_rad)
        arc_length_mm = self.compute_arc_length(abs_angle_rad, radius_of_curvature_mm)
        revolutions = self.compute_revolutions_from_distance(arc_length_mm)
        num_pulses = self.compute_pulses_from_rev(revolutions)
        return num_pulses

    def convert_to_mmps(self, desired_speed_percentage):
        """
        convert speed percentage to real speed in mmps
        """
        capped_speed = cap_to_limits(desired_speed_percentage, -100, 100)
        if capped_speed < 0:
            return self.convert_range(
                capped_speed, -100, 0, -self._max_speed_mmps, -self._min_speed_mmps
            )
        if capped_speed > 0:
            return self.convert_range(
                capped_speed, 0, 100, self._min_speed_mmps, self._max_speed_mmps
            )
        return 0

    def convert_to_percentage(self, desired_speed_mmps):
        """
        convert real speed to speed percentage
        """
        capped_speed = cap_to_limits(
            desired_speed_mmps, -self._max_speed_mmps, self._max_speed_mmps
        )
        if capped_speed <= -self._min_speed_mmps:
            return self.convert_range(
                capped_speed, -self._max_speed_mmps, -self._min_speed_mmps, -100, 0
            )
        if capped_speed >= self._min_speed_mmps:
            return self.convert_range(
                capped_speed, self._min_speed_mmps, self._max_speed_mmps, 0, 100
            )
        return 0

    def compute_pose_speeds(self, left_speed, right_speed):
        """
        computes the pose speeds given left and right wheel speeds
        """
        linear = (right_speed + left_speed) / 2.0
        angular = (right_speed - left_speed) / self._axis_length_mm
        pose_speeds = PoseSpeeds(linear, angular)
        return pose_speeds

    def compute_wheel_speeds(self, linear_speed, angular_speed_rad):
        """
        Computes the wheel speeds from linear and angular speeds
        """
        wheel_speeds = WheelSpeeds()
        wheel_speeds.left = linear_speed - (
            (angular_speed_rad * self._axis_length_mm) / 2.0
        )
        wheel_speeds.right = linear_speed + (
            (angular_speed_rad * self._axis_length_mm) / 2.0
        )
        return wheel_speeds

    def compute_speeds_rpm(self, wheel_speeds_mmps: WheelSpeeds):
        """
        computes the speeds in rpm given the speeds in mm/s
        """
        left_rpm = (wheel_speeds_mmps.left * 60) / (self._wheel_diameter_mm * self._pi)
        right_rpm = (wheel_speeds_mmps.right * 60) / (
            self._wheel_diameter_mm * self._pi
        )
        return WheelSpeeds(left_rpm, right_rpm)
