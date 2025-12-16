import ising_model
import matplotlib.pyplot as plt
import os
os.makedirs("plots", exist_ok=True)

""" 
Took some Referemce from : https://www.youtube.com/watch?v=T72QoIOSbzY for understanding ising Model 
and https://rajeshrinet.github.io/blog/2014/ising-model/ to undersatnd the spin nature
"""


def plot_timeseries(T, t, E, M):
    """Plot energy and magnetization time series"""
    # Energy plot
    plt.figure(figsize=(10, 5))
    plt.plot(t, E, linewidth=0.5)
    plt.title(f"Energy over time (T={T})")
    plt.xlabel("time step")
    plt.ylabel("E")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"plots/energy_T{T}.png", dpi=200, bbox_inches="tight")
    plt.close()

    # Magnetization plot
    plt.figure(figsize=(10, 5))
    plt.plot(t, M, linewidth=0.5)
    plt.title(f"Magnetization over time (T={T})")
    plt.xlabel("time step")
    plt.ylabel("M")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"plots/magnetization_T{T}.png", dpi=200, bbox_inches="tight")
    plt.close()

def plot_snapshots(T, snaps):
    """Plot grid snapshots at different time steps"""
    for step, grid in snaps.items():
        plt.figure(figsize=(8, 8))
        plt.imshow(grid, cmap="RdBu_r", vmin=-1, vmax=1, interpolation="nearest")
        plt.title(f"Grid snapshot at step {step:,} (T={T})")
        plt.colorbar(label="Spin", ticks=[-1, 1])
        plt.tight_layout()
        plt.savefig(f"plots/grid_T{T}_step{step}.png", dpi=200, bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    grid_size = 100
    temperature = 2.5
    energy = 1.0

    # Part a 
    model = ising_model.IsingModel(grid_size, temperature, energy, plot=False)
    print(f"Running simulation at T={temperature} for demonstration...")
    t, E, M, snaps = model.run(
        steps=10,
        sample_every=1000,
        snapshot_steps=(0, 5,8)
    )
    
    plot_snapshots(temperature, snaps)
    plot_timeseries(temperature, t, E, M)

    # Part b
    temperatures = [1.0, 3.0]
    steps = 10
    for temp in temperatures:
        print(f"\nSimulating T={temp} for {steps} steps ...")

        model = ising_model.IsingModel(grid_size, temp, energy, plot=False)

        t, E, M, snaps = model.run(
            steps=steps,
            sample_every=1000,
            snapshot_steps=(0, 5)
        )

        plot_snapshots(temp, snaps)
        plot_timeseries(temp, t, E, M)  

    print("Simulation complete. Plots saved in 'plots' directory.")