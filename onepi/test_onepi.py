"""
Test BnrOneA class
"""

import time
from onepi import BnrOneA


def test_read_line():
    one = BnrOneA(0, 0)
    while True:
        sensor_readings = one.read_line_sensors()
        # line = one.read_line()
        line = one.()
        print("sensor_readings", sensor_readings, "line:", line)
        # one.lcd1(str(line[0]), str(line[1]), str(line[2]), str(line[3]))
        # one.lcd2(line[4], line[5], line[6], line[7])
        time.sleep(0.300)


def main():
    test_read_line()


if __name__ == "__main__":
    main()
