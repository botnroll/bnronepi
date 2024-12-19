class PidParams:
    """
    Set of PID parameters
    """

    def __init__(self, kp_in=0.02, ki_in=0.7, kd_in=0.03):
        """
        Defines the pid parameters
        """
        self.kp = kp_in
        self.ki = ki_in
        self.kd = kd_in
