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
from onepi.one import BnrOneAPlus


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    one = BnrOneAPlus(0, 0)  # object to control Bot'n Roll ONE A+
    one.stop()  # stop motors
    one.set_min_battery_V(9.5)  # set minimum value for battery
    battery = one.read_battery()
    print("battery:", battery)
    left_power = 0
    right_power = 0
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
            one.move_raw(left_power, right_power)
            one.lcd1("Bat:", str(battery))
            one.lcd2(left_power, right_power)
            print(
                "Battery:",
                battery,
                "\tPower left:",
                left_power,
                "\tPower right:",
                right_power,
                end="         \r",
            )

        button = one.read_button()
        if button == 1:
            left_power += 1
            right_power += 1

        elif button == 2:
            left_power -= 1
            right_power -= 1

        elif button == 3:
            print(
                "Battery:", battery, "\tPower left:", left_power, "\tPower right:", right_power
            )
            one.stop()
            left_power = 0
            right_power = 0
            one.lcd1("  Stop motors   ")
            one.lcd2("                ")
            time.sleep(2 / 1000)

        if button != 0:
            while one.read_button() != 0:
                time.sleep(10 / 1000)


if __name__ == "__main__":
    main()
