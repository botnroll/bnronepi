"""
Test line detector
"""

from line_detector import LineDetector
import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()


def test_line_detector():
    line_detector = LineDetector()
    print("No line present")
    sensor_readings = [10] * 8
    line = line_detector.compute_line(sensor_readings)
    print("sensor_readings: ", sensor_readings, "Line = ", line)
    assert line < -99
    print("Line on the centre")
    sensor_readings[3:5] = [800, 800]
    line = line_detector.compute_line(sensor_readings)
    print("sensor_readings: ", sensor_readings, "Line = ", line)
    assert -10 < line < 10


def line_position(line_detector, index, value):
    print(">> Index =", index)
    sensor_readings = [10] * 8
    sensor_readings[index] = value
    line = line_detector.compute_mean_gaussian(sensor_readings)
    print("sensor_readings: ", sensor_readings, "Line = ", line)


def test_compute_mean_gaussian():
    line_detector = LineDetector()
    for i in range(8):
        line_position(line_detector, i, 800)


def discretize_gaussian(mean, std, num_values=8):
    # Generate 8 evenly spaced values
    values = np.linspace(1000, 8000, num_values)

    # Calculate the probabilities for each value based on the Gaussian distribution
    probabilities = np.exp(-0.5 * ((values - mean) / std) ** 2)

    # Normalize the probabilities so that they sum up to 1
    probabilities /= np.sum(probabilities)
    probabilities *= 1e3
    return values, probabilities.astype(int).tolist()


def test_discretise_gaussian():
    # Example usage
    mean = 5000
    std = 600
    num_values = 8

    values, probabilities = discretize_gaussian(mean, std, num_values)
    print("Probab:", probabilities)


def plot_bar(probabilities, title):
    plt.clf()
    categories = ["0", "1", "2", "3", "4", "5", "6", "7"]
    plt.bar(categories, probabilities)
    # plt.hist(probabilities, bins=8, edgecolor="black")
    # Set labels and title
    plt.xlabel("Line sensor")
    plt.ylabel("Reading")
    plt.title(title)
    plt.ylim(0, 1200)
    plt.draw()
    plt.pause(0.01)


def test_compute_line_from_gaussian():
    line_detector = LineDetector()
    # mean = 5000
    std = 600
    num_values = 8

    for mean in range(0, 10000, 100):
        values, probabilities = discretize_gaussian(mean, std, num_values)
        # line = line_detector.compute_mean_gaussian(probabilities)
        line = line_detector.compute_line(probabilities)
        print("Line = ", int(line), "\treadings: ", probabilities)
        plot_bar(probabilities, "Line = " + str(int(line)))


def test_normalise_line_value():
    line_detector = LineDetector()
    for val in range(0, 8100, 100):
        normalised_value = int(line_detector.normalise_line_value(val, 8))
        print("val", val, "normalised_value", normalised_value)


def main():
    # test_compute_mean_gaussian()
    # test_compute_line_from_gaussian()
    test_normalise_line_value()


if __name__ == "__main__":
    main()
