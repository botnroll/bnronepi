import os
import time
from onepi.one import BnrOneA

def monitor_bnr(file_name):
    """
    This main function monitors the BnrOneA.txt file, checking the active PIDs, and cleaning the file when it stops.
    """
    pid = 0
    while True:
        try:
            print(f"Monitor attached to file: {file_name}", pid)
            while True:
                with open(f'{os.path.dirname(__file__)}/{file_name}.txt', 'r') as f: pid = int(f.read().strip())    # Read PID from the BnrOneA.txt file
                if pid > 0:         # If there is an active Process using the BotnRoll
                    print(f"Detected PID: {pid}")
                    try:
                        os.kill(pid, 0)         
                    except Exception as e:          # When the process dies
                        print(f"Process {pid} has terminated. Resetting File.", e)
                        with open(f'{os.path.dirname(__file__)}/{file_name}.txt', 'w') as f: f.write(str("0"))      # Clear File to 0
                        pid = 0
                        
                        # Creates a bnr connection, with monitor at 0, so that it doesn't get monitored
                        bnr = BnrOneA(0, 0, monitor=0)
                        bnr.stop()                         # Stops the Robot
                        bnr.lcd1(f"Botn Roll ONE A+")      # Prints on the screen LCD1
                        bnr.lcd2(f"Python Code Stop")      # Prints on the screen LCD2
                        del bnr                            # Deletes the variable bnr
                        break                              # breaks the loop to restart the moonitoring process

                time.sleep(1)   # Only reads once a second
        except Exception as e:
            print("File not found. Exiting monitor.", e)
            with open(f'{os.path.dirname(__file__)}/{file_name}.txt', 'w') as f: f.write(str("0"))

        time.sleep(1)
        
if __name__ == "__main__":
    shared_memory_name = "BnrOneA"
    monitor_bnr(shared_memory_name)
