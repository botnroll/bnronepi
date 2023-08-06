"""
Test BnrOneA class
"""

import time
from onepi import BnrOneA
from line_detector import LineDetector
from test_line_detector import plot_bar


def test_read_line():
    one = BnrOneA(0, 0)
    line_detector = LineDetector()
    while True:
        sensor_readings = one.read_line_sensors()
        line = line_detector.compute_line(sensor_readings)
        # line = line_detector.compute_mean_gaussian(sensor_readings)
        # line_detector.load_if_necessary()
        # sensor_readings = line_detector.normalise_readings(sensor_readings)
        # line = line_detector.filter_line_value(line)
        print("line:", int(line), "\treadings", sensor_readings)
        plot_bar(sensor_readings, "Line: " + str(int(line)))
        # time.sleep(0.300)


def main():
    test_read_line()


if __name__ == "__main__":
    main()
