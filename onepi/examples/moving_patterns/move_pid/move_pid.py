"""
This example shows how to use a PID controller to control the wheel speeds of Bot'n Roll ONE A
The minimum speed is about 250 mm/s and the max speed is 850 mm/s for a reference battery of 12V.
Note that these values might change depending on the battery you're using and its current charge.
You can specify your own PID params, kp, ki, kd.
This example uses the default values and an update period of 200ms.
Note if you change the update period you need to tune the PID params.
Important: Please run motors calibrate routine but instead of setting the power to when
the wheels start moving set it to when they stop moving.
This allows PID more room to control the speeds at lower values.
"""

from onepi.utils.pid_controller import PIDController
from onepi.utils.control_utils import ControlUtils
from onepi.utils.simple_timer import SimpleTimer
from onepi.one import BnrOneA
import RPi.GPIO as GPIO
import csv

import matplotlib.pyplot as plt
import time
import datetime

GPIO.setmode(GPIO.BCM)
left_dir = 22 #DirL
right_dir = 23 #DirR
GPIO.setup(left_dir, GPIO.IN)
GPIO.setup(right_dir, GPIO.IN)

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

# Define variables
left_speed = 0
right_speed = 0
previous_left_speed = 0
previous_right_speed = 0
milliseconds_update = 100
counter = 0

AXIS_LENGHTH_MM = 163.0
WHEEL_DIAMETER_MM = 65.0
TICKS_PER_REV = 1490
MIN_SPEED_MMPS = 0
MAX_SPEED_MMPS = 850

left_pid = PIDController(0.0, 0.0, 0.0, 0.0, 100)
kp = 0.02
ki = 0.70
kd = 0.03

right_pid = PIDController(kp, ki, kd, -850, 850)
cut = ControlUtils(AXIS_LENGHTH_MM, WHEEL_DIAMETER_MM, TICKS_PER_REV)

speed_ref = 300 #mmps
elapsed_time = []
right_speed_plot = []
ref_speed_plot = []

print(elapsed_time)
print(right_speed_plot)

fig, ax = plt.subplots()
line, = ax.plot(elapsed_time, right_speed_plot)  # Create a line object for the plot

