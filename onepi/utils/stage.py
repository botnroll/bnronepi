"""
Stage class providing a visualisation of the robot on a 'stage'
and the respective path.
"""

import os
import math
import time

import matplotlib.pyplot as plt
from PIL import Image
from onepi.utils.control_utils import Pose

class Stage:
    """
    Draws the robot on the stage.
    Allows to represent the robot path by updating the pose.
    """
    def __init__(self, x_mm=0, y_mm=0, theta_rad=0):
        self.fig, self.ax = plt.subplots()

        self.min_x_range = -500
        self.max_x_range = 500
        self.min_y_range = -500
        self.max_y_range = 500
        self.padding = 50
        self.ax.set_xlim(self.min_x_range, self.max_x_range)
        self.ax.set_ylim(self.min_y_range, self.max_y_range)

        self.x_path = []
        self.y_path = []
        self.path = self.ax.plot([], [], 'b-', zorder=1)  # Example: blue points

        # Load the image
        file_name = "botnrollOneA.png"  # Replace with actual image path
        image_path = os.path.join(os.path.dirname(__file__), file_name)
        self.image = Image.open(image_path)
        self.image = self.image.resize((100, 100))
        self.rotated_image = self.image.rotate(math.degrees(theta_rad), resample=Image.BICUBIC, expand=False)
        self.im = self.ax.imshow(self.rotated_image, zorder=2)


    def clear(self):
        """
        clean existing path off the stage
        """
        self.x_path = []
        self.y_path = []


    def update_path(self, x, y):
        """
        adds a point to the path
        """
        self.x_path.append(x)
        self.y_path.append(y)
        self.path[0].set_data(self.x_path, self.y_path)
        self.ax.relim()
        self.ax.autoscale_view()

    def resize_canvas(self, x, y):
        """
        resizes the canvas (by extending it) if necessary in case the
        new point doesn't fit inside the current dimensions
        """
        # Check if x-axis range is below minimum
        if (x - self.padding) < self.min_x_range:
            self.min_x_range = x - self.padding
        if (x + self.padding) > self.max_x_range:
            self.max_x_range = x + self.padding
        if (y - self.padding) < self.min_y_range:
            self.min_y_range = y - self.padding
        if (y + self.padding) > self.max_y_range:
            self.max_y_range = y + self.padding

        self.ax.set_xlim(self.min_x_range, self.max_x_range)
        self.ax.set_ylim(self.min_y_range, self.max_y_range)

    def update_pose(self, pose: Pose, pause_s=0.000001):
        """
        Updates the pose of the robot on the canvas
        """
        x_mm = pose.x_mm
        y_mm = pose.y_mm
        theta_rad = pose.theta_rad
        self.update_path(x_mm, y_mm)

        # Rotate the image by theta degrees
        self.rotated_image = self.image.rotate(math.degrees(theta_rad), resample=Image.BICUBIC, expand=False)

        # Display the rotated image at coordinates (x, y)
        self.im.set_data(self.rotated_image)
        self.im.set_extent([x_mm - self.rotated_image.width/2,
                            x_mm + self.rotated_image.width/2,
                            y_mm - self.rotated_image.height/2,
                            y_mm + self.rotated_image.height/2])
        self.resize_canvas(x_mm, y_mm)
        plt.pause(pause_s)


# Example of using the class
def main():
    stage = Stage()
    x = 0.0
    y = 0.0
    theta = 0.0
    for x in range(0, 300, 10):
        pose = Pose(x, y, theta)
        stage.update_pose(pose)
        time.sleep(0.01)
    for theta_x10 in range(0, 17, 1):
        theta = theta_x10 / 10.0
        pose = Pose(x, y, theta)
        stage.update_pose(pose)
        time.sleep(0.01)
    for y in range(0, 300, 10):
        pose = Pose(x, y, theta)
        stage.update_pose(pose)
        time.sleep(0.01)
    time.sleep(3)

if __name__ == "__main__":
    main()