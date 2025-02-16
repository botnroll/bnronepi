"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 This program detects automatic start and does the automatic end on the RoboParty Fun Challenge.

"""

import time
import threading
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

TIMER_INTERVAL = 1  # Set the timer interval in seconds

counter = 0
challenge_time = 90  # challenge time
stop_flag = False  # Flag to indicate if the timer thread should stop


def start_timer(interval):
    global stop_flag
    while not stop_flag:
        time.sleep(interval)
        check_timeout()


# Create a thread for the timer
timer_thread = threading.Thread(target=start_timer, args=(TIMER_INTERVAL,))
timer_thread.daemon = True


def check_timeout():
    global counter
    global stop_flag
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


def check_end():
    one.lcd2(counter)  # print the challenge time on LCD line 2
    print("Counter:", counter, end="  \r")
    if stop_flag:
        one.lcd2("END OF CHALLENGE")  # print on LCD line 2
        print("END OF CHALLENGE")
        while True:  # does not allow anything else to be done after the challenge ends
            one.brake(100, 100)  # Stop motors with torque
            # place code here, to stop any additional actuators...


def loop():
    check_end()

    one.move(80, 80)
    time.sleep(1.5)
    one.move(-80, -80)
    time.sleep(2)


def main():
    try:
        setup()
        while True:
            loop()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
