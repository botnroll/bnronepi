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

import RPi.GPIO as GPIO
from onepi.utils.pid_controller import PIDController
from onepi.utils.control_utils import ControlUtils
from onepi.utils.simple_timer import SimpleTimer
from onepi.utils.robot_params import RobotParams
from onepi.one import BnrOneA


class DrivePID:
    """
    This class provides PID control for a differential drive robot.
    """
    _left_speed = 0
    _right_speed = 0
    _previous_left_speed = 0
    _previous_right_speed = 0
    _counter = 0

    KP = 0.02
    KI = 0.70
    KD = 0.03

    _one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

    _initialised = False

    def __init__(self, kp=KP, ki=KI, kd=KD,
                 params=RobotParams(),
                 update_period_ms=100):
        """
        initialises the class with kp, ki, kd,
        max speed (mm/s) and update period (ms)
        """
        self._initialised = False

        self._cut = ControlUtils(params._axis_length_mm,
                                 params.wheel_diameter_mm,
                                 params.ticks_per_rev)

        GPIO.setmode(GPIO.BCM)
        self._left_dir_pin = 22  # DirL
        self._right_dir_pin = 23  # DirR
        GPIO.setup(self._left_dir_pin, GPIO.IN)
        GPIO.setup(self._right_dir_pin, GPIO.IN)
        self._left_pid = PIDController(kp, ki, kd,
                                       -params.max_speed_mmps,
                                       params.max_speed_mmps)
        self._right_pid = PIDController(kp, ki, kd,
                                        -params.max_speed_mmps,
                                        params.max_speed_mmps)
        self._update_period_ms = update_period_ms
        self._pid_timer = SimpleTimer(
            increment=self._update_period_ms / 1000.0,
            function=self._update_speeds
        )

    def _initialise(self):
        """
        resets the system to be ready to start (again)
        """
        self._one.reset_left_encoder()
        self._one.reset_right_encoder()
        self._pid_timer.start()
        self._initialised = True

    def _compute_left_speed(self):
        """
        computes left speed
        """
        left_encoder = self._one.read_left_encoder()
        direction = (GPIO.input(self._left_dir_pin) * 2) - 1
        left_encoder = left_encoder * direction
        left_speed = self._left_pid.compute_output(left_encoder)
        return left_speed

    def _compute_right_speed(self):
        """
        computes right speed
        """
        right_encoder = self._one.read_right_encoder()
        direction = (GPIO.input(self._right_dir_pin) * 2) - 1
        right_encoder = right_encoder * direction
        right_speed = self._right_pid.compute_output(right_encoder)
        return right_speed

    def _update_speeds(self):
        """
        update wheel speeds by running the pid controller and sets the wheel
        speeds of the robot
        """
        left_speed = self._compute_left_speed()
        right_speed = self._compute_right_speed()
        self._one.move(left_speed, right_speed)

    def move(self, left_speed_mmps, right_speed_mmps):
        """
        Makes the robot move at the desired wheel speeds in mm/s
        """
        if not self._initialised:
            self._initialise()
        left_ticks = self._cut.compute_ticks_from_speed(
            left_speed_mmps, self._update_period_ms
        )
        right_ticks = self._cut.compute_ticks_from_speed(
            right_speed_mmps, self._update_period_ms
        )
        self._left_pid.change_set_point(left_ticks)
        self._right_pid.change_set_point(right_ticks)

    def stop(self):
        """
        Stops the robot and stops the corresponding timer
        used by the controller
        """
        self._pid_timer.stop()
        self._one.stop()
        self._initialised = False


def main():
    pass


if __name__ == "__main__":
    main()
