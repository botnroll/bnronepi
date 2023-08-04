"""
 This code example is in the public domain. 
 http://www.botnroll.com

Description: 
 Configure the necessary power in order to move the motors for the lowest possible speed. 
 Use a fully charged battery for the configuration.
 Information is printed in the robot LCD and computer Serial monitor.
 Place the robot on a flat surface.
 Use PB1 to increase the power until the robot moves forward.
 Use PB2 to decrease the power if necessary.
 Use PB3 to store the data in EEPROM. 
Motors Calibration.
"""

import time
import onepi


def main():
    one = onepi.BnrOneA(0, 0)  # object to control Bot'n Roll ONE A
    one.stop()
    # stop motors
    # one.min_battery(9.5)
    # set minimum value for battery
    battery = one.read_battery()
    print("battery:", battery)
    powerL = 40
    powerR = 40
    button = 0
    battery = 0.0
    start_time = time.time()
    print("start_time=", start_time)
    end_time = start_time + 1
    print("end_time=", start_time)
    time.sleep(5)
    while True:
        if time.time() > end_time:
            end_time += 0.250
            battery = one.read_battery()
            one.move_calibrate(powerL, powerR)
            one.lcd1("Bat:", str(battery))
            one.lcd2(powerL, powerR)

        button = one.read_button()
        if button == 1:
            powerL += 1
            powerR += 1

        elif button == 2:
            powerL -= 1
            powerR -= 1

        elif button == 3:
            one.save_calibrate(battery, powerL, powerR)
            print("Calibration data saved:")
            one.lcd1("Calibration data")
            one.lcd2("    Saved!!!    ")
            time.sleep(2 / 1000)

        print("  Battery:", battery)
        print("  PowerL:", powerL)
        print("  PowerR:", powerR)
        print("")
        while one.read_button() != 0:
            time.sleep(50 / 1000)


if __name__ == "__main__":
    main()
