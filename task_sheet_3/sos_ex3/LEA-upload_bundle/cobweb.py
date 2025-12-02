#Script generted by LLM to plot Cobweb diagrams
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- User settings ---
csv_file = "/home/kamran-ali/H-BRS/Semester/Self_organizing_system/Assignments/Self_Organizing_System/boxB_output.csv"   
r = 3.9                        
value_col = "value"          
# ----------------------

# Read CSV
df = pd.read_csv(csv_file)
x = df[value_col].values

# Function for plotting reference (logistic map)
def f(xv):
    return r * xv * (1.0 - xv)

# Plot f(x) and diagonal
xs = np.linspace(0, 1, 500)
plt.figure(figsize=(6,6))
plt.plot(xs, f(xs), label=f"f(x) = {r} x (1-x)")
plt.plot(xs, xs, 'k--', label="y = x")

# Cobweb using the observed sequence: draw vertical then horizontal segments
for i in range(len(x)-1):
    xn = x[i]
    xnext = x[i+1]
    # vertical: (xn, xn) -> (xn, xnext)
    plt.plot([xn, xn], [xn, xnext], color='red')
    # horizontal: (xn, xnext) -> (xnext, xnext)
    plt.plot([xn, xnext], [xnext, xnext], color='red')

# also mark the iterates on the plot
plt.scatter(x[:-1], x[1:], s=20, color='blue', label='(x_n, x_{n+1})')

plt.xlabel('x_n')
plt.ylabel('x_{n+1}')
plt.title('Cobweb plot (observed sequence)')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("cobweb.png", dpi=200)
plt.show()