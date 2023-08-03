
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
    
    bnrOneA = onepi.BnrOneA(0) # creates a BotnRoll interface with spi in channel 0
    
    print("battery = ", bnrOneA.read_battery())
    blink(bnrOneA, 6, 200)
    test_scroll_text(bnrOneA)
    test_read_button(bnrOneA)
    #test_lcd(bnrOneA)
        
if __name__ == '__main__':
    main()
