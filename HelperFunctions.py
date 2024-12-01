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


def update_scene_position(heading, speed, lat, lon, dt=1 / 60):
    """
    Update the scene position and offsets based on heading, speed, and current position.

    :param heading: The heading in degrees (0 = north, 90 = east, etc.)
    :param speed: The speed in km/h
    :param lat: Current latitude in degrees
    :param lon: Current longitude in degrees
    :param offset_x: Current x offset in screen coordinates
    :param offset_y: Current y offset in screen coordinates
    :param dt: Time delta per frame in seconds (default assumes 60 FPS)
    :return: Updated latitude, longitude, offset_x, and offset_y
    """
    # calculate movement based on speed and heading
    if speed > 0:
        speed_km_per_second = speed / 3600  # convert speed to km/s
        distance = speed_km_per_second * dt  # distance traveled in this frame
        heading_radians = math.radians(heading)

        # calculate changes in latitude and longitude
        delta_lat = distance / 111 * math.cos(heading_radians)  # 1 degree lat = ~111 km
        delta_lon = (
            distance / (111 * math.cos(math.radians(lat))) * math.sin(heading_radians)
        )

        # update coordinates with bounds checking
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
    # translate point to origin
    px -= cx
    py -= cy
    # rotate point
    x_new = px * c - py * s
    y_new = px * s + py * c
    # translate point back
    x_new += cx
    y_new += cy
    return (int(x_new), int(y_new))
