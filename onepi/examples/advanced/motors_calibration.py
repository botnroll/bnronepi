"""
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
from one import BnrOneA


def main():
    one = BnrOneA(0, 0)  # object to control Bot'n Roll ONE A
    one.stop()  # stop motors
    one.min_battery(9.5)  # set minimum value for battery
    battery = one.read_battery()
    print("battery:", battery)
    powerL = 40
    powerR = 40
    button = 0
    battery = 0.0
    start_time = time.time()
    end_time = start_time + 1
    print("Information is printed on the LCD of the robot and on the terminal.")
    print("Place the robot on a flat surface.")
    print("Use PB1 to increase the power until the robot moves forward.")
    print("Use PB2 to decrease the power if necessary.")
    print("Use PB3 to store the data in the PIC EEPROM.", end="\n\n")
    time.sleep(5)
    while True:
        if time.time() > end_time:
            end_time += 0.5
            battery = one.read_battery()
            battery = int(battery * 10) / 10
            one.move_calibrate(powerL, powerR)
            one.lcd1("Bat:", str(battery))
            one.lcd2(powerL, powerR)
            print(
                "Battery:",
                battery,
                "\tPower left:",
                powerL,
                "\tPower right:",
                powerR,
                end="\r",
            )

        button = one.read_button()
        if button == 1:
            powerL += 1
            powerR += 1

        elif button == 2:
            powerL -= 1
            powerR -= 1

        elif button == 3:
            one.save_calibrate(battery, powerL, powerR)
            print(
                "Battery:", battery, "\tPower left:", powerL, "\tPower right:", powerR
            )
            print("Calibration data saved:", " " * 20)
            one.lcd1("Calibration data")
            one.lcd2("    Saved!!!    ")
            time.sleep(2 / 1000)

        if button != 0:
            while one.read_button() != 0:
                time.sleep(10 / 1000)


if __name__ == "__main__":
    main()
