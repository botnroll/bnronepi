"""
 HC-SR04 Ping distance sensor:
 VCC to arduino 5v
 GND to arduino GND
 Echo to Arduino pin 6
 Trig to Arduino pin 7

 This sketch originates from Virtualmix: http://goo.gl/kJ8Gl

 This code example is in the public domain.
 http://www.botnroll.com
"""

import time
from one import BnrOneA
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

echoPin = 6    # Echo Pin
trigPin = 7    # Trigger Pin

GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(trigPin, GPIO.OUT)

maximumRange = 200      # Maximum range (200cm)
minimumRange = 0        # Minimum range


def pulseIn(pin, state, timeout_us=1000000):
    """
    In this script, the pulseIn function waits for a pulse with a
    specified state (HIGH or LOW) on the given pin.
    It returns the duration of the pulse in microseconds.
    The timeout_us parameter specifies the maximum time to wait for
    a pulse before giving up.
    If the timeout is reached, the function returns 0.
    """
    start_time = time.time()
    while GPIO.input(pin) != state:
        if (time.time() - start_time) * 1e6 > timeout_us:
            return 0

    pulse_start = time.time()
    while GPIO.input(pin) == state:
        if (time.time() - start_time) * 1e6 > timeout_us:
            return 0

    pulse_end = time.time()
    return int((pulse_end - pulse_start) * 1e6)


def Sonar():
    tempo = time.time()

    GPIO.output(trigPin, GPIO.LOW)
    time.sleep(0.002)

    GPIO.output(trigPin, GPIO.HIGH)
    time.sleep(0.010)

    GPIO.output(trigPin, GPIO.LOW)

    pin_state = GPIO.input(echoPin)
    duration = pulseIn(echoPin, GPIO.HIGH, 11640)
    print(f"Pulse duration: {duration} microseconds")

    time.sleep(0.016 - (time.time() - tempo))  # this routine has fixed time (16 milliseconds)

    # Calculate the distance (in cm) based on the speed of sound
    distance_cm = int(duration / 58.2)
    if (distance_cm >= maximumRange or distance_cm <= minimumRange)
        distance_cm = -1
    return distance_cm


def setup():
    one.stop()             # stop motors
    one.lcd1("www.botnroll.com")
    one.lcd2(" ")


def loop():
    distance_cm = Sonar()
    one.lcd2("distance_cm: ", distance_cm)
    print(distance_cm)
    time.sleep(0.050)


def main():
    setup()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        # Clean up the GPIO configuration
        GPIO.cleanup()


if __name__ == "__main__":
    main()
