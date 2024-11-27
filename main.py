import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

triangle_middle = SCREEN_HEIGHT // 2 + (middle)

# Circle properties
circle_color = WHITE
initial_radius = 100  # Radius of the smallest circle
circle_spacing = 150  # Spacing between circles

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
                SCREEN_HEIGHT // 2 + 115,
            ),  # Circle center at triangle's middle
            radius,
            width=1,  # Outline thickness; use 0 for filled circles
        )

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
