"""
Module that wraps the MotionGenerator module and offers predefined shapes
"""

import math
from onepi.utils.robot_params import RobotParams
from onepi.utils.control_utils import PoseSpeeds
from onepi.utils.motion_generator import MotionGenerator
from onepi.one import BnrOneAPlus


class ShapeGenerator:

    def __init__(self, one: BnrOneAPlus, slip_factor=1.0, robot_params=RobotParams()):
        self._mg = MotionGenerator(one, slip_factor, robot_params)

    def rotate_angle_deg_at_speed(
        self, angle_deg, speed=50, radius_of_curvature_mm=0, slow_down_thresh_deg=0
    ) -> PoseSpeeds:
        """
        wrapper for rotate_angle_deg_at_speed in motion_generator
        """
        self._mg.rotate_angle_deg_at_speed(
            angle_deg, speed, radius_of_curvature_mm, slow_down_thresh_deg
        )

    def move_straight_at_speed(self, distance, speed=50, slow_down_distance=0):
        """
        wrapper for move_straight_at_speed in motion_generator
        """
        self._mg.move_straight_at_speed(distance, speed, slow_down_distance)

    def rotate_90_deg_ccw(self, speed, slow_down_thresh_deg=30) -> PoseSpeeds:
        """
        generate a spot rotation of 90 degrees counterclockwise
        """
        return self._mg.rotate_angle_deg_at_speed(90, speed, 0, slow_down_thresh_deg)

    def polygon(self, side_mm, num_sides, speed=55):
        """
        describes a polygon shaped motion given the side length and the number of sides
        """
        angle_deg = 180 - ((num_sides - 2) * 180.0) / num_sides
        print("angle_deg: ", angle_deg)
        for i in range(num_sides):
            self._mg.move_straight_at_speed(side_mm, speed)
            self._mg.rotate_angle_deg_at_speed(angle_deg, speed)

    def rounded_polygon(self, side_mm, num_sides, speed=55):
        """
        describes a polygon shaped motion given the side length and the number of sides
        """
        angle_deg = 180 - ((num_sides - 2) * 180.0) / num_sides
        print("angle_deg: ", angle_deg)
        for i in range(num_sides):
            self._mg.move_straight_at_speed(side_mm, speed)
            self._mg.rotate_angle_deg_at_speed(90, speed, 80, 0)

    def triangle(self, side_mm, speed=50):
        """
        moves by decribing a triangular motion with side given as the input parameter
        """
        self.polygon(side_mm, 3, speed)

    def square(self, side_mm, speed=60):
        """
        describes a quared motion with side given as input parameter
        """
        self.polygon(side_mm, 4, speed)

    def circle(self, radius_mm, speed=60):
        """
        describes a circular motion with radius given as input parameter
        """
        self._mg.rotate_angle_deg_at_speed(360, speed, radius_mm)

    def semi_circle(self, radius_mm, speed=50):
        """
        describes a semi-circle motion with radius given as input parameter
        """
        self._mg.rotate_angle_deg_at_speed(180, speed, radius_mm)

    def _compute_fibonacci_sequence(number_of_elements):
        """
        computes a fibonacci sequence with a predetermined number of elements
        Note: number_of_elements should be more than 1
        """
        fibonacci_sequence = [1, 1]
        if number_of_elements > 2:
            for i in range(number_of_elements - 2):
                fibonacci_sequence.append(
                    fibonacci_sequence[i] + fibonacci_sequence[i + 1]
                )
        return fibonacci_sequence

    def fibonacci_spiral(self, seed_radius, num_segments, speed=50):
        """
        The fibonacci spiral changes the radius of curvature every 90 degrees
        according to the fibonacci sequence:
        1, 1, 2, 3, 5, 8, 13, ...

        The seed_radius is the initial radius of the spiral.
        num_segments specifies the number of segments of 90 degrees of the spiral.
        """
        numbers = self._compute_fibonacci_sequence(num_segments)
        for i in range(abs(num_segments)):
            radius_of_curvature = numbers[i] * seed_radius
            self._mg.rotate_angle_deg_at_speed(90, speed, radius_of_curvature)

    def archimedean_spiral(self, spiral_factor, total_angle_deg, speed=50):
        """
        The archimedean spiral has an increasing radius of curvature
        radius_of_curvature = a * theta, where a is a constant (spiral_factor)
        """
        angle_step = 5
        current_angle = 0
        for i in range(0, total_angle_deg, angle_step):
            radius_of_curvature_mm = spiral_factor * current_angle
            self._mg.rotate_angle_deg_at_speed(
                angle_step, speed, radius_of_curvature_mm
            )
            current_angle += 5

    def snake(
        self,
        length_mm=700,
        num_elements=7,
        speed=50,
        snaking_angle_deg=60,
        turning_rate_deg=0,
    ):
        """
        describes an ondulatory motion (like a snake)
        All arguments are optional.
        You can specify the length of the motion, the number of ondulatory elements and the speed.
        By adjusting the snaking angle you can tween the amplitude of the ondulatory motion.
        And by setting a turning rate you can also curve the ondulatory motion.
        By adjusting these last two parameters you can create interesting moving patterns.
        """
        secant_length = length_mm / num_elements
        theta_rad = math.radians(snaking_angle_deg)
        radius_of_curvature_mm = secant_length / (2 * math.sin(theta_rad / 2))
        self._mg.rotate_angle_deg_at_speed(-snaking_angle_deg / 2, speed)
        for i in range(num_elements):
            self._mg.rotate_angle_deg_at_speed(
                snaking_angle_deg + turning_rate_deg, speed, radius_of_curvature_mm
            )
            snaking_angle_deg = (-1) * snaking_angle_deg

    def heart(self):
        """
        example on how to set a motion with the shape of a heart
        """
        speed = 50
        self._mg.rotate_angle_deg_at_speed(45, speed)
        self._mg.move_straight_at_speed(200, speed)
        self._mg.rotate_angle_deg_at_speed(230, speed, 100)
        self._mg.rotate_angle_deg_at_speed(-180, speed)
        self._mg.rotate_angle_deg_at_speed(230, speed, 100)
        self._mg.move_straight_at_speed(230, speed)
