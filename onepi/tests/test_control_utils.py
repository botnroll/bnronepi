from onepi.utils.simple_timer import SimpleTimer

import os
import sys
import time

from onepi.utils.robot_params import RobotParams
from onepi.utils.control_utils import (
    cap_to_limits,
    Pose,
    PoseSpeeds,
    WheelSpeeds,
    ControlUtils,
)

# these steps are necessary in order to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)


def test_cap_to_limits():
    assert cap_to_limits(10, 0, 20) == 10
    assert cap_to_limits(-10, 0, 20) == 0
    assert cap_to_limits(30, 0, 20) == 20
    assert (
        cap_to_limits(10, 20, 0) == 0
    )  # although not logical, it is a valid test case
    assert (
        cap_to_limits(-10, 20, 0) == 0
    )  # although not logical, it is a valid test case


def test_convert_range():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert cut.convert_range(50, 0, 100, 0, 10) == 5
    assert cut.convert_range(50, 0, 100, 10, 0) == 5
    assert cut.convert_range(50, 0, 100, 0, -10) == -5
    assert cut.convert_range(50, 0, 100, -10, 0) == -5
    assert cut.convert_range(50, 0, 100, -10, 10) == 0
    assert cut.convert_range(50, 0, 100, 10, -10) == 0


def test_compute_rev_from_pulses():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_rev_from_pulses(0), 2) == 0
    assert round(cut.compute_rev_from_pulses(200), 2) == 0.09
    assert round(cut.compute_rev_from_pulses(1000), 2) == 0.44
    assert round(cut.compute_rev_from_pulses(2000), 2) == 0.89
    assert round(cut.compute_rev_from_pulses(2251), 2) == 1.00


def test_compute_distance_from_rev():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_distance_from_rev(0.0), 1) == 0.0
    assert round(cut.compute_distance_from_rev(0.5), 1) == 99.0
    assert round(cut.compute_distance_from_rev(1), 1) == 197.9
    assert round(cut.compute_distance_from_rev(50), 1) == 9896.0
    assert round(cut.compute_distance_from_rev(100), 1) == 19792.0
    assert round(cut.compute_distance_from_rev(3000), 1) == 593761.0
    assert round(cut.compute_distance_from_rev(-10), 1) == -1979.2
    assert round(cut.compute_distance_from_rev(-300), 1) == -59376.1
    assert round(cut.compute_distance_from_rev(-3000), 1) == -593761.0


def test_compute_distance_from_pulses():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_distance_from_pulses(0), 1) == 0.0
    assert round(cut.compute_distance_from_pulses(1125), 1) == 98.9
    assert round(cut.compute_distance_from_pulses(2251), 1) == 197.9
    assert round(cut.compute_distance_from_pulses(112550), 1) == 9896.0
    assert round(cut.compute_distance_from_pulses(225100), 1) == 19792.0
    assert round(cut.compute_distance_from_pulses(6753000), 1) == 593761.0
    assert round(cut.compute_distance_from_pulses(-22510), 1) == -1979.2
    assert round(cut.compute_distance_from_pulses(-675300), 1) == -59376.1
    assert round(cut.compute_distance_from_pulses(-6753000), 1) == -593761.0


def compute_speed_from_distance():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_speed_from_distance(0, 1000), 1) == 0.0
    assert round(cut.compute_speed_from_distance(1, 1000), 1) == 1.0
    assert round(cut.compute_speed_from_distance(10, 1000), 1) == 10.0
    assert round(cut.compute_speed_from_distance(500, 1000), 1) == 500.0
    assert round(cut.compute_speed_from_distance(-1, 1000), 1) == -1.0
    assert round(cut.compute_speed_from_distance(-10, 1000), 1) == -10.0
    assert round(cut.compute_speed_from_distance(-100, 1000), 1) == -100.0
    assert round(cut.compute_speed_from_distance(-500, 1000), 1) == -500.0


def compute_speed_from_pulses():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_speed_from_pulses(0, 1000), 1) == 0.0
    assert round(cut.compute_speed_from_pulses(1125.5, 1000), 1) == 99.0
    assert round(cut.compute_speed_from_pulses(2251, 1000), 1) == 192.9
    assert round(cut.compute_speed_from_pulses(112550, 1000), 1) == 9896.0
    assert round(cut.compute_speed_from_pulses(225100, 1000), 1) == 19792.0
    assert round(cut.compute_speed_from_pulses(6753000, 1000), 1) == 593761.0
    assert round(cut.compute_speed_from_pulses(-22510, 1000), 1) == -1979.2
    assert round(cut.compute_speed_from_pulses(-675300, 1000), 1) == -59376.1
    assert round(cut.compute_speed_from_pulses(-6753000, 1000), 1) == -593761.0


def test_compute_distance_from_speed():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_distance_from_speed(0, 1000), 1) == 0.0
    assert round(cut.compute_distance_from_speed(1, 1000), 1) == 1.0
    assert round(cut.compute_distance_from_speed(10, 1000), 1) == 10.0
    assert round(cut.compute_distance_from_speed(500, 1000), 1) == 500.0
    assert round(cut.compute_distance_from_speed(-1, 1000), 1) == -1.0
    assert round(cut.compute_distance_from_speed(-10, 1000), 1) == -10.0
    assert round(cut.compute_distance_from_speed(-100, 1000), 1) == -100.0
    assert round(cut.compute_distance_from_speed(-500, 1000), 1) == -500.0


def test_compute_revolutions_from_distance():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_revolutions_from_distance(0.0), 2) == 0.0
    assert round(cut.compute_revolutions_from_distance(99.0), 2) == 0.5
    assert round(cut.compute_revolutions_from_distance(197.9), 2) == 1.0
    assert round(cut.compute_revolutions_from_distance(9896.0), 2) == 50.0
    assert round(cut.compute_revolutions_from_distance(19792.0), 2) == 100.0
    assert round(cut.compute_revolutions_from_distance(593761.0), 2) == 3000.0
    assert round(cut.compute_revolutions_from_distance(-1979.2), 2) == -10.0
    assert round(cut.compute_revolutions_from_distance(-59376.1), 2) == -300.0
    assert round(cut.compute_revolutions_from_distance(-593761.0), 2) == -3000.0

    # compute_revolutions_from_distance

    # compute_arc_length

    # compute_pulses_from_rev

    # compute_pulses_from_speed

    # compute_pulses_from_distance

    # compute_pulses_from_angle_and_curvature

    # convert_to_mmps

    # convert_to_percentage

    # compute_pose_speeds

    # compute_wheel_speeds

    # compute_speeds_rpm


def main():
    print("Run tests using: pytest", os.path.basename(__file__), "-s")


if __name__ == "__main__":
    main()
