# @author botnroll.com

import math
import time
import signal
from onepi.utils.control_utils import ControlUtils
from onepi.utils.control_utils import PoseSpeeds
from onepi.utils.control_utils import Pose
from onepi.one import BnrOneAPlus

PI = 3.14159
AXIS_LENGTH_MM = 162
TICKS_PER_REV = 2240
WHEEL_DIAMETER = 63
WHEEL_RADIUS_MM = WHEEL_DIAMETER / 2.0
STRAIGHT_MOTION = 32767

cut = ControlUtils()
one = BnrOneAPlus()
one.reset_left_encoder()
one.reset_right_encoder()


def print_value(text, value):
    print(text, str(round(value)))


def compute_angular_speed(speed, radius_of_curvature_mm, direction=1):
    """
    calculates the angular speed given the linear speed, the radius of curvature and the direction
    """
    linear_speed = speed
    if radius_of_curvature_mm != 0:
        if radius_of_curvature_mm == STRAIGHT_MOTION:  # straight motion
            angular_speed_rad = 0
            linear_speed = speed
        else:
            angular_speed_rad = (direction) * ((speed) / (radius_of_curvature_mm))
    else:
        angular_speed_rad = (direction) * (speed / (AXIS_LENGTH_MM / 2))
        linear_speed = 0

    return linear_speed, angular_speed_rad


def move_and_slow_down(
    total_pulses,
    speed=50,
    direction=1,
    radius_of_curvature_mm=0,
    slow_down_thresh=TICKS_PER_REV,
):
    """
    @brief Moves and slows down when pulses remaining are less than slow_down_thresh
    If slow_down_thresh is set to zero (or negative number) it does not slow down.
    By default it starts slowing down when a full rotation (TICKS_PER_REV) remains.
    The slow down is a quadratic function of the form y = a * x^2

    @param total_pulses number of pulses necessary from the encoders (average) to complete the manoeuvre
    @param speed
    @param direction of curve in case of a curved motion
    @param radius_of_curvature_mm (positive for CW and negative values for CCW rotations)
    @param slow_down_thresh number of ticks to when the robot should start reducing speed
    @param straight boolean specifying if this is a straight line or not
    """

    coeff = 100.0 / TICKS_PER_REV
    linear_speed, angular_speed_rad = compute_angular_speed(
        speed, radius_of_curvature_mm, direction
    )

    pose_speeds = PoseSpeeds(linear_speed, angular_speed_rad)

    dt = 0.1
    encoder_count = 0
    print("encoder_count: ", encoder_count, " total: ", total_pulses)
    for i in range(30000):
        if encoder_count < total_pulses:
            left_encoder = abs(one.read_left_encoder())
            right_encoder = abs(one.read_right_encoder())
            encoder_count += (left_encoder + right_encoder) / 2.0
            pulses_remaining = total_pulses - encoder_count
            pose_speeds = maybe_slow_down(
                pose_speeds,
                linear_speed,
                pulses_remaining,
                slow_down_thresh,
                radius_of_curvature_mm,
                coeff,
                direction,
            )
            wheel_speeds_mmps = cut.compute_wheel_speeds(
                pose_speeds.linear_mmps, pose_speeds.angular_rad
            )
            wheel_speeds_rpm = cut.compute_speeds_rpm(wheel_speeds_mmps)
            print(wheel_speeds_rpm.left, wheel_speeds_rpm.right)
            one.move_rpm(wheel_speeds_rpm.left, wheel_speeds_rpm.right)
        else:
            one.brake(100, 100)
            break


def maybe_slow_down(
    pose_speeds,
    speed,
    pulses_remaining,
    slow_down_thresh,
    radius_of_curvature_mm,
    coeff,
    direction,
):
    if (pulses_remaining < TICKS_PER_REV) and (
        pulses_remaining < slow_down_thresh
    ):  # slowing down
        percentage = coeff * pulses_remaining * pulses_remaining
        slow_speed = (speed * percentage) / 100
        slow_speed = max(10, slow_speed)  # cap to min
        angular_speed_rad = 0
        linear_speed, angular_speed_rad = compute_angular_speed(
            slow_speed, radius_of_curvature_mm, direction
        )
        pose_speeds = PoseSpeeds(linear_speed, angular_speed_rad)
    return pose_speeds


def get_sign(value):
    if value >= 0:
        return 1
    return -1


