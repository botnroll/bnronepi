#  BnrOneA.h - Library for interfacing with Bot'n Roll ONE Arduino Compatible from www.botnroll.com
#  Released into  public domain.

import time
import spidev

class BnrOneA:

    KEY1 = 0xAA # key used in critical commands
    KEY2 = 0x55 # key used in critical commands
    BRAKE_TORQUE =100
    OFF = 0
    ON  = 1
    AN0 = 0
    AN1 = 1
    AN2 = 2
    AN3 = 3
    AN4 = 4
    AN5 = 5
    AN6 = 6
    AN7 = 7

    # User Commands
    # Read Firmware version
    COMMAND_FIRMWARE        = 0xFE #Read firmware value (integer value)

    # Write Commands->Don't require response from Bot'n Roll ONE A
    COMMAND_LED             = 0xFD #LED
    COMMAND_SERVO1          = 0xFC #Move Servo1
    COMMAND_SERVO2          = 0xFB #Move Servo2
    COMMAND_LCD_L1          = 0xFA #Write LCD line1
    COMMAND_LCD_L2          = 0xF9 #Write LCD line2
    COMMAND_IR_EMITTERS     = 0xF8 #IR Emmiters ON/OFF
    COMMAND_STOP            = 0xF7 #Stop motors freeley
    COMMAND_MOVE            = 0xF6 #Move motors
    COMMAND_BRAKE           = 0xF5 #Stop motors with brake torque
    COMMAND_BAT_MIN         = 0xF4 #Configure low battery level
    COMMAND_MOVE_PID		= 0xF3 #Move motor with PID control
    COMMAND_MOVE_CALIBRATE  = 0xF2 #Move motors for calibration
    COMMAND_SAVE_CALIBRATE  = 0xF1 #Save calibration data
    COMMAND_ENCL_RESET		= 0xF0 #Preset the value of encoder1
    COMMAND_ENCR_RESET      = 0xEF #Preset the value of encoder2
    COMMAND_FUTURE_USE1     = 0xEE
    COMMAND_FUTURE_USE2     = 0xED
    COMMAND_FUTURE_USE3     = 0xEC
    COMMAND_FUTURE_USE4     = 0xEB
    COMMAND_MOVE_1M         = 0xEA #Move 1 motor
    COMMAND_STOP_1M         = 0xE9 #Stop 1 motor
    COMMAND_BRAKE_1M        = 0xE8 #Brake 1 motor
    COMMAND_FUTURE_USE5		= 0xE7

    # Read Commands-> requests to Bot'n Roll ONE
    COMMAND_ADC0            = 0xDF #Read ADC0
    COMMAND_ADC1            = 0xDE #Read ADC1
    COMMAND_ADC2            = 0xDD #Read ADC2
    COMMAND_ADC3            = 0xDC #Read ADC3
    COMMAND_ADC4            = 0xDB #Read ADC4
    COMMAND_ADC5            = 0xDA #Read ADC5
    COMMAND_ADC6            = 0xD9 #Read ADC6
    COMMAND_ADC7            = 0xD8 #Read ADC7
    COMMAND_BAT_READ		= 0xD7 #Read ADC battery
    COMMAND_BUT_READ		= 0xD6 #Read ADC button
    COMMAND_OBSTACLES       = 0xD5 #Read IR obstacle sensors
    COMMAND_IR_SENSORS      = 0xD4 #Read IR sensors instant value
    COMMAND_ENCL            = 0xD3 #Read Encoder1 position
    COMMAND_ENCR            = 0xD2 #Read Encoder2 position
    COMMAND_ENCL_INC		= 0xD1 #Read Encoder1 Incremental value
    COMMAND_ENCR_INC		= 0xD0 #Read Encoder2 Incremental value
    COMMAND_LINE_READ		= 0xCF #Read Line Value (-100 +100)
    COMMAND_RANGE_LEFT      = 0xCE #Read IR obstacles distance range
    COMMAND_RANGE_RIGHT     = 0xCD #Read IR obstacles distance range

    # Read Commands-> Computer to Bot'n Roll ONE A
    COMMAND_ARDUINO_ANA0	= 0xBF #Read analog0 value
    COMMAND_ARDUINO_ANA1	= 0xBE #Read analog1 value
    COMMAND_ARDUINO_ANA2	= 0xBD #Read analog2 value
    COMMAND_ARDUINO_ANA3	= 0xBC #Read analog3 value
    COMMAND_ARDUINO_DIG0	= 0xBB #Read digital0 value
    COMMAND_ARDUINO_DIG1	= 0xBA #Read digital1 value
    #COMMAND_ARDUINO_DIG2	= 0xB9 #Read digital2 value
    COMMAND_ARDUINO_DIG3	= 0xB8 #Read digital3 value
    COMMAND_ARDUINO_DIG4	= 0xB7 #Read digital4 value
    COMMAND_ARDUINO_DIG5	= 0xB6 #Read digital5 value
    COMMAND_ARDUINO_DIG6	= 0xB5 #Read digital6 value
    COMMAND_ARDUINO_DIG7	= 0xB4 #Read digital7 value
    COMMAND_ARDUINO_DIG8	= 0xB3 #Read digital8 value
    COMMAND_ARDUINO_DIG9	= 0xB2 #Read digital9 value
    COMMAND_ARDUINO_DIG10	= 0xB1 #Read digital10 value
    COMMAND_ARDUINO_DIG11	= 0xB0 #Read digital11 value
    COMMAND_ARDUINO_DIG12	= 0xAF #Read digital12 value
    COMMAND_ARDUINO_DIG13	= 0xAE #Read digital13 value
    COMMAND_ARDUINO_BUZ     = 0xAD #Read Buzzer
    COMMAND_ARDUINO_CMP     = 0xAC #Read Compass
    COMMAND_ARDUINO_SNR     = 0xAB #Read Sonar
    COMMAND_ARDUINO_GRP1    = 0xAA #Read gripper1
    COMMAND_ARDUINO_GRP2    = 0x9F #Read gripper2

    LCD_CHARS_PER_LINE      = 16
    
    delayTR = 20; # 20 MinStable:15  Crash:14
    delaySS = 20; # 20 Crash: No crash even with 0 (ZERO)

    usSleep = lambda self, x: time.sleep(x / 1000000)
    msSleep = lambda self, x: time.sleep(x / 1000)
    high_byte = lambda self, x: (x >> 8) & 0xff
    low_byte = lambda self, x: x & 0xff

    def __init__(self, device): # device is the chip select pin. Set to 0 or 1, depending on the connections
        self.bus = 0    # raspberry bus
        self.device = device
        self._spi = spidev.SpiDev()
        return
        
    def open_spi(self):
        self._spi.open(self.bus, self.device)
        self._spi.max_speed_hz = 500000
        self._spi.mode = 1
        return

    def close_spi(self):
        self._spi.close()
        self.usSleep(self.delaySS)
        return
        
    def __request_byte(self, command):
        self.open_spi()
        msg = [command, self.KEY1, self.KEY2]
        self._spi.xfer2(msg)
        self.usSleep(self.delayTR)
        result = self._spi.readbytes(1)
        self.close_spi()
        return result
        
    def __request_word(self, command):
        self.open_spi()
        msg = [command, self.KEY1, self.KEY2]
        self._spi.xfer2(msg)
        self.usSleep(self.delayTR)
        high_byte = self._spi.readbytes(1)
        low_byte = self._spi.readbytes(1)
        self.close_spi()
        return ((high_byte[0] << 8) + low_byte[0])

    def __send_data(self, command, msg = ''):
        self.open_spi()
        to_send = [command, self.KEY1, self.KEY2]
        if msg != '':
            to_send.extend(msg)
        self._spi.xfer2(to_send)
        self.close_spi()
        return

    def move(self, left_speed, right_speed):
        msg = [self.high_byte(left_speed), self.low_byte(left_speed), self.high_byte(right_speed), self.low_byte(right_speed)]
        self.__send_data(self.COMMAND_MOVE, msg)
        self.msSleep(2)
        return

    def move_calibrate(self, left_power, right_power):
        msg = [self.high_byte(left_power), self.low_byte(left_power), self.high_byte(right_power), self.low_byte(right_power)]
        self.__send_data(self.COMMAND_MOVE_CALIBRATE, msg)
        self.msSleep(2)
        return

    def move_1m(self, motor, speed):
        msg = [self.low_byte(motor), self.high_byte(speed), self.low_byte(speed)]
        self.__send_data(self.COMMAND_MOVE_1M, msg)
        self.msSleep(2)
        return

    def stop(self):
        self.__send_data(self.COMMAND_STOP)
        self.msSleep(2)
        return

    def stop_1m(self, motor):
        msg = [self.low_byte(motor)]
        self.__send_data(self.COMMAND_STOP, msg)
        self.msSleep(2)
        return

    def brake(self, left_torque, right_torque):
        msg = [self.COMMAND_BRAKE, self.low_byte(left_torque), self.low_byte(right_torque)]
        self.__send_data(self.COMMAND_STOP, msg)
        self.msSleep(2)
        return

    def brake_1m(self, motor, torque):
        msg = [self.COMMAND_BRAKE, self.low_byte(motor), self.low_byte(torque)]
        self.__send_data(self.COMMAND_BRAKE_1M, msg)
        self.msSleep(2)
        return

    def brake1m(self, motor):
        msg = [self.COMMAND_BRAKE, self.low_byte(motor), self.low_byte(self.BRAKE_TORQUE)]
        self.__send_data(self.COMMAND_BRAKE_1M, msg)
        self.msSleep(2)
        return

    def reset_left_encoder(self):
        self.msSleep(2)
        return self.__send_data(self.COMMAND_ENCL_RESET)

    def reset_right_encoder(self):
        self.msSleep(2)
        return self.__send_data(self.COMMAND_ENCR_RESET)

    def led(self, state):
        state = state % 2 
        msg = [self.low_byte(state)]
        self.__send_data(self.COMMAND_LED, msg)
        self.msSleep(2)
        return

    def obstacle_emitters(self, state):
        msg = [self.low_byte(state % 2)]
        self.__send_data(self.COMMAND_IR_EMITTERS, msg)
        self.msSleep(4)
        return

    def __servo(self, command, position):
        msg = [self.low_byte(position % 2)]
        self.__send_data(command, msg)
        self.self.msSleep(2)
        return

    def servo1(self, position):
        self.__servo(self.COMMAND_SERVO1, position)
        return

    def servo2(self, position):
        self.__servo(self.COMMAND_SERVO2, position)
        return

    def __float_to_bytes(self, number):
        integer, decimal = divmod(number, 1)
        decimal = decimal * 1000
        int_high_byte = self.high_byte(integer)
        int_low_byte = self.low_byte(integer)
        dec_high_byte = self.high_byte(decimal)
        dec_low_byte = self.low_byte(decimal)
        return [int_high_byte, int_low_byte, dec_high_byte, dec_low_byte]

    def min_battery(self, batmin):
        msg = self.__float_to_bytes(batmin)
        self.__send_data(self.COMMAND_BAT_MIN, msg)
        self.msSleep(25)
        return

    def save_calibrate(self, bat, left_power, right_power):
        msg = self.__float_to_bytes(bat)
        msg.append(self.low_byte(left_power), self.low_byte(right_power))
        self.__send_data(self.COMMAND_SAVE_CALIBRATE, msg)
        self.msSleep(35)
        return

    def read_button(self):
        button = 0
        adc = self.__request_word(self.COMMAND_BUT_READ)
        if (adc >= 0 and adc < 100):	 # 0-82
            button = 1
        else:
            if (adc >= 459 and adc < 571): # 509-521
                button = 2
            else:
                if (adc >= 629 and adc < 737): # 679-687
                    button = 3
        return button

    def read_battery(self):
       return (self.__request_word(self.COMMAND_BAT_READ) / 50.7)

    def read_left_encoder(self):
        return self.__request_word(self.COMMAND_ENCL)

    def read_right_encoder(self):
        return self.__request_word(self.COMMAND_ENCR)

    def read_left_encoder_increment(self):
        return self.__request_word(self.COMMAND_ENCL_INC)

    def read_right_encoder_increment(self):
        return self.__request_word(self.COMMAND_ENCR_INC)

    def read_firmware(self):
        self.__send_data(self.COMMAND_FIRMWARE)
        self._spi.read_byte(3)
        usSleep(20)
        return

    def obstacle_sensors(self):
        return self.__request_byte(self.COMMAND_OBSTACLES)

    def read_IR_sensors(self):
        return self.__request_byte(self.COMMAND_IR_SENSORS)

    def read_left_range(self):
        return self.__request_byte(self.COMMAND_RANGE_LEFT)

    def read_right_range(self):
        return self.__request_byte(self.COMMAND_RANGE_RIGHT)

    def read_adc(self, channel):
        command = 0x00
        #match(channel):
        #    case 0:
        #        command = self.COMMAND_ADC0
        #    case 1:
        #        command = self.COMMAND_ADC1
        #    case 2:
        #        command = self.COMMAND_ADC2
        #    case 3:
        #        command = self.COMMAND_ADC3
        #    case 4:
        #        command = self.COMMAND_ADC4
        #    case 5:
        #        command = self.COMMAND_ADC5
        #    case 6:
        #        command = self.COMMAND_ADC6
        #    case 7:
        #        command = self.COMMAND_ADC7
        #    case _:
        #        command = 0x00
        return self.__request_word(command)

    def read_adc_0(self):
        return self.__request_word(self.COMMAND_ADC0)

    def read_adc_1(self):
        return self.__request_word(self.COMMAND_ADC1)

    def read_adc_2(self):
        return self.__request_word(self.COMMAND_ADC2)

    def read_adc_3(self):
        return self.__request_word(self.COMMAND_ADC3)

    def read_adc_4(self):
        return self.__request_word(self.COMMAND_ADC4)

    def read_adc_5(self):
        return self.__request_word(self.COMMAND_ADC5)

    def read_adc_6(self):
        return self.__request_word(self.COMMAND_ADC6)

    def read_adc_7(self):
        return self.__request_word(self.COMMAND_ADC7)

    def read_DBG(self, index):
        command = 0x00
        #match(index):
        #    case 0:
        #        command = 0xB9
        #    case 1:
        #        command = 0xB8
        #    case 2:
        #        command = 0xB7
        #    case 3:
        #        command = 0xB6
        return self.__request_word(command)

    # converts text to bytes with the predefined length
    # crops the text if larger than the specified length
    # and adds spaces if smaller than the specified length
    def text_to_bytes(self, text, length):
        text_length = len(text)
        if text_length < length:
            text += ((length - text_length) * ' ')
        text = text[:length]
        return text.encode('latin-1')
        
    # LCD LINE 1 Handlers
    def __lcd(self, lcd_line, text1, text2 = None, text3 = None, text4 = None):
        if text2 is None:
            #just use 1st
            text_to_send = self.text_to_bytes(str(text1), self.LCD_CHARS_PER_LINE)
        else:
            if text3 is None:
                #just use 1st and 2nd
                text_to_send = self.text_to_bytes(str(text1) + " " + str(text2), self.LCD_CHARS_PER_LINE)
            else:
                if text4 is None:    
                # just use 1st, 2nd, and 3rd
                    text_to_send = self.text_to_bytes(str(text1) + " " + str(text2) + " " + str(text3), self.LCD_CHARS_PER_LINE)
                else:
                #use all four
                    text1 = self.text_to_bytes(str(text1), int(self.LCD_CHARS_PER_LINE / 4))
                    text2 = self.text_to_bytes(str(text2), int(self.LCD_CHARS_PER_LINE / 4)) 
                    text3 = self.text_to_bytes(str(text3), int(self.LCD_CHARS_PER_LINE / 4))
                    text4 = self.text_to_bytes(str(text4), int(self.LCD_CHARS_PER_LINE / 4))
                    text_to_send = text1 + text2 + text3 + text4
                    
        self.__send_data(lcd_line, text_to_send)
        self.msSleep(4)
        return
    
    def lcd1(self, text1, text2 = None, text3 = None, text4 = None):
        self.__lcd(self.COMMAND_LCD_L1, text1, text2, text3, text4)
    
    def lcd2(self, text1, text2 = None, text3 = None, text4 = None):
        self.__lcd(self.COMMAND_LCD_L2, text1, text2, text3, text4)
