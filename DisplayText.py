WHITE = (255, 255, 255)


def display_speed(surface, speed, font):
    label = font.render(f"{int(speed)} km/h", True, WHITE)
    # position the label at the top-left corner
    surface.blit(label, (1180, 10))


def display_altitude(surface, altitude, font):
    label = font.render(f"{int(altitude)}ft", True, WHITE)
    # position the label at the top-left corner
    surface.blit(label, (10, 10))
