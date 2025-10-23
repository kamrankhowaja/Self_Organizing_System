import pygame
import random
import matplotlib.pyplot as plt

class Drunkard:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.prev_pos = pygame.Vector2(pos)  # make a copy
        self.speed = 10
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
    
    def plot(self, N):
        """
        Plot of N steps
        Simulates N steps and plots distance from origin vs iteration number
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