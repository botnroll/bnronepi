"""
 Latest update: 30-08-2023

 This code example is in the public domain.
 http://www.botnroll.com

Calibration of Line sensor
The calibration routine is called in Setup()
Reads and stores the maximum and minimum value for every sensor on vectors
sensor_value_max[8] and sensor_value_min[8].
Low values for white and high values for black.
The user is presented with the options:
- simple calibration
- full calibration
The simple calibration only updates the maximum and minimum values for each sensor.
The full calibration also updates the threshold (THRESHOLD) and correction factor.
The transition value from white to black (THRESHOLD) is defined by the user:
  THRESHOLD is the lowest value above which a colour is considered black.
  By default is suggested the highest of the lower values.
  THRESHOLD should be as low as possible as long as it assures a safe
  transition from white to black.

To calibrate place the robot over the line with the line at the centre of the sensor.
The robot rotates for a few seconds acquiring the 8 sensor max and min values.

The registered values are displayed on the LCD.
Use the push buttons to see more values.

If you have chosen the full calibration then you can define the
THRESHOLD value. To do that you are asked to check the sensor values on a
white background at different places on the track..
Take note of the highest value and give it some margin.
Set the THRESHOLD by pressing PB1 and PB2 on the robot.
Once finish, proceed to calibrate the correction factor.
Place the robot centred on top of the black line and press a button to start.
The robot rotates left and right until it finds the right value.
After that the robot stops. You can repeat the calibration otherwise if you
chose to finish the calibration is automatically saved to the config file.
"""

import json
import os
import time
from onepi.one import BnrOneA
from onepi.utils.config import Config
from onepi.utils.line_detector import LineDetector

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A


M1 = 1  # Motor1
M2 = 2  # Motor2
VMAX = 1000

line_detector = LineDetector()


def wait_button_press():
    while one.read_button() == 0:
        time.sleep(0.050)


def wait_button_release():
    while one.read_button() != 0:
        time.sleep(0.050)


def prepare_calibration():
    """
    Initial instructions so that the user places the robot safely
    on a flat surface ready to rotate on spot
    """
    print("Place robot on the floor ready to rotate on the spot")
    print("Press a button when ready")
    one.lcd1(" Press a button ")
    one.lcd2("  to calibrate  ")
    wait_button_press()
    one.lcd1(" Release button ")
    one.lcd2("   to start     ")
    print("Release the button to start calibration")
    time.sleep(1)
    wait_button_release()
    print("Calibration Started!")
    one.lcd1("  Calibration   ")
    one.lcd2("   started!     ")


def save_config():
    """
    Saves configuration to default file
    """
    global line_detector
    cfg = Config()
    cfg.sensor_min = line_detector._config.sensor_min
    cfg.sensor_max = line_detector._config.sensor_max
    cfg.threshold = line_detector._config.threshold
    cfg.correction_factor = line_detector._config.correction_factor
    cfg.save()
    cfg.print()


def calibrate_min_max():
    """
    Finds the min and max value for each sensor
    """
    global line_detector
    print("Computing min and max for sensor readings...")
    sensor_value_min = [1024] * 8
    sensor_value_max = [0] * 8
    one.move(5, -5)
    start_time = time.time()
    while time.time() < (start_time + 3):
        readings = one.read_line_sensors()
        print("Readings: ", readings)
        for i in range(8):
            if readings[i] > sensor_value_max[i]:
                sensor_value_max[i] = readings[i]
            if readings[i] < sensor_value_min[i]:
                sensor_value_min[i] = readings[i]
        print("Max: ", sensor_value_max)
        print("Min: ", sensor_value_min)
        time.sleep(0.050)
    one.stop()
    print("Done")

    line_detector._config = Config()
    line_detector._config.load()  # loads default values
    line_detector._config.sensor_max = sensor_value_max
    line_detector._config.sensor_min = sensor_value_min
    line_detector._cfg_loaded = True
    line_detector._scaling_factor = line_detector._calculate_factors(
        line_detector._ref_max,
        line_detector._config.sensor_min,
        line_detector._config.sensor_max,
    )


def update_lcd_info(info, value_1, value_2, value_3, value_4):
    """
    Updates lcd info and waits for user to press and release a button
    """
    one.lcd1(info)
    one.lcd2(value_1, value_2, value_3, value_4)
    print("Press and release button to continue")
    wait_button_press()
    wait_button_release()


def display_calibration(sensor_value_min, sensor_value_max):
    """
    Displays calibration data on the lcd
    """
    one.lcd1("                ")
    one.lcd2(" Press a button ")
    wait_button_press()
    wait_button_release()

    update_lcd_info(
        "Max1  2   3   4 ",
        sensor_value_max[0],
        sensor_value_max[1],
        sensor_value_max[2],
        sensor_value_max[3],
    )

    update_lcd_info(
        "Max5  6   7   8 ",
        sensor_value_max[4],
        sensor_value_max[5],
        sensor_value_max[6],
        sensor_value_max[7],
    )

    update_lcd_info(
        "Min1  2   3   4 ",
        sensor_value_min[0],
        sensor_value_min[1],
        sensor_value_min[2],
        sensor_value_min[3],
    )

    update_lcd_info(
        "Min5  6   7   8 ",
        sensor_value_min[4],
        sensor_value_min[5],
        sensor_value_min[6],
        sensor_value_min[7],
    )


