"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
The robot moves and messages are printed on the LCD identifying the movements.
"""

import time
import signal
from onepi.one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


def setup():
    one.stop()  # stop motors


def loop():
    one.lcd2("    Forward ")  # print data on LCD line 2
    one.move(50, 50)  # Forward
    time.sleep(1)  # wait 1 second
    one.lcd2("     Stop   ")
    one.stop()  # Stop Motors
    time.sleep(0.5)
    one.lcd2("   Backwards ")
    one.move(-50, -50)  # Backwards
    time.sleep(1)
    one.lcd2("     Stop   ")
    one.move(0, 0)  # Stop Motors
    time.sleep(0.5)
    one.lcd2("  Rotate Right ")
    one.move(50, -50)  # Rotate Right
    time.sleep(0.5)
    one.lcd2("     Stop   ")
    one.stop()  # Stop
    time.sleep(0.5)
    one.lcd2("  Rotate Left ")
    one.move(-50, 50)  # Rotate Left
    time.sleep(0.5)
    one.lcd2("     Stop   ")
    one.stop()  # Stop Motors
    time.sleep(0.5)
    one.lcd2("    Forward ")
    one.move(100, 100)  # Forward
    time.sleep(1)
    one.lcd2("     Brake    ")
    one.brake(100, 100)  # Stop motors with torque
    time.sleep(0.8)
    one.lcd2("   Backwards ")
    one.move(-100, -100)  # Backwards
    time.sleep(1)
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
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
