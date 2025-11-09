# from bacteria_func import Bacteria, update_populations


# X1 = Bacteria("X1", "A1",
#               effective_production_area=0.1,
#               effective_degradation_area=0.05,
#               growth_rate=1.1,
#               initial_population=100)

# X2 = Bacteria("X2", "A2",
#               effective_production_area=0.1,
#               effective_degradation_area=0.05,
#               growth_rate=1.1,
#               initial_population=100)

# X3 = Bacteria("X3", "A3",
#               effective_production_area=0.1,
#               effective_degradation_area=0.05,
#               growth_rate=1.1,
#               initial_population=100)

# species = [X1, X2, X3]

# for t in range(10):  # 10 time steps
#     # rock–paper–scissors relations:
#     # X2 harms X1, X3 degrades those antibiotics
#     # X3 harms X2, X1 degrades those antibiotics
#     # X1 harms X3, X2 degrades those antibiotics
#     XP = {
#         "X1": X2.X,  # producers harmful to X1 by X2
#         "X2": X3.X,  # producers harmful to X2 by X3
#         "X3": X1.X,  # producers harmful to X3 by X1
#     }
#     XD = {
#         "X1": X3.X,  # degraders of antibiotics harmful to X1 by X3
#         "X2": X1.X,  # degraders of antibiotics harmful to X2 by X1
#         "X3": X2.X,  # degraders of antibiotics harmful to X3 by X2
#     }

#     update_populations(species, XP, XD)

#     print(f"t={t+1}: X1={X1.X:.3f}, X2={X2.X:.3f}, X3={X3.X:.3f}")

from bacteria_func import Bacteria, simulate
import matplotlib.pyplot as plt

# ============================================================================
# Task b) - Find stable parameters
# ============================================================================
print("=" * 70)
print("Task b) - STABLE POPULATIONS")
print("=" * 70)

#I made a case where i kept x1 many, x2 few ad x3 medium to see if they stabilize , rest paramter are constant 

X1_stable = Bacteria("X1", "A1",
                     effective_production_area=0.2,
                     effective_degradation_area=0.05,
                     growth_rate=1.0,
                     initial_population=0.34)

X2_stable = Bacteria("X2", "A2",
                     effective_production_area=0.2,
                     effective_degradation_area=0.05,
                     growth_rate=1.0,
                     initial_population=0.33)

X3_stable = Bacteria("X3", "A3",
                     effective_production_area=0.2,
                     effective_degradation_area=0.05,
                     growth_rate=1.0,
                     initial_population=0.33)


history_stable = simulate(X1_stable, X2_stable, X3_stable, 300)

print(f"Final populations:")
print(f"  X1 = {history_stable['X1'][-1]:.2f}")
print(f"  X2 = {history_stable['X2'][-1]:.2f}")
print(f"  X3 = {history_stable['X3'][-1]:.2f}")

# ============================================================================
# Task c) - Unstable populations by changing KD
# ============================================================================
print("\n" + "=" * 70)
print("Task c) - UNSTABLE POPULATIONS (increased KD)")
print("=" * 70)

X1_unstable = Bacteria("X1", "A1",
                       effective_production_area=0.2,
                       effective_degradation_area=0.15,  # Increased KD!
                       growth_rate=1.0,
                       initial_population=0.34)

X2_unstable = Bacteria("X2", "A2",
                       effective_production_area=00.2,
                       effective_degradation_area=0.15,  # Increased KD!
                       growth_rate=1.0,
                       initial_population=0.33)

X3_unstable = Bacteria("X3", "A3",
                       effective_production_area=0.2,
                       effective_degradation_area=0.15,  # Increased KD!
                       growth_rate=1.0,
                       initial_population=0.33)


history_unstable = simulate(X1_unstable, X2_unstable, X3_unstable, 300)

print(f"Final populations:")
print(f"  X1 = {history_unstable['X1'][-1]:.2f}")
print(f"  X2 = {history_unstable['X2'][-1]:.2f}")
print(f"  X3 = {history_unstable['X3'][-1]:.2f}")

# ============================================================================
# VISUALIZATION 1: Population Dynamics Over Time
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Stable populations
ax1 = axes[0]
ax1.plot(history_stable['X1'], label='X1', linewidth=2)
ax1.plot(history_stable['X2'], label='X2', linewidth=2)
ax1.plot(history_stable['X3'], label='X3', linewidth=2)
ax1.set_xlabel('Time step', fontsize=11)
ax1.set_ylabel('Population (fraction)', fontsize=11)
ax1.set_title('Stable: Population Dynamics\n(KP=0.05, KD=0.05)', fontsize=12)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Unstable populations
ax2 = axes[1]
ax2.plot(history_unstable['X1'], label='X1', linewidth=2)
ax2.plot(history_unstable['X2'], label='X2', linewidth=2)
ax2.plot(history_unstable['X3'], label='X3', linewidth=2)
ax2.set_xlabel('Time step', fontsize=11)
ax2.set_ylabel('Population (fraction)', fontsize=11)
ax2.set_title('Unstable: Population Dynamics\n(KP=0.05, KD=0.15)', fontsize=12)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('bacteria_comprehensive_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================================================
# VISUALIZATION 2: Kill Probabilities (Antibiotic Effects)
# ============================================================================
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))

# Stable kill probabilities
ax3 = axes2[0]
ax3.plot(history_stable['P_kill1'], label='P_kill(X1)', linewidth=2, alpha=0.7)
ax3.plot(history_stable['P_kill2'], label='P_kill(X2)', linewidth=2, alpha=0.7)
ax3.plot(history_stable['P_kill3'], label='P_kill(X3)', linewidth=2, alpha=0.7)
ax3.set_xlabel('Time step', fontsize=11)
ax3.set_ylabel('Kill Probability', fontsize=11)
ax3.set_title('Stable: Antibiotic Pressure\n(Kill Probabilities)', fontsize=12)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_ylim([0, 1])

# Unstable kill probabilities
ax4 = axes2[1]
ax4.plot(history_unstable['P_kill1'], label='P_kill(X1)', linewidth=2, alpha=0.7)
ax4.plot(history_unstable['P_kill2'], label='P_kill(X2)', linewidth=2, alpha=0.7)
ax4.plot(history_unstable['P_kill3'], label='P_kill(X3)', linewidth=2, alpha=0.7)
ax4.set_xlabel('Time step', fontsize=11)
ax4.set_ylabel('Kill Probability', fontsize=11)
ax4.set_title('Unstable: Antibiotic Pressure\n(Kill Probabilities)', fontsize=12)
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)
ax4.set_ylim([0, 1])

plt.tight_layout()
plt.savefig('kill_probabilities.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nVisualization files saved:")
print("  - bacteria_comprehensive_analysis.png")
print("  - kill_probabilities.png")