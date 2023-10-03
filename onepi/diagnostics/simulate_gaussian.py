"""
Test line detector
"""

from onepi.utils.line_detector import LineDetector
import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()


def discretize_gaussian(mean, std, num_bins=8):
    """
    Creates a discrete gaussian curve with a given number of bins
    given a mean value and standard deviation
    """
    # Generate 8 evenly spaced values
    values = np.linspace(1000, 8000, num_bins)

    # Calculate the probabilities for each value based on the Gaussian distribution
    probabilities = np.exp(-0.5 * ((values - mean) / std) ** 2)

    # Normalize the probabilities so that they sum up to 1
    probabilities /= np.sum(probabilities)
    probabilities *= 1e3
    return values, probabilities.astype(int).tolist()


def plot_bar(probabilities, title):
    """
    Plots probabilities in a bar chart
    """
    plt.clf()
    categories = range(len(probabilities))
    plt.bar(categories, probabilities)
    plt.xlabel("Line sensor")
    plt.ylabel("Reading")
    plt.title(title)
    plt.ylim(0, 1200)
    plt.draw()
    plt.pause(0.01)


def compute_line_from_gaussian():
    """
    Computes and plots a discrete gaussian curve with mean ranging from 0 to 10000
    and a constant standart deviation
    """
    line_detector = LineDetector()
    std = 600
    num_values = 8
    for mean in range(0, 10000, 100):
        values, probabilities = discretize_gaussian(mean, std, num_values)
        # line = line_detector.compute_mean_gaussian(probabilities)
        line = line_detector.compute_line(probabilities)
        print("Line = ", int(line), "\treadings: ", probabilities)
        plot_bar(probabilities, "Line = " + str(int(line)))


def main():
    compute_line_from_gaussian()


if __name__ == "__main__":
    main()
