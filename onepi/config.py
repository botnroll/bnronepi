"""
Config module to store variables for the operation of BotnRoll One A.
Some variables are read from config files.
Other variables are computed from values read from config files.
These variables work like static variables.
You can read, modify them in the code and then save the relevant ones
in a file for next time.
"""

import json


class Config:
    """
    Saves and load config values to and from file
    """

    sensor_min = [0] * 8  # array of 8 elements with min value for each line sensor
    sensor_max = [1000] * 8  # array of 8 elements with max value for each line sensor
    threshold = 50
    cfg_file = None

    def __init__(self, filename=None):
        if filename is None:
            self.cfg_file = "config.json"
        else:
            self.cfg_file = filename

    def load(self):
        with open(self.cfg_file) as f:
            data = json.load(f)

        # Access values from the JSON file
        self.sensor_min = data["sensor_min"]
        self.sensor_max = data["sensor_max"]
        self.threshold = data["threshold"]

    def print(self):
        print("sensor_max:", self.sensor_max)
        print("sensor_min:", self.sensor_min)
        print("threshold:", self.threshold)

    def save(self):
        # Save the updated dictionary back to the JSON file
        data = {
            "sensor_max": self.sensor_max,
            "sensor_min": self.sensor_min,
            "threshold": self.threshold,
        }

        with open(self.cfg_file, "w") as f:
            json.dump(data, f, indent=4)  # Optional: indent for pretty formatting


def main():
    cfg = Config()
    cfg.save()
    cfg.load()
    cfg.print()
    cfg.save()
    cfg.print()


if __name__ == "__main__":
    main()
