# This file contains a class to provide a localisation in terms of coordinates x, y
# given the wheel encoder readings. It needs to be initialised with robot params.

from onepi.utils.robot_params import RobotParams
from onepi.utils.control_utils import Pose, ControlUtils

class Odometry:
    '''
    Provides the localisation in x,y coordinates after having the wheel encoder readings
    '''

    def __init__(self, initial_pose=Pose(), robot_params=RobotParams()):
        self._robot_params = robot_params
        self._cut = ControlUtils(robot_params)
        self._pose = initial_pose

    def update_location(self, left_encoder, right_encoder):
        left_distance_mm = self._cut.compute_distance_from_pulses(left_encoder)
        right_distance_mm = self._cut.compute_distance_from_pulses(right_encoder)
        # calculate the average distance travelled
        delta_distance_mm = (right_distance_mm + left_distance_mm) / 2.0
        # calculate the change in orientation
        delta_theta_rad = (right_distance_mm - left_distance_mm) / float(self._robot_params.axis_length_mm)
        # update the pose
        self._pose.update_pose(delta_distance_mm, delta_theta_rad)
        return self._pose
    
    def get_pose(self):
        return self._pose

    def reset_pose(self, new_pose=Pose()):
        self._pose = new_pose


# Example of using the class
def main():
    
    odom = Odometry()
    pose = odom.get_pose()
    
    def print_pose():
        print("(x, y, theta) = ", int(pose.x_mm), int(pose.y_mm), int(pose.theta_rad * 100) / 100.0)
      
    # move forward
    pose = odom.update_location(3500, 3500)
    print_pose()
    # rotate cw
    pose = odom.update_location(900, -900)
    print_pose()
    # move backwards
    pose = odom.update_location(-3500, -3500)
    print_pose()
    # rotate ccw
    pose = odom.update_location(-900, 900)
    print_pose()
    

if __name__ == "__main__":
    main()