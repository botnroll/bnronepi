"""
Line detector class
"""

from config import Config


class LineDetector:
    """
    Facilitates converting line sensor readings into a relative line position on the sensor.
    It assumes that the array of sensors of a sensor peripheral are arranged in a straight line and equally spaced.
    It provides methods to compute the location of the line relative to the device.
    It outputs values in a range [-100, 100] where 0 (zero) corresponds to the centre of the sensor peripheral.
    """

    _ref_max = 1000
    _load_flag = False  # flag to signal whether or not the config values have been read already
    _scaling_factor = [0] * 8  # array of 8 elements with correction factor for each line sensor
    _previous_line_value = 0
    _config = Config()
    _vrt1 = 0  # virtual sensor on the far left
    _vrt2 = 0  # virtual sensor on the far right

    def __normalise(self, reading, minimum, scale):
        """
        normalise a reading taking the minimum value of the range and a scale factor
        """
        return int((reading - minimum) * scale)

    def normalise_readings(self, sensor_reading):
        """
        Normalize values for each sensor reading
        """
        # creating 'aliases' for config values to make code more readable
        sensor_min = self._config.sensor_min
        scaling_factor = self._scaling_factor  # this is a true alias as the object is mutable
        size = len(sensor_reading)
        sensor_normalised = [0] * size
        for i in range(size):
            sensor_normalised[i] = self.__normalise(sensor_reading[i], sensor_min[i], scaling_factor[i])
        return sensor_normalised

    def __get_maximum(self, input):
        """
        Determines the maximum value and corresponding index of the list
        """
        index = -1
        value = -1

        for i in range(len(input)):
            if input[i] > value:
                value = input[i]  # Save the max value
                index = i  # Save the sensor index
        return index, value

    def __calculate_factors(self, ref, min, max):
        """
        Calculates the scaling factor given a reference value\
        and a range defined by min and max values
        This scaling factor is useful in normalising values
        """
        factors = [ref] * len(min)
        divisor = [x - y for x, y in zip(max, min)]
        factors = [x / y for x, y in zip(factors, divisor)]
        return factors

    def load_if_necessary(self):
        """
        Loads values from config if they weren't loaded before
        """
        if not self._load_flag:
            self._config.load()
            self._vrt1 = self._config.sensor_min[1] * 2  # update virtual sensor on the left
            self._vrt2 = self._config.sensor_min[6] * 2  # update virtual sensor on the right
            self._scaling_factor = self.__calculate_factors(
                self._ref_max, self._config.sensor_min, self._config.sensor_max
            )

    def __extend_sensor(self, sensor):
        """
        Returns an extended sensor containing one extra virtual sensor on each side of the input sensor array
        """
        return [0] + sensor + [0]

    def compute_line_value(self, max_reading, max_index, sensor_extended):
        """
        Computes a line value in the range [0, ref_max]
        """
        ref_max = self._ref_max  # not an alias! (changing ref_max does not change self.ref_max)
        line_value = -1
        if max_reading > self._config.threshold:
            # is_previous_greater_than_following = sensor_extended[max_index - 1] >= sensor_extended[max_index + 1]

            # if is_previous_greater_than_following:
            #     line_value = (ref_max * (max_index - 1)) + sensor_extended[max_index]
            # else:
            #     # if not the last sensor
            #     if max_index != 8:
            #         line_value = (ref_max * max_index) + sensor_extended[max_index + 1]
            #     # if it's the last sensor
            #     else:
            #         line_value = (ref_max * max_index) + ref_max - sensor_extended[max_index]
            if max_index == 1:  # max value in the first sensor
                sensor_extended[0] = sensor_extended[2]  # mirror 3rd sensor
                # print("max value in the FIRST sensor. extended = ", sensor_extended)
            if max_index == 2:  # max value in the second sensor
                sensor_extended[0] = int(sensor_extended[1] * 2 / 3)
                # print("max value in the SECOND sensor. extended = ", sensor_extended)
            if max_index == 7:  # max value in the 7th sensor
                sensor_extended[9] = int(sensor_extended[8] * 2 / 3)
                # print("max value in the 7TH sensor. extended = ", sensor_extended)
            if max_index == 8:  # max value in the last sensor
                sensor_extended[9] = sensor_extended[7]  # mirror 7th sensor
                # print("max value in the LAST sensor. extended = ", sensor_extended)
            line_value = self.compute_mean_gaussian(sensor_extended)
        return line_value

    def __normalise_line_value(self, line_value, size):
        """
        Converts a line value in the range [0, 8000] to be in the range [-100, 100]
        """
        if size != 0:
            line_value = ((line_value / size) * 0.2) - 100  # values ranging from -100 to 100
        return line_value

    def filter_line_value(self, line_value, min, max):
        """
        Filters the line value to handle edge cases
        such as no line detected or reading errors
        """
        # out of the line -> all white
        if line_value == -1:
            if self._previous_line_value > min:
                line_value = max
            else:
                line_value = 0
        # possible reading errors
        elif line_value < -1 or line_value > max:
            line_value = self._previous_line_value
        # if normal values
        else:
            self._previous_line_value = (
                line_value  # only updates previous line value if the current is detecting something
            )
        return line_value

    def compute_mean_gaussian(self, reading):
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
        value = list(range(500, (size + 1) * 1000, 1000))  # values = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
        # print("Gaussian value:", value)
        # print("Gaussian reading:", reading)
        product = [x * y for x, y in zip(value, reading)]
        sum_product = sum(product)
        sum_probability = sum(reading)
        if sum_probability == 0:
            mean = 0
        else:
            mean = sum_product / sum_probability
        return mean

    def compute_line(self, sensor_reading):
        """
        Given an input as a set of sensors readings it computes a relative location of a line
        along the length of the sensor and expresses the output in a range [-100, 100]
        where 0 (zero) corresponds to the line being at the centre of the sensor.
        """
        self.load_if_necessary()
        sensor_normalised = self.normalise_readings(sensor_reading)
        max_index, max_reading = self.__get_maximum(sensor_normalised)
        sensor_extended = self.__extend_sensor(sensor_normalised)
        max_index += 1  # increment by one as sensor_extended contains max value at max_index + 1
        line_value = self.compute_line_value(max_reading, max_index, sensor_extended)

        line_value = self.filter_line_value(line_value, 5000, 10000)
        line_value = self.__normalise_line_value(line_value, len(sensor_extended))
        return line_value
