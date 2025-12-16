# Reference File 
# Dont USE this file

# import numpy as np
# import matplotlib.pyplot as plt
# import os

# class IsingModel:
#     """
#     Ising Model with Metropolis algorithm implementation.
    
#     Parameters:
#     -----------
#     n : int
#         Grid size (n x n)
#     temperature : float
#         Temperature T in the Boltzmann factor
#     J : float
#         Coupling constant (energy scale)
#     """
#     def __init__(self, n, temperature, J=1.0):
#         self.n = n
#         self.temperature = temperature
#         self.J = J
#         # Initialize random spin configuration
#         self.spin = np.random.choice([-1, 1], size=(n, n))
    
#     def delta_energy(self, i, j):
#         """
#         Calculate energy change if we flip spin at position (i, j).
#         With periodic boundary conditions.
#         """
#         n = self.n
#         s = self.spin[i, j]
        
#         # Sum over 4 neighbors with periodic boundary conditions
#         neighbors_sum = (
#             self.spin[(i + 1) % n, j] +
#             self.spin[(i - 1) % n, j] +
#             self.spin[i, (j + 1) % n] +
#             self.spin[i, (j - 1) % n]
#         )
        
#         # ΔE = -2 * J * s_i * Σ(neighbors)
#         # Factor of 2 because flipping changes from +s to -s
#         return 2 * self.J * s * neighbors_sum
    
#     def metropolis_step(self):
#         """
#         Perform one Metropolis algorithm step:
#         1. Choose random node
#         2. Calculate ΔE
#         3. Accept/reject flip based on Metropolis criterion
#         """
#         # Choose random node
#         i = np.random.randint(0, self.n)
#         j = np.random.randint(0, self.n)
        
#         # Calculate energy change
#         dE = self.delta_energy(i, j)
        
#         # Accept/reject flip
#         if dE <= 0:
#             # Always accept if energy decreases
#             self.spin[i, j] *= -1
#         else:
#             # Accept with probability exp(-ΔE/T)
#             if np.random.rand() < np.exp(-dE / self.temperature):
#                 self.spin[i, j] *= -1
    
#     def total_energy(self):
#         """
#         Calculate total energy E = -J * Σ_<ij> s_i * s_j
#         Each pair counted once (only right and down neighbors)
#         """
#         s = self.spin
#         # Calculate interactions with right and down neighbors (periodic BC)
#         right = np.roll(s, -1, axis=1)
#         down = np.roll(s, -1, axis=0)
#         return -self.J * np.sum(s * (right + down))
    
#     def magnetization(self):
#         """Calculate total magnetization M = Σ_i s_i"""
#         return np.sum(self.spin)
    
#     def run(self, steps, sample_every=1000, snapshot_steps=None):
#         """
#         Run Metropolis algorithm for specified number of steps.
        
#         Parameters:
#         -----------
#         steps : int
#             Number of Metropolis steps
#         sample_every : int
#             Sample energy and magnetization every N steps
#         snapshot_steps : tuple or list
#             Steps at which to save grid snapshots
        
#         Returns:
#         --------
#         t_hist : array
#             Time points where observables were sampled
#         E_hist : array
#             Energy at each sample point
#         M_hist : array
#             Magnetization at each sample point
#         snaps : dict
#             Grid snapshots at specified steps
#         """
#         if snapshot_steps is None:
#             snapshot_steps = []
        
#         t_hist, E_hist, M_hist = [], [], []
#         snaps = {}
        
#         for t in range(steps + 1):
#             # Save snapshots
#             if t in snapshot_steps:
#                 snaps[t] = self.spin.copy()
            
#             # Sample observables
#             if t % sample_every == 0:
#                 t_hist.append(t)
#                 E_hist.append(self.total_energy())
#                 M_hist.append(self.magnetization())
            
#             # Perform Metropolis step (except at last iteration)
#             if t < steps:
#                 self.metropolis_step()
        
#         return np.array(t_hist), np.array(E_hist), np.array(M_hist), snaps


# def plot_grid(spin_grid, title, filename):
#     """Plot and save a spin configuration."""
#     plt.figure(figsize=(8, 8))
#     plt.imshow(spin_grid, cmap='RdBu_r', vmin=-1, vmax=1, interpolation='nearest')
#     plt.title(title, fontsize=14)
#     plt.colorbar(label='Spin', ticks=[-1, 1])
#     plt.tight_layout()
#     plt.savefig(filename, dpi=150, bbox_inches='tight')
#     plt.close()


