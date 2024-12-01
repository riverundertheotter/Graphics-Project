import pygame
import math


def zoom_input(radius, lat, lat_span, lon_span):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_z]:
        radius = min(radius + 10, 100)
        lat_span = radius / 111
        lon_span = lat_span * math.cos(math.radians(lat))
    elif keys[pygame.K_x]:
        radius = max(radius - 10, 1)
        lat_span = radius / 111
        lon_span = lat_span * math.cos(math.radians(lat))

    return radius, lat_span, lon_span


def handle_input(
    acceleration,
    max_speed,
    speed,
    altitude,
    heading,
    deceleration,
    ascent_rate,
    flight_ceiling,
    descent_rate,
):
    """
    Registers user data and changes airplane attributes accordingly
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        heading = (heading + 1) % 360
    elif keys[pygame.K_a]:
        heading = (heading - 1) % 360

    if keys[pygame.K_w]:
        speed = min(speed + acceleration, max_speed)
    elif keys[pygame.K_s]:
        speed = max(speed - deceleration, 0)

    if keys[pygame.K_LSHIFT]:
        altitude = min(altitude + ascent_rate, flight_ceiling)
    elif keys[pygame.K_LCTRL]:
        altitude = max(altitude - descent_rate, 0)

    return speed, altitude, heading
