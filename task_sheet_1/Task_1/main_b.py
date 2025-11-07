# import pygame
# from classes import Drunkard
# import os


# # Setup
# pygame.init()
# CANVAS_WIDTH = 1000
# CANVAS_HEIGHT = 1000

# # Get the directory where main.py is located
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
# pygame.display.set_caption("Drunkard Walk")
# clock = pygame.time.Clock()

# # Background color (220 in p5.js is gray)
# screen.fill((220, 220, 220))

# # Create drunkard at (0, 0)
# drunkard = Drunkard((0, 0))
# drunkard.diameter = 9

# N = 0

# # Offset for translate(width/2, height/2)
# offset = pygame.Vector2(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)


# # paused = False
# # while N <= 100:

# #     for event in pygame.event.get():

# #         if event.type == pygame.KEYDOWN:
# #             if event.key == pygame.K_SPACE:
# #                 paused = not paused
# #             if event.key == pygame.K_r:
# #                 screen.fill((220, 220, 220))
# #                 drunkard = Drunkard((0, 0))
# #                 drunkard.diameter = 9
    
# #     # Update drunkard with center offset (equivalent to translate)
# #     if not paused:
# #         drunkard.update(screen, offset)
    
# #     pygame.display.flip()
# #     clock.tick(60)

# #     N += 1



# pygame.quit()


# # Plot 1000 steps before starting animation
# #drunkard.plot(N=int(10E3), save_plot=True, script_dir=SCRIPT_DIR) 
# #drunkard.plot(N=int(10E4), save_plot=True, script_dir=SCRIPT_DIR) 
# #drunkard.plot(N=int(10E5), save_plot=True, script_dir=SCRIPT_DIR)  

# # Task 1b

# drunkard.run_boundary_experiment(boundary_type='cliff', radius=300, num_runs=10000, steps_per_run=10000)
# # drunkard.run_boundary_experiment(boundary_type='wall', radius=300, num_runs=10000, steps_per_run=10000)
# # drunkard.run_boundary_experiment(boundary_type='periodic', radius=300, num_runs=10000, steps_per_run=10000)
# # drunkard.run_boundary_experiment(boundary_type='one_sided_periodic', radius=300, num_runs=10000, steps_per_run=10000)


import pygame
from classes import Drunkard
import os

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize pygame (required for Vector2)
pygame.init()

# Create drunkard at origin
drunkard = Drunkard((0, 0))

# Run all scenarios with 10^4 runs and 10^4 steps each
print("Starting boundary experiments...")
results = drunkard.run_all_scenarios(
    radius=100,
    num_runs=10**4,      # 10,000 runs
    steps_per_run=10**4, # 10,000 steps per run
    save_plots=True,
    script_dir=SCRIPT_DIR
)

print("\nExperiment complete! Check the 'plots' directory for results.")

# Optional: Try different parameters
print("\n" + "="*70)
print("Running additional experiments with different parameters...")
print("="*70 + "\n")

# Different radius
drunkard.run_all_scenarios(
    radius=50,
    num_runs=5000,
    steps_per_run=5000,
    save_plots=True,
    script_dir=SCRIPT_DIR
)

# Different step count
drunkard.run_all_scenarios(
    radius=100,
    num_runs=5000,
    steps_per_run=20000,
    save_plots=True,
    script_dir=SCRIPT_DIR
)

pygame.quit()