# def plot_timeseries(t, E, M, T, output_dir):
#     """Plot energy and magnetization time series."""
#     # Energy plot
#     plt.figure(figsize=(10, 5))
#     plt.plot(t, E, linewidth=0.5)
#     plt.xlabel('Time step', fontsize=12)
#     plt.ylabel('Energy E', fontsize=12)
#     plt.title(f'Energy vs Time (T = {T:.2f})', fontsize=14)
#     plt.grid(alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(f'{output_dir}/energy_T{T:.2f}.png', dpi=150, bbox_inches='tight')
#     plt.close()
    
#     # Magnetization plot
#     plt.figure(figsize=(10, 5))
#     plt.plot(t, M, linewidth=0.5)
#     plt.xlabel('Time step', fontsize=12)
#     plt.ylabel('Magnetization M', fontsize=12)
#     plt.title(f'Magnetization vs Time (T = {T:.2f})', fontsize=14)
#     plt.grid(alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(f'{output_dir}/magnetization_T{T:.2f}.png', dpi=150, bbox_inches='tight')
#     plt.close()


# # ============================================================================
# # MAIN SIMULATION
# # ============================================================================

# if __name__ == "__main__":
#     # Create output directory
#     os.makedirs("plots", exist_ok=True)
    
#     # Simulation parameters
#     N = 100
#     steps = 1_000_000
#     sample_every = 1000
#     snapshot_steps = [0, 10_000, 100_000, 1_000_000]
    
#     print("=" * 70)
#     print("ISING MODEL SIMULATION")
#     print("=" * 70)
#     print(f"Grid size: {N}x{N}")
#     print(f"Total steps: {steps:,}")
#     print(f"Sampling every: {sample_every} steps")
#     print()
    
#     # Part (a): Demonstrate algorithm at T = 2.5
#     print("PART (a): Demonstrating Metropolis algorithm at T = 2.5")
#     print("-" * 70)
#     T_demo = 2.5
#     model_demo = IsingModel(N, T_demo)
#     t, E, M, snaps = model_demo.run(steps, sample_every, snapshot_steps)
    
#     for step, grid in snaps.items():
#         plot_grid(grid, f'Grid at step {step:,} (T = {T_demo})', 
#                  f'plots/grid_T{T_demo}_step{step}.png')
#     plot_timeseries(t, E, M, T_demo, 'plots')
#     print(f"✓ Completed simulation at T = {T_demo}")
#     print()
    
#     # Part (b): Run at different temperatures
#     print("PART (b): Exploring temperature dependence")
#     print("-" * 70)
#     print("Note: For 2D Ising model, critical temperature Tc ≈ 2.269")
#     print()
    
#     # Temperatures: well below Tc, near Tc, well above Tc
#     temperatures = [1.0, 2.27, 4.0]
#     temp_labels = ["T << Tc", "T ≈ Tc", "T >> Tc"]
    
#     for T, label in zip(temperatures, temp_labels):
#         print(f"Running simulation: {label} (T = {T:.2f})...")
#         model = IsingModel(N, T)
#         t, E, M, snaps = model.run(steps, sample_every, snapshot_steps)
        
#         # Save plots
#         for step, grid in snaps.items():
#             plot_grid(grid, f'{label}: Grid at step {step:,} (T = {T:.2f})', 
#                      f'plots/grid_T{T:.2f}_step{step}.png')
#         plot_timeseries(t, E, M, T, 'plots')
        
#         # Print final statistics
#         final_M = abs(M[-10000:].mean())  # Average over last 10k samples
#         final_E = E[-10000:].mean()
#         print(f"  Final |M|/N² ≈ {final_M/N**2:.4f}")
#         print(f"  Final E/N²  ≈ {final_E/N**2:.4f}")
#         print()
    
#     print("=" * 70)
#     print("SIMULATION COMPLETE")
#     print("=" * 70)
#     print("All plots saved in 'plots/' directory")
#     print()
#     print("KEY OBSERVATIONS:")
#     print("- At T << Tc: System orders (all spins align), high |M|")
#     print("- At T ≈ Tc:  Critical point, large fluctuations, domains form")
#     print("- At T >> Tc: Disorder dominates, M ≈ 0, spins random")
#     print()
#     print("The transition is continuous (2nd order phase transition):")
#     print("Magnetization decreases smoothly through Tc, not abruptly.")