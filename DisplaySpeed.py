import pygame

WHITE = (255, 255, 255)


def display_speed(width, surface, speed, font):
    label = font.render(f"{speed}", True, WHITE)
    surface.blit(
        label, (width // 2 - label.get_width() // 2, 20)
    )  # Position at top center

    return
