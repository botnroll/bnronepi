import os
from onepi.utils.pose_tracker import PoseTracker
from onepi.utils.control_utils import Pose

def test_odometry():  
    pose_tracker = PoseTracker()
    pose = pose_tracker.get_pose()
    
    def print_pose():
        print("(x, y, theta) = ", pose.x_mm, pose.y_mm, pose.theta_rad)

    def round_pose():
        pose.x_mm = int(pose.x_mm)
        pose.y_mm = int(pose.y_mm)
        pose.theta_rad = int(pose.theta_rad * 100) / 100.0
    
    def assert_equal(pose_ref):
        round_pose()
        print_pose()
        assert pose.x_mm == pose_ref.x_mm
        assert pose.y_mm == pose_ref.y_mm
        assert pose.theta_rad == pose_ref.theta_rad

    
    # move forward
    print("move forward")
    pose = pose_tracker.update_location(3500, 3500)
    assert_equal(Pose(479, 0, 0.0))

    # rotate cw
    print("rotate cw")
    pose = pose_tracker.reset_pose()
    pose = pose_tracker.update_location(900, -900)
    assert_equal(Pose(0, 0, -1.51))
    
    # move backwards
    print("move backwards")
    pose = pose_tracker.reset_pose()
    pose = pose_tracker.update_location(-3500, -3500)
    assert_equal(Pose(-479, 0, 0.0))

    # rotate ccw
    print("rotate ccw")
    pose = pose_tracker.reset_pose()
    pose = pose_tracker.update_location(-900, 900)
    assert_equal(Pose(0, 0, 1.51))

    # move forward and rotate cw
    print("move forward and rotate cw")
    pose = pose_tracker.reset_pose()
    pose = pose_tracker.update_location(3500, 2000)
    assert_equal(Pose(304, -222, -1.26))
    
    # move forward and rotate ccw
    print("move forward and rotate ccw")
    pose = pose_tracker.reset_pose()    
    pose = pose_tracker.update_location(2000, 3500)
    assert_equal(Pose(304, 222, 1.26))

    # move backwards and rotate cw
    print("move backwards and rotate cw")
    pose = pose_tracker.reset_pose()
    pose = pose_tracker.update_location(-2000, -3500)
    assert_equal(Pose(-304, 222, -1.26))

    # move backwards and rotate ccw
    print("move backwards and rotate ccw")
    pose = pose_tracker.reset_pose()
    pose = pose_tracker.update_location(-3500, -2000)
    assert_equal(Pose(-304, -222, 1.26))


def main():
    """
    Calls functions to test public interface with BotnRoll One A Plus
    Most of these tests should be verified with the robot connected
    to the raspberry pi and by visually inspecting the robot and/or the terminal
    """
    print("Run tests using: pytest", os.path.basename(__file__), "-s")


if __name__ == "__main__":
    main()