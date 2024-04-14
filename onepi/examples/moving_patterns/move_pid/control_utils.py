def cap_to_limits(value, min_value, max_value):
    """
    Cap input value within the given min and max limits
    """
    value = max(value, min_value)
    value = min(max_value, value)
    return value


class ControlUtils:
    """
    collection of methods to compute speeds, distance, ticks
    """

    _axis_length_mm = 163.0
    _wheel_diameter_mm = 65.0
    _ticks_per_rev = 80
    _spot_rotation_delta = -14.5  # For spot rotations only
    _pi = 3.14159265

    def __init__(self, axis_length_mm, wheel_diameter_mm, ticks_per_rev):
        """
        constructor
        """
        self._axis_length_mm = axis_length_mm
        self._wheel_diameter_mm = wheel_diameter_mm
        self._ticks_per_rev = ticks_per_rev

    def convert_range(self, x_value, x_min, x_max, y_min, y_max):
        """
        Converts a value x given in the range [x_min : x_max]
        to a new value in the range [y_min : y_max]
        """
        x_range = x_max - x_min
        y_range = y_max - y_min

        # Avoid division by zero
        if x_range == 0:
            return y_min + y_range / 2

        # Calculate the converted value
        y = ((x_value - x_min) / x_range) * y_range + y_min
        return y

    def compute_rev_from_ticks(self, pulses):
        """
           computes the expected number of pulses given the number of revolutions of the wheel
        */
        """
        global TICKS_PER_REV
        return float(pulses) / TICKS_PER_REV

    def compute_distance_from_rev(self, revolutions):
        """
        computes distance given the number of revolutions
        """
        global WHEEL_DIAMETER_MM, PI
        distance_mm = PI * float(WHEEL_DIAMETER_MM) * revolutions
        return distance_mm

    def compute_speed_from_distance(self, distance_mm, time_ms):
        """
        computes speed given the distance and time
        """
        return (distance_mm * 1000) / time_ms

    def compute_speed_from_ticks(self, num_ticks, time_ms):
        """
        computes speed given the number of ticks and time
        """
        revolutions = self.compute_rev_from_ticks(num_ticks)
        distance_mm = self.compute_distance_from_rev(revolutions)
        speed_mmps = self.compute_speed_from_distance(distance_mm, time_ms)
        return speed_mmps

    def compute_distance_from_speed(self, speed_mmps, time_ms):
        """
        computes the distance given the speed and time
        """
        distance_mm = (float(speed_mmps) * time_ms) / 1000.0
        return distance_mm

    def compute_revolutions_from_distance(self, distance_mm):
        """
        computes the number of revolutions expected for the wheel for a given distance
        """
        global PI, WHEEL_DIAMETER_MM
        perimeter_of_circle = PI * float(WHEEL_DIAMETER_MM)
        revolutions = distance_mm / perimeter_of_circle
        return revolutions

    def compute_arc_length(self, angle_rad, radius_of_curvature_mm):
        """
        Computes the arc length given the angle and radius of curvature
        """
        global AXIS_LENGTH_MM, SPOT_ROTATION_DELTA
        arc_length_mm = 0.0
        if radius_of_curvature_mm != 0.0:
            arc_length_mm = angle_rad * radius_of_curvature_mm
        else:
            arc_length_mm = (
                angle_rad * float(AXIS_LENGTH_MM + SPOT_ROTATION_DELTA)
            ) / 2.0
        return arc_length_mm

    def compute_ticks_from_rev(self, revolutions):
        """
        computes number of ticks from number of revolutions
        """
        global TICKS_PER_REV
        return revolutions * TICKS_PER_REV

    def compute_pulses_from_rev(self, revolutions):
        """
        computes the expected number of ticks given the number of revolutions of the wheel
        """
        global TICKS_PER_REV
        return round(TICKS_PER_REV * revolutions)

    def compute_ticks_from_speed(self, speed_mmps, time_ms):
        """
        computes number of ticks given speed and time
        """
        distance_mm = self.compute_distance_from_speed(speed_mmps, time_ms)
        revolutions = self.compute_revolutions_from_distance(distance_mm)
        num_ticks = self.compute_ticks_from_rev(revolutions)
        return num_ticks

    def maybe_change_sign(self, abs_value, ref_value, previous_ref_value):
        """
        sets the sign of the output value to match the sign of refValue
        """
        if (ref_value * previous_ref_value) < 0:
            return 0  # return 0 as there was a change of sign
        if ref_value < 0:
            return -abs_value
        return abs_value

    def convert_to_mmps(self, desired_speed_percentage):
        """
        convert speed percentage to real speed in mmps
        """
        global MAX_SPEED, MIN_SPEED
        capped_speed = cap_to_limits(desired_speed_percentage, -100, 100)
        if capped_speed < 0:
            return convert_range(capped_speed, -100, 0, -MAX_SPEED, -MIN_SPEED)
        if capped_speed > 0:
            return convert_range(capped_speed, 0, 100, MIN_SPEED, MAX_SPEED)
        return 0

    def convert_to_percentage(self, desired_speed_mmps):
        """
        convert real speed to speed percentage
        """
        global MAX_SPEED, MIN_SPEED
        cappedSpeed = cap_to_limits(desired_speed_mmps, -MAX_SPEED, MAX_SPEED)
        if cappedSpeed <= -MIN_SPEED:
            return map(cappedSpeed, -MAX_SPEED, -MIN_SPEED, -100, 0)
        if cappedSpeed >= MIN_SPEED:
            return map(cappedSpeed, MIN_SPEED, MAX_SPEED, 0, 100)
        return 0