def take_note_of_threshold():
    """
    During this stage user should test the robot on white surface and make note of the highest reading.
    That value will be necessary to adjust the threshold if necessary in the next stage
    """
    global line_detector
    one.lcd1(" Test THRESHOLD ")
    one.lcd2(" on white color ")
    print("Test threshold on white color. Make note of the highest value.")
    print("Press and release a button to continue")
    wait_button_press()
    wait_button_release()
    print("When ready, please press a button to go to next stage.")
    while one.read_button() == 0:
        readings = one.read_line_sensors()
        normalised = line_detector._normalise_readings(readings)
        one.lcd1(normalised[0], normalised[1], normalised[2], normalised[3])
        one.lcd2(normalised[4], normalised[5], normalised[6], normalised[7])
        time.sleep(0.100)


def adjust_threshold():
    """
    This step is optional. The threshold is calculated automatically
    but if you want to make your own adjustment this allows you to do it.
    """
    global line_detector
    print("Use PB1 and PB2 to increase or decrease the threshold.")
    print("Use PB3 when ready to save result.")
    threshold = line_detector._config.threshold
    one.lcd1("  PB1++  PB2-- ")
    one.lcd2("threshold:", threshold)
    wait_button_release()
    button = 0
    while button != 3:
        button = one.read_button()
        if button == 1:
            threshold += 10
            one.lcd2("threshold:", threshold)
            time.sleep(0.100)
        if button == 2:
            threshold -= 10
            one.lcd2("threshold:", threshold)
            time.sleep(0.100)

    line_detector._config.threshold = threshold
    print("line_detector._config.threshold = ", line_detector._config.threshold)
    wait_button_release()


def left_side_correction_factor():
    global line_detector
    line_value = 0
    one.move(5, -5)
    while line_value > -100:
        readings = one.read_line_sensors()
        line_value = line_detector.compute_line(readings)
        print("Line:", line_value)
    for i in range(10):
        line_value = line_detector.compute_line(readings)
        if line_value > -100:
            line_detector._config.correction_factor += 1
            one.stop()
            return False
        else:
            time.sleep(0.2)
    one.stop()
    return True


def right_side_correction_factor():
    global line_detector
    line_value = 0
    one.move(-5, 5)
    while line_value < 100:
        readings = one.read_line_sensors()
        line_value = line_detector.compute_line(readings)
        print("Line:", line_value)
    for i in range(10):
        line_value = line_detector.compute_line(readings)
        if line_value < 100:
            line_detector._config.correction_factor += 1
            one.stop()
            return False
        else:
            time.sleep(0.2)
    one.stop()
    return True


def calibrate_correction_factor():
    """
    
    """
    global line_detector
    print("Place robot centred on a black line")
    one.lcd1("  Centre robot  ")
    one.lcd2("Any key to start")
    wait_button_release()
    wait_button_press()
    wait_button_release()
    one.move(5, -5)
    line_detector._config.correction_factor = 0
    right_side_ok = False
    left_side_ok = False
    while not left_side_ok or not right_side_ok:
        left_side_ok = left_side_correction_factor()
        right_side_ok = right_side_correction_factor()
    one.stop()
    print("Calibration of correction factor done.")
    one.lcd1("   Factor OK    ")
    one.lcd2("                ")
    time.sleep(1)


def calibration_done():
    print("Calibration Done!")
    one.lcd1("Calibration Done")
    one.lcd2("                ")
    time.sleep(2)


def display_menu():
    print("If you wish to repeat press PB1 or PB2 on the robot.")
    print("If you wish to continue press PB3.")
    one.lcd1("Repeat: PB1,PB2")
    one.lcd2("Continue: PB3   ")
    wait_button_press()


def calibrate_line(full_calibration=False):
    """
    Performs the calibration in 1 (simple) or 3 (full) main steps:
    1. calibrate_min_max to find the minimum and maximum values for each sensor
    2. adjust_threshold to manually set the value of the threshold to distinguish black and white
    3. adjust_correction_factor to manually set the value of the correction factor to eliminate
     problematic readings at extremities of the line sensor
    """
    global line_detector
    prepare_calibration()
    while one.read_button() != 3:
        calibrate_min_max()
        display_calibration(
            line_detector._config.sensor_min, line_detector._config.sensor_max
        )
        display_menu()

    if full_calibration:
        # full calibration: threshold and correction factor
        wait_button_release()
        while one.read_button() != 3:
            take_note_of_threshold()
            adjust_threshold()
            display_menu()

        # calibration of correction factor
        wait_button_release()
        while one.read_button() != 3:
            calibrate_correction_factor()
            display_menu()

    save_config()
    calibration_done()


def view_calibration():
    """
    Reads and prints saved config values on the terminal
    """
    cfg = Config()
    cfg.load()
    cfg.print()


def full_calibration():
    """
    Asks user to choose between simple or full calibration
    """
    one.lcd1("PB1: Simple")
    one.lcd2("PB2: Full")
    wait_button_release()
    wait_button_press()
    if one.read_button() == 2:
        one.lcd1("                ")
        time.sleep(1)
        return True
    one.lcd2("                ")
    time.sleep(1)
    return False


def setup():
    one.stop()  # stop motors
    one.min_battery(10.5)  # safety voltage for discharging the battery
    time.sleep(1)
    do_full_calibration = full_calibration()
    calibrate_line(do_full_calibration)  # calibrate line sensor
    view_calibration()  # read calibration values from file


def loop():
    line = int(one.read_line())  # Read line
    one.lcd1("     Line:")  # Print values on the LCD
    one.lcd2("      ", line)  # Print values on the LCD
    time.sleep(0.05)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
