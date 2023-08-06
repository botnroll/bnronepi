"""
Test functions to verify methods of onepi class
"""

import time
from onepi import onepi


def ms_sleep(milliseconds):
    """
    wait for the specified time in milliseconds

    :param milliseconds: time in milliseconds
    """
    time.sleep(milliseconds / 1000)


def blink(bnr_one_a, number_of_times, duration_ms):
    """
    Blinks the led on Bot'n Roll One A

    :param bnr_one_a: object to send the command to
    :param number_of_times: number of times to toggle the led
    :duration between toggling
    """
    state = 1
    for i in range(1, number_of_times + 1):
        state = i % 2
        print("LED: ", state)
        bnr_one_a.led(state)
        ms_sleep(duration_ms)


def scroll_text(text, size_of_line):
    """
    From the initial text and a specified size,
    yields a new text each time starting with an empty text
    and then shifting the text to the left
    ending with an empty text again
    :param text: input text
    :param size_of_line: size of the output text
    """
    extended_text = (" " * size_of_line) + text + (" " * size_of_line)
    for i in range(17 + len(text)):
        text = extended_text[i : i + 16]
        yield text


def test_scroll_text():
    """
    Sends scrolling text to the robot
    Text should be displayed in lcd line 2
    """
    print("=== Testing LCD scrolling text ===")
    bnr_one_a = onepi.BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0

    text = "Hi Raspberry Pi!"
    for text in scroll_text(text, 16):
        print(text, end="\n")
        bnr_one_a.lcd2(text)
        ms_sleep(200)
    print(" ")


def test_read_button():
    """
    Reads button pressed from the robot
    Note: User should press the buttons on the robot
    """
    print("=== Testing read button ===")
    bnr_one_a = onepi.BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0

    print("Please press a button on the robot")
    ms_sleep(1000)
    for i in range(20):
        print("Test", i, "/ 20. Button pressed: ", bnr_one_a.read_button())
        ms_sleep(300)


def test_lcd():
    """
    Sends different types of text using both lines of the lcd
    User should verify the output by looking at the lcd on the robot
    """
    print("=== Testing writing data to LCD ===")
    bnr_one_a = onepi.BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0

    delay_ms = 1600
    bnr_one_a.lcd1("")
    bnr_one_a.lcd2("Hi Raspberry Pi!")
    ms_sleep(delay_ms)
    bnr_one_a.lcd1("Hi Raspberry Pi!")
    bnr_one_a.lcd2("Day:", 31, "7", 2023)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1("Day:", 31, "7", 2023)
    bnr_one_a.lcd2(17, "h", 15, "min")
    ms_sleep(delay_ms)
    bnr_one_a.lcd1(17, "h", 15, "min")
    bnr_one_a.lcd2("Ver.", 1, "Sub.", 3)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1("Ver.", 1, "Sub.", 3)
    bnr_one_a.lcd2("Test number:", 1)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1("Test number:", 1)
    bnr_one_a.lcd2("System", "test:", 1)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1("System", "test:", 1)
    bnr_one_a.lcd2(1234567890123456)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1(1234567890123456)
    bnr_one_a.lcd2(12345678, 1234567)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1(12345678, 1234567)
    bnr_one_a.lcd2(12345, 12345, 1234)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1(12345, 12345, 1234)
    bnr_one_a.lcd2(1111, 2222, 3333, 4444)
    ms_sleep(delay_ms)
    bnr_one_a.lcd1(1111, 2222, 3333, 4444)
    bnr_one_a.lcd2("      END       ")
    ms_sleep(delay_ms)
    bnr_one_a.lcd1("      END       ")
    bnr_one_a.lcd2("")


def test_led():
    """
    Main method to test interface with BotnRoll One A
    """
    print("=== Testing led blinking ===")
    bnr_one_a = onepi.BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    blink(bnr_one_a, 6, 200)


def test_read_battery():
    """
    Test voltage battery reading
    """
    print("=== Testing read battery ===")
    bnr_one_a = onepi.BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Battery voltage = ", bnr_one_a.read_battery())


def test_move():
    """
    Test move method
    """
    print("=== Testing move ===")
    bnr_one_a = onepi.BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    delay_ms = 1000
    bnr_one_a.move(30, 30)
    ms_sleep(delay_ms)
    bnr_one_a.move(30, -30)
    ms_sleep(delay_ms)
    bnr_one_a.move(-30, 30)
    ms_sleep(delay_ms)
    bnr_one_a.move(-30, -30)
    ms_sleep(delay_ms)
    bnr_one_a.move(0, 0)


def move_and_stop(bnr_one_a, left_speed, right_speed, delay_ms, extra_delay_ms):
    bnr_one_a.move(left_speed, right_speed)
    ms_sleep(delay_ms)
    bnr_one_a.move(0, 0)
    ms_sleep(extra_delay_ms)


def test_move_calibrate():
    """
    Test move calibrate method
    """
    print("=== Testing move calibrate ===")
    bnr_one_a = onepi.BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    delay_ms = 1000
    print("Moving at 80% speed")
    move_and_stop(bnr_one_a, 80, 80, delay_ms, delay_ms / 4)

    print("Calibrating for 20% power on left motor. Moving at 80% speed")
    bnr_one_a.move_calibrate(20, 100)
    move_and_stop(bnr_one_a, 80, 80, delay_ms, delay_ms / 4)

    print("Calibrating for 20% power on right motor. Moving at 80% speed")
    bnr_one_a.move_calibrate(100, 20)
    move_and_stop(bnr_one_a, 80, 80, delay_ms, delay_ms / 4)


def main():
    """
    Calls functions to test public interface with BotnRoll One A
    """
    test_scroll_text()
    test_read_button()
    test_lcd()
    test_led()
    test_read_battery()

    # functions to test:
    test_move()
    test_move_calibrate()
    # move_1m(self, motor, speed):
    # stop(self):
    # stop_1m(self, motor):
    # brake(self, left_torque, right_torque):
    # brake_1m(self, motor, torque):
    # brake1m(self, motor):
    # reset_left_encoder(self):
    # reset_right_encoder(self):
    # led(self, state):
    # obstacle_emitters(self, state):
    # __servo(self, command, position):
    # servo1(self, position):
    # servo2(self, position):
    # __float_to_bytes(self, number):
    # min_battery(self, batmin):
    # save_calibrate(self, bat, left_power, right_power):
    # read_button(self):
    # read_battery(self):
    # read_left_encoder(self):
    # read_right_encoder(self):
    # read_left_encoder_increment(self):
    # read_right_encoder_increment(self):
    # read_firmware(self):
    # obstacle_sensors(self):
    # read_IR_sensors(self):
    # read_left_range(self):
    # read_right_range(self):
    # read_adc(self, channel):
    # read_adc_0(self):
    # read_adc_1(self):
    # read_adc_2(self):
    # read_adc_3(self):
    # read_adc_4(self):
    # read_adc_5(self):
    # read_adc_6(self):
    # read_adc_7(self):
    # read_DBG(self, index):
    # text_to_bytes(self, text, length):
    # __lcd(self, lcd_line, text1, text2 = None, text3 = None, text4 = None):
    # lcd1(self, text1, text2 = None, text3 = None, text4 = None):
    # lcd2(self, text1, text2 = None, text3 = None, text4 = None):


if __name__ == "__main__":
    main()
