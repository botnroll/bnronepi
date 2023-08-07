
import sys
import os

# these steps are necessary in order to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from utils.config import Config


def test_config():
    """
    Test config class and it's methods namely:
     - loading values from config file
     - saving values to config file
    """
    cfg = Config("test_cfg.json")
    print(">> Create config file")
    cfg.sensor_min = [100, 200, 300, 300]
    cfg.sensor_max = [500, 400, 700, 800]
    cfg.threshold = 18
    cfg.print()
    print(">> Saving config values into file...")
    cfg.save()
    cfg.print()
    print(">> Loading config values from file...")
    cfg.load()
    cfg.print()
    assert cfg.sensor_min == [100, 200, 300, 300]
    assert cfg.sensor_max == [500, 400, 700, 800]
    assert cfg.threshold == 18
    print(">> Changing values directly in config...")
    cfg.sensor_min = [100, 100, 100, 100]
    cfg.sensor_max = [200, 200, 200, 200]
    cfg.threshold = 22
    cfg.print()
    print(">> Assert that after loading values changed back")
    cfg.load()
    cfg.print()
    assert cfg.sensor_min == [100, 200, 300, 300]
    assert cfg.sensor_max == [500, 400, 700, 800]
    assert cfg.threshold == 18


def main():
    print("Run tests using: pytest", os.path.basename(__file__), "-s")

if __name__ == "__main__":
    main()