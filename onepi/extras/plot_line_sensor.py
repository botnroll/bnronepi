"""
Read line sensor from robot and display readings in a bar chart
To perform this test, connect Raspberry pi to BotnRoll One via spi interface
and use a white paper with a strip of black tape to simulate a line.
Place the line sensor of the robot on top of the black strip and
visualise the readings and line output in the chart
"""

from onepi import BnrOneA
from utils.line_detector import LineDetector
import matplotlib.pyplot as plt

plt.ion()


def plot_bar(readings, title):
    """
    plots readings in a bar chart
    """
    plt.clf()
    categories = range(len(readings))
    plt.bar(categories, readings)
    plt.xlabel("Line sensor")
    plt.ylabel("Reading")
    plt.title(title)
    plt.ylim(0, 1200)
    plt.draw()
    plt.pause(0.01)


def plot_line_sensor():
    """
    Gets sensor readings from the robot and displays them in a bar chart
    It also computes the line location and displays it in the title
    """
    one = BnrOneA(0, 0)
    line_detector = LineDetector()
    while True:
        # Check for key press
        key_events = plt.ginput(n=1, timeout=0.001)
        if key_events:
            key, _ = key_events[0]
            if key == "q" or "Q" or "Esc" or ".":  # Exit loop when 'q' key is pressed
                break
        sensor_readings = one.read_line_sensors()
        line = line_detector.compute_line(sensor_readings)
        print("Line = ", int(line), "\treadings: ", sensor_readings)
        plot_bar(sensor_readings, "Line = " + str(int(line)))


def main():
    """
    Read line sensor from robot and display readings in a bar chart
    """
    plot_line_sensor()


if __name__ == "__main__":
    main()
