"""
 Latest update: 07-09-2023

 HC-SR04 Ping distance sensor:
 VCC to 5v
 GND to GND
 Echo to RaspberryPi GPIO5 (BotnRoll pin 6)
 Trig to RaspberryPi GPIO6 (BotnRoll pin 7)

 This code example is in the public domain.
 http://www.botnroll.com
"""

import time
from onepi.one import BnrOneAPlus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # Use GPIO numbering

one = BnrOneAPlus(0, 0)  # object variable to control the Bot'n Roll ONE A+

echo_pin = 5  # 6 on robot side - Echo Pin  (GPIO.BOARD = 29)
trigger_pin = 6  # 7 on robot side - Trigger Pin (GPIO.BOARD = 31)

GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trigger_pin, GPIO.OUT)


def read_sonar():
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150

    return round(distance_cm, 2)


def setup():
    one.stop()  # stop motors
    one.lcd1("www.botnroll.com")
    one.lcd2(" ")
    GPIO.output(trigger_pin, False)
    print("Waiting 2s for Sensor To Settle")
    time.sleep(2)
    print("Reading...")


def loop():
    distance_cm = read_sonar()
    one.lcd2("distance: ", int(distance_cm))
    print("Distance:", distance_cm, "cm", end="   \r")
    time.sleep(0.050)


def main():
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
