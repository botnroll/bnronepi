"""
 This code example is in the public domain.
 http://www.botnroll.com

 Description:
 This program detects automatic start and does the automatic end on the RoboParty Fun Challenge.

"""

import time
from one import BnrOneA

one = BnrOneA(0, 0) # object variable to control the Bot'n Roll ONE A
counter = 0
challenge_time = 90


def automatic_start():
    active = one.read_ir_sensors()          # read IR sensors
    result = False
    if not active:                          # If not active
        tempo_A = time.time()               # read time
        while not active:                   # while not active
            active = one.read_ir_sensors()  # read actual IR sensors state
            elapsed_time = time.time() - tempo_A
            if elapsed_time > 0.050:        # if not active for more than 50ms
                result = True               # start Race
                break
    return result


def initialize_timer():
  # set timer1 interrupt at 1Hz
  # ToDo
  pass


def ISR(TIMER1_COMPA_vect):       # timer1 interrupt 1Hz
  if (counter >= challenge_time):
    one.lcd2("END OF CHALLENGE")  # print on LCD line 2
    while(True)                   # does not allow anything else to be done after the challenge ends
      one.brake(100, 100)         # Stop motors with torque
                                  # place code here, to stop any additional actuators...
  else:
    one.lcd2(counter)             # print the challenge time on LCD line 2
  counter += 1


def setup():
  on = 1
  off = 0
  one.stop()                      # stop motors
  initialize_timer()              # configures the interrupt timer for the end of the challenge
  one.lcd1("FUN CHALLENGE")       # print on LCD line 1
  one.lcd2("READY TO START..")    # print on LCD line 2
  one.obstacle_emitters(off)      # deactivate obstacles IR emitters
  time.sleep(4)                   # time to stabilize IR sensors (DO NOT REMOVE!!!)
  start = 0
  while(not start):
    start = automatic_start()

  TIMSK1 |= (1 << OCIE1A)         # enable timer compare interrupt
  one.obstacle_emmitters(on)      # deactivate obstacles IR emitters

def loop():
    # place code here, to control the robot ...
    pass

def main():
    setup()
    while True:
        loop()