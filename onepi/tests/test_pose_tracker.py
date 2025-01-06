import os
from onepi.utils.pose_tracker import PoseTracker

def test_odometry():  
    pose_tracker = PoseTracker()
    pose = pose_tracker.get_pose()
    
    def print_pose():
        print("(x, y, theta) = ", pose.x_mm, pose.y_mm, pose.theta_rad)

    def round_pose():
        pose.x_mm = int(pose.x_mm)
        pose.y_mm = int(pose.y_mm)
        pose.theta_rad = int(pose.theta_rad * 100) / 100.0
    
    round_pose()
    print_pose()
    
    # move forward
    pose = pose_tracker.update_location(3500, 3500)
    round_pose()
    print_pose()
    assert pose.x_mm == 479
    assert pose.y_mm == 0
    assert pose.theta_rad == 0.0

    # rotate cw
    pose = pose_tracker.update_location(900, -900)
    round_pose()
    print_pose()
    assert pose.x_mm == 479
    assert pose.y_mm == 0
    assert pose.theta_rad == -1.51

    # move backwards
    pose = pose_tracker.update_location(-3500, -3500)
    round_pose()
    print_pose()
    assert pose.x_mm == 449
    assert pose.y_mm == 478
    assert pose.theta_rad == -1.51

    # rotate ccw
    pose = pose_tracker.update_location(-900, 900)
    round_pose()
    print_pose()
    assert pose.x_mm == 449
    assert pose.y_mm == 478
    assert pose.theta_rad == 0.0


def main():
    """
    Calls functions to test public interface with BotnRoll One A Plus
    Most of these tests should be verified with the robot connected
    to the raspberry pi and by visually inspecting the robot and/or the terminal
    """
    print("Run tests using: pytest", os.path.basename(__file__), "-s")


if __name__ == "__main__":
    main()