data = []
def write_to_csv():
    global data
    print("Writing csv file step_data.csv")
    with open('step_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        
def print_pair(text, value1, value2):
    """
    prints pair of values
    """
    print(text, value1, ",", value2)


def print_value(text, value):
    """
    prints value
    """
    print(text, value)

def maybe_set_to_zero(current, previous):
    """
    detects when current value is of different sign from previous
    returns 0 if they are of different sign
    returns current value otherwise
    """
    if ((current * previous) < 0) and (previous != 0):
        print ("========= WARNING: set to zero ========")
        print("previous: ", previous)
        print("current: ", current)
        return 0  # return 0 as there was a change of sign
        
    return current


def compute_left_speed():
    """
    computes left speed
    """
    global left_speed, previous_left_speed, milliseconds_update
    left_encoder = one.read_left_encoder()
    left_encoder = cut.maybe_change_sign(left_encoder, left_speed, previous_left_speed)
    
    left_speed_mmps = cut.compute_speed_from_ticks(left_encoder, milliseconds_update)
    left_speed = left_pid.compute_output(left_speed_mmps)
    left_speed = maybe_set_to_zero(left_speed, previous_left_speed)
    previous_left_speed = left_speed
    #print("left_speed = ", left_speed)
    
    return left_speed


def compute_right_speed():
    """
    computes right speed
    """
    global right_speed, previous_right_speed, elapsed_time, right_speed_plot, counter
    global ref_speed_plot, speed_ref, milliseconds_update, my_timer, data
    right_encoder = one.read_right_encoder()
    direction = (GPIO.input(right_dir) * 2) - 1
    right_encoder = right_encoder * direction
    print("right_encoder =", right_encoder)
    right_speed = right_pid.compute_output(right_encoder)
    previous_right_speed = right_speed
    
    current_speed_mmps = cut.compute_speed_from_ticks(right_encoder, milliseconds_update)
    elapsed_time.append(int(counter * milliseconds_update))
    right_speed_plot.append(int(current_speed_mmps))
    ref_speed_plot.append(speed_ref)
    timestamp = my_timer.get_time()
    data.append([timestamp, speed_ref, right_encoder])
    
    counter = counter + 1
    
    return right_speed


def update_speeds():
    """
    update wheel speeds
    """
    global left_speed, right_speed
    left_speed = compute_left_speed()
    right_speed = compute_right_speed()
    one.move(0, right_speed)
    


def convert_to_mmps(desired_speed):
    """
    converts desired speed in percentage to real speed in mmps
    """
    if desired_speed == 0:
        return 0

    if desired_speed < 0:
        return cut.convert_range(
            desired_speed, -100, 0, -MAX_SPEED_MMPS, -MIN_SPEED_MMPS
        )

    if desired_speed > 0:
        return cut.convert_range(desired_speed, 0, 100, MIN_SPEED_MMPS, MAX_SPEED_MMPS)
    
    return 0

def test_move():
    print("wait 2s")
    time.sleep(1)
    # change the setpoint speed
    print("==== change setpoint ====")
    desired_speed = 10
    desired_speed_mmps = convert_to_mmps(desired_speed)
    print ("desired_speed_mmps= ", desired_speed_mmps)
    ref_ticks = cut.compute_ticks_from_speed(desired_speed_mmps, milliseconds_update)
    left_pid.change_set_point(ref_ticks)
    right_pid.change_set_point(ref_ticks)
    print_value("ref_ticks: ", ref_ticks)
    time.sleep(2)
    print("==== done ====")
    
def set_desired_speed(desired_speed_mmps=500):    
    ref_ticks = cut.compute_ticks_from_speed(desired_speed_mmps, milliseconds_update)
    print("=== > desired_speed_mmps= ", desired_speed_mmps, " ref_ticks: ", ref_ticks)
    left_pid.change_set_point(ref_ticks)
    right_pid.change_set_point(ref_ticks)

my_timer = SimpleTimer(increment=milliseconds_update/1000.0, function=update_speeds)

def plot_pid():
    global line, ax, fig, plt
    global elapsed_time, right_speed_plot
    global ref_speed_plot, speed_ref, my_timer
    one.stop()
    one.min_battery(10.5)
    one.lcd1("....MovePID.....")
    one.lcd2(".....Start......")

    one.reset_left_encoder()
    one.reset_right_encoder()
    my_timer.start()
    # zero
    speed_ref = 100
    set_desired_speed(speed_ref)
    time.sleep(5)
    # 300
    speed_ref = 200
    set_desired_speed(speed_ref)
    time.sleep(5)
    # 0
    speed_ref = 300
    set_desired_speed(speed_ref)
    time.sleep(4)
    # -300
    speed_ref = 400
    set_desired_speed(speed_ref)
    time.sleep(4)
    # zero
    speed_ref = 500
    set_desired_speed(speed_ref)
    time.sleep(3)
    # 600
    speed_ref = 300
    set_desired_speed(speed_ref)
    time.sleep(5)
    # 0
    speed_ref = 200
    set_desired_speed(speed_ref)
    time.sleep(5)
    # -600
    speed_ref = 100
    set_desired_speed(speed_ref)
    time.sleep(5)
    # 0
    speed_ref = 50
    set_desired_speed(speed_ref)
    time.sleep(5)
    
    my_timer.stop()
    time.sleep(0.2)
    one.stop()
    write_to_csv()
    
    # Plotting the first line
    plt.plot(elapsed_time, ref_speed_plot, label='Ref')

    # Plotting the second line
    plt.plot(elapsed_time, right_speed_plot, label='PID')

    # Adding labels and title
    plt.xlabel('time (ms)')
    plt.ylabel('speed (mm/s)')
    title = "PID Control kp:"+str(kp)+" ki:"+str(ki)+" kd:"+str(kd)
    plt.title(title)

    # Adding a legend
    plt.legend()

    date_now = datetime.datetime.now()
    fig_name = str(date_now)+"PID_control.png"
    # Displaying the plot
    plt.savefig(fig_name, bbox_inches='tight')
    plt.savefig("PID_control.png", bbox_inches='tight')
    #plt.show()

def test_encoder_dir():
    one.stop()
    for i in range(0,100):        
        time.sleep(0.2)
        direction = GPIO.input(right_dir)
        print("direction",direction)
    write_to_csv()
    
def setup():
    """
    setup method
    """
    plot_pid()
    #test_encoder_dir()
    
def loop():
    """
    loop method
    """
    one.stop()
    time.sleep(1)


def main():
    setup()
    #while True:
    #    loop()


if __name__ == "__main__":
    main()