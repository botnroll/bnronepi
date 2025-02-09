class PidParams:
    """
    Set of PID parameters
    """
    def __init__(self, kp_in=0.070, ki_in=0.015, kd_in=0.000):
        """
        Defines the pid parameters
        """
        self.kp = kp_in
        self.ki = ki_in
        self.kd = kd_in
