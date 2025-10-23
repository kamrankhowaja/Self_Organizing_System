import pygame
import random
import matplotlib.pyplot as plt
import os

class Drunkard:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.prev_pos = pygame.Vector2(pos)  # make a copy
        self.speed = 1
        self.diameter = 8
        self.origin = pygame.Vector2(pos)  # store origin for distance calculation
    
    def move(self):
        r_x = random.choice([self.speed, -self.speed])
        r_y = random.choice([self.speed, -self.speed])
        self.pos += pygame.Vector2(r_x, r_y)
    
    def get_distance_from_origin(self):
        """Calculate Euclidean distance from origin"""
        return self.pos.distance_to(self.origin)
    
    def show(self, surface, offset):
        pos = self.pos + offset
        pygame.draw.circle(surface, (0, 0, 0), 
                          (int(pos.x), int(pos.y)), 
                          self.diameter // 2)
    
    def plot(self, N, save_plot=False, script_dir=None):
        """
        Plot of N steps
        Simulates N steps and plots distance from origin vs iteration number
        
        Args:
            N: Number of steps to simulate
            save_plot: If True, saves the plot to 'plots' directory instead of showing it
            script_dir: Directory where main.py is located (for saving plots)
        """
        # Save current state
        saved_pos = pygame.Vector2(self.pos)
        saved_prev_pos = pygame.Vector2(self.prev_pos)
        
        # Reset to origin for simulation
        self.pos = pygame.Vector2(self.origin)
        self.prev_pos = pygame.Vector2(self.origin)
        
        # Store data
        iterations = []
        distances = []
        
        # Initial position
        iterations.append(0)
        distances.append(0)
        
        # Simulate N steps
        for i in range(1, N + 1):
            self.move()
            iterations.append(i)
            distances.append(self.get_distance_from_origin())
        
        # Restore original state
        self.pos = saved_pos
        self.prev_pos = saved_prev_pos
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(iterations, distances, linewidth=1.5)
        plt.xlabel('Iteration (N)', fontsize=12)
        plt.ylabel('Distance from Origin', fontsize=12)
        plt.title(f'Drunkard Walk: Distance vs Iterations (N={N})', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_plot:
            # Determine base directory
            if script_dir is None:
                base_dir = os.getcwd()
            else:
                base_dir = script_dir
            
            # Create plots directory if it doesn't exist
            plots_dir = os.path.join(base_dir, 'plots')
            if not os.path.exists(plots_dir):
                os.makedirs(plots_dir)
            
            # Save the plot
            filename = os.path.join(plots_dir, f'drunkard_walk_N{N}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {filename}")
            plt.close()
        else:
            plt.show()
            plt.close()  # Close the figure to free memory
    
    def draw_line(self, surface, offset):
        prev = self.prev_pos + offset
        curr = self.pos + offset
        pygame.draw.line(surface, (0, 0, 0), 
                        (prev.x, prev.y),
                        (curr.x, curr.y), 2)
    
    def update(self, surface, offset):
        self.prev_pos = pygame.Vector2(self.pos)  # store previous FIRST
        self.move()
        self.draw_line(surface, offset)  # draw the segment
        self.show(surface, offset)       # then draw the dot