def rotate_angle_deg_at_speed(
    angle_deg, speed=50, radius_of_curvature_mm=0, slow_down_thresh_deg=0
) -> PoseSpeeds:
    total_pulses = cut.compute_pulses_from_angle_and_curvature(
        math.radians(angle_deg), radius_of_curvature_mm
    )
    print_value("total_pulses: ", total_pulses)
    slow_down_pulses_thresh = cut.compute_pulses_from_angle_and_curvature(
        math.radians(slow_down_thresh_deg), radius_of_curvature_mm
    )
    print_value("slow_down_pulses_thresh: ", slow_down_pulses_thresh)
    move_and_slow_down(
        total_pulses,
        abs(speed),
        get_sign(angle_deg),
        abs(radius_of_curvature_mm),
        slow_down_pulses_thresh,
    )


def rotate_90_deg_ccw(speed, slow_down_thresh_deg=30) -> PoseSpeeds:
    return rotate_angle_deg_at_speed(90, speed, 0, slow_down_thresh_deg)


def check_wheel_speed_limit(speed):
    if speed > 100 or speed < -100:
        print_value("******** ERROR ******** speed out of limits: ", speed)


def check_speed_limits(pose_speeds: PoseSpeeds):
    wheel_speeds = cut.compute_wheel_speeds(
        pose_speeds.linear_mmps, pose_speeds.angular_rad
    )
    check_wheel_speed_limit(wheel_speeds.left)
    check_wheel_speed_limit(wheel_speeds.right)


def move_straight_at_speed(distance, speed=50, slow_down_distance=0):
    """
    moves the robot for the given distance at the given speed.
    If slow down distance is provided then it slows down once the remaining distance is
    less than the slow_down_distance
    """
    abs_distance = abs(distance)
    abs_slow_down_distance = abs(slow_down_distance)
    total_pulses = cut.compute_pulses_from_distance(abs_distance)
    slow_down_pulses = cut.compute_pulses_from_distance(abs_slow_down_distance)
    move_and_slow_down(total_pulses, speed, 1, STRAIGHT_MOTION, slow_down_pulses)


def first_figure():
    rotate_angle_deg_at_speed(180, 50, 100)  # angle_deg, speed, radius_of_curvature_mm
    rotate_angle_deg_at_speed(-180, 50, 60)
    rotate_angle_deg_at_speed(360, 70, 150)
    rotate_angle_deg_at_speed(-180, 50, 60)
    rotate_angle_deg_at_speed(180, 50, 100)


def draw_mickey_mouse():
    rotate_angle_deg_at_speed(140, 50, 150)  # angle_deg, speed, radius_of_curvature_mm
    rotate_angle_deg_at_speed(-155, 50, 0)
    rotate_angle_deg_at_speed(320, 50, 80)
    rotate_angle_deg_at_speed(-155, 50, 0)
    rotate_angle_deg_at_speed(60, 50, 150)
    rotate_angle_deg_at_speed(-155, 50, 0)
    rotate_angle_deg_at_speed(320, 50, 80)
    rotate_angle_deg_at_speed(-155, 50, 0)
    rotate_angle_deg_at_speed(140, 50, 150)


def draw_triangle(side_mm, speed=50):
    """
    moves by decribing a triangular motion with side given as the input parameter
    """
    draw_polygon(side_mm, 3, speed)


def draw_square(side_mm, speed=60):
    """
    describes a quared motion with side given as input parameter
    """
    draw_polygon(side_mm, 4, speed)


def draw_circle(radius_mm, speed=60):
    """
    describes a circular motion with radius given as input parameter
    """
    rotate_angle_deg_at_speed(360, speed, radius_mm)


def draw_semi_circle(radius_mm, speed=50):
    """
    describes a semi-circle motion with radius given as input parameter
    """
    rotate_angle_deg_at_speed(180, speed, radius_mm)


def draw_polygon(side_mm, num_sides, speed=55):
    """
    describes a polygon shaped motion given the side length and the number of sides
    """
    angle_deg = 180 - ((num_sides - 2) * 180.0) / num_sides
    for i in range(num_sides):
        move_straight_at_speed(side_mm, speed)
        rotate_angle_deg_at_speed(angle_deg, speed)


def compute_fibonacci_sequence(number_of_elements):
    """
    computes a fibonacci sequence with a predetermined number of elements
    Note: number_of_elements should be more than 1
    """
    fibonacci_sequence = [1, 1]
    if number_of_elements > 2:
        for i in range(number_of_elements - 2):
            fibonacci_sequence.append(fibonacci_sequence[i] + fibonacci_sequence[i + 1])
    return fibonacci_sequence


