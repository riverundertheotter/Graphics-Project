import pygame
import sys
import math
from OpenSkyHandler import get_aircraft_data
from HeadingIndicator import draw_heading_arc
from DisplaySpeed import display_speed
import HelperFunctions


RADIUS_KM = 50  # set radius to 50 kilometers
LAT_SPAN = (
    RADIUS_KM / 111
)  # approx. degrees latitude for given radius and location above equator

current_altitude = 0

# no worry
CYAN = (0, 255, 255)
# safe distance
GREEN = (0, 255, 0)
# caution
YELLOW = (255, 230, 0)
# threat
RED = (255, 0, 0)


def main():
    def draw_aircraft():
        aircraft_data = get_aircraft_data(lat, lon, RADIUS_KM)
        if aircraft_data:
            # if aircraft are found, find new long span (user will be moving)
            LON_SPAN = LAT_SPAN * math.cos(
                math.radians(lat)  # use cosine scaling to minimize distortion
            )
            # print(json.dumps(aircraft_data, indent=2))
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
            rotated_pos = HelperFunctions.rotate_point(
                (SCREEN_WIDTH // 2, triangle_middle),
                (screen_x, screen_y),
                math.radians(-heading),
            )
            color = HelperFunctions.altitude_assignment(altitude, current_altitude)
            # Draw aircraft at the rotated position
            pygame.draw.circle(screen, color, rotated_pos, 5)

    # initial position at KDFW
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
    acceleration = 1.0  # Acceleration per frame
    max_speed = 900  # Max speed in km/h
    deceleration = 0.7  # Deceleration per frame

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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # turning input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            heading = (heading + 5) % 360
        elif keys[pygame.K_a]:
            heading = (heading - 5) % 360

        # speed increase/decrease
        if keys[pygame.K_w]:
            speed = min(speed + acceleration, max_speed)  # Increase speed up to max
            HelperFunctions.update_scene_position(heading, speed, lat, lon)
            print(f"Lat: {lat}\nLon: {lon}")
        elif keys[pygame.K_s]:
            speed = max(speed - deceleration, 0)  # Decelerate to 0 when pressing s
            HelperFunctions.update_scene_position(heading, speed, lat, lon)
            print(f"Lat: {lat}\nLon: {lon}")

        display_speed(SCREEN_WIDTH, screen, speed, font)

        # clear the screen
        screen.fill(BLACK)

        # draw heading wheel at top of screen
        draw_heading_arc(screen, heading, SCREEN_WIDTH, font)

        num = 4  # amount of range circles to draw

        HelperFunctions.draw_circle(
            num,
            initial_radius,
            circle_spacing,
            screen,
            triangle_middle,
            circle_color,
            SCREEN_WIDTH,
        )

        # draw the triangle wireframe (outline)
        pygame.draw.polygon(
            screen, triangle_color, triangle_vertices, width=2
        )  # `width=2` specifies the outline thickness

        lat, lon = HelperFunctions.update_scene_position(heading, speed, lat, lon)
        draw_aircraft()

        # update the display
        pygame.display.flip()
        clock.tick(60)

    # quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
