import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heading Wheel Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font for direction labels
font = pygame.font.SysFont("Arial", 20)

# Wheel dimensions
WHEEL_RADIUS = 100
CENTER_X, CENTER_Y = WIDTH // 2, 50  # Top center position for the wheel


def draw_heading_wheel(surface, heading):
    """Draws a heading wheel at a given heading angle."""
    wheel_surface = pygame.Surface(
        (WHEEL_RADIUS * 2, WHEEL_RADIUS * 2), pygame.SRCALPHA
    )
    wheel_surface.fill((0, 0, 0, 0))  # Transparent background

    # Draw the outer circle
    pygame.draw.circle(
        wheel_surface, WHITE, (WHEEL_RADIUS, WHEEL_RADIUS), WHEEL_RADIUS, 2
    )

    # Draw cardinal direction labels
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    for i, direction in enumerate(directions):
        angle = math.radians(i * 45)  # 8 directions, 360/8 = 45 degrees
        x = WHEEL_RADIUS + math.cos(angle) * (WHEEL_RADIUS - 20)
        y = WHEEL_RADIUS - math.sin(angle) * (WHEEL_RADIUS - 20)
        label = font.render(direction, True, WHITE)
        surface_x = int(x - label.get_width() / 2)
        surface_y = int(y - label.get_height() / 2)
        wheel_surface.blit(label, (surface_x, surface_y))

    # Draw the heading indicator
    pygame.draw.line(
        wheel_surface, RED, (WHEEL_RADIUS, WHEEL_RADIUS), (WHEEL_RADIUS, 10), 3
    )  # Line pointing upwards

    # Rotate the wheel for the current heading
    rotated_wheel = pygame.transform.rotate(wheel_surface, -heading)
    rect = rotated_wheel.get_rect(center=(CENTER_X, CENTER_Y))

    # Blit the rotated wheel to the main surface
    surface.blit(rotated_wheel, rect.topleft)


# Game loop variables
running = True
clock = pygame.time.Clock()
heading = 0  # Initial heading

# Game loop
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update heading (you can replace this logic with real data)
    heading = (heading + 1) % 360  # Simulate a rotating heading

    # Draw the heading wheel
    draw_heading_wheel(screen, heading)

    # Update the display
    pygame.display.flip()
    clock.tick(30)  # 30 FPS

# Quit Pygame
pygame.quit()
