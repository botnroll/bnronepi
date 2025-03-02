import psutil
import time
import subprocess
import setproctitle
import os


class Monitor:
    """
    This class monitors the BnrOneAPlus process and takes action based on its status.
    It provides the following functionalities:
    1. Check if the BnrOneAPlus process is already running.
        This can be used by the parent process to decide if it should continue running or stop.
    2. Start the Monitor process.
    3. Stop the robot if the BnrOneAPlus process ends.
    """

    _PROCESS_NAME = "BnrOneAPlus"  # name of the process to be monitored
    _MONITOR_NAME = "BnrMonitor"  # name of the monitor process
    _MONITOR_PATH = "monitor.py"  # path to the Monitor

    def __init__(self):
        """
        Initialize the monitor
        """
        self.onepi_running = False  # Track the state of onepi

    def is_process_running(self, process_name):
        """
        Check if a process with the given name is running.
        """
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] == process_name:
                return True
        return False

    def start_monitor(self):
        """
        Start the Monitor process.
        """
        try:
            subprocess.Popen(
                ["python3", f"{os.path.dirname(__file__)}/{self._MONITOR_PATH}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except Exception as e:
            print(f"Failed to start {self._MONITOR_NAME}: {e}")

    def monitor(self):
        """
        Monitor the processes and take action based on their status.
        """

        while True:
            # Check if BnrOneAPlus is running
            if self.is_process_running(self._PROCESS_NAME):
                if not self.onepi_running:
                    print(f"{self._PROCESS_NAME} started.")
                    self.onepi_running = True
            else:
                if self.onepi_running:
                    print(f"{self._PROCESS_NAME} ended.")
                    self.onepi_running = False

                    # Import here to avoid circular import
                    from onepi.one import BnrOneAPlus

                    one = BnrOneAPlus(0, 0, monitor=0)
                    one.stop()
                    one.lcd2("Python Code Stop")
                    del one  # free the SPI communication

            time.sleep(1)


if __name__ == "__main__":
    # Initialize the monitor
    monitor = Monitor()
    setproctitle.setproctitle(monitor._PROCESS_NAME)
    monitor.monitor()
