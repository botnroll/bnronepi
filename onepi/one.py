""" Library to interface with Bot'n Roll ONE A+ from www.botnroll.com """

import os
import time
import spidev
import struct
import time
import setproctitle
from onepi.utils.line_detector import LineDetector
from onepi.utils.monitor import Monitor

class BnrOneAPlus:
    """
    Class definition to interface with BotnRoll One A
    By creating an object of this class one can send and receive data
    to and from a BotnRoll One A robot connected using an spi interface
    """

    _KEY1 = 0xAA  # key used in critical commands
    _KEY2 = 0x55  # key used in critical commands
    _BRAKE_TORQUE = 100
    _OFF = 0
    _ON = 1
    _AN0 = 0
    _AN1 = 1
    _AN2 = 2
    _AN3 = 3
    _AN4 = 4
    _AN5 = 5
    _AN6 = 6
    _AN7 = 7

    # User Commands
    # Read Firmware version
    _COMMAND_FIRMWARE = 0xFE  # Read firmware value (integer value)

    # Write Commands->Don't require response from Bot'n Roll ONE A+
    _COMMAND_LED = 0xFD  # LED
    _COMMAND_SERVO1 = 0xFC  # Move Servo1
    _COMMAND_SERVO2 = 0xFB  # Move Servo2
    _COMMAND_LCD_L1 = 0xFA  # Write LCD line1
    _COMMAND_LCD_L2 = 0xF9  # Write LCD line2
    _COMMAND_IR_EMITTERS = 0xF8  # IR Emmiters ON/OFF
    _COMMAND_STOP = 0xF7  # Stop motors freeley
    _COMMAND_MOVE = 0xF6  # Move motors
    _COMMAND_BRAKE = 0xF5  # Stop motors with brake torque
    _COMMAND_BAT_MIN = 0xF4  # Configure low battery level
    _COMMAND_SET_PID = 0xF3  # Set kp, ki, kd for PID control
    _COMMAND_MOVE_RAW = 0xF2  # Move motors for calibration
    _COMMAND_SET_MOTORS = 0xF1  # Save calibration data
    _COMMAND_ENCL_RESET = 0xF0  # Preset the value of encoder1
    _COMMAND_ENCR_RESET = 0xEF  # Preset the value of encoder2
    _COMMAND_MOVE_RPM = 0xEE # Move motors with speed in rpm
    _COMMAND_FUTURE_USE2 = 0xED
    _COMMAND_FUTURE_USE3 = 0xEC
    _COMMAND_FUTURE_USE4 = 0xEB
    _COMMAND_MOVE_1M = 0xEA  # Move 1 motor
    _COMMAND_STOP_1M = 0xE9  # Stop 1 motor
    _COMMAND_BRAKE_1M = 0xE8  # Brake 1 motor
    _COMMAND_FUTURE_USE5 = 0xE7

    # Read Commands-> requests to Bot'n Roll ONE
    _COMMAND_ADC0 = 0xDF  # Read ADC0
    _COMMAND_ADC1 = 0xDE  # Read ADC1
    _COMMAND_ADC2 = 0xDD  # Read ADC2
    _COMMAND_ADC3 = 0xDC  # Read ADC3
    _COMMAND_ADC4 = 0xDB  # Read ADC4
    _COMMAND_ADC5 = 0xDA  # Read ADC5
    _COMMAND_ADC6 = 0xD9  # Read ADC6
    _COMMAND_ADC7 = 0xD8  # Read ADC7
    _COMMAND_BAT_READ = 0xD7  # Read ADC battery
    _COMMAND_BUT_READ = 0xD6  # Read ADC button
    _COMMAND_OBSTACLES = 0xD5  # Read IR obstacle sensors
    _COMMAND_IR_SENSORS = 0xD4  # Read IR sensors instant value
    _COMMAND_ENCL = 0xD3  # Read Encoder1 position
    _COMMAND_ENCR = 0xD2  # Read Encoder2 position
    _COMMAND_ENCL_INC = 0xD1  # Read Encoder1 Incremental value
    _COMMAND_ENCR_INC = 0xD0  # Read Encoder2 Incremental value
    _COMMAND_LINE_READ = 0xCF  # Read Line Value (-100 +100)
    _COMMAND_RANGE_LEFT = 0xCE  # Read IR obstacles distance range
    _COMMAND_RANGE_RIGHT = 0xCD  # Read IR obstacles distance range

    # Arduino commands -> move to separate file
    # Read Commands-> Computer to Bot'n Roll ONE A+
    _COMMAND_ARDUINO_ANA0 = 0xBF  # Read analog0 value
    _COMMAND_ARDUINO_ANA1 = 0xBE  # Read analog1 value
    _COMMAND_ARDUINO_ANA2 = 0xBD  # Read analog2 value
    _COMMAND_ARDUINO_ANA3 = 0xBC  # Read analog3 value
    _COMMAND_ARDUINO_DIG0 = 0xBB  # Read digital0 value
    _COMMAND_ARDUINO_DIG1 = 0xBA  # Read digital1 value
    _COMMAND_ARDUINO_DIG2 = 0xB9  # Read digital2 value
    _COMMAND_ARDUINO_DIG3 = 0xB8  # Read digital3 value
    _COMMAND_ARDUINO_DIG4 = 0xB7  # Read digital4 value
    _COMMAND_ARDUINO_DIG5 = 0xB6  # Read digital5 value
    _COMMAND_ARDUINO_DIG6 = 0xB5  # Read digital6 value
    _COMMAND_ARDUINO_DIG7 = 0xB4  # Read digital7 value
    _COMMAND_ARDUINO_DIG8 = 0xB3  # Read digital8 value
    _COMMAND_ARDUINO_DIG9 = 0xB2  # Read digital9 value
    _COMMAND_ARDUINO_DIG10 = 0xB1  # Read digital10 value
    _COMMAND_ARDUINO_DIG11 = 0xB0  # Read digital11 value
    _COMMAND_ARDUINO_DIG12 = 0xAF  # Read digital12 value
    _COMMAND_ARDUINO_DIG13 = 0xAE  # Read digital13 value
    _COMMAND_ARDUINO_BUZ = 0xAD  # Read Buzzer
    _COMMAND_ARDUINO_CMP = 0xAC  # Read Compass
    _COMMAND_ARDUINO_SNR = 0xAB  # Read Sonar
    _COMMAND_ARDUINO_GRP1 = 0xAA  # Read gripper1
    _COMMAND_ARDUINO_GRP2 = 0x9F  # Read gripper2

    _LCD_CHARS_PER_LINE = 16

    _delay_TR = 20  # 20 MinStable:15  Crash:14
    _delay_SS = 20  # 20 Crash: No crash even with 0 (ZERO)

    def __init__(self, bus=0, device=0, monitor=1):
        """
        Constructor for BnrOneAPlus class

        :param bus: specifies which bus to use, in the case of raspberry pi should be 0
        :param device: is the chip select pin. Set to 0 or 1, depending on the connections
        :param monitor: specifies if this process should be monitored
        """

        self._monitor_bnr = Monitor()
        # Checks if the Monitor process is running
        if not self._monitor_bnr.is_process_running(self._monitor_bnr._MONITOR_NAME):
            self._monitor_bnr.start_monitor()

        allowed_to_run = True
        if monitor:
            if not self._monitor_bnr.is_process_running(self._monitor_bnr._PROCESS_NAME):
                allowed_to_run = True
                # Sets the process name to BnrOneAPlus
                setproctitle.setproctitle(self._monitor_bnr._PROCESS_NAME)
            else:
                allowed_to_run = False
                print("There is already Python Code communicating with the Bot'n Roll One A+.")
                print("Please quit the other process first.")
                os._exit(1)

        if allowed_to_run:
            self.bus = bus
            self.device = device
            self._spi = spidev.SpiDev()
            self.line_detector = LineDetector()


    def __us_sleep(self, microseconds):
        """
        sleeps for a specified time in microseconds
        """
        time.sleep(microseconds / 1000000)

    def __ms_sleep(self, millisseconds):
        """
        sleeps for a specified time in millisseconds
        """
        time.sleep(millisseconds / 1000)

    def __high_byte(self, word):
        """
        returns the high byte of the input word (2 bytes)
        """
        return (int(word) >> 8) & 0xFF

    def __low_byte(self, word):
        """
        returns the low byte of the input word (2 bytes)
        """
        return int(word) & 0xFF

    def __open_spi(self):
        """
        Opens a spi connection and specifies the speed and mode
        """
        self._spi.open(self.bus, self.device)
        self._spi.max_speed_hz = (
            244000 # see https://www.takaitra.com/spi-device-raspberry-pi/
        )
        self._spi.mode = 1

    def __close_spi(self):
        """
        Closes the spi connection
        """
        self._spi.close()
        self.__us_sleep(self._delay_SS)

    def __request_byte(self, command):
        """
        Reads a byte from the spi device

        :param command: Command to be sent to the device
        :return: returns a byte containing the information requested by the command
        :rtype: byte
        """
        self.__open_spi()
        msg = [command, self._KEY1, self._KEY2]
        self._spi.xfer2(msg)
        self.__us_sleep(self._delay_TR)
        result = self._spi.readbytes(1)
        self.__close_spi()
        return result[0]

    def __request_word(self, command):
        """
        Reads a word from the spi device

        :param command: Command to be sent to the device
        :return: returns a word containing the information requested by the command
        :rtype: word
        """
        self.__open_spi()
        msg = [command, self._KEY1, self._KEY2]
        self._spi.xfer2(msg)
        self.__us_sleep(self._delay_TR)
        high_byte = self._spi.readbytes(1)
        low_byte = self._spi.readbytes(1)
        self.__close_spi()
        return (high_byte[0] << 8) + low_byte[0]

    def __request_float(self, command):
        """
        Reads a float from the spi device

        :param command: Command to be sent to the device
        :return: returns a float containing the information requested by the command
        :rtype: float
        """
        self.__open_spi()
        msg = [command, self._KEY1, self._KEY2]
        self._spi.xfer2(msg)
        self.__us_sleep(self._delay_TR)
        byte1 = self._spi.readbytes(1)
        byte2 = self._spi.readbytes(1)
        byte3 = self._spi.readbytes(1)
        byte4 = self._spi.readbytes(1)
        self.__close_spi()
        byte_data = bytes([byte1[0], byte2[0], byte3[0], byte4[0]])
        float_value = struct.unpack('f', byte_data)[0]
        return float_value


    def __send_data(self, command, msg=""):
        """
        Sends data to the spi device containing the command, the authentication keys and the message

        :param command: Command to be sent to the device
        :param msg: Message to be sent to the device
        """
        self.__open_spi()
        to_send = [command, self._KEY1, self._KEY2]
        if msg != "":
            to_send.extend(msg)
        self._spi.xfer2(to_send)
        self.__close_spi()
        self.__ms_sleep(2)

    def read_debug(self, index):
        """
        reads a debug variable (float) from the spi device
        """
        return self.__request_word(0xB9 - index)

    def read_debug_float(self):
        """
        reads a debug variable (float) from the spi device
        """
        return self.__request_float(0xB5)

    def set_pid(self, kp, ki, kd):
        """
        Sets the pid params for motor control
        """
        msg = [
            self.__high_byte(kp),
            self.__low_byte(kp),
            self.__high_byte(ki),
            self.__low_byte(ki),
            self.__high_byte(kd),
            self.__low_byte(kd),
        ]
        self.__send_data(self._COMMAND_SET_PID, msg)

    def set_motors(self, start_moving_power, ks, ctrl_pulses):
        """
        :param start_moving_power pwm applied initially when wheel is stopped
        :param ks gain multiplier to adjust the inital pwm
        :param ctrl_pulses pulses read at 25ms when running at full speed
        """
        msg = [
            self.__high_byte(start_moving_power),
            self.__low_byte(start_moving_power),
            self.__high_byte(ks),
            self.__low_byte(ks),
            self.__high_byte(ctrl_pulses),
            self.__low_byte(ctrl_pulses),
        ]
        self.__send_data(self._COMMAND_SET_MOTORS, msg)

    def move(self, left_speed, right_speed):
        """
        Sends left and right wheel speeds to the spi device.

        :param left_speed: desired left wheel speed
        :param right_speed: desired right wheel speed
        """
        msg = [
            self.__high_byte(left_speed),
            self.__low_byte(left_speed),
            self.__high_byte(right_speed),
            self.__low_byte(right_speed),
        ]
        self.__send_data(self._COMMAND_MOVE, msg)

    def move_rpm(self, left_rpm, right_rpm):
        """
        Sends left and right wheel speeds to the spi device.

        :param left_speed: desired left wheel speed
        :param right_speed: desired right wheel speed
        """
        msg = [
            self.__high_byte(left_rpm),
            self.__low_byte(left_rpm),
            self.__high_byte(right_rpm),
            self.__low_byte(right_rpm)
        ]
        self.__send_data(self._COMMAND_MOVE_RPM, msg)

    def move_raw(self, left_power, right_power):
        """
        Sends calibration power data to the spi device

        :param left_power: power for left wheel
        :param right_power: power for right wheel
        """
        msg = [
            self.__high_byte(left_power),
            self.__low_byte(left_power),
            self.__high_byte(right_power),
            self.__low_byte(right_power),
        ]
        self.__send_data(self._COMMAND_MOVE_RAW, msg)

    def move_1m(self, motor, speed):
        """
        Sets the specified motor to run at the given speed

        :param motor: number of the motor to set the speed for
        :param speed: speed to set the motor with
        """
        msg = [self.__low_byte(motor), self.__high_byte(speed), self.__low_byte(speed)]
        self.__send_data(self._COMMAND_MOVE_1M, msg)

    def stop(self):
        """
        Sends command to stop both motors
        """
        self.__send_data(self._COMMAND_STOP)

    def stop_1m(self, motor):
        """
        Sends command to stop the specified motor

        :param motor: number of the motor to stop
        """
        msg = [self.__low_byte(motor)]
        self.__send_data(self._COMMAND_STOP_1M, msg)

    def brake(self, left_torque, right_torque):
        """
        Applies brake torques to motors

        :param left_torque: torque to apply to the left motor
        :param right_torque: torque to apply to the right motor
        """
        msg = [
            self.__low_byte(left_torque),
            self.__low_byte(right_torque),
        ]
        self.__send_data(self._COMMAND_BRAKE, msg)

    def brake_1m(self, motor, torque=None):
        """
        Applies brake torque to a motor

        :param motor: motor to apply the torque
        :param torque: torque to apply to the motor
        """
        if torque is None:
            torque = self._BRAKE_TORQUE
        msg = [self.__low_byte(motor), self.__low_byte(torque)]
        self.__send_data(self._COMMAND_BRAKE_1M, msg)

    def reset_left_encoder(self):
        """
        Reset counter for the left encoder
        """
        self.__send_data(self._COMMAND_ENCL_RESET)

    def reset_right_encoder(self):
        """
        Reset counter for the right encoder
        """
        self.__send_data(self._COMMAND_ENCR_RESET)

    def led(self, state):
        """
        Turns on/off the led

        :param state: turns led ON for odd numbers, OFF otherwise
        """
        state = state % 2
        msg = [self.__low_byte(state)]
        self.__send_data(self._COMMAND_LED, msg)

    def obstacle_emitters(self, state):
        """
        Turns on/off the obstacle emitters

        :param state: turns emitters ON for odd numbers, OFF otherwise
        """
        msg = [self.__low_byte(state % 2)]
        self.__send_data(self._COMMAND_IR_EMITTERS, msg)

    def __servo(self, command, position):
        """
        Sends a position to the commanded servo

        :param command: command specifying which servo to use
        :param position: desired servo position [0-255]
        """
        msg = [self.__low_byte(position)]
        self.__send_data(command, msg)

    def servo1(self, position):
        """
        Sets servo1 position

        :param position: desired position
        """
        self.__servo(self._COMMAND_SERVO1, position)

    def servo2(self, position):
        """
        Sets servo2 position

        :param position: desired position
        """
        self.__servo(self._COMMAND_SERVO2, position)

    def __float_to_bytes(self, number):
        """
        converts a floating point number into 4 bytes:
         - 2 for the integer part
         - 2 for the decimal part

        :param number: floating point number
        :return: four bytes representation of the floating point number
        :rtype: array of 4 bytes
        """
        integer, decimal = divmod(number, 1)
        decimal = decimal * 1000
        int_high_byte = self.__high_byte(integer)
        int_low_byte = self.__low_byte(integer)
        dec_high_byte = self.__high_byte(decimal)
        dec_low_byte = self.__low_byte(decimal)
        return [int_high_byte, int_low_byte, dec_high_byte, dec_low_byte]

    def set_min_battery_V(self, batmin):
        """
        Sets the minimum battery level.
        If battery drops below this value the BotnRoll One A will issue a warning
        on the LCD and won't let motors to move

        :para batmin: minimum voltage level acceptable for the battery (V)
        """
        msg = self.__float_to_bytes(batmin)
        self.__send_data(self._COMMAND_BAT_MIN, msg)
        self.__ms_sleep(25)

    def read_button(self):
        """
        Gets the button number of the robot that is being pressed
        Looking at the robot with the buttons on the right side of the LCD,
        returns:
          0 for none
          1 for button on top
          2 for button in the middle
          3 for button at the bottom

        :return: number of the button being pressed (0, 1, 2, 3)
        """
        button = 0
        adc = self.__request_word(self._COMMAND_BUT_READ)
        if 0 <= adc < 100:  # 0-82
            button = 1
        elif 459 <= adc < 571:  # 509-521
            button = 2
        elif 629 <= adc < 737:  # 679-687
            button = 3
        return button

    def read_battery(self):
        """
        Reads the current voltage supplied to BotnRoll One A

        :return: voltage (V) of input power supply
        :rtype: float
        """
        return self.__request_word(self._COMMAND_BAT_READ) / 50.7

    def read_left_encoder(self):
        """
        Reads the value of the left encoder since last request
        Note: Every time we read the encoder it resets itself

        :return: counter of the encoder
        :rtype: int
        """
        value = self.__request_word(self._COMMAND_ENCL)
        if value >= 0x8000:
            value -= 0x10000
        return value

    def read_right_encoder(self):
        """
        Reads the value of the right encoder since last request
        Note: Every time we read the encoder it resets itself

        :return: counter of the encoder
        :rtype: int
        """
        value = self.__request_word(self._COMMAND_ENCR)
        if value >= 0x8000:
            value -= 0x10000
        return value

    def read_left_encoder_increment(self):
        """
        Reads the left encoder and keeps incrementing its value
        It does NOT reset the value after reading it

        :return: encoder reading
        :rtype: int
        """
        value = self.__request_word(self._COMMAND_ENCL_INC)

        # Check if value should be negative
        if value >= 0x8000:
            value -= 0x10000
        return value

    def read_right_encoder_increment(self):
        """
        Reads the right encoder and keeps incrementing its value
        It does NOT reset the value after reading it

        :return: encoder reading
        :rtype: int
        """
        value = self.__request_word(self._COMMAND_ENCR_INC)
        if value >= 0x8000:
            value -= 0x10000
        return value

    def read_firmware(self):
        """
        Reads the version of the firmware on the microcontroller

        :return: firmware version
        :rtype: list of bytes
        """
        self.__send_data(self._COMMAND_FIRMWARE)
        self.__open_spi()
        first_byte = self._spi.readbytes(1)
        second_byte = self._spi.readbytes(1)
        third_byte = self._spi.readbytes(1)
        self.__close_spi()
        self.__us_sleep(20)
        firmware = first_byte + second_byte + third_byte
        return firmware

    def obstacle_sensors(self):
        """
        Reads information from obstacle sensors
        Returns:
            0 if no obstacles detected
            1 if obstacle detected on the left side only
            2 if obstacle detected on the left side only
            3 if obstacle detected on both sides

        :return: number representing the obstacle detection
        :rtype: int
        """
        return self.__request_byte(self._COMMAND_OBSTACLES)

    def read_ir_sensors(self):
        """
        Reads infrared sensors. Returns 1 if both sensors detect input, 0 otherwise.

        :return: 1 if both sensors detect input, 0 otherwise
        """
        return self.__request_byte(self._COMMAND_IR_SENSORS)

    def read_left_range(self):
        """
        Reads the range value detected by the sensor on the left side

        :return: distance reported by the sensor (mm)
        :rtype: int
        """
        return self.__request_byte(self._COMMAND_RANGE_LEFT)

    def read_right_range(self):
        """
        Reads the range value detected by the sensor on the right side

        :return: distance reported by the sensor (mm)
        :rtype: int
        """
        return self.__request_byte(self._COMMAND_RANGE_RIGHT)

    def __get_command_adc(self, channel):
        """
        Converts a channel to the correspondig device command
        If channel doesn't exist returns 0x00
        :param channel: number of the adc channel
        :return: command to read from the given adc channel
        :rtype: byte
        """
        command = 0x00
        if channel == 0:
            command = self._COMMAND_ADC0
        elif channel == 1:
            command = self._COMMAND_ADC1
        elif channel == 2:
            command = self._COMMAND_ADC2
        elif channel == 3:
            command = self._COMMAND_ADC3
        elif channel == 4:
            command = self._COMMAND_ADC4
        elif channel == 5:
            command = self._COMMAND_ADC5
        elif channel == 6:
            command = self._COMMAND_ADC6
        elif channel == 7:
            command = self._COMMAND_ADC7

        return command

    def read_adc(self, channel):
        """
        Reads adc channel. Expects channel to be in the valid range [0-7]
        If ouside the range should return 0.

        :param channel: adc input channel to read from
        :return: value read from the given adc channel
        :rtype: int
        """
        command = self.__get_command_adc(channel)
        return self.__request_word(command)

    def read_adc_0(self):
        """
        Reads adc channel 0

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC0)

    def read_adc_1(self):
        """
        Reads adc channel 1

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC1)

    def read_adc_2(self):
        """
        Reads adc channel 2

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC2)

    def read_adc_3(self):
        """
        Reads adc channel 3

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC3)

    def read_adc_4(self):
        """
        Reads adc channel 4

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC4)

    def read_adc_5(self):
        """
        Reads adc channel 5

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC5)

    def read_adc_6(self):
        """
        Reads adc channel 6

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC6)

    def read_adc_7(self):
        """
        Reads adc channel 7

        :return: value read from the given adc channel
        :rtype: int
        """
        return self.__request_word(self._COMMAND_ADC7)

    def __get_command_dbg(self, index):
        """
        Converts the index [0-3] into a command
        If index outside range returns 0x00

        :param index: index to convert from
        :return: command corresponding to given index
        :rtype: byte
        """
        if index == 0:
            return 0xB9
        elif index == 1:
            return 0xB8
        elif index == 2:
            return 0xB7
        elif index == 3:
            return 0xB6
        else:
            return 0x00

    def read_dbg(self, index):
        """
        Reads debug info from the device

        :param index: index of debug register
        :return: contents of the register
        :rtype: int
        """
        command = self.__get_command_dbg(index)
        return self.__request_word(command)

    def __text_to_bytes(self, text, length):
        """
        Converts text to bytes with the predefined length.
        Crops the text if larger than the specified length
        and adds spaces if smaller than the specified length

        :param text: input text
        :param length: max length of the output text
        :return: output text with specified length
        :rtype: list of chars
        """
        text_length = len(text)
        if text_length < length:
            text += (length - text_length) * " "
        text = text[:length]
        return text.encode("latin-1")

    def __join_and_trim_data(self, data1, data2=None, data3=None, data4=None):
        """
        Concatenates data into a stream of chars with a predefined size:
        It concatenates all the input data such that it fits within the maximum
        number of chars the LCD can accomodate in a single line.
        If up to 3 data inputs are given a space is added between each piece of data and
        trimming is done after concatenating.
        If 4 inputs are given then it trims each of those inputs first to 4 chars each
        and then concatenates all of them.

        :param data1: piece of data
        :param data2: optional piece of data
        :param data3: optional piece of data
        :param data4: optional piece of data
        :return: trimmed stream of chars with predefined size of _LCD_CHARS_PER_LINE
        :rtype: list of chars
        """
        if data2 is None:
            trimmed_data = self.__text_to_bytes(str(data1), self._LCD_CHARS_PER_LINE)
        elif data3 is None:
            trimmed_data = self.__text_to_bytes(
                str(data1) + " " + str(data2), self._LCD_CHARS_PER_LINE
            )
        elif data4 is None:
            trimmed_data = self.__text_to_bytes(
                str(data1) + " " + str(data2) + " " + str(data3),
                self._LCD_CHARS_PER_LINE,
            )
        else:
            data1 = self.__text_to_bytes(str(data1), int(self._LCD_CHARS_PER_LINE / 4))
            data2 = self.__text_to_bytes(str(data2), int(self._LCD_CHARS_PER_LINE / 4))
            data3 = self.__text_to_bytes(str(data3), int(self._LCD_CHARS_PER_LINE / 4))
            data4 = self.__text_to_bytes(str(data4), int(self._LCD_CHARS_PER_LINE / 4))
            trimmed_data = data1 + data2 + data3 + data4

        return trimmed_data

    def lcd1(self, data1, data2=None, data3=None, data4=None):
        """
        Sends data to be displayed on the first line of the lcd
        :param data1: piece of data to display on the lcd
        :param data2: optional piece of data to display on the lcd
        :param data3: optional piece of data to display on the lcd
        :param data4: optional piece of data to display on the lcd
        """
        data_to_send = self.__join_and_trim_data(data1, data2, data3, data4)
        self.__send_data(self._COMMAND_LCD_L1, data_to_send)

    def lcd2(self, data1, data2=None, data3=None, data4=None):
        """
        Sends data to be displayed on the second line of the lcd

        :param data1: piece of data to display on the lcd
        :param data2: optional piece of data to display on the lcd
        :param data3: optional piece of data to display on the lcd
        :param data4: optional piece of data to display on the lcd
        """
        data_to_send = self.__join_and_trim_data(data1, data2, data3, data4)
        self.__send_data(self._COMMAND_LCD_L2, data_to_send)

    def read_line_sensors(self):
        """
        reads sensors from adc channels 0 to 7

        :return: sensor readings in a list
        :rtype: list of integers
        """
        sensor_reading = [0] * 8
        for i in range(8):
            sensor_reading[i] = self.read_adc(i)
        return sensor_reading

    def read_line(self):
        """
        Reads line sensors and returns a value between -100 and 100
        depending on the position the line is detected

        :return: value between -100 and 100
        :rtype: float
        """
        sensor_reading = self.read_line_sensors()
        line = self.line_detector.compute_line(sensor_reading)
        return line