def draw_fibonacci_spiral(seed_radius, num_segments, speed=50):
    """
    The fibonacci spiral changes the radius of curvature every 90 degrees
    according to the fibonacci sequence:
    1, 1, 2, 3, 5, 8, 13, ...

    The seed_radius is the initial radius of the spiral.
    num_segments specifies the number of segments of 90 degrees of the spiral.
    """
    numbers = compute_fibonacci_sequence(num_segments)
    for i in range(abs(num_segments)):
        radius_of_curvature = numbers[i] * seed_radius
        rotate_angle_deg_at_speed(90, speed, radius_of_curvature)


def draw_archimedean_spiral(spiral_factor, total_angle_deg, speed=50):
    """
    The archimedean spiral has an increasing radius of curvature
    radius_of_curvature = a * theta, where a is a constant (spiral_factor)
    """
    angle_step = 5
    current_angle = 0
    for i in range(0, total_angle_deg, angle_step):
        radius_of_curvature_mm = spiral_factor * current_angle
        rotate_angle_deg_at_speed(angle_step, speed, radius_of_curvature_mm)
        current_angle += 5


def draw_snake(
    length_mm=700, num_elements=7, speed=50, snaking_angle_deg=60, turning_rate_deg=0
):
    """
    describes an ondulatory motion (like a snake)
    All arguments are optional.
    You can specify the length of the motion, the number of ondulatory elements and the speed.
    By adjusting the snaking angle you can tween the amplitude of the ondulatory motion.
    And by setting a turning rate you can also curve the ondulatory motion.
    By adjusting these last two parameters you can create interesting moving patterns.
    """
    secant_length = length_mm / num_elements
    theta_rad = deg_to_rad(snaking_angle_deg)
    radius_of_curvature_mm = secant_length / (2 * math.sin(theta_rad / 2))
    rotate_angle_deg_at_speed(-snaking_angle_deg / 2, speed)
    for i in range(num_elements):
        rotate_angle_deg_at_speed(
            snaking_angle_deg + turning_rate_deg, speed, radius_of_curvature_mm
        )
        snaking_angle_deg = (-1) * snaking_angle_deg


def draw_house():
    """
    example on how to set a motion with the shape of a house
    """
    speed = 50
    move_straight_at_speed(200, speed)
    rotate_angle_deg_at_speed(90, speed, 0)
    move_straight_at_speed(200, speed)
    rotate_angle_deg_at_speed(90, speed)
    move_straight_at_speed(200, speed)
    rotate_angle_deg_at_speed(-135, speed)
    move_straight_at_speed(144, speed)
    rotate_angle_deg_at_speed(-90, speed)
    move_straight_at_speed(144, speed)
    rotate_angle_deg_at_speed(-90, speed)
    move_straight_at_speed(282, speed)
    rotate_angle_deg_at_speed(-135, speed)
    move_straight_at_speed(200, speed)
    rotate_angle_deg_at_speed(-135, speed)
    move_straight_at_speed(282, speed)


def draw_heart():
    """
    example on how to set a motion with the shape of a heart
    """
    speed = 50
    rotate_angle_deg_at_speed(45, speed)
    move_straight_at_speed(200, speed)
    rotate_angle_deg_at_speed(230, speed, 100)
    rotate_angle_deg_at_speed(-180, speed)
    rotate_angle_deg_at_speed(230, speed, 100)
    move_straight_at_speed(230, speed)


def move_pattern():
    # move_straight_at_speed(800, 50, 300)

    # rotate_angle_deg_at_speed(360, 50, 100, 60)
    rotate_angle_deg_at_speed(90, 100, 0, 0)
    # draw_circle(150)
    # draw_mickey_mouse()
    # draw_house()
    # draw_heart()
    # draw_triangle(300)
    # draw_polygon(200, 4, 100)
    # draw_polygon(300, 5)
    # draw_polygon(300, 6)
    # draw_polygon(300, 7)
    # draw_polygon(220, 10)
    # draw_fibonacci_spiral(50, 7)
    # draw_archimedean_spiral(0.3, 360 * 3)
    # draw_snake(800, 5, 50, 90)
    # draw_snake(800, 12, 50, 30)
    # draw_snake(800, 2, 50, 45, 0)
    # draw_snake(800, 4, 50, 180, 0)
    # draw_snake(1000, 14, 50, 60, 30)
    # draw_snake(1200, 8, 50, 270, 45)
    # draw_snake(400, 4, 50, 300, 90)
    # draw_snake(400, 6, 50, 300, 120)
    # draw_snake(600, 16, 50, 320, 155)

    time.sleep(5)


def setup():
    move_pattern()


def loop():
    pass


def main():

    # function to stop the robot on exiting with CTRL+C
    def stop_and_exit(sig, frame):
        one.stop()
        time.sleep(0.1)
        exit(0)

    signal.signal(signal.SIGINT, stop_and_exit)

    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
