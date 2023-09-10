
# bnronepi
*Python library to interface with Bot'n Roll One A.*

# 1. Installation:

# 2. Usage:

Simple example:
Displays a message "Hello Pi!" on the robot lcd.

```python
from one import BnrOneA

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A
one.stop()  # stop motors
one.lcd1(" Hello Pi! ")  # print data on LCD line 1
```

# 3. Examples

You can find lots of examples in the examples folder.
It contains several complete programs to allow you to take the most out of Bot'n Roll One A robot.

All the examples are documented and easy to follow.
You can use them as a starting point for your applications.

## 3.1 basic

## 3.2 advanced

## 3.3 extra

## 3.4 line_sensor

## 3.5 obstacles_sensor

## 3.6 fun_challenge



# 4. Tests

## 4.1 test_onepi

## 4.2 test_line_detector

## 4.3 test_config

# 5. Calibration

## 5.1 calibrate motors
## 5.2 calibrate line sensor

# 6. Extras

# 7. Utils

# 8. Diagnostics

## 8.1 plot_line_sensor

## 8.2 simulate_gaussian
