import pygame
import sys
import json
import math
from OpenSkyHandler import get_aircraft_data
from HeadingIndicator import draw_heading_arc
from DisplaySpeed import display_speed


# using KDFW (Dallas/Fort Worth International Airport) as the center for testing purposes
RADIUS_KM = 50  # set radius to 50 kilometers

current_altitude = 0

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


def main():
    lat = 32.8968
    lon = -97.0377

    # initialize Pygame
    pygame.init()

    # font
    font = pygame.font.SysFont("Consolas", 20)

    # screen dimensions
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    clock = pygame.time.Clock()
    heading = 0  # Initial heading
    speed = 0  # Current speed in km/h
    acceleration = 0.5  # Acceleration per frame
    max_speed = 900  # Max speed in km/h
    deceleration = 0.2  # Deceleration per frame

    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Navigation Display")

    top = 100
    bottom = 130
    width = 10

    # triangle properties
    triangle_color = WHITE
    triangle_vertices = [
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + top),  # Top vertex
        (SCREEN_WIDTH // 2 - width, SCREEN_HEIGHT // 2 + bottom),  # Bottom left vertex
        (SCREEN_WIDTH // 2 + width, SCREEN_HEIGHT // 2 + bottom),  # Bottom right vertex
    ]

    middle = (top + bottom) / 2
    triangle_middle = SCREEN_HEIGHT // 2 + middle

    # circle properties
    circle_color = WHITE
    initial_radius = 100  # Radius of the smallest circle
    circle_spacing = 150  # Spacing between circles

    # running flag
    running = True
    LAT_SPAN = (
        RADIUS_KM / 111
    )  # approx. degrees latitude for given radius and location above equator

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            heading = (heading + 5) % 360
        elif keys[pygame.K_a]:
            heading = (heading - 5) % 360

        if keys[pygame.K_w]:
            speed = min(speed + acceleration, max_speed)  # Increase speed up to max
        elif keys[pygame.K_s]:
            speed = max(speed - deceleration, 0)  # Decelerate to 0 when not pressing W

        display_speed(SCREEN_WIDTH, screen, speed, font)

        # clear the screen
        screen.fill(BLACK)

        draw_heading_arc(screen, heading, SCREEN_WIDTH, font)

        # draw concentric circles around the triangle
        for i in range(4):  # Adjust the range for more or fewer circles
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

        # draw the triangle wireframe (outline)
        pygame.draw.polygon(
            screen, triangle_color, triangle_vertices, width=2
        )  # `width=2` specifies the outline thickness

        lat, lon = update_scene_position(heading, speed, lat, lon)

        aircraft_data = get_aircraft_data(lat, lon, RADIUS_KM)
        if aircraft_data:
            # if aircraft are found, find new long span (user will be moving)
            LON_SPAN = LAT_SPAN * math.cos(
                math.radians(lat)  # use cosine scaling to minimize distortion
            )
            print(json.dumps(aircraft_data, indent=2))
        else:
            print("No data available.")
        # draw aircraft positions as red circles
        for aircraft in aircraft_data:
            altitude = int(aircraft["altitude"])
            # Normalize aircraft position
            screen_x = SCREEN_WIDTH // 2 + int(
                ((aircraft["longitude"] - lon) / LON_SPAN) * (SCREEN_WIDTH // 2)
            )
            screen_y = SCREEN_HEIGHT // 2 - int(
                ((aircraft["latitude"] - lat) / LAT_SPAN) * (SCREEN_HEIGHT // 2)
            )
            # Rotate aircraft position
            rotated_pos = rotate_point(
                (SCREEN_WIDTH // 2, triangle_middle),
                (screen_x, screen_y),
                math.radians(-heading),
            )
            color = altitude_assignment(altitude, current_altitude)
            # Draw aircraft at the rotated position
            pygame.draw.circle(screen, color, rotated_pos, 5)

        # update the display
        pygame.display.flip()
        clock.tick(60)

    # quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
