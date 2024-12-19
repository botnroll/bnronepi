"""
This class implements a PDFB Controller
(Proportional Derivative Feedback Controller)
This type of control prevents overshoots as the
transfer function has no zeros
"""

from onepi.utils.maths_utils import MathsUtils


class PDController:

    _min_value = -100
    _max_value = 100
    _setpoint = 0
    _change_sign = False

    def __init__(self, kp, kd):
        """
        Initialize the PDController with proportional (kp)
        and derivative (kd) gains.
        """
        self.kp = kp
        self.kd = kd

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
        Computes the output command by applying the PDFB control algorithm
        input_value: current input value
        return: float output command value
        """
        if self._change_sign:
            input_value = 0
            self._change_sign = False

        # Modify the measurement with kd * input_value
        modified_measurement = input_value + self.kd * input_value
        error = self._setpoint - modified_measurement

        control_output = self.kp * error

        control_output = MathsUtils.cap_to_limits(control_output,
                                                  self._min_value,
                                                  self._max_value)
        # Map the output to control the motor
        mapped_output = MathsUtils.convert_range(
            control_output, self._min_value, self._max_value, -100, 100
        )

        return mapped_output

    def reset_controller(self):
        """
        resets the gains
        """
        self._setpoint = 0
        self._change_sign = False
