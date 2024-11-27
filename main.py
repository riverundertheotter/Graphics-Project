import pygame
import sys
import json
import time
import math
from OpenSkyHandler import get_aircraft_data

# using KDFW (Dallas/Fort Worth International Airport) as the center for testing purposes
LAT = 32.8968
LON = -97.0377
RADIUS_KM = 50  # set radius to 50 kilometers


def main():
    # initialize Pygame
    pygame.init()

    # screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

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

        # clear the screen
        screen.fill(BLACK)

        # draw the triangle wireframe (outline)
        pygame.draw.polygon(
            screen, triangle_color, triangle_vertices, width=2
        )  # `width=2` specifies the outline thickness

        # draw concentric circles around the triangle
        for i in range(3):  # Adjust the range for more or fewer circles
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

        aircraft_data = get_aircraft_data(LAT, LON, RADIUS_KM)
        if aircraft_data:
            # if aircraft are found, find new long span (user will be moving)
            LON_SPAN = LAT_SPAN * math.cos(
                math.radians(LAT)  # use cosine scaling to minimize distortion
            )
            print(json.dumps(aircraft_data, indent=2))
        else:
            print("No data available.")
        # draw aircraft positions as red circles
        for aircraft in aircraft_data:
            # normalize latitude and longitude to screen space
            screen_x = SCREEN_WIDTH // 2 + int(
                ((aircraft["longitude"] - LON) / LON_SPAN) * (SCREEN_WIDTH // 2)
            )
            screen_y = SCREEN_HEIGHT // 2 - int(
                ((aircraft["latitude"] - LAT) / LAT_SPAN) * (SCREEN_HEIGHT // 2)
            )

            # draw the aircraft circle
            pygame.draw.circle(screen, RED, (screen_x, screen_y), 5)  # radius = 5
        # update the display
        pygame.display.flip()
        time.sleep(5)  # delay for 5 seconds to allow for API to catch up

    # quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
