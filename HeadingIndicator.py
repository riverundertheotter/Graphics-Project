import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def draw_heading_arc(surface, heading, SCREEN_WIDTH, font):
    """Draws a numerical heading arc along the top of the screen"""
    # heading variables
    # arc dimensions and positioning
    ARC_RADIUS = 900  # radius of the arc
    ARC_CENTER_X = SCREEN_WIDTH // 2  # center horizontally
    ARC_CENTER_Y = ARC_RADIUS + 20  # adjusted to place at the top of the screen

    arc_range = 90
    step = 1

    pygame.draw.rect(surface, BLACK, (0, 0, SCREEN_WIDTH, ARC_CENTER_Y + 50))

    for i in range(-arc_range, arc_range + step, step):
        display_heading = (heading + i) % 360
        angle = math.radians(i)
        # calculate the x, y positions on the arc
        x = ARC_CENTER_X + math.sin(angle) * ARC_RADIUS
        y = ARC_CENTER_Y - math.cos(angle) * ARC_RADIUS

        if display_heading % 10 == 0:
            # draw the heading number
            label = font.render(f"{display_heading}", True, WHITE)
            label = pygame.transform.rotate(label, -i)
            surface.blit(
                label, (x - label.get_width() // 2, y - label.get_height() // 2 - 10)
            )

        # draw tick marks
        tick_x = ARC_CENTER_X + math.sin(angle) * (ARC_RADIUS - 20)
        tick_y = ARC_CENTER_Y - math.cos(angle) * (ARC_RADIUS - 20)
        pygame.draw.line(surface, WHITE, (tick_x, tick_y), (x, y), 2)

    # draw the central marker (triangle at the top)
    pygame.draw.polygon(
        surface,
        RED,
        [
            (ARC_CENTER_X, ARC_CENTER_Y - ARC_RADIUS + 10),  # tip of the marker
            (ARC_CENTER_X - 10, ARC_CENTER_Y - ARC_RADIUS + 30),  # left base
            (ARC_CENTER_X + 10, ARC_CENTER_Y - ARC_RADIUS + 30),  # right base
        ],
    )
