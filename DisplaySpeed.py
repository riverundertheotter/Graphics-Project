WHITE = (255, 255, 255)


def display_speed(width, height, surface, speed, font):
    label = font.render(f"Speed: {int(speed)} km/h", True, WHITE)
    # Position the label at the top-left corner
    surface.blit(label, (10, 10))
