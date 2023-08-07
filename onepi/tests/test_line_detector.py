"""
Test line detector
"""

import sys
import os
import time
import matplotlib.pyplot as plt
import numpy as np

# these steps are necessary in order to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from utils.line_detector import LineDetector

plt.ion()


# test functions:
def test_normalise_readings():
    pass

def test_load_if_necessary():
    pass

def test_compute_line_value():
    pass

def test_cap_value():
    pass

def test_convert_range():
    pass

def test_normalise_line_value():
    line_detector = LineDetector()
    input_values = [0, 4000, 8000]
    expected_values = [-100, 0, 100]
    for value, expected in zip(input_values, expected_values):
        normalised_value = int(line_detector.normalise_line_value(value, 8))
        assert normalised_value == expected

def test_filter_line_value():
    pass

def test_compute_mean_gaussian():
    line_detector = LineDetector()
    sensor_readings = [10] * 8
    sensor_readings[2] = 600
    line = line_detector.compute_mean_gaussian(sensor_readings)
    assert int(line) == 2679

def test_get_max_value_and_index():
    pass

def test_prune():
    pass

def test_compute_line():
    line_detector = LineDetector()
    # No line present
    sensor_readings = [10] * 8
    line = line_detector.compute_line(sensor_readings)
    assert line < -99
    # Line at the centre
    sensor_readings[3:5] = [800, 800]
    line = line_detector.compute_line(sensor_readings)
    assert -10 < line < 10
    # Line on the right side
    sensor_readings = [10] * 8
    sensor_readings[5] = 800
    line = line_detector.compute_line(sensor_readings)
    assert 40 < line < 60
    # Line not found
    sensor_readings = [10] * 8
    line = line_detector.compute_line(sensor_readings)
    assert line == 100
    # Line on the left side
    sensor_readings = [10] * 8
    sensor_readings[2] = 800
    line = line_detector.compute_line(sensor_readings)
    assert line < 50

def main():
    print("Run tests using: pytest", os.path.basename(__file__), "-s")

if __name__ == "__main__":
    main()
