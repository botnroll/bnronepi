"""
Test line detector
test_compute_line tests the public interface of the line detector class
When developing your own application you should only use the public methods.
All the other tests in this file are testing the private methods.
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


def test_normalise():
    line_detector = LineDetector()
    normalised_reading = line_detector._normalise(50, 20, 1.5)
    expected = 45
    assert normalised_reading == expected
    normalised_reading = line_detector._normalise(0, 20, 1.5)
    expected = -30
    assert normalised_reading == expected
    normalised_reading = line_detector._normalise(-20, 20, 1.5)
    expected = -60
    assert normalised_reading == expected
    normalised_reading = line_detector._normalise(20, 20, 1.5)
    expected = 0
    assert normalised_reading == expected

def test_normalise_readings():
    print("test_normalise_readings")
    line_detector = LineDetector()
    file_name = "test_cfg.json"
    cfg_file = os.path.join(os.path.dirname(__file__), file_name)
    line_detector._config.cfg_file = cfg_file
    line_detector._load_if_necessary()  # depends on config values
    readings = [222, 333, 444, 555]
    normalised_readings = line_detector._normalise_readings(readings)
    expected = [305, 665, 360, 510]
    assert normalised_readings == expected


def test_load_if_necessary():
    print("test_load_if_necessary")
    line_detector = LineDetector()
    file_name = "test_cfg.json"
    cfg_file = os.path.join(os.path.dirname(__file__), file_name)
    line_detector._config.cfg_file = cfg_file
    line_detector._load_if_necessary()  # depends on config values
    # after loading it should have the
    # min_values, max_values and scaling factors
    assert line_detector._config.sensor_min == [100, 200, 300, 300]
    assert line_detector._config.sensor_max == [500, 400, 700, 800]
    assert line_detector._scaling_factor == [2.5, 5.0, 2.5, 2.0]


def test_compute_line_value():
    print("test_compute_line_value")
    line_detector = LineDetector()
    # first we need to load config values
    file_name = "test_cfg.json"
    cfg_file = os.path.join(os.path.dirname(__file__), file_name)
    line_detector._config.cfg_file = cfg_file
    line_detector._load_if_necessary()
    readings = [0, 0, 700, 0]
    line = line_detector._compute_line_value(readings)
    assert line == 2500


def test_cap_value():
    print("test_cap_value")
    line_detector = LineDetector()
    # test below min
    capped = line_detector._cap_value(10, 20, 100)
    assert capped == 20
    # test above max
    capped = line_detector._cap_value(130, 20, 100)
    assert capped == 100
    # test within range
    capped = line_detector._cap_value(60, 20, 100)
    assert capped == 60


def test_convert_range():
    print("test_convert_range")
    line_detector = LineDetector()
    converted = line_detector._convert_range(20, 0, 100, -100, 0)
    assert converted == -80


def test_normalise_line_value():
    print("test_normalise_line_value")
    line_detector = LineDetector()
    input_values = [0, 4000, 8000]
    expected_values = [-100, 0, 100]
    for value, expected in zip(input_values, expected_values):
        normalised_value = int(line_detector._normalise_line_value(value, 8))
        assert normalised_value == expected


def test_filter_line_value():
    print("test_filter_line_value")
    line_detector = LineDetector()
    # first we need to load config values
    file_name = "test_cfg.json"
    cfg_file = os.path.join(os.path.dirname(__file__), file_name)
    line_detector._config.cfg_file = cfg_file
    line_detector._load_if_necessary()
    # test valid reading
    filtered = line_detector._filter_line_value(200, 2000, 4000)
    assert filtered == 200
    # test no line detected
    filtered = line_detector._filter_line_value(-1, 2000, 4000)
    assert filtered == 0
    # test invalid value
    line_detector._filter_line_value(3600, 2000, 4000)
    filtered = line_detector._filter_line_value(-10, 2000, 4000)
    assert filtered == 3600
    # test invalid value above max
    line_detector._filter_line_value(2400, 2000, 4000)
    filtered = line_detector._filter_line_value(6000, 2000, 4000)
    assert filtered == 2400
    # test no line detected
    filtered = line_detector._filter_line_value(3700, 2000, 4000)
    filtered = line_detector._filter_line_value(-1, 2000, 4000)
    assert filtered == 4000


def test_compute_mean_gaussian():
    print("test_compute_mean_gaussian")
    line_detector = LineDetector()
    sensor_readings = [10] * 8
    sensor_readings[2] = 600
    line = line_detector._compute_mean_gaussian(sensor_readings)
    assert int(line) == 2679


def test_get_max_value_and_index():
    print("test_get_max_value_and_index")
    line_detector = LineDetector()
    readings = [4, 8, 6, 2]
    max_value, index = line_detector._get_max_value_and_index(readings)
    assert max_value == 8
    assert index == 1


def test_prune():
    print("test_prune")
    line_detector = LineDetector()
    # first we need to load config values
    file_name = "test_cfg.json"
    cfg_file = os.path.join(os.path.dirname(__file__), file_name)
    line_detector._config.cfg_file = cfg_file
    line_detector._load_if_necessary()
    # test normal case where max is not on the extremety
    readings = [4, 8, 6, 2]
    pruned = line_detector._prune(readings)
    assert pruned == [4, 8, 6, 2]
    # test edge case where max is at the start
    readings = [8, 3, 6, 2]
    pruned = line_detector._prune(readings)
    assert pruned == [18, 3, 6, 2]
    # test edge case where max is at the end
    readings = [8, 3, 6, 12]
    pruned = line_detector._prune(readings)
    assert pruned == [8, 3, 6, 18]


def test_compute_line():
    """
    Test the public interface compute_line
    """
    print("test_compute_line")
    line_detector = LineDetector()
    # first we need to set config values
    line_detector._config.sensor_min = [0] * 4
    line_detector._config.sensor_max = [1000] * 4
    line_detector._scaling_factor = [1] * 4
    line_detector._cfg_loaded = True
    # No line present
    sensor_readings = [10] * 4
    line = line_detector.compute_line(sensor_readings)
    assert line < -99
    # Line at the centre
    sensor_readings[1:3] = [800, 800]
    line = line_detector.compute_line(sensor_readings)
    assert -10 < line < 10
    # Line on the right side
    sensor_readings = [10] * 4
    sensor_readings[2] = 800
    line = line_detector.compute_line(sensor_readings)
    assert 20 < line < 30
    # Line not found
    sensor_readings = [10] * 4
    line = line_detector.compute_line(sensor_readings)
    assert line == 100
    # Line on the left side
    sensor_readings = [10] * 4
    sensor_readings[1] = 800
    line = line_detector.compute_line(sensor_readings)
    assert line < 50


def main():
    print("Run tests using: pytest", os.path.basename(__file__), "-s")


if __name__ == "__main__":
    main()
