import psutil
import time
import subprocess
import setproctitle
import os

class MonitorBnrOneA:

    _BNR_ONE_A_PROCESS_NAME = "BnrOneA" # The name of the process to be monitored
    _MONITOR_BNR_PROCESS_NAME ="MonitorBnr" # The name of the monitor process
    _MONITOR_BNR_PATH = "monitorbnr.py" # The path to the MonitorBNR executable
    
    def __init__(self):
        """
        Initialize the monitor with process names and the path to the MonitorBNR executable.
        """
        self.bnr_one_a_running = False  # Track the state of BnrOneA

    def is_process_running(self, process_name):
        """
        Check if a process with the given name is running.
        """
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return True
        return False

    def start_monitor_bnr(self):
        """
        Start the MonitorBNR process.
        """
        try:
            subprocess.Popen(["python3", f"{os.path.dirname(__file__)}/{self._MONITOR_BNR_PATH}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setpgrp)
        except Exception as e:
            print(f"Failed to start {self._MONITOR_BNR_PROCESS_NAME}: {e}")

    def monitor(self):
        """
        Monitor the processes and take action based on their status.
        """
        
        from onepi.one import BnrOneA       # The import of the library must be inside this function in order to avoid ciruclar imports
        
        while True:
            # Check if BnrOneA is running
            if self.is_process_running(self._BNR_ONE_A_PROCESS_NAME):
                if not self.bnr_one_a_running: # If BnrOneA is running and the flag is not set, set the flag and print a message
                    print(f"{self._BNR_ONE_A_PROCESS_NAME} started.")
                    self.bnr_one_a_running = True
            else:
                if self.bnr_one_a_running:  # If BnrOneA is not running and the flag is set, reset the flag, stops the robot and prints on the LCD
                    print(f"{self._BNR_ONE_A_PROCESS_NAME} ended.")
                    self.bnr_one_a_running = False
                    one = BnrOneA(0, 0, monitor = 0)  # object variable to control the Bot'n Roll ONE A
                    one.stop()  # Stop the Robot
                    one.lcd2("Python Code Stop")  # Print on the LCD
                    del one # Delete the object to free the SPI communication

            time.sleep(1)

if __name__ == "__main__":
    # Initialize the monitor
    monitor = MonitorBnrOneA()
    setproctitle.setproctitle(monitor._MONITOR_BNR_PROCESS_NAME)
    monitor.monitor()