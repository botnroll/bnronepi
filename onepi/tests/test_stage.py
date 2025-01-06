import time
import os
from onepi.utils.stage import Stage
from onepi.utils.control_utils import Pose

def test_stage():
    stage = Stage()
    # 1st quadrant facing east
    stage.update_pose(Pose(400,200,0.0), 1)
    # 1st quadrant facing north
    stage.update_pose(Pose(400,200,1.57), 1)
    # 1st quadrant facing west
    stage.update_pose(Pose(400,200,3.14), 1)
    # 1st quadrant facing south
    stage.update_pose(Pose(400,200,-1.57), 1)
    # 2nd quadrant facing east
    stage.update_pose(Pose(-400,200,0.0), 1)
    # 2nd quadrant facing north
    stage.update_pose(Pose(-400,200,1.57), 1)
    # 2nd quadrant facing west
    stage.update_pose(Pose(-400,200,3.14), 1)
    # 2nd quadrant facing south
    stage.update_pose(Pose(-400,200,-1.57), 1)
    # 3rd quadrant facing east
    stage.update_pose(Pose(-400,-200,0.0), 1)
    # 3rd quadrant facing north
    stage.update_pose(Pose(-400,-200,1.57), 1)
    # 3rd quadrant facing west
    stage.update_pose(Pose(-400,-200,3.14), 1)
    # 3rd quadrant facing south
    stage.update_pose(Pose(-400,-200,-1.57), 1)
    # 4th quadrant facing east
    stage.update_pose(Pose(400,-200,0.0), 1)
    # 4th quadrant facing north 3rd
    stage.update_pose(Pose(400,-200,1.57), 1)
    # 4th quadrant facing west
    stage.update_pose(Pose(400,-200,3.14), 1)
    # 4th quadrant facing south
    stage.update_pose(Pose(400,-200,-1.57), 1)

def main():
    """
    Calls functions to test public interface with BotnRoll One A Plus
    Most of these tests should be verified with the robot connected
    to the raspberry pi and by visually inspecting the robot and/or the terminal
    """
    test_stage()

if __name__ == "__main__":
    main()