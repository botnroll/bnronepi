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
import threading
from onepi.one import BnrOneA
from enum import Enum, auto

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

TIMER_INTERVAL = 1  # Set the timer interval in seconds

counter = 0
challenge_time = 90  # challenge time (s)
stop_flag = False  # Flag to indicate if the timer thread should stop


# Define possible states
class State(Enum):
    ATTACK = auto()
    RETREAT = auto()
    WAIT_PICK_UP = auto()
    WAIT_PUT_DOWN = auto()


# initial state
state = State.ATTACK


def start_timer(interval):
    global stop_flag
    while not stop_flag:
        time.sleep(interval)
        check_timeout()


# Create a thread for the timer
timer_thread = threading.Thread(target=start_timer, args=(TIMER_INTERVAL,))
timer_thread.daemon = True


def check_timeout():
    global counter, stop_flag
    if counter >= challenge_time:
        stop_flag = True
    else:
        counter += 1


def automatic_start():
    active = one.read_ir_sensors()  # read IR sensors
    result = False
    if not active:  # If not active
        start_time = time.time()  # read time
        while not active:  # while not active
            active = one.read_ir_sensors()  # read actual IR sensors state
            elapsed_time = time.time() - start_time
            if elapsed_time > 0.050:  # if not active for more than 50ms
                result = True  # start Race
                break
    return result


def setup():
    on = 1
    off = 0
    one.stop()  # stop motors
    one.lcd1("FUN CHALLENGE")  # print on LCD line 1
    one.lcd2("READY TO START..")  # print on LCD line 2
    one.obstacle_emitters(off)  # deactivate obstacles IR emitters
    time.sleep(4)  # time to stabilize IR sensors (DO NOT REMOVE!!!)
    start = 0
    while not start:
        start = automatic_start()
    timer_thread.start()  # start timer
    one.obstacle_emitters(on)  # activate obstacles IR emitters


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


def check_end():
    one.lcd2(counter)  # print the challenge time on LCD line 2
    if stop_flag:
        one.lcd2("END OF CHALLENGE")  # print on LCD line 2
        print("\nEND OF CHALLENGE")
        while True:  # does not allow anything else to be done after the challenge ends
            one.brake(100, 100)  # Stop motors with torque
            # place code here, to stop any additional actuators...


def loop():
    global state
    check_end()

    average = get_average_reading()
    speed = 80
    if (
        state == State.ATTACK
    ):  # moves forward until it detects the midfield line or obstacles
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
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
