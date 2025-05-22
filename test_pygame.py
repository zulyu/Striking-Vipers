import pygame

# Initialize PyGame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyGame Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with white
    screen.fill(WHITE)
    
    # Draw a black rectangle
    pygame.draw.rect(screen, BLACK, (300, 200, 200, 200))
    
    # Update the display
    pygame.display.flip()

# Quit PyGame
pygame.quit() 