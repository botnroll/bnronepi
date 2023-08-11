"""
This code example is in the public domain. 
 http://www.botnroll.com

Description:
Read obstacle sensors range distance for left and right IR sensors.
Range varies from 0 to 25:
 -> 0 means no obstacle is detected
 -> 25 means obstacle is very close to the sensor
The robot has new readings every 25ms (40 readings per second)
Note: Valid for TSSP4056 IR sensors shipped with robots from 2023.
""" 

import time
from one import BnrOneA

BnrOneA one           # declaration of object variable to control the Bot'n Roll ONE A

# constants definition

def setup():    
    one.stop()                      # stop motors
    one.obstacleEmitters(ON)        # activate IR emitters

def loop():
    rangeL = one.readangeL()        # read left obstacle sensor range 
    rangeR = one.read_rangeR()      # read right obstacle sensor range
    one.lcd1("Range Left : ",rangeL)
    one.lcd2("Range Right: ",rangeR)
    print("L: ", rangeL, "   R: ", rangeR)
    time.sleep(0.025) # The robot has new readings every 25ms (40 readings per second)



def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
