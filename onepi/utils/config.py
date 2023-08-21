"""
Config module to store variables for the operation of BotnRoll One A.
Some variables are read from config files.
Other variables are computed from values read from config files.
These variables work like static variables.
You can read, modify them in the code and then save the relevant ones
in a file for next time.
"""

import json
import os


class Config:
    """
    Saves and load config values to and from file
    """

    sensor_min = [0] * 8  # array of 8 elements with min value for each line sensor
    sensor_max = [1000] * 8  # array of 8 elements with max value for each line sensor
    threshold = 50
    correction_factor = 6
    cfg_file = None

    def __init__(self, filename=None):
        if filename is None:
            file_name = "config.json"
            self.cfg_file = os.path.join(os.path.dirname(__file__), file_name)
        else:
            self.cfg_file = filename

    def load(self):
        with open(self.cfg_file) as f:
            data = json.load(f)

        # Access values from the JSON file
        self.sensor_min = data["sensor_min"]
        self.sensor_max = data["sensor_max"]
        self.threshold = data["threshold"]
        self.correction_factor = data["correction_factor"]

    def print(self):
        print("sensor_max:", self.sensor_max)
        print("sensor_min:", self.sensor_min)
        print("threshold:", self.threshold)
        print("correction_factor:", self.correction_factor)

    def save(self):
        # Save the updated dictionary back to the JSON file
        data = {
            "sensor_max": self.sensor_max,
            "sensor_min": self.sensor_min,
            "threshold": self.threshold,
            "correction_factor": self.correction_factor,
        }

        with open(self.cfg_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


def main():
    cfg = Config()
    cfg.save()
    cfg.load()
    cfg.print()
    cfg.save()
    cfg.print()


if __name__ == "__main__":
    main()
