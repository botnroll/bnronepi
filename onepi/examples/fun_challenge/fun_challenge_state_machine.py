"""
 Latest update: 09-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

Description:
This example implements a finite state machine (FSM)
Each state corresponds to a different task the robot has to execute
If statements are used to evaluate condition that can trigger transitions
between states, meaning changing the task it has to perform.
e.g. if the robot is attacking (moving forward) and detects an obstacle it then
changes the state to retreat (start moving backwards)
"""

import time
import signal
import threading
from onepi.one import BnrOneAPlus
from enum import Enum, auto

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

TIMER_INTERVAL = 1  # Set the timer interval in seconds


# Define possible states
class State(Enum):
    ATTACK = auto()
    RETREAT = auto()
    WAIT_PICK_UP = auto()
    WAIT_PUT_DOWN = auto()


# initial state
state = State.ATTACK


def setup():
    one.stop()  # stop motors
    one.lcd1("  FUN CHALLENGE ")  # print on LCD line 1
    one.lcd2(" Press a button!")  # print on LCD line 1
    while one.read_button() == 0:
        time.sleep(0.050)

def get_average_reading():
    """
    sensor[0] is the value of sensor 0
    sensor[1] is the value of sensor 1
    ...
    average stores the average value of the 8 line sensors
    """
    average = 0
    sensor = [0] * 8
    # read line sensors
    for i in range(8):
        sensor[i] = one.read_adc(i)
        average += sensor[i] / 8

    return int(average)

def loop():
    global state

    average = get_average_reading()
    speed = 80
    if (state == State.ATTACK):  # moves forward until it detects the midfield line or obstacles
        one.move(speed, speed)
        # upon detection of an obstacle it changes it's task to retreat
        if one.obstacle_sensors() > 0:
            state = State.RETREAT

        # if it detects an average above 900 (all sensors detecting black) it changes
        # task to retreat
        if average > 900:
            state = State.RETREAT

    elif state == State.RETREAT:  # moves backwards until sensors detect white
        one.move(-speed, -speed)
        # if the average is below 100 (all sensors detecting white),
        # move backwards for the user to pick it up
        if average < 100:
            state = State.WAIT_PICK_UP

    elif state == State.WAIT_PICK_UP:  # moves backwards until gets picked up
        one.move(-speed, -speed)
        # if the average is above 900 (all sensors detecting black),
        # means the robot has been picked up and it changes its task to move forward
        if average > 900:
            state = State.WAIT_PUT_DOWN

    elif state == State.WAIT_PUT_DOWN:
        # moves forward untill all sensors detect white (robot placed back on the arena)
        one.move(speed, speed)
        # if the average drops below 100 (all sensors detecting white),
        # changes the task to attack
        if average < 100:
            state = State.ATTACK
    print("average reading = ", average, " state = ", state, end="          \r")


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
