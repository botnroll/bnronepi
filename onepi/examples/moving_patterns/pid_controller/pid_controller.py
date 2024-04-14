"""
PID controller
"""

def cap_to_limits(input, min, max):
  input = max(input, min)
  input = min(max, input)
  return input

class pid_controller:
  """
  Construct a new PID controller object
  kp proportional gain
  ki integral gain
  kd derivative gain
  """
  _kp = 2.5
  _ki = 3.5
  _kd = 0.5
  _setpoint = 0
  _changeSign = False
  _lastInput = 0
  _output = 0
  _integral = 0

  def __init__(self, kp, ki, kd):
    """
    construtor
    """
    self._kp = (kp / 1000.0)
    self._ki = ki
    self._kd = kd
    self._setpoint = 0
    self._lastInput = 0
    self._output = 0
    self._integral = 0

  def change_set_point(self, setpoint):
    """
    Change the setpoint or reference value.
    This is the value the PID controller is trying to reach.
    setpoint: reference value
    """
    if ((self._setpoint * setpoint) < 0):
      self._changeSign = True
    self._setpoint = setpoint

  def compute_output(self, input):
    """
    Computes the output command by applying the PID control algorithm
    input: current input value
    return: float output command value
    """
    if (self._changeSign):
      input = 0
      self._changeSign = False
    # Calculate error
    error = self._setpoint - input

    # Proportional term
    proportional = self._kp * error * error * error
    proportional = cap_to_limits(proportional, -255, 255)
    # print_value("proportional: ", proportional)

    # Integral term
    self._integral += self._ki * error

    # print_value("self._integral: ", self._integral)
    self._integral = cap_to_limits(self._integral, -255, 255)

    # Derivative term
    derivative = self._kd * (input - self._lastInput)
    # print_value("derivative: ", derivative)

    # Compute output
    if (abs(self._setpoint) >= 1):
      self._output = proportional + self._integral + derivative
    else
      self._output = (proportional * 0.1) + (self._integral * 0.1)
    self._output = cap_to_limits(self._output, -255, 255)

    # Map the output to control the motor
    mappedOutput = map(self._output, -255.0, 255.0, -100.0, 100.0)
    self._lastInput = input
    return mappedOutput

  def reset_controller(self):
    """
    resets the gains
    """
    self._setpoint = 0
    self._changeSign = False
    self._lastInput = 0
    self._output = 0
    self._integral = 0
