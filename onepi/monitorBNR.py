import psutil
import time
import subprocess
import setproctitle
import os

class MonitorBnrOneA:

    _BNR_ONE_A_PROCESS_NAME = "BnrOneA"
    _MONITOR_BNR_PROCESS_NAME ="MonitorBnr"
    _MONITOR_BNR_PATH = "monitorbnr.py"
    
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
            # print(f"Started {os.path.dirname(__file__)}/{self._MONITOR_BNR_PATH}.")
        except Exception as e:
            # print(f"Failed to start {self._MONITOR_BNR_PROCESS_NAME}: {e}")
            pass

    def monitor(self):
        """
        Monitor the processes and take action based on their status.
        """
        
        from onepi.one import BnrOneA       # The import of the library must be inside this function in order to avoid ciruclar imports
        
        while True:
            # Check if BnrOneA is running
            if self.is_process_running(self._BNR_ONE_A_PROCESS_NAME):
                if not self.bnr_one_a_running:
                    print(f"{self._BNR_ONE_A_PROCESS_NAME} started.")
                    self.bnr_one_a_running = True
            else:
                if self.bnr_one_a_running:
                    print(f"{self._BNR_ONE_A_PROCESS_NAME} ended.")
                    self.bnr_one_a_running = False
                    one = BnrOneA(0, 0, monitor = 0)  # object variable to control the Bot'n Roll ONE A
                    one.stop()
                    one.lcd2("Python Code Stop")
                    del one

            time.sleep(1)

if __name__ == "__main__":
    # Initialize the monitor
    monitor = MonitorBnrOneA()
    setproctitle.setproctitle(monitor._MONITOR_BNR_PROCESS_NAME)
    monitor.monitor()