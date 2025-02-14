"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
 Configure the necessary power (duty cycle) in order to move the motors for the lowest possible speed.
 Use a fully charged battery for the configuration.
 Information is printed on the LCD of the robot and on the terminal.
 Place the robot on a flat surface.
 Use PB1 to increase the power until the robot moves forward.
 Use PB2 to decrease the power if necessary.
 Use PB3 to store the data in the PIC EEPROM.
Motors Calibration.
"""

import time
import signal
from onepi.one import BnrOneA


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    one = BnrOneA(0, 0)  # object to control Bot'n Roll ONE A+
    one.stop()  # stop motors
    #one.set_min_battery_V(9.5)  # set minimum value for battery
    battery = one.read_battery()
    print("battery:", battery)
    
    var1 = one.read_debug(0)
    var2 = one.read_debug(1)
    var3 = one.read_debug(2)
    var4 = one.read_debug(3)
    var5 = one.read_debug_float()
    
    print("Debug:", var1, var2, var3, var4, var5)

if __name__ == "__main__":
    main()
