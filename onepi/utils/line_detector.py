"""
Line detector class
"""

from utils.config import Config


class LineDetector:
    """
    Converts line sensor readings into a relative line position on the sensor.
    It assumes that the array of sensors of a sensor peripheral are arranged in a straight line and equally spaced.
    It provides methods to compute the location of the line relative to the device.
    It outputs values in a range [-100, 100] where 0 (zero) corresponds to the centre of the sensor peripheral.
    """

    _ref_max = 1000
    _cfg_loaded = (
        False  # flag to signal whether or not the config values have been read already
    )
    _scaling_factor = [
        0
    ] * 8  # array of 8 elements with correction factor for each line sensor
    _previous_line_value = 0
    _config = Config()

    def _normalise(self, reading, minimum, scale):
        """
        normalise a reading taking the minimum value of the range and a scale factor
        """
        return int((reading - minimum) * scale)

    def _normalise_readings(self, sensor_reading):
        """
        Normalize values for each sensor reading
        """
        # creating 'aliases' for config values to make code more readable
        sensor_min = self._config.sensor_min
        scaling_factor = (
            self._scaling_factor
        )  # this is a true alias as the object is mutable
        size = len(sensor_reading)
        sensor_normalised = [0] * size
        for i in range(size):
            sensor_normalised[i] = self._normalise(
                sensor_reading[i], sensor_min[i], scaling_factor[i]
            )
        return sensor_normalised

    def _calculate_factors(self, ref, min, max):
        """
        Calculates the scaling factor given a reference value\
        and a range defined by min and max values
        This scaling factor is useful in normalising values
        """
        factors = [ref] * len(min)
        divisor = [x - y for x, y in zip(max, min)]
        factors = [x / y for x, y in zip(factors, divisor)]
        return factors

    def _load_if_necessary(self):
        """
        Loads values from config if they weren't loaded before
        """
        if not self._cfg_loaded:
            self._config.load()
            self._scaling_factor = self._calculate_factors(
                self._ref_max, self._config.sensor_min, self._config.sensor_max
            )

    def _compute_line_value(self, readings):
        """
        Computes a line value in the range [0, ref_max]
        """
        line_value = -1
        max_reading = max(readings)
        if max_reading > self._config.threshold:
            line_value = self._compute_mean_gaussian(readings)
        return line_value

    def _cap_value(self, value, lower_limit, upper_limit):
        """
        Caps the value to lower and upper limits
        """
        if value < lower_limit:
            return lower_limit
        elif value > upper_limit:
            return upper_limit
        else:
            return value

    def _convert_range(self, x_value, x_min, x_max, y_min, y_max):
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

    def _normalise_line_value(self, line_value, size):
        """
        Converts a line value in the range of [0, 8000] to a new range e.g. [-106, 106]
        This method involves two steps:
        1)  Converting the value in the range of [0, 8000] to a new range using a correction factor
            e.g. for a correction factor of 6% the new range is [-106, 106]
            The new range extends beyond 100 by a little margin specified by the correction factor in the config.
            The purpose of this is to enable adjusting the sensitivity of the readings near the extremities.
            For a sensor that is typically higher (away from the floor) this correction factor should be higher
            to prevent large jumps in the readings close to the extremities.
            By increasing the correction factor we are narrowing the sensitivity of the sensors and by reducing it
            we are extending the sensitivity out.
            There is a balance to achieve by tuning this value correctly in order to get the best of both worlds:
            - Smooth transitions in sensor value near the extremeties
            - Maximum sensitivity region of the sensor
        2) Capping the values to the desired range [-100, 100]
        """

        x_min = 0
        x_max = size * self._ref_max  # should be 8000
        y_min = -100 - self._config.correction_factor
        y_max = 100 + self._config.correction_factor
        line_value = self._convert_range(line_value, x_min, x_max, y_min, y_max)
        line_value = self._cap_value(line_value, -100, 100)
        return line_value

    def _filter_line_value(self, line_value, ref_value, max_value):
        """
        Filters the line value to handle edge cases
        such as no line detected or reading errors

        :param line_value: the computed line value
        :param ref_value: the reference value to help determining which side
        is the line in case it's no longer detected (e.g. middle of the range)
        :param max_value: the maximum value of the range
        """
        # out of the line -> all white
        if line_value == -1:
            if self._previous_line_value > ref_value:
                line_value = max_value
            else:
                line_value = 0
        # possible reading errors
        elif line_value < -1 or line_value > max_value:
            line_value = self._previous_line_value
        # if normal values
        else:
            self._previous_line_value = line_value
        return line_value

    def _compute_mean_gaussian(self, reading):
        """
        Lets assume the line detected gives us a discrete gaussian
        where the probabilities are given by each sensor reading and
        the values are pre-determined based on each sensor location:
         |sensor id | value  | probability |
         |----------|--------|-------------|
         |    0     |   1    |  reading[0] |
         |    1     |   2    |  reading[1] |
         |  (...)   | (...)  |    (...)    |
         |    7     |   8    |  reading[7] |

        We can compute the mean of the gaussian (location of line) by:
         1) computing the product for each sensor: product = value * probability
         2) computing sum_products = product[0] + product[1] + ... + product[7]
         3) computing sum_probabilities = reading[0] + reading[1] + ... + reading[7]
         4) computing mean = sum_products / sum_probabilities
        """
        size = len(reading)
        value = list(range(500, (size + 1) * 1000, 1000))
        product = [x * y for x, y in zip(value, reading)]
        sum_product = sum(product)
        sum_probability = sum(reading)
        if sum_probability == 0:
            mean = 0
        else:
            mean = sum_product / sum_probability
        return mean

    def _get_max_value_and_index(self, lst):
        """
        Returns the max value and its corresponding index from a list
        """
        max_value = max(lst)
        max_index = lst.index(max_value)
        return max_value, max_index

    def _prune(self, readings):
        """
        Deals with edge cases such when the max readings is on one of the sensors at the extremety
        In such cases it bumps up the value of the sensor to be at the threshold level
        """
        max_value, max_index = self._get_max_value_and_index(readings)
        if max_value < self._config.threshold:
            if max_index == 0 or max_index == (len(readings) - 1):
                readings[max_index] = self._config.threshold
        return readings

    def compute_line(self, readings):
        """
        Given an input as a set of sensors readings it computes a relative location of a line
        along the length of the sensor and expresses the output in a range [-100, 100]
        where 0 (zero) corresponds to the line being at the centre of the sensor.
        """
        max_range = len(readings) * 1000
        mid_range = max_range / 2
        self._load_if_necessary()
        normalised = self._normalise_readings(readings)
        pruned = self._prune(normalised)
        line_value = self._compute_line_value(pruned)
        line_value = self._filter_line_value(line_value, mid_range, max_range)
        line_value = self._normalise_line_value(line_value, len(pruned))
        line_value = self._cap_value(line_value, -100, 100)
        return line_value
