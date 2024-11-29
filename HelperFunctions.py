import math
import pygame

# no worry
CYAN = (0, 255, 255)
# safe distance
GREEN = (0, 255, 0)
# caution
YELLOW = (255, 230, 0)
# threat
RED = (255, 0, 0)

# Initialize offsets for scene movement
offset_x = 0
offset_y = 0


def draw_circle(
    num,
    initial_radius,
    circle_spacing,
    screen,
    triangle_middle,
    circle_color,
    SCREEN_WIDTH,
):
    # draw concentric circles around the triangle
    for i in range(num):  # Adjust the range for more or fewer circles
        radius = initial_radius + i * circle_spacing
        pygame.draw.circle(
            screen,
            circle_color,
            (
                SCREEN_WIDTH // 2,
                triangle_middle,
            ),  # circle center at triangle's middle
            radius,
            width=1,  # outline thickness; use 0 for filled circles
        )


def update_scene_position(heading, speed, lat, lon):
    global offset_x, offset_y

    # Calculate movement based on speed and heading
    if speed > 0:
        speed_km_per_frame = speed / 3600 / 60
        heading_radians = math.radians(heading)

        delta_lat = speed_km_per_frame / 111 * math.cos(heading_radians)
        delta_lon = (
            speed_km_per_frame
            / (111 * math.cos(math.radians(lat)))
            * math.sin(heading_radians)
        )

        # Update coordinates with bounds checking
        new_lat = lat + delta_lat
        new_lon = lon + delta_lon

        if -90 <= new_lat <= 90:
            lat = new_lat
        else:
            print(f"Latitude out of bounds: {new_lat}")

        if -180 <= new_lon <= 180:
            lon = new_lon
        else:
            print(f"Longitude out of bounds: {new_lon}")

        # Update offsets based on movement
        offset_x += delta_lon
        offset_y += delta_lat

    return lat, lon


def altitude_assignment(altitude_other, altitude_self):
    difference = abs(altitude_other - altitude_self)
    if difference < 50:
        return RED
    elif difference < 1000:
        return YELLOW
    elif difference >= 1000 and difference < 5000:
        return GREEN
    else:
        return CYAN


def rotate_point(center, point, angle):
    """
    Rotates a point around a given center by an angle (in radians).
    :param center: Tuple (cx, cy) for the rotation center.
    :param point: Tuple (px, py) for the point to rotate.
    :param angle: Angle in radians.
    :return: Rotated point (new_x, new_y).
    """
    cx, cy = center
    px, py = point
    s, c = math.sin(angle), math.cos(angle)
    # Translate point to origin
    px -= cx
    py -= cy
    # Rotate point
    x_new = px * c - py * s
    y_new = px * s + py * c
    # Translate point back
    x_new += cx
    y_new += cy
    return (int(x_new), int(y_new))
