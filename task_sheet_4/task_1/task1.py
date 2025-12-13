import ising_model
import matplotlib.pyplot as plt
import os
os.makedirs("plots", exist_ok=True)

def plot_timeseries(T, t, E, M):
    plt.figure()
    plt.plot(t, E)
    plt.title(f"Energy over time (T={T})")
    plt.xlabel("time step")
    plt.ylabel("E")
    plt.savefig(f"plots/energy_T{T}.png", dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(t, M)
    plt.title(f"Magnetization over time (T={T})")
    plt.xlabel("time step")
    plt.ylabel("M")
    plt.savefig(f"plots/magnetization_T{T}.png", dpi=200, bbox_inches="tight")
    plt.close()

def plot_snapshots(T, snaps):
    for step, grid in snaps.items():
        plt.figure()
        plt.imshow(grid, cmap="gray", vmin=-1, vmax=1, interpolation="nearest")
        plt.title(f"Grid snapshot at step {step} (T={T})")
        plt.colorbar(label="Spin")
        plt.savefig(f"plots/grid_T{T}_step{step}.png", dpi=200, bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    grid_size = 4
    temperature = 2.5
    energy = 1.0

    # Part a 
    model = ising_model.IsingModel(grid_size, temperature, energy, plot=False)

    # Part b
    temperatures = [1.0, 3.0]
    steps = 1000000
    for temp in temperatures:
        print(f"\nSimulating T={temp} for {steps} steps ...")

        model = ising_model.IsingModel(grid_size, temp, energy, plot=False)

        t, E, M, snaps = model.run(
            steps=steps,
            sample_every=1000,
            snapshot_steps=(0, 10_000, 100_000, 1_000_000)
        )

        plot_snapshots(temp, snaps)
        plot_timeseries(temp, t, E, M)  

    print("Simulation complete. Plots saved in 'plots' directory.")