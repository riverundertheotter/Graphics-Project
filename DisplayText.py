WHITE = (255, 255, 255)


def display_speed(width, height, surface, speed, font):
    label = font.render(f"{int(speed)} km/h", True, WHITE)
    # Position the label at the top-left corner
    surface.blit(label, (1180, 10))


def display_altitude(width, height, surface, altitude, font):
    label = font.render(f"{int(altitude)}ft", True, WHITE)
    # Position the label at the top-left corner
    surface.blit(label, (10, 10))
