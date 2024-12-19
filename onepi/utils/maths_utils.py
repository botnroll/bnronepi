"""
Collection of methods for useful maths calculations
"""

class MathsUtils:

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