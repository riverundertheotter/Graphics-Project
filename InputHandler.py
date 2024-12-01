import pygame


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
    radius,
):
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

    # if keys[pygame.K_z]:
    #     radius = max(radius - 5, 5)
    # elif keys[pygame.K_x]:
    #     radius = min(radius + 5, 100)

    return speed, altitude, heading  # , radius
