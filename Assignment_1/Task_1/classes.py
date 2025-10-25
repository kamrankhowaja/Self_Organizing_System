import pygame
import random
import matplotlib.pyplot as plt
import os
import math

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
        
    def simulate_walk(self, steps, boundary_type='none', radius=100):
        """
        Simulate a random walk with specified boundary conditions
        
        Args:
            steps: Number of steps in this walk
            boundary_type: 'cliff', 'wall', 'periodic', 'one_sided_periodic', or 'none'
            radius: Radius of circular boundary
        
        Returns:
            final_pos: Final position as (x, y) tuple, or None if hit cliff
            step_ended: Step number where walk ended (for cliff), or total steps
        """
        for step in range(steps):
            self.move()
            
            dist = self.get_distance_from_origin()
            
            if dist > radius:
                if boundary_type == 'cliff':
                    # Walk ends at boundary
                    print(f"  → Hit cliff at step {step+1}, distance {dist:.2f}")
                    return (self.pos.x, self.pos.y), step + 1
                
                elif boundary_type == 'wall':
                    # Undo the move that crossed boundary
                    self.pos = pygame.Vector2(self.prev_pos)
                    # No print here as this happens frequently
                
                elif boundary_type == 'periodic':
                    # Appear at opposite side
                    angle = math.atan2(self.pos.y, self.pos.x)
                    new_x = -radius * math.cos(angle)
                    new_y = -radius * math.sin(angle)
                    print(f"  → Crossed boundary at ({self.pos.x:.1f}, {self.pos.y:.1f}), teleported to ({new_x:.1f}, {new_y:.1f})")
                    self.pos.x = new_x
                    self.pos.y = new_y
                
                elif boundary_type == 'one_sided_periodic':
                    # Periodic for positive x, wall for negative x
                    if self.pos.x > 0:
                        angle = math.atan2(self.pos.y, self.pos.x)
                        new_x = -radius * math.cos(angle)
                        new_y = -radius * math.sin(angle)
                        print(f"  → Crossed at positive x ({self.pos.x:.1f}, {self.pos.y:.1f}), teleported to ({new_x:.1f}, {new_y:.1f})")
                        self.pos.x = new_x
                        self.pos.y = new_y
                    else:
                        # Wall behavior for negative x
                        print(f"  → Hit wall at negative x ({self.pos.x:.1f}, {self.pos.y:.1f}), bounced back")
                        self.pos = pygame.Vector2(self.prev_pos)
        
        print(f"  → Completed {steps} steps without ending. Final distance: {self.get_distance_from_origin():.2f}")
        return (self.pos.x, self.pos.y), steps


    def run_boundary_experiment(self, boundary_type, radius, num_runs=10000, steps_per_run=10000, verbose=True):
        """
        Run multiple independent walks and collect endpoints
        
        Args:
            boundary_type: Type of boundary condition
            radius: Radius of circular boundary
            num_runs: Number of independent runs (default 10,000)
            steps_per_run: Steps per run (default 10,000)
            verbose: If True, print detailed progress
        
        Returns:
            endpoints: List of (x, y) tuples of final positions
            statistics: Dict with cliff hits, wall bounces, etc.
        """
        endpoints = []
        cliff_hits = 0
        total_wall_bounces = 0
        total_teleports = 0
        
        print(f"\n{'='*60}")
        print(f"Starting experiment: {boundary_type.upper()} boundary")
        print(f"Radius: {radius}, Runs: {num_runs}, Steps per run: {steps_per_run}")
        print(f"{'='*60}\n")
        
        for run in range(num_runs):
            # Reset to origin
            self.pos = pygame.Vector2(self.origin)
            self.prev_pos = pygame.Vector2(self.origin)
            
            if verbose and run < 5:  # Print details for first 5 runs
                print(f"Run {run + 1}:")
            
            # Run the walk
            final_pos, steps_taken = self.simulate_walk(steps_per_run, boundary_type, radius)
            
            if final_pos is not None:
                endpoints.append(final_pos)
                
                if boundary_type == 'cliff' and steps_taken < steps_per_run:
                    cliff_hits += 1
            
            # Progress indicator every 1000 runs
            if (run + 1) % 1000 == 0:
                print(f"\n[Progress] Completed {run + 1}/{num_runs} runs")
                if boundary_type == 'cliff':
                    hit_rate = (cliff_hits / (run + 1)) * 100
                    print(f"  Cliff hit rate: {hit_rate:.2f}% ({cliff_hits} hits)")
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"EXPERIMENT COMPLETE: {boundary_type.upper()}")
        print(f"{'='*60}")
        print(f"Total runs: {num_runs}")
        print(f"Endpoints collected: {len(endpoints)}")
        
        if boundary_type == 'cliff':
            hit_rate = (cliff_hits / num_runs) * 100
            print(f"Cliff hits: {cliff_hits} ({hit_rate:.2f}%)")
            print(f"Completed walks: {num_runs - cliff_hits} ({100 - hit_rate:.2f}%)")
        
        print(f"{'='*60}\n")
        
        statistics = {
            'cliff_hits': cliff_hits,
            'total_runs': num_runs,
            'endpoints_collected': len(endpoints)
        }
        
        return endpoints, statistics


    def plot_endpoint_histogram(self, endpoints, boundary_type, radius, bins=50):
        """
        Create 2D histogram of walk endpoints
        """
        import numpy as np
        
        x_coords = [ep[0] for ep in endpoints]
        y_coords = [ep[1] for ep in endpoints]
        
        plt.figure(figsize=(10, 10))
        plt.hist2d(x_coords, y_coords, bins=bins, cmap='hot')
        plt.colorbar(label='Number of endpoints')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title(f'Endpoint Distribution - {boundary_type.capitalize()} Boundary (radius={radius})')
        
        # Draw boundary circle
        circle = plt.Circle((0, 0), radius, fill=False, color='blue', linewidth=2)
        plt.gca().add_patch(circle)
        plt.axis('equal')
        plt.grid(True, alpha=0.3)
        
        return plt.gcf()
    
    def plot(self, N, save_plot=False, script_dir=None):
        """
        Plot of N steps
        Simulates N steps and plots distance from origin vs iteration number
        """
        # Simulate walk and get data
        iterations, distances = self.simulate_walk(N)
        
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
            base_dir = script_dir if script_dir else os.getcwd()
            plots_dir = os.path.join(base_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)
            
            filename = os.path.join(plots_dir, f'drunkard_walk_N{N}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {filename}")
            plt.close()
        else:
            plt.show()
            plt.close()

    
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
