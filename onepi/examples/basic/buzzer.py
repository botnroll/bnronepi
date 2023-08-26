"""
This example code is in the public domain.
 http://arduino.cc/en/Tutorial/Tone
"""

import time
from pitches import *

# notes in the melody:
melody = [note_C4, note_G3, note_G3, note_A3, note_G3, 0, note_B3, note_C4]

# note durations: 4 = quarter note, 8 = eighth note, etc.:
note_durations = [4, 8, 8, 4, 4, 4, 4, 4]


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
        pause_between_notes = note_duration * 1.30
        time.sleep(pause_between_notes)
        # stop the tone playing:
        no_tone(9)


def loop():
    pass  # no need to repeat the melody.


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
