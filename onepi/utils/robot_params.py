class RobotParams:
    """
    Set of robot parameters
    """

    def __init__(
        self,
        max_speed_mmps_in=850,
        axis_length_mm_in=163.0,
        wheel_diameter_mm_in=65.0,
        pulses_per_rev_in=32767,
    ):
        """
        Defines the robot parameters
        """
        self.max_speed_mmps = max_speed_mmps_in
        self.axis_length_mm = axis_length_mm_in
        self.wheel_diameter_mm = wheel_diameter_mm_in
        self.pulses_per_rev = pulses_per_rev_in
