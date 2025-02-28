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
    assert ControlUtils.convert_range(50, 0, 100, 0, 10) == 5
    assert ControlUtils.convert_range(50, 0, 100, 10, 0) == 5
    assert ControlUtils.convert_range(50, 0, 100, 0, -10) == -5
    assert ControlUtils.convert_range(50, 0, 100, -10, 0) == -5
    assert ControlUtils.convert_range(50, 0, 100, -10, 10) == 0
    assert ControlUtils.convert_range(50, 0, 100, 10, -10) == 0


def test_compute_rev_from_pulses():
    robot_params = RobotParams(300, 161, 63, 2251)
    cut = ControlUtils(robot_params)
    assert round(cut.compute_rev_from_pulses(0), 2) == 0
    assert round(cut.compute_rev_from_pulses(200), 2) == 0.09
    assert round(cut.compute_rev_from_pulses(1000), 2) == 0.44
    assert round(cut.compute_rev_from_pulses(2000), 2) == 0.89
    assert round(cut.compute_rev_from_pulses(2251), 2) == 1.00


def test_compute_distance_from_rev():
    assert ControlUtils.compute_distance_from_rev(0, 300) == 0
    assert ControlUtils.compute_distance_from_rev(0.09, 300) == 1.41
    assert ControlUtils.compute_distance_from_rev(0.44, 300) == 6.93
    assert ControlUtils.compute_distance_from_rev(0.89, 300) == 13.86
    assert ControlUtils.compute_distance_from_rev(1.00, 300) == 15.75


def main():
    print("Run tests using: pytest", os.path.basename(__file__), "-s")


if __name__ == "__main__":
    main()
