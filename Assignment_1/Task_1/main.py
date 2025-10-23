import pygame
from classes import Drunkard
import os


# Setup
pygame.init()
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000

# Get the directory where main.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("Drunkard Walk")
clock = pygame.time.Clock()

# Background color (220 in p5.js is gray)
screen.fill((220, 220, 220))

# Create drunkard at (0, 0)
drunkard = Drunkard((0, 0))
drunkard.diameter = 9

N = 0

# Offset for translate(width/2, height/2)
offset = pygame.Vector2(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)


# paused = False
# while N <= 100:

#     for event in pygame.event.get():

#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 paused = not paused
#             if event.key == pygame.K_r:
#                 screen.fill((220, 220, 220))
#                 drunkard = Drunkard((0, 0))
#                 drunkard.diameter = 9
    
#     # Update drunkard with center offset (equivalent to translate)
#     if not paused:
#         drunkard.update(screen, offset)
    
#     pygame.display.flip()
#     clock.tick(60)

#     N += 1



pygame.quit()


# Plot 1000 steps before starting animation
drunkard.plot(N=int(10E3), save_plot=True, script_dir=SCRIPT_DIR) 
drunkard.plot(N=int(10E4), save_plot=True, script_dir=SCRIPT_DIR) 
drunkard.plot(N=int(10E5), save_plot=True, script_dir=SCRIPT_DIR)  
