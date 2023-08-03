###########################################################################
##############################     TEST     ###############################
###########################################################################

from onepi import onepi
import functools
import time

print = functools.partial(print, flush=True)

msSleep = lambda x: time.sleep(x / 1000)

def blink(bnrOneA, number_of_times, duration_ms):
    state = 0
    for i in range (number_of_times):
        state = (state + 1) % 2
        print("LED: ", state)
        bnrOneA.led(state)
        msSleep(duration_ms)

def scroll_text(text):
    for char in text:
        yield char

def lcd_scroll(text):
    text_to_send = "                " + text  + "                "
    for i in range (17 + len(text)):
        text = text_to_send[i:i+16]
        yield text

def test_scroll_text(bnrOneA):
    text = "Hi Raspberry Pi!"
    for text in lcd_scroll(text):
        print(text, end="\n")
        bnrOneA.lcd2(text)
        msSleep(200)
    print(" ")
    
def test_read_button(bnrOneA):
    print("Press a button")
    for i in range(100):
        print (bnrOneA.read_button())
        msSleep(300)
    return 0

def test_lcd(bnrOneA):
    bnrOneA.lcd1("")
    bnrOneA.lcd2("Hi Raspberry Pi!")
    msSleep(2000)
    bnrOneA.lcd1("Hi Raspberry Pi!")
    bnrOneA.lcd2("Day:", 31, "7", 2023)
    msSleep(2000)
    bnrOneA.lcd1("Day:", 31, "7", 2023)
    bnrOneA.lcd2(17, "h", 15, "min")
    msSleep(2000)
    bnrOneA.lcd1(17, "h", 15, "min")
    bnrOneA.lcd2("Ver.", 1, "Sub.", 3)
    msSleep(2000)
    bnrOneA.lcd1("Ver.", 1, "Sub.", 3)
    bnrOneA.lcd2("Test number:", 1)
    msSleep(2000)
    bnrOneA.lcd1("Test number:", 1)
    bnrOneA.lcd2("System", "test:", 1)
    msSleep(2000)
    bnrOneA.lcd1("System", "test:", 1)
    bnrOneA.lcd2(1234567890123456)
    msSleep(2000)
    bnrOneA.lcd1(1234567890123456)
    bnrOneA.lcd2(12345678, 1234567)
    msSleep(2000)
    bnrOneA.lcd1(12345678, 1234567)
    bnrOneA.lcd2(12345, 12345, 1234)
    msSleep(2000)
    bnrOneA.lcd1(12345, 12345, 1234)
    bnrOneA.lcd2(1111,2222,3333,4444)
    msSleep(2000)
    bnrOneA.lcd1(1111,2222,3333,4444)
    bnrOneA.lcd2("      END       ")
    msSleep(2000)
    bnrOneA.lcd1("      END       ")
    bnrOneA.lcd2("")
    
def main() -> int:    
    
    bnrOneA = onepi.BnrOneA(0, 0) # creates a BotnRoll interface with spi in channel 0
    
    print("battery = ", bnrOneA.read_battery())
    blink(bnrOneA, 6, 200)
    test_scroll_text(bnrOneA)
    test_read_button(bnrOneA)
    #test_lcd(bnrOneA)
    
    # functions to test:
    
    #open_spi(self):
    #close_spi(self):
    #__request_byte(self, command):
    #__request_word(self, command):
    #__send_data(self, command, msg = ''):
    #move(self, left_speed, right_speed):
    #move_calibrate(self, left_power, right_power):
    #move_1m(self, motor, speed):
    #stop(self):
    #stop_1m(self, motor):
    #brake(self, left_torque, right_torque):
    #brake_1m(self, motor, torque):
    #brake1m(self, motor):
    #reset_left_encoder(self):
    #reset_right_encoder(self):
    #led(self, state):
    #obstacle_emitters(self, state):
    #__servo(self, command, position):
    #servo1(self, position):
    #servo2(self, position):
    #__float_to_bytes(self, number):
    #min_battery(self, batmin):
    #save_calibrate(self, bat, left_power, right_power):
    #read_button(self):
    #read_battery(self):
    #read_left_encoder(self):
    #read_right_encoder(self):
    #read_left_encoder_increment(self):
    #read_right_encoder_increment(self):
    #read_firmware(self):
    #obstacle_sensors(self):
    #read_IR_sensors(self):
    #read_left_range(self):
    #read_right_range(self):
    #read_adc(self, channel):
    #read_adc_0(self):
    #read_adc_1(self):
    #read_adc_2(self):
    #read_adc_3(self):
    #read_adc_4(self):
    #read_adc_5(self):
    #read_adc_6(self):
    #read_adc_7(self):
    #read_DBG(self, index):
    #text_to_bytes(self, text, length):
    #__lcd(self, lcd_line, text1, text2 = None, text3 = None, text4 = None):
    #lcd1(self, text1, text2 = None, text3 = None, text4 = None):
    #lcd2(self, text1, text2 = None, text3 = None, text4 = None):
if __name__ == '__main__':
    main()
