import pygame
import sys
import math
import threading
import time
from queue import Queue
from OpenSkyHandler import get_aircraft_data
from HeadingIndicator import draw_heading_arc
from DisplayText import display_altitude, display_speed
import HelperFunctions
from InputHandler import handle_input, zoom_input

# no threat
CYAN = (0, 255, 255)
# minimal threat
GREEN = (0, 255, 0)
# potential threat
YELLOW = (255, 230, 0)
# immediate threat
RED = (255, 0, 0)


def draw_aircraft(
    lat,
    lon,
    heading,
    current_altitude,
    screen,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LAT_SPAN,
    aircraft_data,
):
    """Draw aircraft on the screen based on data."""
    if not aircraft_data:
        return

    LON_SPAN = LAT_SPAN * math.cos(math.radians(lat))

    for aircraft in aircraft_data:
        altitude = int(aircraft["altitude"])
        normalized_x = (aircraft["longitude"] - lon) / LON_SPAN
        normalized_y = (aircraft["latitude"] - lat) / LAT_SPAN

        screen_x = SCREEN_WIDTH // 2 + int(normalized_x * (SCREEN_WIDTH // 2))
        screen_y = SCREEN_HEIGHT // 2 + 130 - int(normalized_y * (SCREEN_HEIGHT // 2))

        rotated_pos = HelperFunctions.rotate_point(
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130),
            (screen_x, screen_y),
            math.radians(-heading),
        )

        color = HelperFunctions.altitude_assignment(altitude, current_altitude)
        pygame.draw.circle(screen, color, rotated_pos, 5)


def main():
    RADIUS_KM = 50
    LAT_SPAN = RADIUS_KM / 111

    def get_radius():
        return RADIUS_KM

    def fetch_aircraft_data(lat, lon, radius, data_queue):
        """Background thread to fetch aircraft data periodically."""
        while True:
            aircraft_data = get_aircraft_data(lat, lon, radius)
            data_queue.put(aircraft_data)
            time.sleep(2)  # fetch data every 2 seconds

    # pygame setup
    pygame.init()

    font = pygame.font.SysFont("Consolas", 20)
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    # display colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

    # position
    lat = 32.8968
    lon = -97.0377
    clock = pygame.time.Clock()
    heading = 0
    # aircraft properties
    current_altitude = 0
    speed = 100
    acceleration = 0.5
    max_speed = 900
    deceleration = 0.2
    ascent_rate = 0.5
    descent_rate = 0.8
    flight_ceiling = 32000

    running = True

    trail = []
    trail_max_length = 10000

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Navigation Display")

    # shared queue to hold aircraft data
    data_queue = Queue()
    aircraft_data = []

    # start background thread for fetching data
    threading.Thread(
        target=fetch_aircraft_data,
        args=(lat, lon, get_radius(), data_queue),
        daemon=True,
    ).start()

    while running:
        lat, lon = HelperFunctions.update_scene_position(heading, speed, lat, lon)
        LON_SPAN = LAT_SPAN * math.cos(math.radians(lat))

        # get updated aircraft data from the queue
        while not data_queue.empty():
            aircraft_data = data_queue.get()

        trail.append((lat, lon))
        if len(trail) > trail_max_length:
            trail.pop(0)

        # zoom in/out functionality
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        RADIUS_KM, LAT_SPAN, LON_SPAN = zoom_input(RADIUS_KM, lat, LAT_SPAN, LON_SPAN)

        # get user input and update plane accordingly
        speed, current_altitude, heading = handle_input(
            acceleration,
            max_speed,
            speed,
            current_altitude,
            heading,
            deceleration,
            ascent_rate,
            flight_ceiling,
            descent_rate,
        )

        screen.fill(BLACK)

        draw_heading_arc(screen, heading, SCREEN_WIDTH, font)

        HelperFunctions.draw_circle(
            4, 100, 150, screen, SCREEN_HEIGHT // 2 + 115, WHITE, SCREEN_WIDTH
        )

        # draw triangle
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
                (SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 130),
                (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 130),
            ],
            width=2,
        )

        # calculate rotated trail points
        rotated_trail = []
        for point in trail:
            # the anchor point of the triangle is at (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130)
            normalized_x = (point[1] - lon) / LON_SPAN
            normalized_y = (point[0] - lat) / LAT_SPAN

            screen_x = SCREEN_WIDTH // 2 + int(normalized_x * SCREEN_WIDTH // 2)
            screen_y = SCREEN_HEIGHT // 2 + 130 - int(normalized_y * SCREEN_HEIGHT // 2)

            # calculate the rotated position of the trail points (relative to the bottom of the triangle)
            rotated_point = HelperFunctions.rotate_point(
                (
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2 + 130,
                ),  # bottom of the triangle anchor point
                (
                    screen_x,
                    screen_y,
                ),
                math.radians(-heading),  # rotate based on the aircraft's heading
            )

            # append the rotated point to the trail list
            rotated_trail.append(rotated_point)

        # draw the trail
        if len(rotated_trail) > 1:
            pygame.draw.lines(screen, YELLOW, False, rotated_trail, 2)

        draw_aircraft(
            lat,
            lon,
            heading,
            current_altitude,
            screen,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            LAT_SPAN,
            aircraft_data,
        )

        display_speed(screen, speed, font)
        display_altitude(screen, current_altitude, font)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
