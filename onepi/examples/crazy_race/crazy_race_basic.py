"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 This program detects a button click and moves for the RoboParty Fun Challenge.

"""

import time
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

def setup():
    one.stop()  # stop motors
    one.lcd1("   CRAZY RACE   ")  # print on LCD line 1

left_speed, right_speed = 0, 0
speed = 20

g_obstacle_gain = 2.0
left_range = 0      # Left obstacle sensor range
right_range = 0     # Right obstacle sensor range
max_range = 18  # Maximum range value for obstacle
min_range = 1   # Minimum range value for obstacle

line_gain = 1.0;  # Line linear gain <> Ganho linear da linha
extra_speed = 8;    # Curve outside wheel max g_speed limit <> Limite de

def cap_value(value, lower_limit, upper_limit):
    """
    Caps the value to lower and upper limits
    """
    if value < lower_limit:
        return lower_limit
    elif value > upper_limit:
        return upper_limit
    else:
        return value

def read_and_process_line():
    global left_speed, right_speed
    line = one.read_line()
    left_speed = speed + (line * line_gain)
    right_speed = speed - (line * line_gain)

    left_speed = cap_value(left_speed, -15, speed + extra_speed)
    right_speed = cap_value(right_speed, -15, speed + extra_speed)


def read_and_process_obstacles():
    global left_speed, right_speed
    left_range = one.read_left_range()
    right_range = one.read_right_range()

    if (left_range >= max_range):
        right_speed = -speed
        left_speed = speed
    
    elif (right_range >= max_range):
        right_speed = speed
        left_speed = -speed
    
    if ((left_range <= min_range) and (right_range <= min_range)):
        right_speed = speed
        left_speed = speed
    
    else:
        if (left_range > right_range):
            left_speed = (speed + (left_range / 2.0))
            right_speed = (speed - (left_range * g_obstacle_gain))
            if (right_speed < -speed):
                right_speed = -speed
            
        else:
            right_speed = (speed + (right_range / 2.0))
            left_speed = (speed - (right_range * g_obstacle_gain))
            if (left_speed < -speed):
                left_speed = -speed
            

def isAllDark(readings, threshold):
    for i in range(8):
        if (readings[i] < threshold):
            return False
    return True


def loop():
    global left_speed, right_speed
    if (isAllDark(one.read_line_sensors(), 450)):
        read_and_process_obstacles()
    else:
        read_and_process_line()
    one.move(left_speed, right_speed)
    
    
def main():
    try:
        setup()
        while True:
            loop()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
