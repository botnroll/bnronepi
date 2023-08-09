"""
Test functions to verify methods of BnrOneA class
"""
import os
import time
from one import BnrOneA


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
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0

    text = "Hi Raspberry Pi!"
    for text in scroll_text(text, 16):
        print(text, end="\n")
        one.lcd2(text)
        time.sleep(0.2)
    print(" ")


def test_move():
    """
    Test move method
    """
    print("=== Testing move ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    delay_s = 1
    print("Move forward")
    one.move(30, 30)
    time.sleep(delay_s)
    print("Rotate right")
    one.move(30, -30)
    time.sleep(delay_s)
    print("Rotate left")
    one.move(-30, 30)
    time.sleep(delay_s)
    print("Move backwards")
    one.move(-30, -30)
    time.sleep(delay_s)
    print("Stop")
    one.move(0, 0)


def test_move_calibrate():
    """
    Test move calibrate method
    """
    print("=== Testing move calibrate ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    delay_ms = 2000
    for i in range(0, 101, 5):
        print("Duty_cycle:", i)
        one.move_calibrate(i, i)
        time.sleep(0.5)
    print("Stopping both motors")
    one.move_calibrate(0, 0)
    print("At the start motors are not supposed to move.")
    print("After a certain value they should start moving but not necessarily at the same time.")


def test_move_1m():
    """
    Test move one motor
    """
    print("=== Testing move one motor ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    left_motor = 1
    right_motor = 2
    speed = 30
    delay_s = 2
    print("Left wheel forward")
    one.move_1m(left_motor, speed)
    time.sleep(delay_s)
    print("Right wheel forward")
    one.move_1m(right_motor, speed)
    time.sleep(delay_s)
    print("Left wheel: STOP")
    one.move_1m(left_motor, 0)
    time.sleep(delay_s)
    print("Right wheel backwards")
    one.move_1m(right_motor, -speed)
    time.sleep(delay_s)
    print("Left wheel backwards")
    one.move_1m(left_motor, -speed)
    time.sleep(delay_s)
    print("Right wheel: STOP")
    one.move_1m(right_motor, 0)
    time.sleep(delay_s)
    print("Left wheel: STOP")
    one.move_1m(left_motor, 0)


def test_stop():
    """
    Test stop
    """
    print("=== Testing stop ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    speed = 30
    delay_s = 2
    print("Move forward")
    one.move(speed, speed)
    time.sleep(delay_s)
    print("STOP")
    one.stop()
    time.sleep(delay_s)
    print("Move backwards")
    one.move(-speed, -speed)
    time.sleep(delay_s)
    print("STOP")
    one.stop()
    time.sleep(delay_s)


def test_stop_1m():
    """
    Test stop 1 motor
    """
    print("=== Testing stop 1 motor ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    left_motor = 1
    right_motor = 2
    speed = 30
    delay_s = 2
    print("Move forward")
    one.move(speed, speed)
    time.sleep(delay_s)
    print("Left wheel: STOP")
    one.stop_1m(left_motor)
    time.sleep(delay_s)
    print("Right wheel: STOP")
    one.stop_1m(right_motor)
    time.sleep(delay_s)
    print("Move backwards")
    one.move(-speed, -speed)
    time.sleep(delay_s)
    print("Left wheel: STOP")
    one.stop_1m(left_motor)
    time.sleep(delay_s)
    print("Right wheel: STOP")
    one.stop_1m(right_motor)
    time.sleep(delay_s)


def test_brake():
    """
    Test brake
    """
    print("=== Testing brake ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    speed = 30
    delay_s = 2
    print("Move forward")
    one.move(speed, speed)
    time.sleep(delay_s)
    print("BRAKE 10%")
    one.brake(10, 10)
    time.sleep(delay_s)
    print("Move backwards")
    one.move(-speed, -speed)
    time.sleep(delay_s)
    print("BRAKE 70%")
    one.brake(70, 70)


def test_brake_1m():
    """
    Test brake 1 motor
    """
    print("=== Testing brake 1 motor ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    left_motor = 1
    right_motor = 2
    speed = 30
    delay_s = 2
    print("Move forward")
    one.move(speed, speed)
    time.sleep(delay_s)
    print("BRAKE 70% left motor")
    one.brake_1m(left_motor, 70)
    time.sleep(delay_s)
    print("BRAKE 70% right motor")
    one.brake_1m(right_motor, 70)
    time.sleep(delay_s)
    print("Move backwards")
    one.move(-speed, -speed)
    time.sleep(delay_s)
    print("BRAKE Default torque left motor")
    one.brake_1m(left_motor)
    time.sleep(delay_s)
    print("BRAKE Default torque right motor")
    one.brake_1m(right_motor)


def reset_encoder(side):
    """
    reset encoder
    """
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    motor = side
    left_motor = 1
    speed = 20
    delay_s = 1
    print("Move forward")
    if motor == left_motor:
        one.reset_left_encoder()
    else:
        one.reset_right_encoder()
    one.move_1m(motor, speed)
    time.sleep(delay_s)
    if motor == left_motor:
        before_reseting = int(one.read_left_encoder())
        time.sleep(delay_s)
        one.reset_left_encoder()
        after_reseting = int(one.read_left_encoder())
    else:
        before_reseting = int(one.read_right_encoder())
        time.sleep(delay_s)
        one.reset_right_encoder()
        after_reseting = int(one.read_right_encoder())
    one.stop_1m(motor)
    print("before_reseting:", before_reseting, "\tafter_reseting:", after_reseting)
    assert after_reseting < before_reseting
    assert after_reseting < 2


def test_reset_left_encoder():
    """
    Test reset left encoder
    """
    print("=== Testing reset left encoder ===")
    left_motor = 1
    reset_encoder(left_motor)


def test_reset_right_encoder():
    """
    Test reset right encoder
    """
    print("=== Testing reset right encoder ===")
    right_motor = 2
    reset_encoder(right_motor)


def blink(one, number_of_times, delay_s):
    """
    Blinks the led on Bot'n Roll One A

    :param one: object to send the command to
    :param number_of_times: number of times to toggle the led
    :duration between toggling
    """
    state = 1
    for i in range(1, number_of_times + 1):
        state = i % 2
        print("LED: ", state)
        one.led(state)
        time.sleep(delay_s)


def test_led():
    """
    Test led
    """
    print("=== Testing led blinking ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    blink(one, 6, 1)


def test_obstacle_emitters():
    """
    Test obstacle emitters
    """
    print("=== Testing obstacle emitters ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    one.obstacle_emitters(1)
    state = 0
    number_of_times = 6
    delay_s = 2
    print("Place obstacle close in front of the obstacle sensors")
    print("Verify red leds light on when emitter state is 1 and turn off otherwise")
    for i in range(0, number_of_times + 1):
        state = i % 2
        print("Emitter state: ", state)
        one.obstacle_emitters(state)
        time.sleep(delay_s)


def servo(id):
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    delay_s = 0.1
    print("Rotate in one way")
    for i in range(10, 170, 10):
        if id == 1:
            one.servo1(i)
        else:
            one.servo2(i)
        time.sleep(delay_s)
    print("Rotate in opposite way")
    for i in range(170, 10, -10):
        if id == 1:
            one.servo1(i)
        else:
            one.servo2(i)
        time.sleep(delay_s)
    one.servo1(90)


def test_servo1():
    """
    Test servo 1
    """
    print("=== Testing servo 1 ===")
    servo(1)


def test_servo2():
    """
    Test servo 2
    """
    print("=== Testing servo 2 ===")
    servo(2)


def test_min_battery():
    """
    Test min battery
    """
    print("=== Testing min battery ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Setting to a normal value.")
    print("Robot should move in response to a move command.")
    one.min_battery(8.4)
    print("voltage = ", one.read_battery())
    one.move(30, 30)
    time.sleep(2)
    print("Setting to a high value. LCD should display '* LOW BATTERY *'.")
    print("Robot should not move in response to a move command.")
    one.min_battery(15.0)
    print("voltage = ", one.read_battery())
    one.move(-20, -20)
    time.sleep(2)
    one.stop()
    print("!!! You need to reboot the robot to reestablish moving capabilities !!!")
    one.min_battery(8.4)


def test_save_calibrate_1():
    """
    Test save calibrate - 1st test
    """
    print("=== Testing save calibrate - 1st test===")
    print("!!! You will need to re-calibrate the motors after this test as calibration is lost !!!")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("1st time running this test the wheels are expected to move.")
    print("2nd time running this test the wheels should NOT move.")
    one.move(30, 30)
    time.sleep(2)
    one.stop()
    print("Setting minimum duty cycle as 0.")
    print("If this is the 1st time, please reboot the robot and run same test again.")
    one.save_calibrate(12, 5, 5)


def test_save_calibrate_2():
    """
    Test save calibrate - 2nd test
    """
    print("=== Testing save calibrate - 2nd test ===")
    print("!!! You will need to re-calibrate the motors after this test as calibration is lost !!!")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print(
        "1st time running this test: if test_save_calibrate_1 was run before this one the wheels should not move otherwise they will."
    )
    print("2nd time running this test the wheels should definitely move.")
    one.move(30, 30)
    time.sleep(2)
    one.stop()
    print("Setting minimum duty cycle as 0.")
    print("If this is the 1st time, please reboot the robot and run same test again.")
    one.save_calibrate(12, 70, 70)


def test_read_button():
    """
    Reads button pressed from the robot
    Note: User should press the buttons on the robot
    """
    print("=== Testing read button ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0

    print("Please press a button on the robot")
    time.sleep(2)
    for i in range(30):
        print("Test", i + 1, "of 30. Button pressed: ", one.read_button())
        time.sleep(0.3)


def test_read_battery():
    """
    Test voltage battery reading
    """
    print("=== Testing read battery ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Battery voltage = ", one.read_battery())


def read_encoder(side):
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    motor = side
    left_motor = 1
    speed = 20
    delay_s = 1
    print("Move forward")
    if motor == left_motor:
        one.reset_left_encoder()
    else:
        one.reset_right_encoder()
    one.move_1m(motor, speed)
    time.sleep(delay_s)
    if motor == left_motor:
        first_reading = int(one.read_left_encoder())
        time.sleep(delay_s * 1.1)
        second_reading = int(one.read_left_encoder())
        time.sleep(delay_s * 0.9)
        third_reading = int(one.read_left_encoder())
    else:
        first_reading = int(one.read_right_encoder())
        time.sleep(delay_s * 1.1)
        second_reading = int(one.read_right_encoder())
        time.sleep(delay_s * 0.9)
        third_reading = int(one.read_right_encoder())
    one.stop_1m(motor)
    print("first_reading:", first_reading, "\tsecond_reading:", second_reading, "\tthird_reading:", third_reading)
    assert third_reading < first_reading < second_reading


def test_read_left_encoder():
    """
    Test read left encoder
    """
    print("=== Testing read left encoder ===")
    left_motor = 1
    read_encoder(left_motor)


def test_read_right_encoder():
    """
    Test read right encoder
    """
    print("=== Testing read right encoder ===")
    right_motor = 2
    read_encoder(right_motor)


def read_encoder_increment(side):
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    motor = side
    left_motor = 1
    speed = 20
    delay_s = 1
    print("Move forward")
    if motor == left_motor:
        one.reset_left_encoder()
    else:
        one.reset_right_encoder()
    one.move_1m(motor, speed)
    time.sleep(delay_s)
    if motor == left_motor:
        first_reading = int(one.read_left_encoder_increment())
        time.sleep(delay_s * 1.1)
        second_reading = int(one.read_left_encoder_increment())
        time.sleep(delay_s * 0.9)
        third_reading = int(one.read_left_encoder_increment())
    else:
        first_reading = int(one.read_right_encoder_increment())
        time.sleep(delay_s * 1.1)
        second_reading = int(one.read_right_encoder_increment())
        time.sleep(delay_s * 0.9)
        third_reading = int(one.read_right_encoder_increment())
    one.stop_1m(motor)
    print("first_reading:", first_reading, "\tsecond_reading:", second_reading, "\tthird_reading:", third_reading)
    assert first_reading < second_reading < third_reading


def test_read_left_encoder_increment():
    """
    Test read left encoder increment
    """
    print("=== Testing read left encoder increment ===")
    left_motor = 1
    read_encoder_increment(left_motor)


def test_read_right_encoder_increment():
    """
    Test read right encoder increment
    """
    print("=== Testing read right encoder increment ===")
    right_motor = 2
    read_encoder_increment(right_motor)


def test_read_firmware():
    """
    Test read firmware
    """
    print("=== Testing read firmware ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    firmware = one.read_firmware()
    print("Firmware = ", firmware[0], ".", firmware[1], ".", firmware[2])


def test_obstacle_sensors():
    """
    Test obstacle sensors
    """
    print("=== Testing obstacle sensors ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    for i in range(100):
        print("Test", i + 1, "of 100: Output:", one.obstacle_sensors())
        time.sleep(0.2)


def test_read_IR_sensors():
    """
    Test read IR sensors
    """
    print("=== Testing read IR sensors ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    for i in range(100):
        print("Test", i + 1, "of 100: Output:", one.read_ir_sensors())
        time.sleep(0.2)


def test_read_left_range():
    """
    Test read left range sensor
    """
    print("=== Testing read left range sensor ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    for i in range(100):
        print("Test", i + 1, "of 100: Output:", one.read_left_range())
        time.sleep(0.2)


def test_read_right_range():
    """
    Test read right range sensor
    """
    print("=== Testing read right range sensor ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    for i in range(100):
        print("Test", i + 1, "of 100: Output:", one.read_right_range())
        time.sleep(0.2)


def test_read_adc():
    """
    Test read adc
    """
    print("=== Testing read adc ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    for i in range(8):
        print("Read adc", i, ":", one.read_adc(i))
        time.sleep(0.2)


def test_read_adc_0():
    """
    Test read adc 0
    """
    print("=== Testing read adc 0 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 0:", one.read_adc_0())


def test_read_adc_1():
    """
    Test read adc 1
    """
    print("=== Testing read adc 1 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 1:", one.read_adc_1())


def test_read_adc_2():
    """
    Test read adc 2
    """
    print("=== Testing read adc 2 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 2:", one.read_adc_2())


def test_read_adc_3():
    """
    Test read adc 3
    """
    print("=== Testing read adc 3 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 3:", one.read_adc_3())


def test_read_adc_4():
    """
    Test read adc 4
    """
    print("=== Testing read adc 4 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 4:", one.read_adc_4())


def test_read_adc_5():
    """
    Test read adc 5
    """
    print("=== Testing read adc 5 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 5:", one.read_adc_5())


def test_read_adc_6():
    """
    Test read adc 6
    """
    print("=== Testing read adc 6 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 6:", one.read_adc_6())


def test_read_adc_7():
    """
    Test read adc 7
    """
    print("=== Testing read adc 7 ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    print("Read adc 7:", one.read_adc_7())


def test_read_DBG():
    """
    Test read DBG
    """
    print("=== Testing read DBG ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0
    for i in range(4):
        print("Read dbg", i, ":", one.read_dbg(i))


def test_lcd():
    """
    Sends different types of text using both lines of the lcd
    User should verify the output by looking at the lcd on the robot
    """
    print("=== Testing writing data to LCD ===")
    one = BnrOneA(0, 0)  # creates a BotnRoll interface at bus 0 and channel 0

    delay_s = 1.6
    one.lcd1("")
    one.lcd2("Hi Raspberry Pi!")
    time.sleep(delay_s)
    one.lcd1("Hi Raspberry Pi!")
    one.lcd2("Day:", 31, "7", 2023)
    time.sleep(delay_s)
    one.lcd1("Day:", 31, "7", 2023)
    one.lcd2(17, "h", 15, "min")
    time.sleep(delay_s)
    one.lcd1(17, "h", 15, "min")
    one.lcd2("Ver.", 1, "Sub.", 3)
    time.sleep(delay_s)
    one.lcd1("Ver.", 1, "Sub.", 3)
    one.lcd2("Test number:", 1)
    time.sleep(delay_s)
    one.lcd1("Test number:", 1)
    one.lcd2("System", "test:", 1)
    time.sleep(delay_s)
    one.lcd1("System", "test:", 1)
    one.lcd2(1234567890123456)
    time.sleep(delay_s)
    one.lcd1(1234567890123456)
    one.lcd2(12345678, 1234567)
    time.sleep(delay_s)
    one.lcd1(12345678, 1234567)
    one.lcd2(12345, 12345, 1234)
    time.sleep(delay_s)
    one.lcd1(12345, 12345, 1234)
    one.lcd2(1111, 2222, 3333, 4444)
    time.sleep(delay_s)
    one.lcd1(1111, 2222, 3333, 4444)
    one.lcd2("      END       ")
    time.sleep(delay_s)
    one.lcd1("      END       ")
    one.lcd2("")


def main():
    """
    Calls functions to test public interface with BotnRoll One A
    Most of these tests should be verified with the robot connected to the raspbery pi
    and by visually inspecting the robot and/or the terminal
    """
    print("Run tests using: pytest", os.path.basename(__file__), "-s")

    # test_move()
    # test_move_calibrate()
    # test_move_1m()
    # test_stop()
    # test_stop_1m()
    # test_brake()
    # test_brake_1m()
    # test_reset_left_encoder()
    # test_reset_right_encoder()
    # test_led()
    # test_obstacle_emitters()
    # test_servo1()
    # test_servo2()
    # test_save_calibrate_1() # requires manual reboot
    # test_save_calibrate_2()  # requires manual reboot
    # test_min_battery() # requires manual reboot
    # test_read_button()
    # test_read_battery()
    # test_read_left_encoder()
    # test_read_right_encoder()
    # test_read_left_encoder_increment()
    # test_read_right_encoder_increment()
    # test_read_firmware()
    # test_obstacle_sensors()
    # test_read_IR_sensors()
    # test_read_left_range()
    # test_read_right_range()
    # test_read_adc()
    # test_read_adc_0()
    # test_read_adc_1()
    # test_read_adc_2()
    # test_read_adc_3()
    # test_read_adc_4()
    # test_read_adc_5()
    # test_read_adc_6()
    # test_read_adc_7()
    # test_read_DBG()
    # test_lcd()
    # test_scroll_text()


if __name__ == "__main__":
    main()
