"""
This code example is in the public domain.
 http://www.botnroll.com

Description:
Read obstacle sensors range distance for left and right IR sensors.
Range varies from 0 to 25:
 -> 0 means no obstacle is detected
 -> 25 means obstacle is very close to the sensor
The robot has new readings every 25ms (40 readings per second)
Note: Valid for TSSP4056 sensors shipped with robots from 2023.
"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)             # object variable to control the Bot'n Roll ONE A

left_motor = 0
right_motor = 0
kL = 2.70                       # Linear gain
vel = 60

def setup():
    on = 1
    one.stop()                  # stop motors
    one.obstacleEmitters(on)    # activate IR emitters
    one.lcd1("Obstacles  Range")
    one.lcd2("Press a Button!!")
    while(one.read_button() == 0)  # Wait a button to be pressed
    while(one.read_button() != 0)  # Wait for button release


def loop():
    left_range = one.read_left_range()      # read left obstacle sensor range
    right_range = one.read_right_range()    # read right obstacle sensor range
    one.lcd1("Range Left : ",left_range)
    one.lcd2("Range Right: ",right_range)

    if(left_range>right_range):
        right_motor=(vel-(left_range*kL))
        left_motor=vel

    elif(left_range < right_range):
        right_motor=vel
        left_motor=(vel-(right_range * kL))

    elif(left_range==right_range):
        right_motor=vel
        left_motor=vel

    one.move(left_motor, right_motor)
    time.sleep(0.025) # The robot has new readings every 25ms (40 readings per second)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()