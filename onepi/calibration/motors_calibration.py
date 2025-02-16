"""
This example acquires motor and encoder information to be sent to PIC18F45K22 for PID control.
The robot wheels must rotate freely and should not touch the floor. Motors must have encoders.
This process is done in 3 steps:
Step 1: PMW will increase from 0 until movement is detected by the encoders.
Step 2: With motors at maximum power, encoders counting will be acquired every 25 ms.
Step 3: send data to PIC to be stored in EEPROM
"""

import time
import signal
from onepi.one import BnrOneAPlus

one = BnrOneAPlus(0, 0)  # object to control Bot'n Roll ONE A+
motor_power  =  20
left_encoder_max  =  0
right_encoder_max  =  0
error_flag  =  False
ks  =  750
ONE_SEC = 1
FIVE_SEC = 5
HUNDRED_MS = 0.1
def start_movement_detection():
    global motor_power, left_encoder_max, right_encoder_max, error_flag, ks
    exit_flag = False
    left_encoder = one.read_left_encoder()       # Clear encoder count
    right_encoder = one.read_right_encoder()     # Clear encoder count
    t1sec = time.time() + ONE_SEC

    while(not exit_flag):

        if(time.time() >=  t1sec):
            t1sec +=  ONE_SEC   # Every second
            one.move_raw(motor_power, motor_power)
            left_encoder = one.read_left_encoder()
            right_encoder = one.read_right_encoder()
            one.lcd2(motor_power, left_encoder, right_encoder)
            print("Pow:", motor_power, "  left_encoder:", left_encoder, "  right_encoder:", right_encoder)

            if((abs(left_encoder) < 100) or (abs(right_encoder) < 100)):
                motor_power += 1 # if motors are not moving
            else:
                if(left_encoder < 0): # if left_encoder is Not ok
                    one.lcd1("Motor 1 -> ERROR")
                    print("ERROR: Motor 1 encoder is counting in reverse!!")
                    error_flag = True

                elif(right_encoder < 0): # if encoderR is Not ok
                    one.lcd2("Motor 2 -> ERROR")
                    print("ERROR: Motor 2 encoder is counting in reverse!!")
                    error_flag = True

                exit_flag = True


def max_pulses_detection():
    global left_encoder_max, right_encoder_max
    t_cycle = 0
    end_time = 0
    if(not error_flag):
        one.lcd2(100, 0, 0)
        one.move_raw(100, 100)
        time.sleep(1.5)
        t_cycle = time.time()
        end_time = time.time() + FIVE_SEC
        left_encoder = one.read_left_encoder() # Clear encoder count
        right_encoder = one.read_right_encoder() # Clear encoder count
        while(time.time() < end_time):
            if(time.time() >= t_cycle):
                t_cycle += HUNDRED_MS
                left_encoder = one.read_left_encoder()
                right_encoder = one.read_right_encoder()
                if(left_encoder > left_encoder_max):
                    left_encoder_max = left_encoder
                if(right_encoder > right_encoder_max):
                    right_encoder_max = right_encoder
                print("  left_encoder:", left_encoder, "  right_encoder:", right_encoder)

        one.stop()
        one.lcd2(0, left_encoder_max, right_encoder_max)
        print("  left_encoder_max:", left_encoder_max)
        print("  right_encoder_max:", right_encoder_max)
        time.sleep(2.0)


def send_values():
    enc_min = 30000  # Find minimum encoder value
    if(not error_flag):
        if(left_encoder_max < enc_min):
            enc_min = int(left_encoder_max / 4.0)
        if(right_encoder_max < enc_min):
            enc_min = int(right_encoder_max / 4.0)
        one.set_motors(motor_power, ks, enc_min)
        print("Save values for def setMotors(int Smotor_power, int Ks, int ctrlPulses)")
        print("Set motor pow:", motor_power, "  ctrl pulses:", enc_min)
        print("Calibration Finished!!")
        while(True):
            one.lcd1("Set motor pow:", motor_power)
            one.lcd2("ctrl pulses:  ", enc_min)
            time.sleep(2.5)
            one.lcd1("Save values for ")
            one.lcd2("  set motors    ")
            time.sleep(2.5)
            one.lcd1("  Calibration   ")
            one.lcd2("   finished!    ")
            time.sleep(2.5)
    while(True):
        pass


def setup():
    one.stop()
    one.set_min_battery_V(9.5)  # set minimum value for battery
    one.lcd1(" Press a button ")
    one.lcd2("   to start     ")
    while(one.read_button() == 0):
        time.sleep(10 / 1000)
    one.lcd1("Motor calibrate ")
    one.lcd2(" !!Attention!!  ")
    time.sleep(2)
    one.lcd1("wheel must not  ")
    one.lcd2("touch the floor!")
    time.sleep(2)
    one.lcd1(" Press a button ")
    one.lcd2("   to start     ")
    while(one.read_button() == 0):
        time.sleep(10 / 1000)
    one.lcd1("Power left_encoder right_encoder ")

def loop():
    # 1 - Detect Start Moving Power
    start_movement_detection()
    # 2 - Detect control pulses at max speed every 25ms
    max_pulses_detection()
    # 3 - Send values to PIC18F45K22
    send_values()

def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    loop()


if __name__ == "__main__":
    main()
