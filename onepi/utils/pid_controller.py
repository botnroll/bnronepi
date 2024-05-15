"""
PID controller
"""


def cap_to_limits(value, min_value, max_value):
    """
    cap value to given limits (min and max)
    """
    value = max(value, min_value)
    value = min(max_value, value)
    return value


def convert_range(x_value, x_min, x_max, y_min, y_max):
    """
    Converts a value x given in the range [x_min : x_max]
    to a new value in the range [y_min : y_max]
    """
    x_range = x_max - x_min
    y_range = y_max - y_min

    # Avoid division by zero
    if x_range == 0:
        return y_min + (y_range / 2)

    # Calculate the converted value
    y = (((x_value - x_min) / x_range) * y_range) + y_min
    return y


class PIDParams:
    """
    PID params, kp, ki and kd
    """

    _kp = 2.5
    _ki = 3.5
    _kd = 0.5

    def __init__(self, kp, ki, kd):
        """
        constructor
        """
        self._kp = kp
        self._ki = ki
        self._kd = kd

    def set_params(self, kp, ki, kd):
        """
        sets pid params
        """
        self._kp = kp
        self._ki = ki
        self._kd = kd

    def kp(self):
        """
        returns kp value
        """
        return self._kp

    def ki(self):
        """
        returns ki value
        """
        return self._ki

    def kd(self):
        """
        returns kd value
        """
        return self._kd


class PIDController():
    """
    Construct a new PID controller object
    kp proportional gain
    ki integral gain
    kd derivative gain
    """
    _min_value = -100
    _max_value = 100
    _pid = PIDParams(0, 0, 0)
    _setpoint = 0
    _change_sign = False
    _last_error = 0
    _output = 0
    _integral = 0

    def __init__(self, kp, ki, kd, min_value=-100, max_value=100):
        """
        construtor
        """
        self._pid.set_params(kp, ki, kd)
        self._setpoint = 0
        self._output = 0
        self._integral = 0
        self._min_value = min_value
        self._max_value = max_value

    def change_set_point(self, setpoint):
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
        proportional = self._pid.kp() * error
        #proportional = cap_to_limits(proportional, self._min_value, self._max_value)

        # Integral term
        self._integral += self._pid.ki() * error
        self._integral = cap_to_limits(self._integral, self._min_value, self._max_value)

        # Derivative term
        derivative = self._pid.kd() * (error - self._last_error)

        # Compute output
        #if abs(self._setpoint) >= 1:
        self._output = proportional + self._integral + derivative
        #else:
        #    self._output = (proportional * 0.1) + (self._integral * 0.1)
        self._output = cap_to_limits(self._output, self._min_value, self._max_value)
        # Map the output to control the motor
        mapped_output = convert_range(self._output, self._min_value, self._max_value, -100, 100)
        self._last_error = error
        return mapped_output

    def reset_controller(self):
        """
        resets the gains
        """
        self._setpoint = 0
        self._change_sign = False
        self._last_error = 0
        self._output = 0
        self._integral = 0
