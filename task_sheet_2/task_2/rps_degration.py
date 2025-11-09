import math
import matplotlib.pyplot as plt


def step(X, g, KP, KD):
    """
    One time step of the analytical rock-paper-scissors model with degradation.

    X  : list/tuple of length 3 with populations [X1, X2, X3]
    g  : list of growth factors [g1, g2, g3]
    KP : effective production area
    KD : effective degradation area
    """
    # Index mapping (0 -> X1, 1 -> X2, 2 -> X3)
    # antibiotics of 0 kill 1, degraded by 2
    # antibiotics of 1 kill 2, degraded by 0
    # antibiotics of 2 kill 0, degraded by 1
    XP_idx = [2, 0, 1]  # producer harmful to [X1, X2, X3]
    XD_idx = [1, 2, 0]  # degrader of that producer's antibiotic

    XP = [X[XP_idx[i]] for i in range(3)]
    XD = [X[XD_idx[i]] for i in range(3)]

    # Pkill_i = e^{-KD * XD} * (1 - e^{-KP * XP})
    Pkill = [
        math.exp(-KD * XD[i]) * (1.0 - math.exp(-KP * XP[i]))
        for i in range(3)
    ]

    # Fitness/weighted growth term for each species
    f = [g[i] * (1.0 - Pkill[i]) for i in range(3)]

    # Denominator: sum_j Xj * fj
    total = sum(X[j] * f[j] for j in range(3))
    if total <= 0:
        # avoid division by zero; if this happens, everything is basically dead
        return [0.0, 0.0, 0.0]

    # Next populations (normalized)
    X_next = [X[i] * f[i] / total for i in range(3)]
    return X_next


def simulate(X0, g, KP, KD, T):
    """
    Simulate for T time steps and return history as a list of [X1,X2,X3].
    """
    X = list(X0)
    history = [X]
    for _ in range(T):
        X = step(X, g, KP, KD)
        history.append(X)
    return history


def plot_history(history, title):
    """
    Plot the three populations over time.
    """
    t_vals = list(range(len(history)))
    X1_vals = [x[0] for x in history]
    X2_vals = [x[1] for x in history]
    X3_vals = [x[2] for x in history]

    plt.figure()
    plt.plot(t_vals, X1_vals, label="X1")
    plt.plot(t_vals, X2_vals, label="X2")
    plt.plot(t_vals, X3_vals, label="X3")
    plt.xlabel("time step t")
    plt.ylabel("population fraction")
    plt.title(title)
    plt.legend()
    plt.tight_layout()


def main():
    # Common parameters
    g = [1.0, 1.0, 1.0]           # growth factors g1, g2, g3
    KP = 0.2                      # effective production area
    X0 = [0.34, 0.33, 0.33]       # initial populations (sum to 1)
    T = 300                       # number of time steps

    # --- (b) Stable coexistence case ---
    KD_stable = 2.0               # effective degradation area (strong degradation)
    history_stable = simulate(X0, g, KP, KD_stable, T)
    plot_history(history_stable,
                 f"Stable coexistence (KP={KP}, KD={KD_stable})")

    # --- (c) Unstable case: change only KD ---
    KD_unstable = 0.2             # weaker degradation
    history_unstable = simulate(X0, g, KP, KD_unstable, T)
    plot_history(history_unstable,
                 f"Unstable dynamics (KP={KP}, KD={KD_unstable})")

    # Show both plots
    plt.show()


if __name__ == "__main__":
    main()
