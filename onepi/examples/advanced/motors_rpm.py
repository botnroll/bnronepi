"""
 Latest update: 23-02-2025

 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 Sets the motor moving with different wheel speeds 
 by giving commands in rpm
"""

import time
import signal
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

def setup():
    one.stop()  # stop motors

def loop():
    one.lcd2("    Forward ")  # print data on LCD line 2
    one.move_rpm(50, 50)  # Forward
    time.sleep(1.5)  # wait 1 second
    one.lcd2("     Stop   ")
    one.stop()  # Stop Motors
    time.sleep(0.5)
    one.lcd2("   Backwards ")
    one.move_rpm(-50, -50)  # Backwards
    time.sleep(1.5)
    one.lcd2("     Stop   ")
    one.move_rpm(0, 0)  # Stop Motors
    time.sleep(0.5)
    one.lcd2("  Rotate Right ")
    one.move_rpm(50, -50)  # Rotate Right
    time.sleep(1.5)
    one.lcd2("     Stop   ")
    one.stop()  # Stop
    time.sleep(0.5)
    one.lcd2("  Rotate Left ")
    one.move_rpm(-50, 50)  # Rotate Left
    time.sleep(1.5)
    one.lcd2("     Stop   ")
    one.stop()  # Stop Motors
    time.sleep(0.5)
    one.lcd2("    Forward ")
    one.move_rpm(100, 100)  # Forward
    time.sleep(1.5)
    one.lcd2("     Brake    ")
    one.brake(100, 100)  # Stop motors with torque
    time.sleep(0.8)
    one.lcd2("   Backwards ")
    one.move_rpm(-100, -100)  # Backwards
    time.sleep(1.5)
    one.lcd2("     Brake    ")
    one.brake(100, 100)  # Stop motors with torque
    time.sleep(0.8)
    one.lcd2("     Stop   ")
    one.stop()  # Stop Motors
    time.sleep(1.5)

def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
