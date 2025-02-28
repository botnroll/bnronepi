class RobotParams:
    """
    Set of robot parameters
    """

    def __init__(
        self,
        max_speed_rpm_in=300,    #
        axis_length_mm_in=165,   # increase to move for longer
        wheel_diameter_mm_in=63, # decrease to move for longer
        pulses_per_rev_in=2251,  # increase to move for longer 2251 in theory, 2240 in practice
    ):
        """
        Defines the robot parameters
        """
        self.max_speed_rpm = max_speed_rpm_in
        self.axis_length_mm = axis_length_mm_in
        self.wheel_diameter_mm = wheel_diameter_mm_in
        self.pulses_per_rev = pulses_per_rev_in
