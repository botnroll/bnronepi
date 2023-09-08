"""
 Latest update: 08-09-2023

 This code example is in the public domain.
 http://www.botnroll.com

This example works better by using a software pwm instead of using 
the hardware pwm pins on the Raspberry Pi.
Note that the connection to the Bot'n Roll should be on pin 9 (where the buzzer is attached to).
"""

import time
import RPi.GPIO as GPIO
from pitches import *

# notes in the melody:
melody = [note_C4, note_G3, note_G3, note_A3, note_G3, 0, note_B3, note_C4]
# note durations: 4 = quarter note, 8 = eighth note, etc.:
note_durations = [4, 8, 8, 4, 4, 4, 4, 4]

# Set up GPIO
BUZZER_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


def tone(pin, frequency, duration):
    if frequency <= 0:
        frequency = 1  # inaudible

    p = GPIO.PWM(BUZZER_PIN, frequency)  # Create a PWM object
    p.start(99)  # 99% duty cycle
    time.sleep(duration / 1000)
    p.stop()  # Stop the PWM


def setup():
    # iterate over the notes of the melody:
    for this_note in range(8):
        # to calculate the note duration, take one second
        # divided by the note type.
        # e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
        note_duration = 1000 / note_durations[this_note]
        tone(9, melody[this_note], note_duration)

        # to distinguish the notes, set a minimum time between them.
        # the note's duration + 30% seems to work well:
        pause_between_notes = note_duration * 1.30 / 1000
        time.sleep(pause_between_notes)


def loop():
    pass  # no need to repeat the melody.


def main():
    setup()
    while True:
        loop()
    # Clean up GPIO
    GPIO.cleanup()


if __name__ == "__main__":
    main()
