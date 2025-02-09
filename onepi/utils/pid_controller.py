"""
PID controller
"""

from onepi.utils.pid_params import PidParams
from onepi.utils.maths_utils import MathsUtils


class PidController:
    """
    Construct a new PID controller object
    kp proportional gain
    ki integral gain
    kd derivative gain
    """

    _min_value = -100
    _max_value = 100
    _pid = PidParams()
    _setpoint = 0
    _change_sign = False
    _last_error = 0
    _output = 0
    _integral = 0

    def __init__(self, pid_params=PidParams(), min_value=-100, max_value=100):
        """
        construtor
        """
        self._pid = pid_params
        self._setpoint = 0
        self._output = 0
        self._integral = 0
        self._min_value = min_value
        self._max_value = max_value

    def set_pid_params(self, pid_params):
        """
        updates pid params
        """
        self._pid = pid_params

    def get_pid_params(self):
        """
        returns pid params
        """
        return self._pid

    def get_setpoint(self):
        """
        returns the setpoint
        """
        return self._setpoint

    def change_setpoint(self, setpoint):
        """
        Change the setpoint or reference value.
        This is the value the PID controller is trying to reach.
        setpoint: reference value
        """
        if (self._setpoint * setpoint) < 0:
            self._change_sign = True
        self._setpoint = setpoint

    def compute_output(self, input_value):
        """
        Computes the output command by applying the PID control algorithm
        input_value: current input value
        return: float output command value
        """
        if self._change_sign:
            input_value = 0
            self._change_sign = False
        # Calculate error
        error = self._setpoint - input_value

        # Proportional term
        proportional = self._pid.kp * error
        # proportional = cap_to_limits(proportional, self._min_value, self._max_value)

        # Integral term
        self._integral += self._pid.ki * error
        self._integral = MathsUtils.cap_to_limits(
            self._integral, self._min_value, self._max_value
        )

        # Derivative term
        derivative = self._pid.kd * (error - self._last_error)

        # Compute output
        # if abs(self._setpoint) >= 1:
        self._output = proportional + self._integral + derivative
        # else:
        #    self._output = (proportional * 0.1) + (self._integral * 0.1)
        self._output = MathsUtils.cap_to_limits(
            self._output, self._min_value, self._max_value
        )
        # Map the output to control the motor
        # mapped_output = MathsUtils.convert_range(
        #     self._output, self._min_value, self._max_value, -100, 100
        # )
        self._last_error = error
        
        return self._output
        #return mapped_output

    def reset_controller(self):
        """
        resets the gains
        """
        self._setpoint = 0
        self._change_sign = False
        self._last_error = 0
        self._output = 0
        self._integral = 0
