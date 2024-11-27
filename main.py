import pygame
import sys
import json
import time
from OpenSkyHandler import get_aircraft_data


# Using KDFW (Dallas/Fort Worth International Airport) as the center for testing purposes
LAT = 32.8968
LON = -97.0377
RADIUS_KM = 50  # Set radius to 50 kilometers


def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Navigation Display")

    top = 100
    bottom = 130
    width = 10

    # Triangle properties
    triangle_color = WHITE
    triangle_vertices = [
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + top),  # Top vertex
        (SCREEN_WIDTH // 2 - width, SCREEN_HEIGHT // 2 + bottom),  # Bottom left vertex
        (SCREEN_WIDTH // 2 + width, SCREEN_HEIGHT // 2 + bottom),  # Bottom right vertex
    ]

    middle = (top + bottom) / 2
    triangle_middle = SCREEN_HEIGHT // 2 + middle

    # Circle properties
    circle_color = WHITE
    initial_radius = 100  # Radius of the smallest circle
    circle_spacing = 150  # Spacing between circles

    # Screen bounding box for mapping lat/lon to screen space
    LAT_SPAN = RADIUS_KM / 111  # Approx. degrees latitude for given radius
    LON_SPAN = LAT_SPAN / 1.5  # Adjust longitude range (latitude scaling)

    # Running flag
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Draw the triangle wireframe (outline)
        pygame.draw.polygon(
            screen, triangle_color, triangle_vertices, width=2
        )  # `width=2` specifies the outline thickness

        # Draw concentric circles around the triangle
        for i in range(3):  # Adjust the range for more or fewer circles
            radius = initial_radius + i * circle_spacing
            pygame.draw.circle(
                screen,
                circle_color,
                (
                    SCREEN_WIDTH // 2,
                    triangle_middle,
                ),  # Circle center at triangle's middle
                radius,
                width=1,  # Outline thickness; use 0 for filled circles
            )
        aircraft_data = get_aircraft_data(LAT, LON, RADIUS_KM)
        if aircraft_data:
            print(json.dumps(aircraft_data, indent=2))
        else:
            print("No data available.")
        # Draw aircraft positions as red circles
        for aircraft in aircraft_data:
            # Normalize latitude and longitude to screen space
            screen_x = SCREEN_WIDTH // 2 + int(
                ((aircraft["longitude"] - LON) / LON_SPAN) * (SCREEN_WIDTH // 2)
            )
            screen_y = SCREEN_HEIGHT // 2 - int(
                ((aircraft["latitude"] - LAT) / LAT_SPAN) * (SCREEN_HEIGHT // 2)
            )

            # Draw the aircraft circle
            pygame.draw.circle(screen, RED, (screen_x, screen_y), 5)  # Radius=5
        # Update the display
        pygame.display.flip()
        time.sleep(5)

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
