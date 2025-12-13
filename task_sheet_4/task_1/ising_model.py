import numpy as np
import matplotlib.pyplot as plt

class IsingModel:
    def __init__(self, n, temperature, energy=1.0, plot=False):
        self.n = n
        self.temperature = temperature
        self.energy = energy
        self.spin = np.random.choice([-1, 1], size=(n, n))
        self.grid = self.spin.copy()
        if plot:
            self.ising_model_via_metroplois_algorithm_with_plot()
        else:
            self.ising_model_via_metroplois_algorithm()


    def make_grid(self):
        grid = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                grid[i, j] = self.spin[i, j]
        print("Grid created:")
        print(grid)
        return grid
    
    def visualize_grid(self):
        plt.imshow(self.grid, cmap='gray')
        plt.title(f'Ising Model Grid (T={self.temperature}, J={self.energy})')
        plt.colorbar(label='Spin')
        plt.show()

    def random_node(self):
        i = np.random.randint(0, self.n)
        j = np.random.randint(0, self.n)
        print(f"Randomly selected node: ({i}, {j}) with spin {self.spin[i, j]}")
        return (i, j)

    def delta_E_calc(self, node):
        i, j = node
        n = self.n

        neighbors = [
            ((i + 1) % n, j),     # Down
            ((i - 1) % n, j),     # Up
            (i, (j + 1) % n),     # Right
            (i, (j - 1) % n)      # Left
        ]
        neighbors_spin= [
            self.spin[(i + 1) % n, j],     # Down
            self.spin[(i - 1) % n, j],     # Up
            self.spin[i, (j + 1) % n],     # Right
            self.spin[i, (j - 1) % n]      # Left
        ]
        print(f"Neighbor indices of ({i},{j}): {neighbors}")
        print(f"Neighbor spins: down,up,right,left= {neighbors_spin}")

        delta_e = sum(neighbors_spin) * self.spin[i, j]  * 2 * self.energy
        print(f"Calculated ΔE for node ({i},{j}): {delta_e}")
        return delta_e
    
    def accept_reject(self, delta_e):
        if delta_e <=0:
            print("Energy decrease, accepting spin flip.")
            return True
        else:
            probability = np.exp(-delta_e / self.temperature)
            print(f"Energy increase, acceptance probability: {probability}")
            random_value = np.random.rand()
            print(f"Random value for acceptance check: {random_value}")
            if random_value < probability:
                print("Spin flip accepted based on probability.")
                return True
            else:
                print("Spin flip rejected.")
                return False

    def ising_model_via_metroplois_algorithm(self):

        self.grid = self.make_grid()
        self.visualize_grid()
        r_node = self.random_node()
        delta_e = self.delta_E_calc(r_node)
        status = self.accept_reject(delta_e)
        if status:
            i, j = r_node
            self.spin[i, j] *= -1
            self.grid = self.spin

    def ising_model_via_metroplois_algorithm_with_plot(self):

        self.grid = self.make_grid()
        self.visualize_grid()
        r_node = self.random_node()
        delta_e = self.delta_E_calc(r_node)
        status = self.accept_reject(delta_e)


    def metropolis_step(self):
        node = self.random_node()
        dE = self.delta_E_calc(node)
        if self.accept_reject(dE):
            i, j = node
            self.spin[i, j] *= -1  
        self.grid = self.spin  

    def magnetization(self):
        return int(self.spin.sum())

    def total_energy(self):
        # E = -J * sum_<ij> s_i s_j, count each pair once (right + down)
        s = self.spin
        right = np.roll(s, -1, axis=1)
        down  = np.roll(s, -1, axis=0)
        return float(-self.energy * np.sum(s * (right + down)))

    def run(self, steps=1_000_000, sample_every=1000, snapshot_steps=(0, 10_000, 100_000, 1_000_000)):
        t_hist, E_hist, M_hist = [], [], []
        snaps = {}

        for t in range(steps + 1):
            if t in snapshot_steps:
                snaps[t] = self.spin.copy()

            if t % sample_every == 0:
                t_hist.append(t)
                E_hist.append(self.total_energy())
                M_hist.append(self.magnetization())

            if t < steps:
                self.metropolis_step()

        return np.array(t_hist), np.array(E_hist), np.array(M_hist), snaps


        