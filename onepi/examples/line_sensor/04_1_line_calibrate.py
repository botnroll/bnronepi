"""
 This code example is in the public domain.
 http://www.botnroll.com

Line sensor calibrate
The calibrate routine is called in Setup()
Reads and stores the maximum and minimum value for every sensor on vectors sensor_value_max[8] and sensor_value_min[8].
Low values for white and high values for black.
The transition value from white to black (THRESHOLD) is defined by the user:
  THRESHOLD is the lowest value above white colour that can be considered black.
  By default is suggested the highest of the lower values.
  THRESHOLD should be as low as possible as long as it assures a safe transition from white to black.
Stores the values on EEPROM so they can be used in your programs after robot restart.

To calibrate place the robot over the line with the line at the centre of the sensor.
The robot rotates during 4 seconds acquiring the 8 sensor max and min values.

The registered values are displayed on the LCD. Use the push buttonons to see more values.
Calibration ends after you define THRESHOLD value.
In order to adjust THRESHOLD, sensor reading values should be analysed in real time and at different places on the track.
"""

import json
import os
import time
from one import BnrOneA
from utils.config import Config

one = BnrOneA(0, 0)  # declaration of object variable to control the Bot'n Roll ONE A


M1 = 1       # Motor1
M2 = 2       # Motor2
VMAX = 1000

sensor_value_min = [1023] * 8
sensor_value_max = [0] * 8
sensor_factor = [0] * 8

THRESHOLD = 50  # Line follower limit between white and black

cfg = Config()

def wait_button_press():
    while one.read_button() == 0:
        time.sleep(0.050)

def wait_button_release():
    while one.read_button() != 0:
        time.sleep(0.050)

def calibrate_line():
    one.lcd1(" Press a buttonon ")
    one.lcd2("  to calibrate  ")
    wait_button_press()
    print("Calibrate Starting!")
    one.lcd1("  Calibration   ")
    one.lcd2("   starting     ")
    time.sleep(1)

    wait_button_release()

    # Calibrate for 4 seconds
    one.move(5, -5)
    start_time = time.time()
    while time.time() < (start_time + 10):
        print("Val: ")
        for i in range(8):
            sensor_value = one.read_adc(i)
            if sensor_value > sensor_value_max[i]:
                sensor_value_max[i] = sensor_value
            if sensor_value < sensor_value_min[i]:
                sensor_value_min[i] = sensor_value
            print(sensor_value)
        print("Max: ")
        for i in range(8):
            print(sensor_value_max[i])

        print("Min: ")
        THRESHOLD = 0
        for i in range(8):
            print(sensor_value_min[i])
            if sensor_value_min[i] > THRESHOLD:
                THRESHOLD = sensor_value_min[i]
        time.sleep(0.050)

    print("THRESHOLD:", THRESHOLD)
    one.stop()

    # Write values on file
    cfg.sensor_min = sensor_value_min
    cfg.sensor_max = sensor_value_max
    cfg.threshold = THRESHOLD
    # cfg.correction_factor = 6
    cfg.save()

    print("Calibrate Done! Press a button...")
    one.lcd1(" Calibration done ")
    one.lcd2(" Press a buttonon ")
    while(one.read_button() != 3):
        one.lcd1("Max1  2   3   4 ")
        one.lcd2(sensor_value_max[0], sensor_value_max[1], sensor_value_max[2], sensor_value_max[3])
        wait_button_release()
        wait_button_press()
        one.lcd1("Max5  6   7   8 ")
        one.lcd2(sensor_value_max[4], sensor_value_max[5], sensor_value_max[6], sensor_value_max[7])
        wait_button_release()
        wait_button_press()
        one.lcd1("Min1  2   3   4 ")
        one.lcd2(sensor_value_min[0], sensor_value_min[1], sensor_value_min[2], sensor_value_min[3])
        wait_button_release()
        wait_button_press()
        one.lcd1("Min5  6   7   8 ")
        one.lcd2(sensor_value_min[4],sensor_value_min[5],sensor_value_min[6],sensor_value_min[7])
        wait_button_release()
        wait_button_press()
        one.lcd1("  Test THRESHOLD   ")
        one.lcd2(" on white color ")
        wait_button_press()
        wait_button_release()
        wait_button_press()
        while one.read_button() == 0:
            for i in range(8):
                sensor_value[i] = one.read_adc(i)
            one.lcd1(sensor_value[0] - sensor_value_min[0], sensor_value[1] - sensor_value_min[1], sensor_value[2] - sensor_value_min[2], sensor_value[3] - sensor_value_min[3])
            one.lcd2(sensor_value[4] - sensor_value_min[4], sensor_value[5] - sensor_value_min[5], sensor_value[6] - sensor_value_min[6], sensor_value[7] - sensor_value_min[7])
            time.sleep(0.100)
        one.lcd1("  PB1++  PB2-- ")
        one.lcd2("   THRESHOLD:", THRESHOLD)
        wait_button_release()
        button = 0
        while button != 3:
            button = one.read_button()
            if button == 1:
                THRESHOLD += 10
                one.lcd2("   THRESHOLD:", THRESHOLD)
                time.sleep(0.100)
            if button == 2:
                THRESHOLD -= 10
                one.lcd2("   THRESHOLD:", THRESHOLD)
                time.sleep(0.100)
        EEPROM.write(eepromADD, highByte(THRESHOLD))
        eepromADD += 1
        EEPROM.write(eepromADD, lowByte(THRESHOLD))
        eepromADD -= 1
        one.lcd1("PB1=AdjustTHRESHOLD")
        one.lcd2("PB3=end")
        wait_button_release()
        wait_button_press()
    one.lcd1("Calibration Done!")
    time.sleep(2)


def setup_line():
    global THRESHOLD
    cfg.load()
    cfg.print()

    THRESHOLD = cfg.threshold
    print("THRESHOLD: ", THRESHOLD)

    for i in range(8):
        # Calculate factor for each sensor
        sensor_factor[i] = VMAX / (sensor_value_max[i] - sensor_value_min[i])

def setup():
    one.stop()                  # stop motors
    one.min_battery(10.5)       # safety voltage for discharging the battery
    time.sleep(1)
    calibrate_line()            # calibrate line sensor
    setup_line()                # read line calibration values from file


def loop():
    line = one.read_line()      # Read line
    print(" Line:", line)
    one.lcd1("     Line:")      # Print values on the LCD
    one.lcd2("      ", line)    # Print values on the LCD
    time.sleep(0.05)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
