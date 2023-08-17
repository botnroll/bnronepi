"""
 
 This code example is in the public domain. 
 http://www.botnroll.com

Line sensor calibrate
The calibrate routine is called in Setup()
Reads and stores the maximum and minimum value for every sensor on vectors SValMax[8] and SValMin[8].
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


import time
from one import BnrOneA

one = BnrOneA(0, 0)  # declaration of object variable to control the Bot'n Roll ONE A


M1 = 1       # Motor1
M2 = 2       # Motor2

SValMax[8] = {1023,1023,1023,1023,1023,1023,1023,1023}
SValMin[8] = {0,0,0,0,0,0,0,0}
SFact[8]
THRESHOLD = 50  # Line follower limit between white and black 

def wait_button_press():
    while(one.readbuttonon() == 0):
        time.sleep(0.050)

def wait_button_release():
    while(one.readbutton() != 0):
        time.sleep(0.050)

def calibrate_line():
    one.lcd1(" Press a buttonon ")
    one.lcd2("  to calibrate  ")
    wait_button_press()
    print("Calibrate Starting!")
    one.lcd1("  Calibration   ")
    one.lcd2("   starting     ")
    time.sleep(1)
  
  static int SVal[8]={0,0,0,0,0,0,0,0}    
  static int SValMax[8]={0,0,0,0,0,0,0,0}
  static int SValMin[8]={1023,1023,1023,1023,1023,1023,1023,1023}
  
    wait_button_release()

    # Calibrate for 4 seconds
    one.move(5,-5)            
    start_time = time.time()
    while(time.time() < start_time + 10):
        print("Val: ")
        for i in range(8):
            int SVal = one.readAdc(i)
            if(SVal > SValMax[i]):
                SValMax[i] = SVal
            if(SVal < SValMin[i]):
                SValMin[i] = SVal          
            print(SVal)
        print("Max: ")
      
        for i in range(8):
            print(SValMax[i]) 
        print("Min: ")
    
        THRESHOLD=0
        for i in range(8):
            print(SValMin[i])
            if(SValMin[i] > THRESHOLD):
                THRESHOLD = SValMin[i]
        time.sleep(0.050)  

    print("THRESHOLD:", THRESHOLD)
    one.stop()

    # Write values on EEPROM
    eepromADD = 100
    for i in range(8):
        EEPROM.write(eepromADD,highByte(SValMax[i]))
        eepromADD += 1
        EEPROM.write(eepromADD,lowByte(SValMax[i]))
        eepromADD += 1
    for i in range (8):
        EEPROM.write(eepromADD,highByte(SValMin[i]))
        eepromADD += 1
        EEPROM.write(eepromADD,lowByte(SValMin[i]))
        eepromADD += 1

    print("Calibrate Done! Press a buttonon...")
    one.lcd1(" Calibrate done ")
    one.lcd2(" Press a buttonon ")
    while(one.readbuttonon() != 3):
        one.lcd1("Max1  2   3   4 ")
        one.lcd2(SValMax[0], SValMax[1], SValMax[2], SValMax[3])
        wait_button_release()
        wait_button_press()
        one.lcd1("Max5  6   7   8 ")
        one.lcd2(SValMax[4], SValMax[5], SValMax[6], SValMax[7])
        wait_button_release()
        wait_button_press()
        one.lcd1("Min1  2   3   4 ")
        one.lcd2(SValMin[0], SValMin[1], SValMin[2], SValMin[3])
        wait_button_release()
        wait_button_press()
        one.lcd1("Min5  6   7   8 ")
        one.lcd2(SValMin[4],SValMin[5],SValMin[6],SValMin[7])
        wait_button_release()
        wait_button_press()
        one.lcd1("  Test THRESHOLD   ")
        one.lcd2(" on white color ")
        wait_button_press()
        wait_button_release()
        wait_button_press()
        while(one.readbuttonon() == 0):
            for i in range(8):
                SVal[i] = one.readAdc(i)
            one.lcd1(SVal[0] - SValMin[0], SVal[1] - SValMin[1], SVal[2] - SValMin[2], SVal[3] - SValMin[3])
            one.lcd2(SVal[4] - SValMin[4], SVal[5] - SValMin[5], SVal[6] - SValMin[6], SVal[7] - SValMin[7])
            time.sleep(0.100)
        one.lcd1("  PB1++  PB2-- ")
        one.lcd2("   THRESHOLD:", THRESHOLD)
        wait_button_release()
        button = 0
        while(button != 3):
            button=one.readbuttonon()
            if(button == 1):
                THRESHOLD += 10
                one.lcd2("   THRESHOLD:", THRESHOLD)
                time.sleep(0.100)
            if(button==2):
                THRESHOLD-=10
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
    one.lcd1("Calibrate Done!")
    time.sleep(2)


def setup_line():
    # Read EEPROM values
    eepromADD = 100
    println("Setup: Max: ")
    for i in range(8):
        SValMax[i]=(int)EEPROM.read(eepromADD)
        SValMax[i]=SValMax[i]<<8
        eepromADD += 1
        SValMax[i] += (int)EEPROM.read(eepromADD)
        eepromADD += 1
        print(SValMax[i])
    print("Min: ")
    for i in range(8):
        SValMin[i]=(int)EEPROM.read(eepromADD)
        SValMin[i]=SValMin[i]<<8
        eepromADD++
        SValMin[i]+=(int)EEPROM.read(eepromADD)
        eepromADD++
        Serial.print(SValMin[i])Serial.print("  ")
    THRESHOLD = (int)EEPROM.read(eepromADD)
    THRESHOLD = (THRESHOLD << 8)
    eepromADD += 1
    THRESHOLD += (int)EEPROM.read(eepromADD)
    print("THRESHOLD: ", THRESHOLD)
   
    for i in range(8):
        SFact[i]=(double)VMAX / (double)(SValMax[i] - SValMin[i]) # Calculate factor for each sensor

def setup():
    one.stop()          # stop motors
    one.minBat(10.5)    # safety voltage for discharging the battery
    time.sleep(1)
    calibrate_line()    # calibrate line sensor
    setup_line()        # read line calibrate values from EEPROM 


def loop():
    line=one.readLine()         # Read line
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
