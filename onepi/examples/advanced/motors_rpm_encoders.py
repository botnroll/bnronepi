#!/usr/bin/env python3
"""
This code example is in the public domain.
http://www.botnroll.com

Description:
The robot moves by taking in speed values in rpm (rotations per minute)
and receives back the encoder values.
"""

import time
from onepi.one import BnrOneAPlus


def test_move_rpm_request_encoders(one, increment):
    """
    Test function that moves the robot and reads encoder values

    :param one: BnrOneAPlus object
    :param increment: Speed increment value
    """
    # Move motors and get encoder values
    left_encoder, right_encoder = one.move_rpm_get_encoders(
        200 + increment, 200 + increment
    )

    # Display values on LCD
    one.lcd1("Left: ", left_encoder)
    one.lcd2("Right: ", right_encoder)

    # Print values to console
    print(f"Left: {left_encoder} Right: {right_encoder}")


def main():
    # Create instance of BnrOneAPlus
    # Using default SPI bus=0, device=0
    one = BnrOneAPlus()

    # Stop motors initially
    one.stop()

    # Run test sequence
    try:
        for i in range(50):
            test_move_rpm_request_encoders(one, i)
            time.sleep(0.1)  # 100ms delay
    finally:
        # Make sure motors stop even if there's an error
        one.stop()


if __name__ == "__main__":
    main()
